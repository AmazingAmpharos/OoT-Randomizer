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
    WF = make_dungeon('Woodfall Temple', ['Woodfall Temple Beginning', 'Woodfall Temple Central Pillar'], ItemFactory('Boss Key (Woodfall Temple)'), ItemFactory(['Small Key (Woodfall Temple)'] * 5), ItemFactory(['Map (Woodfall Temple)', 'Compass (Woodfall Temple)']))
    SH = make_dungeon('Snowhead Temple', ['Snowhead Temple Beginning'], ItemFactory('Boss Key (Snowhead Temple)'), ItemFactory(['Small Key (Snowhead Temple)'] * 5), ItemFactory(['Map (Snowhead Temple)', 'Compass (Snowhead Temple)']))
    GB = make_dungeon('Great Bay Temple', ['Great Bay Temple Beginning'], ItemFactory('Boss Key (Great Bay Temple)'), ItemFactory(['Small Key (Great Bay Temple)'] * 6), ItemFactory(['Map (Great Bay Temple)', 'Compass (Great Bay Temple)']))
    ST = make_dungeon('Stone Tower Temple', ['Stone Tower Temple Beginning'], ItemFactory('Boss Key (Stone Tower Temple)'), ItemFactory(['Small Key (Stone Tower Temple)'] * 4), ItemFactory(['Map (Stone Tower Temple)', 'Compass (Stone Tower Temple)']))

    world.dungeons = [WF, SH, GB, ST]

def get_dungeon_item_pool(world):
    return [item for dungeon in world.dungeons for item in dungeon.all_items if item.key or world.place_dungeon_items]

def fill_dungeons_restrictive(world, shuffled_locations):
    all_state_base = world.get_all_state()

    dungeon_items = get_dungeon_item_pool(world)

    # sort in the order Boss Key, Small Key, Other before placing dungeon items
    sort_order = {"BossKey": 3, "SmallKey": 2}
    dungeon_items.sort(key=lambda item: sort_order.get(item.type, 1))

    fill_restrictive(world, all_state_base, shuffled_locations, dungeon_items)

    world.state.clear_cached_unreachable()
