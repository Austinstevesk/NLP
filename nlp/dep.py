from collections import defaultdict

def jason(sent):
    sent = [" ", "root"] + sent.split(" ")
    C = defaultdict(lambda: 0)
    bp = defaultdict(lambda: "")
    n = len(sent)
    model = defaultdict(lambda: 0)
    model[(1,3)] = 60; model[(3,2)] = 20; model[(3,4)] = 20
    S = lambda h,m: model[(h,m)]
    for k in range(1, n):
        for s in range(1, n):
            t = s + k
            if t < n:
               C[(s, t, "<", 0)], bp[(s, t, "<", 0)] = max([(C[(s, r, ">", 1)] + C[(r+1, t, "<", 1)] + S(t,s), r) for r in range(s, t)])
               C[(s, t, ">", 0)], bp[(s, t, ">", 0)] = max([(C[(s, r, ">", 1)] + C[(r+1, t, "<", 1)] + S(s,t), r) for r in range(s,t)])
               
               C[(s, t, "<", 1)], bp[(s, t, "<", 1)] = max([(C[(s, r, "<", 1)] + C[(r, t, "<", 0)], r) for r in range(s,t)])
               C[(s, t, ">", 1)], bp[(s, t, ">", 1)] = max([(C[(s, r, ">", 0)] + C[(r, t, ">", 1)], r) for r in range(s+1, t+1)])
                 
    return  C, bp
        
            
            
    
