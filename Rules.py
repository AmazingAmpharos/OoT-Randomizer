import collections
import logging


def set_rules(world):
    global_rules(world)
    '''
    if world.bridge == 'medallions':
        # require all medallions to form the bridge
        set_rule(world.get_entrance('Rainbow Bridge'), lambda state: state.has('Forest Medallion') and state.has('Fire Medallion') and state.has('Water Medallion') and state.has('Shadow Medallion') and state.has('Spirit Medallion') and state.has('Light Medallion'))
    elif world.bridge == 'vanilla':
        # require only what vanilla did to form the bridge
        set_rule(world.get_entrance('Rainbow Bridge'), lambda state: state.has('Light Arrows') and state.has('Shadow Medallion') and state.has('Spirit Medallion'))
    elif world.bridge == 'dungeons':
        # require all medallions and stones to form the bridge
        set_rule(world.get_entrance('Rainbow Bridge'), lambda state: state.has('Forest Medallion') and state.has('Fire Medallion') and state.has('Water Medallion') and state.has('Shadow Medallion') and state.has('Spirit Medallion') and state.has('Light Medallion') and state.has('Kokiri Emerald') and state.has('Goron Ruby') and state.has('Zora Sapphire'))
    '''

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


def forbid_item(location, item):
    old_rule = location.item_rule
    location.item_rule = lambda i: i.name != item and old_rule(i)


def item_in_locations(state, item, locations):
    for location in locations:
        if item_name(state, location) == item:
            return True
    return False

def item_name(state, location):
    location = state.world.get_location(location)
    if location.item is None:
        return None
    return location.item.name


def global_rules(world):
    set_rule(world.get_location('First Nut'), lambda state: state.form('Deku'))
    set_rule(world.get_location('Clock Town GF Reward'), lambda state: state.has('CT SF'), 1)
    set_rule(world.get_location('Woodfall GF Reward'), lambda state: state.has('WF SF'), 15)
    set_rule(world.get_location('Snowhead GF Reward'), lambda state: state.has('SH SF'), 15)
    set_rule(world.get_location('Great Bay GF Reward'), lambda state: state.has('GB SF'), 15)
    set_rule(world.get_location('Stone Tower GF Reward'), lambda state: state.has('ST SF'), 15)
    set_rule(world.get_location('Bomber Code'), lambda state: state.has('Magic Meter'))
    set_rule(world.get_entrance('Bomber Tunnel'), lambda state: state.has('Bomber Code'))
    set_rule(world.get_entrance('Astral Observatory Fence'), lambda state: state.has('Magic Beans') or state.can('Goron Boost'))
    set_rule(world.get_location('Clock Town Business Scrub'), lambda state: state.has('Moons Tear'))
    set_rule(world.get_location('Swamp Business Scrub'), lambda state: state.has('Town Title Deed'))
    set_rule(world.get_location('Mountain Business Scrub'), lambda state: state.has('Swamp Title Deed'))
    set_rule(world.get_location('Ocean Business Scrub'), lambda state: state.has('Mountain Title Deed'))
    set_rule(world.get_location('Canyon Business Scrub'), lambda state: state.has('Ocean Title Deed'))
    set_rule(world.get_location('Song From Mask Salesman'), lambda state: state.has('Ocarina of Time'))
    set_rule(world.get_location('Remove the Cursed Mask'), lambda state: state.has('Ocarina of Time'))
    set_rule(world.get_location('Tunnel Balloon From Observatory'), lambda state: state.has('Bow') or (state.form('Deku') and state.has('Magic Meter')))
    set_rule(world.get_location('Tunnel Balloon From ECT'), lambda state: state.has('Bow') or (state.form('Deku') and state.has('Magic Meter')))
