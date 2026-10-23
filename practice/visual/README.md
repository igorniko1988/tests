# Визуализации по шагам

Каждая тема учёбы объясняется не только текстом, но и интерактивной страницей,
на которой видно, что происходит на каждом шаге. Страница открывается в браузере
без интернета: `open practice/visual/<файл>.html`.

## Что есть на каждой странице

- кнопки «Шаг →», «← Назад», «▶ Авто», стрелки на клавиатуре;
- код с подсветкой строки, которая выполняется сейчас;
- состояние: то, что меняется по ходу (изменённое выделено);
- пояснение простыми словами на каждом шаге: что произошло и почему;
- история шагов таблицей — так «прогоняют код глазами» на собесе;
- свой ввод или готовые примеры, включая граничные случаи;
- отдельная подсветка мест, где чаще всего ошибаются (и где ошибся ты).

## Что показывается как «состояние» в разных темах

| Тема | Что видно на шагах |
|------|--------------------|
| Алгоритмы, live coding | данные клетками, указатели, переменные, результат |
| Python core | объекты и ссылки, стек вызовов, области видимости, генераторы |
| pytest | порядок сбора и запуска, setup и teardown фикстур по scope, параметры, xdist-воркеры |
| API-тесты | запрос и ответ (метод, URL, заголовки, тело, статус), сессия и токен, ретраи |
| UI-тесты (Playwright, Selenium) | страница и DOM, локатор и найденный элемент, auto-wait, сетевые запросы |
| Фреймворк | слои: тест → фикстура → Page Object / клиент → HTTP или браузер |
| CI/CD | джобы, раннеры, артефакты, порядок `needs:` |
| SQL | таблицы, строки после каждого этапа: FROM → JOIN → WHERE → GROUP BY → HAVING → SELECT |

## Каталог

| Тема | Файл | Онлайн |
|------|------|--------|
| Live coding, t02 compress (RLE) | `interview_prep/livecoding_python/m01_arrays_strings/visual/t02_compress.html` | https://claude.ai/artifact/Az7JJPTVcBMREakNebWSbo |
| API-клиент: как токен попадает в каждый запрос | `practice/visual/api_auth_token.html` | https://claude.ai/artifact/JLuaXZz3yAGAYcvoD6XH7p |
| API-фреймворк: путь теста через слои и папки | `practice/visual/api_framework_layers.html` | https://claude.ai/artifact/XqLJ5YvqfTesE8Ero26soj |
| Settings и envs: откуда берётся каждое значение | `practice/visual/settings_env_sources.html` | https://claude.ai/artifact/Nb8YGKiw5bRqMuFAF8qLmg |
| Live coding, два указателя (Remove Element, к t03) | `interview_prep/livecoding_python/m01_arrays_strings/visual/two_pointers_remove_element.html` | https://claude.ai/artifact/4TmQK4gxy5BWFF5oMnuB2p |
| Live coding: какой паттерн выбрать (дерево решений) | `interview_prep/livecoding_python/pattern_picker.html` | https://claude.ai/artifact/WHT6kR9Rphaw4pznTSNQAk |
| Live coding, t03 move zeros | `interview_prep/livecoding_python/m01_arrays_strings/visual/t03_move_zeros.html` | https://claude.ai/artifact/CgpC6dE6zRLqWFBJ8Ashdd |
| Live coding, t08 merge sorted | `interview_prep/livecoding_python/m01_arrays_strings/visual/t08_merge_sorted.html` | https://claude.ai/artifact/JfzZMFJwvexGc3ku8KY499 |
| Live coding, t09 max profit | `interview_prep/livecoding_python/m01_arrays_strings/visual/t09_max_profit.html` | https://claude.ai/artifact/3215tZnLyjFNDAFpisESBV |
| pytest: кеш фикстур, почему credentials в тесте и в auth_api один | `practice/visual/pytest_fixture_cache.html` | https://claude.ai/artifact/6XpfucJ1jrZLu2rsGiXvtG |
