import json
import logging
import re
import random
import uuid

from functools import reduce

from Fill import FillError
from Hints import lineWrap, gossipLocations
from Item import ItemFactory
from ItemPool import random_choices, item_groups, rewardlist, get_junk_item
from LocationList import location_table, location_groups
from Spoiler import HASH_ICONS
from State import State
from version import __version__
from Utils import random_choices
from JSONDump import dump_obj


per_world_keys = (
    'dungeons',
    'trials',
    'item_pool',
    'starting_items',
    'locations',
    ':woth_locations',
    ':barren_regions',
    'gossip_stones',
)


def SimpleRecord(props):
    class Record(object):
        def __init__(self, src_dict=None):
            self.processed = False
            self.update(src_dict, update_all=True)


        def update(self, src_dict, update_all=False):
            if src_dict is None:
                src_dict = {}
            for k, p in props.items():
                if update_all or k in src_dict:
                    setattr(self, k, src_dict.get(k, p))


        def to_dict(self):
            return {k: getattr(self, k) for (k, d) in props.items() if getattr(self, k) != d}


        def __str__(self):
            return dump_obj(self.to_dict())
    return Record


class DungeonRecord(SimpleRecord({'mq': None})):
    def __init__(self, src_dict='random'):
        if src_dict == 'random':
            src_dict = {'mq': None}
        if src_dict == 'mq':
            src_dict = {'mq': True}
        if src_dict == 'vanilla':
            src_dict = {'mq': False}
        super().__init__(src_dict)


    def to_dict(self):
        if self.mq is None:
            return 'random'
        return 'mq' if self.mq else 'vanilla'


class GossipRecord(SimpleRecord({'gossip': None})):
    pass


class ItemPoolRecord(SimpleRecord({'type': 'set', 'count': 1})):
    def __init__(self, src_dict=1):
        if isinstance(src_dict, int):
            src_dict = {'count':src_dict}
        super().__init__(src_dict)


    def to_dict(self):
        if self.type == 'set':
            return self.count
        else:
            return super().to_dict()


    def update(self, src_dict, update_all=False):
        super().update(src_dict, update_all)
        if self.count < 0:
            raise ValueError("Count cannot be negative in a ItemPoolRecord.")
        if self.type not in ['add', 'remove', 'set']:
            raise ValueError("Type must be 'add', 'remove', or 'set' in a ItemPoolRecord.")


class LocationRecord(SimpleRecord({'item': None, 'player': None, 'price': None, 'model': None})):
    def __init__(self, src_dict):
        if isinstance(src_dict, str):
            src_dict = {'item':src_dict}
        super().__init__(src_dict)


    def to_dict(self):
        self_dict = super().to_dict()
        if list(self_dict.keys()) == ['item']:
            return str(self.item)
        else:
            return self_dict


    @staticmethod
    def from_item(item):
        return LocationRecord({
            'item': item.name,
            'player': None if item.location is not None and item.world is item.location.world else (item.world.id + 1),
            'model': item.looks_like_item.name if item.looks_like_item is not None and item.location.has_preview() and can_cloak(item, item.looks_like_item) else None,
            'price': item.price,
        })


class StarterRecord(SimpleRecord({'count': 1})):
    def __init__(self, src_dict=1):
        if isinstance(src_dict, int):
            src_dict = {'count': src_dict}
        super().__init__(src_dict)


    def to_dict(self):
        return self.count


class TrialRecord(SimpleRecord({'active': None})):
    def __init__(self, src_dict='random'):
        if src_dict == 'random':
            src_dict = {'active': None}
        if src_dict == 'active':
            src_dict = {'active': True}
        if src_dict == 'inactive':
            src_dict = {'active': False}
        super().__init__(src_dict)


    def to_dict(self):
        if self.active is None:
            return 'random'
        return 'active' if self.active else 'inactive'



