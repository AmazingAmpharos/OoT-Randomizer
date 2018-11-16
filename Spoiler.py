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

            for world in self.worlds:
                if self.settings.world_count > 1:
                    outfile.write('\n\nLocations [World %d]:\n\n' % (world.id + 1))
                    outfile.write('\n'.join(['%s [W%d]: %s' % (location, world.id + 1, item) for (location, item) in self.locations[world.id].items()]))
                else:
                    outfile.write('\n\nLocations:\n\n')
                outfile.write('\n'.join(['%-40s %s' % (location + ":", item) for (location, item) in self.locations[world.id].items()]))

            outfile.write('\n\nPlaythrough:\n\n')
            if self.settings.world_count > 1:
                outfile.write('\n'.join(['%s: {\n%s\n}' % (sphere_nr, '\n'.join(['  %s [W%d]: %s [Player %d]' % (location.name, location.world.id + 1, item.name, item.world.id + 1) for (location, item) in sphere.items()])) for (sphere_nr, sphere) in self.playthrough.items()]))
            else:
                outfile.write('\n'.join(['%s: {\n%s\n}' % (sphere_nr, '\n'.join(['%-40s %s' % ('  %s:' % location.name, item.name) for (location, item) in sphere.items()])) for (sphere_nr, sphere) in self.playthrough.items()]))

            if len(self.hints) > 0:
                for world in self.worlds:
                    if self.settings.world_count > 1:
                        outfile.write('\n\nWay of the Hero [Player %d]:\n\n' % (world.id + 1))
                        outfile.write('\n'.join(['%s [W%d]: %s [Player %d]' % (location.name, world.id + 1, location.item.name, location.item.world.id + 1) for location in self.required_locations[world.id]]))
                    else:
                        outfile.write('\n\nWay of the Hero:\n\n')
                        outfile.write('\n'.join(['%-40s %s' % ('%s:' % location.name, location.item.name) for location in self.required_locations[world.id]]))

                from Hints import gossipLocations
                for world in self.worlds:
                    hint_ids = sorted(list(world.spoiler.hints.keys()), key=lambda id: gossipLocations[id].name)
                    if self.settings.world_count > 1:
                        outfile.write('\n\nGossip Stone Hints [Player %d]:\n' % (world.id + 1))
                    else:
                        outfile.write('\n\nGossip Stone Hints:\n')
                    for id in hint_ids:
                        outfile.write('\n%s: %s' % (gossipLocations[id].name if id in gossipLocations else "Unknown", re.sub('\x05[\x40\x41\x42\x43\x44\x45\x46\x47]', '', world.spoiler.hints[id].replace('&', ' ').replace('^', ' '))))

