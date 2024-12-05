from utils.read import read_data

# https://adventofcode.com/2024/day/4

data = read_data(4)

# data = """
# MMMSXXMASM
# MSAMXMSMSA
# AMXSXMAAMM
# MSAMASMSMX
# XMASAMXAMM
# XXAMMXXAMA
# SMSMSASXSS
# SAXAMASAAA
# MAMMMXMMMM
# MXMXAXMASX
# """
# s1 = 18
# s2 = 9

lines = data.strip().splitlines()

cols = len(lines[0])
rows = len(lines)

# part 1

xmas = 'XMAS'

def word_count(line):
    x = 0
    for i in range(len(line)):
        bit = line[i:i+len(xmas)]
        x += 1 if (bit==xmas or bit==xmas[::-1]) else 0
    return x

s1 = 0

for r in range(rows):
    s1 += word_count(lines[r])
 
for c in range(cols):
    s1 += word_count("".join([x[c] for x in lines]))

for r in range(rows):
    for c in range(cols):
        we = ""
        ew = ""
        for i in range(len(xmas)):
            if r+i<rows and c+i<cols:
                we += lines[r+i][c+i]
            if r+i<rows and c-i>=0:
                ew += lines[r+i][c-i]
        s1 += word_count(we)+word_count(ew)

print(s1)

# part 2

s2 = 0
ymas = 'MAS'
i = (len(ymas)-1)//2

for r in range(rows):
    for c in range(cols):
        if r-1>=0 and r+i<rows and c-1>=0 and c+i<cols:
            we = lines[r-i][c-i] + lines[r][c] + lines[r+i][c+i]
            ew = lines[r-i][c+i] + lines[r][c] + lines[r+i][c-i]
            if (we==ymas or we[::-1]==ymas) and (ew==ymas or ew[::-1]==ymas):
                s2 += 1

print(s2)
