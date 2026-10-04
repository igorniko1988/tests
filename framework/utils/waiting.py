import time


def wait_until(check, timeout: float = 10, interval: float = 0.3, message: str = "condition"):
    """Повторяет check() пока он не вернёт что-то истинное или не выйдет время.

    Возвращает результат check(). Если время вышло — падает с понятной ошибкой.
    """
    deadline = time.monotonic() + timeout
    while True:
        result = check()
        if result:
            return result
        if time.monotonic() > deadline:
            raise TimeoutError(f"Не дождались за {timeout} с: {message}")
        time.sleep(interval)
