"""
A collection of helper tools for preprocessing inputs and postprocessing outputs
to support more effective interaction with large language models (LLMs).
"""

import ast
import json
import openai
import os
import re
from agent_config import load_prompt, prompt_dir
from collections import Counter



def check_prediction_discrepancy(run_id, game_id):
    """
    Briefly check whether the pred from multy_agents or multy_agents_devil differs from that of single_agent.
    If there is a mismatch, print the game_id and the type of difference.
    """
    filename = os.path.join("results", f"{run_id}_result.json")

    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)

    game_data = data.get(game_id, {})

    pred_single = game_data.get("single_agent", {}).get("pred", {})
    pred_multy = game_data.get("multy_agents", {}).get("pred", {})
    pred_devil = game_data.get("multy_agents_devil", {}).get("pred", {})

    if pred_multy != pred_single:
        print(f"{game_id}: multy_agents differs from single_agent")

    if pred_devil != pred_single:
        print(f"{game_id}: multy_agents_devil differs from single_agent")


def majority_mafia_vote(run_id, game_id, mode="multy_agents"):
    """
    From the 'mafia' field in each vote entry, count and return the two most frequently
    predicted mafia members.

    Returns:
        List[str]: Names of the top 2 mafia suspects.
    """
    with open(f"results/{run_id}_result.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    votes = data.get(game_id, {}).get(mode, {}).get("vote", [])

    mafia_counter = Counter()

    for vote_entry in votes:
        mafia_list = vote_entry.get("mafias", [])

        if not isinstance(mafia_list, list) or len(mafia_list) != 2:
            print(f"[Warning] Skipping malformed mafia field: {mafia_list}")
            continue

        mafia_counter.update(mafia_list)

    top_mafias = [name for name, _ in mafia_counter.most_common(2)]
    return top_mafias


def majority_winner_vote(run_id, game_id, mode="multy_agents"):
    """
    From the 'winner' field in each vote entry, determine the most commonly predicted
    winning group (e.g., 'mafia' or 'bystander').

    Returns:
        List[str]: A single-element list containing the most voted winner.
    """
    with open(f"results/{run_id}_result.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    votes = data.get(game_id, {}).get(mode, {}).get("vote", [])

    winner_counter = Counter()

    for vote_entry in votes:
        winner = vote_entry.get("winner", None)
        if isinstance(winner, str):
            winner_counter[winner.lower()] += 1
        else:
            print(f"[Warning] Skipping invalid winner field: {winner}")

    top_winner = winner_counter.most_common(1)[0][0] if winner_counter else "unknown"

    return top_winner


def extract_mafia_vote(text):
    """
    Extract the list of mafias from the structured text.
    The return value should be a list in the form [mafia1, mafia2, ...], or None if extraction fails.
    """
    try:

        text = text.replace('\n', ' ').replace('\\n', ' ')


        mafias_match = re.search(r"mafias\s*=\s*(\[[^\]]+\])", text)

        if mafias_match:
            mafias_str = mafias_match.group(1)
            mafias = ast.literal_eval(mafias_str)
            if isinstance(mafias, list):

                return [name.strip() for name in mafias]
    except Exception as e:
        print("Fail:", e)

    return None


def extract_outcome_vote(text):
    """
    Extract the game_outcome from the structured text.
    The return value should be a string such as 'mafia' or 'villager', or None if extraction fails.
    """
    try:

        text = text.replace('\n', ' ').replace('\\n', ' ')


        outcome_match = re.search(r"game_outcome\s*=\s*'([^']+)'", text)

        if outcome_match:
            return outcome_match.group(1).strip()
    except Exception as e:
        print("Fail:", e)

    return None



def score_mafias(run_id, game_id, mode="multy_agents"):
    """
    Compares mafia names against the true mafias.
    Each correct match scores 1 point, with a maximum of 2 points.

    Args:
        run_id (int): run_id
        game_id (str): game_id
        mode (str): 'multy_agents' or 'single_agent'

    Returns:
        int: Mafia prediction score (0–2)
    """
    file_path = f"results/{str(run_id)}_result.json"

    if not os.path.exists(file_path):
        print(f"[Error] File not found: {file_path}")
        return 0

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        game_data = data.get(game_id, {})
        pred_mafias = game_data.get(mode, {}).get("pred", {}).get("mafias", [])
        true_mafias = game_data.get(mode, {}).get("true", {}).get("true mafias", [])

        if len(pred_mafias) < 2 or len(true_mafias) < 2:
            print(f"[Warning] Missing mafia prediction or ground truth in {game_id}")
            return 0

        score = len(set(pred_mafias) & set(true_mafias))
        return score

    except Exception as e:
        print(f"[Error] Failed to compute mafia score in {game_id}: {e}")
        return 0


def score_winner(run_id, game_id, mode="multy_agents"):
    """
    Compares won group between prediction and truth.
    Returns 1 point if correct, 0 wrong.

    Args:
        run_id (int): run_id
        game_id (str): game_id
        mode (str): 'multy_agents' or 'single_agent'

    Returns:
        int: Game outcome prediction score (0–1)
    """
    file_path = f"results/{str(run_id)}_result.json"

    if not os.path.exists(file_path):
        print(f"[Error] File not found: {file_path}")
        return 0

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        game_data = data.get(game_id, {})
        pred_winner = game_data.get(mode, {}).get("pred", {}).get("winner", None)
        true_winner = game_data.get(mode, {}).get("true", {}).get("true winner", None)

        if not pred_winner or not true_winner:
            print(f"[Warning] Missing winner prediction or ground truth in {game_id}")
            return 0

        return int(pred_winner.lower() == true_winner.lower())

    except Exception as e:
        print(f"[Error] Failed to compute winner score in {game_id}: {e}")
        return 0


def save_result_json(run_id, mode, field, entry, game_id="unknown_game"):
    """
    Save content to a specific field in a JSON file.

    Args:
        run_id: Identifier used in the filename.
        mode: Either "multy_agents" or "single_agent".
        entry: The data to be saved (type depends on the field).
        field: The field name to save into (e.g., "log", "pred", "true_mafias", "score_now", "result_part", "vote").
        game_id: The current game ID (used as the top-level key in the JSON file).
    """

    os.makedirs("results", exist_ok=True)
    filename = os.path.join("results", f"{run_id}_result.json")

    # Load data
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {}

    # Initialize the structure for this game_id
    if game_id not in data:
        data[game_id] = {
            "multy_agents": {
                "log": [],
                "vote": [],
                "pred": {},
                "true": {},
                "score_mafias": 0,
                "score_winner": 0
            },
            "multy_agents_devil": {
                "log": [],
                "vote": [],
                "pred": {},
                "true": {},
                "score_mafias": 0,
                "score_winner": 0
            },
            "single_agent": {
                "vote": [],
                "pred": {},
                "true": {},
                "score_mafias": 0,
                "score_winner": 0
            }
        }

    # Write data to the specified field
    section = data[game_id][mode]

    if field in ["log", "vote"]:
        if not isinstance(section.get(field), list):
            section[field] = []
        section[field].append(entry)

    elif field in ["pred", "true"]:
        if not isinstance(section.get(field), dict):
            section[field] = {}
        section[field] = entry

    elif field in ["score_mafias", "score_winner"]:
        section[field] = int(entry)

    else:
        raise ValueError(f"Unsupported field: {field}")
    # Save back to file
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


"""
Discarded Functions
"""

def format_opinion(opinion: str) -> str:
    """The beautification pack is in the format of a .txt file **Discarded**"""

    opinion = re.sub(r'([。？?\.])', r'\1\n', opinion)
    opinion = re.sub(r'\n+', '\n', opinion)
    return opinion.strip()


def conclude(opinion: list[str]) ->[str]:
    """Summarizing dialogue results (.txt format) by LLM **Discarded**"""

    llm_client = openai.OpenAI(
        base_url="https://tulip.kuee.kyoto-u.ac.jp/LlamaServer_saffron7/v1",
        api_key="EMPTY"
    )

    completion = llm_client.chat.completions.create(
        model= "Qwen/Qwen2.5-72B-Instruct",
        messages=[
            {"role": "system", "content": [{"type": "text", "text": load_prompt(prompt_dir, "agent_conclude.txt")}]},
            {"role": "user", "content": [{"type": "text", "text": "\n".join(opinion)}]},
        ],
        temperature=0.0,
    )

    conclusion = completion.choices[0].message.content
    return (conclusion)


def conclude_from_log(run_id, game_id, mode = "multy_agents"):
    """Summarizing dialogue results (.json format) by LLM **Discarded**"""

    llm_client = openai.OpenAI(
        base_url="https://tulip.kuee.kyoto-u.ac.jp/LlamaServer_saffron7/v1",
        api_key="EMPTY"
    )

    file_path = f"results/{run_id}_result.json"

    if not os.path.exists(file_path):
        print(f"[Error] File not found: {file_path}")
        return ""

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        game_data = data.get(game_id, {})
        log_entries = game_data.get(mode, {}).get("log", [])

        log_texts = []
        for entry in log_entries:
            if isinstance(entry, dict) and "speaker" in entry and "message" in entry:
                log_texts.append(f"{entry['speaker']}: {entry['message']}")

        full_log = "\n".join(log_texts)

        completion = llm_client.chat.completions.create(
            model="Qwen/Qwen2.5-72B-Instruct",
            messages=[
                {
                    "role": "system",
                    "content": [{"type": "text", "text": load_prompt(prompt_dir, "agent_conclude.txt")}],
                },
                {
                    "role": "user",
                    "content": [{"type": "text", "text": full_log}],
                },
            ],
            temperature=0.0,
        )

        return completion.choices[0].message.content.strip()

    except Exception as e:
        print(f"[Error] Failed to generate conclusion: {e}")
        return ""

