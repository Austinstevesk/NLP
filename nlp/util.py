#Steal flatten function from nltk or better yet from clojure. While at it check out frequencies from clojure for parallization
#It really is ok, picasso says so; "good artists copy, great programmers steal"
from nltk.util import flatten
from collections import defaultdict


def frequencies(*seq):
    seq = flatten(seq)
    freq = defaultdict(lambda: 0)
    for i in seq:
        freq[i] += 1
    return freq

def first(x): return x[0]

def rest(x): return x[1:]

def last(x): return x[-1]


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
        m1 = {}
    
    for m2 in rest(maps):
        for e in m2.iteritems():
            k = first(e)
            v = last(e)
            if m1.has_key(k):
                m1[k] = f(m1[k], v)
            else:
                m1[k] = f(0, v)    
    return m1
    
    

        
