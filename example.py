events = [
    {"sensor_id": "cam-1",   "seq": 1, "ts": "2026-10-28T10:00:00.000"},
    {"sensor_id": "cam-1",   "seq": 2, "ts": "2026-10-28T10:00:00.100"},
    {"sensor_id": "cam-1",   "seq": 5, "ts": "2026-10-28T10:00:00.400"},
    {"sensor_id": "radar-7", "seq": 1, "ts": "2026-10-28T10:00:00.050"},
    {"sensor_id": "radar-7", "seq": 1, "ts": "2026-10-28T10:00:00.051"},
]

filtered_events = {}

for event in events:
    for k,v in event.items():
        if k == 'seq':
            filtered_events[k] = filtered_events.get(k, 0 ) + 1

print(filtered_events)