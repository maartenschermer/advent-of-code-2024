from utils.read import read_data

# https://adventofcode.com/2024/day/3

data = read_data(3)

# data = """
# xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
# """
# s1 = 161
# s2 = 48

# regex is bliss
import re

# part 1

def mul(a,b):
    return a*b

# it's christmas time, when eval is safe
s1 = sum([eval(x) for x in re.findall( r'mul\(\d{1,},\d{1,}\)', data.strip())])

print(s1)


# part 2

def do():
    return True

def dont():
    return False

def mul(a, b, doing):
    return a*b if doing else 0

doing = True
s2 = 0
for match in re.findall( r'mul\(\d{1,},\d{1,}\)|do\(\)|don\'t\(\)', data.strip()):
    r = eval(re.sub(r"([^(]{1})\)", r"\1,doing)", match.replace("'", "")))
    if isinstance(r, bool):
        doing = r
    else:
        s2 += r

print(s2)
