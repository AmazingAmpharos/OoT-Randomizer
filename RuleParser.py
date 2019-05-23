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

# There's no difference between as_age and as_age_here.
age_subrules = {
    'as_either': None,
    'as_adult': 'is_adult',
    'as_child': 'is_child',
    'as_either_here': None,
    'as_adult_here': 'is_adult',
    'as_child_here': 'is_child',
}


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
            raise Exception('Parse Error: invalid node name %s', node.id)


    def visit_Tuple(self, node):
        if len(node.elts) != 2:
            raise Exception('Parse Error: Tuple must has 2 values')

        item, count = node.elts

        if isinstance(item, ast.Str):
            item = ast.Name(id=item.s, ctx=ast.Load())

        if not isinstance(item, ast.Name):
            raise Exception('Parse Error: first value must be an item. Got %s' % item.__class__.__name__)

        if not (isinstance(count, ast.Name) or isinstance(count, ast.Num)):
            raise Exception('Parse Error: second value must be a number. Got %s' % item.__class__.__name__)

        if isinstance(count, ast.Name):
            count = ast.Attribute(
                value=ast.Attribute(
                    value=ast.Name(id='state', ctx=ast.Load()),
                    attr='world',
                    ctx=ast.Load()),
                attr=count.id,
                ctx=ast.Load())

        if item.id in escaped_items:
            item.id = escaped_items[item.id]

        if not item.id in item_table:
            raise Exception('Parse Error: invalid item name')

        return ast.Call(
            func=ast.Attribute(
                value=ast.Name(id='state', ctx=ast.Load()),
                attr='has',
                ctx=ast.Load()),
            args=[ast.Str(item.id), count],
            keywords=[])


    def visit_Call(self, node):
        if node.func.id in age_subrules:
            return self.replace_subrule(node, self.current_spot.parent_region.name)
        elif node.func.id in dir(self):
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
            else:
                self.visit(child)
            new_args.append(child)

        if isinstance(node.func, ast.Name):
            return ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id='state', ctx=ast.Load()),
                    attr=node.func.id,
                    ctx=ast.Load()),
                args=new_args,
                keywords=node.keywords)
        else:
            return node


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
        if isinstance(node.left, ast.Name):
            if node.left.id in escaped_items:
                node.left = ast.Str(escaped_items[node.left.id])

        if isinstance(node.comparators[0], ast.Name):
            if node.comparators[0].id in escaped_items:
                node.comparators[0] = ast.Str(escaped_items[node.comparators[0].id])

        self.generic_visit(node)
        return node


    def replace_subrule(self, node, target):
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

    def create_subrule(self, body=None, agefunc=None):
        # todo: use rule/spot attributes to check adult_only/child_only/etc.
        if agefunc:
            agefunc = ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id='state', ctx=ast.Load()),
                    attr=agefunc,
                    ctx=ast.Load()),
                args=[],
                keywords=[])

        if body:
            # This could, in theory, create further subrules.
            body = self.visit(body)
            if agefunc:
                if isinstance(body, ast.BoolOp) and isinstance(body.op, ast.And):
                    body.values = [agefunc] + body.values
                else:
                    return ast.BoolOp(op=ast.And(), values=[agefunc, body])
            return body
        elif agefunc:
            return agefunc
        else:
            return ast.NameConstant(True)


    # Requires the target regions have been defined in the world.
    def create_delayed_rules(self):
        for region_name, node, subrule_name in self.delayed_rules:
            region = self.world.get_region(region_name)
            event = Location(subrule_name, type='Event', parent=region)
            event.world = self.world

            self.current_spot = event
            if node.func.id in age_subrules:
                body = self.create_subrule(
                        body=node.args[0] if node.args else None,
                        agefunc=age_subrules[node.func.id])
            elif node.func.id == 'remote':
                body = self.create_subrule(
                        body=node.args[1] if len(node.args) > 1 else None)
            else:
                raise Exception('Parse Error: No such handler for subrule %s' % node.func.id)

            newrule = ast.fix_missing_locations(
                ast.Expression(ast.Lambda(
                    args=ast.arguments(
                        args=[ast.arg(arg='state')],
                        defaults=[],
                        kwonlyargs=[],
                        kw_defaults=[]),
                    body=body)))
            event.access_rule = eval(compile(newrule, '<string>', 'eval'))
            region.locations.append(event)

            item = ItemFactory(subrule_name, self.world, event=True)
            self.world.push_item(event, item)
            event.locked = True
            self.world.event_items.add(subrule_name)
        # Safeguard in case this is called multiple times per world
        self.delayed_rules.clear()


    ## Handlers for specific internal functions used in the json logic.

    # remote(region_name, rule)
    # Creates an internal event at the remote region and depends on it.
    def remote(self, node):
        # Cache this under the target (region) name
        if not node.args or not isinstance(node.args[0], ast.Str):
            raise Exception('Parse Error: invalid remote() arguments')
        return self.replace_subrule(node, node.args[0].s)



    def parse_spot_rule(self, spot):
        if spot.rule_string is None:
            return lambda state: True

        rule = 'lambda state: ' + spot.rule_string
        rule = rule.split('#')[0]

        self.current_spot = spot
        rule_ast = ast.parse(rule, mode='eval')
        rule_ast = ast.fix_missing_locations(self.visit(rule_ast))
        spot.access_rule = eval(compile(rule_ast, '<string>', 'eval'))

