from collections import Counter, defaultdict
import copy
import itertools

from Item import ItemInfo
from Playthrough import Playthrough
from Region import Region, TimeOfDay



class State(object):

    def __init__(self, parent):
        self.prog_items = Counter()
        self.world = parent
        self.playthrough = None


    ## Ensure that this will always have a value
    @property
    def is_glitched(self):
        return self.world.logic_rules != 'glitchless'


    def copy(self, new_world=None):
        if not new_world:
            new_world = self.world
        new_state = State(new_world)
        new_state.prog_items = copy.copy(self.prog_items)
        return new_state


    def item_name(self, location):
        location = self.world.get_location(location)
        if location.item is None:
            return None
        return location.item.name


    def has(self, item, count=1):
        return self.prog_items[item] >= count


    def has_any_of(self, items):
        return any(map(self.prog_items.__contains__, items))


    def has_all_of(self, items):
        return all(map(self.prog_items.__contains__, items))


    def item_count(self, item):
        return self.prog_items[item]


    def can_child_attack(self, age=None):
        return  age == 'child' and \
                   (self.has_slingshot() or \
                    self.has('Boomerang') or \
                    self.has_sticks() or \
                    self.has_explosives() or \
                    self.has('Kokiri Sword') or \
                    self.can_use('Dins Fire'))

    def can_child_damage(self, age=None):
        return  age == 'child' and \
                   (self.has_slingshot() or \
                    self.has_sticks() or \
                    self.has_explosives() or \
                    self.has('Kokiri Sword') or \
                    self.can_use('Dins Fire'))


    def can_stun_deku(self, age=None):
        return  age == 'adult' or \
                self.can_child_attack(age=age) or \
                self.has_nuts() or \
                self.can_use('Deku Shield', age=age)


    def has_nuts(self):
        return self.has_any_of(('Buy Deku Nut (5)', 'Buy Deku Nut (10)', 'Deku Nut Drop'))


    def has_sticks(self):
        return self.has_any_of(('Buy Deku Stick (1)', 'Deku Stick Drop'))


    def has_bow(self):
        return self.has('Bow')


    def has_slingshot(self):
        return self.has('Slingshot')


    def has_bombs(self):
        return self.has('Bomb Bag')


    def has_ocarina(self):
        return self.has_any_of(('Ocarina', 'Fairy Ocarina', 'Ocarina of Time'))


    def can_plant_bean(self, age=None):
        return age == 'child' and self.has_any_of(('Magic Bean', 'Magic Bean Pack'))


    def can_play(self, song):
        return self.has_ocarina() and self.has(song)


    def can_use(self, item, age=None):
        magic_items = ['Dins Fire', 'Farores Wind', 'Nayrus Love', 'Lens of Truth']
        adult_items = ['Bow', 'Hammer', 'Iron Boots', 'Hover Boots']
        adult_buy_or_find = ['Goron Tunic', 'Zora Tunic']
        child_items = ['Slingshot', 'Boomerang', 'Kokiri Sword']
        magic_arrows = ['Fire Arrows', 'Light Arrows']
        if item in magic_items:
            return self.has_all_of((item, 'Magic Meter'))
        elif item in child_items:
            return age == 'child' and self.has(item)
        elif item in adult_buy_or_find:
            return age == 'adult' and self.has_any_of((item, 'Buy ' + item))
        elif item in adult_items:
            return age == 'adult' and self.has(item)
        elif item in magic_arrows:
            return age == 'adult' and self.has_all_of((item, 'Bow', 'Magic Meter'))
        elif item == 'Sticks':
            return age == 'child' and self.has_sticks()
        elif item == 'Deku Shield':
            return age == 'child' and self.has('Buy Deku Shield')
        elif item == 'Hookshot':
            return age == 'adult' and self.has('Progressive Hookshot')
        elif item == 'Longshot':
            return age == 'adult' and self.has('Progressive Hookshot', 2)
        elif item == 'Silver Gauntlets':
            return age == 'adult' and self.has('Progressive Strength Upgrade', 2)
        elif item == 'Golden Gauntlets':
            return age == 'adult' and self.has('Progressive Strength Upgrade', 3)
        elif item == 'Epona':
            # Glitched can steal Epona by hovering over the LLR fences instead of using Epona's Song
            return age == 'adult' and self.has('Epona') and (self.can_play('Eponas Song') or (self.is_glitched and self.can_hover()))
        elif item == 'Scarecrow':
            return age == 'adult' and self.has('Progressive Hookshot') and self.can_play('Scarecrow Song')
        elif item == 'Distant Scarecrow':
            return age == 'adult' and self.has('Progressive Hookshot', 2) and self.can_play('Scarecrow Song')
        else:
            return self.has(item)


    def can_buy_bombchus(self):
        return self.has_any_of(('Buy Bombchu (5)', 'Buy Bombchu (10)', 'Buy Bombchu (20)', 'Bombchu Drop'))


    def has_bombchus(self):
        return self.can_buy_bombchus() and (self.world.bombchus_in_logic or self.has('Bomb Bag'))


    def has_bombchus_item(self):
        if self.world.bombchus_in_logic:
            return self.has_any_of(('Bombchus', 'Bombchus (5)', 'Bombchus (10)', 'Bombchus (20)'))
        else:
            return self.has('Bomb Bag')


    def has_explosives(self):
        return self.has_bombs() or (self.world.bombchus_in_logic and self.has_bombchus())


    def can_blast_or_smash(self, age=None):
        return self.has_explosives() or self.can_use('Hammer', age=age)


    def can_dive(self):
        return self.has('Progressive Scale')


    def can_see_with_lens(self):
        return self.world.logic_lens != 'all' or self.has_all_of(('Magic Meter', 'Lens of Truth'))


    def can_cut_shrubs(self, age=None):
        return age == 'adult' or self.has_sticks() or \
               self.has_any_of(('Kokiri Sword', 'Boomerang')) or \
               self.has_explosives()


    def can_summon_gossip_fairy(self):
        return self.has_ocarina() and self.has_any_of(('Zeldas Lullaby', 'Eponas Song', 'Song of Time', 'Suns Song'))


    def can_summon_gossip_fairy_without_suns(self):
        return self.has_ocarina() and self.has_any_of(('Zeldas Lullaby', 'Eponas Song', 'Song of Time'))


    def can_plant_bugs(self, age=None):
        return age == 'child' and self.has_bugs()


    def has_bugs(self):
        return self.has_any_of(('Bugs', 'Buy Bottle Bug'))


    def has_blue_fire(self):
        return self.has_any_of(('Blue Fire', 'Buy Blue Fire'))


    def has_fish(self):
        return self.has_any_of(('Fish', 'Buy Fish'))


    def has_fairy(self):
        return self.has_any_of(('Fairy', 'Buy Fairy\'s Spirit'))


    def has_big_poe_drop(self):
        return self.has('Big Poe')


    def can_use_projectile(self, age=None):
        if self.has_explosives():
            return True
        if age == 'adult':
            return self.has_any_of(('Bow', 'Progressive Hookshot'))
        else:
            return age == 'child' and self.has_any_of(('Slingshot', 'Boomerang'))


    def has_projectile(self, for_age='either'):
        if self.has_explosives():
            return True
        if for_age == 'child':
            return self.has_any_of(('Slingshot', 'Boomerang'))
        elif for_age == 'adult':
            return self.has_any_of(('Bow', 'Progressive Hookshot'))
        elif for_age == 'both':
            return (self.has_any_of(('Bow', 'Progressive Hookshot'))
                    and self.has_any_of(('Slingshot', 'Boomerang')))
        else:
            return self.has_any_of(('Bow', 'Progressive Hookshot', 'Slingshot', 'Boomerang'))


    def can_leave_forest(self, age=None):
        return self.world.open_forest != 'closed' or age == 'adult' or self.is_glitched or self.has('Deku Tree Clear')


    def guarantee_trade_path(self, age=None):
        if self.world.shuffle_interior_entrances or self.world.shuffle_overworld_entrances:
            # Timers are disabled and items don't revert on save warp in those ER settings
            return True
        else:
            return (
                # Check necessary items for the paths to Biggoron that fit the timer
                self.world.logic_biggoron_bolero
                # Getting to Biggoron without ER or the trick above involves either
                # Darunia's Chamber access or clearing the boulders to get up DMT
                or self.can_blast_or_smash(age=age)
                or self.has('Stop Link the Goron')
            )


    def has_bottle(self):
        # Extra Ruto's Letter are automatically emptied
        return self.has_any_of(ItemInfo.bottles) or self.has('Bottle with Letter', 2)


    def has_hearts(self, count):
        # Warning: This only considers items that are marked as advancement items
        return self.heart_count() >= count


    def has_shield(self, age=None):
        #The mirror shield does not count as it cannot reflect deku scrub attack
        if age == 'adult':
            return self.has('Buy Hylian Shield')
        else:
            return age == 'child' and self.has('Buy Deku Shield')


    def heart_count(self):
        # Warning: This only considers items that are marked as advancement items
        return (
            self.item_count('Heart Container')
            + self.item_count('Piece of Heart') // 4
            + 3 # starting hearts
        )


    def has_fire_source(self, age=None):
        return self.can_use('Dins Fire') or self.can_use('Fire Arrows', age=age)


    def has_fire_source_with_torch(self, age=None):
        return self.has_fire_source() or (age == 'child' and self.has_sticks())


    def guarantee_hint(self):
        if self.world.hints == 'mask':
            # has the mask of truth
            return self.has('Mask of Truth')
        elif self.world.hints == 'agony':
            # has the Stone of Agony
            return self.has('Stone of Agony')
        return True


    def had_night_start(self):
        stod = self.world.starting_tod
        # These are all not between 6:30 and 18:00
        if (stod == 'sunset' or         # 18
            stod == 'evening' or        # 21
            stod == 'midnight' or       # 00
            stod == 'witching-hour'):   # 03
            return True
        else:
            return False


    def can_finish_GerudoFortress(self, age=None):
        if self.world.gerudo_fortress == 'normal':
            return (self.has('Small Key (Gerudo Fortress)', 4) and
                    (age == 'adult' or self.has('Kokiri Sword') or self.is_glitched) and
                    (self.can_use('Bow', age=age)
                        or self.can_use('Hookshot', age=age)
                        or self.can_use('Hover Boots', age=age)
                        or self.has('Gerudo Membership Card')
                        or self.world.logic_gerudo_kitchen
                        or self.is_glitched))
        elif self.world.gerudo_fortress == 'fast':
            return (self.has('Small Key (Gerudo Fortress)', 1) and
                    (age == 'adult' or self.has('Kokiri Sword') or self.is_glitched))
        else:
            return True


    def can_shield(self, age=None):
        if age == 'adult':
            return self.has_any_of(('Buy Hylian Shield', 'Mirror Shield'))
        else:
            return age == 'child' and self.has('Buy Deku Shield')


    def can_mega(self, age=None):
        return self.has_explosives() and self.can_shield(age=age)


    def can_isg(self, age=None):
        return self.can_shield(age=age) and (age == 'adult' or self.has_sticks() or self.has('Kokiri Sword'))


    def can_hover(self, age=None):
        return self.can_mega(age=age) and self.can_isg(age=age)


    def can_weirdshot(self, age=None):
        return self.can_mega(age=age) and self.can_use('Hookshot', age=age)


    def can_jumpslash(self, age=None):
        return age == 'adult' or (age == 'child' and (self.has_sticks or self.has('Kokiri Sword')))


    # Used for fall damage and other situations where damage is unavoidable
    def can_live_dmg(self, hearts):
        mult = self.world.damage_multiplier
        if hearts*4 >= 3:
            return mult != 'ohko' and mult != 'quadruple'
        elif hearts*4 < 3:
            return mult != 'ohko'
        else:
            return True


    def has_all_stones(self):
        return self.has_all_of(('Kokiri Emerald', 'Goron Ruby', 'Zora Sapphire'))


    def has_all_medallions(self):
        return self.has_all_of(('Forest Medallion', 'Fire Medallion', 'Water Medallion', 
                                'Shadow Medallion', 'Spirit Medallion', 'Light Medallion'))


    def can_build_rainbow_bridge(self):
        if self.world.bridge == 'open':
            return True
        if self.world.bridge == 'vanilla':
            return self.has_all_of(('Shadow Medallion', 'Spirit Medallion', 'Light Arrows'))
        if self.world.bridge == 'stones':
            return self.has_all_stones()
        if self.world.bridge == 'medallions':
            return self.has_all_medallions()
        if self.world.bridge == 'dungeons':
            return self.has_all_stones() and self.has_all_medallions()
        if self.world.bridge == 'tokens':
            return self.has('Gold Skulltula Token', 100)
        raise Exception ('Unknown Rainbow Bridge Logic')


    def can_trigger_lacs(self):
        if self.world.lacs_condition == 'vanilla':
            return self.has_all_of(('Shadow Medallion', 'Spirit Medallion'))
        if self.world.lacs_condition == 'stones':
            return self.has_all_stones()
        if self.world.lacs_condition == 'medallions':
            return self.has_all_medallions()
        if self.world.lacs_condition == 'dungeons':
            return self.has_all_stones() and self.has_all_medallions()
        raise Exception ('Unknown Light Arrow Cutscene Logic')


    # Be careful using this function. It will not collect any
    # items that may be locked behind the item, only the item itself.
    def collect(self, item):
        if item.advancement:
            self.prog_items[item.name] += 1


    # Be careful using this function. It will not uncollect any
    # items that may be locked behind the item, only the item itself.
    def remove(self, item):
        if self.prog_items[item.name] > 0:
            self.prog_items[item.name] -= 1
            if self.prog_items[item.name] <= 0:
                del self.prog_items[item.name]


    def __getstate__(self):
        return self.__dict__.copy()


    def __setstate__(self, state):
        self.__dict__.update(state)


    @staticmethod
    def can_beat_game(state_list):
        return Playthrough(state_list).can_beat_game()


    @staticmethod
    def update_required_items(spoiler):
        worlds = spoiler.worlds

        # get list of all of the progressive items that can appear in hints
        # all_locations: all progressive items. have to collect from these
        # item_locations: only the ones that should appear as "required"/WotH
        all_locations = [location for world in worlds for location in world.get_filled_locations()]
        # Set to test inclusion against
        item_locations = {location for location in all_locations if location.item.majoritem and not location.locked and location.item.name != 'Triforce Piece'}

        # if the playthrough was generated, filter the list of locations to the
        # locations in the playthrough. The required locations is a subset of these
        # locations. Can't use the locations directly since they are location to the
        # copied spoiler world, so must compare via name and world id
        if spoiler.playthrough:
            translate = lambda loc: worlds[loc.world.id].get_location(loc.name)
            spoiler_locations = set(map(translate, itertools.chain.from_iterable(spoiler.playthrough.values())))
            item_locations &= spoiler_locations

        required_locations = []

        playthrough = Playthrough([world.state for world in worlds])
        for location in playthrough.iter_reachable_locations(all_locations):
            # Try to remove items one at a time and see if the game is still beatable
            if location in item_locations:
                old_item = location.item
                location.item = None
                # copies state! This is very important as we're in the middle of a playthrough
                # already, but beneficially, has playthrough it can start from
                if not playthrough.can_beat_game():
                    required_locations.append(location)
                location.item = old_item
            playthrough.state_list[location.item.world.id].collect(location.item)

        # Filter the required location to only include location in the world
        required_locations_dict = {}
        for world in worlds:
            required_locations_dict[world.id] = list(filter(lambda location: location.world.id == world.id, required_locations))
        spoiler.required_locations = required_locations_dict
