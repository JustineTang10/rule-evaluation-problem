import os
os.system('pip install pulp')

from pulp import *

"""input_file = open('rule_eval_input.txt', 'r').read()
split_file = input_file.split()
r = int(split_file[0])
m = int(split_file[1])
p = [int(split_file[i]) for i in range(2, 2+m)]
input_file = input_file.splitlines()[2:]

a = [[0]*m for i in range(r)]
for i in range(r):
    cur_line = input_file[i].split()
    for j in cur_line:
        a[i][int(j) - 1] = 1"""

class ILP:
    def __init__(self, r, m, a):
        self.r = r
        self.m = m
        self.p = [1] * self.m
        self.a = a

        self.f = 0
        for i in range(self.m):
            cur_f = 0
            for j in range(self.r):
                cur_f += self.a[j][i]
            self.f = max(self.f, cur_f)
    
    def solve(self):
        prob = LpProblem("rule_evaluation_problem", LpMinimize)
        x_names = list(range(self.m))
        x = LpVariable.dicts('x', x_names, lowBound=0, upBound=1)
        prob += (
            lpSum([self.p[i] * x[i] for i in x_names]),
            'Sum of probabilities of roots',
        )
        for i in range(self.r):
            prob += (
                lpSum([self.a[i][j] * x[j] for j in x_names]) >= 1,
                f'ConstraintForRule{i}',
            )
            
        prob.writeLP('RuleEval.lp')
        prob.solve()
        
        ans = []
        for v in prob.variables():
            if v.varValue >= 1 / self.f:
                ans.append(1)
            else:
                ans.append(0)
        
        for i in range(self.r):
            is_covered = False
            for j in range(self.m):
                if self.a[i][j] * ans[j] == 1:
                    is_covered = True
            if not is_covered:
                min_p = 1
                min_k = -1
                for j in range(self.m):
                    if self.a[i][j] and self.p[j] <= min_p:
                        min_p = self.p[j]
                        min_k = j
                ans[min_k] = 1
        
        return ans

"""solver = ILP(r, m, p, a)
print(' '.join([str(i) for i in solver.solve()]))"""