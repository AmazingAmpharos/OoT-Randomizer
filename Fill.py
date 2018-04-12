import random
import logging

class FillError(RuntimeError):
    pass

def fill_restrictive(world, base_state, locations, itempool):
    def sweep_from_pool():
        new_state = base_state.copy()
        for item in itempool:
            new_state.collect(item, True)
        new_state.sweep_for_events()
        return new_state

    while itempool and locations:
        item_to_place = itempool.pop()
        maximum_exploration_state = sweep_from_pool()

        perform_access_check = True
        if world.check_beatable_only:
            perform_access_check = not world.has_beaten_game(maximum_exploration_state)


        spot_to_fill = None
        for location in locations:
            if location.can_fill(maximum_exploration_state, item_to_place, perform_access_check):
                spot_to_fill = location
                break

        if spot_to_fill is None:
            # we filled all reachable spots. Maybe the game can be beaten anyway?
            if world.can_beat_game():
                if not world.check_beatable_only:
                    logging.getLogger('').warning('Not all items placed. Game beatable anyway.')
                break
            raise FillError('No more spots to place %s' % item_to_place)

        world.push_item(spot_to_fill, item_to_place, False)
        locations.remove(spot_to_fill)
        spot_to_fill.event = True


def distribute_items_restrictive(world, fill_locations=None):
    # If not passed in, then get a shuffled list of locations to fill in
    if not fill_locations:
        fill_locations = world.get_unfilled_locations()
        random.shuffle(fill_locations)

    # get items to distribute
    random.shuffle(world.itempool)
    progitempool = [item for item in world.itempool if item.advancement]
    prioitempool = [item for item in world.itempool if not item.advancement and item.priority]
    restitempool = [item for item in world.itempool if not item.advancement and not item.priority]

    random.shuffle(fill_locations)
    fill_locations.reverse()

    fill_restrictive(world, world.state, fill_locations, progitempool)

    random.shuffle(fill_locations)

    fill_restrictive_fast(world, world.state, fill_locations, prioitempool)

    random.shuffle(fill_locations)

    fast_fill(world, restitempool, fill_locations)

    logging.getLogger('').debug('Unplaced items: %s - Unfilled Locations: %s', [item.name for item in progitempool + prioitempool + restitempool], [location.name for location in fill_locations])


def fast_fill(world, item_pool, fill_locations):
    while item_pool and fill_locations:
        spot_to_fill = fill_locations.pop()
        item_to_place = item_pool.pop()
        world.push_item(spot_to_fill, item_to_place, False)

def fill_restrictive_fast(world, base_state, locations, itempool):
    def sweep_from_pool():
        new_state = base_state.copy()
        for item in itempool:
            new_state.collect(item, True)
        new_state.sweep_for_events()
        return new_state

    while itempool and locations:
        item_to_place = itempool.pop()

        spot_to_fill = None
        for location in locations:
            if location.can_fill_fast(item_to_place):
                spot_to_fill = location
                break

        if spot_to_fill is None:
            # we filled all reachable spots. Maybe the game can be beaten anyway?
            if world.can_beat_game():
                logging.getLogger('').warning('Not all items placed. Game beatable anyway.')
                break
            raise FillError('No more spots to place %s' % item_to_place)

        world.push_item(spot_to_fill, item_to_place, False)
        locations.remove(spot_to_fill)
        spot_to_fill.event = True