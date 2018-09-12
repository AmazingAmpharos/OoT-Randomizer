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
    set_rule(world.get_location('Clock Town GF Reward'), lambda state: state.has('CT SF', 1))
    set_rule(world.get_location('Woodfall GF Reward'), lambda state: state.has('WF SF', 15))
    set_rule(world.get_location('Snowhead GF Reward'), lambda state: state.has('SH SF', 15))
    set_rule(world.get_location('Great Bay GF Reward'), lambda state: state.has('GB SF', 15))
    set_rule(world.get_location('Stone Tower GF Reward'), lambda state: state.has('ST SF', 15))
    set_rule(world.get_location('Bomber Code'), lambda state: state.has('Magic Meter') and state.form('Deku'))
    set_rule(world.get_entrance('Bomber Tunnel'), lambda state: state.has('Bomber Code'))
    set_rule(world.get_entrance('Astral Observatory Fence'), lambda state: state.has('Magic Beans') or state.can('Goron Boost'))
    set_rule(world.get_location('Clock Town Business Scrub'), lambda state: state.has('Moons Tear'))
    set_rule(world.get_location('Swamp Business Scrub'), lambda state: state.has('Town Title Deed'))
    set_rule(world.get_location('Mountain Business Scrub'), lambda state: state.has('Swamp Title Deed'))
    set_rule(world.get_location('Ocean Business Scrub'), lambda state: state.has('Mountain Title Deed'))
    set_rule(world.get_location('Canyon Business Scrub'), lambda state: state.has('Ocean Title Deed'))
    set_rule(world.get_location('Song From Mask Salesman'), lambda state: state.has('Ocarina of Time'))
    set_rule(world.get_location('Remove the Cursed Mask'), lambda state: state.has('Ocarina of Time'))
    set_rule(world.get_location('Tunnel Balloon From Observatory'), lambda state: (state.has('Bow') and state.form('Human')) or (state.form('Deku') and state.has('Magic Meter')))
    set_rule(world.get_location('Tunnel Balloon From ECT'), lambda state: (state.has('Bow') and state.form('Human')) or (state.form('Deku') and state.has('Magic Meter')))
    # RevelationOrange started adding rules here (plus a few changes in rules above)
    # location names used are mostly guesses and can absolutely be changed later
    # item names used are also guesses, as are some state function names probly
    # location names may be longer than necessary so as to be descriptive, like we can change 'South Clock Town Hookshot
    # Ledge Rupee Chest' if we want lol
    set_rule(world.get_location('Clock Tower Platform HP'), lambda state: state.form('Human') or state.form('Goron') or state.form('Zora') or state.can_reach(world.get_location('Clock Town Business Scrub')))
    set_rule(world.get_location('Festival Tower Rupee Chest'), lambda state: state.has('Hookshot') or state.can_reach(world.get_location('Clock Town Business Scrub')))
    set_rule(world.get_location('South Clock Town Hookshot Ledge Rupee Chest'), lambda state: state.has('Hookshot'))
    set_rule(world.get_location('Bremen Mask From Guru Guru'), lambda state: state.form('Human'))
    set_rule(world.get_location('Rosa Sisters HP'), lambda state: state.has('Kamaro Mask'))

    # obviously, this and simliar 'tests' might not be necessary at all
    set_rule(world.get_location('Adult Wallet from bank'), lambda state: True)
    set_rule(world.get_location('Bank HP'), lambda state: True)

    # I don't know that this item matters at all or if we should even have a spot for it
    # but we can if we want, you get it the same way you get the code in the first cycle, you just have to be human to
    # get the actual notebook from them I think
    set_rule(world.get_location('Bomber Notebook'), lambda state: state.has('Magic Meter') and state.form('Deku') and state.form('Human'))

    # since getting the blast mask just involves slashing sakon, it might be possible to get it with other forms? like
    # maybe zora? probly not goron though
    # also you might need to be link to talk to the lady after, so maybe it is only human
    set_rule(world.get_location('Blast Mask'), lambda state: state.form('Human'))

    set_rule(world.get_location('North Clock Town Tree HP'), lambda state: True)
    set_rule(world.get_location('Tingle Clock Town Map'), lambda state: True)
    set_rule(world.get_location('Tingle Woodfall Map'), lambda state: True)
    set_rule(world.get_location('Keaton HP'), lambda state: state.has('Keaton Mask'))

    # I need to figure out all the actual requirements for this, including tricks, so this one is tentative
    # also the trick names are guesses for sure
    set_rule(world.get_location('East Clock Town 100 Rupee Chest'), lambda state: state.form('Human') or state.can('Goron Boost') or state.can('Gainer'))

    set_rule(world.get_location('Ocarina of Time'), lambda state: (state.form('Deku') and state.has('Magic Meter')) or (state.has('Bow') and state.form('Human')))
    set_rule(world.get_location('All Night mask'), lambda state: state.form('Human') and state.has('Giants Wallet'))
    set_rule(world.get_location('Bigger Bomb Bag'), lambda state: state.has('Giants Wallet'))

    # you might not need to be human to get this, but I'd bet the shop owner won't sell to other forms, at least deku
    set_rule(world.get_location('Bomb Bag'), lambda state: state.form('Human'))

    set_rule(world.get_location('Sword School HP'), lambda state: state.form('Human'))

    # i swear this should be an optional trick, it's so hard without the bunny hood lol
    set_rule(world.get_location('Postman Game HP'), lambda state: state.can('Time ten') or state.has('Bunny Hood'))

    set_rule(world.get_location('Deku Scrub Playground HP'), lambda state: state.form('Deku'))
    set_rule(world.get_location('Great Fairy Mask'), lambda state: True)
    set_rule(world.get_location('Clock Town Maze Minigame HP'), lambda state: state.form('Goron'))
    set_rule(world.get_location('Bomber Hideout 100 Rupee Chest'), lambda state: state.has('Bomber Code') and (state.has('Bomb Bag') or state.has('Blast Mask')))
    # set_rule(world.get_location(''), lambda state: state)

# ooh ooh
# maybe have a gate at the clock tower roof that requires the ocarina, to go back to south clock town on the first day
# maayyybe
# to force placement of the ocarina somewhere you can get to it in the first cycle
# depends on how crawling through the graph works
