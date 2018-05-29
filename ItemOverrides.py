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

            if loc.type == 'Grotto':
                base_item = 'Boomerang'
            elif loc.name == 'Treasure Chest Game':
                base_item = 'Piece of Heart (Treasure Chest Game)'
            elif loc.item.index >= 0x80:
                base_item = available_base_items.pop(0)
                if not base_item:
                    raise RuntimeError('Ran out of base items to override')
            else:
                continue

            if (scene is None):
                raise RuntimeError("Can't place extended item %s in location %s" % (loc.item.name, loc.name))
            loc.base_item = ItemFactory(base_item)
            logging.getLogger('').debug('Override %s -> %s in scene %s', loc.base_item, loc.item, '0x{0:0{1}X}'.format(scene, 2))

def get_overrides(world):
    filled = world.get_locations()
    result = [(loc.scene, loc.base_item.index, loc.item.index) for loc in filled if loc.base_item]
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
