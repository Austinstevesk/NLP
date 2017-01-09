from __future__ import division
import GreedyParser
from util import merge_with, merge_without_mutation
from numpy import add, subtract
from collections import defaultdict
#from features import features_gen, labled_features_gen
import features as feats

def train(V, train, inference="M", L=False, T=5):
    V = V
    for t in range(T):
        for x in train:
            F = x["F"]
            Z = GreedyParser.linear_model(V, 1, L=L)(x)
            
            if (F != Z):
                V = merge_with(add, V, merge_without_mutation(subtract, F, Z))
                
    return V
        

def evaluate(V, test, L=False):
    parser = GreedyParser.linear_model(V, L=L)
    scores = defaultdict(lambda : {"score":0, "pred":[], "actual":[]})
    count = 0
    N = len(test)
    for i in range(N):
        x = test[i]
        y = [tuple(t) for t in x["y"]]
        pred = parser(x)
        score = 1 - (len(set(y).difference(set(pred["pred"]))) / len(y))
        scores[i] = {"score":score, "pred": pred, "actual":y}
        print("T minus %s " % (N-count))
        count += 1
              
    return  scores

def parser(V, L=False):
    parser = GreedyParser.linear_model(V, L=L)
    
    def parse(sent):
        return parser(sent)["pred"]
    
    return parse
    
        
        
