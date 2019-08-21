from Region import TimeOfDay


class Entrance(object):

    def __init__(self, name='', parent=None):
        self.name = name
        self.parent_region = parent
        self.world = parent.world
        self.connected_region = None
        self.access_rule = lambda state, **kwargs: True
        self.access_rules = []
        self.reverse = None
        self.replaces = None
        self.assumed = None
        self.type = None
        self.shuffled = False
        self.data = None
        self.primary = False


    def copy(self, new_region):
        new_entrance = Entrance(self.name, new_region)
        new_entrance.connected_region = self.connected_region.name
        new_entrance.access_rule = self.access_rule
        new_entrance.access_rules = list(self.access_rules)
        new_entrance.reverse = self.reverse
        new_entrance.replaces = self.replaces
        new_entrance.assumed = self.assumed
        new_entrance.type = self.type
        new_entrance.shuffled = self.shuffled
        new_entrance.data = self.data
        new_entrance.primary = self.primary

        return new_entrance


    def add_rule(self, lambda_rule):
        self.access_rules.append(lambda_rule)
        self.access_rule = lambda state, **kwargs: all(rule(state, **kwargs) for rule in self.access_rules)


    def set_rule(self, lambda_rule):
        self.access_rule = lambda_rule
        self.access_rules = [lambda_rule]


    def connect(self, region):
        self.connected_region = region
        region.entrances.append(self)


    def disconnect(self):
        self.connected_region.entrances.remove(self)
        previously_connected = self.connected_region
        self.connected_region = None
        return previously_connected


    def assume_reachable(self):
        if self.assumed == None:
            target_region = self.disconnect()
            root = self.world.get_region('Root Exits')
            assumed_entrance = Entrance('Root -> ' + target_region.name, root)
            assumed_entrance.connect(target_region)
            assumed_entrance.replaces = self
            root.exits.append(assumed_entrance)
            self.assumed = assumed_entrance
        return self.assumed


    def bind_two_way(self, other_entrance):
        self.reverse = other_entrance
        other_entrance.reverse = self


    def __str__(self):
        return str(self.__unicode__())


    def __unicode__(self):
        return '%s' % self.name

