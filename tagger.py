import nltk
from nltk import *

def pos_tagger(train_set, tagger_classes, backoff=DefaultTagger('NN')):
    for cls, cutoff in tagger_classes:
        backoff = cls(train_set, backoff=backoff, cutoff=cutoff)
    return backoff
