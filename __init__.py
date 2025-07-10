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

    for run_id in range(0, 50): # the number of repetitions

        score_mult_mafias = score_mult_winner = \
        score_devil_mafias = score_devil_winner = \
        score_single_mafias = score_single_winner = 0

        for game_data in data[:]: # Sequentially read the game log for each game

            game_log = '\n'.join(game_data["log"])


            """STATEMENT
            Call agent_1 and agent_2 to make the initial statement"""
            print("#", end='')
            agent_1_statement = get_agents("agent_1_statement")[0]
            agent_2_statement = get_agents("agent_2_statement")[0]

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


            """Store the initial statement made by agent_1
            
            Since the initial statement is identical across the three modes
            — multy_agents, multy_agents_devil —
            it is recorded three times into separate sections.
            
            Note: The single_agent case will be evaluated.
            """
            save_result_json(
                run_id,
                "multy_agents",
                "log",
                {"speaker": agent_1_statement.name, "message": opinion_agent_1_statement},
                game_id=game_data["id"])

            save_result_json(
                run_id,
                "multy_agents_devil",
                "log",
                {"speaker": agent_1_statement.name, "message": opinion_agent_1_statement},
                game_id=game_data["id"])


            """Store the initial statement made by agent_2

            The initial statement is identical across the two modes
            — multy_agents, multy_agents_devil —
            it is recorded two times into separate sections.

            Note: The single_agent case has already been evaluated.
            """
            save_result_json(
                run_id,
                "multy_agents",
                "log",
                {"speaker": agent_2_statement.name, "message": opinion_agent_2_statement},
                game_id=game_data["id"])

            save_result_json(
                run_id,
                "multy_agents_devil",
                "log",
                {"speaker": agent_2_statement.name, "message": opinion_agent_2_statement},
                game_id=game_data["id"])


            """DISCUSSION 
            Call agent_1, agent_2, and agent_3 to make the discussion
            This includes two different sets related to Agent_3:
            one concerning critical thinking, and the other related to devil (or devil’s advocate)
            """
            print("#", end='')
            agents_discussion = get_agents(["agent_1_discussion", "agent_2_discussion", "agent_3_discussion"])
            agents_devil_discussion = get_agents(["agent_1_discussion", "agent_2_discussion", "agent_3_devil_discussion"])

            for i in range(num_rounds):

                for agent in agents_discussion:

                    opinion_agents_discussion = agent.update(
                        run_id,
                        game_data["id"],
                        "multy_agents",
                        agent.name,
                        game_log)

                    save_result_json(
                        run_id,
                        "multy_agents",
                        "log",
                        {"speaker": agent.name, "message": opinion_agents_discussion},
                        game_id=game_data["id"])

                for agent in agents_devil_discussion:

                    opinion_agents_discussion = agent.update(
                        run_id,
                        game_data["id"],
                        "multy_agents_devil",
                        agent.name,
                        game_log)

                    save_result_json(
                        run_id,
                        "multy_agents_devil",
                        "log",
                        {"speaker": agent.name, "message": opinion_agents_discussion},
                        game_id=game_data["id"])


            """VOTING
            
            """
            print("#", end='')
            agent_1_vote = get_agents("agent_1_vote")[0]
            agent_2_vote = get_agents("agent_2_vote")[0]
            agent_3_vote = get_agents("agent_3_vote")[0]
            agent_3_devil_vote = get_agents("agent_3_devil_vote")[0]


            """MULTY VOTING PART"""
            opinion_agent_1_vote = agent_1_vote.update(
                run_id,
                game_data["id"],
                "multy_agents",
                agent_1_vote.name,
                game_log)

            opinion_agent_2_vote = agent_2_vote.update(
                run_id,
                game_data["id"],
                "multy_agents",
                agent_2_vote.name,
                game_log)

            opinion_agent_3_vote = agent_3_vote.update(
                run_id,
                game_data["id"],
                "multy_agents",
                agent_3_vote.name,
                game_log)

            """DEVIL VOTING PART"""
            opinion_agent_1_devil_vote = agent_1_vote.update(
                run_id,
                game_data["id"],
                "multy_agents_devil",
                agent_1_vote.name,
                game_log)

            opinion_agent_2_devil_vote = agent_2_vote.update(
                run_id,
                game_data["id"],
                "multy_agents_devil",
                agent_2_vote.name,
                game_log)

            opinion_agent_3_devil_vote = agent_3_devil_vote.update(
                run_id,
                game_data["id"],
                "multy_agents_devil",
                agent_3_devil_vote.name,
                game_log)

            """RECORD MULTY VOTING PART"""
            print("#", end='')
            save_result_json(
                run_id,
                "multy_agents",
                "vote",
                {
                    "speaker": agent_1_vote.name,
                    "mafias": extract_mafia_vote(opinion_agent_1_vote),
                    "winner": extract_outcome_vote(opinion_agent_1_vote),
                    "reason": opinion_agent_1_vote,
                },
                game_id=game_data["id"])

            save_result_json(
                run_id,
                "multy_agents",
                "vote",
                {
                    "speaker": agent_2_vote.name,
                    "mafias": extract_mafia_vote(opinion_agent_2_vote),
                    "winner": extract_outcome_vote(opinion_agent_2_vote),
                    "reason": opinion_agent_2_vote,
                },
                game_id=game_data["id"])

            save_result_json(
                run_id,
                "multy_agents",
                "vote",
                {
                    "speaker": agent_3_vote.name,
                    "mafias": extract_mafia_vote(opinion_agent_3_vote),
                    "winner": extract_outcome_vote(opinion_agent_3_vote),
                    "reason": opinion_agent_3_vote,
                },
                game_id=game_data["id"])

            """RECORD DEVIL VOTING PART"""
            save_result_json(
                run_id,
                "multy_agents_devil",
                "vote",
                {
                    "speaker": agent_1_vote.name,
                    "mafias": extract_mafia_vote(opinion_agent_1_devil_vote),
                    "winner": extract_outcome_vote(opinion_agent_1_devil_vote),
                    "reason": opinion_agent_1_devil_vote,
                },
                game_id=game_data["id"])

            save_result_json(
                run_id,
                "multy_agents_devil",
                "vote",
                {
                    "speaker": agent_2_vote.name,
                    "mafias": extract_mafia_vote(opinion_agent_2_devil_vote),
                    "winner": extract_outcome_vote(opinion_agent_2_devil_vote),
                    "reason": opinion_agent_2_devil_vote,
                },
                game_id=game_data["id"])

            save_result_json(
                run_id,
                "multy_agents_devil",
                "vote",
                {
                    "speaker": agent_3_devil_vote.name,
                    "mafias": extract_mafia_vote(opinion_agent_3_devil_vote),
                    "winner": extract_outcome_vote(opinion_agent_3_devil_vote),
                    "reason": opinion_agent_3_devil_vote,
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
                "multy_agents_devil",
                "pred",
                {
                    "mafias": majority_mafia_vote(run_id, game_data["id"], "multy_agents_devil"),
                    "winner": majority_winner_vote(run_id, game_data["id"], "multy_agents_devil")
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
                "multy_agents_devil",
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

            score_devil_mafias += score_mafias(run_id, game_data["id"], "multy_agents_devil")
            score_devil_winner += score_winner(run_id, game_data["id"], "multy_agents_devil")

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

            # multy_agents_devil
            save_result_json(
                run_id,
                "multy_agents_devil",
                "score_mafias",
                score_devil_mafias,
                game_id=game_data["id"]
            )

            save_result_json(
                run_id,
                "multy_agents_devil",
                "score_winner",
                score_devil_winner,
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
            print(f"  multy_agents_devil - mafias: {score_devil_mafias}, winner: {score_devil_winner}")
            print(f"  single_agent       - mafias: {score_single_mafias}, winner: {score_single_winner}")

            check_prediction_discrepancy(run_id, game_data["id"])





