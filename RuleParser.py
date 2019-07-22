import ast
from collections import defaultdict
import logging
import re

from Item import ItemFactory
from ItemList import item_table
from Location import Location
from State import State


escaped_items = {}
for item in item_table:
    escaped_items[re.sub(r'[\'()[\]]', '', item.replace(' ', '_'))] = item

event_name = re.compile(r'\w+')


class Rule_AST_Transformer(ast.NodeTransformer):

    def __init__(self, world):
        self.world = world
        self.events = set()
        # map Region -> rule ast string -> item name
        self.replaced_rules = defaultdict(dict)
        # delayed rules need to keep: region name, ast node, event name
        self.delayed_rules = []


    def visit_Name(self, node):
        if node.id in escaped_items:
            return ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id='state', ctx=ast.Load()),
                    attr='has',
                    ctx=ast.Load()),
                args=[ast.Str(escaped_items[node.id])],
                keywords=[])
        elif node.id in self.world.__dict__:
            return ast.Attribute(
                value=ast.Attribute(
                    value=ast.Name(id='state', ctx=ast.Load()),
                    attr='world',
                    ctx=ast.Load()),
                attr=node.id,
                ctx=ast.Load())
        elif node.id in State.__dict__:
            return ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id='state', ctx=ast.Load()),
                    attr=node.id,
                    ctx=ast.Load()),
                args=[],
                keywords=[])
        elif event_name.match(node.id):
            self.events.add(node.id.replace('_', ' '))
            return ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id='state', ctx=ast.Load()),
                    attr='has',
                    ctx=ast.Load()),
                args=[ast.Str(node.id.replace('_', ' '))],
                keywords=[])
        else:
            raise Exception('Parse Error: invalid node name %s' % node.id, self.current_spot.name, ast.parse(node, False))

    def visit_Str(self, node):
        return ast.Call(
            func=ast.Attribute(
                value=ast.Name(id='state', ctx=ast.Load()),
                attr='has',
                ctx=ast.Load()),
            args=[ast.Str(node.s)],
            keywords=[])

    # python 3.8 compatibility: ast walking now uses visit_Constant for Constant subclasses
    # this includes Num, Str, NameConstant, Bytes, and Ellipsis. We only use Str, so...
    visit_Constant = visit_Str

    def visit_Tuple(self, node):
        if len(node.elts) != 2:
            raise Exception('Parse Error: Tuple must have 2 values', self.current_spot.name, ast.parse(node, False))

        item, count = node.elts

        if not isinstance(item, (ast.Name, ast.Str)):
            raise Exception('Parse Error: first value must be an item. Got %s' % item.__class__.__name__, self.current_spot.name, ast.parse(node, False))
        iname = item.id if isinstance(item, ast.Name) else item.s

        if not (isinstance(count, ast.Name) or isinstance(count, ast.Num)):
            raise Exception('Parse Error: second value must be a number. Got %s' % item.__class__.__name__, self.current_spot.name, ast.parse(node, False))

        if isinstance(count, ast.Name):
            count = ast.Attribute(
                value=ast.Attribute(
                    value=ast.Name(id='state', ctx=ast.Load()),
                    attr='world',
                    ctx=ast.Load()),
                attr=count.id,
                ctx=ast.Load())

        if iname in escaped_items:
            iname = escaped_items[iname]

        if iname not in item_table:
            self.events.add(iname)

        return ast.Call(
            func=ast.Attribute(
                value=ast.Name(id='state', ctx=ast.Load()),
                attr='has',
                ctx=ast.Load()),
            args=[ast.Str(iname), count],
            keywords=[])


    def visit_Call(self, node):
        if not isinstance(node.func, ast.Name):
            return node

        if node.func.id in dir(self):
            return getattr(self, node.func.id)(node)

        new_args = []
        for child in node.args:
            if isinstance(child, ast.Name):
                if child.id in self.world.__dict__:
                    child = ast.Attribute(
                        value=ast.Attribute(
                            value=ast.Name(id='state', ctx=ast.Load()),
                            attr='world',
                            ctx=ast.Load()),
                        attr=child.id,
                        ctx=ast.Load())
                elif child.id in escaped_items:
                    child = ast.Str(escaped_items[child.id])
                else:
                    child = ast.Str(child.id.replace('_', ' '))
            elif not isinstance(child, ast.Str):
                child = self.visit(child)
            new_args.append(child)

        return ast.Call(
            func=ast.Attribute(
                value=ast.Name(id='state', ctx=ast.Load()),
                attr=node.func.id,
                ctx=ast.Load()),
            args=new_args,
            keywords=node.keywords)

    def visit_Subscript(self, node):
        if isinstance(node.value, ast.Name):
            return ast.Subscript(
                value=ast.Attribute(
                    value=ast.Attribute(
                        value=ast.Name(id='state', ctx=ast.Load()),
                        attr='world',
                        ctx=ast.Load()),
                    attr=node.value.id,
                    ctx=ast.Load()),
                slice=ast.Index(value=ast.Str(node.slice.value.id.replace('_', ' '))),
                ctx=node.ctx)
        else:
            return node


    def visit_Compare(self, node):
        def escape_or_string(n):
            if isinstance(n, ast.Name) and n.id in escaped_items:
                return ast.Str(escaped_items[n])
            elif not isinstance(n, ast.Str):
                return self.visit(n)
            return n

        node.left = escape_or_string(node.left)
        node.comparators = list(map(escape_or_string, node.comparators))
        node.ops = list(map(self.visit, node.ops))

        return node


    def replace_subrule(self, target, node):
        rule = ast.dump(node, False)
        if rule in self.replaced_rules[target]:
            return self.replaced_rules[target][rule]

        subrule_name = target + ' Subrule %d' % (1 + len(self.replaced_rules[target]))
        # Save the info to be made into a rule later
        self.delayed_rules.append((target, node, subrule_name))
        # Replace the call with a reference to that item
        item_rule = ast.Call(
            func=ast.Attribute(
                value=ast.Name(id='state', ctx=ast.Load()),
                attr='has',
                ctx=ast.Load()),
            args=[ast.Str(subrule_name)],
            keywords=[])
        # Cache the subrule for any others in this region
        # (and reserve the item name in the process)
        self.replaced_rules[target][rule] = item_rule
        return item_rule


    # Requires the target regions have been defined in the world.
    def create_delayed_rules(self):
        for region_name, node, subrule_name in self.delayed_rules:
            region = self.world.get_region(region_name)
            event = Location(subrule_name, type='Event', parent=region)
            event.world = self.world

            self.current_spot = event
            newrule = ast.fix_missing_locations(
                ast.Expression(ast.Lambda(
                    args=ast.arguments(
                        posonlyargs=[],
                        args=[ast.arg(arg='state')],
                        defaults=[],
                        kwonlyargs=[],
                        kw_defaults=[]),
                    # This could, in theory, create further subrules.
                    body=self.visit(node))))

            event.access_rule = eval(compile(newrule, '<string>', 'eval'))
            region.locations.append(event)

            item = ItemFactory(subrule_name, self.world, event=True)
            self.world.push_item(event, item)
            event.locked = True
            self.world.event_items.add(subrule_name)
        # Safeguard in case this is called multiple times per world
        self.delayed_rules.clear()


    ## Handlers for specific internal functions used in the json logic.

    # at(region_name, rule)
    # Creates an internal event at the remote region and depends on it.
    def at(self, node):
        # Cache this under the target (region) name
        if len(node.args) < 2 or not isinstance(node.args[0], ast.Str):
            raise Exception('Parse Error: invalid at() arguments', self.current_spot.name, ast.dump(node, False))
        return self.replace_subrule(node.args[0].s, node.args[1])


    # here(rule)
    # Creates an internal event in the same region and depends on it.
    def here(self, node):
        if not node.args:
            raise Exception('Parse Error: missing here() argument', self.current_spot.name, ast.parse(node, False))
        return self.replace_subrule(
                self.current_spot.parent_region.name,
                node.args[0])


    def parse_spot_rule(self, spot):
        if spot.rule_string is None:
            return lambda state: True

        rule = 'lambda state: ' + spot.rule_string
        rule = rule.split('#')[0]

        self.current_spot = spot
        rule_ast = ast.parse(rule, mode='eval')
        rule_ast = ast.fix_missing_locations(self.visit(rule_ast))
        spot.access_rule = eval(compile(rule_ast, '<string>', 'eval'))
