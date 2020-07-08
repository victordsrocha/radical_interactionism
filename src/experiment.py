class Experiment(object):

    def __init__(self, label):
        self.label = label
        self.enacted_interactions = set()
        # self.isAbstract = True
        self.intended_interaction = None

    # TODO definir __str__ e funções para lidar com a lista de enactedInt..
