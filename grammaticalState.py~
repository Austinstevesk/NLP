from __future__ import division
import enchant
import nltk
from nltk.metrics import *
import collections
import pandas
import chardet


class CorpusGrammarState:
  def __init__(self, corpus):
    self.words = collections.defaultdict(list)
    self._corpus = [[self.words[fileid], self.words[fileid].extend(nltk.util.flatten([nltk.tokenize.word_tokenize(sent) for sent in nltk.tokenize.sent_tokenize(corpus.raw(fileid))]))] for fileid in corpus.fileids()]

  def corpus_status(self):
    return pandas.DataFrame(data=[GrammerState(x).grammatical_status() for x in self.words.itervalues()], index=self.words.iterkeys())



  

class GrammerState:
  def __init__(self, words, eng_dict=enchant.Dict('en')):
    self._words = [w for w in words if len(w) > 0 and chardet.detect(w)['encoding'] == 'ascii']
    self._eng_dict = eng_dict
    
  def __in_dict(self):
    return sum(1 for w in self._words if self._eng_dict.check(w))
  
  def __not_in_dict(self):
    return sum(1 for w in self._words if not self._eng_dict.check(w))
  
  def words_not_in_dict(self):
    return [w for w in self._words if not self._eng_dict.check(w)]
  
  def attempt_corrections(self, words):
    best_matches = []
    for w in words:
      sugg = self._eng_dict.suggest(w)
      if (len(sugg) > 0):
        top_word =sugg[0]
        edit_dist = edit_distance(w, top_word)
        if (edit_dist < 2): best_matches.append((w, top_word, edit_dist))
    return best_matches
  
  def grammatical_status(self):
    in_dict = self.__in_dict()
    not_in_dict = self.__not_in_dict()
    word_count = len(self._words)
    correct_pct = (in_dict/word_count) * 100
    wrong_pct = (not_in_dict/word_count) * 100
    return {'in_dict':in_dict, 'not_in_dict':not_in_dict, 'word_count':word_count, 'correct_pct':correct_pct, 'wrong_pct':wrong_pct}
