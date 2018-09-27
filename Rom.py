import io
import json
import logging
import os
import platform
import struct
import subprocess
import random
import copy

from Utils import local_path, default_output_path

DMADATA_START = 0x7430

class LocalRom(object):
    def __init__(self, settings, patch=True):
        self.last_address = None

        file = settings.rom
        decomp_file = 'ZOOTDEC.z64'

        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        #os.chdir(output_path(os.path.dirname(os.path.realpath(__file__))))

        with open(local_path('data/symbols.json'), 'r') as stream:
            symbols = json.load(stream)
            self.symbols = { name: int(addr, 16) for name, addr in symbols.items() }

        try:
            # Read decompressed file if it exists
            self.read_rom(decomp_file)
            # This is mainly for validation testing, but just in case...
            self.decompress_rom_file(decomp_file, decomp_file)
        except Exception as ex:
            # No decompressed file, instead read Input ROM
            self.read_rom(file)
            self.decompress_rom_file(file, decomp_file)

        # Add file to maximum size
        self.buffer.extend(bytearray([0x00] * (0x4000000 - len(self.buffer))))

    def decompress_rom_file(self, file, decomp_file):
        validCRC = [
            [0xEC, 0x70, 0x11, 0xB7, 0x76, 0x16, 0xD7, 0x2B], # Compressed
            [0x70, 0xEC, 0xB7, 0x11, 0x16, 0x76, 0x2B, 0xD7], # Byteswap compressed
            [0x93, 0x52, 0x2E, 0x7B, 0xE5, 0x06, 0xD4, 0x27], # Decompressed
        ]

        # Validate ROM file
        file_name = os.path.splitext(file)
        romCRC = list(self.buffer[0x10:0x18])
        if romCRC not in validCRC:
            # Bad CRC validation
            raise RuntimeError('ROM file %s is not a valid OoT 1.0 US ROM.' % file)
        elif len(self.buffer) < 0x2000000 or len(self.buffer) > (0x4000000) or file_name[1] not in ['.z64', '.n64']:
            # ROM is too big, or too small, or not a bad type
            raise RuntimeError('ROM file %s is not a valid OoT 1.0 US ROM.' % file)
        elif len(self.buffer) == 0x2000000:
            # If Input ROM is compressed, then Decompress it
            subcall = []

            if platform.system() == 'Windows':
                if 8 * struct.calcsize("P") == 64:
                    subcall = ["Decompress\\Decompress.exe", file, decomp_file]
                else:
                    subcall = ["Decompress\\Decompress32.exe", file, decomp_file]
            elif platform.system() == 'Linux':
                subcall = ["Decompress/Decompress", file, decomp_file]
            elif platform.system() == 'Darwin':
                subcall = ["Decompress/Decompress.out", file, decomp_file]
            else:
                raise RuntimeError('Unsupported operating system for decompression. Please supply an already decompressed ROM.')

            subprocess.call(subcall)
            self.read_rom(decomp_file)
        else:
            # ROM file is a valid and already uncompressed
            pass

    def sym(self, symbol_name):
        return self.symbols.get(symbol_name)

    def seek_address(self, address):
        self.last_address = address

    def read_byte(self, address):
        self.last_address = address + 1
        return self.buffer[address]

    def read_bytes(self, address, len):
        self.last_address = address + len
        return self.buffer[address : address + len]

    def read_int16(self, address):
        return bytes_as_int16(self.read_bytes(address, 2))

    def read_int24(self, address):
        return bytes_as_int24(self.read_bytes(address, 3))

    def read_int32(self, address):
        return bytes_as_int32(self.read_bytes(address, 4))

    def write_byte(self, address, value):
        if address == None:
            address = self.last_address
        self.buffer[address] = value
        self.last_address = address + 1

    def write_sbyte(self, address, value):
        if address == None:
            address = self.last_address
        self.write_bytes(address, struct.pack('b', value))

    def write_int16(self, address, value):
        if address == None:
            address = self.last_address
        self.write_bytes(address, int16_as_bytes(value))

    def write_int24(self, address, value):
        if address == None:
            address = self.last_address
        self.write_bytes(address, int24_as_bytes(value))

    def write_int32(self, address, value):
        if address == None:
            address = self.last_address
        self.write_bytes(address, int32_as_bytes(value))

    def write_f32(self, address, value:float):
        if address == None:
            address = self.last_address
        self.write_bytes(address, struct.pack('>f', value))

    def write_bytes(self, startaddress, values):
        if startaddress == None:
            startaddress = self.last_address
        for i, value in enumerate(values):
            self.write_byte(startaddress + i, value)

    def write_int16s(self, startaddress, values):
        if startaddress == None:
            startaddress = self.last_address
        for i, value in enumerate(values):
            self.write_int16(startaddress + (i * 2), value)

    def write_int24s(self, startaddress, values):
        if startaddress == None:
            startaddress = self.last_address
        for i, value in enumerate(values):
            self.write_int24(startaddress + (i * 3), value)

    def write_int32s(self, startaddress, values):
        if startaddress == None:
            startaddress = self.last_address
        for i, value in enumerate(values):
            self.write_int32(startaddress + (i * 4), value)

    def write_to_file(self, file):
        self.verify_dmadata()
        self.update_crc()
        with open(file, 'wb') as outfile:
            outfile.write(self.buffer)

    def update_crc(self):
        t1 = t2 = t3 = t4 = t5 = t6 = 0xDF26F436
        u32 = 0xFFFFFFFF

        cur = 0x1000
        while cur < 0x00101000:
            d = self.read_int32(cur)

            if ((t6 + d) & u32) < t6:
                t4 += 1 

            t6 = (t6+d) & u32
            t3 ^= d
            shift = d & 0x1F
            r = ((d << shift) | (d >> (32 - shift))) & u32
            t5 = (t5 + r) & u32

            if t2 > d:
                t2 ^= r
            else:
                t2 ^= t6 ^ d

            data2 = self.read_int32(0x750 + (cur & 0xFF))
            t1 += data2 ^ d
            t1 &= u32

            cur += 4

        crc0 = t6 ^ t4 ^ t3
        crc1 = t5 ^ t2 ^ t1

        # Finally write the crc back to the rom
        self.write_int32s(0x10, [crc0, crc1])


    def read_rom(self, file):
        # "Reads rom into bytearray"
        with open(file, 'rb') as stream:
            self.buffer = bytearray(stream.read())

    # dmadata/file management helper functions

    def _get_dmadata_record(rom, cur):
        start = rom.read_int32(cur)
        end = rom.read_int32(cur+0x04)
        size = end-start
        return start, end, size


    def verify_dmadata(rom):
        cur = DMADATA_START
        overlapping_records = []
        dma_data = []
    
        while True:
            this_start, this_end, this_size = rom._get_dmadata_record(cur)

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
        

    def update_dmadata_record(rom, key, start, end):
        cur = DMADATA_START
        dma_start, dma_end, dma_size = rom._get_dmadata_record(cur)
        while dma_start != key:
            if dma_start == 0 and dma_end == 0:
                break

            cur += 0x10
            dma_start, dma_end, dma_size = rom._get_dmadata_record(cur)

        if dma_start == 0:
            raise Exception('dmadata update failed: key {0:x} not found in dmadata'.format(key))

        else:
            rom.write_int32s(cur, [start, end, start, 0])


def int16_as_bytes(value):
    value = value & 0xFFFF
    return [(value >> 8) & 0xFF, value & 0xFF]

def int24_as_bytes(value):
    value = value & 0xFFFFFF
    return [(value >> 16) & 0xFF, (value >> 8) & 0xFF, value & 0xFF]

def int32_as_bytes(value):
    value = value & 0xFFFFFFFF
    return [(value >> 24) & 0xFF, (value >> 16) & 0xFF, (value >> 8) & 0xFF, value & 0xFF]

def bytes_as_int16(values):
    return (values[0] << 8) | values[1]

def bytes_as_int24(values):
    return (values[0] << 16) | (values[1] << 8) | values[2]

def bytes_as_int32(values):
    return (values[0] << 24) | (values[1] << 16) | (values[2] << 8) | values[3]
