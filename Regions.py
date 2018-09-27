import collections
from BaseClasses import Region, Location, Entrance, RegionType

def shop_address(shop_id, shelf_id):
    return 0xC71ED0 + (0x40 * shop_id) + (0x08 * shelf_id)

def create_regions(world):

    world.regions = [
        create_ow_region(
            'Kokiri Forest', 
            ['Kokiri Sword Chest', 'GS Kokiri Know It All House', 'GS Kokiri Bean Patch', 'GS Kokiri House of Twins', 
             'Deku Baba Sticks', 'Deku Baba Nuts'], 
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
             'LW Deku Scrub Deku Nuts', 'LW Deku Scrub Deku Sticks'], 
            ['Lost Woods Front', 'Meadow Entrance', 'Woods to Goron City', 'Lost Woods Dive Warp', 'Adult Meadow Access', 
             'Lost Woods Generic Grotto', 'Deku Theater', 'Lost Woods Sales Grotto']),
        create_ow_region('Sacred Forest Meadow Entryway', None, ['Meadow Exit', 'Meadow Gate', 'Front of Meadow Grotto']),
        create_ow_region(
            'Sacred Forest Meadow', 
            ['Song from Saria'], 
            ['Meadow Gate Exit', 'Meadow Fairy Grotto', 'Meadow Storms Grotto Child Access']),
        create_ow_region('Lost Woods Bridge', ['Gift from Saria'], ['Kokiri Forest Entrance', 'Forest Exit']),
        create_ow_region('Hyrule Field', 
            ['Ocarina of Time', 'Song from Ocarina of Time'], 
            ['Field to Forest', 'Field to Lake', 'Field to Valley', 'Field to Castle Town', 'Field to Kakariko', 
             'Field to Zora River', 'Lon Lon Rance Entrance', 'Remote Southern Grotto', 'Field Near Lake Outside Fence Grotto', 
             'Field Near Lake Inside Fence Grotto', 'Field Valley Grotto', 'Field West Castle Town Grotto',
             'Field Far West Castle Town Grotto', 'Field Kakariko Grotto', 'Field North Lon Lon Grotto']),
        create_ow_region(
            'Lake Hylia',
            ['Underwater Bottle', 'Lake Hylia Sun', 'Lake Hylia Freestanding PoH', 'GS Lake Hylia Bean Patch', 
             'GS Lake Hylia Lab Wall', 'GS Lake Hylia Small Island', 'GS Lake Hylia Giant Tree'], 
            ['Lake Exit', 'Lake Hylia Dive Warp', 'Lake Hylia Lab', 'Fishing Hole', 'Water Temple Entrance', 'Lake Hylia Grotto']),
        create_interior_region('Lake Hylia Lab', ['Diving in the Lab', 'GS Lab Underwater Crate']),
        create_interior_region('Fishing Hole', ['Child Fishing', 'Adult Fishing']),
        create_ow_region(
            'Gerudo Valley', 
            ['Gerudo Valley Waterfall Freestanding PoH', 'Gerudo Valley Crate Freestanding PoH', 
             'GS Gerudo Valley Small Bridge', 'GS Gerudo Valley Bean Patch'], 
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
            ['Colossus Fairy', 'Spirit Temple Entrance', 'Desert Colossus Grotto']),
        create_interior_region(
            'Colossus Fairy', 
            ['Desert Colossus Fairy Reward']),
        create_ow_region(
            'Castle Town', 
            None, 
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
            ['Malon Egg', 'GS Hyrule Castle Tree'], 
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
            ['Kakariko Exit', 'Carpenter Boss House', 'House of Skulltulla', 'Impas House', 'Impas House Back', 'Windmill',
             'Kakariko Bazaar', 'Kakariko Shooting Gallery', 'Bottom of the Well', 'Kakariko Potion Shop Front', 
             'Kakariko Potion Shop Back', 'Odd Medicine Building', 'Kakariko Bombable Grotto', 'Kakariko Back Grotto', 
             'Graveyard Entrance', 'Death Mountain Entrance']),
        create_interior_region('Carpenter Boss House'),
        create_interior_region(
            'House of Skulltulla', 
            ['10 Gold Skulltulla Reward', '20 Gold Skulltulla Reward', '30 Gold Skulltulla Reward', 
             '40 Gold Skulltulla Reward', '50 Gold Skulltulla Reward']),
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
        create_ow_region('Shadow Temple Warp Region', None, ['Drop to Graveyard', 'Shadow Temple Entrance']),
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
            'Crater Access', 'Goron Shop', 'Goron City Grotto']),
        create_ow_region(
            'Goron City Woods Warp', 
            None, 
            ['Goron City from Woods', 'Goron City to Woods']),
        create_interior_region(
            'Goron Shop', 
            ['Goron Shop Item 1', 'Goron Shop Item 2', 'Goron Shop Item 3', 'Goron Shop Item 4', 
            'Goron Shop Item 5', 'Goron Shop Item 6', 'Goron Shop Item 7', 'Goron Shop Item 8']),        
        create_ow_region('Darunias Chamber', ['Darunias Joy'], ['Darunias Chamber Exit']),
        create_ow_region(
            'Death Mountain Crater Upper', 
            ['DM Crater Wall Freestanding PoH', 'Biggoron', 'GS Death Mountain Crater Crate', 'DMC Deku Scrub Bombs'], 
            ['Crater Exit', 'Crater Hover Boots', 'Crater Scarecrow', 'Top of Crater Grotto']),
        create_ow_region(
            'Death Mountain Crater Lower', 
            None, 
            ['Crater to City', 'Crater Fairy', 'Crater Bridge', 'Crater Ascent', 'DMC Hammer Grotto']),
        create_ow_region(
            'Death Mountain Crater Central', 
            ['DM Crater Volcano Freestanding PoH', 'Sheik in Crater', 'GS Mountain Crater Bean Patch'], 
            ['Crater Bridge Reverse', 'Fire Temple Entrance']),
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
            ['Zora River Child to Shared', 'Zora River Waterfall']),
        create_ow_region(
            'Zora River Adult', 
            ['GS Zora River Near Raised Grottos', 'GS Zora River Above Bridge'], 
            ['Zoras Domain Adult Access', 'Zora River Adult to Shared']),
        create_ow_region(
            'Zora River Shared', 
            ['Zora River Lower Freestanding PoH', 'Zora River Upper Freestanding PoH'], 
            ['Zora River Downstream', 'Zora River Plateau Open Grotto', 'Zora River Plateau Bombable Grotto', 
             'Zora River Dive Warp', 'Zora River Storms Grotto']),
        create_ow_region(
            'Zoras Domain', 
            ['Diving Minigame', 'Zoras Domain Torch Run', 'King Zora Moves', 'Zoras Domain Stick Pot', 
             'Zoras Domain Nut Pot'], 
            ['Zoras Domain Exit', 'Zoras Domain Dive Warp', 'Behind King Zora', 'Zora Shop Child Access']),
        create_ow_region(
            'Zoras Fountain', 
            ['GS Zora\'s Fountain Tree', 'GS Zora\'s Fountain Above the Log'], 
            ['Zoras Fountain Exit', 'Jabu Jabus Belly', 'Zoras Fountain Fairy']),
        create_ow_region(
            'Zoras Domain Frozen', 
            ['King Zora Thawed', 'GS Zora\'s Domain Frozen Waterfall'], 
            ['Zoras Fountain Adult Access', 'Zora Shop Adult Access']),
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
            ['Adult Meadow Exit', 'Forest Temple Entrance', 'Meadow Storms Grotto Adult Access']),
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
        create_grotto_region('Field Valley Grotto', ['GS Hyrule Field Near Gerudo Valley']),
        create_grotto_region('Field West Castle Town Grotto', ['Field West Castle Town Grotto Chest']),
        create_grotto_region('Field Far West Castle Town Grotto'),
        create_grotto_region('Field Kakariko Grotto', ['GS Hyrule Field near Kakariko']),
        create_grotto_region('Field North Lon Lon Grotto', ['Tektite Grotto Freestanding PoH']),
        create_grotto_region('Castle Storms Grotto', ['GS Hyrule Castle Grotto']),
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

    if world.dungeon_mq['DT']:
        world.regions.extend([
            create_dungeon_region(
                'Deku Tree Lobby', 
                ['Deku Tree MQ Lobby Chest', 'Deku Tree MQ Slingshot Chest', 'Deku Tree MQ Slingshot Room Back Chest', 
                 'Deku Tree MQ Basement Chest', 'GS Deku Tree MQ Lobby'], 
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
                 'GS Deku Tree Basement Gate'], 
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

    if world.dungeon_mq['DC']:
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
                ['Dodongos Cavern Bomb Drop']),
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
                ['Dodongos Cavern Retreat', 'Dodongos Cavern Left Door']),
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

    if world.dungeon_mq['JB']:
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

    if world.dungeon_mq['FoT']:
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

    if world.dungeon_mq['FiT']:
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

    if world.dungeon_mq['WT']:
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

    if world.dungeon_mq['SpT']:
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

    if world.dungeon_mq['ShT']:
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
                 'GS Shadow Temple Tripple Giant Pot'])
        ])

    if world.dungeon_mq['BW']:
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

    if world.dungeon_mq['IC']:
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

    if world.dungeon_mq['GTG']:
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

    if world.dungeon_mq['GC']:
        world.regions.extend([
            create_dungeon_region(
                'Ganons Castle Lobby', 
                ['GC MQ Deku Scrub Bombs', 'GC MQ Deku Scrub Arrows', 'GC MQ Deku Scrub Red Potion', 'GC MQ Deku Scrub Green Potion',
                 'GC MQ Deku Scrub Deku Nuts'],
                ['Ganons Castle Exit', 'Ganons Castle Forest Trial', 'Ganons Castle Fire Trial', 'Ganons Castle Water Trial', 
                 'Ganons Castle Shadow Trial', 'Ganons Castle Spirit Trial', 'Ganons Castle Light Trial', 
                 'Ganons Castle Tower']),            
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
                ['GC Deku Scrub Bombs', 'GC Deku Scrub Arrows', 'GC Deku Scrub Red Potion', 'GC Deku Scrub Green Potion'],
                ['Ganons Castle Exit', 'Ganons Castle Forest Trial', 'Ganons Castle Fire Trial', 'Ganons Castle Water Trial', 
                 'Ganons Castle Shadow Trial', 'Ganons Castle Spirit Trial', 'Ganons Castle Light Trial', 
                 'Ganons Castle Tower']),            
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
                 'Ganons Castle Light Trail Invisible Enemies Chest', 'Ganons Castle Light Trial Lullaby Chest', 
                 'Ganons Castle Light Trial Clear'])
        ])

    world.initialize_regions()

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
        address, address2, default, type, scene, hint = location_table[location]
        ret.locations.append(Location(location, address, address2, default, type, scene, hint, ret))
    return ret

