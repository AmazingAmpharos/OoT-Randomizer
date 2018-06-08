import collections
from BaseClasses import Region, Location, Entrance, RegionType


def create_regions(world):

    world.regions = [
        create_ow_region('South Clock Town', ['Big 20 SCT', 'Big Purp SCT'], ['Clock Tower', 'Termina Field', 'Clock Tower Roof', 'North Clock Town', 'East Clock Town', 'Laundry Pool', 'West Clock Town']),
        create_interior_region('Clock Tower', ['Deku Mask', 'Song of Healing'], ['Clock Tower Exit', 'Prologue Area']),
        create_ow_region('East Clock Town', ['Silver Rupee ECT', 'Clock Town SF'], ['Milk Bar', 'Stock Pot Inn', 'Termina Field', 'North Clock Town', 'South Clock Town', 'Bombers Tunnel', 'Honey and Darling', 'Treasure Chest Game', 'Town Shooting Gallery']),
        create_ow_region('North Clock Town', ['Bombers Notebook', ''], ['Termina Field', 'Clock Town Great Fairy', 'Deku Playground']),
    ]
    world.intialize_regions()

def create_ow_region(name, locations=None, exits=None):
    return _create_region(name, RegionType.Overworld, locations, exits)

def create_interior_region(name, locations=None, exits=None):
    return _create_region(name, RegionType.Interior, locations, exits)

def create_dungeon_region(name, locations=None, exits=None):
    return _create_region(name, RegionType.Dungeon, locations, exits)

def create_grotto_region(name, locations=None, exits=None):
    return _create_region(name, RegionType.Grotto, locations, exits)

def _create_region(name, type, locations=None, exits=None):
    ret = Region(name, type)
    if locations is None:
        locations = []
    if exits is None:
        exits = []

    for exit in exits:
        ret.exits.append(Entrance(exit, ret))
    for location in locations:
        address, address2, default, type = location_table[location]
        ret.locations.append(Location(location, address, address2, default, type, ret))
    return ret

location_table = {'Deku Mask': (None, None, None, 'NPC'), 
                    '20 Rupee SCT': (None, None, None, 'Chest'),
                    'WF SF1': (None, None, None, 'SF-WF'),
                    'WF SF2': (None, None, None, 'SF-WF'),
                    'WF SF3': (None, None, None, 'SF-WF'),
                    'WF SF4': (None, None, None, 'SF-WF'),
                    'WF SF5': (None, None, None, 'SF-WF'),
                    'WF SF6': (None, None, None, 'SF-WF'),
                    'WF SF7': (None, None, None, 'SF-WF'),
                    'WF SF8': (None, None, None, 'SF-WF'),
                    'WF SF9': (None, None, None, 'SF-WF'),
                    'WF SF10': (None, None, None, 'SF-WF'),
                    'WF SF11': (None, None, None, 'SF-WF'),
                    'WF SF12': (None, None, None, 'SF-WF'),
                    'WF SF13': (None, None, None, 'SF-WF'),
                    'WF SF14': (None, None, None, 'SF-WF'),
                    'WF SF15': (None, None, None, 'SF-WF'),
                    'SH SF1': (None, None, None, 'SF-SH'),
                    'SH SF2': (None, None, None, 'SF-SH'),
                    'SH SF3': (None, None, None, 'SF-SH'),
                    'SH SF4': (None, None, None, 'SF-SH'),
                    'SH SF5': (None, None, None, 'SF-SH'),
                    'SH SF6': (None, None, None, 'SF-SH'),
                    'SH SF7': (None, None, None, 'SF-SH'),
                    'SH SF8': (None, None, None, 'SF-SH'),
                    'SH SF9': (None, None, None, 'SF-SH'),
                    'SH SF10': (None, None, None, 'SF-SH'),
                    'SH SF11': (None, None, None, 'SF-SH'),
                    'SH SF12': (None, None, None, 'SF-SH'),
                    'SH SF13': (None, None, None, 'SF-SH'),
                    'SH SF14': (None, None, None, 'SF-SH'),
                    'SH SF15': (None, None, None, 'SF-SH'),
                    'GB SF1': (None, None, None, 'SF-GB'),
                    'GB SF2': (None, None, None, 'SF-GB'),
                    'GB SF3': (None, None, None, 'SF-GB'),
                    'GB SF4': (None, None, None, 'SF-GB'),
                    'GB SF5': (None, None, None, 'SF-GB'),
                    'GB SF6': (None, None, None, 'SF-GB'),
                    'GB SF7': (None, None, None, 'SF-GB'),
                    'GB SF8': (None, None, None, 'SF-GB'),
                    'GB SF9': (None, None, None, 'SF-GB'),
                    'GB SF10': (None, None, None, 'SF-GB'),
                    'GB SF11': (None, None, None, 'SF-GB'),
                    'GB SF12': (None, None, None, 'SF-GB'),
                    'GB SF13': (None, None, None, 'SF-GB'),
                    'GB SF14': (None, None, None, 'SF-GB'),
                    'GB SF15': (None, None, None, 'SF-GB'),
                    'ST SF1': (None, None, None, 'SF-ST'),
                    'ST SF2': (None, None, None, 'SF-ST'),
                    'ST SF3': (None, None, None, 'SF-ST'),
                    'ST SF4': (None, None, None, 'SF-ST'),
                    'ST SF5': (None, None, None, 'SF-ST'),
                    'ST SF6': (None, None, None, 'SF-ST'),
                    'ST SF7': (None, None, None, 'SF-ST'),
                    'ST SF8': (None, None, None, 'SF-ST'),
                    'ST SF9': (None, None, None, 'SF-ST'),
                    'ST SF10': (None, None, None, 'SF-ST'),
                    'ST SF11': (None, None, None, 'SF-ST'),
                    'ST SF12': (None, None, None, 'SF-ST'),
                    'ST SF13': (None, None, None, 'SF-ST'),
                    'ST SF14': (None, None, None, 'SF-ST'),
                    'ST SF15': (None, None, None, 'SF-ST')}
