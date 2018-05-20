import copy
from enum import Enum, unique
import logging
from collections import OrderedDict


class World(object):

    def __init__(self, bridge, open_forest, open_door_of_time, place_dungeon_items, check_beatable_only, hints):
        self.shuffle = 'vanilla'
        self.bridge = bridge
        self.dungeons = []
        self.regions = []
        self.itempool = []
        self.seed = None
        self.state = CollectionState(self)
        self._cached_locations = None
        self._entrance_cache = {}
        self._region_cache = {}
        self._entrance_cache = {}
        self._location_cache = {}
        self.required_locations = []
        self.check_beatable_only = check_beatable_only
        self.place_dungeon_items = place_dungeon_items
        self.open_forest = open_forest
        self.open_door_of_time = open_door_of_time
        self.hints = hints
        self.keysanity = False
        self.can_take_damage = True
        self.spoiler = Spoiler(self)

    def intialize_regions(self):
        for region in self.regions:
            region.world = self

    def get_region(self, regionname):
        if isinstance(regionname, Region):
            return regionname
        try:
            return self._region_cache[regionname]
        except KeyError:
            for region in self.regions:
                if region.name == regionname:
                    self._region_cache[regionname] = region
                    return region
            raise RuntimeError('No such region %s' % regionname)

    def get_entrance(self, entrance):
        if isinstance(entrance, Entrance):
            return entrance
        try:
            return self._entrance_cache[entrance]
        except KeyError:
            for region in self.regions:
                for exit in region.exits:
                    if exit.name == entrance:
                        self._entrance_cache[entrance] = exit
                        return exit
            raise RuntimeError('No such entrance %s' % entrance)

    def get_location(self, location):
        if isinstance(location, Location):
            return location
        try:
            return self._location_cache[location]
        except KeyError:
            for region in self.regions:
                for r_location in region.locations:
                    if r_location.name == location:
                        self._location_cache[location] = r_location
                        return r_location
        raise RuntimeError('No such location %s' % location)

    def get_all_state(self, keys=False):
        ret = CollectionState(self)

        def soft_collect(item):
            if item.advancement or item.key:
                ret.prog_items.append(item.name)

        for item in self.itempool:
            soft_collect(item)
        from Items import ItemFactory
        if keys:
            for item in ItemFactory(['Small Key (Forest Temple)'] * 5 + ['Boss Key (Forest Temple)', 'Boss Key (Fire Temple)', 'Boss Key (Water Temple)', 'Boss Key (Shadow Temple)', 'Boss Key (Spirit Temple)', 'Boss Key (Ganons Castle)'] + ['Small Key (Bottom of the Well)'] * 2 + ['Small Key (Fire Temple)'] * 8 + ['Small Key (Water Temple)'] * 6 + ['Small Key (Shadow Temple)'] * 4 + ['Small Key (Gerudo Training Grounds)'] * 8 + ['Small Key (Spirit Temple)'] * 5 + ['Small Key (Ganons Castle)'] * 2):
                soft_collect(item)
        ret.sweep_for_events()
        ret.clear_cached_unreachable()
        return ret

    def get_items(self):
        return [loc.item for loc in self.get_filled_locations()] + self.itempool

    def find_items(self, item):
        return [location for location in self.get_locations() if location.item is not None and location.item.name == item]

    def push_item(self, location, item, collect=True):
        if not isinstance(location, Location):
            location = self.get_location(location)

        if location.can_fill(self.state, item, False):
            location.item = item
            item.location = location
            if collect:
                self.state.collect(item, location.event, location)

            logging.getLogger('').debug('Placed %s at %s', item, location)
        else:
            raise RuntimeError('Cannot assign item %s to location %s.' % (item, location))

    def get_locations(self):
        if self._cached_locations is None:
            self._cached_locations = []
            for region in self.regions:
                self._cached_locations.extend(region.locations)
        return self._cached_locations

    def get_unfilled_locations(self):
        return [location for location in self.get_locations() if location.item is None]

    def get_filled_locations(self):
        return [location for location in self.get_locations() if location.item is not None]

    def get_reachable_locations(self, state=None):
        if state is None:
            state = self.state
        return [location for location in self.get_locations() if state.can_reach(location)]

    def get_placeable_locations(self, state=None):
        if state is None:
            state = self.state
        return [location for location in self.get_locations() if location.item is None and state.can_reach(location)]

    def unlocks_new_location(self, item):
        temp_state = self.state.copy()
        temp_state.clear_cached_unreachable()
        temp_state.collect(item, True)

        for location in self.get_unfilled_locations():
            if temp_state.can_reach(location) and not self.state.can_reach(location):
                return True

        return False

    def has_beaten_game(self, state):
        if state.has('Triforce'):
            return True
        return False

    def can_beat_game(self, starting_state=None):
        if starting_state:
            state = starting_state.copy()
        else:
            state = CollectionState(self)

        if self.has_beaten_game(state):
            return True

        prog_locations = [location for location in self.get_locations() if location.item is not None and (location.item.advancement or location.event) and location not in state.locations_checked]

        while prog_locations:
            sphere = []
            # build up spheres of collection radius. Everything in each sphere is independent from each other in dependencies and only depends on lower spheres
            for location in prog_locations:
                if state.can_reach(location):
                    if location.item.name == 'Triforce':
                        return True
                    sphere.append(location)

            if not sphere:
                # ran out of places and did not find triforce yet, quit
                return False

            for location in sphere:
                prog_locations.remove(location)
                state.collect(location.item, True, location)

        return False

    @property
    def option_identifier(self):
        id_value = 0
        id_value_max = 1

        def markbool(value):
            nonlocal id_value, id_value_max
            id_value += id_value_max * bool(value)
            id_value_max *= 2
        def marksequence(options, value):
            nonlocal id_value, id_value_max
            id_value += id_value_max * options.index(value)
            id_value_max *= len(options)
        markbool(self.place_dungeon_items)
        marksequence(['ganon', 'pedestal', 'dungeons'], self.bridge)
        marksequence(['vanilla', 'simple'], self.shuffle)
        markbool(self.check_beatable_only)
        assert id_value_max <= 0xFFFFFFFF
        return id_value


