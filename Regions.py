import collections
from BaseClasses import Region, Location, Entrance, RegionType


def create_regions(world):

    world.regions = [
        create_interior_region('Pre Game Deku Challenge Room', ['First Nuts'], ['Clock Tower']),
        create_interior_region('Clock Tower', ['Remove the Cursed Mask', 'Song from Mask Salesman'], ['Clock Tower Exit', 'Prologue Area']),
        create_ow_region('Clock Town', ['Clock Town SF' 'Heart up a Tree', 'Bombers Tag Reward', 'Sakon Definitely Wasnt Up To Something', 'Deliver Anjus Letter', 'A Postmans Work Is Never Done', 'Spread the Dance of Kamaro'] +
                            ['Saving Up For A New Wallet', 'Big Money In Da Bank', 'Tingles Town Map', 'Tingles Woodfall Map', 'Tell Town Frog Spring Has Come'],
                            ['Clock Tower', 'Clock Tower Balcony', 'Clock Town Guards', 'Bombers Tunnel', 'Curiosity Shop Backroom', 'Curiosity Shop', 'Trading Post', 'Bomb Shop', 'Post Office', 'Lottery Shop', 'Swordsmans School'] +
                            ['GF Clock Town', 'Deku Playground', 'Honey and Darling', 'Treasure Chest Shop', 'Town Shooting Gallery', 'Milk Bar', 'Stock Pot Inn', 'Mayors Office', 'ECT Shop Rooftops']),
        create_ow_region('Clock Tower Balcony', ['Clock Tower Balcony Prize'], ['Clock Town', 'Clock Tower Rooftop']),
        create_interior_region('Clock Tower Rooftop', ['Dropped Ocarina', 'Memory of the Song of Time'], []),
        create_interior_region('Bomber Tunnel', ['Bomber Bomb Chest', 'Moon Cry'], ['Clock Town', 'Astral Observatory Deck']),
        create_ow_region('Astral Observatory Deck', ['Moons Sad Crater'], ['Bomber Tunnel', 'Astral Observatory Fence']),
        create_interior_region('Astral Observatory Fence', [], ['Astral Observatory Deck', 'Termina Field']),
        create_ow_region('Clock Town Guards', [], ['Clock Town', 'Termina Field']),
        create_ow_region('ECT Shop Rooftops', ['ECT Silver Rupee'], 'Clock Town'),
        create_interior_region('Honey and Darling', ['Honey and Darling Bombchu Bowling Prize', 'Honey and Darling Archery Prize', 'Honey and Darling Basket Bomb Throw Prize', 'Honey and Darling Grand Champion'], ['Clock Town']),
        create_interior_region('Town Shooting Gallery', ['Town Shooting Beat the Record', 'Town Shooting Perfect Score'], ['Clock Town']),
        create_interior_region('Mayors Office', ['Expert Person Solver Takes the Case', 'Love is the True Mayor'], ['Clock Town']),
        create_interior_region('Stock Pot Inn', ['Do You Have a Reservation?', 'Have you seen this man?', 'What is the Carnival of Time?', 'Who are the Four Giants?', 'Help I fell in', 'Theres a Chest in my Bed', 'Stealing From Anjus Chest', 'The Couple is Reunited at Long Last'], ['Clock Town']),
        create_interior_region('Treasure Chest Shop', ['Treasure Chest Game Piece of Heart Prize'], ['Clock Town']),
        create_interior_region('GF Clock Town', ['Clock Town GF Reward'], ['Clock Town']),
        create_interior_region('Deku Playground', ['Deku Challenge Day 1', 'Deku Challenge Day 2', 'Deku Challenge Day 3', 'Master of the Deku Playground'], ['Clock Town']),
        create_interior_region('Curiosity Shop Backroom', ['Deliver This To Anju', 'Kafei Left A Mask', 'Kafei Left A Letter'], ['Clock Town']),
        create_interior_region('Curiosity Shop', ['Buying The Overpriced Mask'], ['Clock Town']),
        create_interior_region('Trading Post', [], ['Clock Town']),
        create_interior_region('Bomb Shop', ['Buy Bomb Bag', 'Buy Bigger Bomb Bag'], ['Clock Town']),
        create_interior_region('Post Office', ['The Highest Priority of Mails', 'Counting Is Hard'], ['Clock Town']),
        create_interior_region('Lottery Shop', [], ['Clock Town']),
        create_interior_region('Swordsmans School', ['Expert Jump Slash Execution'], ['Clock Town']),
        create_ow_region('Termina Field', ['Learn Kamaros Dance', 'TF Chest In The Grass', 'TF Chest On A Stump'], ['Path To Mountain Village', 'Path To Southern Swamp', 'Path To Great Bay', 'Path To Great Bay', 'Path To Ikana', 'Sleeping Peahat Grotto', 'Bees In A Pond Grotto', 'Swamp Gossips', 'Mountain Gossips', 'Ocean Gossips', 'Canyon Gossips', 'Dodongo Grotto']),
        create_ow_region('Path to Swamp', ['Bat Guarded Tree Treasure'], ['Termina Field', 'Swamp Shooting Gallery', 'Southern Swamp']),
        create_ow_region('Southern Swamp', ['Swamp Tourist Roof Love'], ['Lost Woods', 'Potion Shop', 'Swamp Big Octo', 'Tourist Centre Big Octo', 'Swamp Tourist Cenre']),
        create_interior_region('Swamp Tourist Centre', ['Swamp Tourist Free Product', 'Pictograph Contest Winner'], ['Boat Ride', 'Southern Swamp']),
        create_ow_region('Boat Ride', [], ['Poison Swamp']),
        create_ow_region('Woodfall Owl Platform', [], ['Woodfall Temple Entrance', 'GF Woodfall', 'Woodfall']),
        create_interior_region('GF Woodfall', ['Woodfall GF Reward'], ['Woodfall']),
        create_dungeon_region('Woodfall Temple Entrance', [], []),
        create_interior_region('GF Snowhead', ['Snowhead GF Reward'], ['Snowhead Spire']),
        create_interior_region('GF Great Bay', ['Great Bay GF Reward'], ['Great Bay Fairy Ledge']),
        create_interior_region('GF Stone Tower', ['Stone Tower GF Reward'], ['Ikana Canyon'])
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
                    'WF SF1': (None, None, None, 'SFF-WF'),
                    'WF SF2': (None, None, None, 'SFC-WF'),
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
