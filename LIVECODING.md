# Тренажёр лайвкодинга

Задачи в стиле собеседований AQA. Тренажёр: `docker compose up -d trainer` → http://localhost:8090.

Правила: таймер 30 минут, исходник `trainer/` не открывать, решение — в `livecoding/task_NN.py`,
запуск — `uv run pytest livecoding/task_01.py -v`.

---

## Задача 1. Список объявлений

1. Описать тест-кейсы / чек-лист для эндпоинта.
2. Реализовать автотест на Python (requests + pytest) на самый важный кейс, затем — на остальные, сколько успеешь.

```
GET http://localhost:8090/v1/ads/

Параметры:
  commercial: int, 0..100 — процент коммерческих объявлений в выдаче (обязательный)

Ответ 200:
  {
    "count": int,                       — сколько объявлений в ads
    "ads": [
      {
        "ad_id": int,                   — уникальный id
        "type": str,                    — commercial | nonprofit
        "format": str                   — video | picture
      }
    ]
  }

Ошибка: невалидный или отсутствующий commercial → 400 {"error": "bad_request"}
В выдаче всегда 20 объявлений.
```
