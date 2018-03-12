import collections
from BaseClasses import Region, Location, Entrance, RegionType


def create_regions(world):

    world.regions = [
        create_ow_region('Kokiri Forest', ['Kokiri Sword Chest'], ['Links House', 'Mido House', 'Saria House', 'House of Twins', 'Know It All House', 'Kokiri Shop', 'Deku Tree', 'Lost Woods', 'Lost Woods Bridge']),
        create_interior_region('Links House', None, ['Links House Exit']),
        create_interior_region('Mido House', ['Mido Chest Top Left', 'Mido Chest Top Right', 'Mido Chest Bottom Left', 'Mido Chest Bottom Right'], ['Mido House Exit']),
        create_interior_region('Saria House', None, ['Saria House Exit']),
        create_interior_region('House of Twins', None, ['House of Twins Exit']),
        create_interior_region('Know It All House', None, ['Know It All House Exit']),
        create_interior_region('Kokiri Shop', None, ['Kokiri Shop Exit']),
        create_dungeon_region('Deku Tree Lobby', ['Deku Tree Lobby Chest', 'Deku Tree Compass Chest', 'Deku Tree Compass Room Side Chest', 'Deku Tree Basement Chest'], ['Deku Tree Exit', 'Deku Tree Slingshot Passage', 'Deku Tree Basement Path']),
        create_dungeon_region('Deku Tree Slingshot Room', ['Deku Tree Slingshot Chest', 'Deku Tree Slingshot Room Side Chest'], ['Deku Tree Slingshot Exit']),
        create_dungeon_region('Deku Tree Boss Room', ['Queen Gohma'], ['Deku Tree Basement Vines']),        
        create_ow_region('Lost Woods', None, ['Lost Woods Front', 'Meadow Entrance', 'Woods to Goron City', 'Lost Woods Dive Warp', 'Forest Generic Grotto', 'Deku Theater', 'Forest Sales Grotto']),
		create_ow_region('Sacred Forest Meadow Entryway', None, ['Meadow Exit', 'Meadow Gate', 'Front of Meadow Grotto']),
		create_ow_region('Sacred Forest Meadow', ['Song from Saria'], ['Meadow Gate Exit', 'Meadow Fairy Grotto']),
		create_ow_region('Lost Woods Bridge', ['Gift from Saria'], ['Kokiri Forest Entrance', 'Forest Exit']),
        create_ow_region('Hyrule Field', ['Ocarina of Time', 'Song from Ocarina of Time'], ['Field to Forest', 'Field to Lake', 'Field to Valley', 'Field to Castle Town', 'Field to Kakariko', 'Field to Zora River', 'Lon Lon Rance Entrance',
                                                     'Remote Southern Grotto', 'Field Near Lake Outside Fence Grotto', 'Field Near Lake Inside Fence Grotto', 'Field Valley Grotto', 'Field West Castle Town Grotto',
                                                     'Field Far West Castle Town Grotto', 'Field Kakariko Grotto', 'Field North Lon Lon Grotto']),
        create_ow_region('Lake Hylia', ['Underwater Bottle'], ['Lake Exit', 'Lake Hylia Dive Warp', 'Lake Hylia Lab', 'Fishing Hole', 'Lake Hylia Grotto']),
        create_interior_region('Lake Hylia Lab'),
        create_interior_region('Fishing Hole'),
        create_ow_region('Gerudo Valley', None, ['Valley Exit', 'Valley River']),
        create_ow_region('Castle Town', None, ['Castle Town Exit', 'Temple of Time', 'Hyrule Castle Grounds', 'Castle Town Rupee Room', 'Castle Town Bazaar', 'Castle Town Mask Shop', 'Castle Town Shooting Gallery',
                                               'Castle Town Bombchu Bowling', 'Castle Town Potion Shop', 'Castle Town Treasure Chest Game', 'Castle Town Bombchu Shop', 'Castle Town Dog Lady', 'Castle Town Man in Green House']),
        create_interior_region('Temple of Time', None, ['Temple of Time Exit', 'Door of Time']),
        create_interior_region('Beyond Door of Time', ['Master Sword Pedestal', 'Ganon'], ['Emerge as Adult']),
        create_ow_region('Hyrule Castle Grounds', None, ['Hyrule Castle Grounds Exit', 'Hyrule Castle Garden', 'Hyrule Castle Fairy']),
        create_ow_region('Hyrule Castle Garden', ['Zeldas Letter', 'Impa at Castle'], ['Hyrule Castle Garden Exit']),
        create_interior_region('Hyrule Castle Fairy', ['Hyrule Castle Fairy Reward']),
        create_interior_region('Castle Town Rupee Room'),
        create_interior_region('Castle Town Bazaar'),
        create_interior_region('Castle Town Mask Shop'),
        create_interior_region('Castle Town Shooting Gallery'),
        create_interior_region('Castle Town Bombchu Bowling'),
        create_interior_region('Castle Town Potion Shop'),
        create_interior_region('Castle Town Treasure Chest Game'),
        create_interior_region('Castle Town Bombchu Shop'),
        create_interior_region('Castle Town Dog Lady'),
        create_interior_region('Castle Town Man in Green House'),
        create_ow_region('Kakariko Village', None, ['Kakariko Exit', 'Carpenter Boss House', 'House of Skulltulla', 'Impas House', 'Impas House Back', 'Windmill', 'Kakariko Bazaar', 'Kakariko Shooting Gallery',
                                                    'Kakariko Potion Shop Front', 'Kakariko Potion Shop Back', 'Odd Medicine Building', 'Kakariko Bombable Grotto', 'Kakariko Back Grotto', 'Graveyard Entrance', 'Death Mountain Entrance']),
        create_interior_region('Carpenter Boss House'),
        create_interior_region('House of Skulltulla'),
        create_interior_region('Impas House'),
        create_interior_region('Impas House Back'),
        create_interior_region('Windmill'),
        create_interior_region('Kakariko Bazaar'),
        create_interior_region('Kakariko Shooting Gallery'),
        create_interior_region('Kakariko Potion Shop Front'),
        create_interior_region('Kakariko Potion Shop Back'),
        create_interior_region('Odd Medicine Building'),
        create_ow_region('Graveyard', None, ['Shield Grave', 'Composer Grave', 'Heart Piece Grave', 'Dampes House', 'Graveyard Exit']),
        create_interior_region('Shield Grave', ['Shield Grave Chest']),
        create_interior_region('Heart Piece Grave', ['Heart Piece Grave Chest']),
        create_interior_region('Composer Grave', ['Composer Grave Chest', 'Song from Composer Grave']),
        create_interior_region('Dampes House'),
        create_ow_region('Death Mountain', ['Death Mountain Bombable Chest'], ['Death Mountain Exit', 'Goron City Entrance', 'Mountain Crater Entrance', 'Mountain Summit Fairy', 'Dodongos Cavern Rocks', 'Mountain Bombable Grotto']),
        create_ow_region('Dodongos Cavern Entryway', None, ['Dodongos Cavern', 'Mountain Access from Behind Rock']),
        create_ow_region('Goron City', ['Goron City Leftmost Maze Chest', 'Goron City Left Maze Chest', 'Goron City Right Maze Chest'], ['Goron City Exit', 'Goron City Bomb Wall', 'Darunias Chamber']),
        create_ow_region('Goron City Woods Warp', None, ['Goron City from Woods', 'Goron City to Woods']),
        create_ow_region('Darunias Chamber', ['Darunias Sadness', 'Darunias Joy'], ['Darunias Chamber Exit']),
        create_ow_region('Death Mountain Crater', None, ['Crater Exit', 'Top of Crater Grotto']),
        create_interior_region('Mountain Summit Fairy', ['Mountain Summit Fairy Reward']),
        create_dungeon_region('Dodongos Cavern Beginning', None, ['Dodongos Cavern Exit', 'Dodongos Cavern Lobby']),
        create_dungeon_region('Dodongos Cavern Lobby', ['Dodongos Cavern Map Chest'], ['Dodongos Cavern Retreat', 'Dodongos Cavern Left Door']),
        create_dungeon_region('Dodongos Cavern Climb', ['Dodongos Cavern Compass Chest', 'Dodongos Cavern Bomb Flower Platform'], ['Dodongos Cavern Bridge Fall', 'Dodongos Cavern Slingshot Target']),
        create_dungeon_region('Dodongos Cavern Far Bridge', ['Dodongos Cavern Bomb Bag Chest', 'Dodongos Cavern End of Bridge Chest'], ['Dodongos Cavern Bomb Drop', 'Dodongos Cavern Bridge Fall 2']),        
        create_dungeon_region('Dodongos Cavern Boss Area', ['Chest Above King Dodongo', 'King Dodongo'], ['Dodongos Cavern Exit Skull']),
        create_ow_region('Zora River Bottom', None, ['Zora River Exit', 'Zora River Rocks']),
        create_ow_region('Zora River Top', None, ['Zora River Downstream', 'Zora River Dive Warp', 'Zora River Waterfall', 'Zora River Plateau Open Grotto', 'Zora River Plateau Bombable Grotto']),
        create_ow_region('Zoras Domain', ['Diving Minigame', 'Zoras Domain Torch Run', 'King Zora Moves'], ['Zoras Domain Exit', 'Zoras Domain Dive Warp', 'Behind King Zora', 'Zora Shop']),
        create_ow_region('Zoras Fountain', None, ['Zoras Fountain Exit', 'Jabu Jabus Belly', 'Zoras Fountain Fairy']),
        create_interior_region('Zora Shop'),
        create_interior_region('Zoras Fountain Fairy', ['Zoras Fountain Fairy Reward']),
        create_dungeon_region('Jabu Jabus Belly Beginning', None, ['Jabu Jabus Belly Exit', 'Jabu Jabus Belly Ceiling Switch']),
        create_dungeon_region('Jabu Jabus Belly Main', ['Boomerang Chest'], ['Jabu Jabus Belly Retreat', 'Jabu Jabus Belly Tentacles']),
        create_dungeon_region('Jabu Jabus Belly Depths', ['Jabu Jabus Belly Map Chest', 'Jabu Jabus Belly Compass Chest'], ['Jabu Jabus Belly Elevator', 'Jabu Jabus Belly Octopus']),
        create_dungeon_region('Jabu Jabus Belly Boss Area', ['Barinade'], ['Jabu Jabus Belly Final Backtrack']),
        create_ow_region('Lon Lon Ranch', None, ['Lon Lon Exit', 'Talon House', 'Ingo Barn', 'Lon Lon Corner Tower', 'Lon Lon Grotto']),
        create_interior_region('Talon House'),
        create_interior_region('Ingo Barn'),
        create_interior_region('Lon Lon Corner Tower'),
        create_grotto_region('Forest Generic Grotto'),
        create_grotto_region('Deku Theater'),
        create_grotto_region('Forest Sales Grotto'),
        create_grotto_region('Meadow Fairy Grotto'),
        create_grotto_region('Front of Meadow Grotto'),
        create_grotto_region('Lon Lon Grotto'),
        create_grotto_region('Remote Southern Grotto'),
        create_grotto_region('Field Near Lake Outside Fence Grotto'),
        create_grotto_region('Field Near Lake Inside Fence Grotto'),
        create_grotto_region('Field Valley Grotto'),
        create_grotto_region('Field West Castle Town Grotto'),
        create_grotto_region('Field Far West Castle Town Grotto'),
        create_grotto_region('Field Kakariko Grotto'),
        create_grotto_region('Field North Lon Lon Grotto'),
        create_grotto_region('Kakariko Bombable Grotto'),
        create_grotto_region('Kakariko Back Grotto'),
        create_grotto_region('Mountain Bombable Grotto'),
        create_grotto_region('Top of Crater Grotto'),
        create_grotto_region('Zora River Plateau Open Grotto'),
        create_grotto_region('Zora River Plateau Bombable Grotto'),
        create_grotto_region('Lake Hylia Grotto')
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
        address, default, type = location_table[location]
        ret.locations.append(Location(location, address, default, type, ret))
    return ret

location_table = {'Kokiri Sword Chest': (0x20A6142, 0x04E0, 'Chest'),
                  'Mido Chest Top Left': (0x2F7B08A, 0x59A0, 'Chest'),
                  'Mido Chest Top Right': (0x2F7B09A, 0x59A1, 'Chest'),
                  'Mido Chest Bottom Left': (0x2F7B0AA, 0x5982, 'Chest'),
                  'Mido Chest Bottom Right': (0x2F7B0BA, 0x5903, 'Chest'),
                  'Shield Grave Chest': (0x328B096, 0x5540, 'Chest'),
                  'Heart Piece Grave Chest': (0x2D0A056, 0xA7C0, 'Chest'),
                  'Composer Grave Chest': (0x332D0EA, 0x8020, 'Chest'),
                  'Death Mountain Bombable Chest': (0x223C3CA, 0x5AA1, 'Chest'),
                  'Goron City Leftmost Maze Chest': (0x227C23A, 0x5AC0, 'Chest'),
                  'Goron City Left Maze Chest': (0x227C24A, 0x5AA1, 'Chest'),
                  'Goron City Right Maze Chest': (0x227C25A, 0x5AA2, 'Chest'),
                  'Zoras Domain Torch Run': (0x2103166, 0xB7C0, 'Chest'),
                  'Deku Tree Lobby Chest': (0x24A7146, 0x0823, 'Chest'),
                  'Deku Tree Slingshot Chest': (0x24C20C6, 0x00A1, 'Chest'),
                  'Deku Tree Slingshot Room Side Chest': (0x24C20D6, 0x5905, 'Chest'),
                  'Deku Tree Compass Chest': (0x25040D6, 0x0802, 'Chest'),
                  'Deku Tree Compass Room Side Chest': (0x25040E6, 0x5906, 'Chest'),
                  'Deku Tree Basement Chest': (0x24C8166, 0x5904, 'Chest'),
                  'Dodongos Cavern Map Chest': (0x1F2819E, 0x0828, 'Chest'),
                  'Dodongos Cavern Compass Chest': (0x1FAF0AA, 0x0805, 'Chest'),
                  'Dodongos Cavern Bomb Flower Platform': (0x1F890DE, 0x59C6, 'Chest'),
                  'Dodongos Cavern Bomb Bag Chest': (0x1F890CE, 0x0644, 'Chest'),
                  'Dodongos Cavern End of Bridge Chest': (0x1F281CE, 0x552A, 'Chest'),
                  'Chest Above King Dodongo': (0x2EB00BA, 0x5020, 'Chest'),
                  'Boomerang Chest': (0x278A0BA, 0x10C1, 'Chest'),
                  'Jabu Jabus Belly Map Chest': (0x278E08A, 0x1822, 'Chest'),
                  'Jabu Jabus Belly Compass Chest': (0x279608A, 0xB804, 'Chest'),
                  'Impa at Castle': (0x2E8E961, 0x2E8E979, 'Song'),
                  'Song from Composer Grave': (0x332A8AD, 0x332A8C5, 'Song'),
                  'Song from Saria': (0x20B1DED, 0x20B1E05, 'Song'),
                  'Song from Ocarina of Time': (0x252FCC5, 0x252FCDD, 'Song'),
                  'Gift from Saria': (None, None, 'NPC'),
                  'Zeldas Letter': (None, None, 'NPC'),
                  'Mountain Summit Fairy Reward': (None, None, 'Fairy'),
                  'Hyrule Castle Fairy Reward': (None, None, 'Fairy'),
                  'Zoras Fountain Fairy Reward': (None, None, 'Fairy'),
                  'Darunias Sadness': (None, None, 'Event'),
                  'Darunias Joy': (None, None, 'NPC'),
                  'Diving Minigame': (None, None, 'NPC'),
                  'Underwater Bottle': (None, None, 'Event'),
                  'King Zora Moves': (None, None, 'Event'),
                  'Ocarina of Time': (None, None, 'Event'),
                  'Master Sword Pedestal': (None, None, 'Event'),
                  'Queen Gohma': (None, None, 'Boss'),
                  'King Dodongo': (None, None, 'Boss'),
                  'Barinade': (None, None, 'Boss'),
                  'Ganon': (None, None, 'Boss')}