import random
import logging
from State import State
from Rules import set_entrances_based_rules


class EntranceShuffleError(RuntimeError):
    pass


# Set entrances of all worlds, first initializing them to their default regions, then potentially shuffling part of them
def set_entrances(worlds):
    for world in worlds:
        world.initialize_entrances()

    shuffle_entrances(worlds)

    set_entrances_based_rules(worlds)


# Shuffles entrances that need to be shuffled in all worlds
def shuffle_entrances(worlds):

    # Store all locations unreachable to differentiate which locations were already unreachable from those we made unreachable while shuffling entrances
    complete_itempool = [item for world in worlds for item in world.get_itempool_with_dungeon_items()]
    maximum_exploration_state_list = State.get_states_with_items([world.state for world in worlds], complete_itempool)

    all_locations = [location for world in worlds for location in world.get_locations()]
    already_unreachable_locations = [location for location in all_locations if not maximum_exploration_state_list[location.world.id].can_reach(location)]

    # Figure out which entrances should be shuffled based on settings
    entrances_to_shuffle_dict = {} # To replace by a dict of target regions of entrances to shuffle

    # Shuffle entrances only within their own world
    for world in worlds:
        
        # Initialize entrances to shuffle with their addresses and shuffle type
        entrances_to_shuffle = []
        for entrance_name, (type, addresses) in entrances_to_shuffle_dict.items():
            entrance = world.get_entrance(entrance_name)
            entrance.type = type
            entrance.addresses = addresses
            entrance.shuffled = True
            entrances_to_shuffle.append(entrance)

        target_regions = [entrance.connected_region for entrance in entrances_to_shuffle]

        if not entrances_to_shuffle:
            continue

        if len(entrances_to_shuffle) != len(target_regions):
            raise EntranceShuffleError('There should be the same amount of entrances to shuffle as regions to connect, but found %d entrances and %d regions'
                                        % (len(entrances_to_shuffle), len(target_regions)))

        # Shuffle all entrances once first to remove any potential bias
        random.shuffle(entrances_to_shuffle)

        # Split entrances to shuffle based on their requirements (primarly age requirements)
        # One of the reasons is that some entrances are more limited so they should be placed first while more regions are available.
        # The other reason is some entrances are versatile enough that we don't need to check for reachability/beatability when shuffling them
        access_limited_entrances, age_limited_entrances, soft_entrances = split_entrances_by_requirements(worlds, entrances_to_shuffle)

        # First, shuffle entrances that have potentially high access requirements
        # These entrances may be completely innaccessible in some combination of entrances, so we place them first
        shuffle_entrances_restrictive(worlds, access_limited_entrances, target_regions, already_unreachable_locations, entrances_to_shuffle_dict)

        # Then, shuffle entrances with a possible limited age access
        # These entrances may not be accessible as both ages in some combination of entrances, so we place them in second
        shuffle_entrances_restrictive(worlds, age_limited_entrances, target_regions, already_unreachable_locations, entrances_to_shuffle_dict)

        # Finally, shuffle the rest of the entrances that are especially versatile
        # These entrances will always be accessible as both ages no matter which combination of entraces we end up with
        # Thus, they can be placed without checking for reachability because they have no risk of making locations innaccessible
        shuffle_entrances_fast(worlds, soft_entrances, target_regions, entrances_to_shuffle_dict)

    # Multiple checks after shuffling entrances to make sure everything went fine

    for world in worlds:
        entrances_shuffled = [world.get_entrance(entrance_name) for entrance_name in entrances_to_shuffle_dict]

        # Log all entrance replacements
        for entrance in entrances_shuffled:
            logging.getLogger('').debug('%s replaces %s [World %d]', entrance, entrance.replaces, world.id)

        # Check that all target regions have exactly one entrance among those we shuffled
        target_regions = [entrance.connected_region for entrance in entrances_shuffled]
        for region in target_regions:
            region_shuffled_entrances = list(filter(lambda entrance: entrance in entrances_shuffled, region.entrances))
            if len(region_shuffled_entrances) != 1:
                logging.getLogger('').error('%s has %d shuffled entrances after shuffling, expected exactly 1 [World %d]', 
                                                region, len(region_shuffled_entrances), world.id)

    maximum_exploration_state_list = State.get_states_with_items([world.state for world in worlds], complete_itempool)

    # Log all locations unreachable due to shuffling entrances
    alr_compliant = True
    if not worlds[0].check_beatable_only:
        for location in all_locations:
            if not location in already_unreachable_locations and \
               not maximum_exploration_state_list[location.world.id].can_reach(location):
                logging.getLogger('').error('Location now unreachable after shuffling entrances: %s [World %d]', location, location.world.id)
                alr_compliant = False

    # Check for game beatability in all worlds
    if not State.can_beat_game(maximum_exploration_state_list):
        raise EntranceShuffleError('Cannot beat game!')

    # Throw an error if shuffling entrances broke the contract of ALR (All Locations Reachable)
    if not alr_compliant:
        raise EntranceShuffleError('ALR is enabled but not all locations are reachable!')


