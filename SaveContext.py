class Address():
    prev_address = None

    def __init__(self, address=None, size=4, mask=0xFFFFFFFF, max=None, choices=None, value=None):
        if address is None:
            self.address = Address.prev_address
        else:
            self.address = address           
        self.value = value
        self.size = size
        self.choices = choices
        self.mask = mask

        Address.prev_address = self.address + self.size

        self.bit_offset = 0
        while mask & 1 == 0:
            mask = mask >> 1
            self.bit_offset += 1

        if max is None:
            self.max = mask
        else:
            self.max = max


    def get_value(self, default=0):
        if self.value is None:
            return default
        return self.value


    def get_writes(self, save_context):
        if self.value is None:
            return

        value = self.value
        if self.choices is not None:
            value = self.choices[value]
        if not isinstance(value, int):
            raise ValueError("Invalid value type '%s'" % str(value))

        if isinstance(value, bool):
            value = 1 if value else 0
        if value > self.max:
            value = self.max

        value = (value << self.bit_offset) & self.mask
        values = zip(Address.to_bytes(value, self.size), 
                     Address.to_bytes(self.mask, self.size))

        for i, (byte, mask) in enumerate(values):
            if mask == 0:
                continue
            if mask == 0xFF:
                save_context.write_byte(self.address + i, byte)
            else:
                save_context.write_bits(self.address + i, byte, mask=mask)


    def to_bytes(value, size):
        ret = []
        for _ in range(size):
            ret.insert(0, value & 0xFF)
            value = value >> 8
        return ret


