from decimal import Decimal


def format_report(rows: list[tuple[str, str]]) -> str:
    amounts = [f"{Decimal(amount):,.2f}" for _, amount in rows]
    total = f"{sum((Decimal(a) for _, a in rows), Decimal('0')):,.2f}"
    w1 = max([len("Name"), len("Total"), *(len(name) for name, _ in rows)])
    w2 = max([len("Amount"), len(total), *(len(a) for a in amounts)])
    line = "-" * (w1 + 2 + w2)

    lines = [f"{'Name':<{w1}}  {'Amount':>{w2}}", line]
    lines += [f"{name:<{w1}}  {amount:>{w2}}" for (name, _), amount in zip(rows, amounts)]
    lines += [line, f"{'Total':<{w1}}  {total:>{w2}}"]
    return "\n".join(lines)
