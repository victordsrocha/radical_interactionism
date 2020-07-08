from src.interface import Interface


class Enacter(object):

    def __init__(self, memory):
        self.memory = memory
        self.interface = Interface(self.memory)

    def enact(self, intended_interaction):
        if intended_interaction.is_primitive():
            return self.interface.enact(intended_interaction)
        else:
            # Enact the pre-interaction
            enacted_pre_interaction = self.enact(
                intended_interaction.pre_interaction)
            if enacted_pre_interaction != intended_interaction.pre_interaction:
                # if the preInteraction failed then the enaction of the intendedInteraction
                # is interrupted here
                return enacted_pre_interaction
            else:
                # Enact the post-interaction
                enacted_post_interaction = self.enact(
                    intended_interaction.post_interaction)
                return self.memory.add_or_get_composite_interaction(enacted_pre_interaction, enacted_post_interaction)
