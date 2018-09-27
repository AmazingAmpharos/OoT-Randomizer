import random
import logging
from BaseClasses import CollectionState
from Rules import set_shop_rules

class FillError(RuntimeError):
    pass

# Places all items into the world
def distribute_items_restrictive(window, worlds, fill_locations=None):
    song_locations = [world.get_location(location) for world in worlds for location in
        ['Song from Composer Grave', 'Impa at Castle', 'Song from Malon', 'Song from Saria', 
        'Song from Ocarina of Time', 'Song at Windmill', 'Sheik Forest Song', 'Sheik at Temple', 
        'Sheik in Crater', 'Sheik in Ice Cavern', 'Sheik in Kakariko', 'Sheik at Colossus']]

    shop_locations = [location for world in worlds for location in world.get_unfilled_locations() if location.type == 'Shop' and location.price == None]

    # If not passed in, then get a shuffled list of locations to fill in
    if not fill_locations:
        fill_locations = [location for world in worlds for location in world.get_unfilled_locations() if location not in song_locations and location not in shop_locations]
    world_states = [world.state for world in worlds]

    window.locationcount = len(fill_locations) + len(song_locations)
    window.fillcount = 0

    # Generate the itempools
    shopitempool = [item for world in worlds for item in world.itempool if item.type == 'Shop']
    songitempool = [item for world in worlds for item in world.itempool if item.type == 'Song']
    itempool =     [item for world in worlds for item in world.itempool if item.type != 'Shop' and item.type != 'Song']
    if worlds[0].shuffle_song_items:
        itempool.extend(songitempool)
        fill_locations.extend(song_locations)

    # add unrestricted dungeon items to main item pool
    itempool.extend([item for world in worlds for item in world.get_unrestricted_dungeon_items()])
    dungeon_items = [item for world in worlds for item in world.get_restricted_dungeon_items()]

    random.shuffle(itempool) # randomize item placement order. this ordering can greatly affect the location accessibility bias
    progitempool = [item for item in itempool if item.advancement]
    prioitempool = [item for item in itempool if not item.advancement and item.priority]
    restitempool = [item for item in itempool if not item.advancement and not item.priority]


    # We place all the shop items first. Like songs, they have a more limited
    # set of locations that they can be placed in, so placing them first will
    # reduce the odds of creating unbeatable seeds. This also avoids needing
    # to create item rules for every location for whether they are a shop item
    # or not. This shouldn't have much affect on item bias.
    if shop_locations:
        random.shuffle(shop_locations)
        fill_shops(window, worlds, shop_locations, shopitempool, itempool + songitempool + dungeon_items)
    # Update the shop item access rules    
    for world in worlds:
        set_shop_rules(world)

    # If there are dungeon items that are restricted to their original dungeon,
    # we must place them first to make sure that there is always a location to
    # place them. This could probably be replaced for more intelligent item
    # placement, but will leave as is for now
    random.shuffle(fill_locations)
    fill_dungeons_restrictive(window, worlds, fill_locations, dungeon_items, itempool + songitempool)
    for world in worlds:
        world.keys_placed = True
        
    # I have no idea why the locations are reversed but this is how it was, 
    # so whatever. It can't hurt I guess
    random.shuffle(fill_locations)
    fill_locations.reverse()

    # places the songs into the world
    # Currently places songs only at song locations. if there's an option
    # to allow at other locations then they should be in the main pool.
    # Placing songs on their own since they have a relatively high chance
    # of failing compared to other item type. So this way we only have retry
    # the song locations only.
    if not worlds[0].shuffle_song_items:
        fill_songs(window, worlds, song_locations, songitempool, progitempool)

    # Put one item in every dungeon, needs to be done before other items are
    # placed to ensure there is a spot available for them
    if worlds[0].one_item_per_dungeon:
        fill_dungeon_unique_item(window, worlds, fill_locations, progitempool)

    # Place all progression items. This will include keys in keysanity.
    # Items in this group will check for reachability and will be placed
    # such that the game is guaranteed beatable.
    random.shuffle(fill_locations)
    fill_restrictive(window, worlds, [world.state for world in worlds], fill_locations, progitempool)

    # Place all priority items.
    # These items are items that only check if the item is allowed to be
    # placed in the location, not checking reachability. This is important
    # for things like Ice Traps that can't be found at some locations
    random.shuffle(fill_locations)
    fill_restrictive_fast(window, worlds, fill_locations, prioitempool)

    # Place the rest of the items.
    # No restrictions at all. Places them completely randomly. Since they
    # cannot affect the beatability, we don't need to check them
    random.shuffle(fill_locations)
    fast_fill(window, fill_locations, restitempool)

    # Log unplaced item/location warnings
    for item in progitempool + prioitempool + restitempool:
        logging.getLogger('').debug('Unplaced Items: %s [World %d]' % (item.name, item.world.id))
    if progitempool + prioitempool + restitempool:
        for item in progitempool + prioitempool + restitempool:
            print('Unplaced Items: %s [World %d]' % (item.name, item.world.id))

        raise FillError('Not all items are placed.')

    if fill_locations:
        for location in fill_locations:
            logging.getLogger('').debug('Unfilled Locations: %s [World %d]' % (location.name, location.world.id))
        raise FillError('Not all locations have an item.')