class CollectionState(object):

    def __init__(self, parent):
        self.prog_items = []
        self.world = parent
        self.region_cache = {}
        self.location_cache = {}
        self.entrance_cache = {}
        self.recursion_count = 0
        self.events = []
        self.path = {}
        self.locations_checked = set()


    def clear_cached_unreachable(self):
        # we only need to invalidate results which were False, places we could reach before we can still reach after adding more items
        self.region_cache = {k: v for k, v in self.region_cache.items() if v}
        self.location_cache = {k: v for k, v in self.location_cache.items() if v}
        self.entrance_cache = {k: v for k, v in self.entrance_cache.items() if v}

    def copy(self):
        ret = CollectionState(self.world)
        ret.prog_items = copy.copy(self.prog_items)
        ret.region_cache = copy.copy(self.region_cache)
        ret.location_cache = copy.copy(self.location_cache)
        ret.entrance_cache = copy.copy(self.entrance_cache)
        ret.events = copy.copy(self.events)
        ret.path = copy.copy(self.path)
        ret.locations_checked = copy.copy(self.locations_checked)
        return ret

    def can_reach(self, spot, resolution_hint=None):
        try:
            spot_type = spot.spot_type
            if spot_type == 'Location':
                correct_cache = self.location_cache
            elif spot_type == 'Region':
                correct_cache = self.region_cache
            elif spot_type == 'Entrance':
                correct_cache = self.entrance_cache
            else:
                raise AttributeError
        except AttributeError:
            # try to resolve a name
            if resolution_hint == 'Location':
                spot = self.world.get_location(spot)
                correct_cache = self.location_cache
            elif resolution_hint == 'Entrance':
                spot = self.world.get_entrance(spot)
                correct_cache = self.entrance_cache
            else:
                # default to Region
                spot = self.world.get_region(spot)
                correct_cache = self.region_cache

        if spot.recursion_count > 0:
            return False

        if spot not in correct_cache:
            # for the purpose of evaluating results, recursion is resolved by always denying recursive access (as that ia what we are trying to figure out right now in the first place
            spot.recursion_count += 1
            self.recursion_count += 1
            can_reach = spot.can_reach(self)
            spot.recursion_count -= 1
            self.recursion_count -= 1

            # we only store qualified false results (i.e. ones not inside a hypothetical)
            if not can_reach:
                if self.recursion_count == 0:
                    correct_cache[spot] = can_reach
            else:
                correct_cache[spot] = can_reach
            return can_reach
        return correct_cache[spot]

    def sweep_for_events(self, key_only=False):
        # this may need improvement
        new_locations = True
        checked_locations = 0
        while new_locations:
            reachable_events = [location for location in self.world.get_filled_locations() if location.event and (not key_only or location.item.key) and self.can_reach(location)]
            for event in reachable_events:
                if event.name not in self.events:
                    self.events.append(event.name)
                    self.collect(event.item, True, event)
            new_locations = len(reachable_events) > checked_locations
            checked_locations = len(reachable_events)

    def has(self, item, count=1):
        if count == 1:
            return item in self.prog_items
        return self.item_count(item) >= count

    def item_count(self, item):
        return len([pritem for pritem in self.prog_items if pritem == item])

    def is_adult(self):
        return self.has('Master Sword')

    def can_blast(self):
        return self.has('Bomb Bag') or (self.is_adult() and self.has('Hammer'))

    def can_dive(self):
        return self.has('Progressive Scale')

    def can_lift_rocks(self):
        return (self.has('Silver Gauntlets') or self.has('Gold Gauntlets')) and self.is_adult()

    def can_finish_adult_trades(self):
        zora_thawed = self.has_bottle() and self.has('Zeldas Lullaby') and (self.can_reach('Ice Cavern') or self.can_reach('Ganons Castle Water Trial') or self.has('Progressive Wallet', 2))
        carpenter_access = self.has('Epona') or self.has('Progressive Hookshot', 2)
        return (self.has('Claim Check') or ((self.has('Eyedrops') or self.has('Eyeball Frog') or self.has('Prescription') or self.has('Broken Sword')) and zora_thawed) or ((self.has('Poachers Saw') or self.has('Odd Mushroom') or self.has('Cojiro') or self.has('Pocket Cucco') or self.has('Pocket Egg')) and zora_thawed and carpenter_access))

    def has_bottle(self):
        return (self.has('Bottle') or self.has('Bottle with Milk'))

    def bottle_count(self):
        return len([pritem for pritem in self.prog_items if pritem.startswith('Bottle')])

    def has_hearts(self, count):
        # Warning: This only considers items that are marked as advancement items
        return self.heart_count() >= count

    def heart_count(self):
        # Warning: This only considers items that are marked as advancement items
        return (
            self.item_count('Heart Container')
            + self.item_count('Piece of Heart') // 4
            + 3 # starting hearts
        )

    def can_lift_pillars(self):
        return self.has('Gold Gauntlets') and self.is_adult()

    def has_fire_source(self):
        return ((self.has('Dins Fire') or (self.has('Bow') and self.has('Fire Arrows') and self.is_adult())) and self.has('Magic Meter'))

    def guarantee_hint(self):
        return(self.has('Stone of Agony') or not self.world.hints)

    def collect(self, item, event=False, location=None):
        if location:
            self.locations_checked.add(location)
        changed = False
        if item.name.startswith('Bottle'):
            if self.bottle_count() < 4:
                self.prog_items.append(item.name)
                changed = True
        elif event or item.advancement:
            self.prog_items.append(item.name)
            changed = True

        if changed:
            self.clear_cached_unreachable()
            if not event:
                self.sweep_for_events()
                self.clear_cached_unreachable()

    def remove(self, item):
        if item.advancement:
            to_remove = item.name

            if to_remove is not None:
                try:
                    self.prog_items.remove(to_remove)
                except ValueError:
                    return

                # invalidate caches, nothing can be trusted anymore now
                self.region_cache = {}
                self.location_cache = {}
                self.entrance_cache = {}
                self.recursion_count = 0

    def __getattr__(self, item):
        if item.startswith('can_reach_'):
            return self.can_reach(item[10])
        elif item.startswith('has_'):
            return self.has(item[4])

        raise RuntimeError('Cannot parse %s.' % item)