class SaveContext():
    def __init__(self):
        self.save_bits = {}
        self.save_bytes = {}
        self.addresses = self.get_save_context_addresses()


    # will set the bits of value to the offset in the save (or'ing them with what is already there)
    def write_bits(self, address, value, mask=None, predicate=None):
        if predicate and not predicate(value):
            return

        if mask is not None:
            value = value & mask

        if address in self.save_bits:
            if mask is not None:
                self.save_bits[address] &= ~mask
            self.save_bits[address] |= value
        else:
            self.save_bits[address] = value


    # will overwrite the byte at offset with the given value
    def write_byte(self, address, value, predicate=None):
        if predicate and not predicate(value):
            return

        self.save_bytes[address] = value


    # will overwrite the byte at offset with the given value
    def write_bytes(self, address, bytes, predicate=None):
        for i, value in enumerate(bytes):
            self.write_byte(address + i, value, predicate)


    # will overwrite the byte at offset with the given value
    def write_save_table(self, rom):
        for address in self.addresses.values():
            if isinstance(address, dict):
                for sub_address in address.values():
                    sub_address.get_writes(self)
            else:
                address.get_writes(self)

        save_table = []
        for address, value in self.save_bits.items():
            if value != 0:
                save_table += [(address & 0xFF00) >> 8, address & 0xFF, 0x00, value]
        for address, value in self.save_bytes.items():
            save_table += [(address & 0xFF00) >> 8, address & 0xFF, 0x01, value]
        save_table += [0x00,0x00,0x00,0x00]

        table_len = len(save_table)
        if table_len > 0x400:
            raise Exception("The Initial Save Table has exceeded its maximum capacity: 0x%03X/0x400" % table_len)
        rom.write_bytes(rom.sym('INITIAL_SAVE_DATA'), save_table)


    def give_bottle(self, item, count):
        for bottle_id in range(4):
            bottle_slot = 'item_slot_bottle_%d' % (bottle_id + 1)
            if self.addresses[bottle_slot].get_value(0xFF) != 0xFF:
                continue

            self.addresses[bottle_slot].value = SaveContext.bottle_types[item]
            count -= 1

            if count == 0:
                return


    def give_health(self, health):
        health += self.addresses['health_capacity'].get_value(0x30) / 0x10
        health += self.addresses['heart_pieces'].get_value() / 4

        self.addresses['health_capacity'].value = int(health) * 0x10
        self.addresses['health'].value          = int(health) * 0x10
        self.addresses['heart_pieces'].value    = int((health % 1) * 4)


    def give_item(self, item, count):
        if item in SaveContext.bottle_types:
            self.give_bottle(item, count)
        elif item in ["Piece of Heart", "Piece of Heart (Treasure Chest Game)"]:
            self.give_health(count / 4)
        elif item == "Heart Container":
            self.give_health(count)
        elif item in SaveContext.save_writes_table:
            for address, value in SaveContext.save_writes_table[item].items():
                if value is None:
                    value = count
                elif isinstance(value, list):
                    value = value[min(len(value), count) - 1]
                elif isinstance(value, bool):
                    value = 1 if value else 0

                if isinstance(value, int) and value < self.addresses[address].get_value():
                    continue

                self.addresses[address].value = value
        else:
            raise ValueError("Cannot give unknown starting item %s" % item)


    def get_save_context_addresses(self):
        return {
            'entrance_index'             : Address(0x0000, size=4),
            'link_age'                   : Address(size=4, max=1),
            'unk_00'                     : Address(size=2),
            'cutscene_index'             : Address(size=2),
            'time_of_day'                : Address(size=2),
            'unk_01'                     : Address(size=2),
            'night_flag'                 : Address(size=4, max=1),
            'unk_02'                     : Address(size=8),
            'id'                         : Address(size=6),
            'deaths'                     : Address(size=2),
            'file_name'                  : Address(size=8),
            'n64dd_flag'                 : Address(size=2),
            'health_capacity'            : Address(size=2, max=0x140),
            'health'                     : Address(size=2, max=0x140),
            'magic_level'                : Address(size=1, max=2),
            'magic'                      : Address(size=1, max=0x60),
            'rupees'                     : Address(size=2),
            'bgs_hits_left'              : Address(size=2),
            'navi_timer'                 : Address(size=2),
            'magic_acquired'             : Address(size=1, max=1),
            'unk_03'                     : Address(size=1),
            'double_magic'               : Address(size=1, max=1),
            'double_defense'             : Address(size=1, max=1),
            'bgs_flag'                   : Address(size=1, max=1),
            'unk_05'                     : Address(size=1),

            # Equiped Items
            'child_button_items_b'       : Address(size=1),
            'child_button_items_left'    : Address(size=1),
            'child_button_items_down'    : Address(size=1),
            'child_button_items_right'   : Address(size=1),
            'child_button_slots_left'    : Address(size=1),
            'child_button_slots_down'    : Address(size=1),
            'child_button_slots_right'   : Address(size=1),
            'child_equips_sword'         : Address(0x0048, size=2, mask=0x000F),
            'child_equips_shield'        : Address(0x0048, size=2, mask=0x00F0),
            'child_equips_tunic'         : Address(0x0048, size=2, mask=0x0F00),
            'child_equips_boots'         : Address(0x0048, size=2, mask=0xF000),
            'adult_button_items_b'       : Address(size=1),
            'adult_button_items_left'    : Address(size=1),
            'adult_button_items_down'    : Address(size=1),
            'adult_button_items_right'   : Address(size=1),
            'adult_button_slots_left'    : Address(size=1),
            'adult_button_slots_down'    : Address(size=1),
            'adult_button_slots_right'   : Address(size=1),
            'adult_equips_sword'         : Address(0x0052, size=2, mask=0x000F),
            'adult_equips_shield'        : Address(0x0052, size=2, mask=0x00F0),
            'adult_equips_tunic'         : Address(0x0052, size=2, mask=0x0F00),
            'adult_equips_boots'         : Address(0x0052, size=2, mask=0xF000),
            'unk_06'                     : Address(size=12),
            'scene_index'                : Address(size=2),
            'button_items_b'             : Address(size=1),
            'button_items_left'          : Address(size=1),
            'button_items_down'          : Address(size=1),
            'button_items_right'         : Address(size=1),
            'button_slots_left'          : Address(size=1),
            'button_slots_down'          : Address(size=1),
            'button_slots_right'         : Address(size=1),
            'equips_sword'               : Address(0x0070, size=2, mask=0x000F),
            'equips_shield'              : Address(0x0070, size=2, mask=0x00F0),
            'equips_tunic'               : Address(0x0070, size=2, mask=0x0F00),
            'equips_boots'               : Address(0x0070, size=2, mask=0xF000),
            'unk_07'                     : Address(size=2),

            # Item Slots
            'item_slot_stick'            : Address(size=1, choices=SaveContext.item_id_map),
            'item_slot_nut'              : Address(size=1, choices=SaveContext.item_id_map),
            'item_slot_bomb'             : Address(size=1, choices=SaveContext.item_id_map),
            'item_slot_bow'              : Address(size=1, choices=SaveContext.item_id_map),
            'item_slot_fire_arrow'       : Address(size=1, choices=SaveContext.item_id_map),
            'item_slot_dins_fire'        : Address(size=1, choices=SaveContext.item_id_map),
            'item_slot_slingshot'        : Address(size=1, choices=SaveContext.item_id_map),
            'item_slot_ocarina'          : Address(size=1, choices=SaveContext.item_id_map),
            'item_slot_bombchu'          : Address(size=1, choices=SaveContext.item_id_map),
            'item_slot_hookshot'         : Address(size=1, choices=SaveContext.item_id_map),
            'item_slot_ice_arrow'        : Address(size=1, choices=SaveContext.item_id_map),
            'item_slot_farores_wind'     : Address(size=1, choices=SaveContext.item_id_map),
            'item_slot_boomerang'        : Address(size=1, choices=SaveContext.item_id_map),
            'item_slot_lens'             : Address(size=1, choices=SaveContext.item_id_map),
            'item_slot_beans'            : Address(size=1, choices=SaveContext.item_id_map),
            'item_slot_hammer'           : Address(size=1, choices=SaveContext.item_id_map),
            'item_slot_light_arrow'      : Address(size=1, choices=SaveContext.item_id_map),
            'item_slot_nayrus_love'      : Address(size=1, choices=SaveContext.item_id_map),
            'item_slot_bottle_1'         : Address(size=1, choices=SaveContext.item_id_map),
            'item_slot_bottle_2'         : Address(size=1, choices=SaveContext.item_id_map),
            'item_slot_bottle_3'         : Address(size=1, choices=SaveContext.item_id_map),
            'item_slot_bottle_4'         : Address(size=1, choices=SaveContext.item_id_map),
            'item_slot_adult_trade'      : Address(size=1, choices=SaveContext.item_id_map),
            'item_slot_child_trade'      : Address(size=1, choices=SaveContext.item_id_map),

            # Item Ammo
            'ammo_stick'                 : Address(size=1),
            'ammo_nut'                   : Address(size=1),
            'ammo_bomb'                  : Address(size=1),
            'ammo_bow'                   : Address(size=1),
            'ammo_fire_arrow'            : Address(size=1),
            'ammo_dins_fire'             : Address(size=1),
            'ammo_slingshot'             : Address(size=1),
            'ammo_ocarina'               : Address(size=1),
            'ammo_bombchu'               : Address(size=1),
            'ammo_hookshot'              : Address(size=1),
            'ammo_ice_arrow'             : Address(size=1),
            'ammo_farores_wind'          : Address(size=1),
            'ammo_boomerang'             : Address(size=1),
            'ammo_lens'                  : Address(size=1),
            'ammo_beans'                 : Address(size=1),
            'magic_beans_sold'           : Address(size=1),

            # Equipment
            'kokiri_sword'               : Address(0x009C, size=2, mask=0x0001),
            'master_sword'               : Address(0x009C, size=2, mask=0x0002),
            'giants_knife'               : Address(0x009C, size=2, mask=0x0004),
            'broken_knife'               : Address(0x009C, size=2, mask=0x0008),
            'deku_shield'                : Address(0x009C, size=2, mask=0x0010),
            'hylian_shield'              : Address(0x009C, size=2, mask=0x0020),
            'mirror_shield'              : Address(0x009C, size=2, mask=0x0040),
            'kokiri_tunic'               : Address(0x009C, size=2, mask=0x0100),
            'goron_tunic'                : Address(0x009C, size=2, mask=0x0200),
            'zora_tunic'                 : Address(0x009C, size=2, mask=0x0400),
            'kokiri_boots'               : Address(0x009C, size=2, mask=0x1000),
            'iron_boots'                 : Address(0x009C, size=2, mask=0x2000),
            'hover_boots'                : Address(0x009C, size=2, mask=0x4000),

            'unk_08'                     : Address(size=2),

            # Upgrades
            'quiver'                     : Address(0x00A0, mask=0x00000007, max=3),
            'bomb_bag'                   : Address(0x00A0, mask=0x00000038, max=3),
            'strength_upgrade'           : Address(0x00A0, mask=0x000001C0, max=3),
            'diving_upgrade'             : Address(0x00A0, mask=0x00000E00, max=2),
            'wallet'                     : Address(0x00A0, mask=0x00003000, max=3),
            'bullet_bag'                 : Address(0x00A0, mask=0x0001C000, max=3),
            'stick_upgrade'              : Address(0x00A0, mask=0x000E0000, max=3),
            'nut_upgrade'                : Address(0x00A0, mask=0x00700000, max=3),

            # Medallions
            'forest_medallion'           : Address(0x00A4, mask=0x00000001),
            'fire_medallion'             : Address(0x00A4, mask=0x00000002),
            'water_medallion'            : Address(0x00A4, mask=0x00000004),
            'spirit_medallion'           : Address(0x00A4, mask=0x00000008),
            'shadow_medallion'           : Address(0x00A4, mask=0x00000010),
            'light_medallion'            : Address(0x00A4, mask=0x00000020),

            # Songs
            'minuet_of_forest'           : Address(0x00A4, mask=0x00000040),
            'bolero_of_fire'             : Address(0x00A4, mask=0x00000080),
            'serenade_of_water'          : Address(0x00A4, mask=0x00000100),
            'requiem_of_spirit'          : Address(0x00A4, mask=0x00000200),
            'nocturne_of_shadow'         : Address(0x00A4, mask=0x00000400),
            'prelude_of_light'           : Address(0x00A4, mask=0x00000800),
            'zeldas_lullaby'             : Address(0x00A4, mask=0x00001000),
            'eponas_song'                : Address(0x00A4, mask=0x00002000),
            'sarias_song'                : Address(0x00A4, mask=0x00004000),
            'suns_song'                  : Address(0x00A4, mask=0x00008000),
            'song_of_time'               : Address(0x00A4, mask=0x00010000),
            'song_of_storms'             : Address(0x00A4, mask=0x00020000),

            # Spiritual Stones
            'kokiris_emerald'            : Address(0x00A4, mask=0x00040000),
            'gorons_ruby'                : Address(0x00A4, mask=0x00080000),
            'zoras_sapphire'             : Address(0x00A4, mask=0x00100000),

            # Misc Quest
            'stone_of_agony'             : Address(0x00A4, mask=0x00200000),
            'gerudos_card'               : Address(0x00A4, mask=0x00400000),
            'gold_skulltula'             : Address(0x00A4, mask=0x00800000),
            'heart_pieces'               : Address(0x00A4, mask=0xFF000000),

            # Dungeon Items
            'deku_boss_key'              : Address(0x00A8, size=1, mask=0x01),
            'deku_compass'               : Address(0x00A8, size=1, mask=0x02),
            'deku_map'                   : Address(0x00A8, size=1, mask=0x04),
            'dodongo_boss_key'           : Address(0x00A9, size=1, mask=0x01),
            'dodongo_compass'            : Address(0x00A9, size=1, mask=0x02),
            'dodongo_map'                : Address(0x00A9, size=1, mask=0x04),
            'jabu_boss_key'              : Address(0x00AA, size=1, mask=0x01),
            'jabu_compass'               : Address(0x00AA, size=1, mask=0x02),
            'jabu_map'                   : Address(0x00AA, size=1, mask=0x04),
            'forest_boss_key'            : Address(0x00AB, size=1, mask=0x01),
            'forest_compass'             : Address(0x00AB, size=1, mask=0x02),
            'forest_map'                 : Address(0x00AB, size=1, mask=0x04),
            'fire_boss_key'              : Address(0x00AC, size=1, mask=0x01),
            'fire_compass'               : Address(0x00AC, size=1, mask=0x02),
            'fire_map'                   : Address(0x00AC, size=1, mask=0x04),
            'water_boss_key'             : Address(0x00AD, size=1, mask=0x01),
            'water_compass'              : Address(0x00AD, size=1, mask=0x02),
            'water_map'                  : Address(0x00AD, size=1, mask=0x04),
            'spirit_boss_key'            : Address(0x00AE, size=1, mask=0x01),
            'spirit_compass'             : Address(0x00AE, size=1, mask=0x02),
            'spirit_map'                 : Address(0x00AE, size=1, mask=0x04),
            'shadow_boss_key'            : Address(0x00AF, size=1, mask=0x01),
            'shadow_compass'             : Address(0x00AF, size=1, mask=0x02),
            'shadow_map'                 : Address(0x00AF, size=1, mask=0x04),
            'botw_boss_key'              : Address(0x00B0, size=1, mask=0x01),
            'botw_compass'               : Address(0x00B0, size=1, mask=0x02),
            'botw_map'                   : Address(0x00B0, size=1, mask=0x04),
            'ice_boss_key'               : Address(0x00B1, size=1, mask=0x01),
            'ice_compass'                : Address(0x00B1, size=1, mask=0x02),
            'ice_map'                    : Address(0x00B1, size=1, mask=0x04),
            'gt_boss_key'                : Address(0x00B2, size=1, mask=0x01),
            'gt_compass'                 : Address(0x00B2, size=1, mask=0x02),
            'gt_map'                     : Address(0x00B2, size=1, mask=0x04),
            'gtg_boss_key'               : Address(0x00B3, size=1, mask=0x01),
            'gtg_compass'                : Address(0x00B3, size=1, mask=0x02),
            'gtg_map'                    : Address(0x00B3, size=1, mask=0x04),
            'fortress_boss_key'          : Address(0x00B4, size=1, mask=0x01),
            'fortress_compass'           : Address(0x00B4, size=1, mask=0x02),
            'fortress_map'               : Address(0x00B4, size=1, mask=0x04),
            'gc_boss_key'                : Address(0x00B5, size=1, mask=0x01),
            'gc_compass'                 : Address(0x00B5, size=1, mask=0x02),
            'gc_map'                     : Address(0x00B5, size=1, mask=0x04),
            'deku_keys'                  : Address(0x00BC, size=1),
            'dodongo_keys'               : Address(size=1),
            'jabu_keys'                  : Address(size=1),
            'forest_keys'                : Address(size=1),
            'fire_keys'                  : Address(size=1),
            'water_keys'                 : Address(size=1),
            'spirit_keys'                : Address(size=1),
            'shadow_keys'                : Address(size=1),
            'botw_keys'                  : Address(size=1),
            'ice_keys'                   : Address(size=1),
            'gt_keys'                    : Address(size=1),
            'gtg_keys'                   : Address(size=1),
            'fortress_keys'              : Address(size=1),
            'gc_keys'                    : Address(size=1),

            'defense_hearts'             : Address(0x00CF, size=1, max=20),
            'gs_tokens'                  : Address(size=2, max=100),
        }


    item_id_map = {
        'none'                : 0xFF,
        'stick'               : 0x00,
        'nut'                 : 0x01,
        'bomb'                : 0x02,
        'bow'                 : 0x03,
        'fire_arrow'          : 0x04,
        'dins_fire'           : 0x05,
        'slingshot'           : 0x06,
        'fairy_ocarina'       : 0x07,
        'ocarina_of_time'     : 0x08,
        'bombchu'             : 0x09,
        'hookshot'            : 0x0A,
        'longshot'            : 0x0B,
        'ice_arrow'           : 0x0C,
        'farores_wind'        : 0x0D,
        'boomerang'           : 0x0E,
        'lens'                : 0x0F,
        'beans'               : 0x10,
        'hammer'              : 0x11,
        'light_arrow'         : 0x12,
        'nayrus_love'         : 0x13,
        'bottle'              : 0x14,
        'red_potion'          : 0x15,
        'green_potion'        : 0x16,
        'blue_potion'         : 0x17,
        'fairy'               : 0x18,
        'fish'                : 0x19,
        'milk'                : 0x1A,
        'letter'              : 0x1B,
        'blue_fire'           : 0x1C,
        'bug'                 : 0x1D,
        'big_poe'             : 0x1E,
        'half_milk'           : 0x1F,
        'poe'                 : 0x20,
        'weird_egg'           : 0x21,
        'chicken'             : 0x22,
        'zeldas_letter'       : 0x23,
        'keaton_mask'         : 0x24,
        'skull_mask'          : 0x25,
        'spooky_mask'         : 0x26,
        'bunny_hood'          : 0x27,
        'goron_mask'          : 0x28,
        'zora_mask'           : 0x29,
        'gerudo_mask'         : 0x2A,
        'mask_of_truth'       : 0x2B,
        'sold_out'            : 0x2C,
        'pocket_egg'          : 0x2D,
        'pocket_cucco'        : 0x2E,
        'cojiro'              : 0x2F,
        'odd_mushroom'        : 0x30,
        'odd_potion'          : 0x31,
        'poachers_saw'        : 0x32,
        'broken_gorons_sword' : 0x33,
        'prescription'        : 0x34,
        'eyeball_frog'        : 0x35,
        'eye_drops'           : 0x36,
        'claim_check'         : 0x37,
    }


    bottle_types = {
        "Bottle"                   : 'bottle',
        "Bottle with Red Potion"   : 'red_potion',
        "Bottle with Green Potion" : 'green_potion',
        "Bottle with Blue Potion"  : 'blue_potion',
        "Bottle with Fairy"        : 'fairy',
        "Bottle with Fish"         : 'fish',
        "Bottle with Milk"         : 'milk',
        "Bottle with Letter"       : 'letter',
        "Bottle with Blue Fire"    : 'blue_fire',
        "Bottle with Bugs"         : 'bug',
        "Bottle with Big Poe"      : 'big_poe',
        "Bottle with Milk (Half)"  : 'half_milk',
        "Bottle with Poe"          : 'poe',    
    }


    save_writes_table = {
        "Deku Stick Capacity": {
            'item_slot_stick'                       : 'stick',
            'stick_upgrade'                         : [2,3],
        },
        "Deku Sticks": {
            'item_slot_stick'                       : 'stick',
            'stick_upgrade'                         : 1,
            'ammo_stick'                            : None,
        },
        "Deku Nut Capacity": {
            'item_slot_nut'                         : 'nut',
            'nut_upgrade'                           : [2,3],
        },
        "Deku Nuts": {
            'item_slot_nut'                         : 'nut',
            'nut_upgrade'                           : 1,
            'ammo_nut'                              : None,
        },
        "Bomb Bag": {
            'item_slot_bomb'                        : 'bomb',
            'bomb_bag'                              : None,
        },
        "Bombs" : {
            'ammo_bomb'                             : None,
        },
        "Bombchus" : {
            'item_slot_bombchu'                     : 'bombchu',
            'ammo_bombchu'                          : None,
        },
        "Bow" : {
            'item_slot_bow'                         : 'bow',
            'quiver'                                : None,
        },
        "Arrows" : {
            'ammo_bow'                              : None,
        },
        "Slingshot"    : {
            'item_slot_slingshot'                   : 'slingshot',
            'bullet_bag'                            : None,
        },
        "Deku Seeds" : {
            'ammo_slingshot'                        : None,
        },
        "Magic Bean" : {
            'item_slot_beans'                       : 'beans',
            'ammo_beans'                            : None,
            'magic_beans_sold'                      : None,
        },
        "Fire Arrows"    : {'item_slot_fire_arrow'  : 'fire_arrow'},
        "Ice Arrows"     : {'item_slot_ice_arrow'   : 'ice_arrow'},
        "Light Arrows"   : {'item_slot_light_arrow' : 'light_arrow'},
        "Dins Fire"      : {'item_slot_dins_fire'   : 'dins_fire'},
        "Farores Wind"   : {'item_slot_farores_wind': 'farores_wind'},
        "Nayrus Love"    : {'item_slot_nayrus_love' : 'nayrus_love'},
        "Ocarina"        : {'item_slot_ocarina'     : ['fairy_ocarina', 'ocarina_of_time']},
        "Progressive Hookshot" : {'item_slot_hookshot' : ['hookshot', 'longshot']},
        "Boomerang"      : {'item_slot_boomerang'   : 'boomerang'},
        "Lens of Truth"  : {'item_slot_lens'        : 'lens'},
        "Hammer"         : {'item_slot_hammer'      : 'hammer'},
        "Pocket Egg"     : {'item_slot_adult_trade' : 'pocket_egg'},
        "Pocket Cucco"   : {'item_slot_adult_trade' : 'pocket_cucco'},
        "Cojiro"         : {'item_slot_adult_trade' : 'cojiro'},
        "Odd Mushroom"   : {'item_slot_adult_trade' : 'odd_mushroom'},
        "Poachers Saw"   : {'item_slot_adult_trade' : 'poachers_saw'},
        "Broken Sword"   : {'item_slot_adult_trade' : 'broken_knife'},
        "Prescription"   : {'item_slot_adult_trade' : 'prescription'},
        "Eyeball Frog"   : {'item_slot_adult_trade' : 'eyeball_frog'},
        "Eyedrops"       : {'item_slot_adult_trade' : 'eye_drops'},
        "Claim Check"    : {'item_slot_adult_trade' : 'claim_check'},
        "Weird Egg"      : {'item_slot_child_trade' : 'weird_egg'},
        "Chicken"        : {'item_slot_child_trade' : 'chicken'},
        "Goron Tunic"    : {'goron_tunic'           : True},
        "Zora Tunic"     : {'zora_tunic'            : True},
        "Iron Boots"     : {'iron_boots'            : True},
        "Hover Boots"    : {'hover_boots'           : True},
        "Deku Shield"    : {'deku_shield'           : True},
        "Hylian Shield"  : {'hylian_shield'         : True},
        "Mirror Shield"  : {'mirror_shield'         : True},
        "Kokiri Sword"   : {'kokiri_sword'          : True},
        "Biggoron Sword" : {
            'giants_knife'          : True,
            'bgs_flag'              : True,
        },
        "Gerudo Membership Card" : {'gerudos_card'  : True},
        "Stone of Agony" : {'stone_of_agony'        : True},
        "Zeldas Lullaby" : {'zeldas_lullaby'        : True},
        "Eponas Song"    : {'eponas_song'           : True},
        "Sarias Song"    : {'sarias_song'           : True},
        "Suns Song"      : {'suns_song'             : True},
        "Song of Time"   : {'song_of_time'          : True},
        "Song of Storms" : {'song_of_storms'        : True},
        "Minuet of Forest" : {'minuet_of_forest'    : True},
        "Bolero of Fire" : {'bolero_of_fire'        : True},
        "Serenade of Water" : {'serenade_of_water'  : True},
        "Requiem of Spirit" : {'requiem_of_spirit'  : True},
        "Nocturne of Shadow" : {'nocturne_of_shadow': True},
        "Prelude of Light" : {'prelude_of_light'    : True},
        "Kokiri Emerald"   : {'kokiris_emerald'     : True},
        "Goron Ruby"       : {'gorons_ruby'         : True},
        "Zora Sapphire"    : {'zoras_sapphire'      : True},
        "Light Medallion"  : {'light_medallion'     : True},
        "Forest Medallion" : {'forest_medallion'    : True},
        "Fire Medallion"   : {'fire_medallion'      : True},
        "Water Medallion"  : {'water_medallion'     : True},
        "Spirit Medallion" : {'spirit_medallion'    : True},
        "Shadow Medallion" : {'shadow_medallion'    : True},
        "Progressive Strength Upgrade" : {'strength_upgrade' : None},
        "Progressive Scale" : {'diving_upgrade'     : None},
        "Progressive Wallet" : {'wallet'            : None},
        "Gold Skulltula Token" : {
            'gold_skulltula'                        : True,
            'gs_tokens'                             : None,
        },
        "Double Defense" : {
            'double_defense'                        : True,
            'defense_hearts'                        : 20,
        },
        "Magic Meter" : {
            'magic_acquired'                        : True,
            'magic'                                 : [0x30, 0x60],
            'magic_level'                           : None,
            'double_magic'                          : [False, True],
        },
        "Rupees"          : {'rupees'               : None},
    }
