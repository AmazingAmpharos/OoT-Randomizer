import collections
import logging


def set_rules(world):
    global_rules(world)

    #if world.goal == 'dungeons':
        # require all dungeons to beat ganon
        #add_rule(world.get_location('Ganon'), lambda state: state.can_reach('Master Sword Pedestal', 'Location') and state.has('Beat Agahnim 1') and state.has('Beat Agahnim 2'))
    #elif world.goal == 'ganon':
        # require aga2 to beat ganon
        #add_rule(world.get_location('Ganon'), lambda state: state.has('Beat Agahnim 2'))


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
    # ganon can only carry triforce
    world.get_location('Ganon').item_rule = lambda item: item.name == 'Triforce'

    # these are default save&quit points and always accessible
    world.get_region('Links House').can_reach = lambda state: True

    # overworld requirements
    set_rule(world.get_entrance('Deku Tree'), lambda state: state.has('Kokiri Sword') or world.open_forest)
    set_rule(world.get_entrance('Lost Woods Bridge'), lambda state: state.has('Kokiri Emerald') or world.open_forest)
    set_rule(world.get_entrance('Deku Tree Basement Path'), lambda state: state.has('Slingshot') and state.has('Kokiri Sword'))
    set_rule(world.get_location('Heart Piece Grave Chest'), lambda state: state.has('Suns Song'))
    set_rule(world.get_entrance('Composer Grave'), lambda state: state.has('Zeldas Lullaby'))
    set_rule(world.get_location('Composer Grave Chest'), lambda state: state.has_fire_source())
    set_rule(world.get_location('Song from Composer Grave'), lambda state: state.has('Kokiri Sword') or state.has('Slingshot') or state.has_fire_source() or state.can_blast() or state.has('Boomerang') or state.is_adult())
    set_rule(world.get_entrance('Death Mountain Entrance'), lambda state: state.has('Zeldas Letter'))
    set_rule(world.get_location('Death Mountain Bombable Chest'), lambda state: state.can_blast())
    set_rule(world.get_location('Goron City Left Maze Chest'), lambda state: state.can_blast())
    set_rule(world.get_location('Goron City Right Maze Chest'), lambda state: state.can_blast())
    set_rule(world.get_entrance('Darunias Chamber'), lambda state: state.has('Zeldas Lullaby'))
    set_rule(world.get_location('Darunias Joy'), lambda state: state.has('Sarias Song'))
    set_rule(world.get_entrance('Goron City from Woods'), lambda state: state.can_blast())
    set_rule(world.get_entrance('Meadow Gate'), lambda state: state.has('Kokiri Sword') or state.is_adult())
    set_rule(world.get_entrance('Dodongos Cavern Rocks'), lambda state: state.can_blast() or state.has('Goron Bracelet'))
    set_rule(world.get_entrance('Dodongos Cavern Lobby'), lambda state: state.has('Bomb Bag') or state.has('Goron Bracelet'))
    set_rule(world.get_entrance('Dodongos Cavern Left Door'), lambda state: state.has('Kokiri Sword'))
    set_rule(world.get_entrance('Dodongos Cavern Slingshot Target'), lambda state: state.has('Slingshot'))
    set_rule(world.get_entrance('Dodongos Cavern Bomb Drop'), lambda state: state.has('Bomb Bag'))
    set_rule(world.get_location('Song from Saria'), lambda state: state.has('Darunia is Sad Event'))
    set_rule(world.get_entrance('Mountain Summit Fairy'), lambda state: state.has('Bomb Bag'))
    set_rule(world.get_location('Mountain Summit Fairy Reward'), lambda state: state.has('Zeldas Lullaby'))
    set_rule(world.get_entrance('Hyrule Castle Fairy'), lambda state: state.has('Bomb Bag'))
    set_rule(world.get_location('Hyrule Castle Fairy Reward'), lambda state: state.has('Zeldas Lullaby') and state.has('Magic Meter'))
    set_rule(world.get_entrance('Lost Woods Dive Warp'), lambda state: state.can_dive())
    set_rule(world.get_entrance('Zora River Dive Warp'), lambda state: state.can_dive())
    set_rule(world.get_entrance('Lake Hylia Dive Warp'), lambda state: state.can_dive())
    set_rule(world.get_entrance('Zoras Domain Dive Warp'), lambda state: state.can_dive())
    set_rule(world.get_entrance('Zora River Waterfall'), lambda state: state.has('Zeldas Lullaby'))
    set_rule(world.get_location('Underwater Bottle'), lambda state: state.can_dive())
    set_rule(world.get_location('King Zora Moves'), lambda state: state.has('Bottle with Letter'))
    set_rule(world.get_entrance('Behind King Zora'), lambda state: state.has('Bottle with Letter'))
    set_rule(world.get_entrance('Jabu Jabus Belly'), lambda state: state.has('Bottle'))
    set_rule(world.get_entrance('Zoras Fountain Fairy'), lambda state: state.has('Bomb Bag'))
    set_rule(world.get_location('Zoras Fountain Fairy Reward'), lambda state: state.has('Zeldas Lullaby') and state.has('Magic Meter'))
    set_rule(world.get_entrance('Jabu Jabus Belly Ceiling Switch'), lambda state: state.has('Slingshot') or state.has('Bomb Bag') or state.has('Boomerang'))
    set_rule(world.get_entrance('Jabu Jabus Belly Tentacles'), lambda state: state.has('Boomerang'))
    set_rule(world.get_entrance('Jabu Jabus Belly Octopus'), lambda state: state.has('Kokiri Sword'))
    set_rule(world.get_location('Ocarina of Time'), lambda state: state.has('Kokiri Emerald') and state.has('Goron Ruby') and state.has('Zora Sapphire'))
    set_rule(world.get_location('Song from Ocarina of Time'), lambda state: state.has('Kokiri Emerald') and state.has('Goron Ruby') and state.has('Zora Sapphire'))
    set_rule(world.get_entrance('Door of Time'), lambda state: state.has('Kokiri Emerald') and state.has('Goron Ruby') and state.has('Zora Sapphire') and state.has('Song of Time'))


    set_rule(world.get_entrance('Forest Generic Grotto'), lambda state: state.can_blast())
    set_rule(world.get_entrance('Forest Sales Grotto'), lambda state: state.can_blast())
    set_rule(world.get_entrance('Front of Meadow Grotto'), lambda state: state.can_blast())
    set_rule(world.get_entrance('Remote Southern Grotto'), lambda state: state.can_blast())
    set_rule(world.get_entrance('Field Near Lake Inside Fence Grotto'), lambda state: state.can_blast())
    set_rule(world.get_entrance('Field Valley Grotto'), lambda state: state.can_blast())
    set_rule(world.get_entrance('Field West Castle Town Grotto'), lambda state: state.can_blast())
    set_rule(world.get_entrance('Field Far West Castle Town Grotto'), lambda state: state.can_blast())
    set_rule(world.get_entrance('Field Kakariko Grotto'), lambda state: state.can_blast())
    set_rule(world.get_entrance('Field North Lon Lon Grotto'), lambda state: state.can_blast())
    set_rule(world.get_entrance('Kakariko Bombable Grotto'), lambda state: state.can_blast())
    set_rule(world.get_entrance('Mountain Bombable Grotto'), lambda state: state.can_blast())
    set_rule(world.get_entrance('Top of Crater Grotto'), lambda state: state.can_blast())
    set_rule(world.get_entrance('Zora River Plateau Bombable Grotto'), lambda state: state.can_blast())