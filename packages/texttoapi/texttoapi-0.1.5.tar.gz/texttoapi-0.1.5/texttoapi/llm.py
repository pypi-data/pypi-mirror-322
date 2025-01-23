import io
from llama_index.core.tools import FunctionTool
from llama_index.core.agent import FunctionCallingAgentWorker
from llama_index.core.agent import AgentRunner
from llama_index.core import VectorStoreIndex
from llama_index.core.objects import ObjectIndex
from llama_index.core import Settings
from llama_index.core.chat_engine import SimpleChatEngine
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.embeddings.bedrock import BedrockEmbedding
from llama_index.llms.bedrock_converse import BedrockConverse

from . import env

agent = None

def get_embed_model():
    if env.llm == "azure":
        if not (env.emdedding_model and env.embedding_deployment and env.api_key and env.endpoint and env.api_version):
            raise ValueError("Please provide llmEmbeddingModel, llmEmbeddingDeployment, llmApiKey, llmEndpoint and llmApiVersion in the .env file or as environment variables.")

        return AzureOpenAIEmbedding(
            model=env.emdedding_model,
            deployment_name=env.embedding_deployment,
            api_key=env.api_key,
            azure_endpoint=env.endpoint,
            api_version=env.api_version,
        )
    elif env.llm == "aws":
        if not (env.api_id and env.api_key and env.region):
            raise ValueError("Please provide llmApiId, llmApiKey, llmRegion in the .env file or as environment variables.")

        return BedrockEmbedding(
            aws_access_key_id=env.api_id,
            aws_secret_access_key=env.api_key,
            # aws_session_token=os.getenv("AWS_SESSION_TOKEN"),
            region_name=env.region,
            # profile_name="<aws-profile>",
        )

def get_llm():
    if env.llm == "azure":
        if not (env.model and env.api_key and env.endpoint and env.api_version):
            raise ValueError("Please provide llmModel, llmApiKey, llmEndpoint and llmApiVersion in the .env file or as environment variables.")
    
        return AzureOpenAI(
            model=env.model,
            api_key=env.api_key,
            deployment_name=env.model,
            azure_endpoint=env.endpoint,
            api_version=env.api_version,
        )
    elif env.llm == "aws":
        if not (env.model and env.api_id and env.api_key and env.region):
            raise ValueError("Please provide llmModel, llmApiId, llmApiKey, llmRegion in the .env file or as environment variables.")

        return BedrockConverse(
            model=env.model,
            aws_access_key_id=env.api_id,
            aws_secret_access_key=env.api_key,
            # aws_session_token="AWS Session Token to use",
            region_name=env.region,
        )


def get_tools(functions):
    # Convert functions to Llama Index tools
    return [FunctionTool.from_defaults(fn=fn) for fn in functions]

def init_agent(functions):
    llmv = get_llm()
    Settings.llm = llmv
    Settings.embed_model = get_embed_model()

    obj_index = ObjectIndex.from_objects(
        get_tools(functions),
        index_cls=VectorStoreIndex,
    )

    agent_worker = FunctionCallingAgentWorker.from_tools(
        tool_retriever=obj_index.as_retriever(similarity_top_k=6),
        llm=llmv,
        verbose=False,
        allow_parallel_tool_calls=False
        # system_prompt=env.llm_system_prompt
    )
    global agent
    agent = AgentRunner(agent_worker)

def chat_with_agent(user_input):
    output_capture = io.StringIO()
    # with contextlib.redirect_stdout(output_capture):
    response = agent.chat(user_input)
    # Get the captured output
    return response, output_capture.getvalue()

def chat(user_input):
    llmv = get_llm()
    chat_engine = SimpleChatEngine.from_defaults(llm=llmv)
    return chat_engine.chat(user_input)
