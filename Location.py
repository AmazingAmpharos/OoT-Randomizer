class Location(object):

    def __init__(self, name='', address=None, address2=None, default=None, type='Chest', scene=None, hint='Termina', parent=None):
        self.name = name
        self.parent_region = parent
        self.item = None
        self.address = address
        self.address2 = address2
        self.default = default
        self.type = type
        self.scene = scene
        self.hint = hint
        self.spot_type = 'Location'
        self.recursion_count = 0
        self.staleness_count = 0
        self.always_allow = lambda item, state: False
        self.access_rule = lambda state: True
        self.item_rule = lambda item: True
        self.locked = False
        self.price = None
        self.minor_only = False


    def can_fill(self, state, item, check_access=True):
        if self.minor_only and item.majoritem:
            return False
        return self.parent_region.can_fill(item) and (self.always_allow(item, state) or (self.item_rule(item) and (not check_access or state.can_reach(self))))


    def can_fill_fast(self, item):
        return self.item_rule(item)


    def can_reach(self, state):
        if self.access_rule(state) and state.can_reach(self.parent_region):
            return True
        return False


    def __str__(self):
        return str(self.__unicode__())


    def __unicode__(self):
        return '%s' % self.name

