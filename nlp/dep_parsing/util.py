from nltk.util import flatten
from collections import defaultdict
from nltk.parse.dependencygraph import DependencyGraph

def frequencies(*seq):
    seq = flatten(seq)
    freq = defaultdict(lambda: 0)
    for i in seq:
        freq[i] += 1
    return freq

def first(x): return x[0] if x else []

def rest(x): return x[1:]

def last(x): return x[-1]

merge_without_mutation = lambda f, *maps: merge_with(f, {}, *maps)


def merge_with(f, *maps):
    """
    Merge maps where the rest of the maps are merged with the first map.
    If a key in rest exists in first then the function is applied to the value of first and rest, the result updated in first.
    If a key in rest does not exist in first the function is applied to rest and result updated in first.
    
    The new values are being updated in first, hence mutation is present.
    While this is disturbing, the reason is that first, in this use case, will be huge and rest will be small so copying first
    only to reassign it in the calling method will be too expensive.

    Example
    
    merge_with(subtract, {"a":10}, {"a":2, "b":10})
    
    updates {"a":10} to {"a":8, "b":-10}   
    
    """

    if first(maps):
        m1 = first(maps)
    else:
        m1 = maps[1].copy()
        maps = rest(maps)
    if isinstance(m1.values()[0], (int, float)):
        base = 0
    elif isinstance(m1.values()[0], (list)): 
        base = []
        
    for m2 in rest(maps):
        for e in m2.iteritems():
            k = first(e)
            v = last(e)
            if m1.has_key(k):
                m1[k] = f(m1[k], v)
            else:
                m1[k] = f(base, v)    
    return m1
    
    

def next_s(sent):
    def next_value(h):
        if h+1 < len(sent):
            return sent[h+1]
        else:
            return "*STOP*"
    return next_value

def prev_s(sent):
    def prev_value(h):
        if h-1 > -1:
            return sent[h-1]
        else:
            return "*START*"
    return prev_value
    
def in_between(sent):
    n = len(sent)
    PI = defaultdict(lambda : set())
    
    for t in range(2, n):
        for j in range(n):
            s = t + j
            if s < n:
                PI[(j,s)] = PI[(j, s-1)].copy()
                PI[(j,s)].add(sent[s-1])
    
    def get_b_pos(h,m):
        h,m = sorted([h,m])
        return list(PI[(h,m)])
    
    return get_b_pos

def cons(x, y): return x + y

def make_dep_tree(sent, deps):
    adj = merge_with(cons, [], *[{x:[m]} for x,m,_ in deps])
    heads = dict([(m,h) for h,m,_ in deps])
    rel = dict([(m,rel) for _,m,rel in deps])
    n = len(sent["x"])
    pos = sent["pos"]
    x = sent["x"]
    nodelist = defaultdict(lambda: {"address": -1, "head": -1, "deps": [], "rel": "", "tag": "", "word": None})
    
    for i in range(1, n):
        node = nodelist[i]
        node["address"] = i
        node["head"] = heads[i]
        node["deps"] = adj[i] if adj.has_key(i) else []
        node["tag"] = pos[i]
        node["word"] = x[i]
        node["rel"] = rel[i]
    
    g = DependencyGraph()
    g.get_by_address(0)["deps"] = adj[0] if adj.has_key(0) else []
    [g.add_node(node) for node in nodelist.values()]
    g.root = nodelist[adj[0][0]]
    
    return g

    

    

    
