from collections import namedtuple
import logging
import random

from Items import ItemFactory
from Fill import FillError, fill_restrictive

#This file sets the item pools for various modes. Timed modes and triforce hunt are enforced first, and then extra items are specified per mode to fill in the remaining space.
#Some basic items that various modes require are placed here, including pendants and crystals. Medallion requirements for the two relevant entrances are also decided.

alwaysitems = (['Kokiri Sword', 'Biggoron Sword', 'Boomerang', 'Lens of Truth', 'Hammer', 'Iron Boots', 'Goron Tunic', 'Zora Tunic', 'Hover Boots', 'Mirror Shield', 'Stone of Agony', 'Fire Arrows', 'Ice Arrows', 'Light Arrows', 'Dins Fire', 'Farores Wind', 'Nayrus Love', 'Rupee (1)'] + ['Progressive Hookshot'] * 2 + ['Deku Shield'] * 4 +  ['Hylian Shield'] * 2 + ['Ice Trap'] * 6 +
              ['Progressive Strength Upgrade'] * 3 + ['Progressive Scale'] * 2 + ['Piece of Heart'] * 16 + ['Recovery Heart'] * 11 + ['Rupees (5)'] * 13 + ['Rupees (20)'] * 2 + ['Rupees (50)'] * 7 + ['Rupees (200)'] * 5 + ['Bow'] * 3 + ['Slingshot'] * 3 + ['Bomb Bag'] * 3 + ['Bottle'] * 2 + ['Bottle with Letter'] + ['Bottle with Milk'] +
              ['Bombs (5)'] * 2 + ['Bombs (10)'] * 2 + ['Bombs (20)'] + ['Bombchus (5)'] + ['Bombchus (10)'] * 3 + ['Bombchus (20)'] + ['Arrows (5)'] + ['Arrows (10)'] * 6 + ['Arrows (30)'] * 6 + ['Deku Nuts (5)'] + ['Deku Nuts (10)'] + ['Progressive Wallet'] * 2 + ['Deku Stick Capacity'] * 2 + ['Deku Nut Capacity'] * 2)
notmapcompass = ['Rupees (5)'] * 20
songlist = ['Zeldas Lullaby', 'Eponas Song', 'Suns Song', 'Sarias Song', 'Song of Time', 'Song of Storms', 'Minuet of Forest', 'Prelude of Light', 'Bolero of Fire', 'Serenade of Water', 'Nocturne of Shadow', 'Requiem of Spirit']
rewardlist = ['Kokiri Emerald', 'Goron Ruby', 'Zora Sapphire', 'Forest Medallion', 'Fire Medallion', 'Water Medallion', 'Spirit Medallion', 'Shadow Medallion']
boss_rewards = ItemFactory(rewardlist)
skulltulla_locations = (['GS1', 'GS2', 'GS3', 'GS4', 'GS5', 'GS6', 'GS7', 'GS8', 'GS9', 'GS10', 'GS11', 'GS12', 'GS13', 'GS14', 'GS15', 'GS16', 'GS17', 'GS18', 'GS19', 'GS20'] +
                       ['GS21', 'GS22', 'GS23', 'GS24', 'GS25', 'GS26', 'GS27', 'GS28', 'GS29', 'GS30', 'GS31', 'GS32', 'GS33', 'GS34', 'GS35', 'GS36', 'GS37', 'GS38', 'GS39', 'GS40'] +
                       ['GS41', 'GS42', 'GS43', 'GS44', 'GS45', 'GS46', 'GS47', 'GS48', 'GS49', 'GS50', 'GS51', 'GS52', 'GS53', 'GS54', 'GS55', 'GS56', 'GS57', 'GS58', 'GS59', 'GS60'] +
                       ['GS61', 'GS62', 'GS63', 'GS64', 'GS65', 'GS66', 'GS67', 'GS68', 'GS69', 'GS70', 'GS71', 'GS72', 'GS73', 'GS74', 'GS75', 'GS76', 'GS77', 'GS78', 'GS79', 'GS80'] +
                       ['GS81', 'GS82', 'GS83', 'GS84', 'GS85', 'GS86', 'GS87', 'GS88', 'GS89', 'GS90', 'GS91', 'GS92', 'GS93', 'GS94', 'GS95', 'GS96', 'GS97', 'GS98', 'GS99', 'GS100'])
tradeitems = ['Pocket Egg', 'Pocket Cucco', 'Cojiro', 'Odd Mushroom', 'Poachers Saw', 'Broken Sword', 'Prescription', 'Eyeball Frog', 'Eyedrops', 'Claim Check']

#total_items_to_place = 5

