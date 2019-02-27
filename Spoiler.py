from version import __version__
from collections import OrderedDict
from Item import Item
from Hints import gossipLocations
from ItemPool import boss_location_names
import re
import random
import json

HASH_ICONS = [
    'Deku Stick',
    'Deku Nut',
    'Bow',
    'Slingshot',
    'Fairy Ocarina',
    'Bombchu',
    'Longshot',
    'Boomerang',
    'Lens of Truth',
    'Beans',
    'Hammer',
    'Bottled Fish',
    'Bottled Milk',
    'Mask of Truth',
    'SOLD OUT',
    'Cucco',
    'Mushroom',
    'Saw',
    'Frog',
    'Master Sword',
    'Mirror Shield',
    'Kokiri Tunic',
    'Hover Boots',
    'Silver Gauntlets',
    'Gold Scale',
    'Stone of Agony',
    'Skull Token',
    'Heart Container',
    'Boss Key',
    'Compass',
    'Map',
    'Big Magic',
]

class Spoiler(object):

    def __init__(self, worlds):
        self.worlds = worlds
        self.settings = worlds[0].settings
        self.playthrough = {}
        self.locations = {}
        self.metadata = {}
        self.required_locations = {}
        self.hints = {world.id: {} for world in worlds}
        self.file_hash = []


    def build_file_hash(self):
        dist_file_hash = self.settings.distribution.file_hash
        for i in range(5):
            self.file_hash.append(random.randint(0,31) if dist_file_hash[i] is None else HASH_ICONS.index(dist_file_hash[i]))


    def parse_data(self):
        self.locations = {}
        for world in self.worlds:
            spoiler_locations = [location for location in world.get_locations() if not location.locked and location.type != 'GossipStone']
            sort_order = {"Song": 0, "Boss": -1}
            spoiler_locations.sort(key=lambda item: sort_order.get(item.type, 1))
            self.locations[world.id] = OrderedDict([(str(location), location.item) for location in spoiler_locations])
