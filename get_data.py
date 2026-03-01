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
                [0, 0, 0, 0, 0, 0, 0, 0, 0]] # times

    input_file = open(filename, 'r').read()
    split_file = input_file.split()
    r = int(split_file[0]) # number of rules
    m = int(split_file[1]) # number of keywords
    p = [float(split_file[i]) for i in range(2, 2+m)] # probabilities; now unused
    input_file = input_file.splitlines()[2:]

    hash_map = dict()
    d = []
    d_map = {}
    rule_list = []

    cur_time = time.time()

    for i in range(r):
        cur_rule = []
        x = re.findall(r"\(([0-9\s]+)\)", input_file[i])
        for j in x:
            cur_d = sorted([int(k) - 1 for k in j.split()])
            cur_d_tuple = tuple(cur_d)

            if cur_d_tuple not in d_map:
                cur_ind = len(d)
                d_map[cur_d_tuple] = cur_ind
                for k in cur_d:
                    if k not in hash_map: hash_map[k] = set()
                    hash_map[k].add(len(d))
                d.append(cur_d)
            else:
                cur_ind = d_map[cur_d_tuple]
            
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

    a = [[0]*(m + len(d)) for i in range(r)]
    for i in range(r):
        for j in rule_list[i]:
            a[i][j] = 1

    pro_time = time.time() - cur_time
    
    if l:
        bf_solver = Solver(r, m + len(d), a)
    ilp_solver = ILP(r, m + len(d), a)
    gr_solver = Greedy(r, m + len(d), a)

    if l:
        cur_time = time.time()
        data[0][0] = sum(bf_solver.solve()) # Brute force
        data[1][0] = pro_time + time.time() - cur_time

    cur_time = time.time()
    data[0][1 - counter] = sum(ilp_solver.solve()) # LP
    data[1][1 - counter] = pro_time + time.time() - cur_time

    cur_time = time.time()
    data[0][2 - counter] = sum(gr_solver.solve()) # Greedy
    data[1][2 - counter] = pro_time + time.time() - cur_time

    cur_time = time.time()
    
    dset = []
    rset = []
    for cur_dis in d:
        dset.append(set(cur_dis))
    for i in rule_list:
        rset.append(set(i))

    is_in = [set() for _ in range(len(d))]
    is_out = [set() for _ in range(len(d))]

    # Optimize is_in/is_out calculation using keyword indexing
    for i in range(len(d)):
        # Heuristic to reduce checks; ensures potential supersets contain at least one common element
        smallest_keyword_in_i = min(dset[i])

        potential_supersets_indices = set()
        if smallest_keyword_in_i in hash_map:
            for j_idx_from_hashmap in hash_map[smallest_keyword_in_i]:
                if j_idx_from_hashmap != i and len(dset[i]) < len(dset[j_idx_from_hashmap]):
                    potential_supersets_indices.add(j_idx_from_hashmap)
        
        # For each potential superset j, perform the actual subset check
        for j in potential_supersets_indices:
            if dset[i].issubset(dset[j]):
                is_in[j].add(i)
                is_out[i].add(j)
    
    check_ds = []
    for i in range(len(d)):
        if len(is_out[i]) == 0:
            check_ds.append(i)

    mid_time = time.time()

    for rule in range(len(rule_list)):
        cur_rule_components = rule_list[rule]

        # Pre-process cur_rule_components into sets once per rule
        K_basic_in_rule = set()
        D_synth_in_rule = set()
        for comp in cur_rule_components:
            if comp < m: # basic keyword
                K_basic_in_rule.add(comp)
            else: # disjunction keyword (index >= m)
                D_synth_in_rule.add(comp - m)

        for i in check_ds:
            if i + m in rset[rule]:
                continue
            
            implied = False
            # Check if any basic keyword in the rule implies dset[i] (i.e., is present in dset[i])
            if not dset[i].isdisjoint(K_basic_in_rule):
                implied = True
            # Check if any synthetic disjunction in the rule implies dset[i] (i.e., is a subset of dset[i])
            elif not is_in[i].isdisjoint(D_synth_in_rule):
                implied = True
            
            if implied:
                rule_list[rule].append(i + m)

    dis_time = time.time() - cur_time

    data[1][6 - 2 * counter] = dis_time # Disjunction
    if not l:
        data[1][7 - 2 * counter] = pro_time # Preprocessing
        data[1][8 - 2 * counter] = mid_time - cur_time # Loop 1 of disjunction algorithm
        data[1][9 - 2 * counter] = time.time() - mid_time # Loop 2 of disjunction algorithm
        data[1][10 - 2 * counter] = len(d) # Number of disjunctions

    a = [[0]*(m + len(d)) for i in range(r)]
    for i in range(r):
        for j in rule_list[i]:
            a[i][j] = 1
    
    if l:
        bf_solver = Solver(r, m + len(d), a)
    ilp_solver = ILP(r, m + len(d), a)
    gr_solver = Greedy(r, m + len(d), a)

    if l:
        cur_time = time.time()
        data[0][3] = sum(bf_solver.solve()) # Brute force (D)
        data[1][3] = pro_time + dis_time + time.time() - cur_time

    cur_time = time.time()
    data[0][4 - 2 * counter] = sum(ilp_solver.solve()) # LP (D)
    data[1][4 - 2 * counter] = pro_time + dis_time + time.time() - cur_time

    cur_time = time.time()
    data[0][5 - 2 * counter] = sum(gr_solver.solve()) # Greedy (D)
    data[1][5 - 2 * counter] = pro_time + dis_time + time.time() - cur_time

    return data
