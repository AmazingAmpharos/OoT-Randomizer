from collections import namedtuple
import logging
import random

from Items import ItemFactory

#This file sets the item pools for various modes. Timed modes and triforce hunt are enforced first, and then extra items are specified per mode to fill in the remaining space.
#Some basic items that various modes require are placed here, including pendants and crystals. Medallion requirements for the two relevant entrances are also decided.

alwaysitems = ([
    'Biggoron Sword', 
    'Boomerang', 
    'Lens of Truth', 
    'Hammer', 
    'Iron Boots', 
    'Goron Tunic', 
    'Zora Tunic', 
    'Hover Boots', 
    'Mirror Shield', 
    'Stone of Agony', 
    'Fire Arrows', 
    'Ice Arrows', 
    'Light Arrows', 
    'Dins Fire', 
    'Farores Wind', 
    'Rupee (1)'] 
    + ['Progressive Hookshot'] * 2
    + ['Deku Shield']
    + ['Hylian Shield']
    + ['Progressive Strength Upgrade'] * 3
    + ['Progressive Scale'] * 2
    + ['Recovery Heart'] * 6
    + ['Rupees (5)'] * 13
    + ['Rupees (20)'] * 5
    + ['Rupees (50)'] * 7
    + ['Rupees (200)'] * 3
    + ['Bow'] * 3
    + ['Slingshot'] * 3
    + ['Bomb Bag'] * 3
    + ['Bottle with Letter']
    + ['Bombs (5)'] * 2
    + ['Bombs (10)']
    + ['Bombs (20)']
    + ['Arrows (5)']
    + ['Arrows (10)'] * 5
    + ['Progressive Wallet'] * 2
    + ['Deku Stick Capacity'] * 2
    + ['Deku Nut Capacity'] * 2
    + ['Magic Meter'])

DT_vanilla = (['Recovery Heart'] * 2)

DT_MQ = (['Deku Shield'] * 2
         + ['Rupees (50)'])

DC_vanilla = (['Rupees (20)'])

DC_MQ = (['Hylian Shield']
         + ['Rupees (5)'])

JB_MQ = (['Deku Nuts (5)'] * 4
         + ['Recovery Heart']
         + ['Deku Shield']
         + ['Deku Stick (1)'])

FoT_vanilla = (['Recovery Heart']
               + ['Arrows (10)']
               + ['Arrows (30)'])

FoT_MQ = (['Arrows (5)'])

FiT_vanilla = (['Rupees (200)'])

FiT_MQ = (['Bombs (20)']
          + ['Hylian Shield'])

SpT_vanilla = (['Deku Shield'] * 2
               + ['Recovery Heart']
               + ['Bombs (20)'])

SpT_MQ = (['Rupees (50)'] * 2
          + ['Arrows (30)'])

ShT_vanilla = (['Arrows (30)'])

ShT_MQ = (['Arrows (5)'] * 2
          + ['Rupees (20)'])

BW_vanilla = (['Recovery Heart']
               + ['Bombs (10)']
               + ['Rupees (200)']
               + ['Deku Nuts (5)']
               + ['Deku Nuts (10)']
               + ['Deku Shield']
               + ['Hylian Shield'])

GTG_vanilla = (['Arrows (30)'] * 3
               + ['Rupees (200)'])

GTG_MQ = (['Rupee (Treasure Chest Game)'] * 2
          + ['Arrows (10)']
          + ['Rupee (1)']
          + ['Rupees (50)'])

GC_vanilla = (['Rupees (5)'] * 3
               + ['Arrows (30)'])

GC_MQ = (['Arrows (10)'] * 2
         + ['Bombs (5)']
         + ['Rupees (20)']
         + ['Recovery Heart'])

normal_bottles = [
    'Bottle',
    'Bottle with Milk',
    'Bottle with Red Potion',
    'Bottle with Green Potion',
    'Bottle with Blue Potion',
    'Bottle with Fairy',
    'Bottle with Fish',
    'Bottle with Bugs',
    'Bottle with Poe'] # 'Bottle with Blue Fire'

normal_bottle_count = 3

# 10 items get removed for hard+
harditems = (
    ['Bombs (5)'] * 2 
    + ['Arrows (5)'] * 2 
    + ['Deku Nuts (5)'] * 2 
    + ['Rupees (5)'] * 3 
    + ['Rupees (20)'])

