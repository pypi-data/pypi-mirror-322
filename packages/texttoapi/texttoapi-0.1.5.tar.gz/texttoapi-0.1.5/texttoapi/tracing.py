import os
import requests
# Old code.
# from opentelemetry.instrumentation.llamaindex import LlamaIndexInstrumentor
# LlamaIndexInstrumentor().instrument()
# from traceloop.sdk import Traceloop
# Traceloop.init(api_endpoint="https://api.traceloop.com", disable_batch=True)

# Set up tracing and logging
from openinference.instrumentation.llama_index import LlamaIndexInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk import trace as trace_sdk
from opentelemetry.sdk.trace.export import SimpleSpanProcessor

from . import env

# Configure the logger
logger = env.getLogger(os.path.basename(__file__))

def init_tracing():
    try:
        if requests.get(env.trace_url, timeout=3).status_code == 200:
            tracer_provider = trace_sdk.TracerProvider()
            tracer_provider.add_span_processor(SimpleSpanProcessor(OTLPSpanExporter(env.trace_url)))

            LlamaIndexInstrumentor().instrument(tracer_provider=tracer_provider)
            logger.debug("Tracing enabled")
    except Exception:
        logger.debug("Tracing not enabled")

