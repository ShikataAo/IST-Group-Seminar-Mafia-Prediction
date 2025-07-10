Evaluating Collective Intelligence in Multi-Agent LLM Systems via Mafia Game Analysis

This directory contains the implementation files for the report titled
“Evaluating Collective Intelligence in Multi-Agent LLM Systems via Mafia Game Analysis.”
It includes modules for standard experiments, agent configuration, data processing, and statistical analysis.

File descriptions:

__init__.py
Implements the standard multi-agent experiment.

agent_config.py
Used for configuring parameters for agents.

agent_schema.py
Specifies the output format expected from each agent.

agent.py
Module containing the implementation of the Agent class.

data/
Directory containing prompt keywords and the original Mafia game logs.

mafia.json
Structured data extracted from the raw Mafia game logs.

t_test.py
Performs pairwise t-tests for statistical comparison of agent group performance.

utils.py
Provides preprocessing and postprocessing tools to support more effective interaction with large language models (LLMs).

vote_only_test.py
Temporary script implementing the Direct Voting Experiment, in which six agents vote individually without discussion.

Note: All experiments were conducted using the Qwen2.5-72B model.