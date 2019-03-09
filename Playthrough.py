import copy
from collections import deque, defaultdict
import itertools


class Playthrough(object):

    def __init__(self, state_list):
        self.state_list = state_list  # reference, not a copy
        # Each region sphere is a pair (child_regions, adult_regions)
        self.region_spheres = []
        # Mapping from location to sphere index. 0-based.
        self.location_in_sphere = defaultdict(int)

    # Truncates the region sphere cache based on which sphere a location is in.
    # Doesn't forget which sphere locations are in as an optimization, so be careful
    # to only uncollect locations in descending sphere order, or locations that
    # have been revisited in the most recent iteration.
    # Locations never visited in this Playthrough are assumed to be in sphere 0, so
    # uncollecting them will discard everything above sphere 0.
    # Not safe to call during iteration.
    def uncollect(self, location):
        self.region_spheres[self.location_in_sphere[location]+1:] = []

    # Yields every reachable location, by iteratively deepening explored sets of
    # regions (one as child, one as adult) and invoking access rules without
    # calling the recursive can_reach.
    # item_locations is a set of Location objects from state_list that the caller
    # has prefiltered (eg. by whether they contain advancement items).
    #
    # Inside the loop, the caller usually wants to collect items at these
    # locations to see if the game is beatable. This function does not alter provided state.
    def iter_reachable_locations(self, item_locations):
        if not self.region_spheres:
            self.region_spheres = [
                ({state.world.get_region('Links House') for state in self.state_list
                    if state.world.starting_age == 'child'},
                 {state.world.get_region('Temple of Time') for state in self.state_list
                    if state.world.starting_age == 'adult'})
            ]
        collected_set = set(itertools.chain.from_iterable(
            map(state.world.get_location, state.collected_locations)
            for id, state in enumerate(self.state_list)))
        # set of Region.
        child_regions, adult_regions = self.region_spheres[-1]
        # simplified exit.can_reach(self)
        new_child_exit = lambda exit: exit.connected_region not in child_regions and self.state_list[exit.parent_region.world.id].as_child(lambda s: s.with_spot(exit.access_rule, exit))
        new_adult_exit = lambda exit: exit.connected_region not in adult_regions and self.state_list[exit.parent_region.world.id].as_adult(lambda s: s.with_spot(exit.access_rule, exit))

        # simplified loc.can_reach(self), minus the disable check
        child_accessible = lambda loc: loc.parent_region in child_regions and self.state_list[loc.world.id].as_child(lambda s: s.with_spot(loc.access_rule, loc))
        adult_accessible = lambda loc: loc.parent_region in adult_regions and self.state_list[loc.world.id].as_adult(lambda s: s.with_spot(loc.access_rule, loc))

        reachable_locations = True
        # will loop as long as any collections were made, and at least once
        while reachable_locations:
            # 1. Use a queue to iteratively add regions to the accessed set,
            #    until we are stuck or out of regions.
            # queue of (is_child, Entrance)
            exit_queue = deque(itertools.chain(
                ((True, exit) for region in child_regions
                    for exit in region.exits if new_child_exit(exit)),
                ((False, exit) for region in adult_regions
                    for exit in region.exits if new_adult_exit(exit))))
            while exit_queue:
                child, exit = exit_queue.popleft()
                if child:
                    if exit.connected_region not in child_regions:
                        child_regions.add(exit.connected_region)
                        exit_queue.extend(
                            (True, exit) for exit in exit.connected_region.exits
                            if new_child_exit(exit))
                        if exit.connected_region.name == 'Beyond Door of Time':
                            adult_regions.add(exit.connected_region)
                            exit_queue.extend(
                                (False, exit) for exit in exit.connected_region.exits
                                if new_adult_exit(exit))
                            # Adult savewarp point is Temple of Time, which is
                            # always accessible from BDoT, so we can skip adding it specially
                else:
                    # mostly the same but for adult
                    if exit.connected_region not in adult_regions:
                        adult_regions.add(exit.connected_region)
                        exit_queue.extend(
                            (False, exit) for exit in exit.connected_region.exits
                            if new_adult_exit(exit))
                        if exit.connected_region.name == 'Beyond Door of Time':
                            child_regions.add(exit.connected_region)
                            exit_queue.extend(
                                (True, exit) for exit in exit.connected_region.exits
                                if new_adult_exit(exit))
                            # Child savewarp point is Links House, which is
                            # always accessible from BDoT -> ToT -> CT -> HF -> LWB -> KF, so we can skip adding it specially
            # 2. Get all locations in accessible_regions that aren't collected,
            #    and check if they can be reached. Collect them.
            reachable_locations = [
                location for location in item_locations - collected_set
                # Put the more likely one first
                if adult_accessible(location) or child_accessible(location)]
            for location in reachable_locations:
                yield location
                # Mark it collected for this algorithm
                collected_set.add(location)
                self.location_in_sphere[location] = len(self.region_spheres) - 1
            # 3. Save the current region sphere in the cache, duplicate to make a new one to modify
            self.region_spheres.append((copy.copy(child_regions), copy.copy(adult_regions)))
            child_regions, adult_regions = self.region_spheres[-1]

    # This collects all item locations available in the state list given that
    # the states have collected items. The purpose is that it will search for
    # all new items that become accessible with a new item set.
    # Alters provided state.
    def collect_locations(self):
        # Get all item locations in the worlds
        item_locations = {location for state in self.state_list for location in state.world.get_filled_locations() if location.item.advancement}
        collected_locations = [s.collected_locations for s in self.state_list]
        for location in self.iter_reachable_locations(item_locations):
            # Mark the location collected in the state world it exists in
            collected_locations[location.world.id][location.name] = True
            # Collect the item for the state world it is for
            self.state_list[location.item.world.id].collect(location.item)

    # This returns True if every state is beatable. It's important to ensure
    # all states beatable since items required in one world can be in another.
    def can_beat_game(self, scan_for_items=True):
        if scan_for_items:
            # Check if already beaten
            game_beaten = True
            for state in self.state_list:
                if not state.has('Triforce'):
                    game_beaten = False
                    break
            if game_beaten:
                return True

            # collect all available items
            # make a new playthrough since we might be iterating over one already
            playthrough = Playthrough([state.copy() for state in self.state_list])
            # we only need to copy the top sphere since that's what we're starting with and we don't go back
            if self.region_spheres:
                playthrough.region_spheres = [tuple(map(copy.copy, self.region_spheres[-1]))]
            playthrough.collect_locations()
        else:
            playthrough = self

        # if the every state got the Triforce, then return True
        for state in playthrough.state_list:
            if not state.has('Triforce'):
                return False
        return True

