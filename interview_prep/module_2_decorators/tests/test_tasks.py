from tasks.task_01_shout import EXPECTED_OUTPUT, greet
from tasks.task_02_add_exclamation import add_exclamation


def test_task_01_predict_output():
    assert EXPECTED_OUTPUT == greet("igor")


def test_task_02_add_exclamation():
    @add_exclamation
    def say(word):
        return word

    assert say("hi") == "hi!"
    assert say("hello") == "hello!"


def test_task_02_passes_arguments_through():
    @add_exclamation
    def join(a, b, sep=" "):
        return a + sep + b

    assert join("a", "b") == "a b!"
    assert join("a", "b", sep="-") == "a-b!"
