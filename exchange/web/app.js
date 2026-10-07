// Фронтенд мини-биржи: ванильный JS поверх того же API.
// Токен хранится в localStorage, ордера обновляются раз в 2 секунды.

const $ = (selector) => document.querySelector(selector);
const byTestId = (id) => document.querySelector(`[data-testid="${id}"]`);

const state = {
  token: localStorage.getItem("token"),
  email: localStorage.getItem("email"),
  timer: null,
};

async function api(method, path, body) {
  const headers = { "Content-Type": "application/json" };
  if (state.token) headers.Authorization = `Bearer ${state.token}`;
  const response = await fetch(path, {
    method,
    headers,
    body: body === undefined ? undefined : JSON.stringify(body),
  });
  const data = await response.json().catch(() => null);
  if (response.status === 401 && state.token) logout();
  return { ok: response.ok, status: response.status, data };
}

function errorText(data) {
  const error = data && data.error;
  if (!error) return "Что-то пошло не так";
  if (error.details && error.details.length) {
    return error.details.map((d) => `${d.field}: ${d.message}`).join("; ");
  }
  return error.message;
}

function show(element, text) {
  element.textContent = text;
  element.hidden = false;
}

function toast(text) {
  const element = byTestId("toast");
  show(element, text);
  clearTimeout(toast.timer);
  toast.timer = setTimeout(() => (element.hidden = true), 2500);
}

// --- Авторизация ---------------------------------------------------------------

async function login(email, password) {
  const result = await api("POST", "/auth/login", { email, password });
  if (!result.ok) return show(byTestId("auth-error"), errorText(result.data));
  state.token = result.data.access_token;
  state.email = email;
  localStorage.setItem("token", state.token);
  localStorage.setItem("email", email);
  render();
}

async function register(email, password) {
  const result = await api("POST", "/auth/register", { email, password });
  if (!result.ok) return show(byTestId("auth-error"), errorText(result.data));
  await login(email, password);
  toast("Аккаунт создан");
}

function logout() {
  state.token = null;
  state.email = null;
  localStorage.removeItem("token");
  localStorage.removeItem("email");
  render();
}

$("#auth-form").addEventListener("submit", (event) => {
  event.preventDefault();
  const form = new FormData(event.target);
  byTestId("auth-error").hidden = true;
  login(form.get("email"), form.get("password"));
});

byTestId("register-button").addEventListener("click", () => {
  const form = new FormData($("#auth-form"));
  byTestId("auth-error").hidden = true;
  register(form.get("email"), form.get("password"));
});

byTestId("logout-button").addEventListener("click", logout);

// --- Балансы -------------------------------------------------------------------

async function loadBalances() {
  const result = await api("GET", "/balances");
  if (!result.ok) return;
  const rows = result.data.map(
    (b) => `<tr data-testid="balance-row" data-asset="${b.asset}">
      <td>${b.asset}</td>
      <td data-testid="balance-available">${b.available}</td>
      <td data-testid="balance-locked">${b.locked}</td>
    </tr>`,
  );
  $('[data-testid="balances-table"] tbody').innerHTML = rows.join("");
}

$("#deposit-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = new FormData(event.target);
  const button = byTestId("deposit-button");
  button.disabled = true;
  const result = await api("POST", "/balances/deposit", {
    asset: form.get("asset"),
    amount: form.get("amount"),
  });
  button.disabled = false;
  if (!result.ok) return toast(errorText(result.data));
  event.target.reset();
  toast(`Баланс ${result.data.asset} пополнен`);
  loadBalances();
});

// --- Ордера --------------------------------------------------------------------

async function loadOrders() {
  const status = byTestId("orders-filter").value;
  const result = await api("GET", status ? `/orders?status=${status}` : "/orders");
  if (!result.ok) return;
  byTestId("orders-empty").hidden = result.data.length > 0;
  const rows = result.data.map((o) => {
    const open = o.status === "NEW" || o.status === "PARTIALLY_FILLED";
    const cancel = open
      ? `<button type="button" class="danger" data-testid="cancel-order" data-id="${o.id}">Отменить</button>`
      : "";
    return `<tr data-testid="order-row" data-id="${o.id}">
      <td>${o.symbol}</td><td>${o.side}</td><td>${o.price}</td><td>${o.quantity}</td>
      <td data-testid="order-filled">${o.filled_quantity}</td>
      <td class="status" data-testid="order-status">${o.status}</td>
      <td>${cancel}</td>
    </tr>`;
  });
  $('[data-testid="orders-table"] tbody').innerHTML = rows.join("");
}

$("#order-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = new FormData(event.target);
  const error = byTestId("order-error");
  error.hidden = true;
  const button = byTestId("place-order-button");
  button.disabled = true;
  const result = await api("POST", "/orders", {
    symbol: form.get("symbol"),
    side: form.get("side"),
    price: form.get("price"),
    quantity: form.get("quantity"),
  });
  button.disabled = false;
  if (!result.ok) return show(error, errorText(result.data));
  event.target.reset();
  toast("Ордер размещён");
  loadOrders();
  loadBalances();
});

$('[data-testid="orders-table"]').addEventListener("click", async (event) => {
  const button = event.target.closest('[data-testid="cancel-order"]');
  if (!button) return;
  button.disabled = true;
  const result = await api("DELETE", `/orders/${button.dataset.id}`);
  if (!result.ok) return toast(errorText(result.data));
  toast("Ордер отменён");
  loadOrders();
  loadBalances();
});

byTestId("orders-filter").addEventListener("change", loadOrders);

// --- Отрисовка -----------------------------------------------------------------

function render() {
  const loggedIn = Boolean(state.token);
  byTestId("auth-page").hidden = loggedIn;
  byTestId("dashboard").hidden = !loggedIn;
  byTestId("user-panel").hidden = !loggedIn;
  clearInterval(state.timer);
  if (loggedIn) {
    byTestId("user-email").textContent = state.email;
    loadBalances();
    loadOrders();
    state.timer = setInterval(() => {
      loadOrders();
      loadBalances();
    }, 2000);
  } else {
    $("#auth-form").reset();
  }
}

render();
