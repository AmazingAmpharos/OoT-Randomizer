import logging

from Items import ItemFactory


def set_overrides(world):
    filled = world.get_filled_locations()
    by_scene = {}
    for loc in filled:
        if loc.scene is None:
            continue
        locations = by_scene.get(loc.scene, [])
        locations.append(loc)
        by_scene[loc.scene] = locations

    for scene, locations in sorted(by_scene.items()):
        used_items = [loc.item.name for loc in locations]
        available_base_items = [item for item in valid_base_items if item not in used_items]
        for loc in locations:
            if loc.item.index is None:
                continue

            base_item = None
            collectable_flag = None

            if loc.type == 'Collectable':
                collectable_flag = loc.default
            elif loc.type == 'Grotto':
                base_item = 'Boomerang'
            elif loc.name == 'Treasure Chest Game':
                base_item = 'Piece of Heart (Treasure Chest Game)'
            elif loc.type == 'BossHeart':
                base_item = 'Heart Container (Boss)'
            elif loc.item.index >= 0x80:
                base_item = available_base_items.pop(0)
                if not base_item:
                    raise RuntimeError('Ran out of base items to override')
            else:
                continue

            if base_item:
                loc.base_item = ItemFactory(base_item)
                logging.getLogger('').debug('Override %s -> %s in scene %s', loc.base_item, loc.item, '0x{0:0{1}X}'.format(scene, 2))

            byte1 = loc.scene
            byte2 = collectable_flag or loc.base_item.index
            byte3 = 0x01 if collectable_flag else 0x00
            byte4 = loc.item.index
            loc.override_bytes = [byte1, byte2, byte3, byte4]

def get_overrides(world):
    filled = world.get_locations()
    result = [loc.override_bytes for loc in filled if loc.override_bytes]
    result.sort()
    return result

valid_base_items = [
    'Boomerang',
    'Lens of Truth',
    'Hammer',
    'Bottle',
    'Bottle with Milk',
    'Bottle with Letter',
    'Skull Mask',
    'Spooky Mask',
    'Keaton Mask',
    'Bunny Hood',
    'Mask of Truth',
    'Mirror Shield',
    'Iron Boots',
    'Hover Boots',
    'Stone of Agony',
    'Goron Mask',
    'Zora Mask',
    'Gerudo Mask',
    'Fire Arrows',
    'Ice Arrows',
    'Light Arrows',
    'Dins Fire',
    'Farores Wind',
    'Nayrus Love',
]