@unique
class RegionType(Enum):
    Overworld = 1
    Interior = 2
    Dungeon = 3
    Grotto = 4

    @property
    def is_indoors(self):
        """Shorthand for checking if Interior or Dungeon"""
        return self in (RegionType.Interior, RegionType.Dungeon, RegionType.Grotto)



class Region(object):

    def __init__(self, name, type):
        self.name = name
        self.type = type
        self.entrances = []
        self.exits = []
        self.locations = []
        self.dungeon = None
        self.world = None
        self.spot_type = 'Region'
        self.recursion_count = 0

    def can_reach(self, state):
        for entrance in self.entrances:
            if state.can_reach(entrance):
                if not self in state.path:
                    state.path[self] = (self.name, state.path.get(entrance, None))
                return True
        return False

    def can_fill(self, item):
        is_dungeon_item = item.key or item.map or item.compass
        if is_dungeon_item:
            return self.dungeon and self.dungeon.is_dungeon_item(item)
        return True

    def __str__(self):
        return str(self.__unicode__())

    def __unicode__(self):
        return '%s' % self.name


class Entrance(object):

    def __init__(self, name='', parent=None):
        self.name = name
        self.parent_region = parent
        self.connected_region = None
        self.target = None
        self.addresses = None
        self.spot_type = 'Entrance'
        self.recursion_count = 0
        self.vanilla = None
        self.access_rule = lambda state: True

    def can_reach(self, state):
        if self.access_rule(state) and state.can_reach(self.parent_region):
            if not self in state.path:
                state.path[self] = (self.name, state.path.get(self.parent_region, (self.parent_region.name, None)))
            return True

        return False

    def connect(self, region, addresses=None, target=None, vanilla=None):
        self.connected_region = region
        self.target = target
        self.addresses = addresses
        self.vanilla = vanilla
        region.entrances.append(self)

    def __str__(self):
        return str(self.__unicode__())

    def __unicode__(self):
        return '%s' % self.name


