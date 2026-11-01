# Объединение фреймворка: статус (2026-11-02)

Ветка `refactor/unified-framework`. API-слой (`framework/api`) и UI-слой (`framework/ui`) собраны в один пакет
с общим ядром: `config/`, `data/`, `utils/`, `fixtures/`, `plugins/`. Тесты: `tests/unit|api|ui|e2e`.

## Сделано
- Один `Settings` (`framework/config/settings.py`, `get_settings()`), envs: `config/envs/dev|stage|k8s.env`.
- Один API-клиент (`framework/api/client.py`): `Accept`, таймаут, токен, ретраи только безопасных методов,
  POST повторяется только для `/orders` (Idempotency-Key). Playwright-клиент `ExchangeApi` удалён.
- Один генератор данных и одна фикстура `credentials`; `make_user` с уборкой за всеми пользователями.
- Allure: секреты в телах маскируются (`password`, токены, `secret`).
- Модели: `Profile` для `/me` (display_name, role), `Balance` на Decimal, `Order.type` с MARKET.
- `tests/e2e/`: вход по токену из API, депозит через API виден в UI. Маркер `smoke` у 5 ключевых тестов.
- Слой ставится маркером по папке (`framework/plugins/markers.py`), ruff проходит (line-length 120).
- Проверено на стенде: unit 10/10, api 16/16, smoke 5/5.

## Осталось
1. **UI-регистрация не открывает кабинет** с новым генератором (`@test.io`, пароль 12 символов) —
   10 UI-тестов в ERROR на фикстуре `logged_user`. Разобрать (домен / длина пароля / фронт) и прогнать UI целиком.
2. **CI по уровням** вместо `.github/workflows/tests.yml`: composite action подъёма стенда; PR — lint, unit, api,
   ui-smoke (`-m smoke`); main — полная регрессия; nightly — cross-browser; manual — выбор набора и браузера;
   Allure-отчёт артефактом. API-джоба больше не ставит браузер.
3. **Учебное пособие** простым языком: что где лежит и почему, путь теста через слои, фикстуры, данные, отчёты,
   CI, ответы для собеса. Обновить `CLAUDE.md` (пути `ui_framework/` → `framework/ui/`).
4. PR `refactor/unified-framework` → merge делает пользователь.
