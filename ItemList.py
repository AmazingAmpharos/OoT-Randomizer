from collections import namedtuple
import logging
import random

from Items import ItemFactory

#This file sets the item pools for various modes. Timed modes and triforce hunt are enforced first, and then extra items are specified per mode to fill in the remaining space.
#Some basic items that various modes require are placed here, including pendants and crystals. Medallion requirements for the two relevant entrances are also decided.

alwaysitems = (['Kokiri Sword', 'Biggoron Sword', 'Boomerang', 'Lens of Truth', 'Hammer', 'Iron Boots', 'Goron Tunic', 'Zora Tunic', 'Hover Boots', 'Mirror Shield', 'Stone of Agony', 'Fire Arrows', 'Ice Arrows', 'Light Arrows', 'Dins Fire', 'Farores Wind', 'Nayrus Love', 'Rupee (1)'] + ['Progressive Hookshot'] * 2 + ['Deku Shield'] * 4 +  ['Hylian Shield'] * 2 + ['Ice Trap'] * 6 +
              ['Progressive Strength Upgrade'] * 3 + ['Progressive Scale'] * 2 + ['Piece of Heart'] * 35 + ['Recovery Heart'] * 11 + ['Rupees (5)'] * 17 + ['Rupees (20)'] * 5 + ['Rupees (50)'] * 7 + ['Rupees (200)'] * 6 + ['Bow'] * 3 + ['Slingshot'] * 3 + ['Bomb Bag'] * 3 + ['Bottle with Letter'] + ['Heart Container'] * 8 + ['Piece of Heart (Treasure Chest Game)'] +
              ['Bombs (5)'] * 2 + ['Bombs (10)'] * 2 + ['Bombs (20)'] * 2 + ['Arrows (5)'] + ['Arrows (10)'] * 6 + ['Arrows (30)'] * 6 + ['Deku Nuts (5)'] + ['Deku Nuts (10)'] + ['Progressive Wallet'] * 2 + ['Deku Stick Capacity'] * 2 + ['Deku Nut Capacity'] * 2 + ['Magic Meter'] * 2 + ['Double Defense'])
