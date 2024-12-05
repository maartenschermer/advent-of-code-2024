from utils.read import read_data

# https://adventofcode.com/2024/day/2

data = read_data(2)

# data = """
# 7 6 4 2 1
# 1 2 7 8 9
# 9 7 6 2 1
# 1 3 2 4 5
# 8 6 4 4 1
# 1 3 6 7 9
# """
# s1 = 2
# s2 = 4

reports = [list(map(int, x.split())) for x in data.splitlines() if len(x.strip())>0]

# func to check if a report is safe
def process_report(report):
    # check that numbers always increase or decrease, and there's no doubles
    if not (report==sorted(report) or report==sorted(report, reverse=True)) or not len(set(report))==len(report):
        return False
    # split list into overlapping chucks of two adjacent numbers for easy cal, check that difference is < 4 (equals have 
    # already been filtered out above)  
    c = 2 # chunk size
    o = 1 # overlap
    if len(report)>len([x for x in [report[i:i+c] for i in range(0, len(report), c-o)][:-1] if abs(x[0]-x[1])<4])+1:
        return False
    return True

# part 1
s1 = 0
unsafe_reports = []
# count safe ones, save unsafe ones
for report in reports:
    if process_report(report):
        s1 += 1
        continue
    unsafe_reports.append(report)

print(s1)


# part 2
also_safe = 0
for f_report in unsafe_reports:
    # try all variants of a unsafe report by dropping one letter, for all letters
    for i in range(0, len(f_report)):
        report = f_report[:i]+f_report[i+1:]
        if not process_report(report):
            continue
        also_safe += 1
        break

s2 = s1 + also_safe
print(s2)
