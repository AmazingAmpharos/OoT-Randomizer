from version import __version__
from collections import OrderedDict
from Item import Item
from Hints import gossipLocations
import re
import random

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
        for _ in range(0,5):
            self.file_hash.append(random.randint(0,31))


    def parse_data(self):
        self.locations = {}
        for world in self.worlds:
            spoiler_locations = [location for location in world.get_locations() if not location.locked and location.type != 'GossipStone']
            sort_order = {"Song": 0, "Boss": -1}
            spoiler_locations.sort(key=lambda item: sort_order.get(item.type, 1))
            self.locations[world.id] = OrderedDict([(str(location), location.item) for location in spoiler_locations])


    def to_file(self, filename):
        self.parse_data()
        with open(filename, 'w') as outfile:
            outfile.write('OoT Randomizer Version %s  -  Seed: %s\n\n' % (__version__, self.settings.seed))

            outfile.write('File Select Hash:\n')
            outfile.write('\n'.join(['    %s' % HASH_ICONS[icon] for icon in self.file_hash]))
            outfile.write('\n\n')

            outfile.write('Settings (%s):\n%s' % (self.settings.get_settings_string(), self.settings.get_settings_display()))

            extra_padding = 1 if self.settings.world_count < 2 else 6 if self.settings.world_count < 10 else 7
            if self.settings.world_count > 1:
                header_world_string = '\n\n{header} [World {world}]:\n\n'
                header_player_string = '\n\n{header} [Player {player}]:\n\n'
                location_string = '{location} [W{world}]:'
                item_string = '{item} [Player {player}]{cost}'
            else:
                header_world_string = '\n\n{header}:\n\n'
                header_player_string = '\n\n{header}:\n\n'
                location_string = '{location}:'
                item_string = '{item}{cost}'

            location_padding = len(max(self.locations[0].keys(), key=len)) + extra_padding
            for world in self.worlds:
                outfile.write(header_world_string.format(header="Locations", world=world.id+1))
                outfile.write('\n'.join(['{:{width}} {}'.format(location_string.format(location=location, world=world.id+1), item_string.format(item=item.name, player=item.world.id+1, cost=' [Costs %d Rupees]' % item.price if item.price is not None else ''), width=location_padding) for (location, item) in self.locations[world.id].items()]))

            outfile.write('\n\nPlaythrough:\n\n')
            outfile.write('\n'.join(['%s: {\n%s\n}' % (sphere_nr, '\n'.join(['  {:{width}} {}'.format(location_string.format(location=location.name, world=location.world.id+1), item_string.format(item=item.name, player=item.world.id+1, cost=' [Costs %d Rupees]' % item.price if item.price is not None else ''), width=location_padding) for (location, item) in sphere.items()])) for (sphere_nr, sphere) in self.playthrough.items()]))

            if len(self.hints) > 0:
                for world in self.worlds:
                    outfile.write(header_player_string.format(header="Way of the Hero", player=world.id+1))
                    outfile.write('\n'.join(['{:{width}} {}'.format(location_string.format(location=location.name, world=location.world.id+1), item_string.format(item=location.item.name, player=location.item.world.id+1, cost=' [Costs %d Rupees]' % location.item.price if location.item.price is not None else ''), width=location_padding) for location in self.required_locations[world.id]]))

                gossip_padding = len(max([stone.name for stone in gossipLocations.values()], key=len)) + extra_padding
                for world in self.worlds:
                    hint_ids = sorted(list(self.hints[world.id].keys()), key=lambda id: gossipLocations[id].name)
                    outfile.write(header_player_string.format(header="Gossip Stone Hints", player=world.id+1))
                    outfile.write('\n'.join(['{:{width}} {}'.format(location_string.format(location=gossipLocations[id].name, world=world.id+1), re.sub('\x05[\x40\x41\x42\x43\x44\x45\x46\x47]', '', self.hints[world.id][id].replace('&', ' ').replace('^', ' ')), width=gossip_padding) for id in hint_ids]))

