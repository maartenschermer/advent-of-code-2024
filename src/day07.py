from utils.read import read_data

# https://adventofcode.com/2024/day/7

data = read_data(7)

# data = """
# 3267: 81 40 27
# 190: 10 19
# 83: 17 5
# 156: 15 6
# 7290: 6 8 6 15
# 161011: 16 10 13
# 192: 17 8 14
# 21037: 9 7 18 13
# 292: 11 6 16 20
# """
# s1 = 3749
# s2 = 11387

equations = {}

lines = data.strip().splitlines()

for item in [x.split() for x in lines]:
    equations[int(item[0].replace(':',''))] = list(map(int,item[1:]))

assert len(equations)==len(lines)

outcomes = []

def f_sum(out, nums, concat=False):
    out = out + nums[0]
    if len(nums)>1:
        f_sum(out, nums[1:], concat=concat)
        f_mul(out, nums[1:], concat=concat)
        if concat:
            f_con(out, nums[1:])
    else:
        outcomes.append(out)

def f_mul(out, nums, concat=False):
    out = out * nums[0]
    if len(nums)>1:
        f_sum(out, nums[1:], concat=concat)
        f_mul(out, nums[1:], concat=concat)
        if concat:
            f_con(out, nums[1:])
    else:
        outcomes.append(out)

def f_con(out, nums):
    out = int(f"{out}{nums[0]}")
    if len(nums)>1:
        f_sum(out, nums[1:], concat=True)
        f_mul(out, nums[1:], concat=True)
        f_con(out, nums[1:])
    else:
        outcomes.append(out)

# part 1

s1 = 0

no_solution = []

for solution, nums in equations.items():
    outcomes = []
    f_sum(nums[0], nums[1:])
    f_mul(nums[0], nums[1:])
    if solution in outcomes:
        s1 += solution 
    else:
        no_solution.append(solution)

print(s1)

# part 2

s2 = 0

for solution in no_solution:
    outcomes = []
    nums = equations[solution]
    f_sum(out=nums[0], nums=nums[1:], concat=True)
    f_mul(out=nums[0], nums=nums[1:], concat=True)
    f_con(out=nums[0], nums=nums[1:])
    s2 += solution if solution in outcomes else 0
        
# print(s2)
print(s1+s2)
