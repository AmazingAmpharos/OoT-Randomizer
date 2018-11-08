from collections import OrderedDict
import logging
import platform
import random
import subprocess
import time
import os, os.path
import sys
import struct
import zlib
import pickle

from BaseClasses import World, CollectionState, Spoiler
from EntranceShuffle import link_entrances
from Rom import LocalRom
from Patches import patch_rom, patch_cosmetics
from Regions import create_regions
from Dungeons import create_dungeons
from Rules import set_rules
from Fill import distribute_items_restrictive
from ItemList import generate_itempool
from Hints import buildGossipHints
from Utils import default_output_path, is_bundled, subprocess_args
from version import __version__
from OcarinaSongs import verify_scarecrow_song_str
from Settings import setting_infos
from N64Patch import create_patch_file, apply_patch_file

class dummy_window():
    def __init__(self):
        pass
    def update_status(self, text):
        pass
    def update_progress(self, val):
        pass

def main(settings, window=dummy_window()):

    start = time.clock()

    logger = logging.getLogger('')

    worlds = []

    # load worlds from patch file
    if settings.patch_file_action == 'load':
        logger.info('Unpacking World File.')
        patch_file = open(settings.patch_file, 'rb')
        compressed_data = patch_file.read()
        worlds = pickle.loads(zlib.decompress(compressed_data))
        patch_file.close()

        # Get settings from patch file
        for setting in filter(lambda s: s.shared and s.bitwidth > 0, setting_infos):
            settings.__dict__[setting.name] = worlds[0].__dict__[setting.name]
        settings.count = 1
        settings.settings_string = worlds[0].settings_string
        settings.update_seed(worlds[0].seed)

        for world in worlds:
            world.settings = settings
            world.__dict__.update(settings.__dict__)

        if settings.player_num > settings.world_count or settings.player_num < 1:
            raise Exception('Player Num must be between 1 and %d' % settings.world_count)

    # verify that the settings are valid
    if settings.free_scarecrow:
        verify_scarecrow_song_str(settings.scarecrow_song, settings.ocarina_songs)

    # we load the rom before creating the seed so that error get caught early
    if settings.compress_rom != 'None':
        window.update_status('Loading ROM')
        rom = LocalRom(settings)

    # initialize the world
    if settings.patch_file_action != 'load':
        if settings.compress_rom == 'None':
            settings.create_spoiler = True
            settings.update()

        if not settings.world_count:
            settings.world_count = 1
        if settings.world_count < 1 or settings.world_count > 31:
            raise Exception('World Count must be between 1 and 31')
        if settings.player_num > settings.world_count or settings.player_num < 1:
            raise Exception('Player Num must be between 1 and %d' % settings.world_count)

        for i in range(0, settings.world_count):
            worlds.append(World(settings))

        random.seed(worlds[0].numeric_seed)

        logger.info('OoT Randomizer Version %s  -  Seed: %s\n\n', __version__, worlds[0].seed)

        window.update_status('Creating the Worlds')
        for id, world in enumerate(worlds):
            world.id = id
            logger.info('Generating World %d.' % id)

            world.spoiler = Spoiler(worlds)

            window.update_progress(0 + 1*(id + 1)/settings.world_count)
            logger.info('Creating Overworld')

            # Determine MQ Dungeons
            td_count = len(world.dungeon_mq)
            if world.mq_dungeons_random:
                world.mq_dungeons = random.randint(0, td_count)
            mqd_count = world.mq_dungeons
            mqd_picks = random.sample(list(world.dungeon_mq), mqd_count)
            for dung in mqd_picks:
                world.dungeon_mq[dung] = True

            create_regions(world)

            window.update_progress(0 + 2*(id + 1)/settings.world_count)
            logger.info('Creating Dungeons')
            create_dungeons(world)

            window.update_progress(0 + 3*(id + 1)/settings.world_count)
            logger.info('Linking Entrances')
            link_entrances(world)

            if settings.shopsanity != 'off':
                world.random_shop_prices()

            window.update_progress(0 + 4*(id + 1)/settings.world_count)
            logger.info('Calculating Access Rules.')
            set_rules(world)

            window.update_progress(0 + 5*(id + 1)/settings.world_count)
            logger.info('Generating Item Pool.')
            generate_itempool(world)

        window.update_status('Placing the Items')
        logger.info('Fill the world.')
        distribute_items_restrictive(window, worlds)
        window.update_progress(35)

        if settings.create_spoiler:
            window.update_status('Calculating Spoiler Data')
            logger.info('Calculating playthrough.')
            create_playthrough(worlds)
            window.update_progress(50)
        if settings.hints != 'none':
            window.update_status('Calculating Hint Data')
            CollectionState.update_required_items(worlds)
            for world in worlds:
                buildGossipHints(worlds, world)
            window.update_progress(55)

    logger.info('Patching ROM.')

    if settings.world_count > 1:
        outfilebase = 'OoT_%s_%s_W%dP%d' % (worlds[0].settings_string, worlds[0].seed, settings.world_count, settings.player_num)
    else:
        outfilebase = 'OoT_%s_%s' % (worlds[0].settings_string, worlds[0].seed)

    output_dir = default_output_path(settings.output_dir)


    if settings.patch_file_action == 'load':
        # restore rand state for correct post fill state
        random.setstate(worlds[0].rand_state)
    else:
        # save the random state
        worlds[0].rand_state = random.getstate()

    if settings.compress_rom != 'None':
        window.update_status('Patching ROM')
        patch_rom(worlds[settings.player_num - 1], rom)
        patch_cosmetics(worlds[settings.player_num - 1], rom)
        window.update_progress(65)

        rom_path = os.path.join(output_dir, '%s.z64' % outfilebase)

        window.update_status('Saving Uncompressed ROM')
        rom.write_to_file(rom_path)
        if settings.compress_rom == 'True':
            window.update_status('Compressing ROM')
            logger.info('Compressing ROM.')

            if is_bundled():
                compressor_path = "."
            else:
                compressor_path = "Compress"

            if platform.system() == 'Windows':
                if 8 * struct.calcsize("P") == 64:
                    compressor_path += "\\Compress.exe"
                else:
                    compressor_path += "\\Compress32.exe"
            elif platform.system() == 'Linux':
                compressor_path += "/Compress"
            elif platform.system() == 'Darwin':
                compressor_path += "/Compress.out"
            else:
                compressor_path = ""
                logger.info('OS not supported for compression')

            if compressor_path != "":
                run_process(window, logger, [compressor_path, rom_path, os.path.join(output_dir, '%s-comp.z64' % outfilebase)])
            os.remove(rom_path)
            window.update_progress(95)

    for world in worlds:
        for setting in world.settings.__dict__:
            world.settings.__dict__[setting] = world.__dict__[setting]

    if settings.create_spoiler:
        window.update_status('Creating Spoiler Log')
        worlds[settings.player_num - 1].spoiler.to_file(os.path.join(output_dir, '%s_Spoiler.txt' % outfilebase))

    if settings.patch_file_action == 'save':
        create_world_file(logger, worlds, output_dir)

    window.update_progress(100)
    window.update_status('Success: Rom patched successfully')
    logger.info('Done. Enjoy.')
    logger.debug('Total Time: %s', time.clock() - start)

    return worlds[settings.player_num - 1]


