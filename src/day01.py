from utils.read import read_data

# https://adventofcode.com/2024/day/1

data = read_data(1)

# data = """
# 3   4
# 4   3
# 2   5
# 1   3
# 3   9
# 3   3
# """
# s1 = 11
# s2 = 31

# turn data into two lists, one for each column
a, b = list(zip(*[tuple(map(int, x.split())) for x in data.splitlines() if len(x.strip())>0]))

# part 1
# sum the abs difference of elements in the same position of the sorted lists 
s1 = sum([abs(xa-xb) for xa, xb in zip(sorted(list(a)), sorted(list(b)))])

print(s1)

# part 2
# sum the product of each number in list a and its occurrence in list b
s2 = sum([x*b.count(x) for x in a])

print(s2)