# 37 items get removed for very hard
veryharditems = (
    ['Bombs (5)'] * 8 
    + ['Arrows (5)'] * 8 
    + ['Deku Nuts (5)'] * 8 
    + ['Rupees (5)'] * 10 
    + ['Rupees (20)'] * 2 
    + ['Rupees (50)'])

rewardlist = [
    'Kokiri Emerald',
    'Goron Ruby', 
    'Zora Sapphire', 
    'Forest Medallion', 
    'Fire Medallion', 
    'Water Medallion', 
    'Spirit Medallion', 
    'Shadow Medallion', 
    'Light Medallion']

songlist = [
    'Zeldas Lullaby', 
    'Eponas Song', 
    'Suns Song', 
    'Sarias Song', 
    'Song of Time', 
    'Song of Storms', 
    'Minuet of Forest', 
    'Prelude of Light', 
    'Bolero of Fire', 
    'Serenade of Water', 
    'Nocturne of Shadow', 
    'Requiem of Spirit']

skulltulla_locations = ([
    'GS Kokiri Know It All House',
    'GS Kokiri Bean Patch',
    'GS Kokiri House of Twins',
    'GS Lost Woods Bean Patch Near Bridge',
    'GS Lost Woods Bean Patch Near Stage',
    'GS Lost Woods Above Stage',
    'GS Sacred Forest Meadow',
    'GS Hyrule Field near Kakariko',
    'GS Hyrule Field Near Gerudo Valley',
    'GS Castle Market Guard House',
    'GS Hyrule Castle Tree',
    'GS Hyrule Castle Grotto',
    'GS Outside Ganon\'s Castle',
    'GS Lon Lon Ranch Tree',
    'GS Lon Lon Ranch Rain Shed',
    'GS Lon Lon Ranch House Window',
    'GS Lon Lon Ranch Back Wall',
    'GS Kakariko House Under Construction',
    'GS Kakariko Skulltula House',
    'GS Kakariko Guard\'s House',
    'GS Kakariko Tree',
    'GS Kakariko Watchtower',
    'GS Kakariko Above Impa\'s House',
    'GS Graveyard Wall',
    'GS Graveyard Bean Patch',
    'GS Mountain Trail Bean Patch',
    'GS Mountain Trail Bomb Alcove',
    'GS Mountain Trail Path to Crater',
    'GS Mountain Trail Above Dodongo\'s Cavern',
    'GS Goron City Boulder Maze',
    'GS Goron City Center Platform',
    'GS Death Mountain Crater Crate',
    'GS Mountain Crater Bean Patch',
    'GS Zora River Ladder',
    'GS Zora River Tree',
    'GS Zora River Near Raised Grottos',
    'GS Zora River Above Bridge',
    'GS Zora\'s Domain Frozen Waterfall',
    'GS Zora\'s Fountain Tree',
    'GS Zora\'s Fountain Above the Log',
    'GS Zora\'s Fountain Hidden Cave',
    'GS Lake Hylia Bean Patch',
    'GS Lake Hylia Lab Wall',
    'GS Lake Hylia Small Island',
    'GS Lake Hylia Giant Tree',
    'GS Lab Underwater Crate',
    'GS Gerudo Valley Small Bridge',
    'GS Gerudo Valley Bean Patch',
    'GS Gerudo Valley Behind Tent',
    'GS Gerudo Valley Pillar',
    'GS Gerudo Fortress Archery Range',
    'GS Gerudo Fortress Top Floor',
    'GS Wasteland Ruins',
    'GS Desert Colossus Bean Patch',
    'GS Desert Colossus Tree',
    'GS Desert Colossus Hill'])
    
tradeitems = [
    'Pocket Egg',
    'Pocket Cucco', 
    'Cojiro', 
    'Odd Mushroom', 
    'Poachers Saw', 
    'Broken Sword', 
    'Prescription', 
    'Eyeball Frog', 
    'Eyedrops', 
    'Claim Check']


