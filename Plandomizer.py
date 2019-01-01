import json
import logging
import random

from functools import reduce

from Fill import FillError
from Hints import lineWrap, gossipLocations
from Item import ItemFactory
from ItemPool import item_groups, item_generators
from LocationList import location_table, location_groups
from Spoiler import HASH_ICONS
from State import State


per_world_keys = (
    'dungeons',
    'trials',
    'item_count_imbalances',
    'item_pools',
    'item_replacements',
    'starting_items',
    'logic_ignored_items',
    'locations',
    'gossip',
)


def SimpleRecord(props):
    class Record(object):
        def __init__(self, src_dict=None):
            self.processed = False
            self.update(src_dict)


        def update(self, src_dict):
            if src_dict is None:
                src_dict = {}
            for (k, d) in props.items():
                setattr(self, k, src_dict.get(k, d))


        def to_dict(self):
            return {k: getattr(self, k) for (k, d) in props.items() if getattr(self, k) != d}
    return Record


class DungeonRecord(SimpleRecord({'mq': None})):
    pass


class GossipRecord(SimpleRecord({'gossip': None})):
    pass


class ItemPoolRecord(SimpleRecord({'count': 1})):
    pass


class ItemReplacementRecord(SimpleRecord({'add': None, 'remove': None, 'count': 1})):
    pass


class LocationRecord(SimpleRecord({'item': None, 'player': None, 'price': None, 'model': None, 'extra': None})):
    pass


class LogicIgnoredItemRecord(SimpleRecord({'count': 1})):
    pass


class StarterRecord(SimpleRecord({'count': 1, 'extra': None})):
    pass


class TrialRecord(SimpleRecord({'skip': None})):
    pass


