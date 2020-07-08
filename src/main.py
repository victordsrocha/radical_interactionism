from src.agent import Agent
from src.environment import Environment

agent = Agent()
env = Environment()


def step():
    intended_interaction = agent.get_intended_interaction()
    enacted_interaction = enact(intended_interaction)