class WorldDistribution(object):
    def __init__(self, distribution, id, src_dict={}):
        self.distribution = distribution
        self.id = id
        self.base_pool = []
        self.update(src_dict, update_all=True)


    def update(self, src_dict, update_all=False):
        update_dict = {        
            'dungeons': {name: DungeonRecord(record) for (name, record) in src_dict.get('dungeons', {}).items()},
            'trials': {name: TrialRecord(record) for (name, record) in src_dict.get('trials', {}).items()},
            'item_pool': {name: ItemPoolRecord(record) for (name, record) in src_dict.get('item_pool', {}).items()},
            'starting_items': {name: StarterRecord(record) for (name, record) in src_dict.get('starting_items', {}).items()},
            'locations': {name: [LocationRecord(rec) for rec in record] if is_pattern(name) else LocationRecord(record) for (name, record) in src_dict.get('locations', {}).items() if not is_output_only(name)},
            'woth_locations': None,
            'barren_regions': None,
            'gossip_stones': {name: [GossipRecord(rec) for rec in record] if is_pattern(name) else GossipRecord(record) for (name, record) in src_dict.get('gossip', {}).items()},
        }

        if update_all:
            self.__dict__.update(update_dict)
        else:
            for k in src_dict:
                if k in update_dict:
                    value = update_dict[k]
                    if self.__dict__.get(k, None) is None:
                        setattr(self, k, value)
                    elif isinstance(value, dict):
                        getattr(self, k).update(value)
                    elif isinstance(value, list):
                        getattr(self, k).extend(value)
                    else:
                        setattr(self, k, None)


    def to_dict(self):
        return {
            'dungeons': {name: record.to_dict() for (name, record) in self.dungeons.items()},
            'trials': {name: record.to_dict() for (name, record) in self.trials.items()},
            'item_pool': {name: record.to_dict() for (name, record) in self.item_pool.items()},
            'starting_items': {name: record.to_dict() for (name, record) in self.starting_items.items()},
            'locations': {name: [rec.to_dict() for rec in record] if is_pattern(name) else record.to_dict() for (name, record) in self.locations.items()},
            ':woth_locations': None if self.woth_locations is None else {name: record.to_dict() for (name, record) in self.woth_locations.items()},
            ':barren_regions': self.barren_regions,
            'gossip_stones': {name: [rec.to_dict() for rec in record] if is_pattern(name) else record.to_dict() for (name, record) in self.gossip_stones.items()},
        }


    def __str__(self):
        return dump_obj(self.to_dict())


    def configure_dungeons(self, world, dungeon_pool):
        dist_num_mq = 0
        for (name, record) in self.dungeons.items():
            if record.mq is not None:
                dungeon_pool.remove(name)
                if record.mq:
                    dist_num_mq += 1
                    world.dungeon_mq[name] = True
        return dist_num_mq


    def configure_trials(self, trial_pool):
        dist_chosen = []
        for (name, record) in self.trials.items():
            if record.active is not None:
                trial_pool.remove(name)
                if record.active:
                    dist_chosen.append(name)
        return dist_chosen


    def pool_remove_item(self, pools, item_name, count, replace_bottle=False, world_id=None, use_base_pool=True):
        removed_items = []

        if is_pattern(item_name):
            base_remove_matcher = pattern_matcher(item_name, item_groups)
        else:
            base_remove_matcher = lambda item: item_name == item
        remove_matcher = lambda item: base_remove_matcher(item) and ((item in self.base_pool) ^ (not use_base_pool))

        if world_id is None:
            predicate = remove_matcher
        else:
            predicate = lambda item: item.world.id == world_id and remove_matcher(item.name)

        for i in range(count):
            removed_item = pull_random_element(pools, predicate)
            if removed_item is None:
                if not use_base_pool:
                    raise KeyError('No items matching "%s" or all of them have already been removed' % (item_name))
                else:
                    removed_items.extend(self.pool_remove_item(pools, item_name, count - i, world_id=world_id, use_base_pool=False))
                    break
            if use_base_pool:
                if world_id is None:
                    self.base_pool.remove(removed_item)
                else:
                    self.base_pool.remove(removed_item.name)
            removed_items.append(removed_item)

        for item in removed_items:
            if replace_bottle:
                bottle_matcher = pattern_matcher("#Bottle", item_groups)
                trade_matcher  = pattern_matcher("#AdultTrade", item_groups)
                if bottle_matcher(item):
                    self.pool_add_item(pools[0], "#Bottle", 1)
                if trade_matcher(item):
                    self.pool_add_item(pools[0], "#AdultTrade", 1)

        return removed_items


    def pool_add_item(self, pool, item_name, count, replace_bottle=False):
        added_items = []
        if item_name == '#Junk':
            added_items = get_junk_item(count)
        elif is_pattern(item_name):
            add_matcher = pattern_matcher(item_name, item_groups)
            candidates = [item for item in pool if add_matcher(item)]
            added_items = random_choices(candidates, k=count)
        else:
            added_items = [item_name] * count

        for item in added_items:
            if replace_bottle:
                bottle_matcher = pattern_matcher("#Bottle", item_groups)
                trade_matcher  = pattern_matcher("#AdultTrade", item_groups)
                if bottle_matcher(item):
                    self.pool_remove_item([pool], "#Bottle", 1)
                if trade_matcher(item):
                    self.pool_remove_item([pool], "#AdultTrade", 1)
            pool.append(item)


    def alter_pool(self, world, pool):
        self.base_pool = list(pool)
        pool_size = len(pool)

        for item_name, record in self.item_pool.items():
            if record.type == 'add':
                self.pool_add_item(pool, item_name, record.count)
            if record.type == 'remove':
                self.pool_remove_item([pool], item_name, record.count)

        for item_name, record in self.item_pool.items():
            if record.type == 'set':
                if item_name == '#Junk':
                    raise ValueError('#Junk item group cannot have a set number of items')
                elif is_pattern(item_name):
                    predicate = pattern_matcher(item_name, item_groups)
                else:
                    predicate = lambda item: item_name == item
                pool_match = [item for item in pool if predicate(item)]
                add_count = record.count - len(pool_match)
                if add_count > 0:
                    self.pool_add_item(pool, item_name, add_count, replace_bottle=True)
                else:
                    self.pool_remove_item([pool], item_name, -add_count, replace_bottle=True)

        junk_to_add = pool_size - len(pool)
        if junk_to_add > 0:
            self.pool_add_item(pool, "#Junk", junk_to_add)
        else:
            self.pool_remove_item([pool], "#Junk", -junk_to_add)


    def collect_starters(self, state):
        for (name, record) in self.starting_items.items():
            for _ in range(record.count):
                try:
                    item = ItemFactory("Bottle" if name == "Bottle with Milk (Half)" else name)
                except KeyError:
                    continue
                state.collect(item)


    def fill_bosses(self, world, prize_locs, prizepool):
        count = 0
        for (name, record) in pattern_dict_items(self.locations):
            boss = pull_item_or_location([prize_locs], world, name, groups=location_groups)
            if boss is None:
                continue
            if record.player is not None and (record.player - 1) != self.id:
                raise RuntimeError('A boss can only give rewards in its own world')
            reward = pull_item_or_location([prizepool], world, record.item, groups=item_groups)
            if reward is None:
                raise RuntimeError('Reward unknown or already placed in world %d: %s' % (world.id + 1, record.item))
            count += 1
            world.push_item(boss, reward, True)
            record.processed = True
        return count


    def fill(self, window, worlds, location_pools, item_pools):
        world = worlds[self.id]
        for (name, record) in pattern_dict_items(self.locations):
            if record.processed:
                continue
            if record.item is None:
                continue

            player_id = self.id if record.player is None else record.player - 1

            location = pull_item_or_location(location_pools, world, name, groups=location_groups)
            if location is None:
                raise RuntimeError('Location unknown or already filled in world %d: %s' % (self.id + 1, name))

            try:
                item = self.pool_remove_item(item_pools, record.item, 1, world_id=player_id)[0]
            except KeyError:
                try:
                    self.pool_remove_item(item_pools, "#Junk", 1, world_id=player_id)[0]
                    item = ItemFactory(record.item, worlds[player_id])
                except KeyError:
                    raise RuntimeError('Too many items were added to world %d, and not enough junk is available to be removed.' % (self.id + 1))

            if record.price is not None:
                item.price = record.price
            location.world.push_item(location, item, True)
            if item.advancement:
                states_after = State.get_states_with_items([world.state for world in worlds], reduce(lambda a, b: a + b, item_pools))
                if not State.can_beat_game(states_after, True):
                    raise FillError('%s in world %d is not reachable without %s in world %d!' % (location.name, self.id + 1, item.name, player_world.id + 1))
            window.fillcount += 1
            window.update_progress(5 + ((window.fillcount / window.locationcount) * 30))


    def cloak(self, world, location_pools, model_pools):
        for (name, record) in pattern_dict_items(self.locations):
            if record.processed:
                continue
            if record.model is None:
                continue
            location = pull_item_or_location(location_pools, world, name, groups=location_groups)
            if location is None:
                raise RuntimeError('Location unknown or already cloaked in world %d: %s' % (self.id + 1, name))
            model = pull_item_or_location(model_pools, world, record.model, remove=False, groups=item_groups)
            if model is None:
                raise RuntimeError('Unknown model in world %d: %s' % (self.id + 1, record.model))
            if can_cloak(location.item, model):
                location.item.looks_like_item = model


    def configure_gossip(self, spoiler, stoneIDs):
        for (name, record) in pattern_dict_items(self.gossip_stones):
            if is_pattern(name):
                matcher = pattern_matcher(name)
                stoneID = pull_random_element([stoneIDs], lambda id: matcher(gossipLocations[id].name))
            else:
                stoneID = pull_first_element([stoneIDs], lambda id: gossipLocations[id].name == name)
            if stoneID is None:
                raise RuntimeError('Gossip stone unknown or already assigned in world %d: %s' % (self.id + 1, name))
            spoiler.hints[self.id][stoneID] = lineWrap(record.gossip)


    def patch_save(self, save_context):
        for (name, record) in self.starting_items.items():
            if record.count == 0:
                continue
            save_context.give_item(name, record.count)


