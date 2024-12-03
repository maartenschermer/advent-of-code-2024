def read_data(day):
    with open(f'../data/{day:>02}.txt') as f:
        return f.read()
