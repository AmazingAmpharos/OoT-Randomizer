from enum import Enum, unique


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


# Pretends to be an enum, but when the values are raw ints, it's much faster
class TimeOfDay(object):
    NONE = 0
    DAY = 1
    DAMPE = 2
    ALL = DAY | DAMPE


class Region(object):

    def __init__(self, name, type=RegionType.Overworld):
        self.name = name
        self.type = type
        self.entrances = []
        self.exits = []
        self.locations = []
        self.dungeon = None
        self.world = None
        self.hint = None
        self.price = None
        self.world = None
        self.time_passes = False
        self.provides_time = TimeOfDay.NONE
        self.scene = None


    def copy(self, new_world):
        new_region = Region(self.name, self.type)
        new_region.world = new_world
        new_region.price = self.price
        new_region.hint = self.hint
        new_region.time_passes = self.time_passes
        new_region.provides_time = self.provides_time
        new_region.scene = self.scene

        if self.dungeon:
            new_region.dungeon = self.dungeon.name
        new_region.locations = [location.copy(new_region) for location in self.locations]
        new_region.exits = [exit.copy(new_region) for exit in self.exits]

        return new_region


    def can_fill(self, item, manual=False):
        is_dungeon_restricted = False
        if item.map or item.compass:
            is_dungeon_restricted = self.world.shuffle_mapcompass in ['dungeon', 'vanilla']
        elif item.smallkey and item.type != 'FortressSmallKey':
            is_dungeon_restricted = self.world.shuffle_smallkeys in ['dungeon', 'vanilla']
        elif item.bosskey and not item.name.endswith('(Ganons Castle)'):
            is_dungeon_restricted = self.world.shuffle_bosskeys in ['dungeon', 'vanilla']
        elif item.bosskey and item.name.endswith('(Ganons Castle)'):
            is_dungeon_restricted = self.world.shuffle_ganon_bosskey in ['dungeon', 'vanilla']

        if is_dungeon_restricted and not manual:
            return self.dungeon and self.dungeon.is_dungeon_item(item) and item.world.id == self.world.id

        if item.name == 'Triforce Piece':
            return item.world.id == self.world.id

        return True


    def __str__(self):
        return str(self.__unicode__())


    def __unicode__(self):
        return '%s' % self.name

