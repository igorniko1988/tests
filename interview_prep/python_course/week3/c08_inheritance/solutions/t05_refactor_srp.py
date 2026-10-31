class OrderValidator:
    def validate(self, order: dict) -> list[str]:
        errors = []
        if not order.get("symbol"):
            errors.append("symbol is required")
        if order.get("qty", 0) <= 0:
            errors.append("qty must be positive")
        if order.get("side") not in ("BUY", "SELL"):
            errors.append("side must be BUY or SELL")
        return errors


class OrdersApi:
    def __init__(self, session) -> None:
        self.session = session

    def create(self, order: dict):
        return self.session.request("POST", "/orders", json=order)


class ReportFormatter:
    def format(self, order: dict, response: dict) -> str:
        return f"{order['side']} {order['qty']} {order['symbol']}: {response['status']}"


class OrderService:
    def __init__(self, validator: OrderValidator, api: OrdersApi, formatter: ReportFormatter) -> None:
        self.validator = validator
        self.api = api
        self.formatter = formatter

    def place(self, order: dict) -> str:
        errors = self.validator.validate(order)
        if errors:
            raise ValueError("; ".join(errors))
        response = self.api.create(order)
        return self.formatter.format(order, response)
