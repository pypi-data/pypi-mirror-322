import os
import logging
import inspect
from . import env
# Configure the logger
logger = env.getLogger(os.path.basename(__file__))
logging.getLogger("httpx").setLevel(logging.WARNING)

# Below import is used
import readline
from rich.markdown import Markdown
from rich.console import Console

import warnings
from urllib3.exceptions import InsecureRequestWarning
warnings.simplefilter('ignore', InsecureRequestWarning)

from . import chat_utils
import rlcompleter

class Response(chat_utils.Response):
    def __init__(self, question = None, gpt_response = None, time_taken = None, tool_calls = None, verbose_response = None, json_response = None):
        super().__init__(question, gpt_response, time_taken, tool_calls, verbose_response, json_response)
        self.cli_response = response_pretty(gpt_response.response)

autocomplete_commands = []

def completer(text, state):
    options = [i for i in autocomplete_commands if i.startswith(text)]
    if state < len(options):
        return options[state]
    else:
        return None

def autocomplete(commands):
    global autocomplete_commands
    autocomplete_commands = commands
    if 'libedit' in readline.__doc__:
        readline.parse_and_bind("bind ^I rl_complete")
    else:
        readline.parse_and_bind("tab: complete")

    readline.set_completer(completer)

def spinner():
    return Console().status("")
       
def printError(msg):
    logger.error(msg)
    if env.log_level <= logging.ERROR:
        print(msg)

def printInfo(msg):
    logger.info(msg)
    if env.log_level <= logging.INFO:
        print(msg)
    return spinner()

def printDebug(msg):
    logger.debug(msg)
    if env.log_level <= logging.DEBUG:
        print(msg)

def log_function_name():
    printInfo(f"Calling function: {inspect.stack()[1][3]}")

def response_pretty(response):
    return Markdown(response)

def display_response_pretty(response: str):
    """
    Display a response in Markdown format for better readability in the terminal.

    Args:
        response (str): The response from the OpenAI API in Markdown format.
    """
    Console().print(response_pretty(response))

def print_json_aligned(data, indent=0, is_top_level=True):
    """
    Recursively print JSON data in a structured format without braces, brackets, or extra symbols.
    Args:
    - data (dict or list): The JSON object to print.
    - indent (int): The current level of indentation for nested structures.
    - is_top_level (bool): Indicates if the function is at the top level to manage blank lines.
    """
    if isinstance(data, list):
        for item in data:
            print_json_aligned(item, indent, is_top_level=True)
    elif isinstance(data, dict):
        # Calculate the max key length at this level for alignment
        max_key_length = max(len(key) for key in data.keys())
        for key, value in data.items():
            if isinstance(value, dict):
                print(" " * indent + f"{key.ljust(max_key_length)} :")
                print_json_aligned(value, indent + 4, is_top_level=False)
            elif isinstance(value, list):
                print(" " * indent + f"{key.ljust(max_key_length)} :")
                print_json_aligned(value, indent + 4, is_top_level=False)
            else:
                print(" " * indent + f"{key.ljust(max_key_length)} : {value}")
        # Add a blank line after each top-level item for readability
        if is_top_level:
            print()
