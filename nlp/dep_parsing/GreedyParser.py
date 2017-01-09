#Greed is good as long as we are greedy together.

from feature_factory import Model
from inference_algorithms import MST, GreedyJoker, FirstOrder
from util import frequencies, rest
from features import features_gen, labled_features_gen

def linear_model(V, feature_vectors=0, inference="M", L=False):
    weights = Model(V, 2, L=L)
    
    def parser(data):
        n = len(data["x"])
        indexes = range(1,n) 
        model = weights(data)
        g = model["score"]
        f = model["feature_vector"]
        
        algorithms = {"M": MST, "G": GreedyJoker, "F": FirstOrder}
        if L:
            dependencies = algorithms[inference](g,n, L=L)
        else:
            dependencies = algorithms[inference](g,n)


        if feature_vectors:
            if L:
                return frequencies([f(h,m,l) for h,m,l in dependencies["pred"]])
            else:
                return frequencies([f(h,m) for h,m in dependencies["pred"]])
        else:
            return dependencies
            
            
    return parser

    
    
   


    
    
    

    
