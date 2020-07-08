class Interaction:

    def __init__(self, label):
        self.label = label
        self.experiment = None
        self.valence = None
        self.pre_interaction = None
        self.post_interaction = None
        self.weight = 0

    def __str__(self):
        return self.label + ' valence ' + str(self.valence) + ' weight ' + str(self.weight)

    def is_primitive(self):
        return self.pre_interaction is None
