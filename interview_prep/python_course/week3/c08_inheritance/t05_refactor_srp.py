"""C8 t05 (required, ~25 min). Split a god class (Single Responsibility).

The class below does everything at once. Split it into three classes with one job each,
and a thin service that composes them:

- OrderValidator.validate(order: dict) -> list[str]: error messages, in this order:
    "symbol is required"         if no non-empty "symbol";
    "qty must be positive"       if "qty" is missing or <= 0;
    "side must be BUY or SELL"   if "side" not in ("BUY", "SELL");
- OrdersApi(session).create(order) -> session.request("POST", "/orders", json=order);
- ReportFormatter.format(order, response) -> f"{side} {qty} {symbol}: {response['status']}";
- OrderService(validator, api, formatter).place(order):
    errors -> raise ValueError("; ".join(errors)); otherwise create and return the formatted line.

Keep the behaviour of the old OrderManager.place(order). You may delete OrderManager.

Follow-up questions:
- Name the "reasons to change" of the old class.
- How did testing get easier after the split?

Run (from interview_prep/python_course/week3/c08_inheritance): uv run pytest -k t05
Теория: THEORY.md в этой папке, раздел 9.
"""


class OrderManager:
    def __init__(self, session) -> None:
        self.session = session

    def place(self, order: dict) -> str:
        errors = []
        if not order.get("symbol"):
            errors.append("symbol is required")
        if order.get("qty", 0) <= 0:
            errors.append("qty must be positive")
        if order.get("side") not in ("BUY", "SELL"):
            errors.append("side must be BUY or SELL")
        if errors:
            raise ValueError("; ".join(errors))
        response = self.session.request("POST", "/orders", json=order)
        return f"{order['side']} {order['qty']} {order['symbol']}: {response['status']}"


class OrderValidator:
    pass


class OrdersApi:
    pass


class ReportFormatter:
    pass


class OrderService:
    pass
