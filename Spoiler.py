from version import __version__
from collections import OrderedDict
import re


class Spoiler(object):

    def __init__(self, worlds):
        self.worlds = worlds
        self.playthrough = {}
        self.locations = {}
        self.metadata = {}
        self.required_locations = []
        self.hints = {}


    def parse_data(self):
        self.locations = {}
        self.settings = self.worlds[0].settings
        for world in self.worlds:
            spoiler_locations = [location for location in world.get_locations() if not location.locked and location.type != 'GossipStone']
            sort_order = {"Song": 0, "Boss": -1}
            spoiler_locations.sort(key=lambda item: sort_order.get(item.type, 1))
            if self.settings.world_count > 1:
                self.locations[world.id] = OrderedDict([(str(location), "%s [Player %d]" % (str(location.item), location.item.world.id + 1) if location.item is not None else 'Nothing') for location in spoiler_locations])
            else:
                self.locations[world.id] = OrderedDict([(str(location), str(location.item) if location.item is not None else 'Nothing') for location in spoiler_locations])


    def to_file(self, filename):
        self.parse_data()
        with open(filename, 'w') as outfile:
            outfile.write('OoT Randomizer Version %s  -  Seed: %s\n\n' % (__version__, self.settings.seed))
            outfile.write('Settings (%s):\n%s' % (self.settings.get_settings_string(), self.settings.get_settings_display()))

            extra_padding = 0 if self.worlds[0].settings.world_count < 2 else 5 if self.worlds[0].settings.world_count < 10 else 6
            if self.worlds[0].settings.world_count > 1:
                location_string = '{location} [W{world}]:'
                item_string = '{item} [Player {player}]'
            else:
                location_string = '{location}:'
                item_string = '{item}'

            for world in self.worlds:
                if self.settings.world_count > 1:
                    outfile.write('\n\nLocations [World %d]:\n\n' % (world.id + 1))
                else:
                    outfile.write('\n\nLocations:\n\n')
                outfile.write('\n'.join(['{:{width}} {}'.format(location_string.format(location=location, world=world.id+1), item, width=50+extra_padding) for (location, item) in self.locations[world.id].items()]))

            outfile.write('\n\nPlaythrough:\n\n')
            outfile.write('\n'.join(['%s: {\n%s\n}' % (sphere_nr, '\n'.join(['{:{width}} {}'.format(('  ' + location_string).format(location=location.name, world=location.world.id+1), item_string.format(item=item.name, player=item.world.id+1), width=50+extra_padding) for (location, item) in sphere.items()])) for (sphere_nr, sphere) in self.playthrough.items()]))

            if len(self.hints) > 0:
                for world in self.worlds:
                    if self.settings.world_count > 1:
                        outfile.write('\n\nWay of the Hero [Player %d]:\n\n' % (world.id + 1))
                    else:
                        outfile.write('\n\nWay of the Hero:\n\n')
                    outfile.write('\n'.join(['{:{width}} {}'.format(location_string.format(location=location.name, world=location.world.id+1), item_string.format(item=location.item.name, player=location.item.world.id+1), width=50+extra_padding) for location in self.required_locations[world.id]]))

                from Hints import gossipLocations
                for world in self.worlds:
                    hint_ids = sorted(list(world.spoiler.hints.keys()), key=lambda id: gossipLocations[id].name)
                    if self.settings.world_count > 1:
                        outfile.write('\n\nGossip Stone Hints [Player %d]:\n\n' % (world.id + 1))
                    else:
                        outfile.write('\n\nGossip Stone Hints:\n\n')
                    outfile.write('\n'.join(['{:{width}} {}'.format(location_string.format(location=gossipLocations[id].name if id in gossipLocations else "Unknown", world=world.id+1), re.sub('\x05[\x40\x41\x42\x43\x44\x45\x46\x47]', '', world.spoiler.hints[id].replace('&', ' ').replace('^', ' ')), width=40+extra_padding) for id in hint_ids]))

