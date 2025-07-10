"""Used to specify the output format of agents"""

from pydantic import BaseModel
import typing


"""
3 kinds of classes:
AgentConclude: Perform initial analysis and summary based on the game dialogue log.
AgentDiscussion: Discuss based on the game log and the first round of reasoning.
AgentVote: Decide which group won, identify the mafias, and provide reasoning.
"""
class AgentConclude(BaseModel):
    mafias: list[str]
    game_outcome: typing.Literal['mafia', 'bystander']
    reason: str

class AgentDiscussion(BaseModel):
    Discussion: list[str]

class AgentVote(BaseModel):
    mafias: list[str]
    game_outcome: typing.Literal['mafia', 'bystander']
    reason: str