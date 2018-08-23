import io
import json
import logging
import os
import platform
import struct
import subprocess
import random
import copy

from Utils import default_output_path

class LocalRom(object):

    def __init__(self, settings, patch=True):
        self.last_address = None

        file = settings.rom
        decomp_file = os.path.join(default_output_path(settings.output_dir), 'ZOOTDEC.z64')

        validCRC = []
        validCRC.append(bytearray([0xEC, 0x70, 0x11, 0xB7, 0x76, 0x16, 0xD7, 0x2B])) # Compressed
        validCRC.append(bytearray([0x70, 0xEC, 0xB7, 0x11, 0x16, 0x76, 0x2B, 0xD7])) # Byteswap compressed
        validCRC.append(bytearray([0x93, 0x52, 0x2E, 0x7B, 0xE5, 0x06, 0xD4, 0x27])) # Decompressed

        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        #os.chdir(output_path(os.path.dirname(os.path.realpath(__file__))))
        with open(file, 'rb') as stream:
            self.buffer = read_rom(stream)
        file_name = os.path.splitext(file)
        romCRC = self.buffer[0x10:0x18]
        if romCRC not in validCRC:
            raise RuntimeError('ROM is not a valid OoT 1.0 US ROM.')
        if len(self.buffer) < 0x2000000 or len(self.buffer) > (0x4000000) or file_name[1] not in ['.z64', '.n64']:
            raise RuntimeError('ROM is not a valid OoT 1.0 ROM.')
        if len(self.buffer) == 0x2000000:
            if platform.system() == 'Windows':
                subprocess.call(["Decompress\\Decompress.exe", file, decomp_file])
                with open(decomp_file, 'rb') as stream:
                    self.buffer = read_rom(stream)
            elif platform.system() == 'Linux':
                subprocess.call(["Decompress/Decompress", file])
                with open(("ZOOTDEC.z64"), 'rb') as stream:
                    self.buffer = read_rom(stream)
            elif platform.system() == 'Darwin':
                subprocess.call(["Decompress/Decompress.out", file])
                with open(("ZOOTDEC.z64"), 'rb') as stream:
                    self.buffer = read_rom(stream)
            else:
                raise RuntimeError('Unsupported operating system for decompression. Please supply an already decompressed ROM.')
        # extend to 64MB
        self.buffer.extend(bytearray([0x00] * (0x4000000 - len(self.buffer))))
            
    def read_byte(self, address):
        return self.buffer[address]

    def read_bytes(self, address, len):
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
        with open(file, 'wb') as outfile:
            outfile.write(self.buffer)

def read_rom(stream):
    "Reads rom into bytearray"
    buffer = bytearray(stream.read())
    return buffer


def int16_as_bytes(value):
    value = value & 0xFFFF
    return [(value >> 8) & 0xFF, value & 0xFF]

def int24_as_bytes(value):
    value = value & 0xFFFFFFFF
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