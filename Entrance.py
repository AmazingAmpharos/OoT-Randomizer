class Entrance(object):

    def __init__(self, name='', parent=None):
        self.name = name
        self.parent_region = parent
        self.connected_region = None
        self.target = None
        self.addresses = None
        self.spot_type = 'Entrance'
        self.recursion_count = 0
        self.vanilla = None
        self.access_rule = lambda state: True


    def can_reach(self, state):
        if self.access_rule(state) and state.can_reach(self.parent_region):
            return True

        return False


    def connect(self, region, addresses=None, target=None, vanilla=None):
        self.connected_region = region
        self.target = target
        self.addresses = addresses
        self.vanilla = vanilla
        region.entrances.append(self)


    def __str__(self):
        return str(self.__unicode__())


    def __unicode__(self):
        return '%s' % self.name

