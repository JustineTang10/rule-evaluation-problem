import time, re
from instance import create_instance
from get_data import get_data

num_trials = 40

# Changing the number of keywords
times = open('data/mtimes.csv', 'w')
values = open('data/mvalues.csv', 'w')

num_cases = 10
r = 10
data = [[[0] * 6 for j in range(num_cases)],
        [[0] * 7 for j in range(num_cases)]]

for trial in range(num_trials):
    for case in range(num_cases):
        create_instance(f'testcases/test{case:02}.txt',
                        r,
                        case + 1,
                        [1 for i in range(case + 1)])

    for case in range(num_cases):
        cur_data = get_data(f'testcases/test{case:02}.txt')
        for i in range(2):
            for j in range(len(cur_data[i])):
                data[i][case][j] += cur_data[i][j]

values.write('\n'.join([','.join(map(lambda x: str(x / num_trials), i)) for i in data[0]]))
times.write('\n'.join([','.join(map(lambda x: str(x / num_trials), i)) for i in data[1]]))
values.close()
times.close()

"""# Changing the number of rules
times = open('data/rtimes.csv', 'w')
values = open('data/rvalues.csv', 'w')

num_cases = 10
m = 10
data = [[[0] * 6 for j in range(num_cases)],
        [[0] * 7 for j in range(num_cases)]]

for trial in range(num_trials):
    for case in range(num_cases):
        create_instance(f'testcases/test{case:02}.txt',
                        case + 1,
                        m,
                        [1 for i in range(m)])

    for case in range(num_cases):
        cur_data = get_data(f'testcases/test{case:02}.txt')
        for i in range(2):
            for j in range(len(cur_data[i])):
                data[i][case][j] += cur_data[i][j]

values.write('\n'.join([','.join(map(lambda x: str(x / num_trials), i)) for i in data[0]]))
times.write('\n'.join([','.join(map(lambda x: str(x / num_trials), i)) for i in data[1]]))
values.close()
times.close()"""

"""# Changing the maximum number of keywords in a rule
times = open('data/ktimes.csv', 'w')
values = open('data/kvalues.csv', 'w')

r = 10
m = 10
num_cases = m
data = [[[0] * 6 for j in range(num_cases)],
        [[0] * 7 for j in range(num_cases)]]

for trial in range(num_trials):
    for case in range(num_cases):
        create_instance(f'testcases/test{case:02}.txt',
                        r,
                        m,
                        [1 for i in range(m)],
                        max_keywords = case + 1)

    for case in range(num_cases):
        cur_data = get_data(f'testcases/test{case:02}.txt')
        for i in range(2):
            for j in range(len(cur_data[i])):
                data[i][case][j] += cur_data[i][j]

values.write('\n'.join([','.join(map(lambda x: str(x / num_trials), i)) for i in data[0]]))
times.write('\n'.join([','.join(map(lambda x: str(x / num_trials), i)) for i in data[1]]))
values.close()
times.close()"""