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

# these are connections that cannot be shuffled and always exist.
# They logically separate areas that do not cross loading zones
mandatory_connections = [('South Mailbox', 'Mailbox'),
                                                ('East Mailbox', 'Mailbox'),
                                                ('North Mailbox', 'Mailbox'),
                                                ('Tunnel Balloon From Observatory', 'Bomber Tunnel'),
                                                ('Tunnel Balloon From ECT', 'Astral Observatory')
                        ]

# these connections are the pairs of owl statues that may be shuffled
owl_statue_connections = [('', '')
                        ]

# entrances that cross a loading zone and may be shuffled
default_connections = [('Clock Tower Exit', 'Clock Town'),
                                        ('Clock Tower Twisted Hallway', 'Prologue Room'),
                                        ('Clock Tower Entrance', 'Clock Tower'),
                                        ('Clock Tower Carnival Door', 'Clock Tower Rooftop'),
                                        ('SCT Top Exit to WCT', 'West Clock Town'),
                                        ('SCT Bottom Exit to WCT', 'West Clock Town'),
                                        ('SCT Exit to NCT', 'SCT Exit to NCT', 'North Clock Town'),
                                        ('SCT Bottom Exit to ECT', 'East Clock Town'),
                                        ('SCT Top Exit to ECT', 'East Clock Town'),
                                        ('Clock Town South Gate', 'Termina Field'),
                                        ('SCT Exit to Laundry Pool', 'Laundry Pool'),
                                        ('Honey and Darling', 'Honey and Darling'),
                                        ('Treasure Chest Shop', 'Treasure Chest Shop'),
                                        ('Town Shooting Gallery', 'Town Shooting Gallery'),
                                        ('Milk Bar', 'Milk Bar'),
                                        ('Stock Pot Inn', 'Stock Pot Inn'),
                                        ('Stock Pot Inn Secret Entrance', 'Stock Pot Inn'),
                                        ('Mayors Office', 'Mayors Office'),
                                        ('Bomber Bouncer', 'Bomber Tunnel'),
                                        ('Honey and Darling Exit', 'Clock Town'),
                                        ('Treasure Chest Shop Exit', 'Clock Town'),
                                        ('Town Shooting Gallery Exit', 'Clock Town'),
                                        ('Milk Bar Exit', 'Clock Town'),
                                        ('Stock Pot Inn Roof', 'Clock Town'),
                                        ('Stock Pot Inn Front Door', 'Clock Town'),
                                        ('Mayors Office Exit', 'Clock Town'),
                                        ('Bomber Tunnel Exit', 'Clock Town'),
                                        ('ECT Top Exit to SCT', 'South Clock Town'),
                                        ('ECT Bottom Exit to SCT', 'South Clock Town'),
                                        ('ECT Exit to NCT', 'North Clock Town'),
                                        ('Clock Town East Gate', 'Termina Field')
                                        ]

# dungeon entrance links
default_dungeon_connections = [('Woodfall Temple Entrance', 'Woodfall Temple Lobby'),
                              ]

# Fairy Fountain exit IDs
# (entrance, exit)

Fairy_List = ['Clock Town Fairy',
              'Woodfall Fairy',
              'Snowhead Fairy',
              'Great Bay Fairy',
              'Stone Tower Fairy']

Fairy_IDs = {'Clock Town Fairy': (0x0588, 0xBEFD82),
             'Woodfall Fairy': (0x04C2, 0xBEFD6C),
             'Snowhead Fairy': (0x04BE, 0xBEFD6A),
             'Great Bay Fairy': (0x0315, 0xBEFD68),
             'Stone Tower Fairy': (0x0371, 0xBEFD7E)}

# Fairy Fountain exit addresses
# (entrance, exit)

Fairy_addresses = {'Clock Town Fairy': (0x2186114, 0x218D644, 0x218D644, 0x057C),
                   'Woodfall Fairy': (0x21F60E0, 0x21F60E0, 0x21F60E0, 0x0340),
                   'Snowhead Fairy': (0x292B0B4, 0x292B0B4, 0x292B0B4, 0x0340),
                   'Great Bay Fairy': (0x22470FE, 0x224E31A, 0x224E31A, 0x0482),
                   'Stone Tower Fairy': (0x221D104, 0x222467C, 0x222467C, 0x045B)}
