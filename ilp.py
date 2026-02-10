from pulp import *

class ILP:
    def __init__(self, r, m, a):
        self.r = r
        self.m = m
        self.a = a

        self.f = 0
        for i in range(self.r):
            cur_f = 0
            for j in range(self.m):
                cur_f += self.a[i][j]
            self.f = max(self.f, cur_f)
    
    def solve(self):
        prob = LpProblem("rule_evaluation_problem", LpMinimize)
        x_names = list(range(self.m))
        x = LpVariable.dicts('x', x_names, lowBound=0, upBound=1)
        prob += (
            lpSum([x[i] for i in x_names]),
            'Number of roots',
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
                min_k = -1
                for j in range(self.m):
                    if self.a[i][j]:
                        min_k = j
                ans[min_k] = 1
        
        return ans
