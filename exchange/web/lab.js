// Лаборатория: элементы, которых нет в кабинете (вкладки, iframe, диалоги, файлы, drag & drop,
// бесконечная лента, Shadow DOM, окружение браузера). Данные генерируются на клиенте,
// бэкенд не нужен — страница для уроков U3 и U6.

const $ = (selector) => document.querySelector(selector);
const byTestId = (id) => document.querySelector(`[data-testid="${id}"]`);

function toast(text) {
  const element = byTestId("toast");
  element.textContent = text;
  element.hidden = false;
  clearTimeout(toast.timer);
  toast.timer = setTimeout(() => (element.hidden = true), 2500);
}

// --- Часы в шапке (меняются каждую секунду — мешают скриншотам) -------------------

function tick() {
  byTestId("lab-clock").textContent = new Date().toLocaleTimeString("ru-RU");
}
tick();
setInterval(tick, 1000);

// --- Меню «Ещё» по наведению ------------------------------------------------------

const menu = byTestId("more-menu");
menu.addEventListener("mouseenter", () => menu.classList.add("open"));
menu.addEventListener("mouseleave", () => menu.classList.remove("open"));

// --- Cookies --------------------------------------------------------------------

if (!document.cookie.split("; ").includes("consent=1")) byTestId("cookie-banner").hidden = false;
byTestId("cookie-accept").addEventListener("click", () => {
  document.cookie = "consent=1; path=/; max-age=31536000";
  byTestId("cookie-banner").hidden = true;
});

// --- Вкладки и окна ---------------------------------------------------------------

byTestId("popup-button").addEventListener("click", () => {
  window.open("calc.html", "calc", "width=420,height=320");
});
window.addEventListener("message", (event) => {
  if (event.data && event.data.type === "calc-result") {
    byTestId("popup-result").textContent = event.data.value;
  }
  if (event.data && event.data.type === "widget-subscribe") {
    byTestId("widget-message").textContent = `Подписка на ${event.data.symbol}`;
  }
});

// --- Диалоги ----------------------------------------------------------------------

byTestId("alert-button").addEventListener("click", () => {
  alert("Торги идут круглосуточно");
  byTestId("dialog-result").textContent = "Инфо показано";
});
byTestId("confirm-button").addEventListener("click", () => {
  const ok = confirm("Удалить всё избранное?");
  if (ok) $('[data-testid="watchlist-items"]').innerHTML = "";
  byTestId("dialog-result").textContent = ok ? "Избранное очищено" : "Отменено";
});
byTestId("prompt-button").addEventListener("click", () => {
  const name = prompt("Новое имя портфеля", byTestId("portfolio-name").textContent);
  if (name === null) {
    byTestId("dialog-result").textContent = "Переименование отменено";
    return;
  }
  if (!name.trim()) {
    byTestId("dialog-result").textContent = "Имя не может быть пустым";
    return;
  }
  byTestId("portfolio-name").textContent = name.trim();
  byTestId("dialog-result").textContent = "Портфель переименован";
});

// --- Импорт / экспорт -------------------------------------------------------------

function parseCsv(text) {
  const lines = text.trim().split(/\r?\n/);
  const header = lines.shift().split(",").map((h) => h.trim());
  const expected = ["symbol", "side", "price", "quantity"];
  if (header.join() !== expected.join()) throw new Error(`Ожидались колонки: ${expected.join(",")}`);
  return lines.filter(Boolean).map((line, i) => {
    const [symbol, side, price, quantity] = line.split(",").map((v) => v.trim());
    if (!["BUY", "SELL"].includes(side)) throw new Error(`Строка ${i + 2}: side должен быть BUY или SELL`);
    if (!(Number(price) > 0) || !(Number(quantity) > 0)) throw new Error(`Строка ${i + 2}: цена и количество > 0`);
    return { symbol, side, price, quantity };
  });
}

byTestId("import-input").addEventListener("change", async (event) => {
  const files = [...event.target.files];
  const status = byTestId("import-status");
  const tbody = $('[data-testid="import-table"] tbody');
  tbody.innerHTML = "";
  if (!files.length) {
    status.textContent = "Файлы не выбраны";
    return;
  }
  try {
    const rows = [];
    for (const file of files) {
      if (file.size > 1024 * 1024) throw new Error(`${file.name}: файл больше 1 МБ`);
      rows.push(...parseCsv(await file.text()));
    }
    tbody.innerHTML = rows
      .map((r) => `<tr data-testid="import-row"><td>${r.symbol}</td><td>${r.side}</td><td>${r.price}</td><td>${r.quantity}</td></tr>`)
      .join("");
    status.textContent = `Импортировано строк: ${rows.length} (файлов: ${files.length})`;
  } catch (error) {
    status.textContent = `Ошибка: ${error.message}`;
  }
});

