from itertools import product

class Solver:
    def __init__(self, r, m, a):
        self.r = r
        self.m = m
        self.a = a
        
        self.bits = [0 for i in range(self.m)]
        for i in range(self.m):
            for j in range(self.r):
                if self.a[j][i] == 1:
                    self.bits[i] += 2 ** j
    
    def solve(self):
        ans = self.m
        cover = [1 for i in range(self.m)]
        
        for i in product(range(2), repeat=self.m):
            cur_ans = sum(i)
            covered = 0
            for j in range(self.m):
                if i[j] == 1:
                    covered |= self.bits[j]
            if covered == 2 ** self.r - 1 and ans > cur_ans:
                ans = cur_ans
                cover = i
        
        return cover