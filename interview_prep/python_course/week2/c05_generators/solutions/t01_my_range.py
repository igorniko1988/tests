def my_range(start, stop, step=1):
    if step == 0:
        raise ValueError("step must not be zero")

    def generate():
        current = start
        while (current < stop) if step > 0 else (current > stop):
            yield current
            current += step

    return generate()