def run_process(window, logger, args):
    process = subprocess.Popen(args, **subprocess_args(True))
    filecount = None
    while True:
        line = process.stdout.readline()
        if line != b'':
            find_index = line.find(b'files remaining')
            if find_index > -1:
                files = int(line[:find_index].strip())
                if filecount == None:
                    filecount = files
                window.update_progress(65 + 30*(1 - files/filecount))
            logger.info(line.decode('utf-8').strip('\n'))
        else:
            break


def create_playthrough(worlds):
    if worlds[0].check_beatable_only and not CollectionState.can_beat_game([world.state for world in worlds]):
        raise RuntimeError('Uncopied is broken too.')
    # create a copy as we will modify it
    old_worlds = worlds
    worlds = [world.copy() for world in worlds]

    # if we only check for beatable, we can do this sanity check first before writing down spheres
    if worlds[0].check_beatable_only and not CollectionState.can_beat_game([world.state for world in worlds]):
        raise RuntimeError('Cannot beat game. Something went terribly wrong here!')

    state_list = [world.state for world in worlds]

    # Get all item locations in the worlds
    required_locations = []
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
            state_list[location.world.id].collected_locations[location.name] = True
            # Collect the item for the state world it is for
            state_list[location.item.world.id].collect(location.item)
            required_locations.append(location)

    # in the second phase, we cull each sphere such that the game is still beatable, reducing each
    # range of influence to the bare minimum required inside it. Effectively creates a min play
    for location in reversed(required_locations):
        # we remove the item at location and check if game is still beatable
        logging.getLogger('').debug('Checking if %s is required to beat the game.', location.item.name)
        old_item = location.item

        # Uncollect the item location. Removing it from the collected_locations
        # will ensure that can_beat_game will try to collect it if it can.
        # Because we search in reverse sphere order, all the later spheres will
        # have their locations flagged to be re-searched.
        location.item = None
        state_list[old_item.world.id].remove(old_item)
        del state_list[location.world.id].collected_locations[location.name]

        # remove the item from the world and test if the game is still beatable
        if CollectionState.can_beat_game(state_list):
            # cull entries for spoiler walkthrough at end
            required_locations.remove(location)
        else:
            # still required, got to keep it around
            location.item = old_item

    # This ensures the playthrough shows items being collected in the proper order.
    collection_spheres = []
    while required_locations:
        sphere = [location for location in required_locations if state_list[location.world.id].can_reach(location)]
        for location in sphere:
            required_locations.remove(location)
            state_list[location.item.world.id].collect(location.item)
        collection_spheres.append(sphere)

    # we can finally output our playthrough
    for world in old_worlds:
        world.spoiler.playthrough = OrderedDict([(str(i + 1), {location: location.item for location in sphere}) for i, sphere in enumerate(collection_spheres)])


