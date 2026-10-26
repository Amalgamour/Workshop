def count_lines(text):
    return sum(bool(line) for line in text.splitlines())
