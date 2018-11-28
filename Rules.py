import collections
import logging
from Location import DisableType


def set_rules(world):
    if world.bridge == 'medallions':
        # require all medallions to form the bridge
        set_rule(
            world.get_entrance('Ganons Castle Grounds -> Ganons Castle Lobby'),
            lambda state: (
                state.has('Forest Medallion') and 
                state.has('Fire Medallion') and 
                state.has('Water Medallion') and 
                state.has('Shadow Medallion') and 
                state.has('Spirit Medallion') and 
                state.has('Light Medallion')))
    elif world.bridge == 'vanilla':
        # require only what vanilla did to form the bridge
        set_rule(
            world.get_entrance('Ganons Castle Grounds -> Ganons Castle Lobby'),
            lambda state: (
                state.has('Light Arrows') and 
                state.has('Shadow Medallion') and 
                state.has('Spirit Medallion')))
    elif world.bridge == 'dungeons':
        # require all medallions and stones to form the bridge
        set_rule(
            world.get_entrance('Ganons Castle Grounds -> Ganons Castle Lobby'),
            lambda state: (
                state.has('Forest Medallion') and 
                state.has('Fire Medallion') and 
                state.has('Water Medallion') and 
                state.has('Shadow Medallion') and
                state.has('Spirit Medallion') and 
                state.has('Light Medallion') and 
                state.has('Kokiri Emerald') and 
                state.has('Goron Ruby') and 
                state.has('Zora Sapphire')))

    # ganon can only carry triforce
    world.get_location('Ganon').item_rule = lambda item: item.name == 'Triforce'

    # these are default save&quit points and always accessible
    world.get_region('Links House').can_reach = lambda state: True
    
    for location in world.get_locations():
        if location.type != 'Chest':
            forbid_item(location, 'Ice Trap')

        if not world.shuffle_song_items:
            if location.type == 'Song':
                add_item_rule(location, lambda item: item.type == 'Song' and item.world.id == location.world.id)
            else:
                add_item_rule(location, lambda item: item.type != 'Song')

        if location.type == 'Shop':
            if location.name in world.shop_prices:
                add_item_rule(location, lambda item: item.type != 'Shop')
                location.price = world.shop_prices[location.name]
                if location.price > 200:
                    set_rule(location, lambda state: state.has('Progressive Wallet', 2))
                elif location.price > 99:
                    set_rule(location, lambda state: state.has('Progressive Wallet'))
            else:
                add_item_rule(location, lambda item: item.type == 'Shop' and item.world.id == location.world.id)

            if location.parent_region.name in ['Castle Town Bombchu Shop', 'Castle Town Potion Shop', 'Castle Town Bazaar']:
                if not world.check_beatable_only:
                    forbid_item(location, 'Buy Goron Tunic')
                    forbid_item(location, 'Buy Zora Tunic')
        elif not 'Deku Scrub' in location.name:
            add_item_rule(location, lambda item: item.type != 'Shop')

    if world.logic_skulltulas < 10:
        world.get_location('10 Gold Skulltula Reward').disabled = DisableType.PENDING
    if world.logic_skulltulas < 20:
        world.get_location('20 Gold Skulltula Reward').disabled = DisableType.PENDING
    if world.logic_skulltulas < 30:
        world.get_location('30 Gold Skulltula Reward').disabled = DisableType.PENDING
    if world.logic_skulltulas < 40:
        world.get_location('40 Gold Skulltula Reward').disabled = DisableType.PENDING
    if world.logic_skulltulas < 50:
        world.get_location('50 Gold Skulltula Reward').disabled = DisableType.PENDING
    if world.logic_no_big_poes:
        world.get_location('10 Big Poes').disabled = DisableType.PENDING
    if world.logic_no_child_fishing:
        world.get_location('Child Fishing').disabled = DisableType.PENDING
    if world.logic_no_adult_fishing:
        world.get_location('Adult Fishing').disabled = DisableType.PENDING
    if world.logic_no_trade_skull_mask:
        world.get_location('Deku Theater Skull Mask').disabled = DisableType.PENDING
    if world.logic_no_trade_mask_of_truth:
        world.get_location('Deku Theater Mask of Truth').disabled = DisableType.PENDING
    if world.logic_no_ocarina_of_time:
        world.get_location('Ocarina of Time').disabled = DisableType.PENDING
        world.get_location('Song from Ocarina of Time').disabled = DisableType.PENDING
    if world.logic_no_1500_archery:
        world.get_location('Horseback Archery 1500 Points').disabled = DisableType.PENDING
    if world.logic_no_memory_game:
        world.get_location('Ocarina Memory Game').disabled = DisableType.PENDING
    if world.logic_no_frog_ocarina_game:
        world.get_location('Frog Ocarina Game').disabled = DisableType.PENDING
    if world.logic_no_second_dampe_race:
        world.get_location('Dampe Race Freestanding PoH').disabled = DisableType.PENDING
    if world.logic_no_trade_biggoron:
        world.get_location('Biggoron').disabled = DisableType.PENDING


