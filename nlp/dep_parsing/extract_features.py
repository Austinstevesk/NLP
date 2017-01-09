from sklearn.feature_extraction.dict_vectorizer import DictVectorizer
from sklearn.linear_model.logistic import LogisticRegression
from nltk import *
from numpy import *
from scrap import *
from util import *
from features import features_gen, labled_features_gen

def train(data):
    X, Y, _ = vectorize(data)
    classifier = LogisticRegression()
    classifier.fit(X,Y)
    print(classifier.score(X,Y))


def vectorize(data):
    transformer = DictVectorizer()
    values= flatten([make_features(x) for x in  data])
    X = transformer.fit_transform([x["x"] for x in values]).toarray()
    Y = array([x["y"] for x in values])
    return (X, Y, values)

def present(x, dep):
    if(x in dep):
        return x[-1]
    else:
        return "NULL"

def training_features(parsed_sents,L=False):
    if not isinstance(parsed_sents, list):
        parsed_sents = [parsed_sents]
    return frequencies([generate_features(x, L) for x in parsed_sents])

def generate_features(data, L=False):
    return [x["x"].values() for x in make_features(data, L)]

def make_features(data, L=False):
    labels = {'DT', 'IND-OBJ', 'MAIN-VERB', 'OBJ', 'PREP', 'SUBJ'}
    pos = data["pos"]
    dep = data["y"]
    sent = data["x"]
    n = len(sent)
    def labled_features():
        features = labled_features_gen(pos, sent, next_s(pos), prev_s(pos), in_between(pos))
        f = lambda h,m,l: {"x": dict((k, g(h,m,l)) for k, g in features.iteritems()), "y": present((h,m,l), dep)}
        return [f(h,m,l) for h,m,l in dep]
    def unlabled_features():
        features = features_gen(pos, sent, next_s(pos), prev_s(pos), in_between(pos))

        f = lambda h,m: {"x": dict((k, g(h,m)) for k,g in features.iteritems()), "y": int((h,m) in dep)}
        return [f(h,m) for h,m in dep]
    if L:
        return labled_features()
    else:
        return unlabled_features()

def make_dict(data):
    data = data[1:]
    return {"y": [(x["head"], x["address"]) for x in data],
     "x": ["ROOT"] + [x["word"] for x in data],
     "pos": ["ROOT"] + [x["tag"] for x in data]}


    
    


        
    
    
    
    
