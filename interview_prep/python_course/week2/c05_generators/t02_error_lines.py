"""C5 t02 (required, ~15 min). Stream ERROR lines from a big log file.

Implement a generator error_lines(path) that reads a text file lazily and yields
(line_number, line) for every line containing the word ERROR.

Requirements:
- line_number starts at 1; line has no trailing newline.
- Read line by line (`for line in file`), never read() / readlines(): logs can be
  gigabytes. The test checks the source.
- The file must be closed after the generator is fully consumed (use `with`).

Example (file content):
    10:00 INFO start
    10:01 ERROR db timeout
    10:02 ERROR auth failed

    list(error_lines(path)) -> [(2, "10:01 ERROR db timeout"), (3, "10:02 ERROR auth failed")]

Follow-up questions:
- What is the memory complexity, and why does file iteration give it?
- What happens to the open file if the consumer stops after the first item?

Run (from interview_prep/python_course/week2/c05_generators): uv run pytest -k t02
Теория: THEORY.md в этой папке, раздел 4, 9.
"""


def error_lines(path):
    raise NotImplementedError
