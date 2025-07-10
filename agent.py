"""Module for the Agent class"""

from tenacity import retry, wait_fixed, retry_if_exception_type, stop_never
from dataclasses import dataclass, field
from agent_config import llm_client, agent_configs
from utils import format_opinion
import os
import json
import openai


def get_agents(ids=None):
    """
    Extracts agents from agent_configs based on the specified id(s).

    Args:
        ids (str or list[str] or None):
            - If a string, returns the agent with the matching id.
            - If a list of strings, returns all agents with matching ids.
            - If None, returns all agents.

    Returns:
        List[Agent]: A list of Agent instances matching the given ids.
    """
    if ids is None:
        selected_configs = agent_configs
    elif isinstance(ids, str):
        selected_configs = [config for config in agent_configs if config["id"] == ids]
    else:
        selected_configs = [config for config in agent_configs if config["id"] in ids]

    return [Agent(**config) for config in selected_configs]


@dataclass
class Agent:
    """An agent for OpenAI or Qwen models"""

    id: str
    name: str
    model: str
    temperature: float
    system_prompt: str
    history: list[str] = field(default_factory=list)
    latest_opinion: str = ""
    output_schema: type = None

    """Prevent process termination caused by server unresponsiveness"""
    @retry(
        wait=wait_fixed(120),
        stop=stop_never,
        retry=retry_if_exception_type(openai.InternalServerError)
    )


    def update(self, run_id, game_id, mode, agent_name, game_log) -> str:
        """
        run_id: File name (without extension)
        game_id: Unique ID for the current game
        agent_name: Name of the current agent
        mode: E"multy_agents" or "single_agent"
        game_log: Description string of the game
        """

        # 1. Construct the messages (identity reminder, prompt, and game log)
        messages = [
            {"role": "system", "content": [{"type": "text", "text": f"You are{self.name}"}]},
            {"role": "system", "content": [{"type": "text", "text": self.system_prompt}]},
            {"role": "system", "content": [{"type": "text", "text": game_log}]},
        ]

        # 2. Load the log from the JSON file using game_id and mode as keys
        if os.path.exists(f"results/{run_id}_result.json"):
            with open(f"results/{run_id}_result.json", "r", encoding="utf-8") as f:
                all_data = json.load(f)
                game_data = all_data.get(game_id, {})
                log_entries = game_data.get(mode, {}).get("log", [])
        else:
            log_entries = []

        # 3. Separate the conversation history by role: the agent itself is 'assistant', others are 'user'
        for entry in log_entries:
            speaker = entry.get("speaker", "")
            content = entry.get("message", "")

            if speaker == agent_name:
                role = "assistant"
                messages.append({
                    "role": role,
                    "content": [{"type": "text", "text": content}]
                })
            else:
                role = "user"
                messages.append({
                    "role": role,
                    "content": [{"type": "text", "text": f'{speaker}:{content}'}]
                })

        # 4. Call the LLM and set the output format
        if self.output_schema:
            completion = llm_client.beta.chat.completions.parse(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                response_format=self.output_schema,
            )
            parsed = completion.choices[0].message.parsed
            self.latest_opinion = parsed
            return f"{format_opinion(str(parsed))}"
        else:
            completion = llm_client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
            )
            content = completion.choices[0].message.content.strip()
            self.latest_opinion = content
            return f"{format_opinion(content)}"