# Places restricted dungeon items into the worlds. To ensure there is room for them.
# they are placed first so it will assume all other items are reachable
def fill_dungeons_restrictive(window, worlds, shuffled_locations, dungeon_items, itempool):
    # List of states with all non-key items
    all_state_base_list = CollectionState.get_states_with_items([world.state for world in worlds], itempool)

    # shuffle this list to avoid placement bias
    random.shuffle(dungeon_items)

    # sort in the order Boss Key, Small Key, Other before placing dungeon items
    # python sort is stable, so the ordering is still random within groups
    sort_order = {"BossKey": 3, "SmallKey": 2}
    dungeon_items.sort(key=lambda item: sort_order.get(item.type, 1))

    # place dungeon items
    fill_restrictive(window, worlds, all_state_base_list, shuffled_locations, dungeon_items)

    for world in worlds:
        world.state.clear_cached_unreachable()


# Places items into dungeon locations. This is used when there should be exactly
# one progression item per dungeon. This should be ran before all the progression
# items are places to ensure there is space to place them.
def fill_dungeon_unique_item(window, worlds, fill_locations, itempool, attempts=15):
    # We should make sure that we don't count event items, shop items,
    # token items, or dungeon items as a major item. itempool at this
    # point should only be able to have tokens of those restrictions
    # since the rest are already placed.
    major_items = [item for item in itempool if item.type != 'Token']
    token_items = [item for item in itempool if item.type == 'Token']

    while attempts:
        attempts -= 1
        try:
            # choose a random set of items and locations
            dungeon_locations = []
            for dungeon in [dungeon for world in worlds for dungeon in world.dungeons]:
                dungeon_locations.append(random.choice([location for region in dungeon.regions for location in region.locations if location in fill_locations]))
            dungeon_items = random.sample(major_items, len(dungeon_locations))

            new_dungeon_locations = list(dungeon_locations)
            new_dungeon_items = list(dungeon_items)
            non_dungeon_items = [item for item in major_items if item not in dungeon_items]
            all_other_item_state = CollectionState.get_states_with_items([world.state for world in worlds], token_items + non_dungeon_items)

            # attempt to place the items into the locations
            random.shuffle(new_dungeon_locations)
            random.shuffle(new_dungeon_items)
            fill_restrictive(window, worlds, all_other_item_state, new_dungeon_locations, new_dungeon_items)
            if len(new_dungeon_locations) > 0:
                raise FillError('Not all items were placed successfully')

            logging.getLogger('').info("Unique dungeon items placed")

            # remove the placed items from the fill_location and itempool
            for location in dungeon_locations:
                fill_locations.remove(location)
            for item in dungeon_items:
                itempool.remove(item)

        except FillError as e:
            logging.getLogger('').info("Failed to place unique dungeon items. Will retry %s more times", attempts)
            for location in dungeon_locations:
                location.item = None
            for dungeon in [dungeon for world in worlds for dungeon in world.dungeons]:
                dungeon.major_items = 0
            logging.getLogger('').info('\t%s' % str(e))
            continue
        break
    else:
        raise FillError('Unable to place unique dungeon items')


# Places the shop items into the world at the Shop locations
def fill_shops(window, worlds, locations, shoppool, itempool, attempts=15):
    # List of states with all items
    all_state_base_list = CollectionState.get_states_with_items([world.state for world in worlds], itempool)

    while attempts:
        attempts -= 1
        try:
            prizepool = list(shoppool)
            prize_locs = list(locations)
            random.shuffle(prizepool)
            random.shuffle(prize_locs)
            fill_restrictive(window, worlds, all_state_base_list, prize_locs, prizepool)
            logging.getLogger('').info("Shop items placed")
        except FillError as e:
            logging.getLogger('').info("Failed to place shop items. Will retry %s more times", attempts)
            for location in locations:
                location.item = None
            logging.getLogger('').info('\t%s' % str(e))
            continue
        break
    else:
        raise FillError('Unable to place shops')


