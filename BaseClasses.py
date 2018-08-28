import copy
from enum import Enum, unique
import logging
from collections import OrderedDict, Counter
from version import __version__ as OoTRVersion


class World(object):

    def __init__(self, settings):
        self.shuffle = 'vanilla'
        self.dungeons = []
        self.regions = []
        self.itempool = []
        self.state = CollectionState(self)
        self._cached_locations = None
        self._entrance_cache = {}
        self._region_cache = {}
        self._entrance_cache = {}
        self._location_cache = {}
        self.required_locations = []

        # dump settings directly into world's namespace
        # this gives the world an attribute for every setting listed in Settings.py
        self.settings = settings
        self.__dict__.update(settings.__dict__)
        # rename a few attributes...
        self.keysanity = self.shuffle_dungeon_items == 'keysanity'
        self.check_beatable_only = not self.all_reachable
        # group a few others
        self.tunic_colors = [self.kokiricolor, self.goroncolor, self.zoracolor]
        self.navi_colors = [self.navicolordefault, self.navicolorenemy, self.navicolornpc, self.navicolorprop]
        self.navi_hint_sounds = [self.navisfxoverworld, self.navisfxenemytarget]
        # trials that can be skipped will be decided later
        self.skipped_trials = {
            'Forest': False,
            'Fire': False,
            'Water': False,
            'Spirit': False,
            'Shadow': False,
            'Light': False
        }
        # dungeon forms will be decided later
        self.dungeon_mq = {
            'DT': False,
            'DC': False,
            'JB': False,
            'BW': False,
            'IC': False,
            'GTG': False,
            'FoT': False,
            'FiT': False,
            'WT': False,
            'SpT': False,
            'ShT': False,
            'GC': False
}

        self.can_take_damage = True
        self.spoiler = Spoiler(self)


    def copy(self):
        ret = World(self.settings)
        ret.skipped_trials = copy.copy(self.skipped_trials)
        ret.dungeon_mq = copy.copy(self.dungeon_mq)
        ret.can_take_damage = self.can_take_damage
        ret.id = self.id
        from Regions import create_regions
        from Dungeons import create_dungeons
        from Rules import set_rules
        create_regions(ret)
        create_dungeons(ret)
        set_rules(ret)

        # connect copied world
        for region in self.regions:
            copied_region = ret.get_region(region.name)
            for entrance in region.entrances:
                ret.get_entrance(entrance.name).connect(copied_region)

        # fill locations
        for location in self.get_locations():
            if location.item is not None:
                item = Item(location.item.name, location.item.advancement, location.item.priority, location.item.type)
                item.world = location.item.world
                ret.get_location(location.name).item = item
                item.location = ret.get_location(location.name)
                item.location.event = location.event

        # copy remaining itempool. No item in itempool should have an assigned location
        for item in self.itempool:
            new_item = Item(item.name, item.advancement, item.priority, item.type)
            new_item.world = item.world
            ret.itempool.append(new_item)

        # copy progress items in state
        ret.state.prog_items = copy.copy(self.state.prog_items)

        return ret

    def initialize_regions(self):
        for region in self.regions:
            region.world = self
            for location in region.locations:
                location.world = self

    def initialize_items(self):
        for item in self.itempool:
            item.world = self
        for region in self.regions:
            for location in region.locations:
                if location.item != None:
                    location.item.world = self
        for dungeon in self.dungeons:
            for item in dungeon.all_items:
                item.world = self


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

    def get_items(self):
        return [loc.item for loc in self.get_filled_locations()] + self.itempool

    # get a list of items that should stay in their proper dungeon
    def get_restricted_dungeon_items(self):
        if self.shuffle_dungeon_items == 'keysanity':
            itempool = []
        elif self.shuffle_dungeon_items == 'mapcompass':
            itempool = [item for dungeon in self.dungeons for item in dungeon.all_items if item.key]
        else:
            itempool = [item for dungeon in self.dungeons for item in dungeon.all_items]
        for item in itempool:
            item.world = self
        return itempool

    # get a list of items that don't have to be in their proper dungeon
    def get_unrestricted_dungeon_items(self):
        if self.shuffle_dungeon_items == 'keysanity':
            itempool = [item for dungeon in self.dungeons for item in dungeon.all_items]
        elif self.shuffle_dungeon_items == 'mapcompass':
            itempool = [item for dungeon in self.dungeons for item in dungeon.all_items if not item.key]
        else:
            itempool = []
        for item in itempool:
            item.world = self
        return itempool

    def find_items(self, item):
        return [location for location in self.get_locations() if location.item is not None and location.item.name == item]

    def push_item(self, location, item):
        if not isinstance(location, Location):
            location = self.get_location(location)

        # This check should never be false normally, but is here as a sanity check
        if location.can_fill(self.state, item, False):
            location.item = item
            item.location = location

            logging.getLogger('').debug('Placed %s [World %d] at %s [World %d]', item, item.world.id if hasattr(item, 'world') else -1, location, location.world.id if hasattr(location, 'world') else -1)
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
        temp_state.collect(item)

        for location in self.get_unfilled_locations():
            if temp_state.can_reach(location) and not self.state.can_reach(location):
                return True

        return False

    def has_beaten_game(self, state):
        return state.has('Triforce')


