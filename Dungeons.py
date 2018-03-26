import random

from BaseClasses import Dungeon
from Fill import fill_restrictive
from Items import ItemFactory


def create_dungeons(world):
    def make_dungeon(name, dungeon_regions, boss_key, small_keys, dungeon_items):
        dungeon = Dungeon(name, dungeon_regions, boss_key, small_keys, dungeon_items)
        for region in dungeon.regions:
            world.get_region(region).dungeon = dungeon
        return dungeon

    DT = make_dungeon('Deku Tree', ['Deku Tree Lobby', 'Deku Tree Slingshot Room', 'Deku Tree Boss Room'], None, [], ItemFactory(['Map (Deku Tree)', 'Compass (Deku Tree)']))
    DC = make_dungeon('Dodongos Cavern', ['Dodongos Cavern Beginning', 'Dodongos Cavern Lobby', 'Dodongos Cavern Climb', 'Dodongos Cavern Far Bridge', 'Dodongos Cavern Boss Area'], None, [], ItemFactory(['Map (Dodongos Cavern)', 'Compass (Dodongos Cavern)']))
    JB = make_dungeon('Jabu Jabus Belly', ['Jabu Jabus Belly Beginning', 'Jabu Jabus Belly Main', 'Jabu Jabus Belly Depths', 'Jabu Jabus Belly Boss Area'], None, [], ItemFactory(['Map (Jabu Jabus Belly)', 'Compass (Jabu Jabus Belly)']))
    FoT = make_dungeon('Forest Temple', ['Forest Temple Lobby', 'Forest Temple NW Outdoors', 'Forest Temple NE Outdoors', 'Forest Temple Falling Room', 'Forest Temple Block Push Room', 'Forest Temple Straightened Hall', 'Forest Temple Outside Upper Ledge', 'Forest Temple Bow Region', 'Forest Temple Boss Region'], None, ItemFactory(['Small Key (Forest Temple)'] * 5), ItemFactory(['Map (Forest Temple)', 'Compass (Forest Temple)']))
#    EP = make_dungeon('Eastern Palace', ['Eastern Palace'], ItemFactory('Big Key (Eastern Palace)'), [], ItemFactory(['Map (Eastern Palace)', 'Compass (Eastern Palace)']))
 
    world.dungeons = [DT, DC, JB, FoT]


def get_dungeon_item_pool(world):
    return [item for dungeon in world.dungeons for item in dungeon.all_items if item.key or world.place_dungeon_items]

def fill_dungeons_restrictive(world, shuffled_locations):
    all_state_base = world.get_all_state()

#    forest_temple_boss_chest = world.get_location('Forest Temple Boss Key Chest')
#    world.push_item(forest_temple_boss_chest, ItemFactory('Boss Key (Forest Temple)'), False)
#    forest_temple_boss_chest.event = True
#    shuffled_locations.remove(forest_temple_boss_chest)

    dungeon_items = get_dungeon_item_pool(world)

    # sort in the order Boss Key, Small Key, Other before placing dungeon items
    sort_order = {"BossKey": 3, "SmallKey": 2}
    dungeon_items.sort(key=lambda item: sort_order.get(item.type, 1))

    fill_restrictive(world, all_state_base, shuffled_locations, dungeon_items)

    world.state.clear_cached_unreachable()