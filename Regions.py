import collections
from BaseClasses import Region, Location, Entrance, RegionType


def create_regions(world):

    world.regions = [
        create_interior_region('Clock Tower',
            ['Remove the Cursed Mask', 'Song from HMS'],
            ['Clock Tower Exit', 'Clock Tower Twisted Hallway']),
        create_interior_region('Prologue Room', ['First Nuts']),

        create_ow_region('South Clock Town',
            ['SCT 20 Rupee Chest', 'SCT 50 Rupee Chest',
            'Town Deku Salesman', 'Clock Town Owl Statue', 'Love on the Balcony'],
            ['Clock Tower Entrance', 'Clock Tower Carnival Door', 'South Mailbox',
            'SCT Top Exit to WCT', 'SCT Bottom Exit to WCT', 'SCT Exit to NCT',
            'SCT Exit to NCT', 'SCT Bottom Exit to ECT', 'SCT Top Exit to ECT',
            'Clock Town South Gate', 'SCT Exit to Laundry Pool']),
        create_interior_region('Clock Tower Rooftop', ['Dropped Ocarina', 'Song from Skull Kid']),

        create_ow_region('East Clock Town',
            ['Clock Town SF', 'Free The Postman',
            'ECT 100 Rupee Chest', 'Delivery to Mama Kafei'],
            ['Honey and Darling', 'Treasure Chest Shop', 'Town Shooting Gallery', 'East Mailbox',
            'Milk Bar', 'Stock Pot Inn', 'Stock Pot Inn Secret Entrance', 'Mayors Office',
            'Bomber Bouncer', 'ECT Top Exit to SCT', 'ECT Bottom Exit to SCT',
            'ECT Exit to NCT', 'Clock Town East Gate']),
        create_interior_region('Honey and Darling',
            ['Honey and Darling Bombchu Bowling Prize', 'Honey and Darling Archery Prize',
            'Honey and Darling Basket Bomb Throw Prize', 'Honey and Darling Grand Champion'],
            ['Honey and Darling Exit']),
        create_interior_region('Treasure Chest Shop', ['Treasure Chest Game Piece of Heart Prize'], ['Treasure Chest Shop Exit']),
        create_interior_region('Town Shooting Gallery', ['Town Shooting Beat the Record', 'Town Shooting Perfect Score'], ['Town Shooting Gallery Exit']),
        create_interior_region('Milk Bar', ['Bar Performance'], ['Milk Bar Exit']),
        create_interior_region('Stock Pot Inn',
            ['Do You Have a Reservation?', 'Have you seen this man?',
            'What is the Carnival of Time?', 'Who are the Four Giants?',
            'Love in the Toilet?', 'Stock Pot Reservation Chest', 'Anjus Chest',
            'We Shall Greet The Morning Together'],
            ['Stock Pot Inn Roof Exit', 'Stock Pot Inn Front Door']),
        create_interior_region('Mayors Office', ['Expert Person Solver Takes the Case', 'Love is the True Mayor'], ['Mayors Office Exit']),
        create_interior_region('Bomber Tunnel', ['Bomber Tunnel Chest'], ['Bomber Tunnel Exit', 'Tunnel Balloon From ECT']),
        create_interior_region('Astral Observatory', ['Moon Cry'], ['Tunnel Balloon From Observatory', 'Astral Observatory Exit']),
        create_ow_region('Astral Observatory Deck', ['Moons Sad Crater'], ['Bomber Tunnel', 'Astral Observatory Fence']),

        create_ow_region('West Clock Town',
            ['200 Rupee Prize', '5000 Rupee Prize', 'Spread the Dance of Kamaro',
            'Hidden Owl Statue'],
            ['Curiosity Shop', 'Trading Post', 'Bomb Shop',
            'Post Office', 'Lottery Shop', 'Swordsmans School',
             'Clock Town West Gate', 'WCT Top Exit to SCT', 'WCT Bottom Exit to SCT']),
        create_ow_region('Mailbox', ['Deliver Letter to Kafei'])
        create_interior_region('Curiosity Shop', ['Buying The Overpriced Mask'], ['Curiosity Shop Exit']),
        create_interior_region('Trading Post', [], ['Trading Post Exit']),
        create_interior_region('Bomb Shop', ['Buy Bomb Bag', 'Buy Bigger Bomb Bag'], ['Bomb Shop Exit']),
        create_interior_region('Post Office', ['The Highest Priority of Mails', 'Counting Is Hard'], ['Post Office Exit']),
        create_interior_region('Lottery Shop', [], ['Lottery Shop Exit']),
        create_interior_region('Swordsmans School', ['Expert Jump Slash Execution'], ['Swordsmans School Exit']),

        create_ow_region('North Clock Town',
            [ 'Bombers Tag Reward', 'Love on a Tree', 'Tingle Town Map',
            'Tingle Woodfall Map', 'Foil Sakon'],
            ['GF Clock Town', 'Deku Playground', 'Clock Town North Gate',
            'NCT Exit to SCT', 'NCT Exit to ECT', 'North Mailbox']),
        create_interior_region('GF Clock Town', ['Clock Town GF Reward'], ['Clock Town']),
        create_interior_region('Deku Playground', ['Deku Challenge Day 1', 'Deku Challenge Day 2', 'Deku Challenge Day 3', 'Master of the Deku Playground'], ['Clock Town']),

        create_ow_region('Laundry Pool',
            ['Speak To Town Frog', 'Listen To A Grownup Complain'],
            ['Curiosity Backroom Entrance', 'Laundry Pool Exit to SCT']),
        create_interior_region('Curiosity Shop Backroom', ['Deliver This To Anju', 'Kafei Left A Mask', 'Kafei Left A Letter'], ['Clock Town']),

        create_ow_region('Termina Field',
            ['Learn Kamaros Dance', 'TF Chest In The Grass', 'TF Chest On A Stump'],
            ['Path To Mountain Village', 'Path To Southern Swamp',
            'Path To Great Bay', 'Path To Great Bay', 'Path To Ikana',
            'Sleeping Peahat Grotto', 'Bees In A Pond Grotto',
            'Swamp Gossips', 'Mountain Gossips', 'Ocean Gossips',
            'Canyon Gossips', 'Dodongo Grotto']),

        create_ow_region('Path to Swamp', ['Bat Guarded Tree Treasure'], ['Termina Field', 'Swamp Shooting Gallery', 'Southern Swamp']),
        create_ow_region('Southern Swamp', ['Swamp Tourist Roof Love'], ['Lost Woods', 'Potion Shop', 'Swamp Big Octo', 'Tourist Centre Big Octo', 'Swamp Tourist Cenre']),
        create_interior_region('Swamp Tourist Centre', ['Swamp Tourist Free Product', 'Pictograph Contest Winner'], ['Boat Ride', 'Southern Swamp']),
        create_ow_region('Boat Ride', None, ['Poison Swamp']),
        create_ow_region('Woodfall Owl Platform', [], ['Woodfall Temple Entrance', 'GF Woodfall', 'Woodfall']),

        create_dungeon_region('Woodfall Temple Lobby',
            [],
            ['Woodfall Temple Lobby Ledge', 'Woodfall Temple Front Exit']),
        create_dungeon_region('Woodfall Temple First Floor',
            [],
            ['Woodfall Temple Small Key Door', 'Woodfall Temple Wooden Flower']),
        create_dungeon_region('Woodfall Temple Push Block Bridge Room',
            [],
            ['Woodfall Temple Upstairs Spiderweb']),
        create_dungeon_region('Woodfall Temple Dark Puff Gauntlet',
            [],
            ['Woodfall Temple '])
        create_interior_region('GF Woodfall', ['Woodfall GF Reward'], ['Woodfall']),

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
                    'SCT 20 Rupee Chest': (None, None, None, 'Chest'),
                    'SCT 50 Rupee Chest': (None, None, None, 'Chest'),
                    'ECT 100 Rupee Chest': (None, None, None, 'Chest'),
                    'WFT Lobby Floating Fairy': (None, None, None, 'SF'),
                    'WFT Lobby Fairy Chest': (None, None, None, 'SFC'),
                    'WFT Central Flower Deku Baba': (None, None, None, 'SF'),
                    'WFT Central Flower Corner Pot': (None, None, None, 'SF'),
                    'WFT Map Chest': (None, None, None, 'Chest'),
                    'WFT Small Key Chest': (None, None, None, 'Chest'),
                    'WFT Deku Flower Elevator Beehive': (None, None, None, 'SF'),
                    'WFT Bridge Skulltula': (None, None, None, 'SF'),
                    'WFT Bridge Room Beehive': (None, None, None, 'SF'),
                    'WFT Compass Chest': (None, None, None, 'Chest'),
                    'WFT Dark Puff Battle Arena Chest': (None, None, None, 'SFC'),
                    'WFT Bow Chest': (None, None, None, 'Chest'),
                    'WFT Boss Key Chest': (None, None, None, 'Chest'),
                    'WFT Under Poison Bridge': (None, None, None, 'SF'),
                    'WFT Central Flower Bubble Fairy': (None, None, None, 'SF'),
                    'WFT Central Room Switch Chest': (None, None, None, 'SFC'),
                    'WFT Lower East Bubble Fairy': (None, None, None, 'SF'),
                    'WFT Upper East Bubble Fairy': (None, None, None, 'SF'),
                    'WFT West Bubble Fairy': (None, None, None, 'SF'),
                    'WFT Hot Bubble Fairy': (None, None, None, 'SF'),
                    'Defeat Odolwa': (None, None, None, 'NPC'),
                    'WFT Giant Cutscene': (None, None, None, 'Evemt'),
                    'Song from Giants': (None, None, None, 'Song'),
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