# normal_bottles = ['Bottle', 'Bottle with Milk', 'Bottle with Red Potion', 'Bottle with Green Potion', 'Bottle with Blue Potion', 'Bottle with Fairy', 'Bottle with Fish', 'Bottle with Blue Fire', 'Bottle with Bugs', 'Bottle with Poe']
normal_bottles = ['Bottle', 'Bottle with Milk', 'Bottle with Red Potion', 'Bottle with Green Potion', 'Bottle with Blue Potion', 'Bottle with Fairy', 'Bottle with Fish', 'Bottle with Bugs', 'Bottle with Poe']
normal_bottle_count = 3
# notmapcompass = ['Rupees (5)'] * 20
notmapcompass = ['Bombs (5)'] * 4 + ['Arrows (5)'] * 3 + ['Deku Nuts (5)'] * 3 + ['Rupees (5)'] * 7 + ['Rupees (20)'] * 2 + ['Rupees (50)']
rewardlist = ['Kokiri Emerald', 'Goron Ruby', 'Zora Sapphire', 'Forest Medallion', 'Fire Medallion', 'Water Medallion', 'Spirit Medallion', 'Shadow Medallion', 'Light Medallion']
songlist = ['Zeldas Lullaby', 'Eponas Song', 'Suns Song', 'Sarias Song', 'Song of Time', 'Song of Storms', 'Minuet of Forest', 'Prelude of Light', 'Bolero of Fire', 'Serenade of Water', 'Nocturne of Shadow', 'Requiem of Spirit']
skulltulla_locations = (['GS Kokiri Know It All House', 'GS Kokiri Bean Patch', 'GS Kokiri House of Twins', 'GS Lost Woods Bean Patch Near Bridge', 'GS Lost Woods Bean Patch Near Stage', 'GS Lost Woods Above Stage', 'GS Sacred Forest Meadow', 'GS Deku Tree Compass Room', 'GS Deku Tree Basement Vines', 'GS Deku Tree Basement Gate', 'GS Deku Tree Basement Back Room', 'GS Hyrule Field near Kakariko', 'GS Hyrule Field Near Gerudo Valley', 'GS Castle Market Guard House', 'GS Hyrule Castle Tree', 'GS Hyrule Castle Grotto', 'GS Outside Ganon\'s Castle', 'GS Lon Lon Ranch Tree', 'GS Lon Lon Ranch Rain Shed', 'GS Lon Lon Ranch House Window'] +
                       ['GS Lon Lon Ranch Back Wall', 'GS Kakariko House Under Construction', 'GS Kakariko Skulltula House', 'GS Kakariko Guard\'s House', 'GS Kakariko Tree', 'GS Kakariko Watchtower', 'GS Kakariko Above Impa\'s House', 'GS Graveyard Wall', 'GS Graveyard Bean Patch', 'GS Mountain Trail Bean Patch', 'GS Mountain Trail Bomb Alcove', 'GS Mountain Trail Path to Crater', 'GS Mountain Trail Above Dodongo\'s Cavern', 'GS Goron City Boulder Maze', 'GS Goron City Center Platform', 'GS Death Mounter Crater Crate', 'GS Death Mounter Bean Patch', 'GS Dodongo\'s Cavern East Side Room', 'GS Dodongo\'s Cavern Vines Above Stairs', 'GS Dodongo\'s Cavern Back Room'] +
                       ['GS Dodongo\'s Cavern Alcove Above Stairs', 'GS Dodongo\'s Cavern Scarecrow', 'GS Zora River Ladder', 'GS Zora River Tree', 'GS Zora River Near Raised Grottos', 'GS Zora River Above Bridge', 'GS Zora\'s Domain Frozen Waterfall', 'GS Zora\'s Fountain Tree', 'GS Zora\'s Fountain Above the Log', 'GS Zora\'s Fountain Hidden Cave', 'GS Jabu Jabu Water Switch Room', 'GS Jabu Jabu Lobby Basement Lower', 'GS Jabu Jabu Lobby Basement Upper', 'GS Jabu Jabu Near Boss', 'GS Lake Hylia Bean Patch', 'GS Lake Hylia Lab Wall', 'GS Lake Hylia Small Island', 'GS Lake Hylia Giant Tree', 'GS Lab Underwater Crate', 'GS Forest Temple First Room'] +
                       ['GS Forest Temple Lobby', 'GS Forest Temple Outdoor East', 'GS Forest Temple Outdoor West', 'GS Forest Temple Basement', 'GS Fire Temple Song of Time Room', 'GS Fire Temple Unmarked Bomb Wall', 'GS Fire Temple East Tower Climb', 'GS Fire Temple East Tower Top', 'GS Fire Temple Basement', 'GS Ice Cavern Spinning Scythe Room', 'GS Ice Cavern Heart Piece Room', 'GS Ice Cavern Push Block Room', 'GS Water Temple South Basement', 'GS Water Temple Serpent River', 'GS Water Temple Falling Platform Room', 'GS Water Temple Central Room', 'GS Water Temple Near Boss Key Chest', 'GS Well West Inner Room', 'GS Well East Inner Room', 'GS Well Like Like Cage'] +
                       ['GS Shadow Temple Like Like Room', 'GS Shadow Temple Crusher Room', 'GS Shadow Temple Single Giant Pot', 'GS Shadow Temple Near Ship', 'GS Shadow Temple Tripple Giant Pot', 'GS Gerudo Valley Small Bridge', 'GS Gerudo Valley Bean Patch', 'GS Gerudo Valley Behind Tent', 'GS Gerudo Valley Pillar', 'GS Gerudo Fortress Archery Range', 'GS Gerudo Fortress Top Floor', 'GS Wasteland Ruins', 'GS Desert Colossus Bean Patch', 'GS Desert Colossus Tree', 'GS Desert Colossus Hill', 'GS Spirit Temple Metal Fence', 'GS Spirit Temple Bomb for Light Room', 'GS Spirit Temple Hall to West Iron Knuckle', 'GS Spirit Temple Boulder Room', 'GS Spirit Temple Lobby'])
