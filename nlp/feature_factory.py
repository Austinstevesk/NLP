
def Model(X, model, feature_vector = 0):
    sent  = X["x"]
    pos = X["pos"]
    features = {
            "POS:BIGRAM": lambda h,m: ":".join(("POS:BIGRAM", pos[h], pos[m])),
            "WORD:BIGRAM": lambda h,m: ":".join(("WORD:BIGRAM", sent[h], pos[m])),
            "POS:h:WORD:m": lambda h,m: ":".join(("POS:h:WORD:m", pos[h], sent[m])),
            "POS:h:WORD:h:WORD:m": lambda h,m: ":".join(("POS:h:WORD:h:WORD:m", pos[h], sent[h], sent[m])),
            "POS:h:WORD:h:POS:m": lambda h,m: ":".join(("POS:h:WORD:h:POS:m", pos[h], sent[h], pos[m])),
            "POS:m:WORD:h" : lambda h,m: ":".join(("POS:m:WORD:h", pos[m], sent[h])),
        }
  
    def score(h,m):
        active = [f(h,m) for f in features.values()]
        return sum([model[x] for x in active if model.has_key(x)])
        
    def active_features(h,m):
        active = [f(h,m) for f in features.values()]
        return [x for x in active if model.has_key(x)]
        
    functions = {"feature_vector": active_features, "score":score}
    if feature_vector == 0:
        return functions["score"]
    elif feature_vector == 1:
        return functions["feature_vector"]
    else:
        return functions