byTestId("export-button").addEventListener("click", () => {
  const rows = [...document.querySelectorAll('[data-testid="quotes-table"] tbody tr')].map((tr) =>
    [...tr.children].map((td) => td.textContent).join(","),
  );
  const csv = ["ticker,price,change", ...rows].join("\n") + "\n";
  const link = document.createElement("a");
  link.href = URL.createObjectURL(new Blob([csv], { type: "text/csv" }));
  link.download = `quotes-${new Date().toISOString().slice(0, 10)}.csv`;
  link.click();
  toast("Файл сформирован");
});

byTestId("avatar-input").addEventListener("change", (event) => {
  const file = event.target.files[0];
  const preview = byTestId("avatar-preview");
  if (!file) return (preview.hidden = true);
  preview.src = URL.createObjectURL(file);
  preview.alt = file.name;
  preview.hidden = false;
});

// --- Избранное: drag & drop и клавиатура ------------------------------------------

const watchlist = byTestId("watchlist-items");
let dragged = null;
watchlist.addEventListener("dragstart", (event) => {
  dragged = event.target.closest("li");
  event.dataTransfer.effectAllowed = "move";
});
watchlist.addEventListener("dragover", (event) => event.preventDefault());
watchlist.addEventListener("drop", (event) => {
  event.preventDefault();
  const target = event.target.closest("li");
  if (!dragged || !target || dragged === target) return;
  const items = [...watchlist.children];
  if (items.indexOf(dragged) < items.indexOf(target)) target.after(dragged);
  else target.before(dragged);
  toast(`Порядок: ${[...watchlist.children].map((li) => li.textContent).join(", ")}`);
});

const tickerInput = byTestId("ticker-input");
tickerInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter") {
    const value = tickerInput.value.trim().toUpperCase();
    if (!value) return;
    if ([...watchlist.children].some((li) => li.textContent === value)) {
      toast(`${value} уже в избранном`);
      return;
    }
    const li = document.createElement("li");
    li.draggable = true;
    li.dataset.testid = "watch-item";
    li.textContent = value;
    watchlist.append(li);
    tickerInput.value = "";
    toast(`${value} добавлен`);
  }
  if (event.key === "Escape") tickerInput.value = "";
});

document.addEventListener("keydown", (event) => {
  if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "k") {
    event.preventDefault();
    byTestId("trades-search").focus();
  }
});

// --- Котировки: сортировка и фильтр -----------------------------------------------

const TICKERS = ["BTC", "ETH", "SOL", "XRP", "ADA", "DOGE", "DOT", "AVAX", "LINK", "LTC", "ATOM", "NEAR",
  "APT", "ARB", "OP", "TON", "TRX", "BCH", "XLM", "ETC"];
const quotes = TICKERS.map((ticker, i) => ({
  ticker,
  price: Number((((i * 7919) % 5000) + 1 + i / 100).toFixed(2)),
  change: Number(((((i * 37) % 21) - 10) / 2.5).toFixed(2)),
}));
const sort = { key: null, dir: 1 };

function renderQuotes() {
  const query = byTestId("trades-search").value.trim().toUpperCase();
  let rows = quotes.filter((q) => q.ticker.includes(query));
  if (sort.key) {
    rows = [...rows].sort((a, b) => (a[sort.key] > b[sort.key] ? 1 : a[sort.key] < b[sort.key] ? -1 : 0) * sort.dir);
  }
  $('[data-testid="quotes-table"] tbody').innerHTML = rows
    .map((q) => `<tr data-testid="quote-row"><td>${q.ticker}</td><td>${q.price}</td><td>${q.change}</td></tr>`)
    .join("");
  byTestId("quotes-count").textContent = `Показано: ${rows.length} из ${quotes.length}`;
  document.querySelectorAll("[data-sort]").forEach((button) => {
    const th = button.closest("th");
    th.setAttribute("aria-sort", button.dataset.sort !== sort.key ? "none" : sort.dir === 1 ? "ascending" : "descending");
  });
}

document.querySelectorAll("[data-sort]").forEach((button) =>
  button.addEventListener("click", () => {
    sort.dir = sort.key === button.dataset.sort ? -sort.dir : 1;
    sort.key = button.dataset.sort;
    renderQuotes();
  }),
);
let searchTimer;
byTestId("trades-search").addEventListener("input", () => {
  clearTimeout(searchTimer);
  searchTimer = setTimeout(renderQuotes, 300); // debounce, как в настоящих поисках
});
renderQuotes();

// --- Бесконечная лента ------------------------------------------------------------

const feed = byTestId("feed");
const FEED_TOTAL = 200;
let feedLoaded = 0;
let feedLoading = false;

function loadFeed() {
  if (feedLoading || feedLoaded >= FEED_TOTAL) return;
  feedLoading = true;
  setTimeout(() => {
    const items = [];
    for (let i = 0; i < 20 && feedLoaded < FEED_TOTAL; i += 1) {
      feedLoaded += 1;
      items.push(`<div class="feed-item" data-testid="feed-item">#${feedLoaded} ${TICKERS[feedLoaded % TICKERS.length]}-USDT</div>`);
    }
    feed.insertAdjacentHTML("beforeend", items.join(""));
    byTestId("feed-count").textContent =
      feedLoaded >= FEED_TOTAL ? `Загружено: ${feedLoaded}. Это все сделки` : `Загружено: ${feedLoaded}`;
    feedLoading = false;
  }, 400);
}
feed.addEventListener("scroll", () => {
  if (feed.scrollTop + feed.clientHeight >= feed.scrollHeight - 10) loadFeed();
});
loadFeed();

