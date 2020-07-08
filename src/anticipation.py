class Anticipation:

    def __init__(self):
        self.experiment = None
        self.proclivity = None

    def __str__(self):
        return self.experiment.label + ' proclivity ' + str(self.proclivity)
