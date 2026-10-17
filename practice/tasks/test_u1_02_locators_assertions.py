"""U1. Урок 2 — локаторы и проверки подробно.

Теория: practice/u1_02_locators_assertions.md
Запуск:
    uv run pytest tests/ui/test_u1_02_locators_assertions.py --base-url http://localhost:8080 --headed

Правила для всех задач:
    - только page.goto("/app/") (без полного адреса);
    - уникальный email через uuid4;
    - локаторы по приоритету: роль → label/placeholder/text → test-id → CSS. XPath нельзя;
    - никаких sleep, is_visible() и count() в проверках — только expect.

Задача 0. Хелперы.
    Напиши функции register(page) -> str (регистрирует нового пользователя и ждёт кабинет)
    и deposit(page, asset, amount) (пополняет и ждёт тост "Баланс <asset> пополнен").
    Используй их в задачах ниже.

Задача 1. Форма входа целиком.
    Открой /app/. Одной проверкой to_match_aria_snapshot проверь блок auth-page:
    заголовок "Вход" уровня 2, поля Email и Пароль, кнопки "Войти" и "Зарегистрироваться".
    Отдельно: у поля Пароль атрибут type="password", у поля Email — type="email".

Задача 2. Пустой список ордеров.
    Новый пользователь: виден текст "Ордеров пока нет", строк ордеров 0 (to_have_count).

Задача 3. Три ордера и фильтры локаторов.
    Пополни USDT 1000 и ETH 10. Размести три ордера на ETH-USDT:
        BUY  цена 100 кол-во 1
        BUY  цена 101 кол-во 1
        SELL цена 500 кол-во 2
    Сторону выбирай через get_by_label("Купить"/"Продать").check().
    Проверь:
        - строк ордеров 3;
        - строк с SELL ровно 1 (filter(has_text=...));
        - у всех статус NEW — ОДНОЙ проверкой списком (to_have_text([...]));
        - у строки SELL в колонке "Исполнено" 0 (get_by_test_id("order-filled") внутри строки).

Задача 4. Отмена конкретного ордера.
    Создай два BUY-ордера с ценами 100 и 200. Отмени тот, что с ценой 200:
    найди строку по цене (не через nth!), нажми "Отменить" внутри строки.
    Проверь:
        - у этой строки статус CANCELED, кнопки "Отменить" в ней больше нет (to_have_count(0));
        - у ордера с ценой 100 статус по-прежнему NEW и кнопка есть;
        - выбери фильтр "Статус" = CANCELED: в таблице одна строка, и в ней цена 200.

Задача 5. Ошибка валидации ордера.
    Нажми "Разместить ордер" с пустыми ценой и количеством.
    Проверь: ошибка (role="alert" внутри формы ордера) видна и содержит "price" и "quantity"
    (to_contain_text или регулярка). Тост не появился.

Задача 6. Блокировка средств.
    Пополни USDT 1000, размести BUY ETH-USDT цена 100 кол-во 2.
    Проверь в строке USDT таблицы балансов: "Доступно" 800, "Заблокировано" 200.
    Отмени ордер — снова 1000 и 0.
    Подсказка: числа могут прийти как "800" или "800.00" — подумай, какую проверку выбрать
    (to_have_text с регуляркой?). Если результат не совпадает с ожидаемым — это повод
    разобраться, а не подгонять тест.

Вопросы собеса (ответы — в разделе «Собес» теории; ответь своими словами в секции «Ответы»):
    1. Как работает get_by_role? Что такое accessible name? So how does it works browser build accesability tree in the dom tree and playwright looking for the element with role
    2. Как найти кнопку в нужной строке таблицы? find string in the table for example using has-text and than in founded element finds needed element
    3. Чем отличаются to_have_text и to_contain_text? Как проверить список? to have text checking the whole text, and containing only the part
    4. Почему не assert loc.is_visible() / assert loc.count() == 3? is visible works without timing , count with timeot may be
    5. Что делать, если у элементов нет ни ролей, ни test-id? asks for developers to add ids
    6. Чем отличаются to_be_hidden, not_to_be_visible, to_be_attached, to_have_count(0)? to be hidden - may be with disable state, no to be visible - disable state, to be attached may be only in the dom tree
    , count can be not visible may be but exists in the dom tree
    7. Как проверить структуру формы целиком? using aria snapshow in the yaml format, codegen suits very good with it
"""

# Решение пиши в tests/ui/test_u1_02_locators_assertions.py — файл и папки создаёшь сам.
