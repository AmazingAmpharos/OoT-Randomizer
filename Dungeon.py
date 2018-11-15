class Dungeon(object):

    def __init__(self, world, name, regions, boss_key, small_keys, dungeon_items):
        def to_array(obj):
            if obj == None:
                return []
            if isinstance(obj, list):
                return obj
            else:
                return [obj]

        self.world = world
        self.name = name
        self.regions = regions
        self.boss_key = to_array(boss_key)
        self.small_keys = to_array(small_keys)
        self.dungeon_items = to_array(dungeon_items)


    @property
    def keys(self):
        return self.small_keys + self.boss_key


    @property
    def all_items(self):
        return self.dungeon_items + self.keys


    def is_dungeon_item(self, item):
        return item.name in [dungeon_item.name for dungeon_item in self.all_items]


    def __str__(self):
        return str(self.__unicode__())


    def __unicode__(self):
        return '%s' % self.name

