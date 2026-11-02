"""Q2 t04 (required, ~20 min). Send items in batches and collect failures.

Implement send_in_batches(items, n, send) that sends items in batches of n by calling
send(batch) (batch is a list; the last one may be shorter).

If send raises an exception for a batch, do NOT stop: remember the batch number
(starting from 0) and continue with the next batch.

Return a dict:
    {"sent": <number of items in successful batches>, "failed": [<batch numbers>]}

Requirements:
- items may be a generator: no len(), no slicing of items.
- n < 1 -> ValueError.

Example:
    def send(batch):
        if 3 in batch:
            raise ConnectionError
    send_in_batches(range(1, 8), 3, send)
        # batches [1,2,3] [4,5,6] [7] -> first fails
        -> {"sent": 4, "failed": [0]}

Follow-up questions:
- When should you stop at the first error instead of continuing?

Run (from interview_prep/python_course/week2/q2_function_utils): uv run pytest -k t04
Теория: THEORY.md в этой папке, раздел 5.
"""


def send_in_batches(items, n: int, send) -> dict:
    raise NotImplementedError
