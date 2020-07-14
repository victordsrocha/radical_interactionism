from src.experiment import Experiment
from src.interaction import Interaction


class Memory:

    def __init__(self):
        self.known_interactions = {}
        self.known_experiments = {}
        self.init_small_loop()

    def add_or_get_composite_interaction(self, pre_interaction, post_interaction):
        label = '<' + pre_interaction.label + post_interaction.label + '>'

        if label not in self.known_interactions.keys():
            interaction = self.add_or_get_interaction(label)
            interaction.pre_interaction = pre_interaction
            interaction.post_interaction = post_interaction
            interaction.valence = pre_interaction.valence + post_interaction.valence
            self.add_or_get_abstract_experiment(interaction)
        else:
            interaction = self.known_interactions[label]

        return interaction

    def add_or_get_and_reinforce_composite_interaction(self, pre_interaction, post_interaction):
        composite_interaction = self.add_or_get_composite_interaction(pre_interaction, post_interaction)
        composite_interaction.weight += 1
        '''
        if composite_interaction.weight == 1:
            print(f'learn {composite_interaction}')
        else:
            print(f'reinforce {composite_interaction}')
        '''
        return composite_interaction

    # somente por questão de controle todas as criações de novas interações passam por aqui
    def add_or_get_interaction(self, label):
        if label not in self.known_interactions.keys():
            self.known_interactions[label] = Interaction(label)
        return self.known_interactions[label]

    def add_or_get_abstract_experiment(self, interaction):
        label = interaction.label.replace('e', 'E').replace('r', 'R').replace('>', '|')
        if label not in self.known_experiments:
            abstract_experiment = Experiment(label)
            abstract_experiment.intended_interaction = interaction
            interaction.experiment = abstract_experiment
            self.known_experiments[label] = abstract_experiment
        return self.known_experiments[label]

    def add_or_get_primitive_interaction(self, label, valence):
        if label not in self.known_interactions.keys():
            interaction = self.add_or_get_interaction(label)
            interaction.valence = valence
        interaction = self.known_interactions[label]
        return interaction

    def init_small_loop(self):

        turn_left = self.add_or_get_primitive_interaction('^t', -3)  # Left toward empty
        turn_right = self.add_or_get_primitive_interaction('vt', -3)  # Right toward empty

        touch_right = self.add_or_get_primitive_interaction('\\t', -1)  # Touch right wall
        touch_left = self.add_or_get_primitive_interaction('/t', -1)  # Touch left wall
        touch_forward = self.add_or_get_primitive_interaction('-t', -1)  # touch wall

        self.add_or_get_primitive_interaction('\\f', -1)  # Touch right empty
        self.add_or_get_primitive_interaction('/f', -1)  # Touch left empty
        self.add_or_get_primitive_interaction('-f', -1)  # Touch empty

        forward = self.add_or_get_primitive_interaction('>t', 5)  # Move

        self.add_or_get_primitive_interaction('>f', -10)  # Bump

        self.add_or_get_abstract_experiment(turn_left)
        self.add_or_get_abstract_experiment(turn_right)
        self.add_or_get_abstract_experiment(touch_right)
        self.add_or_get_abstract_experiment(touch_left)
        self.add_or_get_abstract_experiment(forward)
        self.add_or_get_abstract_experiment(touch_forward)
