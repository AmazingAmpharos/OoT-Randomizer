import pickle
import zlib
from Utils import local_path, default_output_path
from SettingsList import setting_infos

class world_id:
    def __init__(self, id):
        self.id = id

def load_world_file(path):
    try:
        with open(local_path(path), 'rb') as patch_file:
            compressed_data = patch_file.read()
            worlds = pickle.loads(zlib.decompress(compressed_data))
    except FileNotFoundError:
        return None

    return worlds

def save_world_file(path, worlds):
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
    with open(path, 'wb') as patch_file:
        patch_file.write(compressed_data)