// --- Shadow DOM -------------------------------------------------------------------

class PriceTicker extends HTMLElement {
  connectedCallback() {
    const root = this.attachShadow({ mode: "open" });
    root.innerHTML = `
      <style>.box{display:flex;gap:8px;align-items:center;font-family:sans-serif}</style>
      <div class="box">
        <span part="symbol">${this.getAttribute("symbol")}</span>
        <span part="price" data-testid="ticker-price">${this.getAttribute("price")}</span>
        <button type="button" data-testid="ticker-follow">Следить</button>
      </div>`;
    root.querySelector("button").addEventListener("click", (event) => {
      const on = event.target.textContent === "Следить";
      event.target.textContent = on ? "Не следить" : "Следить";
      toast(on ? `Следим за ${this.getAttribute("symbol")}` : "Слежение выключено");
    });
  }
}
customElements.define("price-ticker", PriceTicker);

// --- Окружение браузера -----------------------------------------------------------

function renderEnv() {
  const tz = Intl.DateTimeFormat().resolvedOptions().timeZone;
  byTestId("env-timezone").textContent = tz;
  byTestId("env-locale").textContent = navigator.language;
  byTestId("env-number").textContent = new Intl.NumberFormat(navigator.language).format(1234567.891);
  byTestId("env-date").textContent = new Date("2030-01-15T12:00:00Z").toLocaleString(navigator.language, {
    timeZone: tz,
    dateStyle: "medium",
    timeStyle: "short",
  });
  byTestId("env-layout").textContent = matchMedia("(max-width: 600px)").matches ? "мобильный" : "десктоп";
  byTestId("env-online").textContent = navigator.onLine ? "онлайн" : "офлайн";
  byTestId("env-scheme").textContent = matchMedia("(prefers-color-scheme: dark)").matches ? "тёмная" : "светлая";
}
renderEnv();
window.addEventListener("online", renderEnv);
window.addEventListener("offline", renderEnv);
window.addEventListener("resize", renderEnv);

byTestId("geo-button").addEventListener("click", () => {
  const result = byTestId("geo-result");
  if (!navigator.geolocation) return (result.textContent = "Геолокация недоступна");
  navigator.geolocation.getCurrentPosition(
    (pos) => (result.textContent = `Широта ${pos.coords.latitude.toFixed(4)}, долгота ${pos.coords.longitude.toFixed(4)}`),
    (err) => (result.textContent = `Ошибка геолокации: ${err.code === 1 ? "доступ запрещён" : err.message}`),
    { timeout: 5000 },
  );
});

byTestId("notify-button").addEventListener("click", async () => {
  const result = byTestId("notify-result");
  if (!("Notification" in window)) return (result.textContent = "Уведомления не поддерживаются");
  const permission = await Notification.requestPermission();
  result.textContent = permission === "granted" ? "Уведомления включены" : `Уведомления: ${permission}`;
});

byTestId("copy-button").addEventListener("click", async () => {
  const result = byTestId("copy-result");
  try {
    await navigator.clipboard.writeText("0xA11CE0000000000000000000000000000000B0B");
    result.textContent = "Адрес скопирован";
  } catch (error) {
    result.textContent = `Не удалось скопировать: ${error.name}`;
  }
});

// --- Модальное окно подтверждения -------------------------------------------------

const overlay = byTestId("modal-overlay");
const withdrawButton = byTestId("withdraw-button");
const agree = byTestId("modal-agree");
const confirmButton = byTestId("modal-confirm");

function openModal(amount) {
  byTestId("modal-text").textContent = `Вывести ${amount} USDT на внешний кошелёк?`;
  agree.checked = false;
  confirmButton.disabled = true;
  overlay.hidden = false;
  agree.focus();
}

function closeModal(result) {
  overlay.hidden = true;
  byTestId("withdraw-result").textContent = result;
  withdrawButton.focus();                       // фокус возвращается на кнопку, открывшую окно
}

withdrawButton.addEventListener("click", () => {
  const amount = byTestId("withdraw-amount").value.trim();
  if (!(Number(amount) > 0)) {
    byTestId("withdraw-result").textContent = "Введите сумму больше 0";
    return;
  }
  openModal(amount);
});
agree.addEventListener("change", () => (confirmButton.disabled = !agree.checked));
confirmButton.addEventListener("click", () => {
  closeModal(`Заявка на вывод ${byTestId("withdraw-amount").value.trim()} USDT создана`);
  toast("Заявка создана");
});
byTestId("modal-cancel").addEventListener("click", () => closeModal("Вывод отменён"));
overlay.addEventListener("click", (event) => {
  if (event.target === overlay) closeModal("Вывод отменён");   // клик по фону
});
document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && !overlay.hidden) closeModal("Вывод отменён");
});
