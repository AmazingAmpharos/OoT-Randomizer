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
        self.always = False
        self.never = False


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
        new_entrance.always = self.always
        new_entrance.never = self.never

        return new_entrance


    def add_rule(self, lambda_rule):
        if self.always:
            self.set_rule(lambda_rule)
            self.always = False
            return
        if self.never:
            return
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


    def bind_two_way(self, other_entrance):
        self.reverse = other_entrance
        other_entrance.reverse = self


    def get_new_target(self):
        root = self.world.get_region('Root Exits')
        target_entrance = Entrance('Root -> ' + self.connected_region.name, root)
        target_entrance.connect(self.connected_region)
        target_entrance.replaces = self
        root.exits.append(target_entrance)
        return target_entrance


    def assume_reachable(self):
        if self.assumed == None:
            self.assumed = self.get_new_target()
            self.disconnect()
        return self.assumed


    def __str__(self):
        return str(self.__unicode__())


    def __unicode__(self):
        return '%s' % self.name

