import time, re
from instance import create_instance
from get_data import get_data

num_trials = 20

# Changing the number of keywords
times = open('data/mtimes.csv', 'w')
values = open('data/mvalues.csv', 'w')

num_cases = 100
r = 100
data = [[[0] * 5 for j in range(num_cases)],
        [[0] * 6 for j in range(num_cases)]]

for i in range(num_cases):
    data[0][i][0] = num_trials * (i + 1)
    data[1][i][0] = num_trials * (i + 1)

for trial in range(num_trials):
    for case in range(num_cases):
        create_instance(f'testcases/test{case:02}.txt',
                        r,
                        case + 1,
                        [1 for i in range(case + 1)])

    for case in range(num_cases):
        cur_data = get_data(f'testcases/test{case:02}.txt', l=False)
        for i in range(2):
            for j in range(len(cur_data[i])):
                data[i][case][j + 1] += cur_data[i][j]

values.write('\n'.join([','.join(map(lambda x: str(x / num_trials), i)) for i in data[0]]))
times.write('\n'.join([','.join(map(lambda x: str(x / num_trials), i)) for i in data[1]]))
values.close()
times.close()

# Changing the number of rules
times = open('data/rtimes.csv', 'w')
values = open('data/rvalues.csv', 'w')

num_cases = 100
m = 100
data = [[[0] * 5 for j in range(num_cases)],
        [[0] * 6 for j in range(num_cases)]]

for i in range(num_cases):
    data[0][i][0] = num_trials * (i + 1)
    data[1][i][0] = num_trials * (i + 1)

for trial in range(num_trials):
    for case in range(num_cases):
        create_instance(f'testcases/test{case:02}.txt',
                        case + 1,
                        m,
                        [1 for i in range(m)])

    for case in range(num_cases):
        cur_data = get_data(f'testcases/test{case:02}.txt', l=False)
        for i in range(2):
            for j in range(len(cur_data[i])):
                data[i][case][j + 1] += cur_data[i][j]

values.write('\n'.join([','.join(map(lambda x: str(x / num_trials), i)) for i in data[0]]))
times.write('\n'.join([','.join(map(lambda x: str(x / num_trials), i)) for i in data[1]]))
values.close()
times.close()

# Changing the maximum number of keywords in a rule
times = open('data/ktimes.csv', 'w')
values = open('data/kvalues.csv', 'w')

r = 100
m = 100
num_cases = m
data = [[[0] * 5 for j in range(num_cases)],
        [[0] * 6 for j in range(num_cases)]]

for i in range(num_cases):
    data[0][i][0] = num_trials * (i + 1)
    data[1][i][0] = num_trials * (i + 1)

for trial in range(num_trials):
    for case in range(num_cases):
        create_instance(f'testcases/test{case:02}.txt',
                        r,
                        m,
                        [1 for i in range(m)],
                        max_keywords = case + 1)

    for case in range(num_cases):
        cur_data = get_data(f'testcases/test{case:02}.txt', l=False)
        for i in range(2):
            for j in range(len(cur_data[i])):
                data[i][case][j + 1] += cur_data[i][j]

values.write('\n'.join([','.join(map(lambda x: str(x / num_trials), i)) for i in data[0]]))
times.write('\n'.join([','.join(map(lambda x: str(x / num_trials), i)) for i in data[1]]))
values.close()
times.close()
