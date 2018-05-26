import itertools

from Items import ItemFactory


def set_overrides(world):
    filled = world.get_filled_locations()
    by_scene = {}
    for loc in filled:
        locations = by_scene.get(loc.scene, [])
        locations.append(loc)
        by_scene[loc.scene] = locations

    for scene, locations in by_scene.items():
        used_items = [loc.item.name for loc in locations]
        available_base_items = [item for item in valid_base_items if item not in used_items]
        for loc in locations:
            if loc.item.index is None:
                continue

            if loc.type == 'Grotto':
                base_item = "Bombs (20)"
            elif loc.item.index >= 0x80:
                base_item = available_base_items.pop(0)
                if not base_item:
                    raise RuntimeError('Ran out of base items to override')
            else:
                continue

            if (scene is None):
                raise RuntimeError("Can't place extended item %s in location %s" % (loc.item.name, loc.name))
            loc.base_item = ItemFactory(base_item)

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
    'Bottle with Letter',
    'Bottle with Milk',
    'Stone of Agony',
    'Fire Arrows',
    'Ice Arrows',
    'Light Arrows',
    'Dins Fire',
    'Farores Wind',
    'Nayrus Love',
    'Mirror Shield',
    'Iron Boots',
    'Hover Boots',
    'Keaton Mask',
    'Skull Mask',
    'Spooky Mask',
    'Bunny Hood',
    'Mask of Truth',
    'Goron Mask',
    'Zora Mask',
    'Gerudo Mask',
]
