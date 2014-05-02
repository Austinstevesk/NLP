import nltk
from nltk.corpus import *
from nltk import *
class BigramChunker(nltk.ChunkParserI):
  def __init__(self, train_sents):
    train_data = [[(t,c) for w,t,c in nltk.chunk.tree2conlltags(sent)] for sent in train_sents]
    self.tagger = nltk.BigramTagger(train_data)

  def parse(self, sentence):
    pos_tags = [pos for (words, pos) in sentence]
    tagged_pos_tags = self.tagger.tag(pos_tags)
    chunktags = [chunktag for (pos, chunktag) in tagged_pos_tags]
    conlltags =[" ".join((word, pos, chunktag))+"\n" for ((word, pos), chunktag) in zip(sentence, chunktags)]
    return nltk.chunk.conllstr2tree("".join(conlltags))