def set_rule(spot, rule):
    spot.access_rule = rule


def set_always_allow(spot, rule):
    spot.always_allow = rule


def add_rule(spot, rule, combine='and'):
    old_rule = spot.access_rule
    if combine == 'or':
        spot.access_rule = lambda state: rule(state) or old_rule(state)
    else:
        spot.access_rule = lambda state: rule(state) and old_rule(state)


def add_item_rule(spot, rule, combine='and'):
    old_rule = spot.item_rule
    if combine == 'or':
        spot.item_rule = lambda item: rule(item) or old_rule(item)
    else:
        spot.item_rule = lambda item: rule(item) and old_rule(item)


def forbid_item(location, item):
    old_rule = location.item_rule
    location.item_rule = lambda i: i.name != item and old_rule(i)


def item_in_locations(state, item, locations):
    for location in locations:
        if state.item_name(location) == item:
            return True
    return False


# This function should be ran once after the shop items are placed in the world.
# It should be ran before other items are placed in the world so that logic has
# the correct checks for them. This is save to do since every shop is still
# accessible when all items are obtained and every shop item is not.
# This function should also be called when a world is copied if the original world
# had called this function because the world.copy does not copy the rules
def set_shop_rules(world):
    for location in world.get_filled_locations():
        if location.item.type == 'Shop':
            # Add wallet requirements
            if location.item.name in ['Buy Arrows (50)', 'Buy Fish', 'Buy Goron Tunic', 'Buy Bombchu (20)', 'Buy Bombs (30)']:
                add_rule(location, lambda state: state.has('Progressive Wallet'))
            elif location.item.name in ['Buy Zora Tunic', 'Buy Blue Fire']:
                add_rule(location, lambda state: state.has('Progressive Wallet', 2))

            # Add adult only checks
            if location.item.name in ['Buy Goron Tunic', 'Buy Zora Tunic']:
                if location.parent_region.name == 'Goron Shop':
                    add_rule(
                        location,
                        lambda state: state.is_adult() and (state.has_explosives() or state.has('Progressive Strength Upgrade') or state.has_bow()))
                elif location.parent_region.name == 'Zora Shop':
                    add_rule(location, lambda state: state.can_reach('Zoras Domain Frozen -> Zora Shop', 'Entrance'))
                elif location.parent_region.name in ['Castle Town Bombchu Shop', 'Castle Town Potion Shop', 'Castle Town Bazaar']:
                    set_rule(location, lambda state: False)
                else:
                    add_rule(location, lambda state: state.is_adult())

            # Add item prerequisit checks
            if location.item.name in ['Buy Blue Fire',
                                      'Buy Blue Potion',
                                      'Buy Bottle Bug',
                                      'Buy Fish',
                                      'Buy Green Potion',
                                      'Buy Poe',
                                      'Buy Red Potion [30]',
                                      'Buy Red Potion [40]',
                                      'Buy Red Potion [50]',
                                      'Buy Fairy\'s Spirit']:
                add_rule(location, lambda state: state.has_bottle())
            if location.item.name in ['Buy Bombchu (10)', 'Buy Bombchu (20)', 'Buy Bombchu (5)']:
                add_rule(location, lambda state: state.has_bombchus_item())

