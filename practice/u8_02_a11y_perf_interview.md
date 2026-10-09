# U8. Урок 2 — доступность и производительность фронта; собес по модулю U8

Задания: `tests/ui/test_u8_02_a11y_perf.py`.

План: доступность (a11y) — что это и кому нужно; axe-core через `axe-playwright-python` (проверено:
находит проблемы на лаборатории и 0 в кабинете); что автоматическая проверка не найдёт — и как дотестировать
Playwright'ом (роли, имена, фокус, клавиатура); производительность фронта — Navigation Timing, Web Vitals
(LCP, CLS, INP), метрики CDP, число и размер запросов; бюджеты без флейков; собес по U8.

---

## 1. Доступность

**Accessibility (a11y)** — сайтом могут пользоваться люди с особенностями: незрячие (скринридер), слабовидящие
(контраст, масштаб), без мыши (клавиатура), с моторными нарушениями. Стандарт — **WCAG 2.1/2.2**, уровни A / AA / AAA;
в требованиях обычно **AA**. Для многих компаний это закон (EAA в ЕС с 2025, ADA в США).

Для тестировщика это не отдельный мир: **локаторы по ролям** (U1.2) уже проверяют доступность — если
`get_by_role("button", name="Пополнить")` не находит кнопку, её не найдёт и скринридер.

---

## 2. axe-core в Playwright

axe-core — движок автоматических проверок доступности (Deque). Для Python — пакет `axe-playwright-python`
(в группе `tests`):

```python
from axe_playwright_python.sync_playwright import Axe

axe = Axe()
results = axe.run(page)                                  # проверка текущей страницы
results.violations_count                                 # число правил с нарушениями
for v in results.response["violations"]:
    print(v["id"], v["impact"], v["help"], len(v["nodes"]))
    for node in v["nodes"]:
        print("   ", node["target"], node["failureSummary"])
print(results.generate_report())                         # читаемый отчёт — приложить в Allure
```

Проверено: на лаборатории axe находит **3 правила** с нарушениями (разной серьёзности), в кабинете `/app/` — **0**.
Какие именно на лаборатории — найдёшь в задании 1.

| Поле | Что |
|---|---|
| `id` | правило: `image-alt`, `color-contrast`, `button-name`, `label`, `region`, `landmark-*` … |
| `impact` | `critical`, `serious`, `moderate`, `minor` |
| `nodes[].target` | CSS-путь к элементу |
| `help`, `helpUrl` | что не так и ссылка на объяснение |

Настройки: проверить часть страницы (`axe.run(page, context="#dashboard")`), только нужные стандарты
(`options={"runOnly": {"type": "tag", "values": ["wcag2a", "wcag2aa"]}}`), отключить правило.

### Как встроить

- тест на ключевые страницы: «нет нарушений `critical` и `serious`» — порог, а не «ноль всего»;
- известные нарушения — **список исключений** с ссылками на задачи (как карантин, U2.4), иначе тест вечно красный
  и его выключат;
- проверять **разные состояния**: открытое меню, ошибка формы, модалка — axe видит только текущий DOM.

---

## 3. Чего axe не найдёт

Автоматика находит примерно **треть** проблем доступности. Остальное — поведение:

| Проблема | Как проверить Playwright'ом |
|---|---|
| кнопка-иконка с «именем» `⟳` — формально имя есть, по смыслу нет | `expect(button).to_have_accessible_name("Обновить")` |
| порядок фокуса | `page.keyboard.press("Tab")` + `expect(el).to_be_focused()` по цепочке |
| форма проходится без мыши | Tab, ввод, Enter — сценарий только клавиатурой |
| фокус после закрытия модалки возвращается на кнопку | `to_be_focused()` после закрытия |
| ошибка поля связана с полем | `to_have_accessible_description` / `to_have_accessible_error_message` |
| структура и имена | `to_match_aria_snapshot` (U1.2) |
| динамические сообщения читаются скринридером | у тоста `role="status"` (U4.2): `to_have_role("status")` |

---

## 4. Производительность фронта

Это **не** нагрузочное тестирование (Locust — в части API): здесь один пользователь, вопрос — насколько быстро
страница отрисовывается и откликается.

### Navigation Timing

```python
nav = page.evaluate("performance.getEntriesByType('navigation')[0].toJSON()")
ttfb = nav["responseStart"] - nav["requestStart"]       # время до первого байта
dcl = nav["domContentLoadedEventEnd"]                    # HTML разобран
load = nav["loadEventEnd"]                               # всё загружено
```

### Web Vitals

