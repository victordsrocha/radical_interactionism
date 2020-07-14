from src.memory import Memory
from src.anticipation import Anticipation
import random


class Decider:

    def __init__(self, memory):

        self.memory = memory

        self.enacted_interaction = None
        self.super_interaction = None
        # self.last_super_interaction = None

    def anticipate(self):
        # TODO criar docstring

        def get_activated_interactions():
            """
            Uma interação é dita ativada quando sua pré-interação é uma interação em contexto.
            Uma interação é dita em contexto quando ela é a interação realizada (enacted) no 
            último passo, incluindo a super-interação criada com base nesta.

            Returns:
                retorna lista de interações ativadas
            """
            context_interactions = []
            if self.enacted_interaction is not None:
                context_interactions.append(self.enacted_interaction)
                if not self.enacted_interaction.is_primitive():
                    context_interactions.append(
                        self.enacted_interaction.post_interaction)
                if self.super_interaction is not None:
                    context_interactions.append(self.super_interaction)

            activated_interactions_ = []
            for know_interaction in self.memory.known_interactions.values():
                if not know_interaction.is_primitive():
                    # Talvez nao seja possivel usar somente a busca por objeto aqui
                    # talvez seja necessario usar a label
                    if know_interaction.pre_interaction in context_interactions:
                        activated_interactions_.append(know_interaction)
                        # print(f'activated {know_interaction}')
            return activated_interactions_

        anticipations = []
        activated_interactions = get_activated_interactions()

        # este bloco cria uma lista de anticipations a partir da lista de interações ativadas
        if self.enacted_interaction is not None:
            for activatedInteraction in activated_interactions:
                if activatedInteraction.post_interaction.experiment is not None:
                    new_antip = Anticipation()  # new anticipation
                    new_antip.experiment = activatedInteraction.post_interaction.experiment
                    new_antip.proclivity = activatedInteraction.weight * activatedInteraction.post_interaction.valence
                    for anticipation in anticipations:
                        if new_antip.experiment == anticipation.experiment:
                            anticipation.proclivity += new_antip.proclivity
                            break
                    # TODO não testado
                    else:
                        anticipations.append(new_antip)

        # este bloco faz uso da lista de enacted interactions armazenadas em experiments
        # se uma dessas interactions é o postInteraction de uma interação ativada:
        # então podemos aumentar a tendência (proclivity) da anticipation de origem
        for anticipation in anticipations:
            for exp_enacted_interaction in anticipation.experiment.enacted_interactions:
                for activatedInteraction in activated_interactions:
                    if exp_enacted_interaction == activatedInteraction.post_interaction:
                        proclivity = activatedInteraction.weight * exp_enacted_interaction.valence
                        anticipation.proclivity += proclivity

        return anticipations

    def select_experiment(self, anticipations):
        """
        The selectExperiment( ) function sorts the list of anticipations by decreasing proclivity of
        their proposed interaction. Then, it takes the fist anticipation (index [0]), which has
        the highest proclivity in the list. If this proclivity is positive, then the agent wants to
        re-enact this proposed interaction, leading to the agent choosing this proposed
        interaction's experiment.

        Por enquanto: se houver alguma anticipation com proclivity >= 0 então a anticipation de
        maior proclivity sempre será escolhida, caso contrário sorteia um experimento conhecido
        qualquer para retornar.

        Args:
            Anticipation list -> Lista de antecipações criadas por Anticipate( )

        Returns:
            Experiment -> experimento selecionado
        """

        def get_other_experiment(experiment):
            """
            Acessa memória de experimentos conhecidos e retorna um experimento diferente do
            recebido como argumento.

            Por enquanto está sendo feito de forma aleatória.
            """
            experiments_set = set(
                self.memory.known_experiments.values()) - {experiment}
            return random.choice(list(experiments_set))

        if len(anticipations) > 0:
            anticipations.sort(key=lambda x: x.proclivity, reverse=True)
            '''
            for e in anticipations:
                print(f'propose {e}')
            '''

            selected_anticipation = anticipations[0]
            if selected_anticipation.proclivity >= 0:
                selected_experiment = selected_anticipation.experiment
            else:
                selected_experiment = get_other_experiment(selected_anticipation.experiment)
        else:
            selected_experiment = get_other_experiment(None)
        return selected_experiment

    def learn_composite_interaction(self, enacted_interaction):
        previous_interaction = self.enacted_interaction
        last_interaction = enacted_interaction
        previous_super_interaction = self.super_interaction
        last_super_interaction = None

        # learn [previous current] called the super interaction
        if previous_interaction is not None:
            last_super_interaction = self.memory.add_or_get_and_reinforce_composite_interaction(previous_interaction,
                                                                                                last_interaction)

        # Learn higher-level interactions
        if previous_super_interaction is not None:
            # learn [penultimate [previous current]]
            self.memory.add_or_get_and_reinforce_composite_interaction(previous_super_interaction.pre_interaction,
                                                                       last_super_interaction)

            # learn [[penultimate previous] current]
            self.memory.add_or_get_and_reinforce_composite_interaction(previous_super_interaction, last_interaction)

        self.super_interaction = last_super_interaction