class Dungeon(object):

    def __init__(self, name, regions, boss_key, small_keys, dungeon_items):
        self.name = name
        self.regions = regions
        self.boss_key = boss_key
        self.small_keys = small_keys
        self.dungeon_items = dungeon_items

    @property
    def keys(self):
        return self.small_keys + ([self.boss_key] if self.boss_key else [])

    @property
    def all_items(self):
        return self.dungeon_items + self.keys

    def is_dungeon_item(self, item):
        return item.name in [dungeon_item.name for dungeon_item in self.all_items]

    def __str__(self):
        return str(self.__unicode__())

    def __unicode__(self):
        return '%s' % self.name


class Location(object):

    def __init__(self, name='', address=None, address2=None, default=None, type='Chest', parent=None):
        self.name = name
        self.parent_region = parent
        self.item = None
        self.address = address
        self.address2 = address2
        self.default = default
        self.type = type
        self.spot_type = 'Location'
        self.recursion_count = 0
        self.staleness_count = 0
        self.event = False
        self.always_allow = lambda item, state: False
        self.access_rule = lambda state: True
        self.item_rule = lambda item: True

    def can_fill(self, state, item, check_access=True):
        return self.always_allow(item, self) or (self.parent_region.can_fill(item) and self.item_rule(item) and (not check_access or self.can_reach(state)))

    def can_fill_fast(self, item):
        return self.item_rule(item)

    def can_reach(self, state):
        if self.access_rule(state) and state.can_reach(self.parent_region):
            return True
        return False

    def __str__(self):
        return str(self.__unicode__())

    def __unicode__(self):
        return '%s' % self.name


