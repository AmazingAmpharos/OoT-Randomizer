from ItemList import item_table

class Item(object):

    def __init__(self, name='', advancement=False, priority=False, type=None, code=None, index=None, object=None, model=None):
        self.name = name
        self.advancement = advancement
        self.priority = priority
        self.type = type
        self.code = code
        self.index = index
        self.location = None
        self.object = object
        self.model = model
        self.price = None


    def copy(self):
        return Item(self.name, self.advancement, self.priority, self.type, self.code, self.index)


    @property
    def key(self):
        return self.type == 'SmallKey' or self.type == 'BossKey'


    @property
    def smallkey(self):
        return self.type == 'SmallKey'


    @property
    def bosskey(self):
        return self.type == 'BossKey'


    @property
    def crystal(self):
        return self.type == 'Crystal'


    @property
    def map(self):
        return self.type == 'Map'


    @property
    def compass(self):
        return self.type == 'Compass'


    @property
    def dungeonitem(self):
        return self.type == 'SmallKey' or self.type == 'BossKey' or self.type == 'Map' or self.type == 'Compass'


    @property
    def majoritem(self):
        if self.type == 'Token' or self.type == 'Event' or self.type == 'Shop' or not self.advancement:
            return False

        if self.name.startswith('Bombchus') and not self.world.bombchus_in_logic:
            return False

        if self.map or self.compass:
            return False
        if self.smallkey and self.world.shuffle_smallkeys == 'dungeon':
            return False
        if self.bosskey and self.world.shuffle_bosskeys == 'dungeon':
            return False

        return True


    def __str__(self):
        return str(self.__unicode__())


    def __unicode__(self):
        return '%s' % self.name


def ItemFactory(items, world=None):
    ret = []
    singleton = False
    if isinstance(items, str):
        items = [items]
        singleton = True
    for item in items:
        if item in item_table:
            advancement, priority, type, code, index, object, model = item_table[item]
            new_item = Item(item, advancement, priority, type, code, index, object, model)
            if world:
                new_item.world = world
            ret.append(new_item)
        else:
            raise KeyError('Unknown Item: %s', item)

    if singleton:
        return ret[0]
    return ret
