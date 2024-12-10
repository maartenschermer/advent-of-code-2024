from dataclasses import dataclass
from utils.read import read_data

# https://adventofcode.com/2024/day/9

data = read_data(9)

# data = """
# 2333133121414131402
# """
# s1 = 1928
# s2 = 2858

mem = list(map(int,list(data.strip())))

EMPTY = '.'
TMP = '!'

# part 1

def diskimage(disk):
    return ''.join(map(str,disk))

# mem to disk
disk = []
f_id = 0
for i in range(len(mem)):
    if i % 2 ==0:
        disk.extend([f_id]*mem[i])
        f_id += 1
    else:
        disk.extend([EMPTY]*mem[i])

# second disk image with same character for all file blocks (to avoid regexing the right-most digit)
b_disk = [x if x==EMPTY else TMP for x in disk]

# rearrange
while True:
    first_space = disk.index(EMPTY)
    last_block = diskimage(b_disk).rindex(TMP)
    if first_space>last_block:
        break
    disk[first_space], disk[last_block] = disk[last_block], EMPTY
    b_disk[first_space], b_disk[last_block] = TMP, EMPTY

# checksum
s1 = sum([key * val for key, val in enumerate(disk) if val != EMPTY])

print(s1)


# part 2

@dataclass
class File:
    f_id: int
    size: int

@dataclass
class FreeSpace:
    x_id: int
    size: int

# mem to disk
disk = []
f_id = 0
x_id = 0
for i in range(len(mem)):
    if i % 2 ==0:
        disk.append(File(f_id=f_id, size=mem[i]))
        f_id += 1
    else:
        disk.append(FreeSpace(x_id=x_id, size=mem[i]))
        x_id += 1

assert len(disk)==len(mem)

def diskimage(disk):
    s = ""
    for item in disk:
        if isinstance(item,File):
            # s += f"({str(item.f_id) * item.size})"
            s += str(item.f_id) * item.size
        else:
            s += EMPTY * item.size
    return s

# go through all file id's once, big to small
for i in range(f_id-1, -1, -1):

    # get File object for current id
    current_file = next((x for x in disk if isinstance(x, File) and x.f_id == i), None)
    # get first FreeSpace object that's big enough to fit the current file
    first_empty = next((x for x in disk if isinstance(x, FreeSpace) and x.size >= current_file.size), None)

    # there's no big enough space left: leave current file where it is
    if not first_empty:
        continue

    # get indexes of both file and free space
    i_current = disk.index(current_file)
    i_empty = disk.index(first_empty)

    # files should only be moved to the beginning of the disk
    if i_empty>i_current:
        continue

    # swao free space and file
    disk[i_current], disk[i_empty] = disk[i_empty], disk[i_current]

    # free space might be bigger than the file: get difference
    diff = first_empty.size - current_file.size
    if diff>0:
        # reset the size of the moved FreeSpace to the size of the File that was there 
        disk[i_current].size = current_file.size
        # insert a new FreeSpace with the size of the difference, right after the moved File
        disk.insert(i_empty+1, FreeSpace(x_id=x_id, size=diff))
        x_id += 1


s2 = 0
index = 0
# loop over the objects in the disk, keep an index for the disk's actual blocks 
for val in disk:
    if isinstance(val, File):
        for i in range(val.size):
            # ...and calc the checksum
            s2 += (index * val.f_id)
            index += 1
    else:
        index += val.size

print(s2)
