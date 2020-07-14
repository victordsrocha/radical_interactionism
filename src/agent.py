from src.decider import Decider
from src.enacter import Enacter
from src.memory import Memory


class Agent:

    def __init__(self):
        self.step_actions_list = []
        self.memory = Memory()
        self.decider = Decider(self.memory)
        self.enacter = Enacter(self.memory)
        self.mood = None

    def get_intended_interaction(self):
        anticipations = self.decider.anticipate()
        experiment = self.decider.select_experiment(anticipations)
        intended_interaction = experiment.intended_interaction
        return intended_interaction, experiment

    def try_enact_intended_interaction_and_learn(self):
        intended_interaction, experiment = self.get_intended_interaction()

        enacted_interaction = self.enacter.enact(intended_interaction, self.step_actions_list)
        if enacted_interaction != intended_interaction:
            experiment.enacted_interactions.add(enacted_interaction)

        # print(f'Enacted {enacted_interaction}')
        self.decider.learn_composite_interaction(enacted_interaction)
        self.decider.enacted_interaction = enacted_interaction

    def set_mood(self):
        if self.decider.enacted_interaction.valence >= 0:
            self.mood = 'PLEASED'
        else:
            self.mood = 'PAINED'

    def step(self):
        self.step_actions_list = []
        self.get_intended_interaction()
        self.try_enact_intended_interaction_and_learn()
        self.set_mood()


if __name__ == '__main__':
    agent_test = Agent()
    for i in range(1000):
        agent_test.step()
