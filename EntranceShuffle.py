import random

def link_entrances(world):

    # setup mandatory connections
    for exitname, regionname in mandatory_connections:
        connect_simple(world, exitname, regionname)

    # if we do not shuffle, set default connections
    if world.shuffle == 'vanilla':
        for exitname, regionname in default_connections:
            connect_simple(world, exitname, regionname)
        for exitname, regionname in default_dungeon_connections:
            connect_simple(world, exitname, regionname)
        targets = list(Fairy_List)
        destinations = list(Fairy_List)
        random.shuffle(targets)
        random.shuffle(destinations)
        Fairy_Pairs = []
        for i in range (0, 6):
            Fairy_Pairs.append((targets[i], destinations[i]))
        for i in range (0, 6):
            connect_fairy(world, Fairy_Pairs[i][0], Fairy_Pairs[i][1])
    else:
        raise NotImplementedError('Shuffling not supported yet')


def connect_simple(world, exitname, regionname):
    world.get_entrance(exitname).connect(world.get_region(regionname))

def connect_entrance(world, entrancename, exitname):
    entrance = world.get_entrance(entrancename)
    # check if we got an entrance or a region to connect to
    try:
        region = world.get_region(exitname)
        exit = None
    except RuntimeError:
        exit = world.get_entrance(exitname)
        region = exit.parent_region

    # if this was already connected somewhere, remove the backreference
    if entrance.connected_region is not None:
        entrance.connected_region.entrances.remove(entrance)

    target = exit_ids[exit.name][0] if exit is not None else exit_ids.get(region.name, None)
    addresses = door_addresses[entrance.name][0]

    entrance.connect(region, addresses, target)
    world.spoiler.set_entrance(entrance.name, exit.name if exit is not None else region.name, 'entrance')


def connect_exit(world, exitname, entrancename):
    entrance = world.get_entrance(entrancename)
    exit = world.get_entrance(exitname)

    # if this was already connected somewhere, remove the backreference
    if exit.connected_region is not None:
        exit.connected_region.entrances.remove(exit)

    exit.connect(entrance.parent_region, door_addresses[entrance.name][1], exit_ids[exit.name][1])
    world.spoiler.set_entrance(entrance.name, exit.name, 'exit')


def connect_random(world, exitlist, targetlist, two_way=False):
    targetlist = list(targetlist)
    random.shuffle(targetlist)

    for exit, target in zip(exitlist, targetlist):
        if two_way:
            connect_two_way(world, exit, target)
        else:
            connect_entrance(world, exit, target)


def connect_doors(world, doors, targets):
    """This works inplace"""
    random.shuffle(doors)
    random.shuffle(targets)
    while doors:
        door = doors.pop()
        target = targets.pop()
        connect_entrance(world, door, target)


def connect_fairy(world, entrancename, exitname):
    entrance = world.get_entrance(entrancename)
    exit = world.get_region(exitname)

    entrance.connect(exit, Fairy_addresses[entrance.name], Fairy_IDs[exit.name])
    world.spoiler.set_entrance(entrance.name, exit.name, 'both')