class Distribution(object):
    def __init__(self, settings, src_dict={}):
        self.settings = settings
        self.world_dists = [WorldDistribution(self, id) for id in range(settings.world_count)]
        self.update(src_dict, update_all=True)


    def fill(self, window, worlds, location_pools, item_pools):
        max_states = State.get_states_with_items([world.state for world in worlds], reduce(lambda a, b: a + b, item_pools))
        if not State.can_beat_game(max_states, True):
            raise FillError('Item pool does not contain items required to beat game!')

        for world_dist in self.world_dists:
            world_dist.fill(window, worlds, location_pools, item_pools)


    def cloak(self, worlds, location_pools, model_pools):
        for world_dist in self.world_dists:
            world_dist.cloak(worlds[world_dist.id], location_pools, model_pools)


    def update(self, src_dict, update_all=False):
        update_dict = {        
            'file_hash': (src_dict.get('file_hash', []) + [None, None, None, None, None])[0:5],
            'playthrough': None,
        }

        if update_all:
            self.__dict__.update(update_dict)
            for world in self.world_dists:
                world.update({}, update_all=True)
        else:
            for k in src_dict:
                setattr(self, k, update_dict[k])

        for k in per_world_keys:
            if k in src_dict:
                for world_id, world in enumerate(self.world_dists):
                    world_key = 'World %d' % (world_id + 1)
                    if world_key in src_dict[k]:
                        world.update({k: src_dict[k][world_key]})
                        del src_dict[k][world_key]
                for world in self.world_dists:
                    if src_dict[k]:
                        world.update({k: src_dict[k]})


    def to_dict(self, include_output=True):
        self_dict = {
            ':version': __version__,
            ':seed': self.settings.seed,
            'file_hash': self.file_hash,
            ':settings_string': self.settings.settings_string,
            ':settings': self.settings.to_dict(),
            ':playthrough': None if self.playthrough is None else 
                {sphere_nr: {name: record.to_dict() for name, record in sphere.items()} 
                    for (sphere_nr, sphere) in self.playthrough.items()},
        }

        world_dist_dicts = [world_dist.to_dict() for world_dist in self.world_dists]
        if self.settings.world_count > 1:
            for k in per_world_keys:
                for id, world_dist_dict in enumerate(world_dist_dicts):
                    self_dict[k]['World %d' % (id + 1)] = world_dist_dict[k]
        else:
            self_dict.update({k: world_dist_dicts[0][k] for k in per_world_keys})

        if not include_output:
            strip_output_only(self_dict)
        return self_dict


    def to_str(self, include_output_only=True):
        return dump_obj(self.to_dict(include_output_only))


    def __str__(self):
        return dump_obj(self.to_dict())


    @staticmethod
    def from_spoiler(spoiler):
        dist = Distribution(spoiler.settings)

        dist.file_hash = [HASH_ICONS[icon] for icon in spoiler.file_hash]

        for world in spoiler.worlds:
            world_dist = dist.world_dists[world.id]
            world.distribution = world_dist
            world_dist.dungeons = {dung: DungeonRecord({ 'mq': world.dungeon_mq[dung] }) for dung in world.dungeon_mq}
            world_dist.trials = {trial: TrialRecord({ 'active': not world.skipped_trials[trial] }) for trial in world.skipped_trials}
            world_dist.locations = {loc: LocationRecord.from_item(item) for (loc, item) in spoiler.locations[world.id].items()}
            world_dist.woth_locations = {loc.name: LocationRecord.from_item(loc.item) for loc in spoiler.required_locations[world.id]}
            world_dist.barren_regions = [*world.empty_areas]
            world_dist.gossip_stones = {gossipLocations[loc].name: GossipRecord({ 'gossip': spoiler.hints[world.id][loc] }) for loc in spoiler.hints[world.id]}
            world_dist.item_pool = {}

        for world in spoiler.worlds:
            for (_, item) in spoiler.locations[world.id].items():
                if item.dungeonitem or item.type == 'Event':
                    continue
                player_dist = item.world.distribution
                if item.name in player_dist.item_pool:
                    player_dist.item_pool[item.name].count += 1
                else:
                    player_dist.item_pool[item.name] = ItemPoolRecord()

        dist.playthrough = {}
        for (sphere_nr, sphere) in spoiler.playthrough.items():
            loc_rec_sphere = {}
            dist.playthrough[sphere_nr] = loc_rec_sphere
            for location in sphere:
                if spoiler.settings.world_count > 1:
                    location_key = '%s [W%d]' % (location.name, location.world.id + 1)
                else:
                    location_key = location.name

                loc_rec_sphere[location_key] = LocationRecord.from_item(location.item)

        return dist


    @staticmethod
    def from_file(settings, filename):
        with open(filename) as infile:
            src_dict = json.load(infile)
        return Distribution(settings, src_dict)


    def to_file(self, filename):
        json = str(self)
        with open(filename, 'w') as outfile:
            outfile.write(json)


