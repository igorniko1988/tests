"""Mock interview — task 1 (≈25 min).

Our junction controller receives events from roadside sensors (cameras, radars).
Every sensor numbers its own events with a sequence number `seq`, starting from 1.

Write `find_issues(events)` that reports, for each sensor:
  - missing sequence numbers (gaps),
  - duplicated sequence numbers.

Then write pytest tests for it (in this file or in test_task1.py next to it).

Example:
    events = [
        {"sensor_id": "cam-1", "seq": 1, "ts": "2026-10-28T10:00:00.000"},
        {"sensor_id": "cam-1", "seq": 2, "ts": "2026-10-28T10:00:00.100"},
        {"sensor_id": "cam-1", "seq": 5, "ts": "2026-10-28T10:00:00.400"},
        {"sensor_id": "radar-7", "seq": 1, "ts": "2026-10-28T10:00:00.050"},
        {"sensor_id": "radar-7", "seq": 1, "ts": "2026-10-28T10:00:00.051"},
    ]
    find_issues(events) -> ?   # agree on the output format with the interviewer
"""


def find_issues(events):
    raise NotImplementedError