# these are connections that cannot be shuffled and always exist. They link together separate parts of the world we need to divide into regions
mandatory_connections = [('Adult Forest Warp Pad', 'Forest Temple Entry Area'),
                         ('Child Forest Warp Pad', 'Sacred Forest Meadow'),
                         ('Temple Warp Pad', 'Temple of Time'),
                         ('Crater Warp Pad', 'Death Mountain Crater Central'),
                         ('Lake Warp Pad', 'Lake Hylia'),
                         ('Graveyard Warp Pad', 'Shadow Temple Warp Region'),
                         ('Colossus Warp Pad', 'Desert Colossus'),
                         ('Lost Woods', 'Lost Woods'),
                         ('Lost Woods Front', 'Kokiri Forest'),
                         ('Woods to Goron City', 'Goron City Woods Warp'),
                         ('Goron City to Woods', 'Lost Woods'),
                         ('Goron City from Woods', 'Goron City'),
                         ('Goron City Bomb Wall', 'Goron City Woods Warp'),
                         ('Lost Woods Dive Warp', 'Zora River Top'),
                         ('Zora River Dive Warp', 'Lost Woods'),
                         ('Meadow Entrance', 'Sacred Forest Meadow Entryway'),
                         ('Meadow Exit', 'Lost Woods'),
                         ('Meadow Gate', 'Sacred Forest Meadow'),
                         ('Meadow Gate Exit', 'Sacred Forest Meadow Entryway'),
                         ('Adult Meadow Access', 'Forest Temple Entry Area'),
                         ('Adult Meadow Exit', 'Lost Woods'),
                         ('Lost Woods Bridge', 'Lost Woods Bridge'),
                         ('Kokiri Forest Entrance', 'Kokiri Forest'),
                         ('Field to Forest', 'Lost Woods Bridge'),
                         ('Forest Exit', 'Hyrule Field'),
                         ('Field to Lake', 'Lake Hylia'),
                         ('Lake Hylia Dive Warp', 'Zoras Domain'),
                         ('Zoras Domain Dive Warp', 'Lake Hylia'),
                         ('Lake Exit', 'Hyrule Field'),
                         ('Field to Valley', 'Gerudo Valley'),
                         ('Valley Exit', 'Hyrule Field'),
                         ('Valley River', 'Lake Hylia'),
                         ('Bridge Crossing', 'Gerudo Valley Far Side'),
                         ('Fortress Entrance', 'Gerudo Fortress'),
                         ('Haunted Wasteland Entrance', 'Haunted Wasteland'),
                         ('Haunted Wasteland Crossing', 'Desert Colossus'),
                         ('Field to Castle Town', 'Castle Town'),
                         ('Castle Town Exit', 'Hyrule Field'),
                         ('Hyrule Castle Grounds', 'Hyrule Castle Grounds'),
                         ('Hyrule Castle Grounds Exit', 'Castle Town'),
                         ('Hyrule Castle Garden', 'Hyrule Castle Garden'),
                         ('Hyrule Castle Garden Exit', 'Hyrule Castle Grounds'),
                         ('Ganons Castle Grounds', 'Ganons Castle Grounds'),
                         ('Ganons Castle Grounds Exit', 'Castle Town'),
                         ('Field to Kakariko', 'Kakariko Village'),
                         ('Kakariko Exit', 'Hyrule Field'),
                         ('Graveyard Entrance', 'Graveyard'),
                         ('Graveyard Exit', 'Kakariko Village'),
                         ('Drop to Graveyard', 'Graveyard'),
                         ('Death Mountain Entrance', 'Death Mountain'),
                         ('Death Mountain Exit', 'Kakariko Village'),
                         ('Goron City Entrance', 'Goron City'),
                         ('Goron City Exit', 'Death Mountain'),
                         ('Darunias Chamber', 'Darunias Chamber'),
                         ('Darunias Chamber Exit', 'Goron City'),
                         ('Mountain Crater Entrance', 'Death Mountain Crater Upper'),
                         ('Crater Exit', 'Death Mountain'),
                         ('Crater Hover Boots', 'Death Mountain Crater Lower'),
                         ('Crater Ascent', 'Death Mountain Crater Upper'),
                         ('Crater Scarecrow', 'Death Mountain Crater Central'),
                         ('Crater Bridge', 'Death Mountain Crater Central'),
                         ('Crater Bridge Reverse', 'Death Mountain Crater Lower'),
                         ('Crater to City', 'Goron City'),
                         ('Crater Access', 'Death Mountain Crater Lower'),
                         ('Dodongos Cavern Rocks', 'Dodongos Cavern Entryway'),
                         ('Mountain Access from Behind Rock', 'Death Mountain'),
                         ('Field to Zora River', 'Zora River Bottom'),
                         ('Zora River Exit', 'Hyrule Field'),
                         ('Zora River Rocks', 'Zora River Top'),
                         ('Zora River Downstream', 'Zora River Bottom'),
                         ('Zora River Waterfall', 'Zoras Domain'),
                         ('Zoras Domain Exit', 'Zora River Top'),
                         ('Behind King Zora', 'Zoras Fountain'),
                         ('Zoras Fountain Exit', 'Zoras Domain'),
                         ('Zora River Adult', 'Zora River Adult'),
                         ('Zoras Domain Adult Access', 'Zoras Domain Frozen'),
                         ('Zoras Fountain Adult Access', 'Outside Ice Cavern'),
                         ('Lon Lon Rance Entrance', 'Lon Lon Ranch'),
                         ('Lon Lon Exit', 'Hyrule Field'),
                         ('Deku Tree Slingshot Passage', 'Deku Tree Slingshot Room'),
                         ('Deku Tree Slingshot Exit', 'Deku Tree Lobby'),
                         ('Deku Tree Basement Path', 'Deku Tree Boss Room'),
                         ('Deku Tree Basement Vines', 'Deku Tree Lobby'),
                         ('Dodongos Cavern Lobby', 'Dodongos Cavern Lobby'),
                         ('Dodongos Cavern Retreat', 'Dodongos Cavern Beginning'),
                         ('Dodongos Cavern Left Door', 'Dodongos Cavern Climb'),
                         ('Dodongos Cavern Bridge Fall', 'Dodongos Cavern Lobby'),
                         ('Dodongos Cavern Slingshot Target', 'Dodongos Cavern Far Bridge'),
                         ('Dodongos Cavern Bridge Fall 2', 'Dodongos Cavern Lobby'),
                         ('Dodongos Cavern Bomb Drop', 'Dodongos Cavern Boss Area'),
                         ('Dodongos Cavern Exit Skull', 'Dodongos Cavern Lobby'),
                         ('Jabu Jabus Belly Ceiling Switch', 'Jabu Jabus Belly Main'),
                         ('Jabu Jabus Belly Retreat', 'Jabu Jabus Belly Beginning'),
                         ('Jabu Jabus Belly Tentacles', 'Jabu Jabus Belly Depths'),
                         ('Jabu Jabus Belly Elevator', 'Jabu Jabus Belly Main'),
                         ('Jabu Jabus Belly Octopus', 'Jabu Jabus Belly Boss Area'),
                         ('Jabu Jabus Belly Final Backtrack', 'Jabu Jabus Belly Main'),
                         ('Forest Temple Song of Time Block', 'Forest Temple NW Outdoors'),
                         ('Forest Temple Lobby Eyeball Switch', 'Forest Temple NE Outdoors'),
                         ('Forest Temple Lobby Locked Door', 'Forest Temple Block Push Room'),
                         ('Forest Temple Through Map Room', 'Forest Temple NE Outdoors'),
                         ('Forest Temple Well Connection', 'Forest Temple NW Outdoors'),
                         ('Forest Temple Outside to Lobby', 'Forest Temple Lobby'),
                         ('Forest Temple Scarecrows Song', 'Forest Temple Falling Room'),
                         ('Forest Temple Falling Room Exit', 'Forest Temple NE Outdoors'),
                         ('Forest Temple Elevator', 'Forest Temple Boss Region'),
                         ('Forest Temple Outside Backdoor', 'Forest Temple Outside Upper Ledge'),
                         ('Forest Temple Twisted Hall', 'Forest Temple Bow Region'),
                         ('Forest Temple Straightened Hall', 'Forest Temple Straightened Hall'),
                         ('Forest Temple Boss Key Chest Drop', 'Forest Temple Outside Upper Ledge'),
                         ('Forest Temple Outside Ledge Drop', 'Forest Temple NW Outdoors'),
                         ('Forest Temple Drop to Falling Room', 'Forest Temple Falling Room'),
                         ('Fire Temple Early Climb', 'Fire Temple Middle'),
                         ('Fire Temple Fire Maze Escape', 'Fire Temple Upper'),
                         ('Water Temple Central Pillar', 'Water Temple Middle Water Level'),
                         ('Water Temple Upper Locked Door', 'Water Temple Dark Link Region'),
                         ('Shadow Temple First Pit', 'Shadow Temple First Beamos'),
                         ('Shadow Temple Bomb Wall', 'Shadow Temple Huge Pit'),
                         ('Shadow Temple Hookshot Target', 'Shadow Temple Wind Tunnel'),
                         ('Shadow Temple Boat', 'Shadow Temple Beyond Boat'),
                         ('Gerudo Training Ground Left Silver Rupees', 'Gerudo Training Grounds Heavy Block Room'),
                         ('Gerudo Training Ground Beamos', 'Gerudo Training Grounds Lava Room'),
                         ('Gerudo Training Ground Central Door', 'Gerudo Training Grounds Central Maze'),
                         ('Gerudo Training Grounds Right Locked Doors', 'Gerudo Training Grounds Central Maze Right'),
                         ('Gerudo Training Grounds Maze Exit', 'Gerudo Training Grounds Lava Room'),
                         ('Gerudo Training Grounds Maze Ledge', 'Gerudo Training Grounds Central Maze Right'),
                         ('Gerudo Training Grounds Right Hookshot Target', 'Gerudo Training Grounds Hammer Room'),
                         ('Gerudo Training Grounds Hammer Target', 'Gerudo Training Grounds Eye Statue Lower'),
                         ('Gerudo Training Grounds Hammer Room Clear', 'Gerudo Training Grounds Lava Room'),
                         ('Gerudo Training Grounds Eye Statue Exit', 'Gerudo Training Grounds Hammer Room'),
                         ('Gerudo Training Grounds Eye Statue Drop', 'Gerudo Training Grounds Eye Statue Lower'),
                         ('Gerudo Training Grounds Hidden Hookshot Target', 'Gerudo Training Grounds Eye Statue Upper'),
                         ('Spirit Temple Crawl Passage', 'Child Spirit Temple'),
                         ('Spirit Temple Silver Block', 'Early Adult Spirit Temple'),
                         ('Child Spirit Temple Passthrough', 'Spirit Temple Central Chamber'),
                         ('Adult Spirit Temple Passthrough', 'Spirit Temple Central Chamber'),
                         ('Spirit Temple to Hands', 'Spirit Temple Outdoor Hands'),
                         ('Spirit Temple Central Locked Door', 'Spirit Temple Beyond Central Locked Door'),
                         ('Spirit Temple Final Locked Door', 'Spirit Temple Beyond Final Locked Door'),
                         ('Ganons Castle Forest Trial', 'Ganons Castle Forest Trial'),
                         ('Ganons Castle Fire Trial', 'Ganons Castle Fire Trial'),
                         ('Ganons Castle Water Trial', 'Ganons Castle Water Trial'),
                         ('Ganons Castle Shadow Trial', 'Ganons Castle Shadow Trial'),
                         ('Ganons Castle Spirit Trial', 'Ganons Castle Spirit Trial'),
                         ('Ganons Castle Light Trial', 'Ganons Castle Light Trial'),
                         ('Ganons Castle Tower', 'Ganons Castle Tower')
                        ]