def strip_output_only(obj):
    if isinstance(obj, list):
        for elem in obj:
            strip_output_only(elem)
    elif isinstance(obj, dict):
        output_only_keys = [key for key in obj if is_output_only(key)]
        for key in output_only_keys:
            del obj[key]
        for elem in obj.values():
            strip_output_only(elem)


def can_cloak(actual_item, model):
    return actual_item.index == 0x7C # Ice Trap


def is_output_only(pattern):
    return pattern.startswith(':')


def is_pattern(pattern):
    return pattern.startswith('!') or pattern.startswith('*') or pattern.startswith('#') or pattern.endswith('*')


def pattern_matcher(pattern, groups={}):
    invert = pattern.startswith('!')
    if invert:
        pattern = pattern[1:]
    if pattern.startswith('#'):
        group = groups[pattern[1:]]
        return lambda s: invert != (s in group)
    wildcard_begin = pattern.startswith('*')
    if wildcard_begin:
        pattern = pattern[1:]
    wildcard_end = pattern.endswith('*')
    if wildcard_end:
        pattern = pattern[:-1]
        if wildcard_begin:
            return lambda s: invert != (pattern in s)
        else:
            return lambda s: invert != s.startswith(pattern)
    else:
        if wildcard_begin:
            return lambda s: invert != s.endswith(pattern)
        else:
            return lambda s: invert != (s == pattern)