| Метрика | Что | Хорошо |
|---|---|---|
| **LCP** (Largest Contentful Paint) | отрисован самый большой элемент | < 2,5 с |
| **CLS** (Cumulative Layout Shift) | насколько «прыгает» вёрстка | < 0,1 |
| **INP** (Interaction to Next Paint) | отклик на действие пользователя | < 200 мс |
| FCP (First Contentful Paint) | первый контент на экране | < 1,8 с |

Собрать — подписаться на события до загрузки:

```python
page.add_init_script("""
  window.__vitals = {lcp: 0, cls: 0};
  new PerformanceObserver(list => {
    for (const e of list.getEntries()) window.__vitals.lcp = e.startTime;
  }).observe({type: 'largest-contentful-paint', buffered: true});
  new PerformanceObserver(list => {
    for (const e of list.getEntries()) if (!e.hadRecentInput) window.__vitals.cls += e.value;
  }).observe({type: 'layout-shift', buffered: true});
""")
page.goto("/app/lab.html")
vitals = page.evaluate("window.__vitals")
fcp = page.evaluate("performance.getEntriesByName('first-contentful-paint')[0]?.startTime")
```

Проверено на лаборатории (локально): TTFB ≈ 3 мс, DCL ≈ 130 мс, load ≈ 135 мс, LCP = FCP ≈ 176 мс, CLS = 0.
INP требует реального взаимодействия — его меряют действием (клик) и событием `event` в PerformanceObserver
или библиотекой `web-vitals`.

### CDP и сеть

```python
cdp = page.context.new_cdp_session(page)
cdp.send("Performance.enable")
metrics = {m["name"]: m["value"] for m in cdp.send("Performance.getMetrics")["metrics"]}
metrics["JSHeapUsedSize"], metrics["Nodes"], metrics["LayoutCount"]
```

Число и вес запросов — `page.on("response", ...)`: страница грузит 150 запросов или картинку 5 МБ — это видно и без
Lighthouse. Lighthouse (полный аудит) запускают отдельно (CLI) на тех же страницах.

### Бюджеты без флейков

- метрики **шумят**: CI медленнее (U7.2), соседние джобы. Порог — с запасом (LCP < 2,5 с, а не < 200 мс);
- несколько замеров и **медиана**, а не один;
- одинаковые условия: throttling сети и CPU (U2.1, U7.2) — сравнимо от прогона к прогону;
- отдельный маркер (`perf`) и отдельный прогон — не мешать функциональным тестам;
- тренд важнее одного числа: писать метрики в отчёт и смотреть, как меняются от релиза к релизу.

---

## 5. Шпаргалка по модулю U8

- Визуал (U8.1): в Python нет `to_have_screenshot` — своё сравнение Pillow + pixelmatch (`threshold`, допуск пикселей,
  actual/diff в отчёт); эталоны в git и в окружении CI; маски, скриншот элемента, моки, clock, `animations="disabled"`.
- Доступность (U8.2): axe через `axe-playwright-python`, порог по `impact`, исключения с задачами, разные состояния;
  axe находит треть — остальное ролями, именами, фокусом, клавиатурой.
- Производительность (U8.2): Navigation Timing, LCP/CLS/INP/FCP через PerformanceObserver, CDP-метрики, запросы;
  бюджеты с запасом, медиана, одинаковые условия, тренд.

---

## Собес: вопросы и ответы

Плюс вопросы U8.1 (4).

**1. Как проверяешь доступность в автотестах?**
> axe-core через Playwright на ключевых страницах и состояниях — меню, ошибки, модалки; падаю на critical и serious,
> известные проблемы — в исключениях с задачами. Плюс то, что axe не видит: имена кнопок по смыслу, порядок фокуса,
> прохождение сценария только клавиатурой, возврат фокуса, связь ошибок с полями. Локаторы по ролям — уже
> проверка доступности.

**2. Что такое Web Vitals и как их измерить в Playwright?**
> LCP — когда отрисован главный контент, CLS — насколько прыгает вёрстка, INP — отклик на действие; плюс FCP, TTFB.
> Подписываюсь через PerformanceObserver в init script до загрузки и читаю значения из страницы; Navigation Timing —
> через `performance.getEntriesByType`. Бюджеты — с запасом, медиана нескольких замеров, одинаковый throttling.

**3. Чем проверка производительности фронта отличается от нагрузочного тестирования?**
> Здесь один пользователь и вопрос «насколько быстро отрисовывается и откликается страница» — метрики браузера.
> Нагрузка — много одновременных пользователей и поведение сервера: RPS, перцентили, ошибки — это Locust или k6.

**4. Почему тесты производительности в CI флейкают?**
> Шумит окружение: другая машина, соседние джобы, сеть. Поэтому пороги с запасом, медиана, фиксированный throttling,
> отдельный прогон и внимание к тренду, а не к одному числу.
