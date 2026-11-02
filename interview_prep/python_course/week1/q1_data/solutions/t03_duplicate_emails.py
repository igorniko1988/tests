from collections import Counter


def duplicate_emails(users: list[dict]) -> list[str]:
    counts = Counter(user["email"].strip().lower() for user in users)
    return [email for email, count in counts.items() if count > 1]
