from ilp import ILP
from brute_force import Solver
from greedy import Greedy
import re

input_file = open('testcases/test999.txt', 'r').read()
split_file = input_file.split()
r = int(split_file[0]) # number of rules
m = int(split_file[1]) # number of keywords
p = [float(split_file[i]) for i in range(2, 2+m)] # probabilities
input_file = input_file.splitlines()[2:]

hash_map = dict()
d = []
rule_list = []

for i in range(r):
    cur_rule = []
    x = re.findall(r"\((.+)\)", input_file[i])
    for j in x:
        cur_d = sorted([int(k) - 1 for k in j.split()])
        cur_ind = 0
        for k in d:
            if cur_d == k:
                break
            cur_ind += 1
        
        if cur_ind == len(d):
            for k in cur_d:
                if k not in hash_map: hash_map[k] = set()
                hash_map[k].add(len(d))
            cur_rule.append(m + len(d))
            d.append(cur_d)
        else:
            cur_rule.append(m + cur_ind)
    
    is_d = False 
    for j in input_file[i].split():
        if '(' in j:
            is_d = True
        if is_d:
            if ')' in j:
                is_d = False
            continue
        cur_rule.append(int(j) - 1)
    
    rule_list.append(cur_rule)

for rule in range(len(rule_list)):
    cur_rule = rule_list[rule]
    for i in range(len(d)):
        dis = d[i]
        implied = False
        for j in cur_rule:
            if j >= m:
                in_dis = True
                for j in d[j - m]:
                    if i not in hash_map[j]:
                        in_dis = False
                        break
                if in_dis:
                    implied = True
                    break
            elif j in dis:
                implied = True
                break
        
        if implied:
            rule_list[rule].append(i + m)

a = [[0]*(m + len(d)) for i in range(r)]
for i in range(r):
    for j in rule_list[i]:
        a[i][j] = 1

solver = ILP(r, m + len(d), a)
print(' '.join([str(i) for i in solver.solve()]))

"""bf = Solver(r, m + len(d), a)
cover = bf.solve()

for i in range(m + len(d)):
    if cover[i]:
        if i < m:
            print(i)
        else:
            print(' '.join([str(j) for j in d[i - m]]))"""

gsolver = Greedy(r, m + len(d), a)
print(gsolver.solve())