# F4. Урок 3 — Kubernetes на уровне QA

Задания: `practice/f4_03_kubernetes_answers.md`. Манифест стенда: `k8s/exchange.yaml`.

## Зачем QA

В компаниях стенды (dev, stage) обычно крутятся в Kubernetes. QA не настраивает кластер, но должен уметь:
найти свой сервис, посмотреть логи и статус, понять, почему под перезапускается, пробросить порт
к сервису для отладки. На собесе — «тест упал на стенде в k8s, что будешь делать».

## 1. Основные объекты

```text
Namespace "exchange"
 ├── Deployment exchange (replicas: 2) ──создаёт──▶ Pod exchange-7c9-abc, Pod exchange-7c9-xyz
 ├── Service exchange :8000 ──раздаёт трафик на──▶ эти поды
 ├── Deployment db ──▶ Pod db-5f4-qwe
 ├── Service db :5432
 ├── ConfigMap exchange-config   (обычные настройки: CHAOS_RATE)
 └── Secret exchange-secrets     (пароли, JWT-секрет)
```

| Объект | Что это | Аналогия с compose |
|---|---|---|
| **Pod** | 1+ контейнеров, самая мелкая единица; одноразовый, имя меняется | контейнер |
| **Deployment** | «держи N одинаковых подов», перезапускает упавшие, обновляет версию | сервис с `replicas` |
| **Service** | постоянное имя и адрес для набора подов, балансирует | имя сервиса в сети compose |
| **ConfigMap** | настройки как переменные/файлы | `environment` |
| **Secret** | то же для секретов (base64, не шифрование!) | `.env` с паролями |
| **Namespace** | папка для объектов одного проекта/окружения | отдельный compose-проект |
| **Ingress** | вход снаружи по домену и пути | `ports` |

Поды умирают и пересоздаются — поэтому к ним обращаются через **Service**, а не по IP пода.

## 2. Probes — как k8s понимает, что сервис жив

- **readinessProbe** — «готов принимать трафик?». Пока нет — Service не шлёт на под запросы.
- **livenessProbe** — «жив?». Если нет — k8s **перезапускает** контейнер.

В нашем манифесте обе бьют в `/health`. Если `/health` начнёт падать — поды будут перезапускаться,
в `kubectl get pods` вырастет `RESTARTS`.

## 3. kubectl — команды QA

```bash
kubectl config get-contexts              # к каким кластерам есть доступ;  use-context — переключиться
kubectl get ns                           # namespaces
kubectl -n exchange get pods             # поды: STATUS, RESTARTS, AGE
kubectl -n exchange get pods -o wide     # + на какой ноде, IP
kubectl -n exchange get deploy,svc,cm    # несколько типов сразу
kubectl -n exchange describe pod <pod>   # подробно + Events внизу — ПЕРВОЕ, что смотреть при проблеме
kubectl -n exchange logs <pod>           # логи;  -f — в реальном времени;  --previous — до перезапуска
kubectl -n exchange logs -l app=exchange --prefix   # логи всех подов по метке
kubectl -n exchange exec -it <pod> -- sh # зайти в под
kubectl -n exchange port-forward svc/exchange 8082:8000   # localhost:8082 → сервис в кластере
kubectl -n exchange rollout restart deploy/exchange       # перезапустить все поды
kubectl -n exchange get events --sort-by=.lastTimestamp   # события namespace
```

`-n exchange` можно не писать каждый раз: `kubectl config set-context --current --namespace=exchange`.

## 4. Статусы подов и что они значат

| STATUS | Причина | Где смотреть |
|---|---|---|
| `Running`, READY 1/1 | всё хорошо | — |
| `Running`, READY 0/1 | readiness не проходит (например, нет БД) | `describe` → Events, `logs` |
| `Pending` | нет ресурсов на нодах / не может примонтировать | `describe` → Events |
| `ImagePullBackOff` / `ErrImagePull` | неверный образ/тег, нет доступа к registry | `describe` |
| `CrashLoopBackOff` | контейнер падает сразу после старта | `logs --previous` |
| `OOMKilled` | превысил лимит памяти | `describe` → Last State |
| `Terminating` завис | не может корректно остановиться | `describe` |

## 5. Как тесты ходят к стенду в k8s

- снаружи — через **Ingress** (домен stage.company.com) — так обычно в CI;
- для отладки — **port-forward** на свой localhost;
- тесты внутри кластера (Job) — по имени сервиса `http://exchange.exchange.svc.cluster.local:8000`
  (сервис.namespace.svc...).

Несколько реплик: запросы одного теста могут попасть в **разные поды**. Логи одного сценария
надо искать во всех подах — поэтому важны request id и централизованные логи (урок 4).

## Практика: поднять стенд в k8s

1. Docker Desktop → Settings → Kubernetes → **Enable Kubernetes** → Apply (подождать, пока станет зелёным).
2. `kubectl config use-context docker-desktop`
3. `docker compose build exchange` (образ `api_learning-exchange:latest` должен быть локально).
4. `kubectl apply -f k8s/exchange.yaml`
5. `kubectl -n exchange get pods -w` — дождаться Running 1/1 (Ctrl+C).
6. `kubectl -n exchange port-forward svc/exchange 8082:8000` → http://localhost:8082/docs.

Убрать всё: `kubectl delete namespace exchange`. Кластер потребляет ресурсы — выключай в настройках, когда не нужен.

## Вопросы собеседования

1. Что такое pod, deployment, service? Почему обращаются к service, а не к поду?
2. Чем ConfigMap отличается от Secret?
3. readiness vs liveness probe?
4. Под в `CrashLoopBackOff` — твои действия?
5. Как посмотреть логи пода, который уже перезапустился?
6. Как подключиться к сервису в кластере со своего ноутбука?
