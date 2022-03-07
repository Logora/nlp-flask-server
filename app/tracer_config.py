import os
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

resource = Resource(attributes={
    "service.name": os.environ.get("SERVICE_NAME")
})

trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer(__name__)

otlp_exporter = OTLPSpanExporter(endpoint=os.environ.get("OTLP_EXPORTER_ENDPONT"), insecure=True)
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# console_exporter = ConsoleSpanExporter()
# console_span_processor = BatchSpanProcessor(console_exporter)
# trace.get_tracer_provider().add_span_processor(console_span_processor)