# non-shuffled entrance links
default_connections = [('Links House Exit', 'Kokiri Forest'),
                       ('Links House', 'Links House'),
                       ('Mido House Exit', 'Kokiri Forest'),
                       ('Mido House', 'Mido House'),
                       ('Saria House Exit', 'Kokiri Forest'),
                       ('Saria House', 'Saria House'),
                       ('House of Twins Exit', 'Kokiri Forest'),
                       ('House of Twins', 'House of Twins'),
                       ('Know It All House Exit', 'Kokiri Forest'),
                       ('Know It All House', 'Know It All House'),
                       ('Kokiri Shop Exit', 'Kokiri Forest'),
                       ('Kokiri Shop', 'Kokiri Shop'),
                       ('Lake Hylia Lab', 'Lake Hylia Lab'),
                       ('Fishing Hole', 'Fishing Hole'),
                       ('Temple of Time', 'Temple of Time'),
                       ('Temple of Time Exit', 'Castle Town'),
                       ('Door of Time', 'Beyond Door of Time'),
                       ('Emerge as Adult', 'Temple of Time'),
                       ('Castle Town Rupee Room', 'Castle Town Rupee Room'),
                       ('Castle Town Bazaar', 'Castle Town Bazaar'),
                       ('Castle Town Mask Shop', 'Castle Town Mask Shop'),
                       ('Castle Town Shooting Gallery', 'Castle Town Shooting Gallery'),
                       ('Castle Town Bombchu Bowling', 'Castle Town Bombchu Bowling'),
                       ('Castle Town Potion Shop', 'Castle Town Potion Shop'),
                       ('Castle Town Treasure Chest Game', 'Castle Town Treasure Chest Game'),
                       ('Castle Town Bombchu Shop', 'Castle Town Bombchu Shop'),
                       ('Castle Town Dog Lady', 'Castle Town Dog Lady'),
                       ('Castle Town Man in Green House', 'Castle Town Man in Green House'),
                       ('Carpenter Boss House', 'Carpenter Boss House'),
                       ('House of Skulltulla', 'House of Skulltulla'),
                       ('Impas House', 'Impas House'),
                       ('Impas House Back', 'Impas House Back'),
                       ('Windmill', 'Windmill'),
                       ('Kakariko Bazaar', 'Kakariko Bazaar'),
                       ('Kakariko Shooting Gallery', 'Kakariko Shooting Gallery'),
                       ('Kakariko Potion Shop Front', 'Kakariko Potion Shop Front'),
                       ('Kakariko Potion Shop Back', 'Kakariko Potion Shop Back'),
                       ('Odd Medicine Building', 'Odd Medicine Building'),
                       ('Shield Grave', 'Shield Grave'),
                       ('Heart Piece Grave', 'Heart Piece Grave'),
                       ('Composer Grave', 'Composer Grave'),
                       ('Dampes Grave', 'Dampes Grave'),
                       ('Dampes House', 'Dampes House'),
                       ('Talon House', 'Talon House'),
                       ('Ingo Barn', 'Ingo Barn'),
                       ('Lon Lon Corner Tower', 'Lon Lon Corner Tower'),
                       ('Zora Shop', 'Zora Shop'),
                       ('Forest Generic Grotto', 'Forest Generic Grotto'),
                       ('Deku Theater', 'Deku Theater'),
                       ('Forest Sales Grotto', 'Forest Sales Grotto'),
                       ('Meadow Fairy Grotto', 'Meadow Fairy Grotto'),
                       ('Front of Meadow Grotto', 'Front of Meadow Grotto'),
                       ('Lon Lon Grotto', 'Lon Lon Grotto'),
                       ('Remote Southern Grotto', 'Remote Southern Grotto'),
                       ('Field Near Lake Outside Fence Grotto', 'Field Near Lake Outside Fence Grotto'),
                       ('Field Near Lake Inside Fence Grotto', 'Field Near Lake Inside Fence Grotto'),
                       ('Field Valley Grotto', 'Field Valley Grotto'),
                       ('Field West Castle Town Grotto', 'Field West Castle Town Grotto'),
                       ('Field Far West Castle Town Grotto', 'Field Far West Castle Town Grotto'),
                       ('Field Kakariko Grotto', 'Field Kakariko Grotto'),
                       ('Kakariko Bombable Grotto', 'Kakariko Bombable Grotto'),
                       ('Kakariko Back Grotto', 'Kakariko Back Grotto'),
                       ('Mountain Bombable Grotto', 'Mountain Bombable Grotto'),
                       ('Top of Crater Grotto', 'Top of Crater Grotto'),
                       ('Field North Lon Lon Grotto', 'Field North Lon Lon Grotto'),
                       ('Castle Storms Grotto', 'Castle Storms Grotto'),
                       ('Zora River Plateau Open Grotto', 'Zora River Plateau Open Grotto'),
                       ('Zora River Plateau Bombable Grotto', 'Zora River Plateau Bombable Grotto'),
                       ('Lake Hylia Grotto', 'Lake Hylia Grotto')
                      ]