def generate_itempool(world):

    for location in skulltulla_locations:
        world.push_item(location, ItemFactory('Gold Skulltulla Token'), False)
        world.get_location(location).event = True

    world.push_item('Ganon', ItemFactory('Triforce'), False)
    world.get_location('Ganon').event = True
    world.push_item('Gift from Saria', ItemFactory('Fairy Ocarina'), False)
    world.get_location('Gift from Saria').event = True
    world.push_item('Zeldas Letter', ItemFactory('Zeldas Letter'), False)
    world.get_location('Zeldas Letter').event = True
    world.push_item('Mountain Summit Fairy Reward', ItemFactory('Magic Meter'), False)
    world.get_location('Mountain Summit Fairy Reward').event = True
    world.push_item('Magic Bean Salesman', ItemFactory('Magic Bean'), False)
    world.get_location('Magic Bean Salesman').event = True
    world.push_item('King Zora Moves', ItemFactory('Bottle'), False)
    world.get_location('King Zora Moves').event = True
    world.push_item('Ocarina of Time', ItemFactory('Ocarina of Time'), False)
    world.get_location('Ocarina of Time').event = True
    world.push_item('Master Sword Pedestal', ItemFactory('Master Sword'), False)
    world.get_location('Master Sword Pedestal').event = True
    world.push_item('Epona', ItemFactory('Epona'), False)
    world.get_location('Epona').event = True
    world.push_item('Gerudo Fortress Carpenter Rescue', ItemFactory('Gerudo Membership Card'), False)
    world.get_location('Gerudo Fortress Carpenter Rescue').event = True
    world.push_item('Ganons Castle Forest Trial Clear', ItemFactory('Forest Trial Clear'), False)
    world.get_location('Ganons Castle Forest Trial Clear').event = True
    world.push_item('Ganons Castle Fire Trial Clear', ItemFactory('Fire Trial Clear'), False)
    world.get_location('Ganons Castle Fire Trial Clear').event = True
    world.push_item('Ganons Castle Water Trial Clear', ItemFactory('Water Trial Clear'), False)
    world.get_location('Ganons Castle Water Trial Clear').event = True
    world.push_item('Ganons Castle Shadow Trial Clear', ItemFactory('Shadow Trial Clear'), False)
    world.get_location('Ganons Castle Shadow Trial Clear').event = True
    world.push_item('Ganons Castle Spirit Trial Clear', ItemFactory('Spirit Trial Clear'), False)
    world.get_location('Ganons Castle Spirit Trial Clear').event = True
    world.push_item('Ganons Castle Light Trial Clear', ItemFactory('Light Trial Clear'), False)
    world.get_location('Ganons Castle Light Trial Clear').event = True

    # set up item pool
    (pool, placed_items) = get_pool_core(world.place_dungeon_items)
    world.itempool = ItemFactory(pool)
    for (location, item) in placed_items:
        world.push_item(location, ItemFactory(item), False)
        world.get_location(location).event = True

    fill_bosses(world)
    fill_songs(world)

def get_pool_core(dungeon_items):
    pool = []
    placed_items = []

    if not dungeon_items:
        pool.extend(notmapcompass)
    pool.extend(alwaysitems)
    tradeitem = random.choice(tradeitems)
    pool.append(tradeitem)

    return (pool, placed_items)

def fill_bosses(world, bossCount=8):
    boss_locations = [world.get_location('Queen Gohma'), world.get_location('King Dodongo'), world.get_location('Barinade'), world.get_location('Phantom Ganon'),
                      world.get_location('Volvagia'), world.get_location('Morpha'), world.get_location('Bongo Bongo'), world.get_location('Twinrova')]
    placed_prizes = [loc.item.name for loc in boss_locations if loc.item is not None]
    unplaced_prizes = [item for item in boss_rewards if item.name not in placed_prizes]
    empty_boss_locations = [loc for loc in boss_locations if loc.item is None]
    prizepool = list(unplaced_prizes)
    prize_locs = list(empty_boss_locations)

    while bossCount:
        bossCount -= 1
        random.shuffle(prizepool)
        random.shuffle(prize_locs)
        item = prizepool.pop()
        loc = prize_locs.pop()
        world.push_item(loc, item, False)
        world.get_location(loc).event = True

def fill_songs(world, attempts=15):
    songs = ItemFactory(songlist)
    song_locations = [world.get_location('Song from Composer Grave'), world.get_location('Impa at Castle'), world.get_location('Song from Malon'), world.get_location('Song from Saria'), world.get_location('Song from Ocarina of Time'), world.get_location('Song at Windmill'), world.get_location('Sheik Forest Song'), world.get_location('Sheik at Temple'), world.get_location('Sheik in Crater'), world.get_location('Sheik in Ice Cavern'), world.get_location('Sheik in Kakariko'), world.get_location('Sheik at Colossus')]
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
