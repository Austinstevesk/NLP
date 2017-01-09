from nltk.util import flatten
from collections import *
from itertools import chain
from nltk.corpus.reader.util import LazyConcatenation
from scipy import *
from numpy import *

class Hist():
    def __init__(self, docs):
        self.tuples = flatten([Process(x).hist for x in docs])

class Process():
    def __init__(self, doc):
        self.doc = [x.split(" ") for x in doc]
        self.sent = LazyConcatenation([self._get_sent()])
        self.tags = self._get_tags()
        self.hist = self.package()
        
    def _get_tags(self):
        return [x for _,x in self.doc]

    def _get_sent(self):
        return [x for x,_ in self.doc]

    def tri(self, n = 3):
        seq = list(chain(("*",) * (n - 1), self.tags, ("STOP",)))
        count = max(0, len(seq) - n + 1)
        return [seq[x:x+n] for x in range(count)]

        
    def package(self):
        n = len(self.sent)
        vals = [flatten(x) for x in enumerate(self.tri())]
        return [{"w":self.sent, "i":i, "y2":y2, "y1":y1, "y":y}  for i, y2, y1, y in vals]


class Feats():
    def __init__(self, hist):
        self.hist = hist
        self.i, self.w, self.y, self.y1, self.y2 = hist["i"], hist["w"], hist["y"], hist["y1"], hist["y2"]
        self.sent_len = len(self.w)
        if (self.i < self.sent_len):
            #self.features = [self.unigram_tag(), self.bigram_tags(), self.trigram_tags(), self.word_trigram_tags(), self.word_bigram_tags(), self.bigram_with_tags(), self.trigram_with_tags()]
            self.features = [self.unigram_tag(), self.trigram_tags()]
        else:
            self.features = [self.trigram_tags()]
        
    def _word(self):
        try: 
            return self.w[self.i]
        except:
            return "NULL"

    def _prev_word(self):
        return "NULL" if self.i == 0 else self.w[self.i - 1]

    def _second_prev_word(self):
        return "NULL" if self.i <= 1 else self.w[self.i - 2]

    def unigram_tag(self):
        return "TAG:"+self._word()+":"+ self.y
            
    def bigram_tags(self):
        return "BIGRAM:"+self.y1+":"+self.y
        
    def trigram_tags(self):
        return "TRIGRAM:"+self.y2+":"+self.y1+":"+self.y
                
    def word_trigram_tags(self):
        return self.trigram_tags()+":TAG:"+self._word()

    def word_bigram_tags(self):
        return self.bigram_tags()+":TAG:"+self._word()
        
    def bigram_with_tags(self):
        return "BIGRAM:TAG:"+self._prev_word()+":"+self.y1+":"+self._word()+":"+self.y
        
    def trigram_with_tags(self):
        return "TRIGRAM:TAG:"+self._second_prev_word()+":"+self.y2+":"+self._prev_word()+":"+self.y1+":"+self._word()+":"+self.y

class Dict(dict):
    def inc(self, v):
        if self.has_key(v):
            self[v] += 1 
    def dec(self, v):
        if self.has_key(v):
            self[v] -= 1 

get_features = lambda x: tagger.Feats(x).features

make_dict_features  = lambda features: Dict([(x,0) for x in features])
    

def iterate(hist):
    hist_a = hist
    hist_b = hist.copy()
    hist_b.y = hist_b.y.map(lambda x: "O" if x == "I-GENE" else "I-GENE")
    

            
def feature_vals(features, hists):
    def check(feats):
        [features.inc(x) for x in feats]
        vals = array(features.values())
        [features.dec(x) for x in feats]
        return vals
        
    return array([check(x) for x in hists])

def scores(F, v, hists):
    return feature_vals(F, hists).dot(v)
    
    
class Viterbi():
    def __init__(self, U,V, T, sent, theta, g):
        self.U, self.V, self.T = U, V, T
        self.sent = sent
        self.theta = array(theta)
        self.n = len(sent)
        self.g = make_dict_features(g)
        self.Table = defaultdict(lambda: {"score":0, "t":""})
        self.table(0, "*", "*")["score"] = 1
        self.tags = []
        self._run()
        self.get_tag_sequence()
    
    def local_features(self, y2, y1, i, y):
            features = Feats({"w":self.sent, "i":i, "y2":y2, "y1":y1, "y":y}).features
            return feature_vals(self.g, [features])[0]
            
    def table(self,k, u, v):
        return self.Table[(k, u, v)]
    
            
    def _run(self):
        for k in range(1, self.n+1):
            for u in self.U:
                for v in self.V:
                    self.Table[(k,u,v)]  = max([{"score":( self.Table[((k-1), t, u)]["score"] + 
                                                          self.theta.dot(self.local_features(t, u, k, v))), "t":t} for t in self.T],
                                               key=lambda x: x["score"])
    

    
    def get_tag_sequence(self):
        self.tags = flatten([max([(x,y) for x,y in self.Table.items() if x[0] == self.n], key=lambda k: k[-1]["score"])[0][-2:]])
        i = range(1, self.n - 1)
        i.reverse()
        i = array(i) + 2
        for k in i:
            self.tags.insert(0, self.Table[tuple(flatten(k, self.tags[:2]))]["t"])

            
    
    
























