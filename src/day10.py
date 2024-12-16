import threading
from concurrent import futures
from dataclasses import dataclass, field
from utils.read import read_data

# https://adventofcode.com/2024/day/10

data = read_data(10)

# data = """
# 89010123
# 78121874
# 87430965
# 96549874
# 45678903
# 32019012
# 01329801
# 10456732
# """
# s1 = 36
# s2 = 81

# get the map
topo = data.strip().splitlines()

cols = len(topo[0])
rows = len(topo)

for x in range(cols):    
    topo[x] = list(map(int,topo[x]))

# define all a Trail can be
@dataclass
class Trail:
    start: tuple = (-1,-1)
    ends: list[tuple] = field(default_factory=list)
    score: int = 0
    paths: list[list[tuple]] = field(default_factory=list)
    rating: int = 0

trails = []

def val_at(x, y):
    if x<0 or x>=cols or y<0 or y>=rows:
        return
    return topo[x][y]

# finding all trailheads & creating Trail instances for each
for x in range(cols):    
    for y in range(rows):
        if val_at(x,y)==0:
            trails.append(Trail(start=(x,y)))

def follow_trail(trail, pos=None, path=''):
    if not pos:
        pos = trail.start
    z = val_at(*pos)
    for mod in [(0,-1),(1,0),(0,1),(-1,0)]:
        neighbour = tuple(x-y for x,y in zip(pos,mod))
        n = val_at(*neighbour)
        if n and z==8 and n==9:
            # trail ends
            trail.ends.append(neighbour)
            trail.paths.append(path)
            trail.score = len(set(trail.ends))
            trail.rating = len(set(trail.paths))
        if n and n-z==1:
            # take a step
            # list of tuples no be hashable for futures, hence string thingy
            path += f"{neighbour[0]},{neighbour[1]}|"
            # keep walking
            follow_trail(trail, neighbour, path)
    return trail

# print(f"starting {len(trails)} trails")

# parallel walking
ex = futures.ProcessPoolExecutor(max_workers=16)
# collect results
travelled_trails = list(ex.map(follow_trail, trails))

# part 1

s1 = sum([x.score for x in travelled_trails])
print(s1)

# part 2

s2 = sum([x.rating for x in travelled_trails])
print(s2)