location_table = {
    'Kokiri Sword Chest': (0x20A6142, None, 0x04E0, 'Chest', 0x55, 'Kokiri Forest'),
    'Mido Chest Top Left': (0x2F7B08A, None, 0x59A0, 'Chest', 0x28, 'Kokiri Forest'),
    'Mido Chest Top Right': (0x2F7B09A, None, 0x59A1, 'Chest', 0x28, 'Kokiri Forest'),
    'Mido Chest Bottom Left': (0x2F7B0AA, None, 0x5982, 'Chest', 0x28, 'Kokiri Forest'),
    'Mido Chest Bottom Right': (0x2F7B0BA, None, 0x5903, 'Chest', 0x28, 'Kokiri Forest'),
    'Shield Grave Chest': (0x328B096, None, 0x5540, 'Chest', 0x40, 'the Graveyard'),
    'Heart Piece Grave Chest': (0x2D0A056, None, 0xA7C0, 'Chest', 0x3F, 'the Graveyard'),
    'Composer Grave Chest': (0x332D0EA, None, 0x8020, 'Chest', 0x41, 'the Graveyard'),
    'Death Mountain Bombable Chest': (0x223C3CA, 0x223C7B2, 0x5AA1, 'Chest', 0x60, 'Death Mountain Trail'),
    'Goron City Leftmost Maze Chest': (0x227C23A, 0x227C70A, 0x5AC0, 'Chest', 0x62, 'Goron City'),
    'Goron City Left Maze Chest': (0x227C24A, 0x227C71A, 0x5AA1, 'Chest', 0x62, 'Goron City'),
    'Goron City Right Maze Chest': (0x227C25A, 0x227C72A, 0x5AA2, 'Chest', 0x62, 'Goron City'),
    'Zoras Domain Torch Run': (0x2103166, None, 0xB7C0, 'Chest', 0x58, 'Zora\'s Domain'),
    'Hookshot Chest': (0x3063092, None, 0x1100, 'Chest', 0x48, 'the Graveyard'),
    'Gerudo Valley Hammer Rocks Chest': (0x213D676, None, 0x5AA0, 'Chest', 0x5A, 'Gerudo Valley'),
    'Gerudo Fortress Rooftop Chest': (0x21BD4AA, 0x21BD6EA, 0x07C0, 'Chest', 0x5D, 'Gerudo Fortress'),
    'Haunted Wasteland Structure Chest': (0x21E20DE, None, 0x8AA0, 'Chest', 0x5E, 'Haunted Wasteland'),
    'Redead Grotto Chest': (0x26CF076, None, 0x7ACA, 'Chest', 0x3E, 'Kakariko Village'),
    'Wolfos Grotto Chest': (0x26EB076, None, 0x7AB1, 'Chest', 0x3E, 'Sacred Forest Meadow'),
    'Silver Gauntlets Chest': (0x21A02DE, 0x21A06F2, 0x06AB, 'Chest', 0x5C, 'Desert Colossus'),
    'Mirror Shield Chest': (0x21A02CE, 0x21A06E2, 0x3569, 'Chest', 0x5C, 'Desert Colossus'),
    'Field West Castle Town Grotto Chest': (None, None, 0x00, 'Chest', 0x3E, 'Hyrule Field'),
    'Remote Southern Grotto Chest': (None, None, 0x02, 'Chest', 0x3E, 'Hyrule Field'),
    'Field Near Lake Outside Fence Grotto Chest': (None, None, 0x03, 'Chest', 0x3E, 'Hyrule Field'),
    'Kakariko Back Grotto Chest': (None, None, 0x08, 'Chest', 0x3E, 'Kakariko Village'),
    'Zora River Plateau Open Grotto Chest': (None, None, 0x09, 'Chest', 0x3E, 'Zora River'),
    'Kokiri Forest Storms Grotto Chest': (None, None, 0x0C, 'Chest', 0x3E, 'Kokiri Forest'),
    'Lost Woods Generic Grotto Chest': (None, None, 0x14, 'Chest', 0x3E, 'the Lost Woods'),
    'Mountain Storms Grotto Chest': (None, None, 0x17, 'Chest', 0x3E, 'Death Mountain Trail'),
    'Top of Crater Grotto Chest': (None, None, 0x1A, 'Chest', 0x3E, 'Death Mountain Crater'),
    'Impa at Castle': (0x2E8E925, 0x2E8E925, 0x67, 'Song', 0x51, 'Hyrule Castle'),
    'Song from Malon': (0xD7EB53, 0xD7EBCF, 0x68, 'Song', 0x63, 'Lon Lon Ranch'),
    'Song from Composer Grave': (0x332A871, 0x332A871, 0x6A, 'Song', 0x41, 'the Graveyard'),
    'Song from Saria': (0x20B1DB1, 0x20B1DB1, 0x69, 'Song', 0x56, 'Sacred Forest Meadow'),
    'Song from Ocarina of Time': (0x252FC89, 0x252FC89, 0x6B, 'Song', 0x51, 'Hyrule Field'),
    'Song at Windmill': (0xE42C07, 0xE42B8B, 0x6C, 'Song', 0x48, 'Kakariko'),
    'Sheik Forest Song': (0x20B0809, 0x20B0809, 0x61, 'Song', 0x56, 'Sacred Forest Meadow'),
    'Sheik at Temple': (0x2531329, 0x2531329, 0x66, 'Song', 0x43, 'Temple of Time'),
    'Sheik in Crater': (0x224D7F1, 0x224D7F1, 0x62, 'Song', 0x61, 'Death Mountain Crater'),
    'Sheik in Ice Cavern': (0x2BEC889, 0x2BEC889, 0x63, 'Song', 0x09, 'Ice Cavern'),
    'Sheik in Kakariko': (0x2000FE1, 0x2000FE1, 0x65, 'Song', 0x52, 'Kakariko'),
    'Sheik at Colossus': (0x218C57D, 0x218C57D, 0x64, 'Song', 0x5C, 'Desert Colossus'),
    'Gift from Saria': (None, None, 0x3B, 'NPC', 0x5B, 'the Lost Woods'),
    'Malon Egg': (None, None, 0x47, 'NPC', 0x5F, 'Hyrule Castle'),
    'Zeldas Letter': (None, None, None, 'NPC', None, 'Hyrule Castle'),
    'Zelda': (0x3481400, None, 0x5A, 'NPC', 0x43, 'the Temple of Time'),
    'Zoras Fountain Fairy Reward': (0x3481401, None, 0x5D, 'NPC', 0x3D, 'Zora\'s Fountain'),
    'Hyrule Castle Fairy Reward': (0x3481402, None, 0x5C, 'NPC', 0x3D, 'Hyrule Castle'),
    'Desert Colossus Fairy Reward': (0x3481403, None, 0x5E, 'NPC', 0x3D, 'Desert Colossus'),
    'Mountain Summit Fairy Reward': (0x3481404, None, 0x51, 'NPC', 0x3B, 'Death Mountain Trail'),
    'Crater Fairy Reward': (0x3481405, None, 0x52, 'NPC', 0x3B, 'Death Mountain Crater'),
    'Ganons Castle Fairy Reward': (0x3481406, None, 0x53, 'NPC', 0x3B, 'outside Ganon\'s Castle'),
    'Treasure Chest Game': (None, None, 0x0A, 'Chest', 0x10, 'the Market'),
    'Darunias Joy': (0xCF1BFF, None, 0x54, 'NPC', 0x62, 'Goron City'),
    'Diving Minigame': (0xE01A2B, 0xE01AA7, 0x37, 'NPC', 0x58, 'Zora\'s Domain'),
    'Child Fishing': (0xDCBFBF, None, 0x3E, 'NPC', 0x49, 'Lake Hylia'),
    'Adult Fishing': (0xDCC087, None, 0x38, 'NPC', 0x49, 'Lake Hylia'),
    'Diving in the Lab': (0xE2CB97, None, 0x3E, 'NPC', 0x38, 'Lake Hylia'),
    'Link the Goron': (0xED30EB, 0xED64F3, 0x2C, 'NPC', 0x62, 'Goron City'),
    'King Zora Thawed': (0xE56AD7, None, 0x2D, 'NPC', 0x58, 'Zora\'s Domain'),
    'Bombchu Bowling Bomb Bag': (0xE2F093, None, 0x34, 'NPC', 0x4B, 'the Market'),
    'Bombchu Bowling Piece of Heart': (0xE2F097, None, 0x3E, 'NPC', 0x4B, 'the Market'),
    'Dog Lady': (0xE65163, 0xE661BB, 0x3E, 'NPC', 0x35, 'the Market'),
    'Skull Kid': (0xDF0F33, 0xDF0E9B, 0x3E, 'NPC', 0x5B, 'the Lost Woods'),
    'Ocarina Memory Game': (0xDF264F, None, 0x76, 'NPC', 0x5B, 'the Lost Woods'),
    '10 Gold Skulltulla Reward': (0xEA7173, None, 0x45, 'NPC', 0x50, 'Kakariko Village'),
    '20 Gold Skulltulla Reward': (0xEA7175, None, 0x39, 'NPC', 0x50, 'Kakariko Village'),
    '30 Gold Skulltulla Reward': (0xEA7177, None, 0x46, 'NPC', 0x50, 'Kakariko Village'),
    '40 Gold Skulltulla Reward': (0xEA7179, None, 0x03, 'NPC', 0x50, 'Kakariko Village'),
    '50 Gold Skulltulla Reward': (0xEA717B, None, 0x3E, 'NPC', 0x50, 'Kakariko Village'),
    'Man on Roof': (0xE587E3, None, 0x3E, 'NPC', 0x52, 'Kakariko Village'),
    'Frog Ocarina Game': (0xDB13D3, None, 0x76, 'NPC', 0x54, 'Zora River'),
    'Frogs in the Rain': (0xDB1387, None, 0x3E, 'NPC', 0x54, 'Zora River'),
    'Horseback Archery 1000 Points': (0xE12B6F, 0xE12AA3, 0x3E, 'NPC', 0x5D, 'Gerudo Fortress'),
    'Horseback Archery 1500 Points': (0xE12BC3, 0xE12AFB, 0x30, 'NPC', 0x5D, 'Gerudo Fortress'),
    'Child Shooting Gallery': (0xD35EF3, None, 0x60, 'NPC', 0x42, 'the Market'),
    'Adult Shooting Gallery': (0xD35F5B, None, 0x30, 'NPC', 0x42, 'Kakariko Village'),
    'Target in Woods': (0xE59CDF, None, 0x60, 'NPC', 0x5B, 'the Lost Woods'),
    'Deku Theater Skull Mask': (0xEC9A87, None, 0x77, 'NPC', 0x3E, 'the Lost Woods'),
    'Deku Theater Mask of Truth': (0xEC9CE7, None, 0x7A, 'NPC', 0x3E, 'the Lost Woods'),
    'Anju as Adult': (0xE1EABB, None, 0x1D, 'NPC', 0x52, 'Kakariko Village'),
    'Biggoron': (0xED338F, 0xED650F, 0x57, 'NPC', 0x60, 'Death Mountain Trail'),
    'Anjus Chickens': (0xE1E7A7, None, 0x0F, 'NPC', 0x52, 'Kakariko Village'),
    'Talons Chickens': (0xCC14EB, None, 0x14, 'NPC', 0x4C, 'Lon Lon Ranch'),
    '10 Big Poes': (0xEE6AEF, None, 0x0F, 'NPC', 0x4D, 'the Market'),
    'Rolling Goron as Child': (0xED296F, 0xED6503, 0x34, 'NPC', 0x62, 'Goron City'),
    'Lake Hylia Sun': (0xE9E1F2, None, 0x5B08, 'Chest', 0x57, 'Lake Hylia'),
    'Underwater Bottle': (0xDE10FB, None, 0x15, 'NPC', 0x57, 'Lake Hylia'),
    'Impa House Freestanding PoH': (None, None, 0x01, 'Collectable', 0x37, 'Kakariko Village'),
    'Tektite Grotto Freestanding PoH': (None, None, 0x01, 'Collectable', 0x3E, 'Hyrule Field'),
    'Windmill Freestanding PoH': (None, None, 0x01, 'Collectable', 0x48, 'Kakariko Village'),
    'Dampe Race Freestanding PoH': (None, None, 0x07, 'Collectable', 0x48, 'the Graveyard'),
    'Lon Lon Tower Freestanding PoH': (None, None, 0x01, 'Collectable', 0x4C, 'Lon Lon Ranch'),
    'Graveyard Freestanding PoH': (None, None, 0x04, 'Collectable', 0x53, 'the Graveyard'),
    'Gravedigging Tour': (None, None, 0x00, 'Collectable', 0x53, 'the Graveyard'),
    'Zora River Lower Freestanding PoH': (None, None, 0x04, 'Collectable', 0x54, 'Zora River'),
    'Zora River Upper Freestanding PoH': (None, None, 0x0B, 'Collectable', 0x54, 'Zora River'),
    'Lake Hylia Freestanding PoH': (None, None, 0x1E, 'Collectable', 0x57, 'Lake Hylia'),
    'Zoras Fountain Iceberg Freestanding PoH': (None, None, 0x01, 'Collectable', 0x59, 'Zora\'s Fountain'),
    'Zoras Fountain Bottom Freestanding PoH': (None, None, 0x14, 'Collectable', 0x59, 'Zora\'s Fountain'),
    'Gerudo Valley Waterfall Freestanding PoH': (None, None, 0x01, 'Collectable', 0x5A, 'Gerudo Valley'),
    'Gerudo Valley Crate Freestanding PoH': (None, None, 0x02, 'Collectable', 0x5A, 'Gerudo Valley'),
    'Colossus Freestanding PoH': (None, None, 0x0D, 'Collectable', 0x5C, 'Desert Colossus'),
    'DM Trail Freestanding PoH': (None, None, 0x1E, 'Collectable', 0x60, 'Death Mountain Trail'),
    'DM Crater Wall Freestanding PoH': (None, None, 0x02, 'Collectable', 0x61, 'Death Mountain Crater'),
    'DM Crater Volcano Freestanding PoH': (None, None, 0x08, 'Collectable', 0x61, 'Death Mountain Crater'),
    'Goron City Pot Freestanding PoH': (None, None, 0x1F, 'Collectable', 0x62, 'Goron City'),
    'Gerudo Fortress North F1 Carpenter': (None, None, 0x0C, 'Collectable', 0x0C, 'Gerudo Fortress'),
    'Gerudo Fortress North F2 Carpenter': (None, None, 0x0A, 'Collectable', 0x0C, 'Gerudo Fortress'),
    'Gerudo Fortress South F1 Carpenter': (None, None, 0x0E, 'Collectable', 0x0C, 'Gerudo Fortress'),
    'Gerudo Fortress South F2 Carpenter': (None, None, 0x0F, 'Collectable', 0x0C, 'Gerudo Fortress'),
    'Gerudo Fortress Membership Card': (None, None, 0x3A, 'NPC', 0x0C, 'Gerudo Fortress'),
    'Queen Gohma Heart': (None, None, 0x4F, 'BossHeart', 0x11, 'Deku Tree'),
    'King Dodongo Heart': (None, None, 0x4F, 'BossHeart', 0x12, 'Dodongo\'s Cavern'),
    'Barinade Heart': (None, None, 0x4F, 'BossHeart', 0x13, 'Jabu Jabu\'s Belly'),
    'Phantom Ganon Heart': (None, None, 0x4F, 'BossHeart', 0x14, 'Forest Temple'),
    'Volvagia Heart': (None, None, 0x4F, 'BossHeart', 0x15, 'Fire Temple'),
    'Morpha Heart': (None, None, 0x4F, 'BossHeart', 0x16, 'Water Temple'),
    'Twinrova Heart': (None, None, 0x4F, 'BossHeart', 0x17, 'Spirit Temple'),
    'Bongo Bongo Heart': (None, None, 0x4F, 'BossHeart', 0x18, 'Shadow Temple'),
    'Magic Bean Salesman': (None, None, None, 'Event', None, 'Zora\'s River'),
    'King Zora Moves': (None, None, None, 'Event', None, 'Zora\'s Domain'),
    'Ocarina of Time': (None, None, 0x0C, 'NPC', 0x51, 'Hyrule Field'),
    'Master Sword Pedestal': (None, None, None, 'Event', None, 'the Temple of Time'),
    'Epona': (None, None, None, 'Event', None, 'Lon Lon Ranch'),
    'Deku Baba Sticks': (None, None, None, 'Event', None, 'Kokiri Forest'),
    'Deku Baba Nuts': (None, None, None, 'Event', None, 'Kokiri Forest'),
    'Goron City Stick Pot': (None, None, None, 'Event', None, 'Goron City'),
    'Bottom of the Well Stick Pot': (None, None, None, 'Event', None, 'Bottom of the Well'),
    'Zoras Domain Stick Pot': (None, None, None, 'Event', None, 'Zora\'s Domain'),
    'Zoras Domain Nut Pot': (None, None, None, 'Event', None, 'Zora\'s Domain'),
    'Spirit Temple Nut Crate': (None, None, None, 'Event', None, 'Spirit Temple'),
    'Gerudo Fortress Carpenter Rescue': (None, None, None, 'Event', None, 'Gerudo Fortress'),
    'Ganons Castle Forest Trial Clear': (None, None, None, 'Event', None, 'Ganon\'s Castle'),
    'Ganons Castle Fire Trial Clear': (None, None, None, 'Event', None, 'Ganon\'s Castle'),
    'Ganons Castle Water Trial Clear': (None, None, None, 'Event', None, 'Ganon\'s Castle'),
    'Ganons Castle Shadow Trial Clear': (None, None, None, 'Event', None, 'Ganon\'s Castle'),
    'Ganons Castle Spirit Trial Clear': (None, None, None, 'Event', None, 'Ganon\'s Castle'),
    'Ganons Castle Light Trial Clear': (None, None, None, 'Event', None, 'Ganon\'s Castle'),

    # Deku Tree vanilla
    'Deku Tree Lobby Chest': (0x24A7146, None, 0x0823, 'Chest', 0x00, 'Deku Tree'),
    'Deku Tree Slingshot Chest': (0x24C20C6, None, 0x00A1, 'Chest', 0x00, 'Deku Tree'),
    'Deku Tree Slingshot Room Side Chest': (0x24C20D6, None, 0x5905, 'Chest', 0x00, 'Deku Tree'),
    'Deku Tree Compass Chest': (0x25040D6, None, 0x0802, 'Chest', 0x00, 'Deku Tree'),
    'Deku Tree Compass Room Side Chest': (0x25040E6, None, 0x5906, 'Chest', 0x00, 'Deku Tree'),
    'Deku Tree Basement Chest': (0x24C8166, None, 0x5904, 'Chest', 0x00, 'Deku Tree'),
    # Deku Tree MQ
    'Deku Tree MQ Lobby Chest': (0, None, 0x0823, 'Chest', 0x00, 'Deku Tree'),
    'Deku Tree MQ Compass Chest': (0, None, 0x0801, 'Chest', 0x00, 'Deku Tree'),
    'Deku Tree MQ Slingshot Chest': (0, None, 0x10A6, 'Chest', 0x00, 'Deku Tree'),
    'Deku Tree MQ Slingshot Room Back Chest': (0, None, 0x8522, 'Chest', 0x00, 'Deku Tree'),
    'Deku Tree MQ Basement Chest': (0, None, 0x8524, 'Chest', 0x00, 'Deku Tree'),
    'Deku Tree MQ Before Spinning Log Chest': (0, None, 0x5905, 'Chest', 0x00, 'Deku Tree'),
    'Deku Tree MQ After Spinning Log Chest': (0, None, 0x5AA0, 'Chest', 0x00, 'Deku Tree'),

    # Dodongo's Cavern shared
    'Chest Above King Dodongo': (0x2EB00BA, None, 0x5020, 'Chest', 0x12, 'Dodongo\'s Cavern'),
    # Dodongo's Cavern vanilla
    'Dodongos Cavern Map Chest': (0x1F2819E, None, 0x0828, 'Chest', 0x01, 'Dodongo\'s Cavern'),
    'Dodongos Cavern Compass Chest': (0x1FAF0AA, None, 0x0805, 'Chest', 0x01, 'Dodongo\'s Cavern'),
    'Dodongos Cavern Bomb Flower Platform': (0x1F890DE, None, 0x59C6, 'Chest', 0x01, 'Dodongo\'s Cavern'),
    'Dodongos Cavern Bomb Bag Chest': (0x1F890CE, None, 0x0644, 'Chest', 0x01, 'Dodongo\'s Cavern'),
    'Dodongos Cavern End of Bridge Chest': (0x1F281CE, None, 0x552A, 'Chest', 0x01, 'Dodongo\'s Cavern'),
    # Dodongo's Cavern MQ
    'Dodongos Cavern MQ Map Chest': (0, None, 0x0820, 'Chest', 0x01, 'Dodongo\'s Cavern'),
    'Dodongos Cavern MQ Bomb Bag Chest': (0, None, 0x0644, 'Chest', 0x01, 'Dodongo\'s Cavern'),
    'Dodongos Cavern MQ Compass Chest': (0, None, 0x1805, 'Chest', 0x01, 'Dodongo\'s Cavern'),
    'Dodongos Cavern MQ Larva Room Chest': (0, None, 0x7522, 'Chest', 0x01, 'Dodongo\'s Cavern'),
    'Dodongos Cavern MQ Torch Puzzle Room Chest': (0, None, 0x59A3, 'Chest', 0x01, 'Dodongo\'s Cavern'),
    'Dodongos Cavern MQ Under Grave Chest': (0, None, 0x5541, 'Chest', 0x01, 'Dodongo\'s Cavern'),

    # Jabu Jabu's Belly vanilla
    'Boomerang Chest': (0x278A0BA, None, 0x10C1, 'Chest', 0x02, 'Jabu Jabu\'s Belly'),
    'Jabu Jabus Belly Map Chest': (0x278E08A, None, 0x1822, 'Chest', 0x02, 'Jabu Jabu\'s Belly'),
    'Jabu Jabus Belly Compass Chest': (0x279608A, None, 0xB804, 'Chest', 0x02, 'Jabu Jabu\'s Belly'),
    # Jabu Jabu's Belly MQ
    'Jabu Jabus Belly MQ Entry Side Chest': (0, None, 0x8045, 'Chest', 0x02, 'Jabu Jabu\'s Belly'),
    'Jabu Jabus Belly MQ Map Chest': (0, None, 0xB823, 'Chest', 0x02, 'Jabu Jabu\'s Belly'),
    'Jabu Jabus Belly MQ Second Room Lower Chest': (0, None, 0x5042, 'Chest', 0x02, 'Jabu Jabu\'s Belly'),
    'Jabu Jabus Belly MQ Compass Chest': (0, None, 0xB800, 'Chest', 0x02, 'Jabu Jabu\'s Belly'),
    'Jabu Jabus Belly MQ Second Room Upper Chest': (0, None, 0x8907, 'Chest', 0x02, 'Jabu Jabu\'s Belly'),
    'Jabu Jabus Belly MQ Basement North Chest': (0, None, 0x8048, 'Chest', 0x02, 'Jabu Jabu\'s Belly'),
    'Jabu Jabus Belly MQ Basement South Chest': (0, None, 0x8064, 'Chest', 0x02, 'Jabu Jabu\'s Belly'),
    'Jabu Jabus Belly MQ Near Boss Chest': (0, None, 0x852A, 'Chest', 0x02, 'Jabu Jabu\'s Belly'),
    'Jabu Jabus Belly MQ Falling Like Like Room Chest': (0, None, 0x70E9, 'Chest', 0x02, 'Jabu Jabu\'s Belly'),
    'Jabu Jabus Belly MQ Boomerang Room Small Chest': (0, None, 0x5041, 'Chest', 0x02, 'Jabu Jabu\'s Belly'),
    'MQ Boomerang Chest': (0, None, 0x10C6, 'Chest', 0x02, 'Jabu Jabu\'s Belly'),

    # Forest Temple vanilla
    'Forest Temple First Chest': (0x23E5092, None, 0x5843, 'Chest', 0x03, 'Forest Temple'),
    'Forest Temple Chest Behind Lobby': (0x2415082, None, 0x7840, 'Chest', 0x03, 'Forest Temple'),
    'Forest Temple Well Chest': (0x244A062, None, 0x5849, 'Chest', 0x03, 'Forest Temple'),
    'Forest Temple Map Chest': (0x2455076, None, 0x1821, 'Chest', 0x03, 'Forest Temple'),
    'Forest Temple Outside Hookshot Chest': (0x241F0D6, None, 0x5905, 'Chest', 0x03, 'Forest Temple'),
    'Forest Temple Falling Room Chest': (0x247E09E, None, 0x5947, 'Chest', 0x03, 'Forest Temple'),
    'Forest Temple Block Push Chest': (0x245B096, None, 0x8964, 'Chest', 0x03, 'Forest Temple'),
    'Forest Temple Boss Key Chest': (0xCB0DC2, None, 0x27EE, 'Chest', 0x03, 'Forest Temple'),
    'Forest Temple Floormaster Chest': (0x2490072, None, 0x7842, 'Chest', 0x03, 'Forest Temple'),
    'Forest Temple Bow Chest': (0x2415092, None, 0xB08C, 'Chest', 0x03, 'Forest Temple'),
    'Forest Temple Red Poe Chest': (0x246607E, None, 0x784D, 'Chest', 0x03, 'Forest Temple'),
    'Forest Temple Blue Poe Chest': (0x246F07E, None, 0x180F, 'Chest', 0x03, 'Forest Temple'),
    'Forest Temple Near Boss Chest': (0x2486082, None, 0x592B, 'Chest', 0x03, 'Forest Temple'),
    # Forest Temple MQ
    'Forest Temple MQ First Chest': (0, None, 0x8843, 'Chest', 0x03, 'Forest Temple'),
    'Forest Temple MQ Chest Behind Lobby': (0, None, 0x7840, 'Chest', 0x03, 'Forest Temple'),
    'Forest Temple MQ Bow Chest': (0, None, 0xB08C, 'Chest', 0x03, 'Forest Temple'),
    'Forest Temple MQ NE Outdoors Lower Chest': (0, None, 0x5841, 'Chest', 0x03, 'Forest Temple'),
    'Forest Temple MQ NE Outdoors Upper Chest': (0, None, 0x5845, 'Chest', 0x03, 'Forest Temple'),
    'Forest Temple MQ Well Chest': (0, None, 0x5849, 'Chest', 0x03, 'Forest Temple'),
    'Forest Temple MQ Map Chest': (0, None, 0x182D, 'Chest', 0x03, 'Forest Temple'),
    'Forest Temple MQ Compass Chest': (0, None, 0x180F, 'Chest', 0x03, 'Forest Temple'),
    'Forest Temple MQ Falling Room Chest': (0, None, 0x8926, 'Chest', 0x03, 'Forest Temple'),
    'Forest Temple MQ Near Boss Chest': (0, None, 0x592B, 'Chest', 0x03, 'Forest Temple'),
    'Forest Temple MQ Redead Chest': (0, None, 0x7842, 'Chest', 0x03, 'Forest Temple'),
    'Forest Temple MQ Boss Key Chest': (0, None, 0x27EE, 'Chest', 0x03, 'Forest Temple'), # This needs tested to see if it has changed from vanilla.

    # Fire Temple vanilla
    'Fire Temple Chest Near Boss': (0x230808A, None, 0x5841, 'Chest', 0x04, 'Fire Temple'),
    'Fire Temple Fire Dancer Chest': (0x2318082, None, 0x7CC0, 'Chest', 0x04, 'Fire Temple'),
    'Fire Temple Boss Key Chest': (0x238A0D6, None, 0x27EC, 'Chest', 0x04, 'Fire Temple'),
    'Fire Temple Big Lava Room Bombable Chest': (0x23AD076, None, 0x5842, 'Chest', 0x04, 'Fire Temple'),
    'Fire Temple Big Lava Room Open Chest': (0x239D0A6, None, 0x5844, 'Chest', 0x04, 'Fire Temple'),
    'Fire Temple Boulder Maze Lower Chest': (0x2323152, None, 0x5843, 'Chest', 0x04, 'Fire Temple'),
    'Fire Temple Boulder Maze Upper Chest': (0x2323182, None, 0x5846, 'Chest', 0x04, 'Fire Temple'),
    'Fire Temple Boulder Maze Side Room': (0x23B40B2, None, 0x5848, 'Chest', 0x04, 'Fire Temple'),
    'Fire Temple Boulder Maze Bombable Pit': (0x231B0E2, None, 0x584B, 'Chest', 0x04, 'Fire Temple'),
    'Fire Temple Scarecrow Chest': (0x2339082, None, 0x5ACD, 'Chest', 0x04, 'Fire Temple'),
    'Fire Temple Map Chest': (0x237E0C2, None, 0x082A, 'Chest', 0x04, 'Fire Temple'),
    'Fire Temple Compass Chest': (0x23C1082, None, 0x0807, 'Chest', 0x04, 'Fire Temple'),
    'Fire Temple Highest Goron Chest': (0x2365066, None, 0x5849, 'Chest', 0x04, 'Fire Temple'),
    'Fire Temple Megaton Hammer Chest': (0x236C102, None, 0x01A5, 'Chest', 0x04, 'Fire Temple'),
    # Fire Temple MQ
    'Fire Temple MQ Chest Near Boss': (0, None, 0x5847, 'Chest', 0x04, 'Fire Temple'),
    'Fire Temple MQ Megaton Hammer Chest': (0, None, 0x11A0, 'Chest', 0x04, 'Fire Temple'),
    'Fire Temple MQ Compass Chest': (0, None, 0x080B, 'Chest', 0x04, 'Fire Temple'),
    'Fire Temple MQ Maze Lower Chest': (0, None, 0x5CC3, 'Chest', 0x04, 'Fire Temple'),
    'Fire Temple MQ Maze Upper Chest': (0, None, 0x5CE6, 'Chest', 0x04, 'Fire Temple'),
    'Fire Temple MQ West Tower Top Chest': (0, None, 0x5845, 'Chest', 0x04, 'Fire Temple'),
    'Fire Temple MQ Entrance Hallway Small Chest': (0, None, 0x7542, 'Chest', 0x04, 'Fire Temple'),
    'Fire Temple MQ Map Chest': (0, None, 0x082C, 'Chest', 0x04, 'Fire Temple'),
    'Fire Temple MQ Boss Key Chest': (0, None, 0x27E4, 'Chest', 0x04, 'Fire Temple'),
    'Fire Temple MQ Big Lava Room Bombable Chest': (0, None, 0x5841, 'Chest', 0x04, 'Fire Temple'),
    'Fire Temple MQ Maze Side Room': (0, None, 0x5848, 'Chest', 0x04, 'Fire Temple'),
    'Fire Temple MQ Freestanding Key': (None, None, 0x1C, 'Collectable', 0x04, 'Fire Temple'), 

    # Water Temple vanilla
    'Water Temple Map Chest': (0x26690A6, None, 0x1822, 'Chest', 0x05, 'Water Temple'),
    'Water Temple Compass Chest': (0x25FC0D2, None, 0x0809, 'Chest', 0x05, 'Water Temple'),
    'Water Temple Torches Chest': (0x26640A6, None, 0x7841, 'Chest', 0x05, 'Water Temple'),
    'Water Temple Dragon Chest': (0x261F0BA, None, 0x584A, 'Chest', 0x05, 'Water Temple'),
    'Water Temple Central Bow Target Chest': (0x266D072, None, 0x5848, 'Chest', 0x05, 'Water Temple'),
    'Water Temple Central Pillar Chest': (0x25EF0D6, None, 0x5846, 'Chest', 0x05, 'Water Temple'),
    'Water Temple Cracked Wall Chest': (0x265B0A6, None, 0x5840, 'Chest', 0x05, 'Water Temple'),
    'Water Temple Boss Key Chest': (0x2657066, None, 0x27E5, 'Chest', 0x05, 'Water Temple'),
    'Water Temple Dark Link Chest': (0x261907A, None, 0x0127, 'Chest', 0x05, 'Water Temple'),
    'Water Temple River Chest': (0x26740DE, None, 0x5843, 'Chest', 0x05, 'Water Temple'),
    # Water Temple MQ
    'Water Temple MQ Central Pillar Chest': (0, None, 0x8846, 'Chest', 0x05, 'Water Temple'),
    'Water Temple MQ Boss Key Chest': (0, None, 0x27E5, 'Chest', 0x05, 'Water Temple'),
    'Water Temple MQ Longshot Chest': (0, None, 0xB120, 'Chest', 0x05, 'Water Temple'),
    'Water Temple MQ Compass Chest': (0, None, 0x1801, 'Chest', 0x05, 'Water Temple'),
    'Water Temple MQ Map Chest': (0, None, 0xB822, 'Chest', 0x05, 'Water Temple'),
    'Water Temple MQ Freestanding Key': (None, None, 0x01, 'Collectable', 0x05, 'Water Temple'), 

    # Spirit Temple vanilla
    'Spirit Temple Child Left Chest': (0x2B190BA, None, 0x5528, 'Chest', 0x06, 'Spirit Temple'),
    'Spirit Temple Child Right Chest': (0x2B13182, None, 0x8840, 'Chest', 0x06, 'Spirit Temple'),
    'Spirit Temple Compass Chest': (0x2B6B08A, None, 0x3804, 'Chest', 0x06, 'Spirit Temple'),
    'Spirit Temple Early Adult Right Chest': (0x2B6207A, None, 0x5847, 'Chest', 0x06, 'Spirit Temple'),
    'Spirit Temple First Mirror Right Chest': (0x2B700C6, None, 0x890D, 'Chest', 0x06, 'Spirit Temple'),
    'Spirit Temple First Mirror Left Chest': (0x2B700D6, None, 0x8F8E, 'Chest', 0x06, 'Spirit Temple'),
    'Spirit Temple Map Chest': (0x2B25126, None, 0xB823, 'Chest', 0x06, 'Spirit Temple'),
    'Spirit Temple Child Climb East Chest': (0x2B1D122, None, 0x8066, 'Chest', 0x06, 'Spirit Temple'),
    'Spirit Temple Child Climb North Chest': (0x2B1D132, None, 0x852C, 'Chest', 0x06, 'Spirit Temple'),
    'Spirit Temple Sun Block Room Chest': (0x2B481B2, None, 0x8841, 'Chest', 0x06, 'Spirit Temple'),
    'Spirit Temple Statue Hand Chest': (0x2B25136, None, 0x8842, 'Chest', 0x06, 'Spirit Temple'),
    'Spirit Temple NE Main Room Chest': (0x2B25146, None, 0x888F, 'Chest', 0x06, 'Spirit Temple'),
    'Spirit Temple Near Four Armos Chest': (0x2B9F076, None, 0x5845, 'Chest', 0x06, 'Spirit Temple'),
    'Spirit Temple Hallway Left Invisible Chest': (0x2B900B6, None, 0x6914, 'Chest', 0x06, 'Spirit Temple'),
    'Spirit Temple Hallway Right Invisible Chest': (0x2B900C6, None, 0x6915, 'Chest', 0x06, 'Spirit Temple'),
    'Spirit Temple Boss Key Chest': (0x2BA4162, None, 0x27EA, 'Chest', 0x06, 'Spirit Temple'),
    'Spirit Temple Topmost Chest': (0x2BCF0FE, None, 0x8CF2, 'Chest', 0x06, 'Spirit Temple'),
    # Spirit Temple MQ
    'Spirit Temple MQ Entrance Front Left Chest': (0, None, 0x507A, 'Chest', 0x06, 'Spirit Temple'),
    'Spirit Temple MQ Entrance Back Right Chest': (0, None, 0x807F, 'Chest', 0x06, 'Spirit Temple'),
    'Spirit Temple MQ Entrance Front Right Chest': (0, None, 0x885B, 'Chest', 0x06, 'Spirit Temple'),
    'Spirit Temple MQ Entrance Back Left Chest': (0, None, 0x885E, 'Chest', 0x06, 'Spirit Temple'),
    'Spirit Temple MQ Child Center Chest': (0, None, 0x885D, 'Chest', 0x06, 'Spirit Temple'),
    'Spirit Temple MQ Map Chest': (0, None, 0x0820, 'Chest', 0x06, 'Spirit Temple'),
    'Spirit Temple MQ Child Left Chest': (0, None, 0x7848, 'Chest', 0x06, 'Spirit Temple'),
    'Spirit Temple MQ Child Climb North Chest': (0, None, 0x7066, 'Chest', 0x06, 'Spirit Temple'),
    'Spirit Temple MQ Child Climb South Chest': (0, None, 0x884C, 'Chest', 0x06, 'Spirit Temple'),
    'Spirit Temple MQ Compass Chest': (0, None, 0xB803, 'Chest', 0x06, 'Spirit Temple'),
    'Spirit Temple MQ Lower NE Main Room Chest': (0, None, 0x888F, 'Chest', 0x06, 'Spirit Temple'),
    'Spirit Temple MQ Upper NE Main Room Chest': (0, None, 0x6902, 'Chest', 0x06, 'Spirit Temple'),
    'Spirit Temple MQ Silver Block Hallway Chest': (0, None, 0x885C, 'Chest', 0x06, 'Spirit Temple'),
    'Spirit Temple MQ Sun Block Room Chest': (0, None, 0x8901, 'Chest', 0x06, 'Spirit Temple'),
    'Spirit Temple MQ Lower Adult Right Chest': (0, None, 0x5AA7, 'Chest', 0x06, 'Spirit Temple'),
    'Spirit Temple MQ Lower Adult Left Chest': (0, None, 0x7AA4, 'Chest', 0x06, 'Spirit Temple'),
    'Spirit Temple MQ Beamos Room Chest': (0, None, 0x7979, 'Chest', 0x06, 'Spirit Temple'),
    'Spirit Temple MQ Ice Trap Chest': (0, None, 0x5F98, 'Chest', 0x06, 'Spirit Temple'),
    'Spirit Temple MQ Boss Key Chest': (0, None, 0x27E5, 'Chest', 0x06, 'Spirit Temple'),
    'Spirit Temple MQ Mirror Puzzle Invisible Chest': (0, None, 0x6852, 'Chest', 0x06, 'Spirit Temple'),

    # Shadow Temple vanilla
    'Shadow Temple Map Chest': (0x27CC0AA, None, 0x1821, 'Chest', 0x07, 'Shadow Temple'),
    'Shadow Temple Hover Boots Chest': (0x27DC0CA, None, 0x15E7, 'Chest', 0x07, 'Shadow Temple'),
    'Shadow Temple Compass Chest': (0x27EC09E, None, 0x1803, 'Chest', 0x07, 'Shadow Temple'),
    'Shadow Temple Early Silver Rupee Chest': (0x27E40F6, None, 0x5842, 'Chest', 0x07, 'Shadow Temple'),
    'Shadow Temple Invisible Blades Visible Chest': (0x282212A, None, 0x588C, 'Chest', 0x07, 'Shadow Temple'),
    'Shadow Temple Invisible Blades Invisible Chest': (0x282211A, None, 0x6976, 'Chest', 0x07, 'Shadow Temple'),
    'Shadow Temple Falling Spikes Lower Chest': (0x2801132, None, 0x5945, 'Chest', 0x07, 'Shadow Temple'),
    'Shadow Temple Falling Spikes Upper Chest': (0x2801142, None, 0x5886, 'Chest', 0x07, 'Shadow Temple'),
    'Shadow Temple Falling Spikes Switch Chest': (0x2801122, None, 0x8844, 'Chest', 0x07, 'Shadow Temple'),
    'Shadow Temple Invisible Spikes Chest': (0x28090EE, None, 0x7889, 'Chest', 0x07, 'Shadow Temple'),
    'Shadow Temple Wind Hint Chest': (0x283609A, None, 0x6955, 'Chest', 0x07, 'Shadow Temple'),
    'Shadow Temple After Wind Enemy Chest': (0x28390FE, None, 0x7888, 'Chest', 0x07, 'Shadow Temple'),
    'Shadow Temple After Wind Hidden Chest': (0x28390EE, None, 0x6854, 'Chest', 0x07, 'Shadow Temple'),
    'Shadow Temple Spike Walls Left Chest': (0x28130B6, None, 0x588A, 'Chest', 0x07, 'Shadow Temple'),
    'Shadow Temple Boss Key Chest': (0x28130A6, None, 0x27EB, 'Chest', 0x07, 'Shadow Temple'),
    'Shadow Temple Hidden Floormaster Chest': (0x282508A, None, 0x784D, 'Chest', 0x07, 'Shadow Temple'),
    'Shadow Temple Freestanding Key': (None, None, 0x01, 'Collectable', 0x07, 'Shadow Temple'),
    # Shadow Temple MQ
    'Shadow Temple MQ Compass Chest': (0, None, 0x1801, 'Chest', 0x07, 'Shadow Temple'),
    'Shadow Temple MQ Hover Boots Chest': (0, None, 0x15E7, 'Chest', 0x07, 'Shadow Temple'),
    'Shadow Temple MQ Early Gibdos Chest': (0, None, 0x0822, 'Chest', 0x07, 'Shadow Temple'),
    'Shadow Temple MQ Map Chest': (0, None, 0x7843, 'Chest', 0x07, 'Shadow Temple'),
    'Shadow Temple MQ Beamos Silver Rupees Chest': (0, None, 0x892F, 'Chest', 0x07, 'Shadow Temple'),
    'Shadow Temple MQ Falling Spikes Switch Chest': (0, None, 0x8844, 'Chest', 0x07, 'Shadow Temple'),
    'Shadow Temple MQ Falling Spikes Lower Chest': (0, None, 0x5945, 'Chest', 0x07, 'Shadow Temple'),
    'Shadow Temple MQ Falling Spikes Upper Chest': (0, None, 0x5886, 'Chest', 0x07, 'Shadow Temple'),
    'Shadow Temple MQ Invisible Spikes Chest': (0, None, 0x7889, 'Chest', 0x07, 'Shadow Temple'),
    'Shadow Temple MQ Boss Key Chest': (0, None, 0x27EB, 'Chest', 0x07, 'Shadow Temple'),
    'Shadow Temple MQ Spike Walls Left Chest': (0, None, 0x588A, 'Chest', 0x07, 'Shadow Temple'),
    'Shadow Temple MQ Stalfos Room Chest': (0, None, 0x79D0, 'Chest', 0x07, 'Shadow Temple'),
    'Shadow Temple MQ Invisible Blades Invisible Chest': (0, None, 0x6856, 'Chest', 0x07, 'Shadow Temple'),
    'Shadow Temple MQ Invisible Blades Visible Chest': (0, None, 0x588C, 'Chest', 0x07, 'Shadow Temple'),
    'Shadow Temple MQ Bomb Flower Chest': (0, None, 0x794D, 'Chest', 0x07, 'Shadow Temple'),
    'Shadow Temple MQ Wind Hint Chest': (0, None, 0x6855, 'Chest', 0x07, 'Shadow Temple'),
    'Shadow Temple MQ After Wind Hidden Chest': (0, None, 0x6934, 'Chest', 0x07, 'Shadow Temple'),
    'Shadow Temple MQ After Wind Enemy Chest': (0, None, 0x7888, 'Chest', 0x07, 'Shadow Temple'),
    'Shadow Temple MQ Near Ship Invisible Chest': (0, None, 0x684E, 'Chest', 0x07, 'Shadow Temple'),
    'Shadow Temple MQ Freestanding Key': (None, None, 0x06, 'Collectable', 0x07, 'Shadow Temple'), 

    # Bottom of the Well vanilla
    'Bottom of the Well Front Left Hidden Wall': (0x32D317E, None, 0x5848, 'Chest', 0x08, 'Bottom of the Well'),
    'Bottom of the Well Front Center Bombable': (0x32D30FE, None, 0x5062, 'Chest', 0x08, 'Bottom of the Well'),
    'Bottom of the Well Right Bottom Hidden Wall': (0x32D314E, None, 0x5845, 'Chest', 0x08, 'Bottom of the Well'),
    'Bottom of the Well Center Large Chest': (0x32D30EE, None, 0x0801, 'Chest', 0x08, 'Bottom of the Well'),
    'Bottom of the Well Center Small Chest': (0x32D31AE, None, 0x504E, 'Chest', 0x08, 'Bottom of the Well'),
    'Bottom of the Well Back Left Bombable': (0x32D313E, None, 0x5C84, 'Chest', 0x08, 'Bottom of the Well'),
    'Bottom of the Well Defeat Boss': (0x32FB0AA, None, 0x1143, 'Chest', 0x08, 'Bottom of the Well'),
    'Bottom of the Well Invisible Chest': (0x32FB0BA, None, 0x6AD4, 'Chest', 0x08, 'Bottom of the Well'),
    'Bottom of the Well Underwater Front Chest': (0x32D31BE, None, 0x5CD0, 'Chest', 0x08, 'Bottom of the Well'),
    'Bottom of the Well Underwater Left Chest': (0x32D318E, None, 0x5909, 'Chest', 0x08, 'Bottom of the Well'),
    'Bottom of the Well Basement Chest': (0x32E9252, None, 0x0827, 'Chest', 0x08, 'Bottom of the Well'),
    'Bottom of the Well Locked Pits': (0x32F90AA, None, 0x552A, 'Chest', 0x08, 'Bottom of the Well'),
    'Bottom of the Well Behind Right Grate': (0x32D319E, None, 0x554C, 'Chest', 0x08, 'Bottom of the Well'),
    'Bottom of the Well Freestanding Key': (None, None, 0x01, 'Collectable', 0x08, 'Bottom of the Well'),
    # Bottom of the Well MQ
    'Bottom of the Well MQ Map Chest': (0, None, 0x0823, 'Chest', 0x08, 'Bottom of the Well'),
    'Bottom of the Well MQ Lens Chest': (0, None, 0xB141, 'Chest', 0x08, 'Bottom of the Well'),
    'Bottom of the Well MQ Compass Chest': (0, None, 0x1802, 'Chest', 0x08, 'Bottom of the Well'),
    'Bottom of the Well MQ Dead Hand Freestanding Key': (None, None, 0x02, 'Collectable', 0x08, 'Bottom of the Well'), 
    'Bottom of the Well MQ East Inner Room Freestanding Key': (None, None, 0x01, 'Collectable', 0x08, 'Bottom of the Well'),

    # Ice Cavern vanilla
    'Ice Cavern Map Chest': (0x2C4016A, None, 0x0820, 'Chest', 0x09, 'Ice Cavern'),
    'Ice Cavern Compass Chest': (0x2C4E236, None, 0x0801, 'Chest', 0x09, 'Ice Cavern'),
    'Ice Cavern Iron Boots Chest': (0x2C380A2, None, 0x15C2, 'Chest', 0x09, 'Ice Cavern'),
    'Ice Cavern Freestanding PoH': (None, None, 0x01, 'Collectable', 0x09, 'Ice Cavern'),
    # Ice Cavern MQ
    'Ice Cavern MQ Iron Boots Chest': (0, None, 0x15C2, 'Chest', 0x09, 'Ice Cavern'),
    'Ice Cavern MQ Compass Chest': (0, None, 0x0800, 'Chest', 0x09, 'Ice Cavern'),
    'Ice Cavern MQ Map Chest': (0, None, 0xB821, 'Chest', 0x09, 'Ice Cavern'),
    'Ice Cavern MQ Freestanding PoH': (None, None, 0x01, 'Collectable', 0x09, 'Ice Cavern'),

    # Gerudo Training Grounds vanilla
    'Gerudo Training Grounds Lobby Left Chest': (0x28870CA, None, 0x8893, 'Chest', 0x0B, 'Gerudo Training Grounds'),
    'Gerudo Training Grounds Lobby Right Chest': (0x28870BA, None, 0x8947, 'Chest', 0x0B, 'Gerudo Training Grounds'),
    'Gerudo Training Grounds Stalfos Chest': (0x28970AA, None, 0x8840, 'Chest', 0x0B, 'Gerudo Training Grounds'),
    'Gerudo Training Grounds Beamos Chest': (0x28C715E, None, 0x8841, 'Chest', 0x0B, 'Gerudo Training Grounds'),
    'Gerudo Training Grounds Hidden Ceiling Chest': (0x28D010E, None, 0x584B, 'Chest', 0x0B, 'Gerudo Training Grounds'),
    'Gerudo Training Grounds Maze Path First Chest': (0x28D00CE, None, 0x5AA6, 'Chest', 0x0B, 'Gerudo Training Grounds'),
    'Gerudo Training Grounds Maze Path Second Chest': (0x28D00FE, None, 0x59CA, 'Chest', 0x0B, 'Gerudo Training Grounds'),
    'Gerudo Training Grounds Maze Path Third Chest': (0x28D00EE, None, 0x5969, 'Chest', 0x0B, 'Gerudo Training Grounds'),
    'Gerudo Training Grounds Maze Path Final Chest': (0x28D011E, None, 0x0B2C, 'Chest', 0x0B, 'Gerudo Training Grounds'),
    'Gerudo Training Grounds Maze Right Central Chest': (0x28D00BE, None, 0x5D45, 'Chest', 0x0B, 'Gerudo Training Grounds'),
    'Gerudo Training Grounds Maze Right Side Chest': (0x28D00DE, None, 0x5968, 'Chest', 0x0B, 'Gerudo Training Grounds'),
    'Gerudo Training Grounds Underwater Silver Rupee Chest': (0x28D91D6, None, 0x884D, 'Chest', 0x0B, 'Gerudo Training Grounds'),
    'Gerudo Training Grounds Hammer Room Clear Chest': (0x28B91AE, None, 0x7952, 'Chest', 0x0B, 'Gerudo Training Grounds'),
    'Gerudo Training Grounds Hammer Room Switch Chest': (0x28B919E, None, 0x5850, 'Chest', 0x0B, 'Gerudo Training Grounds'),
    'Gerudo Training Grounds Eye Statue Chest': (0x28AE09E, None, 0x8843, 'Chest', 0x0B, 'Gerudo Training Grounds'),
    'Gerudo Training Grounds Near Scarecrow Chest': (0x28D00AE, None, 0x5844, 'Chest', 0x0B, 'Gerudo Training Grounds'),
    'Gerudo Training Grounds Before Heavy Block Chest': (0x28A611E, None, 0x7971, 'Chest', 0x0B, 'Gerudo Training Grounds'),
    'Gerudo Training Grounds Heavy Block First Chest': (0x28DD0BE, None, 0x7ACF, 'Chest', 0x0B, 'Gerudo Training Grounds'),
    'Gerudo Training Grounds Heavy Block Second Chest': (0x28DD0AE, None, 0x788E, 'Chest', 0x0B, 'Gerudo Training Grounds'),
    'Gerudo Training Grounds Heavy Block Third Chest': (0x28DD08E, None, 0x6854, 'Chest', 0x0B, 'Gerudo Training Grounds'),
    'Gerudo Training Grounds Heavy Block Fourth Chest': (0x28DD09E, None, 0x5F82, 'Chest', 0x0B, 'Gerudo Training Grounds'),
    'Gerudo Training Grounds Freestanding Key': (None, None, 0x01, 'Collectable', 0x0B, 'Gerudo Training Grounds'),
    # Gerudo Training Grounds MQ
    'Gerudo Training Grounds MQ Lobby Right Chest': (0, None, 0x5D47, 'Chest', 0x0B, 'Gerudo Training Grounds'),
    'Gerudo Training Grounds MQ Lobby Left Chest': (0, None, 0x5953, 'Chest', 0x0B, 'Gerudo Training Grounds'),
    'Gerudo Training Grounds MQ First Iron Knuckle Chest': (0, None, 0x89A0, 'Chest', 0x0B, 'Gerudo Training Grounds'),
    'Gerudo Training Grounds MQ Before Heavy Block Chest': (0, None, 0x7951, 'Chest', 0x0B, 'Gerudo Training Grounds'),
    'Gerudo Training Grounds MQ Eye Statue Chest': (0, None, 0x8063, 'Chest', 0x0B, 'Gerudo Training Grounds'),
    'Gerudo Training Grounds MQ Flame Circle Chest': (0, None, 0x884E, 'Chest', 0x0B, 'Gerudo Training Grounds'),
    'Gerudo Training Grounds MQ Second Iron Knuckle Chest': (0, None, 0x7952, 'Chest', 0x0B, 'Gerudo Training Grounds'),
    'Gerudo Training Grounds MQ Dinolfos Chest': (0, None, 0x8841, 'Chest', 0x0B, 'Gerudo Training Grounds'),
    'Gerudo Training Grounds MQ Ice Arrows Chest': (0, None, 0xBB24, 'Chest', 0x0B, 'Gerudo Training Grounds'),
    'Gerudo Training Grounds MQ Maze Right Central Chest': (0, None, 0x5885, 'Chest', 0x0B, 'Gerudo Training Grounds'),
    'Gerudo Training Grounds MQ Maze Path First Chest': (0, None, 0x5986, 'Chest', 0x0B, 'Gerudo Training Grounds'),
    'Gerudo Training Grounds MQ Maze Right Side Chest': (0, None, 0x5E48, 'Chest', 0x0B, 'Gerudo Training Grounds'),
    'Gerudo Training Grounds MQ Maze Path Third Chest': (0, None, 0x5E49, 'Chest', 0x0B, 'Gerudo Training Grounds'),
    'Gerudo Training Grounds MQ Maze Path Second Chest': (0, None, 0x59CA, 'Chest', 0x0B, 'Gerudo Training Grounds'),
    'Gerudo Training Grounds MQ Hidden Ceiling Chest': (0, None, 0x5AAB, 'Chest', 0x0B, 'Gerudo Training Grounds'),
    'Gerudo Training Grounds MQ Underwater Silver Rupee Chest': (0, None, 0x884D, 'Chest', 0x0B, 'Gerudo Training Grounds'),
    'Gerudo Training Grounds MQ Heavy Block Chest': (0, None, 0x7AA2, 'Chest', 0x0B, 'Gerudo Training Grounds'),

    # Ganon's Castle shared
    'Ganons Tower Boss Key Chest': (0x2F040EE, None, 0x27EB, 'Chest', 0x0A, 'my tower'),
    # Ganon's Castle vanilla
    'Ganons Castle Forest Trial Chest': (0x31F106E, None, 0x7889, 'Chest', 0x0D, 'my castle'),
    'Ganons Castle Water Trial Left Chest': (0x31D7236, None, 0x5F87, 'Chest', 0x0D, 'my castle'),
    'Ganons Castle Water Trial Right Chest': (0x31D7226, None, 0x5906, 'Chest', 0x0D, 'my castle'),
    'Ganons Castle Shadow Trial First Chest': (0x32350CA, None, 0x5888, 'Chest', 0x0D, 'my castle'),
    'Ganons Castle Shadow Trial Second Chest': (0x32350BA, None, 0x36C5, 'Chest', 0x0D, 'my castle'),
    'Ganons Castle Spirit Trial First Chest': (0x3268132, None, 0x8D72, 'Chest', 0x0D, 'my castle'),
    'Ganons Castle Spirit Trial Second Chest': (0x3268142, None, 0x6954, 'Chest', 0x0D, 'my castle'),
    'Ganons Castle Light Trial First Left Chest': (0x321B11E, None, 0x588C, 'Chest', 0x0D, 'my castle'),
    'Ganons Castle Light Trial Second Left Chest': (0x321B10E, None, 0x5F8B, 'Chest', 0x0D, 'my castle'),
    'Ganons Castle Light Trial Third Left Chest': (0x321B12E, None, 0x590D, 'Chest', 0x0D, 'my castle'),
    'Ganons Castle Light Trial First Right Chest': (0x321B13E, None, 0x5F8E, 'Chest', 0x0D, 'my castle'),
    'Ganons Castle Light Trial Second Right Chest': (0x321B0FE, None, 0x596A, 'Chest', 0x0D, 'my castle'),
    'Ganons Castle Light Trial Third Right Chest': (0x321B14E, None, 0x5F8F, 'Chest', 0x0D, 'my castle'),
    'Ganons Castle Light Trail Invisible Enemies Chest': (0x321B15E, None, 0x7850, 'Chest', 0x0D, 'my castle'),
    'Ganons Castle Light Trial Lullaby Chest': (0x321B17E, None, 0x8851, 'Chest', 0x0D, 'my castle'),
    # Ganon's Castle MQ
    'Ganons Castle MQ Water Trial Chest': (0, None, 0x59C1, 'Chest', 0x0D, 'my castle'),
    'Ganons Castle MQ Forest Trial First Chest': (0, None, 0x8942, 'Chest', 0x0D, 'my castle'),
    'Ganons Castle MQ Forest Trial Second Chest': (0, None, 0x8023, 'Chest', 0x0D, 'my castle'),
    'Ganons Castle MQ Light Trial Lullaby Chest': (0, None, 0x8904, 'Chest', 0x0D, 'my castle'),
    'Ganons Castle MQ Shadow Trial First Chest': (0, None, 0x8940, 'Chest', 0x0D, 'my castle'),
    'Ganons Castle MQ Shadow Trial Second Chest': (0, None, 0x8845, 'Chest', 0x0D, 'my castle'),
    'Ganons Castle MQ Spirit Trial Golden Gauntlets Chest': (0, None, 0xB6C6, 'Chest', 0x0D, 'my castle'),
    'Ganons Castle MQ Spirit Trial Sun Back Right Chest': (0, None, 0x8907, 'Chest', 0x0D, 'my castle'),
    'Ganons Castle MQ Spirit Trial Sun Back Left Chest': (0, None, 0x8848, 'Chest', 0x0D, 'my castle'),
    'Ganons Castle MQ Spirit Trial Sun Front Left Chest': (0, None, 0x8909, 'Chest', 0x0D, 'my castle'),
    'Ganons Castle MQ Spirit Trial First Chest': (0, None, 0x506A, 'Chest', 0x0D, 'my castle'),
    'Ganons Castle MQ Spirit Trial Second Chest': (0, None, 0x6954, 'Chest', 0x0D, 'my castle'),
    'Ganons Castle MQ Forest Trial Freestanding Key': (None, None, 0x01, 'Collectable', 0x0D, 'my castle'), 

    # I don't think the addresses matter for Link's Pocket anymore, but they can't be None for some reason
    'Links Pocket': (0x34806FB, 0x34806FF, None, 'Boss', None, 'Link\'s Pocket'), 
    'Queen Gohma': (0xCA315F, 0x2079571, 0x6C, 'Boss', None, 'Deku Tree'),
    'King Dodongo': (0xCA30DF, 0x2223309, 0x6D, 'Boss', None, 'Dodongo\'s Cavern'),
    'Barinade': (0xCA36EB, 0x2113C19, 0x6E, 'Boss', None, 'Jabu Jabu\'s Belly'),
    'Phantom Ganon': (0xCA3D07, 0xD4ED79, 0x66, 'Boss', None, 'Shadow Temple'),
    'Volvagia': (0xCA3D93, 0xD10135, 0x67, 'Boss', None, 'Fire Temple'),
    'Morpha': (0xCA3E1F, 0xD5A3A9, 0x68, 'Boss', None, 'Water Temple'),
    'Twinrova': (0xCA3EB3, 0xD39FF1, 0x69, 'Boss', None, 'Spirit Temple'),
    'Bongo Bongo': (0xCA3F43, 0xD13E19, 0x6A, 'Boss', None, 'Shadow Temple'),
    'Ganon': (None, None, None, 'Boss', None, 'Ganon\'s Castle'),
    # note that the scene for skulltulas is not the actual scene the token appears in
    # rather, it is the index of the grouping used when storing skulltula collection
    # for example, zora river, zora's domain, and zora fountain are all a single 'scene' for skulltulas
    'GS Deku Tree Basement Back Room': (None, None, 0x01, 'GS Token', 0x00, 'Deku Tree'),
    'GS Deku Tree Basement Gate': (None, None, 0x02, 'GS Token', 0x00, 'Deku Tree'),
    'GS Deku Tree Basement Vines': (None, None, 0x04, 'GS Token', 0x00, 'Deku Tree'),
    'GS Deku Tree Compass Room': (None, None, 0x08, 'GS Token', 0x00, 'Deku Tree'),

    'GS Deku Tree MQ Lobby': (None, None, 0x02, 'GS Token', 0x00, 'Deku Tree'),
    'GS Deku Tree MQ Compass Room': (None, None, 0x08, 'GS Token', 0x00, 'Deku Tree'),
    'GS Deku Tree MQ Basement Ceiling': (None, None, 0x04, 'GS Token', 0x00, 'Deku Tree'),
    'GS Deku Tree MQ Basement Back Room': (None, None, 0x01, 'GS Token', 0x00, 'Deku Tree'),

    'GS Dodongo\'s Cavern Vines Above Stairs': (None, None, 0x01, 'GS Token', 0x01, 'Dodongo\'s Cavern'),
    'GS Dodongo\'s Cavern Scarecrow': (None, None, 0x02, 'GS Token', 0x01, 'Dodongo\'s Cavern'),
    'GS Dodongo\'s Cavern Alcove Above Stairs': (None, None, 0x04, 'GS Token', 0x01, 'Dodongo\'s Cavern'),
    'GS Dodongo\'s Cavern Back Room': (None, None, 0x08, 'GS Token', 0x01, 'Dodongo\'s Cavern'),
    'GS Dodongo\'s Cavern East Side Room': (None, None, 0x10, 'GS Token', 0x01, 'Dodongo\'s Cavern'),

    'GS Dodongo\'s Cavern MQ Scrub Room': (None, None, 0x02, 'GS Token', 0x01, 'Dodongo\'s Cavern'),
    'GS Dodongo\'s Cavern MQ Song of Time Block Room': (None, None, 0x08, 'GS Token', 0x01, 'Dodongo\'s Cavern'),
    'GS Dodongo\'s Cavern MQ Lizalfos Room': (None, None, 0x04, 'GS Token', 0x01, 'Dodongo\'s Cavern'),
    'GS Dodongo\'s Cavern MQ Larva Room': (None, None, 0x10, 'GS Token', 0x01, 'Dodongo\'s Cavern'),
    'GS Dodongo\'s Cavern MQ Back Area': (None, None, 0x01, 'GS Token', 0x01, 'Dodongo\'s Cavern'),

    'GS Jabu Jabu Lobby Basement Lower': (None, None, 0x01, 'GS Token', 0x02, 'Jabu Jabu\'s Belly'),
    'GS Jabu Jabu Lobby Basement Upper': (None, None, 0x02, 'GS Token', 0x02, 'Jabu Jabu\'s Belly'),
    'GS Jabu Jabu Near Boss': (None, None, 0x04, 'GS Token', 0x02, 'Jabu Jabu\'s Belly'),
    'GS Jabu Jabu Water Switch Room': (None, None, 0x08, 'GS Token', 0x02, 'Jabu Jabu\'s Belly'),

    'GS Jabu Jabu MQ Tailpasaran Room': (None, None, 0x04, 'GS Token', 0x02, 'Jabu Jabu\'s Belly'),
    'GS Jabu Jabu MQ Invisible Enemies Room': (None, None, 0x08, 'GS Token', 0x02, 'Jabu Jabu\'s Belly'),
    'GS Jabu Jabu MQ Boomerang Room': (None, None, 0x01, 'GS Token', 0x02, 'Jabu Jabu\'s Belly'),
    'GS Jabu Jabu MQ Near Boss': (None, None, 0x02, 'GS Token', 0x02, 'Jabu Jabu\'s Belly'),

    'GS Forest Temple Outdoor East': (None, None, 0x01, 'GS Token', 0x03, 'Forest Temple'),
    'GS Forest Temple First Room': (None, None, 0x02, 'GS Token', 0x03, 'Forest Temple'),
    'GS Forest Temple Outdoor West': (None, None, 0x04, 'GS Token', 0x03, 'Forest Temple'),
    'GS Forest Temple Lobby': (None, None, 0x08, 'GS Token', 0x03, 'Forest Temple'),
    'GS Forest Temple Basement': (None, None, 0x10, 'GS Token', 0x03, 'Forest Temple'),

    'GS Forest Temple MQ First Hallway': (None, None, 0x02, 'GS Token', 0x03, 'Forest Temple'),
    'GS Forest Temple MQ Block Push Room': (None, None, 0x10, 'GS Token', 0x03, 'Forest Temple'),
    'GS Forest Temple MQ Outdoor East': (None, None, 0x01, 'GS Token', 0x03, 'Forest Temple'),
    'GS Forest Temple MQ Outdoor West': (None, None, 0x04, 'GS Token', 0x03, 'Forest Temple'),
    'GS Forest Temple MQ Well': (None, None, 0x08, 'GS Token', 0x03, 'Forest Temple'),

    'GS Fire Temple Song of Time Room': (None, None, 0x01, 'GS Token', 0x04, 'Fire Temple'),
    'GS Fire Temple Basement': (None, None, 0x02, 'GS Token', 0x04, 'Fire Temple'),
    'GS Fire Temple Unmarked Bomb Wall': (None, None, 0x04, 'GS Token', 0x04, 'Fire Temple'),
    'GS Fire Temple East Tower Top': (None, None, 0x08, 'GS Token', 0x04, 'Fire Temple'),
    'GS Fire Temple East Tower Climb': (None, None, 0x10, 'GS Token', 0x04, 'Fire Temple'),

    'GS Fire Temple MQ Above Fire Wall Maze': (None, None, 0x02, 'GS Token', 0x04, 'Fire Temple'),
    'GS Fire Temple MQ Fire Wall Maze Center': (None, None, 0x08, 'GS Token', 0x04, 'Fire Temple'),
    'GS Fire Temple MQ Big Lava Room': (None, None, 0x01, 'GS Token', 0x04, 'Fire Temple'),
    'GS Fire Temple MQ Fire Wall Maze Side Room': (None, None, 0x10, 'GS Token', 0x04, 'Fire Temple'),
    'GS Fire Temple MQ East Tower Top': (None, None, 0x04, 'GS Token', 0x04, 'Fire Temple'),

    'GS Water Temple South Basement': (None, None, 0x01, 'GS Token', 0x05, 'Water Temple'),
    'GS Water Temple Falling Platform Room': (None, None, 0x02, 'GS Token', 0x05, 'Water Temple'),
    'GS Water Temple Central Room': (None, None, 0x04, 'GS Token', 0x05, 'Water Temple'),
    'GS Water Temple Near Boss Key Chest': (None, None, 0x08, 'GS Token', 0x05, 'Water Temple'),
    'GS Water Temple Serpent River': (None, None, 0x10, 'GS Token', 0x05, 'Water Temple'),

    'GS Water Temple MQ Before Upper Water Switch': (None, None, 0x04, 'GS Token', 0x05, 'Water Temple'),
    'GS Water Temple MQ North Basement': (None, None, 0x08, 'GS Token', 0x05, 'Water Temple'),
    'GS Water Temple MQ Lizalfos Hallway': (None, None, 0x01, 'GS Token', 0x05, 'Water Temple'),
    'GS Water Temple MQ Serpent River': (None, None, 0x02, 'GS Token', 0x05, 'Water Temple'),
    'GS Water Temple MQ South Basement': (None, None, 0x10, 'GS Token', 0x05, 'Water Temple'),

    'GS Spirit Temple Hall to West Iron Knuckle': (None, None, 0x01, 'GS Token', 0x06, 'Spirit Temple'),
    'GS Spirit Temple Boulder Room': (None, None, 0x02, 'GS Token', 0x06, 'Spirit Temple'),
    'GS Spirit Temple Lobby': (None, None, 0x04, 'GS Token', 0x06, 'Spirit Temple'),
    'GS Spirit Temple Bomb for Light Room': (None, None, 0x08, 'GS Token', 0x06, 'Spirit Temple'),
    'GS Spirit Temple Metal Fence': (None, None, 0x10, 'GS Token', 0x06, 'Spirit Temple'),

    'GS Spirit Temple MQ Lower Adult Right': (None, None, 0x08, 'GS Token', 0x06, 'Spirit Temple'),
    'GS Spirit Temple MQ Lower Adult Left': (None, None, 0x02, 'GS Token', 0x06, 'Spirit Temple'),
    'GS Spirit Temple MQ Iron Knuckle West': (None, None, 0x04, 'GS Token', 0x06, 'Spirit Temple'),
    'GS Spirit Temple MQ Iron Knuckle North': (None, None, 0x10, 'GS Token', 0x06, 'Spirit Temple'),
    'GS Spirit Temple MQ Sun Block Room': (None, None, 0x01, 'GS Token', 0x06, 'Spirit Temple'),

    'GS Shadow Temple Single Giant Pot': (None, None, 0x01, 'GS Token', 0x07, 'Shadow Temple'),
    'GS Shadow Temple Crusher Room': (None, None, 0x02, 'GS Token', 0x07, 'Shadow Temple'),
    'GS Shadow Temple Tripple Giant Pot': (None, None, 0x04, 'GS Token', 0x07, 'Shadow Temple'),
    'GS Shadow Temple Like Like Room': (None, None, 0x08, 'GS Token', 0x07, 'Shadow Temple'),
    'GS Shadow Temple Near Ship': (None, None, 0x10, 'GS Token', 0x07, 'Shadow Temple'),

    'GS Shadow Temple MQ Crusher Room': (None, None, 0x02, 'GS Token', 0x07, 'Shadow Temple'),
    'GS Shadow Temple MQ Wind Hint Room': (None, None, 0x01, 'GS Token', 0x07, 'Shadow Temple'),
    'GS Shadow Temple MQ After Wind': (None, None, 0x08, 'GS Token', 0x07, 'Shadow Temple'),
    'GS Shadow Temple MQ After Ship': (None, None, 0x10, 'GS Token', 0x07, 'Shadow Temple'),
    'GS Shadow Temple MQ Near Boss': (None, None, 0x04, 'GS Token', 0x07, 'Shadow Temple'),

    'GS Well Like Like Cage': (None, None, 0x01, 'GS Token', 0x08, 'Bottom of the Well'),
    'GS Well East Inner Room': (None, None, 0x02, 'GS Token', 0x08, 'Bottom of the Well'),
    'GS Well West Inner Room': (None, None, 0x04, 'GS Token', 0x08, 'Bottom of the Well'),

    'GS Well MQ Basement': (None, None, 0x01, 'GS Token', 0x08, 'Bottom of the Well'),
    'GS Well MQ Coffin Room': (None, None, 0x04, 'GS Token', 0x08, 'Bottom of the Well'),
    'GS Well MQ West Inner Room': (None, None, 0x02, 'GS Token', 0x08, 'Bottom of the Well'),

    'GS Ice Cavern Push Block Room': (None, None, 0x01, 'GS Token', 0x09, 'Ice Cavern'),
    'GS Ice Cavern Spinning Scythe Room': (None, None, 0x02, 'GS Token', 0x09, 'Ice Cavern'),
    'GS Ice Cavern Heart Piece Room': (None, None, 0x04, 'GS Token', 0x09, 'Ice Cavern'),

    'GS Ice Cavern MQ Scarecrow': (None, None, 0x01, 'GS Token', 0x09, 'Ice Cavern'),
    'GS Ice Cavern MQ Ice Block': (None, None, 0x04, 'GS Token', 0x09, 'Ice Cavern'),
    'GS Ice Cavern MQ Red Ice': (None, None, 0x02, 'GS Token', 0x09, 'Ice Cavern'),

    'GS Hyrule Field Near Gerudo Valley': (None, None, 0x01, 'GS Token', 0x0A, 'Hyrule Field'),
    'GS Hyrule Field near Kakariko': (None, None, 0x02, 'GS Token', 0x0A, 'Hyrule Field'),

    'GS Lon Lon Ranch Back Wall': (None, None, 0x01, 'GS Token', 0x0B, 'Lon Lon Ranch'),
    'GS Lon Lon Ranch Rain Shed': (None, None, 0x02, 'GS Token', 0x0B, 'Lon Lon Ranch'),
    'GS Lon Lon Ranch House Window': (None, None, 0x04, 'GS Token', 0x0B, 'Lon Lon Ranch'),
    'GS Lon Lon Ranch Tree': (None, None, 0x08, 'GS Token', 0x0B, 'Lon Lon Ranch'),

    'GS Kokiri Bean Patch': (None, None, 0x01, 'GS Token', 0x0C, 'Kokiri Forest'),
    'GS Kokiri Know It All House': (None, None, 0x02, 'GS Token', 0x0C, 'Kokiri Forest'),
    'GS Kokiri House of Twins': (None, None, 0x04, 'GS Token', 0x0C, 'Kokiri Forest'),

    'GS Lost Woods Bean Patch Near Bridge': (None, None, 0x01, 'GS Token', 0x0D, 'the Lost Woods'),
    'GS Lost Woods Bean Patch Near Stage': (None, None, 0x02, 'GS Token', 0x0D, 'the Lost Woods'),
    'GS Lost Woods Above Stage': (None, None, 0x04, 'GS Token', 0x0D, 'the Lost Woods'),
    'GS Sacred Forest Meadow': (None, None, 0x08, 'GS Token', 0x0D, 'Sacred Forest Meadow'),

    'GS Outside Ganon\'s Castle': (None, None, 0x01, 'GS Token', 0x0E, 'outside Ganon\'s Castle'),
    'GS Hyrule Castle Grotto': (None, None, 0x02, 'GS Token', 0x0E, 'Hyrule Castle'),
    'GS Hyrule Castle Tree': (None, None, 0x04, 'GS Token', 0x0E, 'Hyrule Castle'),
    'GS Castle Market Guard House': (None, None, 0x08, 'GS Token', 0x0E, 'the Market'),

    'GS Mountain Crater Bean Patch': (None, None, 0x01, 'GS Token', 0x0F, 'Death Mountain Crater'),
    'GS Mountain Trail Bean Patch': (None, None, 0x02, 'GS Token', 0x0F, 'Death Mountain Trail'),
    'GS Mountain Trail Bomb Alcove': (None, None, 0x04, 'GS Token', 0x0F, 'Death Mountain Trail'),
    'GS Mountain Trail Above Dodongo\'s Cavern': (None, None, 0x08, 'GS Token', 0x0F, 'Death Mountain Trail'),
    'GS Mountain Trail Path to Crater': (None, None, 0x10, 'GS Token', 0x0F, 'Death Mountain Trail'),
    'GS Goron City Center Platform': (None, None, 0x20, 'GS Token', 0x0F, 'Goron City'),
    'GS Goron City Boulder Maze': (None, None, 0x40, 'GS Token', 0x0F, 'Goron City'),
    'GS Death Mountain Crater Crate': (None, None, 0x80, 'GS Token', 0x0F, 'Death Mountain Crater'),

    'GS Kakariko House Under Construction': (None, None, 0x08, 'GS Token', 0x10, 'Kakariko Village'),
    'GS Kakariko Skulltula House': (None, None, 0x10, 'GS Token', 0x10, 'Kakariko Village'),
    'GS Kakariko Guard\'s House': (None, None, 0x02, 'GS Token', 0x10, 'Kakariko Village'),
    'GS Kakariko Tree': (None, None, 0x20, 'GS Token', 0x10, 'Kakariko Village'),
    'GS Kakariko Watchtower': (None, None, 0x04, 'GS Token', 0x10, 'Kakariko Village'),
    'GS Kakariko Above Impa\'s House': (None, None, 0x40, 'GS Token', 0x10, 'Kakariko Village'),
    'GS Graveyard Wall': (None, None, 0x80, 'GS Token', 0x10, 'the Graveyard'),
    'GS Graveyard Bean Patch': (None, None, 0x01, 'GS Token', 0x10, 'the Graveyard'),

    'GS Zora River Ladder': (None, None, 0x01, 'GS Token', 0x11, 'Zora River'),
    'GS Zora River Tree': (None, None, 0x02, 'GS Token', 0x11, 'Zora River'),
    'GS Zora\'s Fountain Above the Log': (None, None, 0x04, 'GS Token', 0x11, 'Zora\'s Fountain'),
    'GS Zora River Above Bridge': (None, None, 0x08, 'GS Token', 0x11, 'Zora River'),
    'GS Zora River Near Raised Grottos': (None, None, 0x10, 'GS Token', 0x11, 'Zora River'),
    'GS Zora\'s Fountain Hidden Cave': (None, None, 0x20, 'GS Token', 0x11, 'Zora\'s Fountain'),
    'GS Zora\'s Domain Frozen Waterfall': (None, None, 0x40, 'GS Token', 0x11, 'Zora\'s Domain'),
    'GS Zora\'s Fountain Tree': (None, None, 0x80, 'GS Token', 0x11, 'Zora\'s Fountain'),

    'GS Lake Hylia Bean Patch': (None, None, 0x01, 'GS Token', 0x12, 'Lake Hylia'),
    'GS Lake Hylia Small Island': (None, None, 0x02, 'GS Token', 0x12, 'Lake Hylia'),
    'GS Lake Hylia Lab Wall': (None, None, 0x04, 'GS Token', 0x12, 'Lake Hylia'),
    'GS Lab Underwater Crate': (None, None, 0x08, 'GS Token', 0x12, 'Lake Hylia'),
    'GS Lake Hylia Giant Tree': (None, None, 0x10, 'GS Token', 0x12, 'Lake Hylia'),

    'GS Gerudo Valley Bean Patch': (None, None, 0x01, 'GS Token', 0x13, 'Gerudo Valley'),
    'GS Gerudo Valley Small Bridge': (None, None, 0x02, 'GS Token', 0x13, 'Gerudo Valley'),
    'GS Gerudo Valley Pillar': (None, None, 0x04, 'GS Token', 0x13, 'Gerudo Valley'),
    'GS Gerudo Valley Behind Tent': (None, None, 0x08, 'GS Token', 0x13, 'Gerudo Valley'),

    'GS Gerudo Fortress Archery Range': (None, None, 0x01, 'GS Token', 0x14, 'Gerudo Fortress'),
    'GS Gerudo Fortress Top Floor': (None, None, 0x02, 'GS Token', 0x14, 'Gerudo Fortress'),
    'GS Desert Colossus Bean Patch': (None, None, 0x01, 'GS Token', 0x15, 'Desert Colossus'),
    'GS Wasteland Ruins': (None, None, 0x02, 'GS Token', 0x15, 'Haunted Wasteland'),
    'GS Desert Colossus Hill': (None, None, 0x04, 'GS Token', 0x15, 'Desert Colossus'),
    'GS Desert Colossus Tree': (None, None, 0x08, 'GS Token', 0x15, 'Desert Colossus'),

    'Kokiri Shop Item 1': (shop_address(0, 0), None, 0x30, 'Shop', 0x2D, 'Kokiri Forest'),
    'Kokiri Shop Item 2': (shop_address(0, 1), None, 0x31, 'Shop', 0x2D, 'Kokiri Forest'),
    'Kokiri Shop Item 3': (shop_address(0, 2), None, 0x32, 'Shop', 0x2D, 'Kokiri Forest'),
    'Kokiri Shop Item 4': (shop_address(0, 3), None, 0x33, 'Shop', 0x2D, 'Kokiri Forest'),
    'Kokiri Shop Item 5': (shop_address(0, 4), None, 0x34, 'Shop', 0x2D, 'Kokiri Forest'),
    'Kokiri Shop Item 6': (shop_address(0, 5), None, 0x35, 'Shop', 0x2D, 'Kokiri Forest'),
    'Kokiri Shop Item 7': (shop_address(0, 6), None, 0x36, 'Shop', 0x2D, 'Kokiri Forest'),
    'Kokiri Shop Item 8': (shop_address(0, 7), None, 0x37, 'Shop', 0x2D, 'Kokiri Forest'),
    'Kakariko Potion Shop Item 1': (shop_address(1, 0), None, 0x30, 'Shop', 0x30, 'Kakariko Village'),
    'Kakariko Potion Shop Item 2': (shop_address(1, 1), None, 0x31, 'Shop', 0x30, 'Kakariko Village'),
    'Kakariko Potion Shop Item 3': (shop_address(1, 2), None, 0x32, 'Shop', 0x30, 'Kakariko Village'),
    'Kakariko Potion Shop Item 4': (shop_address(1, 3), None, 0x33, 'Shop', 0x30, 'Kakariko Village'),
    'Kakariko Potion Shop Item 5': (shop_address(1, 4), None, 0x34, 'Shop', 0x30, 'Kakariko Village'),
    'Kakariko Potion Shop Item 6': (shop_address(1, 5), None, 0x35, 'Shop', 0x30, 'Kakariko Village'),
    'Kakariko Potion Shop Item 7': (shop_address(1, 6), None, 0x36, 'Shop', 0x30, 'Kakariko Village'),
    'Kakariko Potion Shop Item 8': (shop_address(1, 7), None, 0x37, 'Shop', 0x30, 'Kakariko Village'),
    'Bombchu Shop Item 1': (shop_address(2, 0), None, 0x30, 'Shop', 0x32, 'the Market'),
    'Bombchu Shop Item 2': (shop_address(2, 1), None, 0x31, 'Shop', 0x32, 'the Market'),
    'Bombchu Shop Item 3': (shop_address(2, 2), None, 0x32, 'Shop', 0x32, 'the Market'),
    'Bombchu Shop Item 4': (shop_address(2, 3), None, 0x33, 'Shop', 0x32, 'the Market'),
    'Bombchu Shop Item 5': (shop_address(2, 4), None, 0x34, 'Shop', 0x32, 'the Market'),
    'Bombchu Shop Item 6': (shop_address(2, 5), None, 0x35, 'Shop', 0x32, 'the Market'),
    'Bombchu Shop Item 7': (shop_address(2, 6), None, 0x36, 'Shop', 0x32, 'the Market'),
    'Bombchu Shop Item 8': (shop_address(2, 7), None, 0x37, 'Shop', 0x32, 'the Market'),
    'Castle Town Potion Shop Item 1': (shop_address(3, 0), None, 0x30, 'Shop', 0x31, 'the Market'),
    'Castle Town Potion Shop Item 2': (shop_address(3, 1), None, 0x31, 'Shop', 0x31, 'the Market'),
    'Castle Town Potion Shop Item 3': (shop_address(3, 2), None, 0x32, 'Shop', 0x31, 'the Market'),
    'Castle Town Potion Shop Item 4': (shop_address(3, 3), None, 0x33, 'Shop', 0x31, 'the Market'),
    'Castle Town Potion Shop Item 5': (shop_address(3, 4), None, 0x34, 'Shop', 0x31, 'the Market'),
    'Castle Town Potion Shop Item 6': (shop_address(3, 5), None, 0x35, 'Shop', 0x31, 'the Market'),
    'Castle Town Potion Shop Item 7': (shop_address(3, 6), None, 0x36, 'Shop', 0x31, 'the Market'),
    'Castle Town Potion Shop Item 8': (shop_address(3, 7), None, 0x37, 'Shop', 0x31, 'the Market'),
    'Castle Town Bazaar Item 1': (shop_address(4, 0), None, 0x30, 'Shop', 0x2C, 'the Market'),
    'Castle Town Bazaar Item 2': (shop_address(4, 1), None, 0x31, 'Shop', 0x2C, 'the Market'),
    'Castle Town Bazaar Item 3': (shop_address(4, 2), None, 0x32, 'Shop', 0x2C, 'the Market'),
    'Castle Town Bazaar Item 4': (shop_address(4, 3), None, 0x33, 'Shop', 0x2C, 'the Market'),
    'Castle Town Bazaar Item 5': (shop_address(4, 4), None, 0x34, 'Shop', 0x2C, 'the Market'),
    'Castle Town Bazaar Item 6': (shop_address(4, 5), None, 0x35, 'Shop', 0x2C, 'the Market'),
    'Castle Town Bazaar Item 7': (shop_address(4, 6), None, 0x36, 'Shop', 0x2C, 'the Market'),
    'Castle Town Bazaar Item 8': (shop_address(4, 7), None, 0x37, 'Shop', 0x2C, 'the Market'),
    'Kakariko Bazaar Item 1': (shop_address(5, 0), None, 0x38, 'Shop', 0x2C, 'Kakariko Village'),
    'Kakariko Bazaar Item 2': (shop_address(5, 1), None, 0x39, 'Shop', 0x2C, 'Kakariko Village'),
    'Kakariko Bazaar Item 3': (shop_address(5, 2), None, 0x3A, 'Shop', 0x2C, 'Kakariko Village'),
    'Kakariko Bazaar Item 4': (shop_address(5, 3), None, 0x3B, 'Shop', 0x2C, 'Kakariko Village'),
    'Kakariko Bazaar Item 5': (shop_address(5, 4), None, 0x3D, 'Shop', 0x2C, 'Kakariko Village'),
    'Kakariko Bazaar Item 6': (shop_address(5, 5), None, 0x3E, 'Shop', 0x2C, 'Kakariko Village'),
    'Kakariko Bazaar Item 7': (shop_address(5, 6), None, 0x3F, 'Shop', 0x2C, 'Kakariko Village'),
    'Kakariko Bazaar Item 8': (shop_address(5, 7), None, 0x40, 'Shop', 0x2C, 'Kakariko Village'),
    'Zora Shop Item 1': (shop_address(7, 0), None, 0x30, 'Shop', 0x2F, 'Zora\'s Domain'),
    'Zora Shop Item 2': (shop_address(7, 1), None, 0x31, 'Shop', 0x2F, 'Zora\'s Domain'),
    'Zora Shop Item 3': (shop_address(7, 2), None, 0x32, 'Shop', 0x2F, 'Zora\'s Domain'),
    'Zora Shop Item 4': (shop_address(7, 3), None, 0x33, 'Shop', 0x2F, 'Zora\'s Domain'),
    'Zora Shop Item 5': (shop_address(7, 4), None, 0x34, 'Shop', 0x2F, 'Zora\'s Domain'),
    'Zora Shop Item 6': (shop_address(7, 5), None, 0x35, 'Shop', 0x2F, 'Zora\'s Domain'),
    'Zora Shop Item 7': (shop_address(7, 6), None, 0x36, 'Shop', 0x2F, 'Zora\'s Domain'),
    'Zora Shop Item 8': (shop_address(7, 7), None, 0x37, 'Shop', 0x2F, 'Zora\'s Domain'),
    'Goron Shop Item 1': (shop_address(8, 0), None, 0x30, 'Shop', 0x2E, 'Goron City'),
    'Goron Shop Item 2': (shop_address(8, 1), None, 0x31, 'Shop', 0x2E, 'Goron City'),
    'Goron Shop Item 3': (shop_address(8, 2), None, 0x32, 'Shop', 0x2E, 'Goron City'),
    'Goron Shop Item 4': (shop_address(8, 3), None, 0x33, 'Shop', 0x2E, 'Goron City'),
    'Goron Shop Item 5': (shop_address(8, 4), None, 0x34, 'Shop', 0x2E, 'Goron City'),
    'Goron Shop Item 6': (shop_address(8, 5), None, 0x35, 'Shop', 0x2E, 'Goron City'),
    'Goron Shop Item 7': (shop_address(8, 6), None, 0x36, 'Shop', 0x2E, 'Goron City'),
    'Goron Shop Item 8': (shop_address(8, 7), None, 0x37, 'Shop', 0x2E, 'Goron City'),

    'DC Deku Scrub Deku Nuts': (None, None, 0x30, 'NPC', 0x01, 'Dodongo\'s Cavern'), 
    'DC Deku Scrub Deku Sticks': (None, None, 0x31, 'NPC', 0x01, 'Dodongo\'s Cavern'), 
    'DC Deku Scrub Deku Seeds': (None, None, 0x33, 'NPC', 0x01, 'Dodongo\'s Cavern'), 
    'DC Deku Scrub Deku Shield': (None, None, 0x34, 'NPC', 0x01, 'Dodongo\'s Cavern'), 
    'Jabu Deku Scrub Deku Nuts': (None, None, 0x30, 'NPC', 0x02, 'Jabu Jabu\'s Belly'), 
    'GC Deku Scrub Bombs': (None, None, 0x37, 'NPC', 0x0D, 'Ganon\'s Castle'), 
    'GC Deku Scrub Arrows': (None, None, 0x33, 'NPC', 0x0D, 'Ganon\'s Castle'), 
    'GC Deku Scrub Red Potion': (None, None, 0x39, 'NPC', 0x0D, 'Ganon\'s Castle'), 
    'GC Deku Scrub Green Potion': (None, None, 0x3A, 'NPC', 0x0D, 'Ganon\'s Castle'), 

    'DT MQ Deku Scrub Deku Shield': (None, None, 0x34, 'NPC', 0x00, 'Deku Tree'), 
    'DC MQ Deku Scrub Deku Sticks': (None, None, 0x31, 'NPC', 0x01, 'Dodongo\'s Cavern'), 
    'DC MQ Deku Scrub Deku Seeds': (None, None, 0x33, 'NPC', 0x01, 'Dodongo\'s Cavern'), 
    'DC MQ Deku Scrub Deku Shield': (None, None, 0x34, 'NPC', 0x01, 'Dodongo\'s Cavern'), 
    'DC MQ Deku Scrub Red Potion': (None, None, 0x39, 'NPC', 0x01, 'Dodongo\'s Cavern'), 
    'GC MQ Deku Scrub Deku Nuts': (None, None, 0x30, 'NPC', 0x0D, 'Ganon\'s Castle'), 
    'GC MQ Deku Scrub Bombs': (None, None, 0x37, 'NPC', 0x0D, 'Ganon\'s Castle'), 
    'GC MQ Deku Scrub Arrows': (None, None, 0x33, 'NPC', 0x0D, 'Ganon\'s Castle'), 
    'GC MQ Deku Scrub Red Potion': (None, None, 0x39, 'NPC', 0x0D, 'Ganon\'s Castle'), 
    'GC MQ Deku Scrub Green Potion': (None, None, 0x3A, 'NPC', 0x0D, 'Ganon\'s Castle'), 

    'HF Grotto Deku Scrub Piece of Heart': (None, None, 0x3E, 'GrottoNPC', 0x01, 'Hyrule Field'), 
    'ZR Grotto Deku Scrub Red Potion': (None, None, 0x39, 'GrottoNPC', 0x02, 'Zora\'s River'), 
    'ZR Grotto Deku Scrub Green Potion': (None, None, 0x3A, 'GrottoNPC', 0x02, 'Zora\'s River'),
    'SFM Grotto Deku Scrub Red Potion': (None, None, 0x39, 'GrottoNPC', 0x03, 'Sacred Forest Meadow'), 
    'SFM Grotto Deku Scrub Green Potion': (None, None, 0x3A, 'GrottoNPC', 0x03, 'Sacred Forest Meadow'),
    'LH Grotto Deku Scrub Deku Nuts': (None, None, 0x30, 'GrottoNPC', 0x04, 'Lake Hylia'), 
    'LH Grotto Deku Scrub Bombs': (None, None, 0x37, 'GrottoNPC', 0x04, 'Lake Hylia'), 
    'LH Grotto Deku Scrub Arrows': (None, None, 0x33, 'GrottoNPC', 0x04, 'Lake Hylia'), 
    'Valley Grotto Deku Scrub Red Potion': (None, None, 0x39, 'GrottoNPC', 0x05, 'Gerudo Valley'), 
    'Valley Grotto Deku Scrub Green Potion': (None, None, 0x3A, 'GrottoNPC', 0x05, 'Gerudo Valley'),
    'LW Deku Scrub Deku Nuts': (None, None, 0x30, 'NPC', 0x5B, 'Lost Woods'), 
    'LW Deku Scrub Deku Sticks': (None, None, 0x31, 'NPC', 0x5B, 'Lost Woods'), 
    'LW Deku Scrub Deku Stick Upgrade': (None, None, 0x77, 'NPC', 0x5B, 'Lost Woods'), 
    'LW Grotto Deku Scrub Arrows': (None, None, 0x33, 'GrottoNPC', 0x06, 'Lost Woods'), 
    'LW Grotto Deku Scrub Deku Nut Upgrade': (None, None, 0x79, 'GrottoNPC', 0x06, 'Lost Woods'), 
    'Desert Grotto Deku Scrub Red Potion': (None, None, 0x39, 'GrottoNPC', 0x07, 'Desert Colossus'), 
    'Desert Grotto Deku Scrub Green Potion': (None, None, 0x3A, 'GrottoNPC', 0x07, 'Desert Colossus'), 
    'DMC Deku Scrub Bombs': (None, None, 0x37, 'NPC', 0x61, 'Death Mountain Crater'), 
    'DMC Grotto Deku Scrub Deku Nuts': (None, None, 0x30, 'GrottoNPC', 0x08, 'Death Mountain Crater'), 
    'DMC Grotto Deku Scrub Bombs': (None, None, 0x37, 'GrottoNPC', 0x08, 'Death Mountain Crater'), 
    'DMC Grotto Deku Scrub Arrows': (None, None, 0x33, 'GrottoNPC', 0x08, 'Death Mountain Crater'),
    'Goron Grotto Deku Scrub Deku Nuts': (None, None, 0x30, 'GrottoNPC', 0x09, 'Goron City'), 
    'Goron Grotto Deku Scrub Bombs': (None, None, 0x37, 'GrottoNPC', 0x09, 'Goron City'), 
    'Goron Grotto Deku Scrub Arrows': (None, None, 0x33, 'GrottoNPC', 0x09, 'Goron City'), 
    'LLR Grotto Deku Scrub Deku Nuts': (None, None, 0x30, 'GrottoNPC', 0x0A, 'Lon Lon Ranch'), 
    'LLR Grotto Deku Scrub Bombs': (None, None, 0x37, 'GrottoNPC', 0x0A, 'Lon Lon Ranch'), 
    'LLR Grotto Deku Scrub Arrows': (None, None, 0x33, 'GrottoNPC', 0x0A, 'Lon Lon Ranch'), 
}
