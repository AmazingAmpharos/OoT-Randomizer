from collections import namedtuple
import logging
import random

from Items import ItemFactory
from Fill import FillError, fill_restrictive

#This file sets the item pools for various modes. Timed modes and triforce hunt are enforced first, and then extra items are specified per mode to fill in the remaining space.
#Some basic items that various modes require are placed here, including pendants and crystals. Medallion requirements for the two relevant entrances are also decided.

alwaysitems = ['Kokiri Sword', 'Slingshot', 'Bomb Bag', 'Boomerang', 'Deku Shield', 'Hylian Shield', 'Rupee (1)', 'Rupees (20)'] + ['Piece of Heart'] * 2 + ['Recovery Heart'] * 4 + ['Rupees (5)'] * 2 + ['Rupees (50)'] * 3 + ['Bombs (5)'] * 2
songlist = ['Zeldas Lullaby', 'Suns Song', 'Sarias Song', 'Song of Time']

total_items_to_place = 5

def generate_itempool(world):

    world.push_item('Ganon', ItemFactory('Triforce'), False)
    world.get_location('Ganon').event = True
    world.push_item('Queen Gohma', ItemFactory('Kokiri Emerald'), False)
    world.get_location('Queen Gohma').event = True
    world.push_item('King Dodongo', ItemFactory('Goron Ruby'), False)
    world.get_location('King Dodongo').event = True
    world.push_item('Barinade', ItemFactory('Zora Sapphire'), False)
    world.get_location('Barinade').event = True
    world.push_item('Gift from Saria', ItemFactory('Fairy Ocarina'), False)
    world.get_location('Gift from Saria').event = True
    world.push_item('Zeldas Letter', ItemFactory('Zeldas Letter'), False)
    world.get_location('Zeldas Letter').event = True
    world.push_item('Mountain Summit Fairy Reward', ItemFactory('Magic Meter'), False)
    world.get_location('Mountain Summit Fairy Reward').event = True
    world.push_item('Hyrule Castle Fairy Reward', ItemFactory('Dins Fire'), False)
    world.get_location('Hyrule Castle Fairy Reward').event = True
    world.push_item('Zoras Fountain Fairy Reward', ItemFactory('Farores Wind'), False)
    world.get_location('Zoras Fountain Fairy Reward').event = True
    world.push_item('Darunias Sadness', ItemFactory('Darunia is Sad Event'), False)
    world.get_location('Darunias Sadness').event = True
    world.push_item('Darunias Joy', ItemFactory('Goron Bracelet'), False)
    world.get_location('Darunias Joy').event = True
    world.push_item('Diving Minigame', ItemFactory('Silver Scale'), False)
    world.get_location('Diving Minigame').event = True
    world.push_item('Underwater Bottle', ItemFactory('Bottle with Letter'), False)
    world.get_location('Underwater Bottle').event = True
    world.push_item('King Zora Moves', ItemFactory('Bottle'), False)
    world.get_location('King Zora Moves').event = True
    world.push_item('Ocarina of Time', ItemFactory('Ocarina of Time'), False)
    world.get_location('Ocarina of Time').event = True
    world.push_item('Master Sword Pedestal', ItemFactory('Master Sword'), False)
    world.get_location('Master Sword Pedestal').event = True
    world.push_item('Goron City Leftmost Maze Chest', ItemFactory('Rupees (200)'), False)
    world.get_location('Goron City Leftmost Maze Chest').event = True

    # set up item pool
    (pool, placed_items) = get_pool_core()
    world.itempool = ItemFactory(pool)
    for (location, item) in placed_items:
        world.push_item(location, ItemFactory(item), False)
        world.get_location(location).event = True

    fill_songs(world)

def get_pool_core():
    pool = []
    placed_items = []

    pool.extend(alwaysitems)

    return (pool, placed_items)

def fill_songs(world, attempts=15):
    songs = ItemFactory(songlist)
    song_locations = [world.get_location('Song from Composer Grave'), world.get_location('Impa at Castle'), world.get_location('Song from Saria'), world.get_location('Song from Ocarina of Time')]
    placed_prizes = [loc.item.name for loc in song_locations if loc.item is not None]
    unplaced_prizes = [song for song in songs if song.name not in placed_prizes]
    empty_song_locations = [loc for loc in song_locations if loc.item is None]

    while attempts:
        attempts -= 1
        try:
            prizepool = list(unplaced_prizes)
            prize_locs = list(empty_song_locations)
            random.shuffle(prizepool)
            random.shuffle(prize_locs)
            fill_restrictive(world, world.get_all_state(keys=False), prize_locs, prizepool) #TODO: Set keys to true once keys are properly implemented
        except FillError:
            logging.getLogger('').info("Failed to place songs. Will retry %s more times", attempts)
            for location in empty_song_locations:
                location.item = None
            continue
        break
    else:
        raise FillError('Unable to place songs')