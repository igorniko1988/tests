"""OpenTelemetry: трейсы запросов и SQL (asyncpg) уходят в Jaeger (UI http://localhost:16686).

Без EXCHANGE_OTEL_ENDPOINT выключено. Входящий заголовок traceparent (W3C) продолжает трейс клиента,
id трейса возвращается в ответе заголовком X-Trace-ID и пишется в строку лога.
"""

from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.asyncpg import AsyncPGInstrumentor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace.sampling import Decision, ParentBased, Sampler, SamplingResult
from opentelemetry.trace import SpanKind

from exchange.config import settings


class _ServerRootsOnly(Sampler):
    """Новый трейс начинается только с входящего запроса: фоновые SQL сопоставления не шумят."""

    def should_sample(self, parent_context, trace_id, name, kind=None, attributes=None, *_, **__):
        decision = Decision.RECORD_AND_SAMPLE if kind is SpanKind.SERVER else Decision.DROP
        return SamplingResult(decision, attributes)

    def get_description(self) -> str:
        return "ServerRootsOnly"


def install_tracing(app: FastAPI) -> None:
    if not settings.otel_endpoint:
        return
    resource = Resource.create({"service.name": settings.otel_service_name})
    provider = TracerProvider(resource=resource, sampler=ParentBased(root=_ServerRootsOnly()))
    exporter = OTLPSpanExporter(endpoint=f"{settings.otel_endpoint.rstrip('/')}/v1/traces")
    provider.add_span_processor(BatchSpanProcessor(exporter))
    trace.set_tracer_provider(provider)
    FastAPIInstrumentor.instrument_app(app, excluded_urls="health,app", tracer_provider=provider)
    AsyncPGInstrumentor().instrument(tracer_provider=provider)


def current_trace_id() -> str | None:
    context = trace.get_current_span().get_span_context()
    return format(context.trace_id, "032x") if context.is_valid else None
