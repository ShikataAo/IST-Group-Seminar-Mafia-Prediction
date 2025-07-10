"""
A temporary experimental addition for creating the six-agent individual voting experiment
"""

import json
import openai
from utils import save_result_json, extract_mafia_vote, extract_outcome_vote, majority_mafia_vote, majority_winner_vote, score_mafias, score_winner, check_prediction_discrepancy

from agent import get_agents


"""Initialization of model count and related parameters"""
num_agents = 3
num_rounds = 5
run_id = 0


"""Invoke the model"""
llm_client = openai.OpenAI(
    base_url="https://tulip.kuee.kyoto-u.ac.jp/LlamaServer_saffron7/v1",
    api_key="EMPTY"
)


if __name__ == '__main__':


    with open('./mafia.json', "r") as f: # Read the game log file
        data = json.load(f)

    for run_id in range(100, 130): # the number of repetitions

        score_mult_mafias = score_mult_winner = \
        score_single_mafias = score_single_winner = 0

        for game_data in data[:]: # Sequentially read the game log for each game

            game_log = '\n'.join(game_data["log"])


            """STATEMENT
            Call agent_1 ~ agent_6 to make the initial statement"""
            print("#", end='')
            agent_1_statement = get_agents("agent_1_statement")[0]
            agent_2_statement = get_agents("agent_2_statement")[0]
            agent_3_statement = get_agents("agent_3_statement")[0]
            agent_4_statement = get_agents("agent_4_statement")[0]
            agent_5_statement = get_agents("agent_5_statement")[0]
            agent_6_statement = get_agents("agent_6_statement")[0]


            opinion_agent_1_statement = agent_1_statement.update(
                run_id,
                game_data["id"],
                "multy_agents",
                agent_1_statement.name,
                game_log)

            opinion_agent_2_statement = agent_2_statement.update(
                run_id,
                game_data["id"],
                "multy_agents",
                agent_2_statement.name,
                game_log)

            opinion_agent_3_statement = agent_3_statement.update(
                run_id,
                game_data["id"],
                "multy_agents",
                agent_2_statement.name,
                game_log)

            opinion_agent_4_statement = agent_4_statement.update(
                run_id,
                game_data["id"],
                "multy_agents",
                agent_1_statement.name,
                game_log)

            opinion_agent_5_statement = agent_5_statement.update(
                run_id,
                game_data["id"],
                "multy_agents",
                agent_2_statement.name,
                game_log)

            opinion_agent_6_statement = agent_6_statement.update(
                run_id,
                game_data["id"],
                "multy_agents",
                agent_2_statement.name,
                game_log)

            """Store the initial statement made by agent_1~6

            """

            save_result_json(
                run_id,
                "multy_agents",
                "vote",
                {
                    "speaker": agent_1_statement.name,
                    "mafias": extract_mafia_vote(opinion_agent_1_statement),
                    "winner": extract_outcome_vote(opinion_agent_1_statement),
                    "reason": opinion_agent_1_statement,
                },
                game_id=game_data["id"])

            save_result_json(
                run_id,
                "multy_agents",
                "vote",
                {
                    "speaker": agent_2_statement.name,
                    "mafias": extract_mafia_vote(opinion_agent_2_statement),
                    "winner": extract_outcome_vote(opinion_agent_2_statement),
                    "reason": opinion_agent_2_statement,
                },
                game_id=game_data["id"])


            save_result_json(
                run_id,
                "multy_agents",
                "vote",
                {
                    "speaker": agent_3_statement.name,
                    "mafias": extract_mafia_vote(opinion_agent_3_statement),
                    "winner": extract_outcome_vote(opinion_agent_3_statement),
                    "reason": opinion_agent_3_statement,
                },
                game_id=game_data["id"])


            save_result_json(
                run_id,
                "multy_agents",
                "vote",
                {
                    "speaker": agent_4_statement.name,
                    "mafias": extract_mafia_vote(opinion_agent_4_statement),
                    "winner": extract_outcome_vote(opinion_agent_4_statement),
                    "reason": opinion_agent_4_statement,
                },
                game_id=game_data["id"])

            save_result_json(
                run_id,
                "multy_agents",
                "vote",
                {
                    "speaker": agent_5_statement.name,
                    "mafias": extract_mafia_vote(opinion_agent_5_statement),
                    "winner": extract_outcome_vote(opinion_agent_5_statement),
                    "reason": opinion_agent_5_statement,
                },
                game_id=game_data["id"])

            save_result_json(
                run_id,
                "multy_agents",
                "vote",
                {
                    "speaker": agent_6_statement.name,
                    "mafias": extract_mafia_vote(opinion_agent_6_statement),
                    "winner": extract_outcome_vote(opinion_agent_6_statement),
                    "reason": opinion_agent_6_statement,
                },
                game_id=game_data["id"])




            """RECORD SINGLE VOTING PART"""
            save_result_json(
                run_id,
                "single_agent",
                "vote",
                {
                    "speaker": agent_1_statement.name,
                    "mafias": extract_mafia_vote(opinion_agent_1_statement),
                    "winner": extract_outcome_vote(opinion_agent_1_statement),
                    "reason": opinion_agent_1_statement,
                },
                game_id=game_data["id"])


            """MAJORITY VOTE

            """
            print("#", end='')
            save_result_json(
                run_id,
                "multy_agents",
                "pred",
                {
                    "mafias": majority_mafia_vote(run_id, game_data["id"], "multy_agents"),
                    "winner": majority_winner_vote(run_id, game_data["id"], "multy_agents")
                },
                game_id=game_data["id"])

            save_result_json(
                run_id,
                "single_agent",
                "pred",
                {
                    "mafias": majority_mafia_vote(run_id, game_data["id"], "single_agent"),
                    "winner": majority_winner_vote(run_id, game_data["id"], "single_agent")
                },
                game_id=game_data["id"])


            """SCORING

            """
            print("#", end='')
            """True result saving"""
            true_mafias = [agent["name"] for agent in game_data["agents"] if agent["role"] == "mafioso"]
            true_winner = ("mafia") if game_data["win"] == "mafioso" else "bystander"

            save_result_json(
                run_id,
                "multy_agents",
                "true",
                {
                    "true mafias": true_mafias,
                    "true winner": true_winner
                },
                game_id=game_data["id"])

            save_result_json(
                run_id,
                "single_agent",
                "true",
                {
                    "true mafias": true_mafias,
                    "true winner": true_winner
                },
                game_id=game_data["id"])

            """Scoring"""
            score_mult_mafias += score_mafias(run_id, game_data["id"], "multy_agents")
            score_mult_winner += score_winner(run_id, game_data["id"], "multy_agents")

            score_single_mafias += score_mafias(run_id, game_data["id"], "single_agent")
            score_single_winner += score_winner(run_id, game_data["id"], "single_agent")

            # multy_agents
            save_result_json(
                run_id,
                "multy_agents",
                "score_mafias",
                score_mult_mafias,
                game_id=game_data["id"]
            )

            save_result_json(
                run_id,
                "multy_agents",
                "score_winner",
                score_mult_winner,
                game_id=game_data["id"]
            )

            # single_agent
            save_result_json(
                run_id,
                "single_agent",
                "score_mafias",
                score_single_mafias,
                game_id=game_data["id"]
            )

            save_result_json(
                run_id,
                "single_agent",
                "score_winner",
                score_single_winner,
                game_id=game_data["id"]
            )



            print("Scores:")
            print(f"  multy_agents      - mafias: {score_mult_mafias}, winner: {score_mult_winner}")
            print(f"  single_agent       - mafias: {score_single_mafias}, winner: {score_single_winner}")

            check_prediction_discrepancy(run_id, game_data["id"])





