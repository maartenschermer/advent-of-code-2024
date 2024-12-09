from dataclasses import dataclass
from utils.read import read_data

# https://adventofcode.com/2024/day/8

data = read_data(8)

# data = """
# ............
# ........0...
# .....0......
# .......0....
# ....0.......
# ......A.....
# ............
# ............
# ........A...
# .........A..
# ............
# ............
# """
# s1 = 14
# s2 = 34

@dataclass
class Antenna:
    x: int
    y: int
    freq: str

plan = data.strip().splitlines()

cols = len(plan[0])
rows = len(plan)

antennas = []

for row in range(rows):
    for col in range(cols):
        if plan[row][col]=='.':
            continue
        antennas.append(Antenna(x=col, y=row, freq=plan[row][col]))

def print_map(antennas, nodes):

    def color(s):
        return '\033[92m' + s + '\033[0m'

    for row in range(rows):
        for col in range(cols):
            z = '.'
            ants = [x for x in antennas if x.x==col and x.y==row]
            if len(ants)==1:
                z = ants[0].freq
            ns = [x for x in nodes if x[0]==col and x[1]==row]
            if len(ns)==1:
                z = '#' if z=='.' else color('#')

            print(z,end='')
        print()

def generate_antinodes(repeat=False):
    antinodes = []
    lonely_antennas = []
    for ant in antennas:
        p_antennas = [x for x in antennas if x.freq==ant.freq and (x.x != ant.x and x.y != ant.y)]
        if len(p_antennas)==0:
            lonely_antennas.append(ant) 
        for p_ant in p_antennas:
            d_x, d_y = abs(ant.x-p_ant.x), abs(ant.y-p_ant.y)
            a_x = ant.x
            a_y = ant.y
            for i in range(rows if repeat else 1):
                if ant.x>p_ant.x:
                    a_x = a_x + d_x
                elif ant.x<p_ant.x:
                    a_x = a_x - d_x

                if ant.y>p_ant.y:
                    a_y = a_y + d_y
                elif ant.y<p_ant.y:
                    a_y = a_y - d_y

                if a_y>=cols or a_x>=rows:
                    break

                antinodes.append((a_x, a_y))

    return set([x for x in antinodes if x[0]>=0 and x[1]>=0 and x[0]<cols and x[1]<rows]), lonely_antennas

# part 1

nodes, _ = generate_antinodes()
s1 = len(nodes)

print(s1)

# part 2

nodes, lonely_antennas = generate_antinodes(repeat=True)
# also count the antennas, as they will be overlapped by their own antinodes
# unless they're the only one of their frequency (which never seems to happen)
s2 = len(set(list(nodes)+[(x.x, x.y) for x in antennas if x not in lonely_antennas]))

print(s2)

# print_map(antennas, nodes)
