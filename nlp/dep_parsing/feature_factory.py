from util import next_s, prev_s, in_between
from nltk.util import flatten
from features import features_gen, labled_features_gen

def Model(model, feature_vector = 0, L=False):
    def parser(X):
        sent  = X["x"]
        pos = X["pos"]
        if L:
            features = labled_features_gen(pos, sent, next_s(pos), prev_s(pos), in_between(pos))
        else:
            features = features_gen(pos, sent, next_s(pos), prev_s(pos), in_between(pos))
        
        def score(h,m,l=None):
            if l:
                active = flatten([f(h,m,l) for f in features.values()])    
            else:
                active = flatten([f(h,m) for f in features.values()])
            return sum([model[x] for x in active if model.has_key(x)])
            
        def active_features(h,m,l=None):
            if l:
                active = flatten([f(h,m,l) for f in features.values()])
            else:
                active = flatten([f(h,m) for f in features.values()])
            return [x for x in active if model.has_key(x)]
            
        functions = {"feature_vector": active_features, "score":score}
        if feature_vector == 0:
            return functions["score"]
        elif feature_vector == 1:
            return functions["feature_vector"]
        else:
            return functions
        
    return parser
