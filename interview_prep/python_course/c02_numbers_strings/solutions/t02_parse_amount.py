import re
from decimal import Decimal

AMOUNT = re.compile(r"-?[0-9]+(\.[0-9]+)?")  # [0-9], а не \d: \d пускает Unicode-цифры


def parse_amount(text) -> Decimal | None:
    if not isinstance(text, str):
        return None
    text = text.strip()
    if not AMOUNT.fullmatch(text):
        return None
    return Decimal(text)


# try: Decimal(text) except InvalidOperation — НЕ достаточно: Decimal("NaN"), Decimal("1e3"),
# Decimal("+5") создаются без ошибки. Формат проверяем явно, потом конвертируем.