# non shuffled dungeons
default_dungeon_connections = [('Deku Tree', 'Deku Tree Lobby'),
                               ('Deku Tree Exit', 'Kokiri Forest'),
                               ('Dodongos Cavern', 'Dodongos Cavern Beginning'),
                               ('Dodongos Cavern Exit', 'Dodongos Cavern Entryway'),
                               ('Jabu Jabus Belly', 'Jabu Jabus Belly Beginning'),
                               ('Jabu Jabus Belly Exit', 'Zoras Fountain'),
                               ('Forest Temple Entrance', 'Forest Temple Lobby'),
                               ('Forest Temple Exit', 'Forest Temple Entry Area'),
                               ('Bottom of the Well', 'Bottom of the Well'),
                               ('Bottom of the Well Exit', 'Kakariko Village'),
                               ('Fire Temple Entrance', 'Fire Temple Lower'),
                               ('Fire Temple Exit', 'Death Mountain Crater Central'),
                               ('Ice Cavern Entrance', 'Ice Cavern'),
                               ('Ice Cavern Exit', 'Outside Ice Cavern'),
                               ('Water Temple Entrance', 'Water Temple Lobby'),
                               ('Water Temple Exit', 'Lake Hylia'),
                               ('Shadow Temple Entrance', 'Shadow Temple Beginning'),
                               ('Shadow Temple Exit', 'Shadow Temple Warp Region'),
                               ('Gerudo Training Grounds Entrance', 'Gerudo Training Grounds Lobby'),
                               ('Gerudo Training Grounds Exit', 'Gerudo Fortress'),
                               ('Spirit Temple Entrance', 'Spirit Temple Lobby'),
                               ('Spirit Temple Exit', 'Desert Colossus'),
                               ('Rainbow Bridge', 'Ganons Castle Lobby'),
                               ('Ganons Castle Exit', 'Ganons Castle Grounds')
                              ]

