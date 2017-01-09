from collections import defaultdict

def first_order(S, n):
    C = defaultdict(lambda: 0)
    bp = defaultdict(lambda: "")
    dep = []
    for k in range(1, n+1):
        for s in range(n+1):
            t = s + k
            if t <= n:
               C[(s, t, "<", 0)], bp[(s, t, "<", 0)] = max([(C[(s, r, ">", 1)] + C[(r+1, t, "<", 1)] + S(t,s), r) for r in range(s, t)])
               C[(s, t, ">", 0)], bp[(s, t, ">", 0)] = max([(C[(s, r, ">", 1)] + C[(r+1, t, "<", 1)] + S(s,t), r) for r in range(s,t)])
               
               C[(s, t, "<", 1)], bp[(s, t, "<", 1)] = max([(C[(s, r, "<", 1)] + C[(r, t, "<", 0)], r) for r in range(s,t)])
               C[(s, t, ">", 1)], bp[(s, t, ">", 1)] = max([(C[(s, r, ">", 0)] + C[(r, t, ">", 1)], r) for r in range(s+1, t+1)])
                 
    def decode(s,t,d,c):
        if (s != t):
            if c == 0:
                if d == "<":
                    dep.append((t,s))
                elif d == ">":
                    dep.append((s,t))
            r = bp[(s, t, d ,c)]
            if c == 0:
                decode(s, r, ">", 1); decode(r+1, t, "<", 1)
            elif c == 1:
                if d == "<":
                    decode(s, r, d, 1); decode(r, t, d, 0)
                elif d == ">":
                    decode(s, r, d, 0); decode(r, t, d, 1)
            
    decode(0, n, ">", 1)
    
    return dep
            
            
        
            
            
    