class WorldDistribution(object):
    def __init__(self, distribution, id, src_dict={}):
        self.distribution = distribution
        self.id = id
        self.update(src_dict)


    def update(self, src_dict):
        self.dungeons = {name: DungeonRecord(record) for (name, record) in src_dict.get('dungeons', {}).items()}
        self.trials = {name: TrialRecord(record) for (name, record) in src_dict.get('trials', {}).items()}
        self.item_count_imbalance = src_dict.get('item_count_imbalances', 0)
        item_pool = src_dict.get('item_pools', None)
        self.item_pool = None if item_pool is None else {name: ItemPoolRecord(record) for (name, record) in item_pool.items()}
        self.item_replacements = [ItemReplacementRecord(record) for record in src_dict.get('item_replacements', [])]
        self.starting_items = {name: StarterRecord(record) for (name, record) in src_dict.get('starting_items', {}).items()}
        self.logic_ignored_items = {name: LogicIgnoredItemRecord(record) for (name, record) in src_dict.get('logic_ignored_items', {}).items()}
        self.locations = {name: [LocationRecord(rec) for rec in record] if is_pattern(name) else LocationRecord(record) for (name, record) in src_dict.get('locations', {}).items()}
        self.gossip = {name: [GossipRecord(rec) for rec in record] if is_pattern(name) else GossipRecord(record) for (name, record) in src_dict.get('gossip', {}).items()}


    def to_dict(self):
        return {
            'dungeons': {name: record.to_dict() for (name, record) in self.dungeons.items()},
            'trials': {name: record.to_dict() for (name, record) in self.trials.items()},
            'item_count_imbalances': self.item_count_imbalance,
            'item_pools': None if self.item_pool is None else {name: record.to_dict() for (name, record) in self.item_pool.items()},
            'item_replacements': [record.to_dict() for record in self.item_replacements],
            'starting_items': {name: record.to_dict() for (name, record) in self.starting_items.items()},
            'logic_ignored_items': {name: record.to_dict() for (name, record) in self.logic_ignored_items.items()},
            'locations': {name: [rec.to_dict() for rec in record] if is_pattern(name) else record.to_dict() for (name, record) in self.locations.items()},
            'gossip': {name: [rec.to_dict() for rec in record] if is_pattern(name) else record.to_dict() for (name, record) in self.gossip.items()},
        }


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
            if record.skip is not None:
                trial_pool.remove(name)
                if not record.skip:
                    dist_chosen.append(name)
        return dist_chosen


    def get_all_item_replacements(self):
        yield from self.item_replacements
        add_items = []
        remove_items = []
        for (_, record) in pattern_dict_items(self.locations):
            if record.extra if record.extra is not None else self.distribution.locations_default_extra:
                add_items.append(record.item)
        for (name, record) in self.starting_items.items():
            if not (record.extra if record.extra is not None else self.distribution.starting_default_extra):
                remove_items.extend([name] * record.count)
        if len(remove_items) > len(add_items):
            add_items.extend(['#Junk'] * (len(remove_items) - len(add_items)))
        elif len(add_items) > len(remove_items):
            remove_items.extend(['#Junk'] * (len(add_items) - len(remove_items)))
        yield from (ItemReplacementRecord({ 'add': add_item, 'remove': remove_item }) for (add_item, remove_item) in zip(add_items, remove_items))


    def alter_pool(self, pool):
        pool_size = len(pool) + self.item_count_imbalance
        junk_matcher = pattern_matcher('#Junk', item_groups)
        junk_to_remove = 0
        if self.item_pool is not None:
            del pool[:]
            for (name, record) in self.item_pool.items():
                if name.startswith('#'):
                    generator = item_generators[name[1:]]
                    for _ in range(record.count):
                        pool.append(generator())
                else:
                    pool.extend([name] * record.count)
            if len(pool) > pool_size:
                junk_to_remove = len(pool) - pool_size
            else:
                junk_generator = item_generators['Junk']
                for _ in range(pool_size - len(pool)):
                    pool.append(junk_generator())
        else:
            if self.item_count_imbalance > 0:
                junk_generator = item_generators['Junk']
                for _ in range(self.item_count_imbalance):
                    pool.append(junk_generator())
            elif self.item_count_imbalance < 0:
                candidates = [item for item in pool if junk_matcher(item)]
                junk_to_remove = -self.item_count_imbalance - len(candidates)
                if junk_to_remove < 0:
                    junk_to_remove = 0
                    random.shuffle(candidates)
                    for i in range(-self.item_count_imbalance):
                        pool.remove(candidates[i])
                else:
                    for item in candidates:
                        pool.remove(item)

        dist_extension = []

        for record in self.get_all_item_replacements():
            remove_item = record.remove
            add_item = record.add
            if remove_item is None:
                remove_item = '#Junk'
            if is_pattern(remove_item):
                remove_matcher = pattern_matcher(remove_item, item_groups)
            else:
                remove_matcher = None
            if add_item is None:
                add_item = '#Junk'
            count = record.count
            replace_all = count == "all"
            if replace_all:
                count = len(pool) # Upper bound of the number of iterations
            for _ in range(count):
                if remove_matcher is not None:
                    candidates = [item for item in pool if remove_matcher(item)]
                    if len(candidates) == 0:
                        if replace_all:
                            break
                        raise RuntimeError('No items matching "%s" in world %d, or all of them have already been replaced' % (remove_item, self.id))
                    pool.remove(candidates[random.randint(0, len(candidates) - 1)])
                else:
                    if remove_item not in pool:
                        if replace_all:
                            break
                        raise RuntimeError('No items matching "%s" in world %d, or all of them have already been replaced' % (remove_item, self.id))
                    pool.remove(remove_item)
                if add_item.startswith('#'):
                    dist_extension.append(item_generators[add_item[1:]]())
                else:
                    dist_extension.append(add_item)

        pool.extend(dist_extension)

        if junk_to_remove > 0:
            candidates = [item for item in pool if junk_matcher(item)]
            if junk_to_remove > len(candidates):
                raise RuntimeError('Item pool too big for world %d and not enough junk to remove, expecting %d items, and cannot get below %d!' % (self.id, pool_size, len(pool) - len(candidates)))
            elif junk_to_remove < len(candidates):
                random.shuffle(candidates)
                for i in range(junk_to_remove):
                    pool.remove(candidates[i])
            else:
                for item in candidates:
                    pool.remove(item)


    def collect_starters(self, state):
        for (name, record) in self.starting_items.items():
            for _ in range(record.count):
                state.collect(ItemFactory(name))

        for (name, record) in self.logic_ignored_items.items():
            for _ in range(record.count):
                state.collect(ItemFactory(name))


    def fill_bosses(self, world, prize_locs, prizepool):
        count = 0
        for (name, record) in pattern_dict_items(self.locations):
            boss = pull_item_or_location([prize_locs], world, name, groups=location_groups)
            if boss is None:
                continue
            if record.player is not None and record.player != self.id:
                raise RuntimeError('A boss can only give rewards in its own world')
            reward = pull_item_or_location([prizepool], world, record.item, groups=item_groups)
            if reward is None:
                raise RuntimeError('Reward unknown or already placed in world %d: %s' % (world.id, record.item))
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
            player_world = worlds[record.player] if record.player is not None else world
            location = pull_item_or_location(location_pools, world, name, groups=location_groups)
            if location is None:
                raise RuntimeError('Location unknown or already filled in world %d: %s' % (self.id, name))
            item = pull_item_or_location(item_pools, player_world, record.item, groups=item_groups)
            if item is None:
                raise RuntimeError('Item unknown or already placed in world %d: %s' % (player_world.id, record.item))
            if record.price is not None:
                item.special['price'] = record.price
                item.price = record.price
            location.world.push_item(location, item, True)
            if item.advancement:
                states_after = State.get_states_with_items([world.state for world in worlds], reduce(lambda a, b: a + b, item_pools))
                if not State.can_beat_game(states_after, True):
                    raise FillError('%s in world %d is not reachable without %s in world %d!' % (location.name, self.id, item.name, player_world.id))
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
                raise RuntimeError('Location unknown or already cloaked in world %d: %s' % (self.id, name))
            model = pull_item_or_location(model_pools, world, record.model, remove=False, groups=item_groups)
            if model is None:
                raise RuntimeError('Unknown model in world %d: %s' % (self.id, record.model))
            location.item.looks_like_item = model


    def configure_gossip(self, spoiler, stoneIDs):
        for (name, record) in pattern_dict_items(self.gossip):
            if is_pattern(name):
                matcher = pattern_matcher(name)
                stoneID = pull_random_element([stoneIDs], lambda id: matcher(gossipLocations[id].name))
            else:
                stoneID = pull_first_element([stoneIDs], lambda id: gossipLocations[id].name == name)
            if stoneID is None:
                raise RuntimeError('Gossip stone unknown or already assigned in world %d: %s' % (self.id, name))
            spoiler.hints[self.id][stoneID] = lineWrap(record.gossip)


    def patch_save(self, write_byte_to_save, write_bits_to_save):
        if len(self.starting_items) > 0:
            raise NotImplementedError('starting_items is not implemented at the moment!')


