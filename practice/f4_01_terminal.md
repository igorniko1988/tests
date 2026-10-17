# F4. Урок 1 — терминал: файлы, поиск, curl, jq, env, процессы и порты

Задания: `practice/f4_01_terminal_answers.md` (пиши туда команды и что увидел).

## Зачем QA

Стенды, CI-агенты и контейнеры — это Linux без мышки. Найти ошибку в логе, дёрнуть API, проверить,
кто занял порт, — всё делается из терминала. На собесе: «как посмотришь логи на сервере?».

## 1. Навигация и файлы

```bash
pwd                      # где я
ls -la                   # файлы, включая скрытые, с правами и размерами
cd practice              # перейти;  cd ..  — наверх;  cd ~  — домой
cat file.txt             # вывести файл целиком
head -n 20 file.txt      # первые 20 строк;  tail -n 20 — последние
less big.log             # листать: пробел/b, /текст — поиск, n — следующее, q — выход
mkdir -p a/b             # создать папки
cp, mv, rm, rm -r        # копировать, переместить, удалить (без корзины!)
```

## 2. Поиск: grep и find

```bash
grep "ERROR" app.log                 # строки с ERROR
grep -i "error" app.log              # без учёта регистра
grep -n "ERROR" app.log              # с номерами строк
grep -c "ERROR" app.log              # сколько строк
grep -v "health" app.log             # строки БЕЗ health
grep -C 3 "Traceback" app.log        # +3 строки контекста до и после
grep -r "base_url" framework/        # рекурсивно по папке
grep -E "status\": (4|5)[0-9]{2}" app.log   # регулярное выражение
find . -name "*.py" -mtime -1        # .py файлы, изменённые за сутки
```

## 3. Конвейер `|` — главная сила терминала

Вывод одной команды — вход следующей.

```bash
docker compose logs exchange | grep WARNING | tail -n 5
cat app.log | grep ERROR | wc -l                    # посчитать ошибки
grep -o '"path": "[^"]*"' app.log | sort | uniq -c | sort -rn | head   # топ эндпоинтов
```

`sort` — сортировать, `uniq -c` — схлопнуть одинаковые соседние строки со счётчиком, `wc -l` — число строк.

Перенаправление: `> file` — записать в файл (перезаписать), `>> file` — дописать, `2>&1` — ошибки туда же, куда вывод.

## 4. Живой лог: tail -f

```bash
tail -f app.log                         # смотреть, как появляются новые строки (Ctrl+C — выход)
docker compose logs -f exchange         # то же для контейнера
docker compose logs -f exchange | grep --line-buffered ERROR
```

Типичный приём: в одном окне `logs -f`, в другом запускаешь тест — видишь, что сервис делает.

## 5. curl — HTTP из терминала

```bash
curl http://localhost:8080/health
curl -i http://localhost:8080/health                    # с заголовками ответа
curl -s -o /dev/null -w "%{http_code} %{time_total}\n" http://localhost:8080/health   # только код и время
curl -X POST http://localhost:8080/auth/login \
     -H "Content-Type: application/json" \
     -d '{"email": "a@b.com", "password": "secret123"}'
curl -H "Authorization: Bearer $TOKEN" http://localhost:8080/balances
curl -v ...                                              # всё: заголовки запроса, TLS, редиректы
```

Флаги: `-X` метод, `-H` заголовок, `-d` тело, `-i` заголовки ответа, `-s` тихо, `-v` подробно.
**curl — лучший формат шагов в баг-репорте на API**: разработчик копирует и воспроизводит.
В DevTools / Playwright trace есть «Copy as cURL».

## 6. jq — разбор JSON

```bash
brew install jq
curl -s .../balances -H "..." | jq                       # красиво
... | jq '.[0]'                                          # первый элемент
... | jq '.[] | select(.asset == "USDT") | .available'   # фильтр и поле
... | jq -r '.access_token'                              # строка без кавычек
TOKEN=$(curl -s -X POST .../auth/login -H "Content-Type: application/json" -d '...' | jq -r .access_token)
```

`$(...)` — подставить вывод команды. Так токен попадает в переменную.

## 7. Переменные окружения

```bash
echo $HOME                         # прочитать
export BASE_URL=http://localhost:8080   # задать для этой сессии и дочерних процессов
BASE_URL=http://localhost:8081 uv run pytest   # задать только для одной команды
env | grep EXCHANGE                # посмотреть все
```

Через env в CI передают адрес стенда, логины и секреты — в коде их нет. Python читает `os.environ["BASE_URL"]`,
pydantic-settings делает это автоматически.

## 8. Процессы и порты

```bash
ps aux | grep uvicorn              # найти процесс
kill 12345                         # попросить завершиться;  kill -9 — убить принудительно
lsof -i :8080                      # кто слушает порт 8080 (macOS/Linux)
ss -tlnp                           # слушающие порты (Linux)
top / htop                         # нагрузка CPU и память
df -h ; du -sh *                   # место на диске
```

Классика: «Address already in use» → `lsof -i :8000` → `kill <pid>`.

## 9. Права и ssh (знать)

```bash
chmod +x run.sh                    # сделать исполняемым
ls -l → -rwxr-xr-- : владелец / группа / остальные (r чтение, w запись, x запуск)
ssh user@host                      # зайти на сервер
scp user@host:/var/log/app.log .   # скачать файл
```

## Вопросы собеседования

1. Как найти все ошибки в логе за последний час и посчитать их?
2. Как смотреть лог в реальном времени?
3. Что делает `|`? Пример полезного конвейера.
4. Как отправить POST с JSON и токеном через curl?
5. Порт занят — как найти и остановить процесс?
6. Зачем переменные окружения в тестах?
