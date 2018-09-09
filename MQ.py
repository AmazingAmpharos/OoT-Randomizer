# mzxrules 2018
#
# In order to patch MQ to the existing data...
# 
# Ice Cavern (Scene 9) needs to have it's header altered to support MQ's path list. This 
# expansion will delete the otherwise unused alternate headers command
# 
# Scenes:
# 
# Transition actors will be patched over the old data, as the number of records is the same
# Path data will be appended to the end of the scene file. 
# 
# The size of a single path on file is NUM_POINTS * 6, rounded up to the nearest 4 byte boundary
# The total size consumed by the path data is NUM_PATHS * 8, plus the sum of all path file sizes
# padded to the nearest 0x10 bytes
# 
# Rooms:
# 
# Object file initialization data will be appended to the end of the room file.
# The total size consumed by the object file data is NUM_OBJECTS * 0x02, aligned to
# the nearest 0x04 bytes
# 
# Actor spawn data will be appended to the end of the room file, after the objects.
# The total size consumed by the actor spawn data is NUM_ACTORS * 0x10
# 
# Finally:
# 
# Scene and room files will be padded to the nearest 0x10 bytes

from Utils import local_path
from Rom import LocalRom
import json
from struct import pack, unpack

DMA_TABLE = 0x7430
SCENE_TABLE = 0xB71440


class File(object):
    def __init__(self, file):
        self.name = file['Name']
        self.start = int(file['Start'], 16)
        self.end = int(file['End'], 16)
        self.remap = file['RemapStart']

        # used to update the file's associated dmadata record
        self.dma_key = self.start

        if self.remap is not None:
            self.remap = int(self.remap, 16)

    def __repr__(self):
        remap = "None"
        if self.remap is not None:
            remap = "{0:x}".format(self.remap)
        return "{0}: {1:x} {2:x}, remap {3}".format(self.name, self.start, self.end, remap)

    def relocate(self, rom:LocalRom):
        if self.remap is None:
            return

        new_start = self.remap
       
        offset = new_start - self.start
        new_end = self.end + offset

        rom.buffer[new_start:new_end] = rom.buffer[self.start:self.end]
        self.start = new_start
        self.end = new_end


class Scene(object):
    def __init__(self, scene):
        self.file = File(scene['File'])
        self.id = scene['Id']
        self.transition_actors = [convert_actor_data(x) for x in scene['TActors']]
        self.rooms = [Room(x) for x in scene['Rooms']]
        self.paths = []
        temp_paths = scene['Paths']
        for item in temp_paths:
            self.paths.append(item['Points'])


    def write_data(self, rom:LocalRom):
        
        # move file to remap address
        self.file.relocate(rom)

        start = self.file.start
        headcur = self.file.start

        room_list_offset = 0

        code = rom.read_byte(headcur)
        loop = 0x20
        while loop > 0 and code != 0x14: #terminator
            loop -= 1

            if code == 0x04: #rooms
                room_list_offset = rom.read_int24(headcur + 5)

            elif code == 0x0D: #paths
                path_offset = self.append_path_data(rom)
                rom.write_int32(headcur + 4, path_offset)

            elif code == 0x0E: #transition actors
                t_offset = rom.read_int24(headcur + 5)
                addr = self.file.start + t_offset
                write_actor_data(rom, addr, self.transition_actors)

            headcur += 8
            code = rom.read_byte(headcur)

        # update file references
        self.file.end = align16(self.file.end)
        update_dmadata(rom, self.file)
        update_scene_table(rom, self.id, self.file.start, self.file.end)
        
        # write room file data
        for room in self.rooms:
            room.write_data(rom)

        cur = self.file.start + room_list_offset
        for room in self.rooms:
            rom.write_int32s(cur, [room.file.start, room.file.end])
            cur += 0x08


    # appends path data to the end of the rom
    # returns segment address to path data
    def append_path_data(self, rom:LocalRom):
        start = self.file.start
        cur = self.file.end
        records = []
        records_offset = 0

        for path in self.paths:
            nodes = len(path)
            offset = get_segment_address(2, cur - start)
            records.append((nodes, offset))

            #flatten
            points = [x for points in path for x in points]
            rom.write_int16s(cur, points)
            path_size = align4(len(path) * 6)
            cur += path_size

        records_offset = get_segment_address(2, cur - start) 
        for node, offset in records:
            rom.write_byte(cur, node)
            rom.write_int32(cur + 4, offset)
            cur += 8

        self.file.end = cur
        return records_offset


