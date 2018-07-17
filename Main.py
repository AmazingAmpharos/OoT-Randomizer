from collections import OrderedDict
from itertools import zip_longest
import json
import logging
import platform
import random
import subprocess
import time
import os

from BaseClasses import World, CollectionState, Item
from EntranceShuffle import link_entrances
from Rom import patch_rom, LocalRom
from Regions import create_regions
from Dungeons import create_dungeons
from Rules import set_rules
from Fill import distribute_items_restrictive
from ItemList import generate_itempool
from Utils import default_output_path
from version import __version__

def main(settings):
    start = time.clock()

    # initialize the world

    worlds = []

    if not settings.world_count:
        settings.world_count = 1
    if settings.world_count < 1:
        raise Exception('World Count must be at least 1')
    if settings.player_num > settings.world_count or settings.player_num < 1:
        raise Exception('Player Num must be between 1 and %d' % settings.world_count)

    for i in range(0, settings.world_count):
        worlds.append(World(settings))

    logger = logging.getLogger('')

    random.seed(worlds[0].numeric_seed)

    logger.info('OoT Randomizer Version %s  -  Seed: %s\n\n', __version__, worlds[0].seed)

    for id, world in enumerate(worlds):
        world.id = id
        logger.info('Generating World %d.' % id)

        logger.info('Creating Overworld')
        create_regions(world)
        logger.info('Creating Dungeons')
        create_dungeons(world)
        logger.info('Linking Entrances')
        link_entrances(world)
        logger.info('Calculating Access Rules.')
        set_rules(world)
        logger.info('Generating Item Pool.')
        generate_itempool(world)

    logger.info('Fill the world.')
    distribute_items_restrictive(worlds)

    logger.info('Calculating playthrough.')
    create_playthrough(worlds)

    logger.info('Patching ROM.')

    if settings.world_count > 1:
        outfilebase = 'OoT_%s_%s_W%dP%d' % (worlds[0].settings_string, worlds[0].seed, worlds[0].world_count, worlds[0].player_num)
    else:
        outfilebase = 'OoT_%s_%s' % (worlds[0].settings_string, worlds[0].seed)

    output_dir = default_output_path(settings.output_dir)

    if not settings.suppress_rom:
        rom = LocalRom(settings)
        patch_rom(worlds[settings.player_num - 1], rom)

        rom_path = os.path.join(output_dir, '%s.z64' % outfilebase)

        rom.write_to_file(rom_path)
        if settings.compress_rom:
            logger.info('Compressing ROM.')
            if platform.system() == 'Windows':
                subprocess.call(["Compress\\Compress.exe", rom_path, os.path.join(output_dir, '%s-comp.z64' % outfilebase)])
            elif platform.system() == 'Linux':
                subprocess.call(["Compress/Compress", ('%s.z64' % outfilebase)])
            elif platform.system() == 'Darwin':
                subprocess.call(["Compress/Compress.out", ('%s.z64' % outfilebase)])
            else:
                logger.info('OS not supported for compression')

    if settings.create_spoiler:
        worlds[settings.player_num - 1].spoiler.to_file(os.path.join(output_dir, '%s_Spoiler.txt' % outfilebase))

    logger.info('Done. Enjoy.')
    logger.debug('Total Time: %s', time.clock() - start)

    return worlds[settings.player_num - 1]

