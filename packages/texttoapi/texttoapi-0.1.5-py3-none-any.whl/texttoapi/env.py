import os
import sys
import logging
import yaml

from dotenv import load_dotenv
load_dotenv()

config_path = os.getenv("CONFIG_PATH", "/app/config.yaml")
# Load YAML configuration from file
if os.path.exists(config_path):
    with open(config_path, "r") as f:
        try:
            config = yaml.safe_load(f)
            for key, value in config.items():
                os.environ[key] = str(value)
        except yaml.YAMLError as e:
            print(f"Failed to parse config file {config_path}: {e}")

log_level = logging.INFO if os.getenv("logLevel") == "info" else logging.DEBUG if os.getenv("logLevel") == "debug" else logging.ERROR

llm = os.getenv("llm")
api_version = os.getenv("llmApiVersion")
model=os.getenv("llmModel")
emdedding_model=os.getenv("llmEmbeddingModel")
embedding_deployment=os.getenv("llmEmbeddingDeployment")
api_key = os.getenv("llmApiKey")
api_id = os.getenv("llmApiId")
endpoint = os.getenv("llmEndpoint")
region = os.getenv("llmRegion")
data_limit = int(os.getenv("llmDataLimit")) * 1000 * 1000
llm_system_prompt = os.getenv("llmSystemPrompt")
trace_url = os.getenv("traceUrl")

if not llm:
    raise ValueError("Please provide llm name in the .env file or as environment variables. Example usage: llm=azure")

def getLogger(name):
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    return logger