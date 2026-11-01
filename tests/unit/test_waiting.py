import pytest

from framework.utils.waiting import wait_until


def test_condition_true_on_third_attempt():
    answers = iter([False, False, True])
    wait_until(lambda: next(answers), timeout=2, interval=0.01)


def test_condition_never_true():
    with pytest.raises(AssertionError, match='order not filled'):
        wait_until(lambda: False, timeout=0.1, interval=0.01, message='order not filled')


def test_ignored_exception_means_not_yet():
    answers = iter([KeyError, KeyError, True])

    def condition():
        answer = next(answers)
        if answer is KeyError:
            raise KeyError('not created yet')
        return answer

    wait_until(condition, timeout=2, interval=0.01, ignore=(KeyError,))


def test_not_ignored_exception_raises_immediately():
    def condition():
        raise KeyError('bug in condition')

    with pytest.raises(KeyError):
        wait_until(condition, timeout=2, interval=0.01)
