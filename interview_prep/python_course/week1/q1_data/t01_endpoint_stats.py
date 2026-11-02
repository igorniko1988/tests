"""Q1 t01 (★ optional, ~20 min). Endpoint stats from an access log.

You get access log lines like:
    "GET /orders 200 15ms"
    method, path, status code, duration.

Return a dict {path: {"count": int, "errors": int}}:
- count - number of requests to the path;
- errors - number of requests with status >= 500;
- paths in order of first appearance.
Skip lines that do not have exactly 4 parts or whose status is not a number.

Example:
    endpoint_stats([
        "GET /orders 200 15ms",
        "POST /orders 503 120ms",
        "GET /health 200 1ms",
        "broken line",
        "GET /orders 500 30ms",
    ]) -> {"/orders": {"count": 3, "errors": 2}, "/health": {"count": 1, "errors": 0}}

Follow-up questions:
- How do you check that the status is a number without try/except? With it?
- How would you add the error rate in percent?

Run (from interview_prep/python_course/week1/q1_data): uv run pytest -k t01
Теория: interview_prep/python_course/c03_collections/s05_counter_defaultdict/THEORY.md.
"""


def endpoint_stats(lines: list[str]) -> dict[str, dict[str, int]]:
    raise NotImplementedError