class Room(object):
    def __init__(self, room):
        self.file = File(room['File'])
        self.id = room['Id']
        self.objects = [int(x, 16) for x in room['Objects']]
        self.actors = [convert_actor_data(x) for x in room['Actors']]

    def write_data(self, rom:LocalRom):

        # move file to remap address
        self.file.relocate(rom)

        headcur = self.file.start

        code = rom.read_byte(headcur)
        loop = 0x20
        while loop != 0 and code != 0x14: #terminator
            loop -= 1

            if code == 0x01: # actors
                offset = self.file.end - self.file.start
                write_actor_data(rom, self.file.end, self.actors)
                self.file.end += len(self.actors) * 0x10

                rom.write_byte(headcur + 1, len(self.actors))
                rom.write_int32(headcur + 4, get_segment_address(3, offset))

            elif code == 0x0B: # objects
                offset = self.append_object_data(rom, self.objects)

                rom.write_byte(headcur + 1, len(self.objects))
                rom.write_int32(headcur + 4, get_segment_address(3, offset))

            headcur += 8
            code = rom.read_byte(headcur)

        # update file reference
        self.file.end = align16(self.file.end)
        update_dmadata(rom, self.file)
        

    def append_object_data(self, rom:LocalRom, objects):
        offset = self.file.end - self.file.start
        cur = self.file.end
        rom.write_int16s(cur, objects)

        objects_size = align4(len(objects) * 2)
        self.file.end += objects_size
        return offset


def patch_files(world, rom:LocalRom):
    #patch_ice_cavern_scene_header(rom)

    data = get_json()
    scenes = [Scene(x) for x in data]

    if world.dungeon_mq['DT']:
        scenes[0].write_data(rom)
    if world.dungeon_mq['DC']:
        scenes[1].write_data(rom)

    verify_dma(rom)


def get_json():
    with open(local_path('data/mqu.json'), 'r') as stream:
        data = json.load(stream)
    return data


def convert_actor_data(str):
    spawn_args = str.split(" ")
    return [ int(x,16) for x in spawn_args ]


def get_segment_address(base, offset):
    offset &= 0xFFFFFF
    base *= 0x01000000
    return base + offset


def patch_ice_cavern_scene_header(rom):
    rom.buffer[0x2BEB000:0x2BEB038] = rom.buffer[0x2BEB008:0x2BEB040]
    rom.write_int32s(0x2BEB038, [0x0D000000, 0x02000000])


def get_dma_record(rom:LocalRom, cur):
    start = rom.read_int32(cur)
    end = rom.read_int32(cur+0x04)
    size = end-start
    return start, end, size


def verify_remap(scenes):
    def test_remap(file:File):
        if file.remap is not None:
            if file.start < file.remap:
                return False
        return True
    print("test code: verify remap won't corrupt data")

    for scene in scenes:
        file = scene.file
        result = test_remap(file)
        print("{0} - {1}".format(result, file))

        for room in scene.rooms:
            file = room.file
            result = test_remap(file)
            print("{0} - {1}".format(result, file))


def verify_dma(rom:LocalRom):
    cur = DMA_TABLE
    overlapping_records = []
    dma_data = []
    
    while True:
        this_start, this_end, this_size = get_dma_record(rom, cur)

        if this_start == 0 and this_end == 0:
            break

        dma_data.append((this_start, this_end, this_size))
        cur += 0x10

    dma_data.sort(key=lambda v: v[0])

    for i in range(0, len(dma_data) - 1):
        this_start, this_end, this_size = dma_data[i]
        next_start, next_end, next_size = dma_data[i + 1]

        if this_end > next_start:
            overlapping_records.append(
                    '0x%08X - 0x%08X (Size: 0x%04X)\n0x%08X - 0x%08X (Size: 0x%04X)' % \
                     (this_start, this_end, this_size, next_start, next_end, next_size)
                )

    if len(overlapping_records) > 0:
        raise Exception("Overlapping DMA Data Records!\n%s" % \
            '\n-------------------------------------\n'.join(overlapping_records))


def update_dmadata(rom:LocalRom, file:File):
    cur = DMA_TABLE

    key, start, end = file.dma_key, file.start, file.end

    dma_start, dma_end, dma_size = get_dma_record(rom, cur)
    while dma_start != key:
        if dma_start == 0 and dma_end == 0:
            break

        cur += 0x10
        dma_start, dma_end, dma_size = get_dma_record(rom, cur)

    if dma_start == 0:
        raise Exception('dmadata update failed: key {0:x} not found in dmadata'.format(key))

    else:
        rom.write_int32s(cur, [start, end, start, 0])


def update_scene_table(rom:LocalRom, sceneId, start, end):
    cur = sceneId * 0x14 + SCENE_TABLE
    rom.write_int32s(cur, [start, end])


def write_actor_data(rom:LocalRom, cur, actors):
    for actor in actors:
        rom.write_int16s(cur, actor)
        cur += 0x10

