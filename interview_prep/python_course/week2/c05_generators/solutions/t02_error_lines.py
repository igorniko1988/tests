def error_lines(path):
    with open(path, encoding="utf-8") as file:
        for number, line in enumerate(file, start=1):
            if "ERROR" in line:
                yield number, line.rstrip("\n")
