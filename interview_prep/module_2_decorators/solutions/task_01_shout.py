def shout(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result.upper()
    return wrapper


@shout
def greet(name):
    return "hello, " + name


EXPECTED_OUTPUT = "HELLO, IGOR"