class Distribution(object):
    def __init__(self, src_dict={}):
        self.worlds = []
        self.update(src_dict)


    def for_world(self, world_id):
        while world_id >= len(self.worlds):
            self.worlds.append(WorldDistribution(self, len(self.worlds)))
        return self.worlds[world_id]


    def fill(self, window, worlds, location_pools, item_pools):
        states_before = State.get_states_with_items([world.state for world in worlds], reduce(lambda a, b: a + b, item_pools))
        if not State.can_beat_game(states_before, True):
            raise FillError('Item pool does not contain items required to beat game!')

        for world_dist in self.worlds:
            world_dist.fill(window, worlds, location_pools, item_pools)


    def cloak(self, worlds, location_pools, model_pools):
        for world_dist in self.worlds:
            world_dist.cloak(worlds[world_dist.id], location_pools, model_pools)


    def update(self, src_dict):
        world_count = reduce(lambda n, k: max(n, len(src_dict.get(k, []))), per_world_keys, 0)
        if sum(src_dict.get('item_count_imbalances', [])) != 0:
            raise RuntimeError('The item count imbalances must compensate each other (sum must be 0)!')
        self.file_hash = (src_dict.get('file_hash', []) + [None, None, None, None, None])[0:5]
        for world_id in range(world_count):
            self.for_world(world_id).update({k: src_dict[k][world_id] for k in per_world_keys if k in src_dict and len(src_dict[k]) > world_id})
        self.locations_default_extra = src_dict.get('locations_default_extra', False)
        self.starting_default_extra = src_dict.get('starting_default_extra', True)


    def to_dict(self):
        worlds = [world.to_dict() for world in self.worlds]
        self_dict = {
            'file_hash': self.file_hash,
            **{k: [world[k] for world in worlds] for k in per_world_keys},
        }
        if self.locations_default_extra:
            self_dict['locations_default_extra'] = True
        if not self.starting_default_extra:
            self_dict['starting_default_extra'] = False
        return self_dict


    @staticmethod
    def from_spoiler(spoiler):
        dist = Distribution()
        dist.file_hash = [HASH_ICONS[icon] for icon in spoiler.file_hash]
        for world in spoiler.worlds:
            world_dist = dist.for_world(world.id)
            src_dist = world.get_distribution()
            world_dist.dungeons = {dung: DungeonRecord({ 'mq': world.dungeon_mq[dung] }) for dung in world.dungeon_mq}
            world_dist.trials = {trial: TrialRecord({ 'skip': world.skipped_trials[trial] }) for trial in world.skipped_trials}
            world_dist.item_count_imbalance = src_dist.item_count_imbalance
            world_dist.item_pool = {}
            world_dist.starting_items = {name: StarterRecord({ 'count': record.count }) for (name, record) in src_dist.starting_items.items()}
            world_dist.logic_ignored_items = src_dist.logic_ignored_items
            world_dist.locations = {loc: LocationRecord({ 'item': item.name, 'player': None if item.world is world else item.world.id, 'model': item.looks_like_item.name if item.looks_like_item is not None else None, 'price': item.price }) for (loc, item) in spoiler.locations[world.id].items()}
            world_dist.gossip = {gossipLocations[loc].name: GossipRecord({ 'gossip': spoiler.hints[world.id][loc] }) for loc in spoiler.hints[world.id]}
        for world in spoiler.worlds:
            for (_, item) in spoiler.locations[world.id].items():
                if item.dungeonitem or item.type == 'Event':
                    continue
                player_dist = dist.for_world(item.world.id)
                if item.name in player_dist.item_pool:
                    player_dist.item_pool[item.name].count += 1
                else:
                    player_dist.item_pool[item.name] = ItemPoolRecord()
        return dist


    @staticmethod
    def from_file(filename):
        with open(filename) as infile:
            src_dict = json.load(infile)
        return Distribution(src_dict)


    def to_file(self, filename):
        self_dict = self.to_dict()
        with open(filename, 'w') as outfile:
            json.dump(self_dict, outfile, indent=4)


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


def pull_element(pools, predicate, first=True, remove=True):
    return pull_first_element(pools, predicate, remove) if first else pull_random_element(pools, predicate, remove)


def pull_first_element(pools, predicate, remove=True):
    for pool in pools:
        for element in pool:
            if predicate(element):
                if remove:
                    pool.remove(element)
                return element
    return None


def pull_random_element(pools, predicate, remove=True):
    candidates = [(element, pool) for pool in pools for element in pool if predicate(element)]
    if len(candidates) == 0:
        return None
    element, pool = candidates[random.randint(0, len(candidates) - 1)]
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