# Places the songs into the world at the Song locations
def fill_songs(window, worlds, locations, songpool, itempool, attempts=15):
    # get the song locations for each world

    # look for preplaced items
    placed_prizes = [loc.item.name for loc in locations if loc.item is not None]
    unplaced_prizes = [song for song in songpool if song.name not in placed_prizes]
    empty_song_locations = [loc for loc in locations if loc.item is None]

    # List of states with all items
    all_state_base_list = CollectionState.get_states_with_items([world.state for world in worlds], itempool)

    while attempts:
        attempts -= 1
        try:
            prizepool = list(unplaced_prizes)
            prize_locs = list(empty_song_locations)
            random.shuffle(prizepool)
            random.shuffle(prize_locs)
            fill_restrictive(window, worlds, all_state_base_list, prize_locs, prizepool)
            logging.getLogger('').info("Songs placed")
        except FillError as e:
            logging.getLogger('').info("Failed to place songs. Will retry %s more times", attempts)
            for location in empty_song_locations:
                location.item = None
            logging.getLogger('').info('\t%s' % str(e))
            continue
        break
    else:
        raise FillError('Unable to place songs')


# Places items in the itempool into locations.
# worlds is a list of worlds and is redundant of the worlds in the base_state_list
# base_state_list is a list of world states prior to placing items in the item pool
# items and locations have pointers to the world that they belong to
#
# The algorithm places items in the world in reverse.
# This means we first assume we have every item in the item pool and
# remove an item and try to place it somewhere that is still reachable
# This method helps distribution of items locked behind many requirements
def fill_restrictive(window, worlds, base_state_list, locations, itempool):
    # loop until there are no items or locations
    while itempool and locations:
        # get and item and remove it from the itempool
        item_to_place = itempool.pop()

        # generate the max states that include every remaining item
        # this will allow us to place this item in a reachable location
        maximum_exploration_state_list = CollectionState.get_states_with_items(base_state_list, itempool)     

        # perform_access_check checks location reachability
        perform_access_check = True
        if worlds[0].check_beatable_only:
            # if any world can not longer be beatable with the remaining items
            # then we must check for reachability no matter what.
            # This way the reachability test is monotonic. If we were to later
            # stop checking, then we could place an item needed in one world
            # in an unreachable place in another world
            perform_access_check = not CollectionState.can_beat_game(maximum_exploration_state_list)

        # find a location that the item can be places. It must be a valid location
        # in the world we are placing it (possibly checking for reachability)
        spot_to_fill = None
        for location in locations:
            if location.can_fill(maximum_exploration_state_list[location.world.id], item_to_place, perform_access_check):
                spot_to_fill = location
                break

        # if we failed to find a suitable location, then stop placing items
        if spot_to_fill is None:
            raise FillError('Game unbeatable: No more spots to place %s [World %d]' % (item_to_place, item_to_place.world.id))
            
        # Place the item in the world and continue
        spot_to_fill.world.push_item(spot_to_fill, item_to_place)
        locations.remove(spot_to_fill)
        window.fillcount += 1
        window.update_progress(5 + ((window.fillcount / window.locationcount) * 30))


# This places items in the itempool into the locations
# It does not check for reachability, only that the item is
# allowed in the location
def fill_restrictive_fast(window, worlds, locations, itempool):
    while itempool and locations:
        item_to_place = itempool.pop()

        # get location that allows this item
        spot_to_fill = None
        for location in locations:
            if location.can_fill_fast(item_to_place):
                spot_to_fill = location
                break

        # if we failed to find a suitable location, then stop placing items
        # we don't need to check beatability since world must be beatable
        # at this point
        if spot_to_fill is None:
            if not worlds[0].check_beatable_only:
                logging.getLogger('').debug('Not all items placed. Game beatable anyway.')
            break

        # Place the item in the world and continue
        spot_to_fill.world.push_item(spot_to_fill, item_to_place)
        locations.remove(spot_to_fill)
        window.fillcount += 1
        window.update_progress(5 + ((window.fillcount / window.locationcount) * 30))


# this places item in item_pool completely randomly into
# fill_locations. There is no checks for validity since
# there should be none for these remaining items
def fast_fill(window, locations, itempool):
    while itempool and locations:
        spot_to_fill = locations.pop()
        item_to_place = itempool.pop()
        spot_to_fill.world.push_item(spot_to_fill, item_to_place)
        window.fillcount += 1
        window.update_progress(5 + ((window.fillcount / window.locationcount) * 30))