def pattern_dict_items(pattern_dict):
    for (key, value) in pattern_dict.items():
        if is_pattern(key):
            for subvalue in value:
                yield (key, subvalue)
        else:
            yield (key, value)


def pull_element(pools, predicate=lambda k:True, first=True, remove=True):
    if first:
        return pull_first_element(pools, predicate, remove)
    else:
        return pull_random_element(pools, predicate, remove)


def pull_first_element(pools, predicate=lambda k:True, remove=True):
    for pool in pools:
        for element in pool:
            if predicate(element):
                if remove:
                    pool.remove(element)
                return element
    return None


def pull_random_element(pools, predicate=lambda k:True, remove=True):
    candidates = [(element, pool) for pool in pools for element in pool if predicate(element)]
    if len(candidates) == 0:
        return None
    element, pool = random.choice(candidates)
    if remove:
        pool.remove(element)
    return element


# Finds and removes (unless told not to do so) an item or location matching the criteria from a list of pools.
def pull_item_or_location(pools, world, name, remove=True, groups={}):
    if is_pattern(name):
        matcher = pattern_matcher(name, groups)
        return pull_random_element(pools, lambda e: e.world is world and matcher(e.name), remove)
    else:
        return pull_first_element(pools, lambda e: e.world is world and e.name == name, remove)