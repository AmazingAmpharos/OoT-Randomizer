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
        base_items = list(valid_base_items)
        used_items = [loc.item.name for loc in locations]
        available_base_items = [item for item in base_items if item not in used_items]
        for loc in locations:
            if loc.item.index is None:
                continue

            if loc.type == 'Grotto':
                base_item = "Bombs (20)"
            elif (0x89 <= loc.item.index <= 0x91) and (loc.scene == 0x3D or loc.name == "Zelda"):
                # Temporary hack: Zelda and Great Fairies can't currently accept extended items,
                # so if an extended bottle was placed there, replace it with milk.
                loc.item = ItemFactory("Bottle with Milk")
                loc.item.location = loc
                continue
            elif loc.item.index >= 0x80:
                base_item = available_base_items.pop(0)
                if not base_item:
                    raise RuntimeError('Ran out of base items to override')
            else:
                continue

            if (scene is None):
                raise RuntimeError("Can't place extended item %s in location %s" % (loc.item.name, loc.name))
            loc.override_item = loc.item
            loc.item = ItemFactory(base_item)
            loc.item.location = loc

def get_overrides(world):
    filled = world.get_locations()
    result = [(loc.scene, loc.item.index, loc.override_item.index) for loc in filled if loc.override_item]
    result.sort()
    return result

valid_base_items = [
    "Hammer",
    "Boomerang",
    "Lens of Truth",
    "Dins Fire",
    "Farores Wind",
    "Nayrus Love",
    "Fire Arrows",
    "Ice Arrows",
    "Light Arrows",
    "Bottle",
    "Bottle with Letter",
    "Bottle with Milk",
    "Mirror Shield",
    "Iron Boots",
    "Hover Boots",
    "Stone of Agony",
    "Arrows (30)",
    "Bombs (20)",
    "Bombchus (20)",
    "Pocket Egg",
    "Cojiro",
    "Odd Potion",
    "Poachers Saw",
    "Claim Check",
]
