from collections import namedtuple
import logging
import random

from Items import ItemFactory
from Fill import FillError, fill_restrictive

#This file sets the item pools for various modes. Timed modes and triforce hunt are enforced first, and then extra items are specified per mode to fill in the remaining space.
#Some basic items that various modes require are placed here, including pendants and crystals. Medallion requirements for the two relevant entrances are also decided.

alwaysitems = (['Kokiri Sword', 'Slingshot', 'Bomb Bag', 'Boomerang', 'Lens of Truth', 'Hammer', 'Iron Boots', 'Hover Boots', 'Bow', 'Rupee (1)', 'Rupees (20)'] + ['Progressive Hookshot'] * 2 + ['Deku Shield'] * 2 +  ['Hylian Shield'] * 2 +
              ['Progressive Strength Upgrade'] + ['Progressive Scale'] * 2 + ['Piece of Heart'] * 4 + ['Recovery Heart'] * 6 + ['Rupees (5)'] * 7 + ['Rupees (50)'] * 3 + ['Rupees (200)'] * 3 +
              ['Bombs (5)'] * 2 + ['Bombs (10)'] * 2 + ['Bombchus (10)'] + ['Arrows (5)'] + ['Arrows (10)'] * 3 + ['Arrows (30)'] * 2 + ['Deku Nuts (5)'] + ['Deku Nuts (10)'])
songlist = ['Zeldas Lullaby', 'Eponas Song', 'Suns Song', 'Sarias Song', 'Song of Time', 'Song of Storms', 'Minuet of Forest', 'Prelude of Light', 'Bolero of Fire', 'Serenade of Water', 'Nocturne of Shadow']
skulltulla_locations = (['GS1', 'GS2', 'GS3', 'GS4', 'GS5', 'GS6', 'GS7', 'GS8', 'GS9', 'GS10', 'GS11', 'GS12', 'GS13', 'GS14', 'GS15', 'GS16', 'GS17', 'GS18', 'GS19', 'GS20'] +
                       ['GS21', 'GS22', 'GS23', 'GS24', 'GS25', 'GS26', 'GS27', 'GS28', 'GS29', 'GS30', 'GS31', 'GS32', 'GS33', 'GS34', 'GS35', 'GS36', 'GS37', 'GS38', 'GS39', 'GS40'] +
                       ['GS41', 'GS42', 'GS43', 'GS44', 'GS45', 'GS46', 'GS47', 'GS48', 'GS49', 'GS50', 'GS51', 'GS52', 'GS53', 'GS54', 'GS55', 'GS56', 'GS57', 'GS58', 'GS59', 'GS60'] +
                       ['GS61', 'GS62', 'GS63', 'GS64', 'GS65', 'GS66', 'GS67', 'GS68', 'GS69', 'GS70', 'GS71', 'GS72', 'GS73', 'GS74', 'GS75', 'GS76', 'GS77', 'GS78', 'GS79', 'GS80'] +
                       ['GS81', 'GS82', 'GS83', 'GS84', 'GS85'])

#total_items_to_place = 5

def generate_itempool(world):

    for location in skulltulla_locations:
        world.push_item(location, ItemFactory('Gold Skulltulla Token'), False)
        world.get_location(location).event = True

    world.push_item('Ganon', ItemFactory('Triforce'), False)
    world.get_location('Ganon').event = True
    world.push_item('Queen Gohma', ItemFactory('Kokiri Emerald'), False)
    world.get_location('Queen Gohma').event = True
    world.push_item('King Dodongo', ItemFactory('Goron Ruby'), False)
    world.get_location('King Dodongo').event = True
    world.push_item('Barinade', ItemFactory('Zora Sapphire'), False)
    world.get_location('Barinade').event = True
    world.push_item('Phantom Ganon', ItemFactory('Forest Medallion'), False)
    world.get_location('Phantom Ganon').event = True
    world.push_item('Volvagia', ItemFactory('Fire Medallion'), False)
    world.get_location('Volvagia').event = True
    world.push_item('Morpha', ItemFactory('Water Medallion'), False)
    world.get_location('Morpha').event = True
    world.push_item('Bongo Bongo', ItemFactory('Shadow Medallion'), False)
    world.get_location('Bongo Bongo').event = True
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
    world.push_item('Magic Bean Salesman', ItemFactory('Magic Bean'), False)
    world.get_location('Magic Bean Salesman').event = True
    world.push_item('Underwater Bottle', ItemFactory('Bottle with Letter'), False)
    world.get_location('Underwater Bottle').event = True
    world.push_item('King Zora Moves', ItemFactory('Bottle'), False)
    world.get_location('King Zora Moves').event = True
    world.push_item('Ocarina of Time', ItemFactory('Ocarina of Time'), False)
    world.get_location('Ocarina of Time').event = True
    world.push_item('Master Sword Pedestal', ItemFactory('Master Sword'), False)
    world.get_location('Master Sword Pedestal').event = True
    world.push_item('Link the Goron', ItemFactory('Goron Tunic'), False)
    world.get_location('Link the Goron').event = True
    world.push_item('King Zora Thawed', ItemFactory('Zora Tunic'), False)
    world.get_location('King Zora Thawed').event = True

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
    song_locations = [world.get_location('Song from Composer Grave'), world.get_location('Impa at Castle'), world.get_location('Song from Malon'), world.get_location('Song from Saria'), world.get_location('Song from Ocarina of Time'), world.get_location('Song at Windmill'), world.get_location('Sheik Forest Song'), world.get_location('Sheik at Temple'), world.get_location('Sheik in Crater'), world.get_location('Sheik in Ice Cavern'), world.get_location('Sheik in Kakariko')]
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
            fill_restrictive(world, world.get_all_state(keys=True), prize_locs, prizepool) #TODO: Set keys to true once keys are properly implemented
        except FillError:
            logging.getLogger('').info("Failed to place songs. Will retry %s more times", attempts)
            for location in empty_song_locations:
                location.item = None
            continue
        break
    else:
        raise FillError('Unable to place songs')