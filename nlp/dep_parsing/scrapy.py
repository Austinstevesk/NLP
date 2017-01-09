from collections import defaultdict

class BPOS:
    def __init__(self, sent):
        self.sent = sent
        self.n = len(self.sent)
        self.PI = defaultdict(lambda : set())
        self.words_inbetween()
    
    def words_inbetween(self):
        for t in range(2, self.n):
            for j in range(self.n):
                s = t + j
                if s < self.n:
                    self.PI[(j,s)] = self.PI[(j, s-1)].copy()
                    self.PI[(j,s)].add(self.sent[s-1])

    def get_b_pos(self, h,m):
        h,m = sorted([h,m])
        return self.PI[(h,m)]
