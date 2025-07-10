"""
Used for configuring parameters for agents
"""
from pathlib import Path
import openai
from agent_schema import AgentConclude, AgentDiscussion, AgentVote

model_type = "Qwen/Qwen2.5-72B-Instruct"
base_url = "https://tulip.kuee.kyoto-u.ac.jp/LlamaServer_saffron7/v1"
default_temperature = 2.0
prompt_dir = Path("./data/mafia/prompt_keyword")

llm_client = openai.OpenAI(
    base_url="https://tulip.kuee.kyoto-u.ac.jp/LlamaServer_saffron7/v1",
    api_key="EMPTY"
)


def load_prompt(prompt_dir, file_name: str) -> str:
    with open(prompt_dir / file_name, "r", encoding="utf-8") as file:
        return file.read()


agent_configs = [
    {
        "id": "agent_1_statement",
        "name": "Agent_1",
        "model": model_type,
        "temperature": default_temperature,
        "system_prompt": load_prompt(prompt_dir, "agent_1_statement.txt"),
        "output_schema": AgentConclude
    },
    {
        "id": "agent_2_statement",
        "name": "Agent_2",
        "model": model_type,
        "temperature": default_temperature,
        "system_prompt": load_prompt(prompt_dir, "agent_2_statement.txt"),
        "output_schema": AgentConclude
    },
    {
        "id": "agent_1_discussion",
        "name": "Agent_1",
        "model": model_type,
        "temperature": default_temperature,
        "system_prompt": load_prompt(prompt_dir, "agent_1_discussion.txt"),
        #"output_schema": AgentDiscussion
    },
    {
        "id": "agent_2_discussion",
        "name": "Agent_2",
        "model": model_type,
        "temperature": default_temperature,
        "system_prompt": load_prompt(prompt_dir, "agent_2_discussion.txt"),
        #"output_schema": AgentDiscussion
    },
    {
        "id": "agent_3_discussion",
        "name": "Agent_3",
        "model": model_type,
        "temperature": default_temperature,
        "system_prompt": load_prompt(prompt_dir, "agent_3_discussion.txt"),
        #"output_schema": AgentDiscussion
    },
    {
        "id": "agent_1_vote",
        "name": "Agent_1",
        "model": model_type,
        "temperature": default_temperature,
        "system_prompt": load_prompt(prompt_dir, "agent_1_vote.txt"),
        "output_schema": AgentVote
    },
    {
        "id": "agent_2_vote",
        "name": "Agent_2",
        "model": model_type,
        "temperature": default_temperature,
        "system_prompt": load_prompt(prompt_dir, "agent_2_vote.txt"),
        "output_schema": AgentVote
    },
    {
        "id": "agent_3_vote",
        "name": "Agent_3",
        "model": model_type,
        "temperature": default_temperature,
        "system_prompt": load_prompt(prompt_dir, "agent_3_vote.txt"),
        "output_schema": AgentVote
    },
    {
        "id": "agent_3_devil_discussion",
        "name": "Agent_3",
        "model": model_type,
        "temperature": default_temperature,
        "system_prompt": load_prompt(prompt_dir, "agent_3_devil_discussion.txt"),
        # "output_schema": AgentDiscussion
    },
    {
        "id": "agent_3_devil_vote",
        "name": "Agent_3",
        "model": model_type,
        "temperature": default_temperature,
        "system_prompt": load_prompt(prompt_dir, "agent_3_devil_vote.txt"),
        "output_schema": AgentVote
    },
    {
        "id": "agent_3_statement",
        "name": "Agent_3",
        "model": model_type,
        "temperature": default_temperature,
        "system_prompt": load_prompt(prompt_dir, "agent_3_statement.txt"),
        "output_schema": AgentConclude
    },
    {
        "id": "agent_4_statement",
        "name": "Agent_4",
        "model": model_type,
        "temperature": default_temperature,
        "system_prompt": load_prompt(prompt_dir, "agent_4_statement.txt"),
        "output_schema": AgentConclude
    },
    {
        "id": "agent_5_statement",
        "name": "Agent_5",
        "model": model_type,
        "temperature": default_temperature,
        "system_prompt": load_prompt(prompt_dir, "agent_5_statement.txt"),
        "output_schema": AgentConclude
    },
    {
        "id": "agent_6_statement",
        "name": "Agent_6",
        "model": model_type,
        "temperature": default_temperature,
        "system_prompt": load_prompt(prompt_dir, "agent_6_statement.txt"),
        "output_schema": AgentConclude
    },
]



