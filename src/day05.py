from utils.read import read_data

# https://adventofcode.com/2024/day/5

data = read_data(5)

# data = """
# 47|53
# 97|13
# 97|61
# 97|47
# 75|29
# 61|13
# 75|53
# 29|13
# 97|29
# 53|29
# 61|53
# 97|53
# 61|29
# 47|13
# 75|47
# 97|75
# 47|61
# 75|61
# 47|29
# 75|13
# 53|13

# 75,47,61,53,29
# 97,61,53,29,13
# 75,29,13
# 75,97,47,61,53
# 61,13,29
# 97,13,75,29,47
# """
# s1 = 143
# s2 = 123

rules, updates = *[x.split() for x in data.strip().split("\n\n")],
rules = [list(map(int,x.split('|'))) for x in rules]
updates = [list(map(int,x.split(','))) for x in updates]

# part 1

s1 = 0
i_updates = []
for update in updates:
    valid = True
    for rule in [x for x in rules if x[0] in update and x[1] in update]:
        if update.index(rule[0])>update.index(rule[1]):
            valid = False
            break
    if not valid:
        i_updates.append(update)
        continue

    s1 += update[(len(update)//2)]

print(s1)

# part 2

s2 = 0
for update in i_updates:
    while True:
        done = True
        for rule in [x for x in rules if x[0] in update and x[1] in update]:
            a = update.index(rule[0])
            b = update.index(rule[1])
            if a>b:
                # swap positions if wrong order
                update[a], update[b] = update[b], update[a]
                done = False
        if done:
            # repeat until nothing changes anymore
            break

    s2 += update[(len(update)//2)]

print(s2)