class CollectionState(object):

    def __init__(self, parent):
        self.prog_items = Counter()
        self.world = parent
        self.region_cache = {}
        self.location_cache = {}
        self.entrance_cache = {}
        self.recursion_count = 0
        self.collected_locations = {}

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
        ret.collected_locations = copy.copy(self.collected_locations)
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

    def has(self, item, count=1):
        return self.prog_items[item] >= count

    def item_count(self, item):
    	return self.prog_items[item]

    def is_adult(self):
        return self.has('Master Sword')

    def has_ocarina(self):
        return (self.has('Ocarina') or self.has("Fairy Ocarina") or self.has("Ocarina of Time"))

    def can_play(self, song):
        return self.has_ocarina() and self.has(song)

    def has_bombchus(self):
        return (self.world.bombchus_in_logic and \
                    (any(pritem.startswith('Bombchus') for pritem in self.prog_items) \
                    or (self.has('Progressive Wallet') and self.can_reach('Haunted Wasteland')))) \
            or (not self.world.bombchus_in_logic and self.has('Bomb Bag'))

    def has_explosives(self):
        return self.has('Bomb Bag') or self.has_bombchus()

    def can_blast_or_smash(self):
        return self.has('Bomb Bag') or (self.is_adult() and self.has('Hammer')) or self.has_bombchus()

    def can_dive(self):
        return self.has('Progressive Scale')

    def can_lift_rocks(self):
        return (self.has('Silver Gauntlets') or self.has('Gold Gauntlets')) and self.is_adult()

    def can_see_with_lens(self):
        return ((self.has('Magic Meter') and self.has('Lens of Truth')) or self.world.logic_lens != 'all')

    def has_GoronTunic(self):
        return (self.has('Goron Tunic') or (self.has('Progressive Wallet') and (self.has_explosives() or self.has('Progressive Strength Upgrade') or self.has('Bow'))))

    def has_ZoraTunic(self):
        return (self.has('Zora Tunic') or (self.has('Progressive Wallet', 2) and self.has_bottle() and self.can_play('Zeldas Lullaby')))

    def can_leave_forest(self):
        return (self.world.open_forest or (self.has('Slingshot') and self.has('Kokiri Sword')))

    def can_finish_adult_trades(self):
        if self.world.dungeon_mq['GTG']:
            zora_thawed = self.has_bottle() and (self.can_play('Zeldas Lullaby') or (self.has('Hover Boots') and self.world.logic_zora_with_hovers)) and (self.can_reach('Ice Cavern') or self.can_reach('Ganons Castle Water Trial') or self.has('Progressive Wallet', 2) or self.can_reach('Gerudo Training Grounds Stalfos Room'))
        else:
            zora_thawed = self.has_bottle() and (self.can_play('Zeldas Lullaby') or (self.has('Hover Boots') and self.world.logic_zora_with_hovers)) and (self.can_reach('Ice Cavern') or self.can_reach('Ganons Castle Water Trial') or self.has('Progressive Wallet', 2))
        carpenter_access = self.has('Epona') or self.has('Progressive Hookshot', 2)
        return (self.has('Claim Check') or ((self.has('Eyedrops') or self.has('Eyeball Frog') or self.has('Prescription') or self.has('Broken Sword')) and zora_thawed) or ((self.has('Poachers Saw') or self.has('Odd Mushroom') or self.has('Cojiro') or self.has('Pocket Cucco') or self.has('Pocket Egg')) and zora_thawed and carpenter_access))

    def has_bottle(self):
        is_normal_bottle = lambda item: (item.startswith('Bottle') and item != 'Bottle with Letter')
        return any(is_normal_bottle(pritem) for pritem in self.prog_items)

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
        if(self.world.hints == 'mask'):
            # has the mask of truth
            return self.has('Zeldas Letter') and self.has('Sarias Song') and self.has('Kokiri Emerald') and self.has('Goron Ruby') and self.has('Zora Sapphire')
        elif(self.world.hints == 'agony'):
            # has the stone of agony
            return self.has('Stone of Agony')
        return True

    def nighttime(self):
        if self.world.logic_no_night_tokens_without_suns_song:
            return self.can_play('Suns Song')
        return True

    def collect(self, item):
        changed = False
        if item.name.startswith('Bottle'):
            if self.bottle_count() < 4:
                self.prog_items[item.name] += 1
                changed = True
        elif item.advancement:
            self.prog_items[item.name] += 1
            changed = True

        if changed:
            self.clear_cached_unreachable()
            
    def remove(self, item):
        if self.prog_items[item.name] > 0:
            self.prog_items[item.name] -= 1
            if self.prog_items[item.name] <= 0:
            	del self.prog_items[item.name]

            # invalidate collected cache. unreachable locations are still unreachable
            self.region_cache =   {k: v for k, v in self.region_cache.items() if not v}
            self.location_cache = {k: v for k, v in self.location_cache.items() if not v}
            self.entrance_cache = {k: v for k, v in self.entrance_cache.items() if not v}
            self.recursion_count = 0

    def __getattr__(self, item):
        if item.startswith('can_reach_'):
            return self.can_reach(item[10])
        elif item.startswith('has_'):
            return self.has(item[4])

        raise RuntimeError('Cannot parse %s.' % item)

    # This function returns a list of states that is each of the base_states
    # with every item still in the itempool. It only adds items that belong
    # to its respective world. See fill_restrictive
    @staticmethod
    def get_states_with_items(base_state_list, itempool):
        new_state_list = []
        for base_state in base_state_list:
            new_state = base_state.copy()
            for item in itempool:
                if item.world.id == base_state.world.id: # Check world
                    new_state.collect(item)
            new_state_list.append(new_state)
        CollectionState.collect_locations(new_state_list)
        return new_state_list

    # This collected all item locations available in the state list given that
    # the states have collected items. The purpose is that it will search for
    # all new items that become accessible with a new item set
    @staticmethod
    def collect_locations(state_list):
        # Get all item locations in the worlds
        item_locations = [location for state in state_list for location in state.world.get_filled_locations() if location.item.advancement]

        # will loop if there is more items opened up in the previous iteration. Always run once
        reachable_items_locations = True
        while reachable_items_locations:
            # get reachable new items locations
            reachable_items_locations = [location for location in item_locations if location.name not in state_list[location.world.id].collected_locations and state_list[location.world.id].can_reach(location)]
            for location in reachable_items_locations:
                # Mark the location collected in the state world it exists in
                state_list[location.world.id].collected_locations[location.name] = True
                # Collect the item for the state world it is for
                state_list[location.item.world.id].collect(location.item)


    # This removes all item locations collected in the state list given that
    # the states have collected items. The purpose is that it will search for
    # all new items that become no longer accessible with a removed item
    @staticmethod
    def remove_locations(state_list):
        # Get all item locations in the worlds
        item_locations = [location for state in state_list for location in state.world.get_filled_locations() if location.item.advancement]

        # will loop if there is more items removed in the previous iteration. Always run once
        unreachable_items_locations = True
        while unreachable_items_locations:
            # get unreachable new items locations
            unreachable_items_locations = [location for location in item_locations if location.name in state_list[location.world.id].collected_locations and not state_list[location.world.id].can_reach(location)]
            for location in unreachable_items_locations:
                # Mark the location uncollected in the state world it exists in
                del state_list[location.world.id].collected_locations[location.name]
                # Remove the item for the state world it is for
                state_list[location.item.world.id].remove(location.item)


    # This returns True is every state is beatable. It's important to ensure
    # all states beatable since items required in one world can be in another.
    @staticmethod
    def can_beat_game(state_list, scan_for_items=True):
        if scan_for_items:
            # Check if already beaten
            game_beaten = True
            for state in state_list:
                if not state.has('Triforce'):
                    game_beaten = False
                    break
            if game_beaten:
                return True

            # collect all available items
            new_state_list = [state.copy() for state in state_list]
            CollectionState.collect_locations(new_state_list)
        else:
            new_state_list = state_list

        # if the every state got the Triforce, then return True
        for state in new_state_list:
            if not state.has('Triforce'):
                return False
        return True

    @staticmethod
    def update_required_items(worlds):
        state_list = [CollectionState(world) for world in worlds]
        CollectionState.collect_locations(state_list)

        item_locations = []
        if worlds[0].spoiler.playthrough:
            item_locations = [location for _,sphere in worlds[0].spoiler.playthrough.items() for location in sphere
                if location.item.type != 'Event' and not location.event and (worlds[0].keysanity or not location.item.key)]
        else:
            item_locations = [location for world in worlds for location in world.get_filled_locations() 
                if location.item.advancement and location.item.type != 'Event' and not location.event and (worlds[0].keysanity or not location.item.key)]

        required_locations = []
        for location in item_locations:
            old_item = location.item
            new_state_list = [state.copy() for state in state_list]

            location.item = None
            new_state_list[old_item.world.id].remove(old_item)
            CollectionState.remove_locations(new_state_list)

            if not CollectionState.can_beat_game(new_state_list, False):
                required_locations.append(location)
            location.item = old_item

        for world in worlds:
            world.spoiler.required_locations = [location for location in required_locations if location.world.id == world.id]


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
                return True
        return False

    def can_fill(self, item):
        if self.world.shuffle_dungeon_items == 'keysanity':
            is_dungeon_restricted = False
        elif self.world.shuffle_dungeon_items == 'mapcompass':
            is_dungeon_restricted = item.key
        else:
            is_dungeon_restricted = item.key or item.map or item.compass
        if is_dungeon_restricted:
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

    def __init__(self, name='', address=None, address2=None, default=None, type='Chest', scene=None, hint='Termina', parent=None):
        self.name = name
        self.parent_region = parent
        self.item = None
        self.address = address
        self.address2 = address2
        self.default = default
        self.type = type
        self.scene = scene
        self.hint = hint
        self.spot_type = 'Location'
        self.recursion_count = 0
        self.staleness_count = 0
        self.always_allow = lambda item, state: False
        self.access_rule = lambda state: True
        self.item_rule = lambda item: True
        self.event = False

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

    def copy(self):
        return Item(self.name, self.advancement, self.priority, self.type, self.code, self.index)

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
        self.playthrough = {}
        self.locations = {}
        self.metadata = {}
        self.required_locations = []

    def parse_data(self):
        spoiler_locations = [location for location in self.world.get_locations() if not location.event]
        sort_order = {"Song": 0, "Boss": -1}
        spoiler_locations.sort(key=lambda item: sort_order.get(item.type, 1))
        if self.world.settings.world_count > 1:
            self.locations = {'other locations': OrderedDict([(str(location), "%s [Player %d]" % (str(location.item), location.item.world.id + 1) if location.item is not None else 'Nothing') for location in spoiler_locations])}
        else:
            self.locations = {'other locations': OrderedDict([(str(location), str(location.item) if location.item is not None else 'Nothing') for location in spoiler_locations])}            
        self.version = OoTRVersion
        self.settings = self.world.settings

    def to_file(self, filename):
        self.parse_data()
        with open(filename, 'w') as outfile:
            outfile.write('OoT Randomizer Version %s  -  Seed: %s\n\n' % (self.version, self.settings.seed))
            outfile.write('Settings (%s):\n%s' % (self.settings.get_settings_string(), self.settings.get_settings_display()))

            if self.settings.world_count > 1:
                outfile.write('\n\nLocations [World %d]:\n\n' % (self.settings.player_num))
            else:
                outfile.write('\n\nLocations:\n\n')
            outfile.write('\n'.join(['%s: %s' % (location, item) for (location, item) in self.locations['other locations'].items()]))

            outfile.write('\n\nPlaythrough:\n\n')
            if self.settings.world_count > 1:
                outfile.write('\n'.join(['%s: {\n%s\n}' % (sphere_nr, '\n'.join(['  %s [World %d]: %s [Player %d]' % (location.name, location.world.id + 1, item.name, item.world.id + 1) for (location, item) in sphere.items()])) for (sphere_nr, sphere) in self.playthrough.items()]))
            else:
                outfile.write('\n'.join(['%s: {\n%s\n}' % (sphere_nr, '\n'.join(['  %s: %s' % (location.name, item.name) for (location, item) in sphere.items()])) for (sphere_nr, sphere) in self.playthrough.items()]))

            outfile.write('\n\nAlways Required Locations:\n\n')
            if self.settings.world_count > 1:
                outfile.write('\n'.join(['%s: %s [Player %d]' % (location.name, location.item.name, location.item.world.id + 1) for location in self.required_locations]))
            else:
                outfile.write('\n'.join(['%s: %s' % (location.name, location.item.name) for location in self.required_locations]))
