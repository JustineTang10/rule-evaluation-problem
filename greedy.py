class Greedy:
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
        uncovered = 2 ** self.r - 1
        cover = [0 for i in range(self.m)]

        while uncovered != 0:
            max_uncovered = 0
            key_uncovered = -1
            for i in range(self.m):
                if cover[i] == 1:
                    continue
                cur_uncovered = bin(self.bits[i] & uncovered).count("1")
                if cur_uncovered >= max_uncovered:
                    max_uncovered = cur_uncovered
                    key_uncovered = i
            
            cover[key_uncovered] = 1
            uncovered -= self.bits[key_uncovered] & uncovered
        
        return cover