import copy
from collections import deque, defaultdict
import itertools


class Playthrough(object):

    def __init__(self, state_list):
        self.state_list = state_list  # reference, not a copy
        # Each cached sphere is a dict with 4 values:
        #  child_regions, adult_regions: sets of Region, all the regions in that sphere
        #  child_queue, adult_queue: queue of Entrance, all the exits to try next sphere
        self.cached_spheres = []

        # Mapping from location to sphere index. 0-based.
        self.location_in_sphere = defaultdict(int)

    # Truncates the sphere cache based on which sphere a location is in.
    # Doesn't forget which sphere locations are in as an optimization, so be careful
    # to only uncollect locations in descending sphere order, or locations that
    # have been revisited in the most recent iteration.
    # Locations never visited in this Playthrough are assumed to be in sphere 0, so
    # uncollecting them will discard everything above sphere 0.
    # Not safe to call during iteration.
    def uncollect(self, location):
        self.cached_spheres[self.location_in_sphere[location]+1:] = []

    # Internal to the iteration. Modifies the exit_queue, region_set,
    # and may modify those for cross_age. Returns a queue of the exits
    # whose access rule failed, as a cache for the exits to try on the next iteration.
    @staticmethod
    def _expand_regions(exit_queue, region_set, validate,
                        cross_age_queue, cross_age_set):
        new_exit = lambda exit: exit.connected_region not in region_set
        failed = []
        while exit_queue:
            exit = exit_queue.popleft()
            if new_exit(exit):
                if validate(exit):
                    region_set.add(exit.connected_region)
                    exit_queue.extend(filter(new_exit, exit.connected_region.exits))
                    if exit.connected_region.name == 'Beyond Door of Time':
                        cross_age_set.add(exit.connected_region)
                        cross_age_queue.extend(exit.connected_region.exits)
                        # Adult savewarp point is Temple of Time, which is
                        # always accessible from BDoT, so we can skip adding it specially
                        # Child savewarp point is Links House, which is
                        # always accessible from BDoT -> ToT -> CT -> HF -> LWB -> KF, so we can skip adding it specially
                else:
                    failed.append(exit)
        return failed


    # Yields every reachable location, by iteratively deepening explored sets of
    # regions (one as child, one as adult) and invoking access rules without
    # calling the recursive can_reach.
    # item_locations is a set of Location objects from state_list that the caller
    # has prefiltered (eg. by whether they contain advancement items).
    #
    # Inside the loop, the caller usually wants to collect items at these
    # locations to see if the game is beatable. This function does not alter provided state.
    def iter_reachable_locations(self, item_locations):
        collected_set = set(itertools.chain.from_iterable(
            map(state.world.get_location, state.collected_locations)
            for id, state in enumerate(self.state_list)))

        new_child_exit = lambda exit: exit.connected_region not in child_regions
        new_adult_exit = lambda exit: exit.connected_region not in adult_regions

        # simplified exit.can_reach(state)
        validate_child = lambda exit: self.state_list[exit.parent_region.world.id].as_child(lambda s: s.with_spot(exit.access_rule, exit))
        validate_adult = lambda exit: self.state_list[exit.parent_region.world.id].as_adult(lambda s: s.with_spot(exit.access_rule, exit))

        # simplified loc.can_reach(state), minus the disable check
        # Check adult first; it's the most likely.
        accessible = lambda loc: (
                loc.parent_region in adult_regions
                and self.state_list[loc.world.id].as_adult(lambda s: s.with_spot(loc.access_rule, loc))
                or (loc.parent_region in child_regions
                    and self.state_list[loc.world.id].as_child(lambda s: s.with_spot(loc.access_rule, loc))))

        had_reachable_locations = True
        # will loop as long as any collections were made, and at least once
        while had_reachable_locations:
            # 0. Use cached regions and queues or initialize starting values.
            if self.cached_spheres:
                child_regions = copy.copy(self.cached_spheres[-1]['child_regions'])
                adult_regions = copy.copy(self.cached_spheres[-1]['adult_regions'])
                # queues of Entrance where the entrance is not yet validated
                child_queue = copy.copy(self.cached_spheres[-1]['child_queue'])
                adult_queue = copy.copy(self.cached_spheres[-1]['adult_queue'])
            else:
                child_regions = {
                        state.world.get_region('Links House') for state in self.state_list
                        if state.world.starting_age == 'child'}
                adult_regions = {
                        state.world.get_region('Temple of Time') for state in self.state_list
                        if state.world.starting_age == 'adult'}
                child_queue = deque(
                        exit for region in child_regions for exit in region.exits
                        if exit.connected_region not in child_regions)
                adult_queue = deque(
                        exit for region in adult_regions for exit in region.exits
                        if exit.connected_region not in adult_regions)

            # 1. Use the queue to iteratively add regions to the accessed set,
            #    until we are stuck or out of regions.
            child_failed = Playthrough._expand_regions(
                    child_queue, child_regions, validate_child,
                    adult_queue, adult_regions)
            adult_failed = Playthrough._expand_regions(
                    adult_queue, adult_regions, validate_adult,
                    child_queue, child_regions)
            # This only does anything with an adult starting state if BDoT was reached.
            if child_queue:
                child_failed.extend(Playthrough._expand_regions(
                        child_queue, child_regions, validate_child,
                        adult_queue, adult_regions))

            # 2. Get all locations in accessible_regions that aren't collected,
            #    and check if they can be reached. Collect them.
            reachable_locations = filter(accessible, item_locations - collected_set)
            had_reachable_locations = False
            for location in reachable_locations:
                had_reachable_locations = True
                yield location
                # Mark it collected for this algorithm
                collected_set.add(location)
                self.location_in_sphere[location] = len(self.cached_spheres)
            # 3. Save the current data into the cache.
            self.cached_spheres.append({
                'child_regions': child_regions,
                'adult_regions': adult_regions,
                # Exits that didn't pass validation (and still point to new places)
                # are the only exits we'll be interested in
                'child_queue': deque(filter(new_child_exit, child_failed)),
                'adult_queue': deque(filter(new_adult_exit, adult_failed)),
            })

    # This collects all item locations available in the state list given that
    # the states have collected items. The purpose is that it will search for
    # all new items that become accessible with a new item set.
    # This function modifies provided state.
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
            if self.cached_spheres:
                playthrough.cached_spheres = [{k: copy.copy(v) for k,v in self.cached_spheres[-1].items()}]
            playthrough.collect_locations()
        else:
            playthrough = self

        # if the every state got the Triforce, then return True
        for state in playthrough.state_list:
            if not state.has('Triforce'):
                return False
        return True

