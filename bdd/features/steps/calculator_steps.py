from behave import given, then, when


class Calculator:
    def __init__(self):
        self.result = 0

    def add(self, a, b):
        self.result = a + b
        return self.result

    def subtract(self, a, b):
        self.result = a - b
        return self.result


# --- Given ---


@given("The calculator is on")
def step_calculator_on(context):
    context.calculator = Calculator()


# --- When ---


@when("I add {a:d} and {b:d}")
def step_add(context, a, b):
    context.calculator.add(a, b)


@when("I subtract {b:d} from {a:d}")
def step_subtract(context, a, b):
    context.calculator.subtract(a, b)


@when("I sum the numbers")
def step_sum_numbers(context):
    numbers = [int(row["number"]) for row in context.table]
    context.calculator.result = sum(numbers)


@when("I run the operations")
def step_run_operations(context):
    context.results = []
    for row in context.table:
        method = getattr(context.calculator, row["operation"])
        context.results.append(method(int(row["a"]), int(row["b"])))


@when("I evaluate the expression")
def step_evaluate(context):
    parts = context.text.split("+")
    context.calculator.result = sum(int(part) for part in parts)


# --- Then ---


@then("The result is {expected:d}")
def step_check_result(context, expected):
    actual = context.calculator.result
    assert actual == expected, f"got {actual}, expected {expected}"


@then("The result is positive")
def step_result_positive(context):
    actual = context.calculator.result
    assert actual > 0, f"got {actual}"


@then("The result is not {unexpected:d}")
def step_result_not(context, unexpected):
    actual = context.calculator.result
    assert actual != unexpected, f"got {actual}, must not be {unexpected}"


@then("The results are {first:d} and {second:d}")
def step_check_results(context, first, second):
    assert context.results == [first, second], f"got {context.results}"
