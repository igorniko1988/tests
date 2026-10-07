# F4. Урок 3 — задания

Теория: `practice/f4_03_kubernetes.md`. Сначала подними стенд в k8s по разделу «Практика» в теории.
Для каждой задачи — команда и коротко результат.

## Задача 1. Осмотр

- a) выведи все объекты namespace `exchange` (поды, deployments, services, configmaps, secrets);
- b) сколько подов у exchange и на каких IP;
- c) `describe` одного пода exchange: какой образ, какие переменные из ConfigMap/Secret, что в Events.

**Ответ:**


## Задача 2. Доступ и логи

- a) сделай port-forward и пройди через curl: register → login → GET /balances;
- b) выведи логи **всех** подов exchange с префиксом имени пода. В какие поды попали твои запросы?
- c) найди свой запрос по `X-Request-ID` в логах всех подов одной командой.

**Ответ:**


## Задача 3. Self-healing

- a) удали один под exchange (`kubectl delete pod ...`). Что произошло через несколько секунд? Почему?
- b) уменьши реплики до 1 (`kubectl scale deploy/exchange --replicas=1`), потом верни 2.

**Ответ:**


## Задача 4. Сломай и почини (1): образ

Поменяй образ на несуществующий: `kubectl -n exchange set image deploy/exchange api=api_learning-exchange:nope`.
Какой статус у новых подов? Что пишет `describe`? Почему старые поды продолжают работать?
Верни: `kubectl -n exchange rollout undo deploy/exchange`.

**Ответ:**


## Задача 5. Сломай и почини (2): конфиг

Поменяй в Secret `EXCHANGE_DATABASE_URL` на неверный хост (`kubectl -n exchange edit secret exchange-secrets`
или заново `apply` с изменённым файлом-копией), сделай `rollout restart`.
Что со статусом подов (READY, RESTARTS)? Что в `logs` и `logs --previous`? Почини.

**Ответ:**


## Задача 6. ConfigMap

Включи chaos 0.2 через ConfigMap и перезапусти deployment. Проверь, что часть запросов отвечает 503.
Почему после правки ConfigMap нужен рестарт подов?

**Ответ:**


## Вопросы собеса

1. Что такое pod, deployment, service? Почему обращаются к service, а не к поду?
2. Чем ConfigMap отличается от Secret?
3. readiness vs liveness probe?
4. Под в `CrashLoopBackOff` — твои действия?
5. Как посмотреть логи пода, который уже перезапустился?
6. Как подключиться к сервису в кластере со своего ноутбука?

**Ответы:**