def create_playthrough(worlds):
    if worlds[0].check_beatable_only and not CollectionState.can_beat_game([world.state for world in worlds]):
        raise RuntimeError('Uncopied is broken too.')
    # create a copy as we will modify it
    old_worlds = worlds
    worlds = [world.copy() for world in worlds]

    # if we only check for beatable, we can do this sanity check first before writing down spheres
    if worlds[0].check_beatable_only and not CollectionState.can_beat_game([world.state for world in worlds]):
        raise RuntimeError('Cannot beat game. Something went terribly wrong here!')

    state_list = [CollectionState(world) for world in worlds]
    cached_state_list = [[state.copy() for state in state_list]]

    # Get all item locations in the worlds
    collection_spheres = []
    item_locations = [location for state in state_list for location in state.world.get_filled_locations() if location.item.advancement]

    # in the first phase, we create the generous spheres. Collecting every item in a sphere will
    # mean that every item in the next sphere is collectable. Will contain every reachable item
    logging.getLogger('').debug('Building up collection spheres.')

    # will loop if there is more items opened up in the previous iteration. Always run once
    reachable_items_locations = True
    while reachable_items_locations:
        # get reachable new items locations
        reachable_items_locations = [location for location in item_locations if location.name not in state_list[location.world.id].collected_locations and state_list[location.world.id].can_reach(location)]
        for location in reachable_items_locations:
            # Mark the location collected in the state world it exists in
            state_list[location.world.id].collected_locations.append(location.name)
            # Collect the item for the state world it is for
            state_list[location.item.world.id].collect(location.item)
        if reachable_items_locations:
            collection_spheres.append(reachable_items_locations)
            cached_state_list.append([state.copy() for state in state_list])

    # in the second phase, we cull each sphere such that the game is still beatable, reducing each 
    # range of influence to the bare minimum required inside it. Effectively creates a min play
    for num, sphere in reversed(list(enumerate(collection_spheres))):
        to_delete = []
        for location in sphere:
            # we remove the item at location and check if game is still beatable
            logging.getLogger('').debug('Checking if %s is required to beat the game.', location.item.name)
            old_item = location.item
            location.item = None
            if CollectionState.can_beat_game(cached_state_list[num]):
                to_delete.append(location)
            else:
                # still required, got to keep it around
                location.item = old_item

        # cull entries in spheres for spoiler walkthrough at end
        for location in to_delete:
            sphere.remove(location)

    # we are now down to just the required progress items in collection_spheres. Unfortunately
    # the previous pruning stage could potentially have made certain items dependant on others
    # in the same or later sphere (because the location had 2 ways to access but the item originally
    # used to access it was deemed not required.) So we need to do one final sphere collection pass
    # to build up the correct spheres
    required_locations = [item for sphere in collection_spheres for item in sphere]
    state_list = cached_state_list[0]
    collection_spheres = []
    reachable_items_locations = True
    while reachable_items_locations:
        # get reachable new items locations
        reachable_items_locations = [location for location in required_locations if location.name not in state_list[location.world.id].collected_locations and state_list[location.world.id].can_reach(location)]
        for location in reachable_items_locations:
            # Mark the location collected in the state world it exists in
            state_list[location.world.id].collected_locations.append(location.name)
            # Collect the item for the state world it is for
            state_list[location.item.world.id].collect(location.item)
        if reachable_items_locations:
            collection_spheres.append(reachable_items_locations)

    logging.getLogger('').debug('Calculated final sphere %i, containing %i of %i progress items.', len(collection_spheres), len(sphere), len(required_locations))
    if not sphere:
        raise RuntimeError('Not all required items reachable. Something went terribly wrong here.')

    def flist_to_iter(node):
        while node:
            value, node = node
            yield value

    def get_path(state, region):
        reversed_path_as_flist = state.path.get(region, (region, None))
        string_path_flat = reversed(list(map(str, flist_to_iter(reversed_path_as_flist))))
        # Now we combine the flat string list into (region, exit) pairs
        pathsiter = iter(string_path_flat)
        pathpairs = zip_longest(pathsiter, pathsiter)
        return list(pathpairs)


    # we can finally output our playthrough
    for world in old_worlds:
        world.required_locations = [location for sphere in collection_spheres for location in sphere]
        world.spoiler.playthrough = OrderedDict([(str(i + 1), {location: location.item for location in sphere}) for i, sphere in enumerate(collection_spheres)])
        world.spoiler.paths = {location.name : get_path(world.state, location.parent_region) for sphere in collection_spheres for location in sphere}