eventlocations = {
    'Ganon': 'Triforce',
    'Zeldas Letter': 'Zeldas Letter',
    'Magic Bean Salesman': 'Magic Bean',
    'King Zora Moves': 'Bottle',
    'Master Sword Pedestal': 'Master Sword',
    'Epona': 'Epona',
    'Gerudo Fortress Carpenter Rescue': 'Carpenter Rescue',
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
        
    if world.shuffle_kokiri_sword:
        pool.append('Kokiri Sword')
    else:
        placed_items['Kokiri Sword Chest'] = 'Kokiri Sword'

    if world.shuffle_weird_egg:
        pool.append('Weird Egg')
    else:
        placed_items['Malon Egg'] = 'Weird Egg'

    if world.shuffle_ocarinas:
        pool.extend(['Ocarina'] * 2)
    else:
        placed_items['Gift from Saria'] = 'Ocarina'
        placed_items['Ocarina of Time'] = 'Ocarina'

    if world.dungeon_mq['DT']:
        skulltulla_locations_final = skulltulla_locations + [
            'GS Deku Tree MQ Lobby',
            'GS Deku Tree MQ Compass Room',
            'GS Deku Tree MQ Basement Ceiling',
            'GS Deku Tree MQ Basement Back Room']
    else:
        skulltulla_locations_final = skulltulla_locations + [
            'GS Deku Tree Compass Room',
            'GS Deku Tree Basement Vines',
            'GS Deku Tree Basement Gate',
            'GS Deku Tree Basement Back Room']
    if world.dungeon_mq['DC']:
        skulltulla_locations_final.extend([
            'GS Dodongo\'s Cavern MQ Scrub Room',
            'GS Dodongo\'s Cavern MQ Song of Time Block Room',
            'GS Dodongo\'s Cavern MQ Lizalfos Room',
            'GS Dodongo\'s Cavern MQ Larva Room',
            'GS Dodongo\'s Cavern MQ Back Area'])
    else:
        skulltulla_locations_final.extend([
            'GS Dodongo\'s Cavern East Side Room',
            'GS Dodongo\'s Cavern Vines Above Stairs',
            'GS Dodongo\'s Cavern Back Room',
            'GS Dodongo\'s Cavern Alcove Above Stairs',
            'GS Dodongo\'s Cavern Scarecrow'])
    if world.dungeon_mq['JB']:
        skulltulla_locations_final.extend([
            'GS Jabu Jabu MQ Tailpasaran Room',
            'GS Jabu Jabu MQ Invisible Enemies Room',
            'GS Jabu Jabu MQ Boomerang Room',
            'GS Jabu Jabu MQ Near Boss'])
    else:
        skulltulla_locations_final.extend([
            'GS Jabu Jabu Water Switch Room',
            'GS Jabu Jabu Lobby Basement Lower',
            'GS Jabu Jabu Lobby Basement Upper',
            'GS Jabu Jabu Near Boss'])
    if world.dungeon_mq['FoT']:
        skulltulla_locations_final.extend([
            'GS Forest Temple MQ First Hallway',
            'GS Forest Temple MQ Block Push Room',
            'GS Forest Temple MQ Outdoor East',
            'GS Forest Temple MQ Outdoor West',
            'GS Forest Temple MQ Well'])
    else:
        skulltulla_locations_final.extend([
            'GS Forest Temple First Room',
            'GS Forest Temple Lobby',
            'GS Forest Temple Outdoor East',
            'GS Forest Temple Outdoor West',
            'GS Forest Temple Basement'])
    if world.dungeon_mq['FiT']:
        skulltulla_locations_final.extend([
            'GS Fire Temple MQ Above Fire Wall Maze',
            'GS Fire Temple MQ Fire Wall Maze Center',
            'GS Fire Temple MQ Big Lava Room',
            'GS Fire Temple MQ Fire Wall Maze Side Room',
            'GS Fire Temple MQ East Tower Top'])
    else:
        skulltulla_locations_final.extend([
            'GS Fire Temple Song of Time Room',
            'GS Fire Temple Unmarked Bomb Wall',
            'GS Fire Temple East Tower Climb',
            'GS Fire Temple East Tower Top',
            'GS Fire Temple Basement'])
    if world.dungeon_mq['WT']:
        skulltulla_locations_final.extend([
            'GS Water Temple MQ Before Upper Water Switch',
            'GS Water Temple MQ North Basement',
            'GS Water Temple MQ Lizalfos Hallway',
            'GS Water Temple MQ Serpent River',
            'GS Water Temple MQ South Basement'])
    else:
        skulltulla_locations_final.extend([
            'GS Water Temple South Basement',
            'GS Water Temple Serpent River',
            'GS Water Temple Falling Platform Room',
            'GS Water Temple Central Room',
            'GS Water Temple Near Boss Key Chest'])
    if world.dungeon_mq['SpT']:
        skulltulla_locations_final.extend([
            'GS Spirit Temple MQ Lower Adult Right',
            'GS Spirit Temple MQ Lower Adult Left',
            'GS Spirit Temple MQ Iron Knuckle West',
            'GS Spirit Temple MQ Iron Knuckle North',
            'GS Spirit Temple MQ Sun Block Room'])
    else:
        skulltulla_locations_final.extend([
            'GS Spirit Temple Metal Fence',
            'GS Spirit Temple Bomb for Light Room',
            'GS Spirit Temple Hall to West Iron Knuckle',
            'GS Spirit Temple Boulder Room',
            'GS Spirit Temple Lobby'])
    if world.dungeon_mq['ShT']:
        skulltulla_locations_final.extend([
            'GS Shadow Temple MQ Crusher Room',
            'GS Shadow Temple MQ Wind Hint Room',
            'GS Shadow Temple MQ After Wind',
            'GS Shadow Temple MQ After Ship',
            'GS Shadow Temple MQ Near Boss'])
    else:
        skulltulla_locations_final.extend([
            'GS Shadow Temple Like Like Room',
            'GS Shadow Temple Crusher Room',
            'GS Shadow Temple Single Giant Pot',
            'GS Shadow Temple Near Ship',
            'GS Shadow Temple Tripple Giant Pot'])
    if world.dungeon_mq['BW']:
        skulltulla_locations_final.extend([
            'GS Well MQ Basement',
            'GS Well MQ Coffin Room',
            'GS Well MQ West Inner Room'])
    else:
        skulltulla_locations_final.extend([
            'GS Well West Inner Room',
            'GS Well East Inner Room',
            'GS Well Like Like Cage'])
    if world.dungeon_mq['IC']:
        skulltulla_locations_final.extend([
            'GS Ice Cavern MQ Scarecrow',
            'GS Ice Cavern MQ Ice Block',
            'GS Ice Cavern MQ Red Ice'])
    else:
        skulltulla_locations_final.extend([
            'GS Ice Cavern Spinning Scythe Room',
            'GS Ice Cavern Heart Piece Room',
            'GS Ice Cavern Push Block Room'])
    if world.tokensanity == 'off':
        for location in skulltulla_locations_final:
            placed_items[location] = 'Gold Skulltulla Token'
    elif world.tokensanity == 'dungeons':
        for location in skulltulla_locations_final:
            if world.get_location(location).scene >= 0x0A:
                placed_items[location] = 'Gold Skulltulla Token'
            else:
                pool.append('Gold Skulltulla Token')
    else:
        pool.extend(['Gold Skulltulla Token'] * 100)

    if world.bombchus_in_logic:
        pool.extend(['Bombchus'] * 4)
        if world.dungeon_mq['JB']:
            pool.extend(['Bombchus'])
        if world.dungeon_mq['SpT']:
            pool.extend(['Bombchus'] * 2)
        if not world.dungeon_mq['BW']:
            pool.extend(['Bombchus'])
        if world.dungeon_mq['GTG']:
            pool.extend(['Bombchus'])
    else:
        pool.extend(['Bombchus (5)'] + ['Bombchus (10)'] * 2)
        if world.dungeon_mq['JB']:
            pool.extend(['Bombchus (10)'])
        if world.dungeon_mq['SpT']:
            pool.extend(['Bombchus (10)'] * 2)
        if not world.dungeon_mq['BW']:
            pool.extend(['Bombchus (10)'])
        if world.dungeon_mq['GTG']:
            pool.extend(['Bombchus (10)'])
        if world.dungeon_mq['GC']:
            pool.extend(['Bombchus (10)'])
        else:
            pool.extend(['Bombchus (20)'])

    if world.difficulty == 'ohko':
        pool.extend(['Recovery Heart'])
        if not world.dungeon_mq['GTG']:
            pool.extend(['Recovery Heart'])
        if not world.dungeon_mq['GC']:
            pool.extend(['Recovery Heart'] * 4)
    else:
        pool.extend(['Ice Trap'])
        if not world.dungeon_mq['GTG']:
            pool.extend(['Ice Trap'])
        if not world.dungeon_mq['GC']:
            pool.extend(['Ice Trap'] * 4)

    if world.difficulty == 'normal':
        pool.extend(['Magic Meter', 'Double Defense'] + ['Heart Container'] * 8)
    else:
        pool.extend(harditems)

    if world.difficulty == 'very_hard' or world.difficulty == 'ohko':
        pool.extend(veryharditems)
    else:
        pool.extend(['Nayrus Love', 'Piece of Heart (Treasure Chest Game)'] + ['Piece of Heart'] * 35)

    if world.gerudo_fortress == 'open':
        placed_items['Gerudo Fortress North F1 Carpenter'] = 'Recovery Heart'
        placed_items['Gerudo Fortress North F2 Carpenter'] = 'Recovery Heart'
        placed_items['Gerudo Fortress South F1 Carpenter'] = 'Recovery Heart'
        placed_items['Gerudo Fortress South F2 Carpenter'] = 'Recovery Heart'
    elif world.keysanity:
        if world.gerudo_fortress == 'fast':
            pool.append('Small Key (Gerudo Fortress)')
            placed_items['Gerudo Fortress North F2 Carpenter'] = 'Recovery Heart'
            placed_items['Gerudo Fortress South F1 Carpenter'] = 'Recovery Heart'
            placed_items['Gerudo Fortress South F2 Carpenter'] = 'Recovery Heart'
        else:
            pool.extend(['Small Key (Gerudo Fortress)'] * 4)
    else:
        if world.gerudo_fortress == 'fast':
            placed_items['Gerudo Fortress North F1 Carpenter'] = 'Small Key (Gerudo Fortress)'
            placed_items['Gerudo Fortress North F2 Carpenter'] = 'Recovery Heart'
            placed_items['Gerudo Fortress South F1 Carpenter'] = 'Recovery Heart'
            placed_items['Gerudo Fortress South F2 Carpenter'] = 'Recovery Heart'
        else:
            placed_items['Gerudo Fortress North F1 Carpenter'] = 'Small Key (Gerudo Fortress)'
            placed_items['Gerudo Fortress North F2 Carpenter'] = 'Small Key (Gerudo Fortress)'
            placed_items['Gerudo Fortress South F1 Carpenter'] = 'Small Key (Gerudo Fortress)'
            placed_items['Gerudo Fortress South F2 Carpenter'] = 'Small Key (Gerudo Fortress)'

    if world.shuffle_gerudo_card and world.gerudo_fortress != 'open':
        pool.append('Gerudo Membership Card')
    else:
        placed_items['Gerudo Fortress Membership Card'] = 'Gerudo Membership Card'


    pool.extend(alwaysitems)
    if world.dungeon_mq['DT']:
        pool.extend(DT_MQ)
    else:
        pool.extend(DT_vanilla)
    if world.dungeon_mq['DC']:
        pool.extend(DC_MQ)
    else:
        pool.extend(DC_vanilla)
    if world.dungeon_mq['JB']:
        pool.extend(JB_MQ)
    if world.dungeon_mq['FoT']:
        pool.extend(FoT_MQ)
    else:
        pool.extend(FoT_vanilla)
    if world.dungeon_mq['FiT']:
        pool.extend(FiT_MQ)
    else:
        pool.extend(FiT_vanilla)
    if world.dungeon_mq['SpT']:
        pool.extend(SpT_MQ)
    else:
        pool.extend(SpT_vanilla)
    if world.dungeon_mq['ShT']:
        pool.extend(ShT_MQ)
    else:
        pool.extend(ShT_vanilla)
    if not world.dungeon_mq['BW']:
        pool.extend(BW_vanilla)
    if world.dungeon_mq['GTG']:
        pool.extend(GTG_MQ)
    else:
        pool.extend(GTG_vanilla)
    if world.dungeon_mq['GC']:
        pool.extend(GC_MQ)
    else:
        pool.extend(GC_vanilla)
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
    boss_locations = [
        world.get_location('Queen Gohma'), 
        world.get_location('King Dodongo'), 
        world.get_location('Barinade'), 
        world.get_location('Phantom Ganon'),
        world.get_location('Volvagia'), 
        world.get_location('Morpha'), 
        world.get_location('Bongo Bongo'), 
        world.get_location('Twinrova'), 
        world.get_location('Links Pocket')]

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
