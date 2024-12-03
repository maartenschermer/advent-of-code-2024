from utils.read import read_data

# https://adventofcode.com/2024/day/1

data = read_data(1)

# turn data into two lists, one for each column
a, b = list(zip(*[tuple(map(int, x.split())) for x in data.splitlines() if len(x.strip())>0]))

# part 1
# sum the abs difference of elements in the same position of the sorted lists 
print(sum([abs(xa-xb) for xa, xb in zip(sorted(list(a)), sorted(list(b)))]))

# part 2
# sum the product of each number in list a and its occurrence in list b
s = sum([x*b.count(x) for x in a])
print(s)
