import markdown2
import os
from http import HTTPStatus

from . import env
from . import chat_utils

# Configure the logger
logger = env.getLogger(os.path.basename(__file__))

class Response(chat_utils.Response):
    def __init__(self, question = None, gpt_response = None, time_taken = None, tool_calls = None, verbose_response = None, json_response = None):
        super().__init__(question, gpt_response, time_taken, tool_calls, verbose_response, json_response)
        self.html_response = html_response_pretty(gpt_response.response)

def html_response_pretty(gpt_response: str) -> str:
    """
    Convert a GPT response in Markdown format to plain text, preserving bullet points and line breaks.

    Args:
        gpt_response (str): The response from the OpenAI API in Markdown format.

    Returns:
        str: The plain-text response.
    """
    # Convert Markdown to HTML
    return markdown2.markdown(gpt_response)

def post_chat(chat_history, user_input):
    try:
        response = chat_utils.chat_with_agent(chat_history, user_input)
        response = Response(response.question, response.gpt_response, response.time_taken, response.tool_calls, response.verbose_response, response.json_response)
        return response, HTTPStatus.OK
    except Exception as e:
        logger.error(f"Error processing user input: {user_input}")
        logger.error(f"Error details: {str(e)}")
        return None, HTTPStatus.BAD_REQUEST