# Split entrances based on their requirements to figure out how each entrance should be handled when shuffling them
# This is done to ensure that we can place them in an order less likely to fail, and with the appropriate method to optimize the placement speed
# Indeed, some entrances should be handled before others, and this also allows us to determine which entrances don't need to check for reachability
# If all entrances were handled in a random order, the algorithm could have high chances to fail to connect the last few entrances because of requirements
def split_entrances_by_requirements(worlds, entrances_to_split):

    # Retrieve all items in the itempool, all worlds included
    complete_itempool = [item for world in worlds for item in world.get_itempool_with_dungeon_items()]

    # First, disconnect all entrances and save which regions they were originally connected to, so we can reconnect them later
    original_connected_regions = {}
    for entrance in entrances_to_split:
        original_connected_regions[entrance.name] = entrance.disconnect()

    # Generate the states with all entrances disconnected
    # This ensures that no pre exisiting entrances among those to shuffle are required in order for an entrance to be reachable as one age
    # Some entrances may not be reachable because of this, but this is fine as long as we deal with those entrances as being very limited
    maximum_exploration_state_list = State.get_states_with_items([world.state for world in worlds], complete_itempool)

    access_limited_entrances = []
    age_limited_entrances = []
    soft_entrances = []

    for entrance in entrances_to_split:
        # Here we look for entrances unreachable in both ages (because of other entrances being disconnected)
        if not maximum_exploration_state_list[entrance.world.id].can_reach(entrance, age='either'):
            access_limited_entrances.append(entrance)
            continue
        # Here, we find entrances that are only reachable as one age (with all other entrances disconnected)
        if not maximum_exploration_state_list[entrance.world.id].can_reach(entrance, age='both'):
            age_limited_entrances.append(entrance)
            continue
        # If an entrance is reachable as both ages with all the other entrances disconnected,
        # then it will always be accessible as both ages no matter which combination of entrances we end up with.
        # Thus, those entrances aren't bound to any specific requirements and are very versatile
        soft_entrances.append(entrance)

    # Reconnect all entrances afterwards
    for entrance in entrances_to_split:
        entrance.connect(original_connected_regions[entrance.name])

    return access_limited_entrances, age_limited_entrances, soft_entrances


# Shuffle entrances by connecting them to a region among the provided target regions list
# While shuffling entrances, the algorithm will use states generated from all items yet to be placed to figure how entrances can be placed
# If ALR is enabled, this will mean checking that all locations previously reachable are still reachable every time we try to place an entrance
# Otherwise, only the beatability of the game may be assured, which is what would be expected without ALR enabled
def shuffle_entrances_restrictive(worlds, entrances, target_regions, already_unreachable_locations, all_entrances):

    all_locations = [location for world in worlds for location in world.get_locations()]

    # Retrieve all items in the itempool, all worlds included
    complete_itempool = [item for world in worlds for item in world.get_itempool_with_dungeon_items()]

    maximum_exploration_state_list = []

    while entrances:
        random.shuffle(target_regions)

        # Get an entrance to place and disconnect it from its current region
        entrance_to_place = entrances.pop()

        # Loop through all remaining regions and try to find one that can be connected (which could involve checking for reachability)
        connected_region = None

        for tested_region in target_regions:

            # If the tested region is the same as the region connected originally, we can just use that entrance without any extra checks
            if tested_region == entrance_to_place.connected_region:
                connected_region = tested_region
                break

            can_connect = True

            # Swap the entrances between the tested region and the region connected originally
            other_entrance = next(filter(lambda entrance: entrance.name in all_entrances, tested_region.entrances))
            entrance_to_place.swap_connections(other_entrance)

            # Regenerate the states because the final states might have changed after connecting/disconnecting entrances
            # We also clear all state caches first because what was reachable before could now be unreachable and vice versa
            for maximum_exploration_state in maximum_exploration_state_list:
                maximum_exploration_state.clear_cache()
            maximum_exploration_state_list = State.get_states_with_items([world.state for world in worlds], complete_itempool)

            # If we only have to check that the game is still beatable, and the game is indeed still beatable, we can use that region
            if not (worlds[0].check_beatable_only and State.can_beat_game(maximum_exploration_state_list)):

                # Figure out if this entrance can be connected to the region being tested
                # We consider that it can be connected if ALL locations previously reachable are still reachable
                for location in all_locations:
                    if not location in already_unreachable_locations and \
                       not maximum_exploration_state_list[location.world.id].can_reach(location):
                        logging.getLogger('').debug('Failed to connect %s To %s (because of %s) [World %d]',
                                                        entrance_to_place, tested_region, location, entrance_to_place.world.id)
                        can_connect = False
                        break

            if can_connect:
                # If the entrance can successfully be connected to the region, keep the entrances as is and continue
                connected_region = tested_region
                break
            else:
                # If the tested region is not suitable, swap the entrances back
                entrance_to_place.swap_connections(other_entrance)

        # If we didn't find any suitable region, not all entrances can be placed so we should throw an error
        if connected_region == None:
            raise EntranceShuffleError('Game unbeatable: No more suitable regions to connect %s [World %d]' % (entrance_to_place, entrance_to_place.world.id))

        # Remove the connected region from the pool of target regions
        target_regions.remove(connected_region)

        logging.getLogger('').debug('Connected %s To %s [World %d]', entrance_to_place, connected_region, entrance_to_place.world.id)


# Shuffle entrances by connecting them to a random region among the provided target regions list
# This doesn't check for reachability nor beatability and just connects all entrances to random regions
# This is only meant to be used to shuffle entrances that we already know as completely versatile
# Which means that they can't ever permanently prevent the access of any locations, no matter how they are placed
def shuffle_entrances_fast(worlds, entrances, target_regions, all_entrances):

    while entrances:
        random.shuffle(target_regions)

        entrance_to_place = entrances.pop()
        region_to_connect = target_regions.pop()
        
        # Only swap entrances if needed (i.e. the entrance to place is not already connected to that region)
        if not region_to_connect == entrance_to_place.connected_region:
            other_entrance = next(filter(lambda entrance: entrance.name in all_entrances, region_to_connect.entrances))
            entrance_to_place.swap_connections(other_entrance)

        logging.getLogger('').debug('Connected %s To %s [World %d]', entrance_to_place, region_to_connect, entrance_to_place.world.id)
