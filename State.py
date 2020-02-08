from collections import Counter, defaultdict
import copy
from functools import partial
import itertools

from Item import ItemInfo
from Search import Search
from Region import Region, TimeOfDay



class State(object):

    def __init__(self, parent):
        self.prog_items = Counter()
        self.world = parent
        self.search = None


    ## Ensure that this will always have a value
    @property
    def is_glitched(self):
        return self.world.logic_rules != 'glitchless'


    def copy(self, new_world=None):
        if not new_world:
            new_world = self.world
        new_state = State(new_world)
        new_state.prog_items = copy.copy(self.prog_items)
        return new_state


    def item_name(self, location):
        location = self.world.get_location(location)
        if location.item is None:
            return None
        return location.item.name


    def has(self, item, count=1):
        return self.prog_items[item] >= count


    def has_any_of(self, items):
        return any(map(self.prog_items.__contains__, items))


    def has_all_of(self, items):
        return all(map(self.prog_items.__contains__, items))


    def item_count(self, item):
        return self.prog_items[item]


    def has_bottle(self, **kwargs):
        # Extra Ruto's Letter are automatically emptied
        return self.has_any_of(ItemInfo.bottles) or self.has('Bottle with Letter', 2)


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


    def had_night_start(self):
        stod = self.world.starting_tod
        # These are all not between 6:30 and 18:00
        if (stod == 'sunset' or         # 18
            stod == 'evening' or        # 21
            stod == 'midnight' or       # 00
            stod == 'witching-hour'):   # 03
            return True
        else:
            return False


    # Used for fall damage and other situations where damage is unavoidable
    def can_live_dmg(self, hearts):
        mult = self.world.damage_multiplier
        if hearts*4 >= 3:
            return mult != 'ohko' and mult != 'quadruple'
        elif hearts*4 < 3:
            return mult != 'ohko'
        else:
            return True


    # Use the guarantee_hint rule defined in json.
    def guarantee_hint(self):
        return self.world.parser.parse_rule('guarantee_hint')(self)


    # Be careful using this function. It will not collect any
    # items that may be locked behind the item, only the item itself.
    def collect(self, item):
        if item.advancement:
            self.prog_items[item.name] += 1


    # Be careful using this function. It will not uncollect any
    # items that may be locked behind the item, only the item itself.
    def remove(self, item):
        if self.prog_items[item.name] > 0:
            self.prog_items[item.name] -= 1
            if self.prog_items[item.name] <= 0:
                del self.prog_items[item.name]


    def __getstate__(self):
        return self.__dict__.copy()


    def __setstate__(self, state):
        self.__dict__.update(state)


    @staticmethod
    def can_beat_game(state_list):
        return Search(state_list).can_beat_game()


    @staticmethod
    def update_required_items(spoiler):
        worlds = spoiler.worlds

        # get list of all of the progressive items that can appear in hints
        # all_locations: all progressive items. have to collect from these
        # item_locations: only the ones that should appear as "required"/WotH
        all_locations = [location for world in worlds for location in world.get_filled_locations()]
        # Set to test inclusion against
        item_locations = {location for location in all_locations if location.item.majoritem and not location.locked and location.item.name != 'Triforce Piece'}

        # if the playthrough was generated, filter the list of locations to the
        # locations in the playthrough. The required locations is a subset of these
        # locations. Can't use the locations directly since they are location to the
        # copied spoiler world, so must compare via name and world id
        if spoiler.playthrough:
            translate = lambda loc: worlds[loc.world.id].get_location(loc.name)
            spoiler_locations = set(map(translate, itertools.chain.from_iterable(spoiler.playthrough.values())))
            item_locations &= spoiler_locations

        required_locations = []

        search = Search([world.state for world in worlds])
        for location in search.iter_reachable_locations(all_locations):
            # Try to remove items one at a time and see if the game is still beatable
            if location in item_locations:
                old_item = location.item
                location.item = None
                # copies state! This is very important as we're in the middle of a search
                # already, but beneficially, has search it can start from
                if not search.can_beat_game():
                    required_locations.append(location)
                location.item = old_item
            search.state_list[location.item.world.id].collect(location.item)

        # Filter the required location to only include location in the world
        required_locations_dict = {}
        for world in worlds:
            required_locations_dict[world.id] = list(filter(lambda location: location.world.id == world.id, required_locations))
        spoiler.required_locations = required_locations_dict
