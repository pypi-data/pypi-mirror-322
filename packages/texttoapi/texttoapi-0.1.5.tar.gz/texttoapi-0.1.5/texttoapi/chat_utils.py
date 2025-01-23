import time
import datetime
import os
import re
from . import env
# Configure the logger
logger = env.getLogger(os.path.basename(__file__))

from . import llm

class Response:
    def __init__(self, question = None, gpt_response = None, time_taken = None, tool_calls = None, verbose_response = None, json_response = None):
        self.question = question
        self.gpt_response = gpt_response
        self.time_taken = time_taken
        self.tool_calls = tool_calls
        self.verbose_response = verbose_response
        self.json_response = json_response


def chat_with_agent(chat_history, user_input):
    start_time = time.time()
    
    response, captured_output = llm.chat_with_agent(user_input)

    # Extract function call and output to print
    # func, output= utils.extract_function_details(captured_output)

    tool_outputs = response.sources
    results = [(output.tool_name, output.raw_input) for output in tool_outputs if not output.is_error]

    for i in range(len(results)):
        logger.debug(f"gpt: function {i+1}: {results[i]}")
    
    # Calculate duration
    end_time = time.time()
    duration = end_time - start_time

    json_response = [output.raw_output for output in tool_outputs if not output.is_error]

    logger.info(f'Question: {user_input}')
    logger.info(f'Time taken: {datetime.datetime.fromtimestamp(duration).strftime("%S")} seconds')
    logger.debug("===json response===")
    logger.debug(json_response)
    logger.info("===gpt response===")
    logger.info(response)

    # Return structured data
    response = Response(user_input, response, duration, results, captured_output, json_response)
    return response

def extract_function_details(text):
    # Regular expressions to match the function call and function output sections
    function_call_pattern = r'=== Calling Function ===\nCalling function: (.*?) with args: (.*?)\n'
    function_output_pattern = r'=== Function Output ===\n(.*?)\n=== LLM Response ==='

    # Extract the function call with args
    function_call_match = re.findall(function_call_pattern, text)
    function_call = ""
    if function_call_match:
        for func in function_call_match:
            function_call += f"Calling function: {func[0]} with args: {func[1]}\n"
        # function_call = f"Calling function: {function_call_match.group(1)} with args: {function_call_match.group(2)}"
    else:
        function_call = "Function call not found"

    # Extract the nested functions
    nested_function_call_pattern = r'Calling function: (.*?)\n'
    # Extract the function call with args
    function_call_match = re.findall(nested_function_call_pattern, text)
    if function_call_match:
        for func in function_call_match:
            function_call += f"Calling function: {func}\n"

    # Extract the function output
    function_output_match = re.search(function_output_pattern, text, re.DOTALL)
    if function_output_match:
        function_output = f"Function Output: {function_output_match.group(1).strip()}"
    else:
        function_output = "Function output not found"

    return function_call, function_output