tradeitems = ['Pocket Egg', 'Pocket Cucco', 'Cojiro', 'Odd Mushroom', 'Poachers Saw', 'Broken Sword', 'Prescription', 'Eyeball Frog', 'Eyedrops', 'Claim Check']

eventlocations = {
    'Ganon': 'Triforce',
    'Zeldas Letter': 'Zeldas Letter',
    'Magic Bean Salesman': 'Magic Bean',
    'King Zora Moves': 'Bottle',
    'Master Sword Pedestal': 'Master Sword',
    'Epona': 'Epona',
    'Gerudo Fortress Carpenter Rescue': 'Gerudo Membership Card',
    'Ganons Castle Forest Trial Clear': 'Forest Trial Clear',
    'Ganons Castle Fire Trial Clear': 'Fire Trial Clear',
    'Ganons Castle Water Trial Clear': 'Water Trial Clear',
    'Ganons Castle Shadow Trial Clear': 'Shadow Trial Clear',
    'Ganons Castle Spirit Trial Clear': 'Spirit Trial Clear',
    'Ganons Castle Light Trial Clear': 'Light Trial Clear'
}

#total_items_to_place = 5

def generate_itempool(world):
    for location, item in eventlocations.items():
        world.push_item(location, ItemFactory(item))
        world.get_location(location).event = True

    # set up item pool
    (pool, placed_items) = get_pool_core(world)
    world.itempool = ItemFactory(pool)
    for (location, item) in placed_items.items():
        world.push_item(location, ItemFactory(item))
        world.get_location(location).event = True

    choose_trials(world)
    fill_bosses(world)

    world.initialize_items()


def get_pool_core(world):
    pool = []
    placed_items = {}

    if not world.place_dungeon_items:
        pool.extend(notmapcompass)

    if world.shuffle_weird_egg:
        pool.append('Weird Egg')
    else:
        placed_items['Malon Egg'] = 'Weird Egg'

    if world.shuffle_ocarinas:
        pool.extend(['Ocarina'] * 2)
    else:
        placed_items['Gift from Saria'] = 'Ocarina'
        placed_items['Ocarina of Time'] = 'Ocarina'

    if world.tokensanity == 'off':
        for location in skulltulla_locations:
            placed_items[location] = 'Gold Skulltulla Token'
    elif world.tokensanity == 'dungeons':
        for location in skulltulla_locations:
            if world.get_location(location).scene >= 0x0A:
                placed_items[location] = 'Gold Skulltulla Token'
            else:
                pool.append('Gold Skulltulla Token')
    else:
        pool.extend(['Gold Skulltulla Token'] * 100)

    if world.progressive_bombchus:
        pool.extend(['Bombchus'] * 5)
    else:
        pool.extend(['Bombchus (5)'] + ['Bombchus (10)'] * 3 + ['Bombchus (20)'])

    pool.extend(alwaysitems)
    for _ in range(normal_bottle_count):
        bottle = random.choice(normal_bottles)
        pool.append(bottle)
    tradeitem = random.choice(tradeitems)
    pool.append(tradeitem)
    pool.extend(songlist)

    return (pool, placed_items)

def choose_trials(world):
    num_trials = int(world.trials)
    choosen_trials = random.sample(['Forest', 'Fire', 'Water', 'Spirit', 'Shadow', 'Light'], num_trials)
    for trial in world.skipped_trials:
        if trial not in choosen_trials:
            world.skipped_trials[trial] = True

def fill_bosses(world, bossCount=9):
    boss_rewards = ItemFactory(rewardlist)
    boss_locations = [world.get_location('Queen Gohma'), world.get_location('King Dodongo'), world.get_location('Barinade'), world.get_location('Phantom Ganon'),
                      world.get_location('Volvagia'), world.get_location('Morpha'), world.get_location('Bongo Bongo'), world.get_location('Twinrova'), world.get_location('Links Pocket')]
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
        world.push_item(loc, item)