class Item(object):

    def __init__(self, name='', advancement=False, priority=False, type=None, code=None, index=None):
        self.name = name
        self.advancement = advancement
        self.priority = priority
        self.type = type
        self.code = code
        self.index = index
        self.location = None

    @property
    def key(self):
        return self.type == 'SmallKey' or self.type == 'BossKey'

    @property
    def crystal(self):
        return self.type == 'Crystal'

    @property
    def map(self):
        return self.type == 'Map'

    @property
    def compass(self):
        return self.type == 'Compass'

    def __str__(self):
        return str(self.__unicode__())

    def __unicode__(self):
        return '%s' % self.name


class Spoiler(object):

    def __init__(self, world):
        self.world = world
        self.entrances = []
        self.playthrough = {}
        self.locations = {}
        self.paths = {}
        self.metadata = {}

    def set_entrance(self, entrance, exit, direction):
        self.entrances.append(OrderedDict([('entrance', entrance), ('exit', exit), ('direction', direction)]))

    def parse_data(self):
        spoiler_locations = []
        for location in self.world.get_locations():
            if location.item.name not in ['Gold Skulltulla Token', 'Epona', 'Triforce', 'Fairy Ocarina', 'Ocarina of Time', 'Zeldas Letter', 'Master Sword',
                                          'Magic Bean', 'Gerudo Membership Card', 'Forest Trial Clear', 'Fire Trial Clear', 'Water Trial Clear', 'Shadow Trial Clear', 'Spirit Trial Clear', 'Light Trial Clear']:
                spoiler_locations.append(location)
        sort_order = {"Song": 0, "Boss": -1}
        spoiler_locations.sort(key=lambda item: sort_order.get(item.type, 1))
        self.locations = {'other locations': OrderedDict([(str(location), str(location.item) if location.item is not None else 'Nothing') for location in spoiler_locations])}
        from Main import __version__ as OoTRVersion
        self.metadata = {'version': OoTRVersion,
                         'seed': self.world.seed,
                         'bridge': self.world.bridge,
                         'forest': self.world.open_forest,
                         'door': self.world.open_door_of_time,
                         'completeable': not self.world.check_beatable_only,
                         'dungeonitems': self.world.place_dungeon_items}

    def to_file(self, filename):
        self.parse_data()
        with open(filename, 'w') as outfile:
            outfile.write('OoT Randomizer Version %s  -  Seed: %s\n\n' % (self.metadata['version'], self.metadata['seed']))
            outfile.write('Rainbow Bridge Requirement:      %s\n' % self.metadata['bridge'])
            outfile.write('Open Forest:                     %s\n' % ('Yes' if self.metadata['forest'] else 'No'))
            outfile.write('Open Door of Time:               %s\n' % ('Yes' if self.metadata['door'] else 'No'))
            outfile.write('All Locations Accessible:        %s\n' % ('Yes' if self.metadata['completeable'] else 'No, some locations may be unreachable'))
            outfile.write('Maps and Compasses in Dungeons:  %s\n' % ('Yes' if self.metadata['dungeonitems'] else 'No'))
            outfile.write('\n\nEntrances:\n\n')
            outfile.write('\n'.join(['%s %s %s' % (entry['entrance'], '<=>' if entry['direction'] == 'both' else '<=' if entry['direction'] == 'exit' else '=>', entry['exit']) for entry in self.entrances]))
            outfile.write('\n\nLocations:\n\n')
            outfile.write('\n'.join(['%s: %s' % (location, item) for (location, item) in self.locations['other locations'].items()]))
            outfile.write('\n\nPlaythrough:\n\n')
            outfile.write('\n'.join(['%s: {\n%s\n}' % (sphere_nr, '\n'.join(['  %s: %s' % (location, item) for (location, item) in sphere.items()])) for (sphere_nr, sphere) in self.playthrough.items()]))
            outfile.write('\n\nPaths:\n\n')

            path_listings = []
            for location, path in sorted(self.paths.items()):
                path_lines = []
                for region, exit in path:
                    if exit is not None:
                        path_lines.append("{} -> {}".format(region, exit))
                    else:
                        path_lines.append(region)
                path_listings.append("{}\n        {}".format(location, "\n   =>   ".join(path_lines)))

            outfile.write('\n'.join(path_listings))
