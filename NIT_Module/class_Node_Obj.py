__author__ = 'Nathaniel'


class FSPair():
    def __init__(self, FSName, FSFunction, IP, MappingNodes):
        self.FSName = FSName
        self.FSFunction = FSFunction
        self.IP = IP
        self.MappingNodes = MappingNodes


class M2M_RuleObj():
    def __init__(self, TopicName, Target, TargetValueOverride):
        self.TopicName = TopicName
        self.Target = Target
        self.TargetValueOverride = TargetValueOverride
