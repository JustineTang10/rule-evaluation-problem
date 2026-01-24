import time, re
from brute_force import Solver
from greedy import Greedy
from ilp import ILP

def get_data(filename, l=True):
    counter = 0
    data = [[0, 0, 0, 0, 0, 0], # values
            [0, 0, 0, 0, 0, 0, 0]] # times
    if not l:
        counter = 1
        data = [[0, 0, 0, 0], # values
                [0, 0, 0, 0, 0]] # times

    input_file = open(filename, 'r').read()
    split_file = input_file.split()
    r = int(split_file[0]) # number of rules
    m = int(split_file[1]) # number of keywords
    p = [float(split_file[i]) for i in range(2, 2+m)] # probabilities
    input_file = input_file.splitlines()[2:]

    hash_map = dict()
    d = []
    rule_list = []

    cur_time = time.time()

    for i in range(r):
        cur_rule = []
        x = re.findall(r"\(([0-9\s]+)\)", input_file[i])
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

    pro_time = time.time() - cur_time

    a = [[0]*(m + len(d)) for i in range(r)]
    for i in range(r):
        for j in rule_list[i]:
            a[i][j] = 1
        
    bf_solver = Solver(r, m + len(d), a)
    ilp_solver = ILP(r, m + len(d), a)
    gr_solver = Greedy(r, m + len(d), a)

    if l:
        cur_time = time.time()
        data[0][0] = sum(bf_solver.solve())
        data[1][0] = pro_time + time.time() - cur_time

    cur_time = time.time()
    data[0][1 - counter] = sum(ilp_solver.solve())
    data[1][1 - counter] = pro_time + time.time() - cur_time

    cur_time = time.time()
    data[0][2 - counter] = sum(gr_solver.solve())
    data[1][2 - counter] = pro_time + time.time() - cur_time

    cur_time = time.time()
    
    dset = []
    rset = []
    for i in d:
        dset.append(set(i))
    for i in rule_list:
        rset.append(set(i))

    is_in = [set() for i in range(len(d))]
    for i in range(len(d)):
        for j in range(len(d)):
            if len(d[i]) >= len(d[j]):
                continue
            in_dis = True
            for k in d[i]:
                if j not in hash_map[k]:
                    in_dis = False
                    break
            if in_dis:
                is_in[j].add(i)
    
    mid_time = time.time()

    for rule in range(len(rule_list)):
        cur_rule = rule_list[rule]
        for i in range(len(d)):
            if i + m in rset[rule]:
                continue
            dis = d[i]
            implied = False
            for j in cur_rule:
                if j >= m:
                    if j - m in is_in[i]:
                        implied = True
                        break
                elif j in dset[i]:
                    implied = True
                    break
            
            if implied:
                rule_list[rule].append(i + m)

    dis_time = time.time() - cur_time
    print(pro_time)
    print(mid_time - cur_time)
    print(time.time() - mid_time)

    a = [[0]*(m + len(d)) for i in range(r)]
    for i in range(r):
        for j in rule_list[i]:
            a[i][j] = 1
        
    bf_solver = Solver(r, m + len(d), a)
    ilp_solver = ILP(r, m + len(d), a)
    gr_solver = Greedy(r, m + len(d), a)

    if l:
        cur_time = time.time()
        data[0][3] = sum(bf_solver.solve())
        data[1][3] = pro_time + dis_time + time.time() - cur_time

    cur_time = time.time()
    data[0][4 - 2 * counter] = sum(ilp_solver.solve())
    data[1][4 - 2 * counter] = pro_time + dis_time + time.time() - cur_time

    cur_time = time.time()
    data[0][5 - 2 * counter] = sum(gr_solver.solve())
    data[1][5 - 2 * counter] = pro_time + dis_time + time.time() - cur_time

    data[1][6 - 2 * counter] = dis_time

    print(len(d))
    return data