# Fairy Fountain exit IDs
# (entrance, exit)

Fairy_List = ['Colossus Fairy',
              'Hyrule Castle Fairy',
              'Ganons Castle Fairy',
              'Crater Fairy',
              'Mountain Summit Fairy',
              'Zoras Fountain Fairy']

Fairy_IDs = {'Colossus Fairy': (0x0588, 0xBEFD82),
             'Hyrule Castle Fairy': (0x0578, 0xBEFD80),
             'Ganons Castle Fairy': (0x04C2, 0xBEFD6C),
             'Crater Fairy': (0x04BE, 0xBEFD6A),
             'Mountain Summit Fairy': (0x0315, 0xBEFD68),
             'Zoras Fountain Fairy': (0x0371, 0xBEFD7E)}

# Fairy Fountain exit addresses
# (entrance, exit)

Fairy_addresses = {'Colossus Fairy': (0x2186114, 0x218D644, 0x218D644, 0x057C),
                   'Hyrule Castle Fairy': (0x21F60E0, 0x21F60E0, 0x21F60E0, 0x0340),
                   'Ganons Castle Fairy': (0x292B0B4, 0x292B0B4, 0x292B0B4, 0x0340),
                   'Crater Fairy': (0x22470FE, 0x224E31A, 0x224E31A, 0x0482),
                   'Mountain Summit Fairy': (0x221D104, 0x222467C, 0x222467C, 0x045B),
                   'Zoras Fountain Fairy': (0x21100F4, 0x2114624, 0x2114444, 0x0394)}