def align4(value):
    return ((value + 3) // 4) * 4

def align16(value):
    return ((value + 0xF) // 0x10) * 0x10

# This function inserts space in a ovl section at the section's offset
# The section size is expanded
# Every relocation entry in the section after the offet is moved accordingly
# Every relocation value that is after the inserted space is increased accordingly
def insert_space(rom, file, vram_start, insert_section, insert_offset, insert_size):
    sections = []
    val_hi = {}
    adr_hi = {}

    # get the ovl header
    cur = file.end - rom.read_int32(file.end - 4)
    section_total = 0
    for i in range(0, 4):
        # build the section offsets
        section_size = rom.read_int32(cur)
        sections.append(section_total)
        section_total += section_size

        # increase the section to be expanded
        if insert_section == i:
            rom.write_int32(cur, section_size + insert_size)

        cur += 4

    # calculate the insert address in vram
    insert_vram = sections[insert_section] + insert_offset + vram_start
    insert_rom = sections[insert_section] + insert_offset + file.start

    # iterate over the relocation table
    relocate_count = rom.read_int32(cur)
    cur += 4
    for i in range(0, relocate_count):
        entry = rom.read_int32(cur)

        # parse relocation entry
        section = ((entry & 0xC0000000) >> 30) - 1
        type = (entry & 0x3F000000) >> 24
        offset = entry & 0x00FFFFFF

        # calculate relocation address in rom
        address = file.start + sections[section] + offset

        # move relocation if section is increased and it's after the insert
        if insert_section == section and offset >= insert_offset:
            # rebuild new relocation entry
            rom.write_int32(cur, 
                ((section + 1) << 30) | 
                (type << 24) | 
                (offset + insert_size))

        # value contains the vram address
        value = rom.read_int32(address)
        raw_value = value
        if type == 2:
            # Data entry: value is the raw vram address
            pass
        elif type == 4:
            # Jump OP: Get the address from a Jump instruction
            value = 0x80000000 | (value & 0x03FFFFFF) << 2
        elif type == 5:
            # Load High: Upper half of an address load
            reg = (value >> 16) & 0x1F
            val_hi[reg] = (value & 0x0000FFFF) << 16
            adr_hi[reg] = address
            # Do not process, wait until the lower half is read
            value = None
        elif type == 6:
            # Load Low: Lower half of the address load
            reg = (value >> 21) & 0x1F
            val_low = value & 0x0000FFFF
            val_low = unpack('h', pack('H', val_low))[0]
            # combine with previous load high
            value = val_hi[reg] + val_low
        else:
            # unknown. OoT does not use any other types
            value = None

        # update the vram values if it's been moved
        if value != None and value >= insert_vram:
            # value = new vram address
            new_value = value + insert_size

            if type == 2:
                # Data entry: value is the raw vram address
                rom.write_int32(address, new_value)
            elif type == 4:
                # Jump OP: Set the address in the Jump instruction
                op = rom.read_int32(address) & 0xFC000000
                new_value = (new_value & 0x0FFFFFFC) >> 2
                new_value = op | new_value
                rom.write_int32(address, new_value)
            elif type == 6:
                # Load Low: Lower half of the address load
                op = rom.read_int32(address) & 0xFFFF0000
                new_val_low = new_value & 0x0000FFFF
                rom.write_int32(address, op | new_val_low)

                # Load High: Upper half of an address load
                op = rom.read_int32(adr_hi[reg]) & 0xFFFF0000
                new_val_hi = (new_value & 0xFFFF0000) >> 16
                if new_val_low >= 0x8000:
                    # add 1 if the lower part is negative for borrow
                    new_val_hi += 1
                rom.write_int32(adr_hi[reg], op | new_val_hi)

        cur += 4

    # Move rom bytes
    rom.buffer[(insert_rom + insert_size):(file.end + insert_size)] = rom.buffer[insert_rom:file.end]
    rom.buffer[insert_rom:(insert_rom + insert_size)] = [0] * insert_size
    file.end += insert_size


def add_relocations(rom, file, addresses):
    relocations = []
    sections = []
    header_size = rom.read_int32(file.end - 4)
    header = file.end - header_size
    cur = header

    # read section sizes and build offsets
    section_total = 0
    for i in range(0, 4):
        section_size = rom.read_int32(cur)
        sections.append(section_total)
        section_total += section_size
        cur += 4

    # get all entries in relocation table
    relocate_count = rom.read_int32(cur)
    cur += 4
    for i in range(0, relocate_count):
        relocations.append(rom.read_int32(cur))
        cur += 4

    # create new enties
    for address in addresses:
        if isinstance(address, tuple):
            # if type provided use it
            type, address = address
        else:
            # Otherwise, try to infer type from value
            value = rom.read_int32(address)
            op = value >> 26
            type = 2 # default: data
            if op == 0x02 or op == 0x03: # j or jal
                type = 4
            elif op == 0x0F: # lui
                type = 5
            elif op == 0x08: # addi
                type = 6

        # Calculate section and offset
        address = address - file.start
        section = 0
        for section_start in sections:
            if address >= section_start:
                section += 1
            else:
                break
        offset = address - sections[section - 1]

        # generate relocation entry
        relocations.append((section << 30) 
                        | (type << 24) 
                        | (offset & 0x00FFFFFF))

    # Rebuild Relocation Table
    cur = header + 0x10
    relocations.sort(key = lambda val: val & 0xC0FFFFFF)
    rom.write_int32(cur, len(relocations))
    cur += 4
    for relocation in relocations:
        rom.write_int32(cur, relocation)
        cur += 4

    # Add padded 0?
    rom.write_int32(cur, 0)
    cur += 4

    # Update Header and File size
    new_header_size = (cur + 4) - header
    rom.write_int32(cur, new_header_size)
    file.end += (new_header_size - header_size)
