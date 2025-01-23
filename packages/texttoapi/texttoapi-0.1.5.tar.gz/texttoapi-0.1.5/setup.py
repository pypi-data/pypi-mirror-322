from setuptools import setup, find_packages

setup(
    name="texttoapi",
    version="0.1.5", 
    description="A package for the TextToAPI tool",
    author="Gopesh Sharma",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "setuptools==75.6.0",
        "python-dotenv==1.0.1",
        "llama-index==0.12.1",
        "llama-index-embeddings-azure-openai==0.3.0",
        "llama-index-embeddings-bedrock==0.4.0",
        "llama-index-llms-azure-openai==0.3.0",
        "llama-index-llms-bedrock-converse==0.4.0",
        "openinference-instrumentation-llama-index==3.0.4",
        "opentelemetry-sdk==1.28.2",
        "opentelemetry-exporter-otlp==1.28.2",
        "opentelemetry-proto==1.28.2",
        "rich==13.9.4",
        "markdown2==2.5.2",
        "Flask",
    ],
    python_requires=">=3.7",
)
