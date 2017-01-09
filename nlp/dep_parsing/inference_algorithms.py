from Graphs import DirectedGraph
from util import rest, last
import numpy as np
from collections import defaultdict

def MST(model, n, L=False):
    N = range(n)
    words = range(1, n)
    G = DirectedGraph(n)
    if L:
        PI = defaultdict()
        for h in N:
            for m in words:
                PI[(h,m)] = last(max([(model(h,m,l),l) for l in L]))
                
        G.add_edges([(h,m, PI[(h,m)], model(h,m, PI[(h,m)])) for h in N for m in words if h != m])
    else:
        G.add_edges([(h, m, model(h,m)) for h in N for m in words if h != m])
    pruned = G.prune()
    
    cycle_nodes = pruned.has_cycle()
    if cycle_nodes:
        return {"pred":[(x.fro, x.to, x.label if L else None) for x in pruned.edges()], "cycle":cycle_nodes}
    else:
        return {"pred":[(x.fro, x.to, x.label if L else None) for x in pruned.edges()]}

def GreedyJoker(model, n, l=False):
    return {"pred": [rest(max([(model(h,m), h, m) for h in range(n)])) 
                     for m in range(1, n)]}

def IncidenceMatrix(model, n):
    return np.array([[model(h,m) for h in range(n)]
                     for m in range(1, n)])

def FirstOrder(S, n):
    C = defaultdict(lambda: 0)
    bp = defaultdict(lambda: "")
    dep = []
    for k in range(1, n):
        for s in range(n):
            t = s + k
            if t < n:
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

    decode(0, n-1, ">", 1)

    return {"pred":dep}


    
    
