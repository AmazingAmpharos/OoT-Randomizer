from Region import Region, RegionType
from Entrance import Entrance
from LocationList import location_table
from Location import Location


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
        type, scene, default, hint, addresses = location_table[location]
        if addresses is None:
            addresses = (None, None)
        address, address2 = addresses

        ret.locations.append(Location(location, address, address2, default, type, scene, hint, ret))
    return ret


def create_regions(world):

    world.regions = [
        create_ow_region(
            'Kokiri Forest',
            ['Kokiri Sword Chest', 'GS Kokiri Know It All House', 'GS Kokiri Bean Patch', 'GS Kokiri House of Twins',
             'Deku Baba Sticks', 'Deku Baba Nuts', 'Kokiri Forest Gossip Stone'],
            ['Links House', 'Mido House', 'Saria House', 'House of Twins', 'Know It All House', 'Kokiri Shop', 'Deku Tree',
             'Lost Woods', 'Lost Woods Bridge', 'Kokiri Forest Storms Grotto']),
        create_interior_region(
            'Links House',
            ['Links Pocket'],
            ['Links House Exit', 'Child Forest Warp Pad', 'Adult Forest Warp Pad', 'Temple Warp Pad', 'Crater Warp Pad',
             'Lake Warp Pad', 'Graveyard Warp Pad', 'Colossus Warp Pad']),
        create_interior_region(
            'Mido House',
            ['Mido Chest Top Left', 'Mido Chest Top Right', 'Mido Chest Bottom Left', 'Mido Chest Bottom Right'],
            ['Mido House Exit']),
        create_interior_region(
            'Saria House',
            None,
            ['Saria House Exit']),
        create_interior_region(
            'House of Twins',
            None,
            ['House of Twins Exit']),
        create_interior_region(
            'Know It All House',
            None,
            ['Know It All House Exit']),
        create_interior_region(
            'Kokiri Shop',
            ['Kokiri Shop Item 1', 'Kokiri Shop Item 2', 'Kokiri Shop Item 3', 'Kokiri Shop Item 4',
             'Kokiri Shop Item 5', 'Kokiri Shop Item 6', 'Kokiri Shop Item 7', 'Kokiri Shop Item 8'],
            ['Kokiri Shop Exit']),
        create_ow_region(
            'Lost Woods',
            ['Skull Kid', 'Ocarina Memory Game', 'Target in Woods', 'LW Deku Scrub Deku Stick Upgrade',
             'GS Lost Woods Bean Patch Near Bridge', 'GS Lost Woods Bean Patch Near Stage',
             'LW Deku Scrub Deku Nuts', 'LW Deku Scrub Deku Sticks', 'Lost Woods Gossip Stone'],
            ['Lost Woods Front', 'Meadow Entrance', 'Woods to Goron City', 'Lost Woods Dive Warp', 'Adult Meadow Access',
             'Lost Woods Generic Grotto', 'Deku Theater', 'Lost Woods Sales Grotto']),
        create_ow_region('Sacred Forest Meadow Entryway', None, ['Meadow Exit', 'Meadow Gate', 'Front of Meadow Grotto']),
        create_ow_region(
            'Sacred Forest Meadow',
            ['Song from Saria'],
            ['Meadow Gate Exit', 'Meadow Fairy Grotto', 'Meadow Storms Grotto Child Access',
             'Sacred Forest Meadow Gossip Stones Child Access']),
        create_interior_region(
            'Sacred Forest Meadow Gossip Stones', 
            ['Sacred Forest Meadow Maze Gossip Stone (Lower)', 
             'Sacred Forest Meadow Maze Gossip Stone (Upper)', 
             'Sacred Forest Meadow Saria Gossip Stone']
        ),
        create_ow_region('Lost Woods Bridge', ['Gift from Saria'], ['Kokiri Forest Entrance', 'Forest Exit']),
        create_ow_region('Hyrule Field',
            ['Ocarina of Time', 'Song from Ocarina of Time', 'Generic Grotto Gossip Stone'],
            ['Field to Forest', 'Field to Lake', 'Field to Valley', 'Field to Castle Town', 'Field to Kakariko',
             'Field to Zora River', 'Lon Lon Ranch Entrance', 'Remote Southern Grotto', 'Field Near Lake Outside Fence Grotto',
             'Field Near Lake Inside Fence Grotto', 'Field Valley Grotto', 'Field West Castle Town Grotto',
             'Field Far West Castle Town Grotto', 'Field Kakariko Grotto', 'Field North Lon Lon Grotto']),
        create_ow_region(
            'Lake Hylia',
            ['Underwater Bottle', 'Lake Hylia Sun', 'Lake Hylia Freestanding PoH', 'GS Lake Hylia Bean Patch',
             'GS Lake Hylia Lab Wall', 'GS Lake Hylia Small Island', 'GS Lake Hylia Giant Tree',
             'Lake Hylia Lab Gossip Stone', 'Lake Hylia Gossip Stone (Southeast)', 'Lake Hylia Gossip Stone (Southwest)'],
            ['Lake Exit', 'Lake Hylia Dive Warp', 'Lake Hylia Lab', 'Fishing Hole', 'Water Temple Entrance', 'Lake Hylia Grotto']),
        create_interior_region('Lake Hylia Lab', ['Diving in the Lab', 'GS Lab Underwater Crate']),
        create_interior_region('Fishing Hole', ['Child Fishing', 'Adult Fishing']),
        create_ow_region(
            'Gerudo Valley',
            ['Gerudo Valley Waterfall Freestanding PoH', 'Gerudo Valley Crate Freestanding PoH',
             'GS Gerudo Valley Small Bridge', 'GS Gerudo Valley Bean Patch', 'Gerudo Valley Gossip Stone'],
            ['Valley Exit', 'Valley River', 'Bridge Crossing']),
        create_ow_region(
            'Gerudo Valley Far Side',
            ['Gerudo Valley Hammer Rocks Chest', 'GS Gerudo Valley Behind Tent', 'GS Gerudo Valley Pillar'],
            ['Fortress Entrance', 'Gerudo Valley Storms Grotto']),
        create_ow_region(
            'Gerudo Fortress',
            ['Gerudo Fortress Rooftop Chest', 'Horseback Archery 1000 Points', 'Horseback Archery 1500 Points',
             'Gerudo Fortress North F1 Carpenter', 'Gerudo Fortress North F2 Carpenter',
             'Gerudo Fortress South F1 Carpenter', 'Gerudo Fortress South F2 Carpenter', 'Gerudo Fortress Carpenter Rescue',
             'Gerudo Fortress Membership Card', 'GS Gerudo Fortress Archery Range', 'GS Gerudo Fortress Top Floor'],
            ['Haunted Wasteland Entrance', 'Gerudo Training Grounds Entrance']),
        create_ow_region(
            'Haunted Wasteland',
            ['Haunted Wasteland Structure Chest', 'GS Wasteland Ruins'],
            ['Haunted Wasteland Crossing']),
        create_ow_region(
            'Desert Colossus',
            ['Colossus Freestanding PoH', 'Sheik at Colossus', 'GS Desert Colossus Bean Patch', 'GS Desert Colossus Tree',
             'GS Desert Colossus Hill'],
            ['Colossus Fairy', 'Spirit Temple Entrance', 'Desert Colossus Grotto', 'Desert Colossus Gossip Stone']),
        create_interior_region(
            'Colossus Fairy',
            ['Desert Colossus Fairy Reward']),
        create_interior_region('Desert Colossus Gossip Stone', ['Desert Colossus Gossip Stone']),
        create_ow_region(
            'Castle Town',
            ['Temple of Time Gossip Stone (Left)',
             'Temple of Time Gossip Stone (Left-Center)',
             'Temple of Time Gossip Stone (Right)',
             'Temple of Time Gossip Stone (Right-Center)'],
            ['Castle Town Exit', 'Temple of Time', 'Hyrule Castle Grounds', 'Castle Town Rupee Room', 'Castle Town Bazaar',
             'Castle Town Mask Shop', 'Castle Town Shooting Gallery', 'Ganons Castle Grounds',
             'Castle Town Bombchu Bowling', 'Castle Town Potion Shop', 'Castle Town Treasure Chest Game',
             'Castle Town Bombchu Shop', 'Castle Town Dog Lady', 'Castle Town Man in Green House']),
        create_interior_region(
            'Temple of Time',
            ['Zelda'],
            ['Temple of Time Exit', 'Door of Time']),
        create_interior_region(
            'Beyond Door of Time',
            ['Master Sword Pedestal', 'Sheik at Temple'],
            ['Emerge as Adult']),
        create_ow_region(
            'Hyrule Castle Grounds',
            ['Malon Egg', 'GS Hyrule Castle Tree', 'Hyrule Castle Malon Gossip Stone', 'Hyrule Castle Rock Wall Gossip Stone'],
            ['Hyrule Castle Grounds Exit', 'Hyrule Castle Garden', 'Hyrule Castle Fairy', 'Castle Storms Grotto']),
        create_ow_region(
            'Hyrule Castle Garden',
            ['Zeldas Letter', 'Impa at Castle'],
            ['Hyrule Castle Garden Exit']),
        create_interior_region(
            'Hyrule Castle Fairy',
            ['Hyrule Castle Fairy Reward']),
        create_ow_region(
            'Ganons Castle Grounds',
            ['GS Outside Ganon\'s Castle'],
            ['Ganons Castle Grounds Exit', 'Ganons Castle Fairy', 'Rainbow Bridge']),
        create_interior_region('Ganons Castle Fairy', ['Ganons Castle Fairy Reward']),
        create_interior_region('Castle Town Rupee Room', ['10 Big Poes', 'GS Castle Market Guard House']),
        create_interior_region(
            'Castle Town Bazaar',
            ['Castle Town Bazaar Item 1', 'Castle Town Bazaar Item 2', 'Castle Town Bazaar Item 3',
             'Castle Town Bazaar Item 4', 'Castle Town Bazaar Item 5', 'Castle Town Bazaar Item 6',
             'Castle Town Bazaar Item 7', 'Castle Town Bazaar Item 8']),
        create_interior_region('Castle Town Mask Shop'),
        create_interior_region('Castle Town Shooting Gallery', ['Child Shooting Gallery']),
        create_interior_region(
            'Castle Town Bombchu Bowling',
            ['Bombchu Bowling Bomb Bag', 'Bombchu Bowling Piece of Heart']),
        create_interior_region(
            'Castle Town Potion Shop',
            ['Castle Town Potion Shop Item 1', 'Castle Town Potion Shop Item 2',
             'Castle Town Potion Shop Item 3', 'Castle Town Potion Shop Item 4',
             'Castle Town Potion Shop Item 5', 'Castle Town Potion Shop Item 6',
             'Castle Town Potion Shop Item 7', 'Castle Town Potion Shop Item 8']),
        create_interior_region('Castle Town Treasure Chest Game', ['Treasure Chest Game']),
        create_interior_region(
            'Castle Town Bombchu Shop',
            ['Bombchu Shop Item 1', 'Bombchu Shop Item 2', 'Bombchu Shop Item 3', 'Bombchu Shop Item 4',
             'Bombchu Shop Item 5', 'Bombchu Shop Item 6', 'Bombchu Shop Item 7', 'Bombchu Shop Item 8']),
        create_interior_region('Castle Town Dog Lady', ['Dog Lady']),
        create_interior_region('Castle Town Man in Green House'),
        create_ow_region(
            'Kakariko Village',
            ['Man on Roof', 'Anju as Adult', 'Anjus Chickens', 'Sheik in Kakariko', 'GS Kakariko House Under Construction',
             'GS Kakariko Skulltula House', 'GS Kakariko Guard\'s House', 'GS Kakariko Tree', 'GS Kakariko Watchtower',
             'GS Kakariko Above Impa\'s House'],
            ['Kakariko Exit', 'Carpenter Boss House', 'House of Skulltula', 'Impas House', 'Impas House Back', 'Windmill',
             'Kakariko Bazaar', 'Kakariko Shooting Gallery', 'Bottom of the Well', 'Kakariko Potion Shop Front',
             'Kakariko Potion Shop Back', 'Odd Medicine Building', 'Kakariko Bombable Grotto', 'Kakariko Back Grotto',
             'Graveyard Entrance', 'Death Mountain Entrance']),
        create_interior_region('Carpenter Boss House'),
        create_interior_region(
            'House of Skulltula',
            ['10 Gold Skulltula Reward', '20 Gold Skulltula Reward', '30 Gold Skulltula Reward',
             '40 Gold Skulltula Reward', '50 Gold Skulltula Reward']),
        create_interior_region('Impas House'),
        create_interior_region('Impas House Back', ['Impa House Freestanding PoH']),
        create_interior_region('Windmill', ['Windmill Freestanding PoH', 'Song at Windmill']),
        create_interior_region(
            'Kakariko Bazaar',
            ['Kakariko Bazaar Item 1', 'Kakariko Bazaar Item 2', 'Kakariko Bazaar Item 3',
             'Kakariko Bazaar Item 4', 'Kakariko Bazaar Item 5', 'Kakariko Bazaar Item 6',
             'Kakariko Bazaar Item 7', 'Kakariko Bazaar Item 8']),
        create_interior_region('Kakariko Shooting Gallery', ['Adult Shooting Gallery']),
        create_interior_region(
            'Kakariko Potion Shop Front',
            ['Kakariko Potion Shop Item 1', 'Kakariko Potion Shop Item 2',
             'Kakariko Potion Shop Item 3', 'Kakariko Potion Shop Item 4',
             'Kakariko Potion Shop Item 5', 'Kakariko Potion Shop Item 6',
             'Kakariko Potion Shop Item 7', 'Kakariko Potion Shop Item 8']),
        create_interior_region('Kakariko Potion Shop Back'),
        create_interior_region('Odd Medicine Building'),
        create_ow_region(
            'Graveyard',
            ['Graveyard Freestanding PoH', 'Gravedigging Tour', 'GS Graveyard Wall', 'GS Graveyard Bean Patch'],
            ['Shield Grave', 'Composer Grave', 'Heart Piece Grave', 'Dampes Grave', 'Dampes House', 'Graveyard Exit']),
        create_interior_region('Shield Grave', ['Shield Grave Chest']),
        create_interior_region('Heart Piece Grave', ['Heart Piece Grave Chest']),
        create_interior_region('Composer Grave', ['Composer Grave Chest', 'Song from Composer Grave']),
        create_interior_region('Dampes Grave', ['Hookshot Chest', 'Dampe Race Freestanding PoH']),
        create_interior_region('Dampes House'),
        create_ow_region('Shadow Temple Warp Region', ['Graveyard Gossip Stone'], ['Drop to Graveyard', 'Shadow Temple Entrance']),
        create_ow_region(
            'Death Mountain',
            ['Death Mountain Bombable Chest', 'DM Trail Freestanding PoH', 'GS Mountain Trail Bean Patch',
             'GS Mountain Trail Bomb Alcove', 'GS Mountain Trail Path to Crater',
             'GS Mountain Trail Above Dodongo\'s Cavern'],
            ['Death Mountain Exit', 'Goron City Entrance', 'Mountain Crater Entrance', 'Mountain Summit Fairy',
             'Dodongos Cavern Rocks', 'Mountain Bombable Grotto', 'Mountain Storms Grotto']),
        create_ow_region(
            'Dodongos Cavern Entryway',
            None,
            ['Dodongos Cavern', 'Mountain Access from Behind Rock']),
        create_ow_region(
            'Goron City',
            ['Goron City Leftmost Maze Chest', 'Goron City Left Maze Chest', 'Goron City Right Maze Chest',
             'Goron City Pot Freestanding PoH', 'Rolling Goron as Child', 'Link the Goron', 'GS Goron City Boulder Maze',
             'GS Goron City Center Platform', 'Goron City Stick Pot'],
            ['Goron City Exit', 'Goron City Bomb Wall', 'Darunias Chamber',
             'Crater Access', 'Goron Shop', 'Goron City Grotto',
             'Goron City Maze Gossip Stone', 'Goron City Medigoron Gossip Stone']),
        create_ow_region(
            'Goron City Woods Warp',
            None,
            ['Goron City from Woods', 'Goron City to Woods']),
        create_interior_region(
            'Goron Shop',
            ['Goron Shop Item 1', 'Goron Shop Item 2', 'Goron Shop Item 3', 'Goron Shop Item 4',
             'Goron Shop Item 5', 'Goron Shop Item 6', 'Goron Shop Item 7', 'Goron Shop Item 8']),
        create_ow_region('Darunias Chamber', ['Darunias Joy'], ['Darunias Chamber Exit']),
        create_interior_region('Goron City Maze Gossip Stone', ['Goron City Maze Gossip Stone']),
        create_interior_region('Goron City Medigoron Gossip Stone', ['Goron City Medigoron Gossip Stone']),
        create_ow_region(
            'Death Mountain Crater Upper',
            ['DM Crater Wall Freestanding PoH', 'Biggoron', 'GS Death Mountain Crater Crate', 'DMC Deku Scrub Bombs'],
            ['Crater Exit', 'Crater Hover Boots', 'Crater Scarecrow', 'Top of Crater Grotto',
             'Death Mountain Crater Gossip Stone', 'Death Mountain Trail Gossip Stone']),
        create_ow_region(
            'Death Mountain Crater Lower',
            None,
            ['Crater to City', 'Crater Fairy', 'Crater Bridge', 'Crater Ascent', 'DMC Hammer Grotto']),
        create_ow_region(
            'Death Mountain Crater Central',
            ['DM Crater Volcano Freestanding PoH', 'Sheik in Crater', 'GS Mountain Crater Bean Patch'],
            ['Crater Bridge Reverse', 'Fire Temple Entrance']),
        create_interior_region('Death Mountain Crater Gossip Stone', ['Death Mountain Crater Gossip Stone']),
        create_interior_region('Death Mountain Trail Gossip Stone', ['Death Mountain Trail Gossip Stone']),
        create_interior_region(
            'Crater Fairy',
            ['Crater Fairy Reward']),
        create_interior_region('Mountain Summit Fairy', ['Mountain Summit Fairy Reward']),
        create_ow_region(
            'Zora River Front',
            ['GS Zora River Tree'],
            ['Zora River Rocks', 'Zora River Adult', 'Zora River Exit']),
        create_ow_region(
            'Zora River Child',
            ['Magic Bean Salesman', 'Frog Ocarina Game', 'Frogs in the Rain', 'GS Zora River Ladder'],
            ['Zora River Child to Shared', 'Zora River Waterfall',
             'Zoras River Gossip Stone Child Access']),
        create_ow_region(
            'Zora River Adult',
            ['GS Zora River Near Raised Grottos', 'GS Zora River Above Bridge'],
            ['Zoras Domain Adult Access', 'Zora River Adult to Shared',
             'Zoras River Gossip Stone Adult Access']),
        create_interior_region(
            'Zoras River Gossip Stone',
            ['Zoras River Plateau Gossip Stone', 'Zoras River Waterfall Gossip Stone']),
        create_ow_region(
            'Zora River Shared',
            ['Zora River Lower Freestanding PoH', 'Zora River Upper Freestanding PoH'],
            ['Zora River Downstream', 'Zora River Plateau Open Grotto', 'Zora River Plateau Bombable Grotto',
             'Zora River Dive Warp', 'Zora River Storms Grotto']),
        create_ow_region(
            'Zoras Domain',
            ['Diving Minigame', 'Zoras Domain Torch Run', 'King Zora Moves', 'Zoras Domain Stick Pot',
             'Zoras Domain Nut Pot'],
            ['Zoras Domain Exit', 'Zoras Domain Dive Warp', 'Behind King Zora', 'Zora Shop Child Access', 'Zoras Domain Gossip Stone Child']),
        create_ow_region(
            'Zoras Fountain',
            ['GS Zora\'s Fountain Tree', 'GS Zora\'s Fountain Above the Log',
             'Zoras Fountain Fairy Gossip Stone', 'Zoras Fountain Jabu Gossip Stone'],
            ['Zoras Fountain Exit', 'Jabu Jabus Belly', 'Zoras Fountain Fairy']),
        create_ow_region(
            'Zoras Domain Frozen',
            ['King Zora Thawed', 'GS Zora\'s Domain Frozen Waterfall'],
            ['Zoras Fountain Adult Access', 'Zora Shop Adult Access', 'Zoras Domain Gossip Stone Adult']),
        create_ow_region(
            'Outside Ice Cavern',
            ['Zoras Fountain Iceberg Freestanding PoH', 'Zoras Fountain Bottom Freestanding PoH',
             'GS Zora\'s Fountain Hidden Cave'],
            ['Ice Cavern Entrance']),
        create_interior_region(
            'Zora Shop',
            ['Zora Shop Item 1', 'Zora Shop Item 2', 'Zora Shop Item 3', 'Zora Shop Item 4',
             'Zora Shop Item 5', 'Zora Shop Item 6', 'Zora Shop Item 7', 'Zora Shop Item 8']),
        create_interior_region('Zoras Fountain Fairy', ['Zoras Fountain Fairy Reward']),
        create_interior_region('Zoras Domain Gossip Stone', ['Zoras Domain Gossip Stone']),
        create_ow_region(
            'Lon Lon Ranch',
            ['Epona', 'Song from Malon', 'GS Lon Lon Ranch Tree', 'GS Lon Lon Ranch Rain Shed',
             'GS Lon Lon Ranch House Window', 'GS Lon Lon Ranch Back Wall'],
            ['Lon Lon Exit', 'Talon House', 'Ingo Barn', 'Lon Lon Corner Tower', 'Lon Lon Grotto']),
        create_interior_region('Talon House', ['Talons Chickens']),
        create_interior_region('Ingo Barn'),
        create_interior_region('Lon Lon Corner Tower', ['Lon Lon Tower Freestanding PoH']),
        create_interior_region(
            'Forest Temple Entry Area',
            ['Sheik Forest Song', 'GS Lost Woods Above Stage', 'GS Sacred Forest Meadow'],
            ['Adult Meadow Exit', 'Forest Temple Entrance', 'Meadow Storms Grotto Adult Access',
             'Sacred Forest Meadow Gossip Stones Adult Access']),
        create_dungeon_region(
            'Ganons Castle Tower',
            ['Ganons Tower Boss Key Chest', 'Ganon']),
        create_grotto_region(
            'Kokiri Forest Storms Grotto',
            ['Kokiri Forest Storms Grotto Chest']),
        create_grotto_region(
            'Lost Woods Generic Grotto',
            ['Lost Woods Generic Grotto Chest']),
        create_grotto_region('Deku Theater', ['Deku Theater Skull Mask', 'Deku Theater Mask of Truth']),
        create_grotto_region('Lost Woods Sales Grotto',
            ['LW Grotto Deku Scrub Arrows', 'LW Grotto Deku Scrub Deku Nut Upgrade']),
        create_grotto_region('Meadow Fairy Grotto'),
        create_grotto_region('Meadow Storms Grotto',
            ['SFM Grotto Deku Scrub Red Potion', 'SFM Grotto Deku Scrub Green Potion']),
        create_grotto_region('Front of Meadow Grotto', ['Wolfos Grotto Chest']),
        create_grotto_region('Lon Lon Grotto',
            ['LLR Grotto Deku Scrub Deku Nuts', 'LLR Grotto Deku Scrub Bombs', 'LLR Grotto Deku Scrub Arrows']),
        create_grotto_region('Remote Southern Grotto', ['Remote Southern Grotto Chest']),
        create_grotto_region('Field Near Lake Outside Fence Grotto', ['Field Near Lake Outside Fence Grotto Chest']),
        create_grotto_region('Field Near Lake Inside Fence Grotto', ['HF Grotto Deku Scrub Piece of Heart']),
        create_grotto_region('Field Valley Grotto', ['GS Hyrule Field Near Gerudo Valley'], ['Field Valley Grotto Gossip Stone']),
        create_interior_region('Field Valley Grotto Gossip Stone', ['Field Valley Grotto Gossip Stone']),
        create_grotto_region('Field West Castle Town Grotto', ['Field West Castle Town Grotto Chest']),
        create_grotto_region('Field Far West Castle Town Grotto'),
        create_grotto_region('Field Kakariko Grotto', ['GS Hyrule Field near Kakariko']),
        create_grotto_region('Field North Lon Lon Grotto', ['Tektite Grotto Freestanding PoH']),
        create_grotto_region('Castle Storms Grotto', ['GS Hyrule Castle Grotto'], ['Castle Storms Grotto Gossip Stone']),
        create_interior_region('Castle Storms Grotto Gossip Stone', ['Castle Storms Grotto Gossip Stone']),
        create_grotto_region('Kakariko Bombable Grotto', ['Redead Grotto Chest']),
        create_grotto_region('Kakariko Back Grotto', ['Kakariko Back Grotto Chest']),
        create_grotto_region('Mountain Bombable Grotto'),
        create_grotto_region('Mountain Storms Grotto', ['Mountain Storms Grotto Chest']),
        create_grotto_region('Goron City Grotto',
            ['Goron Grotto Deku Scrub Deku Nuts', 'Goron Grotto Deku Scrub Bombs', 'Goron Grotto Deku Scrub Arrows']),
        create_grotto_region('Top of Crater Grotto', ['Top of Crater Grotto Chest']),
        create_grotto_region('DMC Hammer Grotto',
            ['DMC Grotto Deku Scrub Deku Nuts', 'DMC Grotto Deku Scrub Bombs', 'DMC Grotto Deku Scrub Arrows']),
        create_grotto_region('Zora River Plateau Open Grotto', ['Zora River Plateau Open Grotto Chest']),
        create_grotto_region('Zora River Plateau Bombable Grotto'),
        create_grotto_region('Zora River Storms Grotto',
            ['ZR Grotto Deku Scrub Red Potion', 'ZR Grotto Deku Scrub Green Potion']),
        create_grotto_region('Lake Hylia Grotto',
            ['LH Grotto Deku Scrub Deku Nuts', 'LH Grotto Deku Scrub Bombs', 'LH Grotto Deku Scrub Arrows']),
        create_grotto_region('Desert Colossus Grotto',
            ['Desert Grotto Deku Scrub Red Potion', 'Desert Grotto Deku Scrub Green Potion']),
        create_grotto_region('Gerudo Valley Storms Grotto',
            ['Valley Grotto Deku Scrub Red Potion', 'Valley Grotto Deku Scrub Green Potion']),
    ]

    if world.dungeon_mq['Deku Tree']:
        world.regions.extend([
            create_dungeon_region(
                'Deku Tree Lobby',
                ['Deku Tree MQ Lobby Chest', 'Deku Tree MQ Slingshot Chest', 'Deku Tree MQ Slingshot Room Back Chest',
                 'Deku Tree MQ Basement Chest', 'GS Deku Tree MQ Lobby',
                 'Deku Tree Gossip Stone (Left)', 'Deku Tree Gossip Stone (Right)'],
                ['Deku Tree Exit', 'Deku Tree Compass Passage', 'Deku Tree Basement Path']),
            create_dungeon_region(
                'Deku Tree Compass Room',
                ['Deku Tree MQ Compass Chest', 'GS Deku Tree MQ Compass Room'],
                ['Deku Tree Compass Exit']),
            create_dungeon_region(
                'Deku Tree Boss Room',
                ['Deku Tree MQ Before Spinning Log Chest', 'Deku Tree MQ After Spinning Log Chest',
                 'GS Deku Tree MQ Basement Ceiling', 'GS Deku Tree MQ Basement Back Room',
                 'DT MQ Deku Scrub Deku Shield', 'Queen Gohma Heart', 'Queen Gohma'],
                ['Deku Tree Basement Vines'])
        ])
    else:
        world.regions.extend([
            create_dungeon_region(
                'Deku Tree Lobby',
                ['Deku Tree Lobby Chest', 'Deku Tree Compass Chest', 'Deku Tree Compass Room Side Chest',
                 'Deku Tree Basement Chest', 'GS Deku Tree Compass Room', 'GS Deku Tree Basement Vines',
                 'GS Deku Tree Basement Gate', 'Deku Tree Gossip Stone (Left)', 'Deku Tree Gossip Stone (Right)'],
                ['Deku Tree Exit', 'Deku Tree Slingshot Passage', 'Deku Tree Basement Path']),
            create_dungeon_region(
                'Deku Tree Slingshot Room',
                ['Deku Tree Slingshot Chest', 'Deku Tree Slingshot Room Side Chest'],
                ['Deku Tree Slingshot Exit']),
            create_dungeon_region(
                'Deku Tree Boss Room',
                ['GS Deku Tree Basement Back Room', 'Queen Gohma Heart', 'Queen Gohma'],
                ['Deku Tree Basement Vines'])
        ])

    if world.dungeon_mq['Dodongos Cavern']:
        world.regions.extend([
            create_dungeon_region(
                'Dodongos Cavern Beginning',
                None,
                ['Dodongos Cavern Exit', 'Dodongos Cavern Lobby']),
            create_dungeon_region(
                'Dodongos Cavern Lobby',
                ['Dodongos Cavern MQ Map Chest', 'Dodongos Cavern MQ Compass Chest', 'Dodongos Cavern MQ Larva Room Chest',
                 'Dodongos Cavern MQ Torch Puzzle Room Chest', 'Dodongos Cavern MQ Bomb Bag Chest',
                 'GS Dodongo\'s Cavern MQ Song of Time Block Room', 'GS Dodongo\'s Cavern MQ Larva Room',
                 'GS Dodongo\'s Cavern MQ Lizalfos Room', 'GS Dodongo\'s Cavern MQ Scrub Room',
                 'DC MQ Deku Scrub Deku Sticks', 'DC MQ Deku Scrub Deku Seeds',
                 'DC MQ Deku Scrub Deku Shield', 'DC MQ Deku Scrub Red Potion'],
                ['Dodongos Cavern Bomb Drop', 'Dodongos Gossip Stone']),
            create_interior_region('Dodongos Gossip Stone', ['Dodongos Cavern Gossip Stone']),
            create_dungeon_region(
                'Dodongos Cavern Boss Area',
                ['Dodongos Cavern MQ Under Grave Chest', 'Chest Above King Dodongo', 'King Dodongo Heart',
                 'King Dodongo', 'GS Dodongo\'s Cavern MQ Back Area']),
        ])
    else:
        world.regions.extend([
            create_dungeon_region(
                'Dodongos Cavern Beginning',
                None,
                ['Dodongos Cavern Exit', 'Dodongos Cavern Lobby']),
            create_dungeon_region(
                'Dodongos Cavern Lobby',
                ['Dodongos Cavern Map Chest', 'Dodongos Cavern Compass Chest', 'GS Dodongo\'s Cavern East Side Room',
                 'GS Dodongo\'s Cavern Scarecrow', 'DC Deku Scrub Deku Sticks', 'DC Deku Scrub Deku Shield'],
                ['Dodongos Cavern Retreat', 'Dodongos Cavern Left Door', 'Dodongos Gossip Stone']),
            create_interior_region('Dodongos Gossip Stone', ['Dodongos Cavern Gossip Stone']),
            create_dungeon_region(
                'Dodongos Cavern Climb',
                ['Dodongos Cavern Bomb Flower Platform', 'GS Dodongo\'s Cavern Vines Above Stairs',
                 'DC Deku Scrub Deku Seeds', 'DC Deku Scrub Deku Nuts'],
                ['Dodongos Cavern Bridge Fall', 'Dodongos Cavern Slingshot Target']),
            create_dungeon_region(
                'Dodongos Cavern Far Bridge',
                ['Dodongos Cavern Bomb Bag Chest', 'Dodongos Cavern End of Bridge Chest',
                 'GS Dodongo\'s Cavern Alcove Above Stairs'],
                ['Dodongos Cavern Bomb Drop', 'Dodongos Cavern Bridge Fall 2']),
            create_dungeon_region(
                'Dodongos Cavern Boss Area',
                ['Chest Above King Dodongo', 'King Dodongo Heart', 'King Dodongo', 'GS Dodongo\'s Cavern Back Room'],
                ['Dodongos Cavern Exit Skull'])
        ])

    if world.dungeon_mq['Jabu Jabus Belly']:
        world.regions.extend([
            create_dungeon_region(
                'Jabu Jabus Belly Beginning',
                ['Jabu Jabus Belly MQ Map Chest', 'Jabu Jabus Belly MQ Entry Side Chest'],
                ['Jabu Jabus Belly Exit', 'Jabu Jabus Belly Cow Switch']),
            create_dungeon_region(
                'Jabu Jabus Belly Main',
                ['Jabu Jabus Belly MQ Second Room Lower Chest', 'Jabu Jabus Belly MQ Compass Chest',
                 'Jabu Jabus Belly MQ Basement South Chest', 'Jabu Jabus Belly MQ Basement North Chest',
                 'Jabu Jabus Belly MQ Boomerang Room Small Chest', 'MQ Boomerang Chest', 'GS Jabu Jabu MQ Boomerang Room'],
                ['Jabu Jabus Belly Retreat', 'Jabu Jabus Belly Tentacle Access']),
            create_dungeon_region(
                'Jabu Jabus Belly Depths',
                ['Jabu Jabus Belly MQ Falling Like Like Room Chest', 'GS Jabu Jabu MQ Tailpasaran Room',
                 'GS Jabu Jabu MQ Invisible Enemies Room'],
                ['Jabu Jabus Belly Elevator', 'Jabu Jabus Belly Octopus']),
            create_dungeon_region(
                'Jabu Jabus Belly Boss Area',
                ['Jabu Jabus Belly MQ Second Room Upper Chest', 'Jabu Jabus Belly MQ Near Boss Chest',
                 'Barinade Heart', 'Barinade', 'GS Jabu Jabu MQ Near Boss'],
                ['Jabu Jabus Belly Final Backtrack'])
        ])
    else:
        world.regions.extend([
            create_dungeon_region(
                'Jabu Jabus Belly Beginning',
                None,
                ['Jabu Jabus Belly Exit', 'Jabu Jabus Belly Ceiling Switch']),
            create_dungeon_region(
                'Jabu Jabus Belly Main',
                ['Boomerang Chest', 'GS Jabu Jabu Water Switch Room', 'Jabu Deku Scrub Deku Nuts'],
                ['Jabu Jabus Belly Retreat', 'Jabu Jabus Belly Tentacles']),
            create_dungeon_region(
                'Jabu Jabus Belly Depths',
                ['Jabu Jabus Belly Map Chest', 'Jabu Jabus Belly Compass Chest', 'GS Jabu Jabu Lobby Basement Lower',
                 'GS Jabu Jabu Lobby Basement Upper'],
                ['Jabu Jabus Belly Elevator', 'Jabu Jabus Belly Octopus']),
            create_dungeon_region(
                'Jabu Jabus Belly Boss Area',
                ['Barinade Heart', 'Barinade', 'GS Jabu Jabu Near Boss'],
                ['Jabu Jabus Belly Final Backtrack'])
        ])

    if world.dungeon_mq['Forest Temple']:
        world.regions.extend([
            create_dungeon_region(
                'Forest Temple Lobby',
                ['Forest Temple MQ First Chest', 'GS Forest Temple MQ First Hallway'],
                ['Forest Temple Exit', 'Forest Temple Lobby Locked Door']),
            create_dungeon_region(
                'Forest Temple Central Area',
                ['Forest Temple MQ Chest Behind Lobby', 'GS Forest Temple MQ Block Push Room'],
                ['Forest Temple West Eye Switch', 'Forest Temple East Eye Switch',
                 'Forest Temple Block Puzzle Solve', 'Forest Temple Crystal Switch Jump']),
            create_dungeon_region(
                'Forest Temple After Block Puzzle',
                ['Forest Temple MQ Boss Key Chest'],
                ['Forest Temple Twisted Hall']),
            create_dungeon_region(
                'Forest Temple Outdoor Ledge',
                ['Forest Temple MQ Redead Chest'],
                ['Forest Temple Drop to NW Outdoors']),
            create_dungeon_region(
                'Forest Temple NW Outdoors',
                ['GS Forest Temple MQ Outdoor West'],
                ['Forest Temple Well Connection', 'Forest Temple Webs']),
            create_dungeon_region(
                'Forest Temple NE Outdoors',
                ['Forest Temple MQ Well Chest', 'GS Forest Temple MQ Outdoor East', 'GS Forest Temple MQ Well'],
                ['Forest Temple Climb to Top Ledges', 'Forest Temple Longshot to NE Outdoors Ledge']),
            create_dungeon_region(
                'Forest Temple Outdoors Top Ledges',
                ['Forest Temple MQ NE Outdoors Upper Chest'],
                ['Forest Temple Top Drop to NE Outdoors']),
            create_dungeon_region(
                'Forest Temple NE Outdoors Ledge',
                ['Forest Temple MQ NE Outdoors Lower Chest'],
                ['Forest Temple Drop to NE Outdoors', 'Forest Temple Song of Time Block Climb']),
            create_dungeon_region(
                'Forest Temple Bow Region',
                ['Forest Temple MQ Bow Chest', 'Forest Temple MQ Map Chest', 'Forest Temple MQ Compass Chest'],
                ['Forest Temple Drop to Falling Room']),
            create_dungeon_region(
                'Forest Temple Falling Room',
                ['Forest Temple MQ Falling Room Chest'],
                ['Forest Temple Falling Room Exit', 'Forest Temple Elevator']),
            create_dungeon_region(
                'Forest Temple Boss Region',
                ['Forest Temple MQ Near Boss Chest', 'Phantom Ganon Heart', 'Phantom Ganon'])
        ])
    else:
        world.regions.extend([
            create_dungeon_region(
                'Forest Temple Lobby',
                ['Forest Temple First Chest', 'Forest Temple Chest Behind Lobby', 'GS Forest Temple First Room',
                 'GS Forest Temple Lobby'],
                ['Forest Temple Exit', 'Forest Temple Song of Time Block', 'Forest Temple Lobby Eyeball Switch',
                 'Forest Temple Lobby Locked Door']),
            create_dungeon_region(
                'Forest Temple NW Outdoors',
                ['Forest Temple Well Chest', 'Forest Temple Map Chest', 'GS Forest Temple Outdoor West'],
                ['Forest Temple Through Map Room']),
            create_dungeon_region(
                'Forest Temple NE Outdoors',
                ['Forest Temple Outside Hookshot Chest', 'GS Forest Temple Outdoor East'],
                ['Forest Temple Well Connection', 'Forest Temple Outside to Lobby', 'Forest Temple Scarecrows Song']),
            create_dungeon_region(
                'Forest Temple Falling Room',
                ['Forest Temple Falling Room Chest'],
                ['Forest Temple Falling Room Exit', 'Forest Temple Elevator']),
            create_dungeon_region(
                'Forest Temple Block Push Room',
                ['Forest Temple Block Push Chest'],
                ['Forest Temple Outside Backdoor', 'Forest Temple Twisted Hall', 'Forest Temple Straightened Hall']),
            create_dungeon_region(
                'Forest Temple Straightened Hall',
                ['Forest Temple Boss Key Chest'],
                ['Forest Temple Boss Key Chest Drop']),
            create_dungeon_region(
                'Forest Temple Outside Upper Ledge',
                ['Forest Temple Floormaster Chest'],
                ['Forest Temple Outside Ledge Drop']),
            create_dungeon_region(
                'Forest Temple Bow Region',
                ['Forest Temple Bow Chest', 'Forest Temple Red Poe Chest', 'Forest Temple Blue Poe Chest'],
                ['Forest Temple Drop to Falling Room']),
            create_dungeon_region(
                'Forest Temple Boss Region',
                ['Forest Temple Near Boss Chest', 'Phantom Ganon Heart', 'Phantom Ganon', 'GS Forest Temple Basement'])
        ])

    if world.dungeon_mq['Fire Temple']:
        world.regions.extend([
            create_dungeon_region(
                'Fire Temple Lower',
                ['Fire Temple MQ Entrance Hallway Small Chest', 'Fire Temple MQ Chest Near Boss'],
                ['Fire Temple Exit', 'Fire Temple Boss Door', 'Fire Temple Lower Locked Door', 'Fire Temple Hammer Statue']),
            create_dungeon_region(
                'Fire Lower Locked Door',
                ['Fire Temple MQ Megaton Hammer Chest', 'Fire Temple MQ Map Chest']),
            create_dungeon_region(
                'Fire Big Lava Room',
                ['Fire Temple MQ Boss Key Chest', 'Fire Temple MQ Big Lava Room Bombable Chest', 'GS Fire Temple MQ Big Lava Room'],
                ['Fire Temple Early Climb']),
            create_dungeon_region(
                'Fire Lower Maze',
                ['Fire Temple MQ Maze Lower Chest'],
                ['Fire Temple Maze Climb']),
            create_dungeon_region(
                'Fire Upper Maze',
                ['Fire Temple MQ Maze Upper Chest', 'Fire Temple MQ Maze Side Room', 'Fire Temple MQ Compass Chest',
                 'GS Fire Temple MQ East Tower Top'],
                ['Fire Temple Maze Escape']),
            create_dungeon_region(
                'Fire Temple Upper',
                ['Fire Temple MQ Freestanding Key', 'Fire Temple MQ West Tower Top Chest', 'GS Fire Temple MQ Fire Wall Maze Side Room',
                 'GS Fire Temple MQ Fire Wall Maze Center', 'GS Fire Temple MQ Above Fire Wall Maze']),
            create_dungeon_region(
                'Fire Boss Room',
                ['Volvagia Heart', 'Volvagia'])
        ])
    else:
        world.regions.extend([
            create_dungeon_region(
                'Fire Temple Lower',
                ['Fire Temple Chest Near Boss', 'Fire Temple Fire Dancer Chest', 'Fire Temple Boss Key Chest',
                 'Fire Temple Big Lava Room Bombable Chest', 'Fire Temple Big Lava Room Open Chest', 'Volvagia Heart',
                 'Volvagia', 'GS Fire Temple Song of Time Room', 'GS Fire Temple Basement'],
                ['Fire Temple Exit', 'Fire Temple Early Climb']),
            create_dungeon_region(
                'Fire Temple Middle',
                ['Fire Temple Boulder Maze Lower Chest', 'Fire Temple Boulder Maze Upper Chest',
                 'Fire Temple Boulder Maze Side Room', 'Fire Temple Boulder Maze Bombable Pit', 'Fire Temple Scarecrow Chest',
                 'Fire Temple Map Chest', 'Fire Temple Compass Chest', 'GS Fire Temple Unmarked Bomb Wall',
                 'GS Fire Temple East Tower Climb', 'GS Fire Temple East Tower Top'],
                ['Fire Temple Fire Maze Escape']),
            create_dungeon_region(
                'Fire Temple Upper',
                ['Fire Temple Highest Goron Chest', 'Fire Temple Megaton Hammer Chest'])
        ])

    if world.dungeon_mq['Water Temple']:
        world.regions.extend([
            create_dungeon_region(
                'Water Temple Lobby',
                ['Water Temple MQ Map Chest', 'Water Temple MQ Central Pillar Chest', 'Morpha Heart', 'Morpha'],
                ['Water Temple Exit', 'Water Temple Water Level Switch', 'Water Temple Locked Door']),
            create_dungeon_region(
                'Water Temple Lowered Water Levels',
                ['Water Temple MQ Compass Chest', 'Water Temple MQ Longshot Chest',
                 'GS Water Temple MQ Lizalfos Hallway', 'GS Water Temple MQ Before Upper Water Switch']),
            create_dungeon_region(
                'Water Temple Dark Link Region',
                ['Water Temple MQ Boss Key Chest', 'GS Water Temple MQ Serpent River'],
                ['Water Temple Basement Gates Switch']),
            create_dungeon_region(
                'Water Temple Basement Gated Areas',
                ['Water Temple MQ Freestanding Key', 'GS Water Temple MQ South Basement', 'GS Water Temple MQ North Basement'])
        ])
    else:
        world.regions.extend([
            create_dungeon_region(
                'Water Temple Lobby',
                ['Water Temple Map Chest', 'Water Temple Compass Chest', 'Water Temple Torches Chest', 'Water Temple Dragon Chest',
                 'Water Temple Central Bow Target Chest', 'Water Temple Boss Key Chest', 'Morpha Heart', 'Morpha',
                 'GS Water Temple South Basement', 'GS Water Temple Near Boss Key Chest'],
                ['Water Temple Exit', 'Water Temple Central Pillar', 'Water Temple Upper Locked Door']),
            create_dungeon_region(
                'Water Temple Middle Water Level',
                ['Water Temple Central Pillar Chest', 'Water Temple Cracked Wall Chest', 'GS Water Temple Central Room']),
            create_dungeon_region(
                'Water Temple Dark Link Region',
                ['Water Temple Dark Link Chest', 'Water Temple River Chest', 'GS Water Temple Serpent River',
                 'GS Water Temple Falling Platform Room'])
        ])

    if world.dungeon_mq['Spirit Temple']:
        world.regions.extend([
            create_dungeon_region(
                'Spirit Temple Lobby',
                ['Spirit Temple MQ Entrance Front Left Chest', 'Spirit Temple MQ Entrance Back Left Chest',
                 'Spirit Temple MQ Entrance Back Right Chest'],
                ['Spirit Temple Exit', 'Spirit Temple Crawl Passage', 'Spirit Temple Ceiling Passage']),
            create_dungeon_region(
                'Child Spirit Temple',
                ['Spirit Temple MQ Child Left Chest', 'Spirit Temple MQ Map Chest', 'Spirit Temple MQ Silver Block Hallway Chest'],
                ['Child Spirit Temple to Shared']),
            create_dungeon_region(
                'Adult Spirit Temple',
                ['Spirit Temple MQ Child Center Chest', 'Spirit Temple MQ Child Climb South Chest', 'Spirit Temple MQ Lower NE Main Room Chest',
                 'Spirit Temple MQ Upper NE Main Room Chest', 'Spirit Temple MQ Beamos Room Chest', 'Spirit Temple MQ Ice Trap Chest',
                 'Spirit Temple MQ Boss Key Chest', 'GS Spirit Temple MQ Sun Block Room', 'GS Spirit Temple MQ Iron Knuckle West',
                 'GS Spirit Temple MQ Iron Knuckle North'],
                ['Adult Spirit Temple Descent', 'Adult Spirit Temple to Shared', 'Spirit Temple Climbable Wall', 'Mirror Shield Exit']),
            create_dungeon_region(
                'Spirit Temple Shared',
                ['Spirit Temple MQ Child Climb North Chest', 'Spirit Temple MQ Compass Chest', 'Spirit Temple MQ Sun Block Room Chest'],
                ['Silver Gauntlets Exit']),
            create_dungeon_region(
                'Lower Adult Spirit Temple',
                ['Spirit Temple MQ Lower Adult Left Chest', 'Spirit Temple MQ Lower Adult Right Chest',
                 'Spirit Temple MQ Entrance Front Right Chest', 'GS Spirit Temple MQ Lower Adult Left',
                 'GS Spirit Temple MQ Lower Adult Right']),
            create_dungeon_region(
                'Spirit Temple Boss Area',
                ['Spirit Temple MQ Mirror Puzzle Invisible Chest', 'Twinrova Heart', 'Twinrova']),
            create_dungeon_region(
                'Mirror Shield Hand',
                ['Mirror Shield Chest']),
            create_dungeon_region(
                'Silver Gauntlets Hand',
                ['Silver Gauntlets Chest'])
        ])
    else:
        world.regions.extend([
            create_dungeon_region(
                'Spirit Temple Lobby',
                None,
                ['Spirit Temple Exit', 'Spirit Temple Crawl Passage', 'Spirit Temple Silver Block']),
            create_dungeon_region(
                'Child Spirit Temple',
                ['Spirit Temple Child Left Chest', 'Spirit Temple Child Right Chest', 'GS Spirit Temple Metal Fence',
                 'Spirit Temple Nut Crate'],
                ['Child Spirit Temple Climb']),
            create_dungeon_region(
                'Child Spirit Temple Climb',
                ['Spirit Temple Child Climb East Chest', 'Spirit Temple Child Climb North Chest',
                 'GS Spirit Temple Bomb for Light Room'],
                ['Child Spirit Temple Passthrough']),
            create_dungeon_region(
                'Early Adult Spirit Temple',
                ['Spirit Temple Compass Chest', 'Spirit Temple Early Adult Right Chest',
                 'Spirit Temple First Mirror Right Chest', 'Spirit Temple First Mirror Left Chest',
                 'GS Spirit Temple Boulder Room'],
                ['Adult Spirit Temple Passthrough']),
            create_dungeon_region(
                'Spirit Temple Central Chamber',
                ['Spirit Temple Map Chest', 'Spirit Temple Sun Block Room Chest', 'Spirit Temple Statue Hand Chest',
                 'Spirit Temple NE Main Room Chest', 'GS Spirit Temple Hall to West Iron Knuckle', 'GS Spirit Temple Lobby'],
                ['Spirit Temple to Hands', 'Spirit Temple Central Locked Door', 'Spirit Temple Middle Child Door']),
            create_dungeon_region(
                'Spirit Temple Outdoor Hands',
                ['Silver Gauntlets Chest', 'Mirror Shield Chest']),
            create_dungeon_region(
                'Spirit Temple Beyond Central Locked Door',
                ['Spirit Temple Near Four Armos Chest', 'Spirit Temple Hallway Left Invisible Chest',
                 'Spirit Temple Hallway Right Invisible Chest'],
                ['Spirit Temple Final Locked Door']),
            create_dungeon_region(
                'Spirit Temple Beyond Final Locked Door',
                ['Spirit Temple Boss Key Chest', 'Spirit Temple Topmost Chest', 'Twinrova Heart', 'Twinrova'])
        ])

    if world.dungeon_mq['Shadow Temple']:
        world.regions.extend([
            create_dungeon_region(
                'Shadow Temple Beginning',
                None,
                ['Shadow Temple Exit', 'Shadow Temple First Pit', 'Shadow Temple Beginning Locked Door']),
            create_dungeon_region(
                'Shadow Temple Dead Hand Area',
                ['Shadow Temple MQ Compass Chest', 'Shadow Temple MQ Hover Boots Chest']),
            create_dungeon_region(
                'Shadow Temple First Beamos',
                ['Shadow Temple MQ Map Chest', 'Shadow Temple MQ Early Gibdos Chest', 'Shadow Temple MQ Near Ship Invisible Chest'],
                ['Shadow Temple Bomb Wall']),
            create_dungeon_region(
                'Shadow Temple Huge Pit',
                ['Shadow Temple MQ Invisible Blades Visible Chest', 'Shadow Temple MQ Invisible Blades Invisible Chest',
                 'Shadow Temple MQ Beamos Silver Rupees Chest', 'Shadow Temple MQ Falling Spikes Lower Chest',
                 'Shadow Temple MQ Falling Spikes Upper Chest', 'Shadow Temple MQ Falling Spikes Switch Chest',
                 'Shadow Temple MQ Invisible Spikes Chest', 'Shadow Temple MQ Stalfos Room Chest', 'GS Shadow Temple MQ Crusher Room'],
                ['Shadow Temple Hookshot Target']),
            create_dungeon_region(
                'Shadow Temple Wind Tunnel',
                ['Shadow Temple MQ Wind Hint Chest', 'Shadow Temple MQ After Wind Enemy Chest', 'Shadow Temple MQ After Wind Hidden Chest',
                 'GS Shadow Temple MQ Wind Hint Room', 'GS Shadow Temple MQ After Wind'],
                ['Shadow Temple Boat']),
            create_dungeon_region(
                'Shadow Temple Beyond Boat',
                ['Bongo Bongo Heart', 'Bongo Bongo', 'GS Shadow Temple MQ After Ship', 'GS Shadow Temple MQ Near Boss'],
                ['Shadow Temple Longshot Target']),
            create_dungeon_region(
                'Shadow Temple Invisible Maze',
                ['Shadow Temple MQ Spike Walls Left Chest', 'Shadow Temple MQ Boss Key Chest',
                 'Shadow Temple MQ Bomb Flower Chest', 'Shadow Temple MQ Freestanding Key'])
        ])
    else:
        world.regions.extend([
            create_dungeon_region(
                'Shadow Temple Beginning',
                ['Shadow Temple Map Chest', 'Shadow Temple Hover Boots Chest'],
                ['Shadow Temple Exit', 'Shadow Temple First Pit']),
            create_dungeon_region(
                'Shadow Temple First Beamos',
                ['Shadow Temple Compass Chest', 'Shadow Temple Early Silver Rupee Chest'],
                ['Shadow Temple Bomb Wall']),
            create_dungeon_region(
                'Shadow Temple Huge Pit',
                ['Shadow Temple Invisible Blades Visible Chest', 'Shadow Temple Invisible Blades Invisible Chest',
                 'Shadow Temple Falling Spikes Lower Chest', 'Shadow Temple Falling Spikes Upper Chest',
                 'Shadow Temple Falling Spikes Switch Chest', 'Shadow Temple Invisible Spikes Chest',
                 'Shadow Temple Freestanding Key', 'GS Shadow Temple Like Like Room', 'GS Shadow Temple Crusher Room',
                 'GS Shadow Temple Single Giant Pot'],
                ['Shadow Temple Hookshot Target']),
            create_dungeon_region(
                'Shadow Temple Wind Tunnel',
                ['Shadow Temple Wind Hint Chest', 'Shadow Temple After Wind Enemy Chest',
                 'Shadow Temple After Wind Hidden Chest', 'GS Shadow Temple Near Ship'],
                ['Shadow Temple Boat']),
            create_dungeon_region(
                'Shadow Temple Beyond Boat',
                ['Shadow Temple Spike Walls Left Chest', 'Shadow Temple Boss Key Chest',
                 'Shadow Temple Hidden Floormaster Chest', 'Bongo Bongo Heart', 'Bongo Bongo',
                 'GS Shadow Temple Triple Giant Pot'])
        ])

    if world.dungeon_mq['Bottom of the Well']:
        world.regions.extend([
            create_dungeon_region(
                'Bottom of the Well',
                ['Bottom of the Well MQ Compass Chest', 'Bottom of the Well MQ Map Chest', 'Bottom of the Well MQ Lens Chest',
                 'Bottom of the Well MQ Dead Hand Freestanding Key', 'Bottom of the Well MQ East Inner Room Freestanding Key',
                 'GS Well MQ Basement', 'GS Well MQ West Inner Room', 'GS Well MQ Coffin Room'],
                ['Bottom of the Well Exit'])
        ])
    else:
        world.regions.extend([
            create_dungeon_region(
                'Bottom of the Well',
                ['Bottom of the Well Front Left Hidden Wall', 'Bottom of the Well Front Center Bombable',
                 'Bottom of the Well Right Bottom Hidden Wall', 'Bottom of the Well Center Large Chest',
                 'Bottom of the Well Center Small Chest', 'Bottom of the Well Back Left Bombable',
                 'Bottom of the Well Freestanding Key', 'Bottom of the Well Defeat Boss', 'Bottom of the Well Invisible Chest',
                 'Bottom of the Well Underwater Front Chest', 'Bottom of the Well Underwater Left Chest',
                 'Bottom of the Well Basement Chest', 'Bottom of the Well Locked Pits', 'Bottom of the Well Behind Right Grate',
                 'GS Well West Inner Room', 'GS Well East Inner Room', 'GS Well Like Like Cage', 'Bottom of the Well Stick Pot'],
                ['Bottom of the Well Exit'])
        ])

    if world.dungeon_mq['Ice Cavern']:
        world.regions.extend([
            create_dungeon_region(
                'Ice Cavern',
                ['Ice Cavern MQ Map Chest', 'Ice Cavern MQ Compass Chest', 'Ice Cavern MQ Iron Boots Chest',
                 'Ice Cavern MQ Freestanding PoH', 'Sheik in Ice Cavern', 'GS Ice Cavern MQ Red Ice',
                 'GS Ice Cavern MQ Ice Block', 'GS Ice Cavern MQ Scarecrow'],
                ['Ice Cavern Exit'])
        ])
    else:
        world.regions.extend([
            create_dungeon_region(
                'Ice Cavern',
                ['Ice Cavern Map Chest', 'Ice Cavern Compass Chest', 'Ice Cavern Iron Boots Chest',
                 'Ice Cavern Freestanding PoH', 'Sheik in Ice Cavern', 'GS Ice Cavern Spinning Scythe Room',
                 'GS Ice Cavern Heart Piece Room', 'GS Ice Cavern Push Block Room'],
                ['Ice Cavern Exit'])
        ])

    if world.dungeon_mq['Gerudo Training Grounds']:
        world.regions.extend([
            create_dungeon_region(
                'Gerudo Training Grounds Lobby',
                ['Gerudo Training Grounds MQ Lobby Left Chest', 'Gerudo Training Grounds MQ Lobby Right Chest',
                 'Gerudo Training Grounds MQ Hidden Ceiling Chest', 'Gerudo Training Grounds MQ Maze Path First Chest',
                 'Gerudo Training Grounds MQ Maze Path Second Chest', 'Gerudo Training Grounds MQ Maze Path Third Chest'],
                ['Gerudo Training Grounds Exit', 'Gerudo Training Grounds Left Door', 'Gerudo Training Grounds Right Door']),
            create_dungeon_region(
                'Gerudo Training Grounds Right Side',
                ['Gerudo Training Grounds MQ Dinolfos Chest', 'Gerudo Training Grounds MQ Underwater Silver Rupee Chest']),
            create_dungeon_region(
                'Gerudo Training Grounds Left Side',
                ['Gerudo Training Grounds MQ First Iron Knuckle Chest'],
                ['Gerudo Training Grounds Longshot Target']),
            create_dungeon_region(
                'Gerudo Training Grounds Stalfos Room',
                ['Gerudo Training Grounds MQ Before Heavy Block Chest', 'Gerudo Training Grounds MQ Heavy Block Chest'],
                ['Gerudo Training Grounds Song of Time Block']),
            create_dungeon_region(
                'Gerudo Training Grounds Back Areas',
                ['Gerudo Training Grounds MQ Eye Statue Chest', 'Gerudo Training Grounds MQ Second Iron Knuckle Chest',
                 'Gerudo Training Grounds MQ Flame Circle Chest'],
                ['Gerudo Training Grounds Rusted Switch', 'Gerudo Training Grounds Loop Around']),
            create_dungeon_region(
                'Gerudo Training Grounds Central Maze Right',
                ['Gerudo Training Grounds MQ Maze Right Central Chest', 'Gerudo Training Grounds MQ Maze Right Side Chest',
                 'Gerudo Training Grounds MQ Ice Arrows Chest'])
        ])
    else:
        world.regions.extend([
            create_dungeon_region(
                'Gerudo Training Grounds Lobby',
                ['Gerudo Training Grounds Lobby Left Chest', 'Gerudo Training Grounds Lobby Right Chest',
                 'Gerudo Training Grounds Stalfos Chest', 'Gerudo Training Grounds Beamos Chest'],
                ['Gerudo Training Grounds Exit', 'Gerudo Training Ground Left Silver Rupees', 'Gerudo Training Ground Beamos',
                 'Gerudo Training Ground Central Door']),
            create_dungeon_region(
                'Gerudo Training Grounds Central Maze',
                ['Gerudo Training Grounds Hidden Ceiling Chest', 'Gerudo Training Grounds Maze Path First Chest',
                 'Gerudo Training Grounds Maze Path Second Chest', 'Gerudo Training Grounds Maze Path Third Chest',
                 'Gerudo Training Grounds Maze Path Final Chest'],
                ['Gerudo Training Grounds Right Locked Doors']),
            create_dungeon_region(
                'Gerudo Training Grounds Central Maze Right',
                ['Gerudo Training Grounds Maze Right Central Chest', 'Gerudo Training Grounds Maze Right Side Chest',
                 'Gerudo Training Grounds Freestanding Key'],
                ['Gerudo Training Grounds Maze Exit']),
            create_dungeon_region(
                'Gerudo Training Grounds Lava Room',
                ['Gerudo Training Grounds Underwater Silver Rupee Chest'],
                ['Gerudo Training Grounds Maze Ledge', 'Gerudo Training Grounds Right Hookshot Target']),
            create_dungeon_region(
                'Gerudo Training Grounds Hammer Room',
                ['Gerudo Training Grounds Hammer Room Clear Chest', 'Gerudo Training Grounds Hammer Room Switch Chest'],
                ['Gerudo Training Grounds Hammer Target', 'Gerudo Training Grounds Hammer Room Clear']),
            create_dungeon_region(
                'Gerudo Training Grounds Eye Statue Lower',
                ['Gerudo Training Grounds Eye Statue Chest'],
                ['Gerudo Training Grounds Eye Statue Exit']),
            create_dungeon_region(
                'Gerudo Training Grounds Eye Statue Upper',
                ['Gerudo Training Grounds Near Scarecrow Chest'],
                ['Gerudo Training Grounds Eye Statue Drop']),
            create_dungeon_region(
                'Gerudo Training Grounds Heavy Block Room',
                ['Gerudo Training Grounds Before Heavy Block Chest', 'Gerudo Training Grounds Heavy Block First Chest',
                 'Gerudo Training Grounds Heavy Block Second Chest', 'Gerudo Training Grounds Heavy Block Third Chest',
                 'Gerudo Training Grounds Heavy Block Fourth Chest'],
                ['Gerudo Training Grounds Hidden Hookshot Target'])
        ])

    if world.dungeon_mq['Ganons Castle']:
        world.regions.extend([
            create_dungeon_region(
                'Ganons Castle Lobby',
                None,
                ['Ganons Castle Exit', 'Ganons Castle Forest Trial', 'Ganons Castle Fire Trial', 'Ganons Castle Water Trial',
                 'Ganons Castle Shadow Trial', 'Ganons Castle Spirit Trial', 'Ganons Castle Light Trial',
                 'Ganons Castle Tower', 'Ganons Castle Deku Scrubs']),
            create_dungeon_region(
                'Ganons Castle Deku Scrubs',
                ['GC MQ Deku Scrub Bombs', 'GC MQ Deku Scrub Arrows', 'GC MQ Deku Scrub Red Potion', 'GC MQ Deku Scrub Green Potion',
                 'GC MQ Deku Scrub Deku Nuts']),
            create_dungeon_region(
                'Ganons Castle Forest Trial',
                ['Ganons Castle MQ Forest Trial First Chest', 'Ganons Castle MQ Forest Trial Second Chest',
                 'Ganons Castle MQ Forest Trial Freestanding Key', 'Ganons Castle Forest Trial Clear']),
            create_dungeon_region(
                'Ganons Castle Fire Trial',
                ['Ganons Castle Fire Trial Clear']),
            create_dungeon_region(
                'Ganons Castle Water Trial',
                ['Ganons Castle MQ Water Trial Chest', 'Ganons Castle Water Trial Clear']),
            create_dungeon_region(
                'Ganons Castle Shadow Trial',
                ['Ganons Castle MQ Shadow Trial First Chest', 'Ganons Castle MQ Shadow Trial Second Chest',
                 'Ganons Castle Shadow Trial Clear']),
            create_dungeon_region(
                'Ganons Castle Spirit Trial',
                ['Ganons Castle MQ Spirit Trial First Chest', 'Ganons Castle MQ Spirit Trial Second Chest',
                 'Ganons Castle MQ Spirit Trial Sun Front Left Chest', 'Ganons Castle MQ Spirit Trial Sun Back Left Chest',
                 'Ganons Castle MQ Spirit Trial Golden Gauntlets Chest', 'Ganons Castle MQ Spirit Trial Sun Back Right Chest',
                 'Ganons Castle Spirit Trial Clear']),
            create_dungeon_region(
                'Ganons Castle Light Trial',
                ['Ganons Castle MQ Light Trial Lullaby Chest', 'Ganons Castle Light Trial Clear'])
        ])
    else:
        world.regions.extend([
            create_dungeon_region(
                'Ganons Castle Lobby',
                None,
                ['Ganons Castle Exit', 'Ganons Castle Forest Trial', 'Ganons Castle Fire Trial', 'Ganons Castle Water Trial',
                 'Ganons Castle Shadow Trial', 'Ganons Castle Spirit Trial', 'Ganons Castle Light Trial',
                 'Ganons Castle Tower', 'Ganons Castle Deku Scrubs']),
            create_dungeon_region(
                'Ganons Castle Deku Scrubs',
                ['GC Deku Scrub Bombs', 'GC Deku Scrub Arrows', 'GC Deku Scrub Red Potion', 'GC Deku Scrub Green Potion']),
            create_dungeon_region(
                'Ganons Castle Forest Trial',
                ['Ganons Castle Forest Trial Chest', 'Ganons Castle Forest Trial Clear']),
            create_dungeon_region(
                'Ganons Castle Fire Trial',
                ['Ganons Castle Fire Trial Clear']),
            create_dungeon_region(
                'Ganons Castle Water Trial',
                ['Ganons Castle Water Trial Left Chest', 'Ganons Castle Water Trial Right Chest',
                 'Ganons Castle Water Trial Clear']),
            create_dungeon_region(
                'Ganons Castle Shadow Trial',
                ['Ganons Castle Shadow Trial First Chest', 'Ganons Castle Shadow Trial Second Chest',
                 'Ganons Castle Shadow Trial Clear']),
            create_dungeon_region(
                'Ganons Castle Spirit Trial',
                ['Ganons Castle Spirit Trial First Chest', 'Ganons Castle Spirit Trial Second Chest',
                 'Ganons Castle Spirit Trial Clear']),
            create_dungeon_region(
                'Ganons Castle Light Trial',
                ['Ganons Castle Light Trial First Left Chest', 'Ganons Castle Light Trial Second Left Chest',
                 'Ganons Castle Light Trial Third Left Chest', 'Ganons Castle Light Trial First Right Chest',
                 'Ganons Castle Light Trial Second Right Chest', 'Ganons Castle Light Trial Third Right Chest',
                 'Ganons Castle Light Trial Invisible Enemies Chest', 'Ganons Castle Light Trial Lullaby Chest',
                 'Ganons Castle Light Trial Clear'])
        ])

    world.initialize_regions()

