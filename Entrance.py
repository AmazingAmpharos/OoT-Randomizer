class Entrance(object):

    def __init__(self, name='', parent=None):
        self.name = name
        self.parent_region = parent
        self.connected_region = None
        self.addresses = None
        self.spot_type = 'Entrance'
        self.recursion_count = { 'child': 0, 'adult': 0 }
        self.replaces = self
        self.access_rule = lambda state: True
        self.world = None
        self.type = None
        self.shuffled = False


    def copy(self, new_region):
        new_entrance = Entrance(self.name, new_region)
        new_entrance.world = new_region.world

        new_entrance.connected_region = self.connected_region.name
        new_entrance.addresses = self.addresses
        new_entrance.spot_type = self.spot_type
        new_entrance.replaces = self.replaces
        new_entrance.access_rule = self.access_rule
        new_entrance.type = self.type
        new_entrance.shuffled = self.shuffled

        return new_entrance


    def can_reach(self, state):
        return state.with_spot(self.access_rule, spot=self) and state.can_reach(self.parent_region)


    def connect(self, region, replaces=None):
        self.connected_region = region
        if replaces:
            self.replaces = replaces
        region.entrances.append(self)


    def disconnect(self):
        self.connected_region.entrances = list(filter(lambda entrance: self != entrance, self.connected_region.entrances))
        previously_connected = self.connected_region
        self.connected_region = None
        return previously_connected


    def swap_connections(self, other_entrance):
        self_connected_region = self.disconnect()
        other_connected_region = other_entrance.disconnect()
        old_other_entrance_replaces = other_entrance.replaces
        other_entrance.connect(self_connected_region, replaces=self.replaces)
        self.connect(other_connected_region, replaces=old_other_entrance_replaces)


    def __str__(self):
        return str(self.__unicode__())


    def __unicode__(self):
        return '%s' % self.name

