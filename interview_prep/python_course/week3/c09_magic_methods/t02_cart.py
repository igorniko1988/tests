"""C9 t02 (required, ~20 min). A cart that behaves like a container.

Implement a class Cart:
- add(item, qty=1) - add qty of item (qty must be > 0, else ValueError); adding again sums up;
- remove(item) - remove the item completely; missing item -> KeyError;
- len(cart) - number of DIFFERENT items;
- item in cart - is the item there;
- cart[item] - quantity; missing -> KeyError;
- for item, qty in cart - iterate in the order items were first added;
- bool(cart) - False when empty;
- total_qty property - sum of all quantities.

Example:
    cart = Cart()
    cart.add("apple", 2); cart.add("pear"); cart.add("apple")
    len(cart), cart["apple"], "pear" in cart, cart.total_qty   -> 2, 3, True, 4
    list(cart)   -> [("apple", 3), ("pear", 1)]

Follow-up questions:
- What does Python fall back to for `in` without __contains__?

Run (from interview_prep/python_course/week3/c09_magic_methods): uv run pytest -k t02
Теория: THEORY.md в этой папке, раздел 5.
"""


class Cart:
    def __init__(self) -> None:
        raise NotImplementedError