class world_id:
    def __init__(self, id):
        self.id = id


def create_world_file(logger, worlds, output_dir):
    logger.info('Creating World File.')

    # Remove references to Lambdas so that pickle works
    for world in worlds:
        # delete the cache and state
        world._cached_locations = None
        world._entrance_cache = {}
        world._region_cache = {}
        world._location_cache = {}
        world.state = None

        # delete the spoiler world rules
        if world.spoiler and world.spoiler.playthrough:
            for location in [location for _,sphere in world.spoiler.playthrough.items() for location in sphere]:
                location.access_rule = None
                location.item_rule = None
                location.always_allow = None
                location.parent_region = None
                location.world = world_id(location.world.id)
        if world.spoiler:
            for location in [location for _,world_locations in world.spoiler.required_locations.items() for location in world_locations]:
                location.access_rule = None
                location.item_rule = None
                location.always_allow = None
                location.parent_region = None
                location.world = world_id(location.world.id)

        # delete the main world rules
        for region in world.regions:
            region.can_reach = None
            for entrance in region.entrances:
                entrance.access_rule = None
            for entrance in region.exits:
                entrance.access_rule = None
            for location in region.locations:
                location.access_rule = None
                location.item_rule = None
                location.always_allow = None

    # Remove setting fields that will be overwritten
    settings = worlds[0].settings
    for setting in filter(lambda s: not (s.shared and s.bitwidth > 0), setting_infos):
        if setting.name not in ['seed', 'count', 'player_num']:
            settings.__dict__[setting.name] = None
    for world in worlds:
        world.settings = settings
        world.__dict__.update(settings.__dict__)

    compressed_data = zlib.compress(pickle.dumps(worlds))
    filename = 'OoT_%s_%s_W%d.wf' % (worlds[0].settings_string, worlds[0].seed, worlds[0].world_count)
    patch_file = open(os.path.join(output_dir, filename), 'wb')
    patch_file.write(compressed_data)
    patch_file.close()
