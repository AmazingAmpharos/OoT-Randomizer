from enum import Enum, unique


class Region(object):

    def __init__(self, name, type):
        self.name = name
        self.type = type
        self.entrances = []
        self.exits = []
        self.locations = []
        self.dungeon = None
        self.world = None
        self.spot_type = 'Region'
        self.recursion_count = 0
        self.price = None


    def can_reach(self, state):
        for entrance in self.entrances:
            if state.can_reach(entrance):
                return True
        return False


    def can_fill(self, item):
        is_dungeon_restricted = False
        if item.map or item.compass:
            is_dungeon_restricted = self.world.shuffle_mapcompass == 'dungeon'
        elif item.smallkey:
            is_dungeon_restricted = self.world.shuffle_smallkeys == 'dungeon'
        elif item.bosskey:
            is_dungeon_restricted = self.world.shuffle_bosskeys == 'dungeon'

        if is_dungeon_restricted:
            return self.dungeon and self.dungeon.is_dungeon_item(item) and item.world.id == self.world.id
        return True


    def __str__(self):
        return str(self.__unicode__())


    def __unicode__(self):
        return '%s' % self.name


@unique
class RegionType(Enum):

    Overworld = 1
    Interior = 2
    Dungeon = 3
    Grotto = 4


    @property
    def is_indoors(self):
        """Shorthand for checking if Interior or Dungeon"""
        return self in (RegionType.Interior, RegionType.Dungeon, RegionType.Grotto)

