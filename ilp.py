import highspy
import numpy as np

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
        h = highspy.Highs()
        h.setOptionValue("output_flag", False)

        for i in range(self.m):
            h.addVariable(0, 1)
            h.changeColCost(i, 1)

        inf = highspy.kHighsInf
        for i in range(self.r):
            nz_indices = []
            nz_values = []
            for j in range(self.m):
                if self.a[i][j] != 0:
                    nz_indices.append(j)
                    nz_values.append(1)
            num_nz = sum(self.a[i])
            h.addRow(1, inf, num_nz, np.array(nz_indices), np.array(nz_values))
        
        h.run()
        solution = h.getSolution()

        ans = []
        for v in solution.col_value:
            if v >= 1 / self.f:
                ans.append(1)
            else:
                ans.append(0)
        
        return ans
