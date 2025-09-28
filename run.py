#############################################################
# Code written by Hojun Choi                                #
# Date: 2024-12-18                                          #
#############################################################

from getpass import getpass
from dotenv import load_dotenv
import importlib
import argparse
import os

# Environment variable setup
def setup_env(required_vars):
    load_dotenv()
    for var in required_vars:
        if not os.environ.get(var):
            os.environ[var] = getpass(f"{var}: ")

def get_env_var(var_name, default=None):
    return os.environ.get(var_name, default)

REQUIRED_ENV_VARS = ["OPENAI_API_KEY"]
setup_env(REQUIRED_ENV_VARS)

OPENAI_API_KEY = get_env_var("OPENAI_API_KEY", "NOT_SET")
DEBUG_MODE = get_env_var("DEBUG_MODE", "False").lower() in ("true", "1", "t")
DEBUG_LIMIT = int(get_env_var("DEBUG_LIMIT", 1))
if DEBUG_MODE:
    print("Debug mode is ON. DEBUG_LIMIT=", DEBUG_LIMIT, "OPENAI_API_KEY=", OPENAI_API_KEY)

AGENTS = [
    "ImageAgent",
    "CaptionAgent",
    "CatAgent",
    "QAAgent",
    "EvaluationAgent",
    "InstructionAgent",
    "CoIAgent",
]

def import_agent(agent_name):
    try:
        module = importlib.import_module(f"agents.{agent_name}")
        return getattr(module, agent_name)
    except (ModuleNotFoundError, AttributeError) as e:
        print(f"Error importing {agent_name}: {e}")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a specific agent with a given category.")
    parser.add_argument("--category", type=str, required=True, help="The category to be processed by the agent.")
    parser.add_argument("--agent_name", type=str, required=True, help="The name of the agent to use.", choices=AGENTS)
    args = parser.parse_args()

    agent_class = import_agent(args.agent_name)

    if agent_class is not None:
        agent_instance = agent_class(OPENAI_API_KEY, args.category)
        agent_instance.run()
    else:
        print(f"{args.agent_name} could not be imported or instantiated.")
