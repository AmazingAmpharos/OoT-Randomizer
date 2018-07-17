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
    for i in range(0, 2): # settings.player_count):
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

    outfilebase = 'OoT_%s_%s' % (world.settings_string,  world.seed)
    output_dir = default_output_path(settings.output_dir)

    if not settings.suppress_rom:
        rom = LocalRom(settings)
        patch_rom(world, rom)

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
        world.spoiler.to_file(os.path.join(output_dir, '%s_Spoiler.txt' % outfilebase))

    logger.info('Done. Enjoy.')
    logger.debug('Total Time: %s', time.clock() - start)

    return world

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

    # in the first phase, we create the generous spheres. Collecting every item in a sphere will
    # mean that every item in the next sphere is collectable. Will contain ever reachable item
    logging.getLogger('').debug('Building up collection spheres.')
    collection_spheres = CollectionState.collect_locations(state_list)

    # in the second phase, we cull each sphere such that the game is still beatable, reducing each 
    # range of influence to the bare minimum required inside it. Effectively creates a min play
    state_list = [CollectionState(world) for world in worlds]
    for num, sphere in reversed(list(enumerate(collection_spheres))):
        to_delete = []
        for location in sphere:
            # we remove the item at location and check if game is still beatable
            logging.getLogger('').debug('Checking if %s is required to beat the game.', location.item.name)
            old_item = location.item
            location.item = None
            if CollectionState.can_beat_game(state_list):
                to_delete.append(location)
            else:
                # still required, got to keep it around
                location.item = old_item

        # cull entries in spheres for spoiler walkthrough at end
        for location in to_delete:
            sphere.remove(location)
    collection_spheres = [sphere for sphere in collection_spheres if sphere]

    # we are now down to just the required progress items in collection_spheres. Unfortunately
    # the previous pruning stage could potentially have made certain items dependant on others
    # in the same or later sphere (because the location had 2 ways to access but the item originally
    # used to access it was deemed not required.) So we need to do one final sphere collection pass
    # to build up the correct spheres


#    required_locations = [item for sphere in collection_spheres for item in sphere]
#    state = CollectionState(world)
#    collection_spheres = []
#    while required_locations:
#        state.sweep_for_events(key_only=True)

#        sphere = list(filter(state.can_reach, required_locations))

#        for location in sphere:
#            required_locations.remove(location)
#            state.collect(location.item, True, location)

#        collection_spheres.append(sphere)

#        logging.getLogger('').debug('Calculated final sphere %i, containing %i of %i progress items.', len(collection_spheres), len(sphere), len(required_locations))
#        if not sphere:
#            raise RuntimeError('Not all required items reachable. Something went terribly wrong here.')


    # store the required locations for statistical analysis

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
        world.required_locations = [location.name for sphere in collection_spheres for location in sphere]
        world.spoiler.playthrough = OrderedDict([(str(i + 1), {str(location): str(location.item) for location in sphere}) for i, sphere in enumerate(collection_spheres)])
        world.spoiler.paths = {location.name : get_path(world.state, location.parent_region) for sphere in collection_spheres for location in sphere}

