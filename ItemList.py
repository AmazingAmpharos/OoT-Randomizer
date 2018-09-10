from collections import namedtuple
import logging
import random

from Items import ItemFactory
from Fill import FillError, fill_restrictive

#This file sets the item pools for various modes. Timed modes and triforce hunt are enforced first, and then extra items are specified per mode to fill in the remaining space.
#Some basic items that various modes require are placed here, including pendants and crystals. Medallion requirements for the two relevant entrances are also decided.

alwaysitems = (['Gilded Sword', 'Fierce Deity Mask', 'Hookshot', 'Lens of Truth', 'Powder Keg', 'Deku Mask', 'Goron Mask', 'Zora Mask', 'Mirror Shield', 'Fire Arrows', 'Ice Arrows', 'Light Arrows'] +
              ['Postmans Hat', 'Blast Mask', 'Great Fairy Mask', 'All Night Mask', 'Stone Mask'] + ['Keaton Mask', 'Bremen Mask', 'Bunny Hood', 'Don Geros Mask', 'Mask of Scents'] +
              ['Romani Mask', 'Circus Leader Mask', 'Couple Mask', 'Mask of Truth'] + ['Kamaros Mask', 'Garo Mask', 'Captains Hat', 'Gibdo Mask', 'Giant Mask'] +
              ['Bow'] * 3 + ['Bomb Bag'] * 3 + ['Bottle'] * 2 + ['Bottle with Gold Dust'] + ['Bottle with Red Potion'] + ['Bottle with Milk'] + ['Bottle with Chateau Romani'] +
              ['Deku Nuts (10)'] + ['Piece of Heart'] * 14 + ['Piece of Heart (Free)'] * 4 + ['Rupees (5)'] + ['Rupees (20)'] + ['Rupees (100)'] * 4 + ['Rupees (50)'] * 6 +
              ['Pictograph Box'])
              #['Hylian Shield'] * 2 + ['Progressive Wallet'] * 2) + ['Great Fairy Sword'] + ['Ice Trap'] * 6 +
              #['Bombs (5)'] * 2 + ['Bombs (10)'] * 2 + ['Bombs (20)'] + ['Bombchus (5)'] + ['Bombchus (10)'] * 3 + ['Bombchus (20)'] + ['Arrows (5)'] + ['Arrows (10)'] * 6 + ['Arrows (30)'] * 6 +
              #['Deku Nuts (5)']
notmapcompass = ['Rupees (5)'] * 20
rewardlist = ['Odolwa Remains', 'Goht Remains', 'Gyorg Remains', 'Twinmold Remains']
songlist = ['Song of Time', 'Song of Healing', 'Song of Soaring', 'Eponas Song','Song of Storms', 'Sonata of Awakening', 'Goron Lullaby', 'New Wave Bossa Nova', 'Elegy of Emptiness', 'Oath to Order']
stray_fairy_locations = (['WF-SF1', 'WF-SF2', 'WF-SF3', 'WF-SF4', 'WF-SF5', 'WF-SF6', 'WF-SF7', 'WF-SF8', 'WF-SF9', 'WF-SF10', 'WF-SF11', 'WF-SF12', 'WF-SF13', 'WF-SF14', 'WF-SF15'] +
                        ['SH-SF1', 'SH-SF2', 'SH-SF3', 'SH-SF4', 'SH-SF5', 'SH-SF6', 'SH-SF7', 'SH-SF8', 'SH-SF9', 'SH-SF10', 'SH-SF11', 'SH-SF12', 'SH-SF13', 'SH-SF14', 'SH-SF15'] +
                        ['GB-SF1', 'GB-SF2', 'GB-SF3', 'GB-SF4', 'GB-SF5', 'GB-SF6', 'GB-SF7', 'GB-SF8', 'GB-SF9', 'GB-SF10', 'GB-SF11', 'GB-SF12', 'GB-SF13', 'GB-SF14', 'GB-SF15'] +
                        ['ST-SF1', 'ST-SF2', 'ST-SF3', 'ST-SF4', 'ST-SF5', 'ST-SF6', 'ST-SF7', 'ST-SF8', 'ST-SF9', 'ST-SF10', 'ST-SF11', 'ST-SF12', 'ST-SF13', 'ST-SF14', 'ST-SF15'])
tradeitems = (['Moon Tear', 'Town Title Deed', 'Swamp Title Deed', 'Mountain Title Deed', 'Ocean Title Deed'] +
                ['Room Key', 'Letter to Kafei', 'Pendant of Memories', 'Letter to Mama'] +
                []) # Will fill properly when I find out which slots are actually shared for the above

#total_items_to_place = 5

def generate_itempool(world):

    world.push_item('Majoras Wrath', ItemFactory('Majora Mask'), False)
    world.get_location('Majoras Wrath').event = True
    world.push_item('Gift from Skull Kid', ItemFactory('Fairy Ocarina'), False)
    world.get_location('Gift from Skull Kid').event = True

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

def fill_bosses(world, bossCount=4):
    boss_rewards = ItemFactory(rewardlist)
    boss_locations = [world.get_location('Odolwa'), world.get_location('Goht'), world.get_location('Gyorg'), world.get_location('Twinmold')]
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
    song_locations = [world.get_location('Song from Skull Kid'), world.get_location('Song from HMS'), world.get_location('Song from Owl Tablet'), world.get_location('Song from Romani'), world.get_location('Song at Grave'), world.get_location('Song from Monkey'), world.get_location('Song from Baby Goron'), world.get_location('Song from Goron Elder'), world.get_location('Song from Zora Eggs'), world.get_location('Song from Igos'), world.get_location('Song from the Giants')]
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
