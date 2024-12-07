import threading
from utils.read import read_data
from concurrent import futures

# https://adventofcode.com/2024/day/6

data = read_data(6)

# data = """
# ....#.....
# .........#
# ..........
# ..#.......
# .......#..
# ..........
# .#..^.....
# ........#.
# #.........
# ......#...
# """
# s1 = 41
# s2 = 6


init_floorplan = data.strip().splitlines()

OBJ = '#'
FLOOR = '.'
EXIT = '!'
GUARD = {'^': {'y':-1, 'x': 0, 'next':'>'},
         '>': {'y': 0, 'x': 1, 'next':'v'},
         'v': {'y': 1, 'x': 0, 'next':'<'},
         '<': {'y': 0, 'x':-1, 'next':'^'}}

cols = len(init_floorplan[0])
rows = len(init_floorplan)

def identify_pos(x,y,floorplan):
    if y<0 or y>(rows-1) or x<0 or x>(cols-1):
        return EXIT
    c = floorplan[y][x]
    if c==OBJ:
        return OBJ
    if c==FLOOR:
        return FLOOR
    return GUARD[c]

# get start pos
start_pos = None
for x in range(cols):    
    for y in range(rows):
        p = identify_pos(x,y,init_floorplan)
        if p not in [OBJ, FLOOR]:
            start_pos = x,y,p

def tiles_covered(floorplan):
    pos = start_pos
    visited = [(pos[0], pos[1])]
    prev_positions = set()
    while True:

        x, y, mod = pos

        # pos is a dict, no be hashable, so:
        uniq = f"{x},{y},{mod['next']}"

        if uniq not in prev_positions:
            prev_positions.add(uniq)
        else:
            # if we're in the same spot with the same direction, we're looping
            return None

        neighbour = identify_pos(x+mod['x'],y+mod['y'],floorplan)
        if neighbour not in [OBJ, EXIT]:
            visited.append((x,y))
            pos = x+mod['x'], y+mod['y'], mod
        elif neighbour==EXIT:
            break
        else:
            pos = x, y, GUARD[mod['next']]

        # safeguard: if we've seen more tiles than the floor is big,
        # we've surely seen it all (shouldn't happen though)
        if len(visited)>(len(floorplan) * len(floorplan[0])):
            return None

    # +1 for the last tile before the exit
    return len(set(visited))+1

# part 1

s1 = tiles_covered(floorplan=init_floorplan)

print(s1)

# part 2

def new_floorplan(mod_x, mod_y):
    # create new floorplan with one extra object
    a = []
    for y in range(cols):    
        b = []
        for x in range(rows):
            if (x,y)==(mod_x,mod_y) and init_floorplan[y][x]==FLOOR:
                b.append(OBJ)
            else:
                b.append(init_floorplan[y][x])
        a.append(b)
    return a

def count_loopers(arg):
    x,y = arg
    loopers = 0
    floorplan = new_floorplan(x,y)
    if floorplan!=init_floorplan:
        loopers += 1 if not tiles_covered(floorplan=floorplan) else 0
    return loopers

# calculation is pretty slow, so we're going to parallelize

# define tasks (one task = one new blocked point)
tasks = []
for y in range(cols):    
    for x in range(rows):
        tasks.append((x,y))

# send them off in parallel processes
ex = futures.ProcessPoolExecutor(max_workers=16)
# sum the results of all parallel processes
s2 = sum(list(ex.map(count_loopers, tasks)))

print(s2)
