def direction(h, m): return "R" if h < m else "L"

def dist(h,m): return str(10) if abs(h-m) > 5 else str(abs(h-m))

features_gen = lambda pos, sent, next_pos, prev_pos, in_between_pos: {
    "UNIGRAM:WORD:h:POS:h": lambda h,m: ":".join(("UNIGRAM:WORD:h:POS:h", sent[h], pos[h])),
    "UNIGRAM:WORD:h": lambda h,m: ":".join(("UNIGRAM:WORD:h", sent[h])),
    "UNIGRAM:POS:h": lambda h,m: ":".join(("UNIGRAM:POS:h", pos[h])),
    "UNIGRAM:WORD:m:POS:m": lambda h,m: ":".join(("UNIGRAM:WORD:m:POS:m", sent[m], pos[m])),
    "UNIGRAM:WORD:m": lambda h,m: ":".join(("UNIGRAM:WORD:m", sent[m])),
    "UNIGRAM:POS:m": lambda h,m: ":".join(("UNIGRAM:POS:m", pos[m])),

    "BIGRAM:POS:h:POS:m": lambda h,m: ":".join(("BIGRAM:POS:h:POS:m", pos[h], pos[m])),
    "BIGRAM:WORD:h:WORD:m": lambda h,m: ":".join(("BIGRAM:WORD:h:WORD:m", sent[h], sent[m])),
    "BIGRAM:WORD:h:POS:h:WORD:m" : lambda h,m: ":".join(("BIGRAM:WORD:h:POS:h:WORD:m", sent[h], pos[h], sent[m])),
    "BIGRAM:WORD:h:POS:h:POS:m" : lambda h,m: ":".join(("BIGRAM:WORD:h:POS:h:POS:m", sent[h], pos[h], pos[m])),
    "BIGRAM:WORD:h:WORD:m:POS:m" : lambda h,m: ":".join(("BIGRAM:WORD:h:WORD:h:POS:m", sent[h], sent[m], pos[m])),
    "BIGRAM:POS:h:WORD:m:POS:m" : lambda h,m: ":".join(("BIGRAM:POS:h:WORD:m:POS:m", pos[h], sent[h], pos[m])),
    "BIGRAM:WORD:h:POS:h:WORD:m:POS:m" : lambda h,m: ":".join(("BIGRAM:WORD:h:POS:h:WORD:m:POS:m", sent[h], pos[h], sent[m], pos[m])),

    "SURROUNDING:POS:h:NEXT:h:PREV:m:POS:m": lambda h,m: ":".join(("SURROUNDING:POS:h:NEXT:h:PREV:m:POS:m", pos[h], next_pos(h), prev_pos(m), pos[m])),
    "SURROUNDING:PREV:h:POS:h:PREV:m:POS:m": lambda h,m: ":".join(("SURROUNDING:PREV:h:POS:h:PREV:m:POS:m", prev_pos(h), pos[h], prev_pos(m), pos[m])),
    "SURROUNDING:POS:h:NEXT:h:POS:m:NEXT:m": lambda h,m: ":".join(("SURROUNDING:POS:h:NEXT:h:POS:m:NEXT:m", pos[h], next_pos(h), pos[m], next_pos(m))),
    "SURROUNDING:PREV:h:POS:h:POS:m:NEXT:m": lambda h,m: ":".join(("SURROUNDING:PREV:h:POS:h:POS:m:NEXT:m", prev_pos(h), pos[h], pos[m], next_pos(m))),

    "IN-BETWEEN:POS:h:BETWEEN:pos:POS:m" : lambda h, m:  [":".join(("IN-BETWEEN:POS:h:BETWEEN:pos:POS:m:dir:dist", pos[h], between, pos[m])) for between in in_between_pos(h, m)],
    
    "UNIGRAM:WORD:h:POS:h:dir:dist": lambda h,m: ":".join(("UNIGRAM:WORD:h:POS:h:dir:dist", sent[h], pos[h], direction(h,m), dist(h,m))),
    "UNIGRAM:WORD:h:dir:dist": lambda h,m: ":".join(("UNIGRAM:WORD:h:dir:dist", sent[h], direction(h,m), dist(h,m))),
    "UNIGRAM:POS:h:dir:dist": lambda h,m: ":".join(("UNIGRAM:POS:h:dir:dist", pos[h], direction(h,m), dist(h,m))),
    "UNIGRAM:WORD:m:POS:m:dir:dist": lambda h,m: ":".join(("UNIGRAM:WORD:m:POS:m:dir:dist", sent[m], pos[m], direction(h,m), dist(h,m))),
    "UNIGRAM:WORD:m:dir:dist": lambda h,m: ":".join(("UNIGRAM:WORD:m:dir:dist", sent[m], direction(h,m), dist(h,m))),
    "UNIGRAM:POS:m:dir:dist": lambda h,m: ":".join(("UNIGRAM:POS:m:dir:dist", pos[m], direction(h,m), dist(h,m))),

    "BIGRAM:POS:h:POS:m:dir:dist": lambda h,m: ":".join(("BIGRAM:POS:h:POS:m:dir:dist", pos[h], pos[m], direction(h,m), dist(h,m))),
    "BIGRAM:WORD:h:WORD:m:dir:dist": lambda h,m: ":".join(("BIGRAM:WORD:h:WORD:m:dir:dist", sent[h], sent[m], direction(h,m), dist(h,m))),
    "BIGRAM:WORD:h:POS:h:WORD:m:dir:dist" : lambda h,m: ":".join(("BIGRAM:WORD:h:POS:h:WORD:m:dir:dist", sent[h], pos[h], sent[m], direction(h,m), dist(h,m))),
    "BIGRAM:WORD:h:POS:h:POS:m:dir:dist" : lambda h,m: ":".join(("BIGRAM:WORD:h:POS:h:POS:m:dir:dist", sent[h], pos[h], pos[m], direction(h,m), dist(h,m))),
    "BIGRAM:WORD:h:WORD:m:POS:m:dir:dist" : lambda h,m: ":".join(("BIGRAM:WORD:h:WORD:h:POS:m:dir:dist", sent[h], sent[m], pos[m], direction(h,m), dist(h,m))),
    "BIGRAM:POS:h:WORD:m:POS:m:dir:dist" : lambda h,m: ":".join(("BIGRAM:POS:h:WORD:m:POS:m:dir:dist", pos[h], sent[h], pos[m], direction(h,m), dist(h,m))),
    "BIGRAM:WORD:h:POS:h:WORD:m:POS:m:dir:dist" : lambda h,m: ":".join(("BIGRAM:WORD:h:POS:h:WORD:m:POS:m:dir:dist", sent[h], pos[h], sent[m], pos[m], direction(h,m), dist(h,m))),

    "SURROUNDING:POS:h:NEXT:h:PREV:m:POS:m:dir:dist": lambda h,m: ":".join(("SURROUNDING:POS:h:NEXT:h:PREV:m:POS:m:dir:dist", pos[h], next_pos(h), prev_pos(m), pos[m], direction(h,m), dist(h,m))),
    "SURROUNDING:PREV:h:POS:h:PREV:m:POS:m:dir:dist": lambda h,m: ":".join(("SURROUNDING:PREV:h:POS:h:PREV:m:POS:m:dir:dist", prev_pos(h), pos[h], prev_pos(m), pos[m], direction(h,m), dist(h,m))),
    "SURROUNDING:POS:h:NEXT:h:POS:m:NEXT:m:dir:dist": lambda h,m: ":".join(("SURROUNDING:POS:h:NEXT:h:POS:m:NEXT:m:dir:dist", pos[h], next_pos(h), pos[m], next_pos(m), direction(h,m), dist(h,m))),
    "SURROUNDING:PREV:h:POS:h:POS:m:NEXT:m:dir:dist": lambda h,m: ":".join(("SURROUNDING:PREV:h:POS:h:POS:m:NEXT:m:dir:dist", prev_pos(h), pos[h], pos[m], next_pos(m), direction(h,m), dist(h,m))),

    "IN-BETWEEN:POS:h:BETWEEN:pos:POS:m:dir:dist" : lambda h, m:  [":".join(("IN-BETWEEN:POS:h:BETWEEN:pos:POS:m:dir:dist", pos[h], between, pos[m], direction(h,m), dist(h,m))) for between in in_between_pos(h, m)],


}



labled_features_gen = lambda pos, sent, next_pos, prev_pos, in_between_pos: {
    "UNIGRAM:WORD:h:POS:h": lambda h,m,l: ":".join(("UNIGRAM:WORD:h:POS:h", sent[h], pos[h], l)),
    "UNIGRAM:WORD:h": lambda h,m,l: ":".join(("UNIGRAM:WORD:h", sent[h], l)),
    "UNIGRAM:POS:h": lambda h,m,l: ":".join(("UNIGRAM:POS:h", pos[h], l)),
    "UNIGRAM:WORD:m:POS:m": lambda h,m,l: ":".join(("UNIGRAM:WORD:m:POS:m", sent[m], pos[m], l)),
    "UNIGRAM:WORD:m": lambda h,m,l: ":".join(("UNIGRAM:WORD:m", sent[m], l)),
    "UNIGRAM:POS:m": lambda h,m,l: ":".join(("UNIGRAM:POS:m", pos[m], l)),

    "BIGRAM:POS:h:POS:m": lambda h,m,l: ":".join(("BIGRAM:POS:h:POS:m", pos[h], pos[m], l)),
    "BIGRAM:WORD:h:WORD:m": lambda h,m,l: ":".join(("BIGRAM:WORD:h:WORD:m", sent[h], sent[m], l)),
    "BIGRAM:WORD:h:POS:h:WORD:m" : lambda h,m,l: ":".join(("BIGRAM:WORD:h:POS:h:WORD:m", sent[h], pos[h], sent[m], l)),
    "BIGRAM:WORD:h:POS:h:POS:m" : lambda h,m,l: ":".join(("BIGRAM:WORD:h:POS:h:POS:m", sent[h], pos[h], pos[m], l)),
    "BIGRAM:WORD:h:WORD:m:POS:m" : lambda h,m,l: ":".join(("BIGRAM:WORD:h:WORD:h:POS:m", sent[h], sent[m], pos[m], l)),
    "BIGRAM:POS:h:WORD:m:POS:m" : lambda h,m,l: ":".join(("BIGRAM:POS:h:WORD:m:POS:m", pos[h], sent[h], pos[m], l)),
    "BIGRAM:WORD:h:POS:h:WORD:m:POS:m" : lambda h,m,l: ":".join(("BIGRAM:WORD:h:POS:h:WORD:m:POS:m", sent[h], pos[h], sent[m], pos[m], l)),

    "SURROUNDING:POS:h:NEXT:h:PREV:m:POS:m": lambda h,m,l: ":".join(("SURROUNDING:POS:h:NEXT:h:PREV:m:POS:m", pos[h], next_pos(h), prev_pos(m), pos[m], l)),
    "SURROUNDING:PREV:h:POS:h:PREV:m:POS:m": lambda h,m,l: ":".join(("SURROUNDING:PREV:h:POS:h:PREV:m:POS:m", prev_pos(h), pos[h], prev_pos(m), pos[m], l)),
    "SURROUNDING:POS:h:NEXT:h:POS:m:NEXT:m": lambda h,m,l: ":".join(("SURROUNDING:POS:h:NEXT:h:POS:m:NEXT:m", pos[h], next_pos(h), pos[m], next_pos(m), l)),
    "SURROUNDING:PREV:h:POS:h:POS:m:NEXT:m": lambda h,m,l: ":".join(("SURROUNDING:PREV:h:POS:h:POS:m:NEXT:m", prev_pos(h), pos[h], pos[m], next_pos(m), l)),

    "IN-BETWEEN:POS:h:BETWEEN:pos:POS:m" : lambda h, m,l:  [":".join(("IN-BETWEEN:POS:h:BETWEEN:pos:POS:m:dir:dist", pos[h], between, pos[m], l)) for between in in_between_pos(h, m)],

    "UNIGRAM:WORD:h:POS:h:dir:dist": lambda h,m,l: ":".join(("UNIGRAM:WORD:h:POS:h:dir:dist", sent[h], pos[h], direction(h,m), dist(h,m), l)),
    "UNIGRAM:WORD:h:dir:dist": lambda h,m,l: ":".join(("UNIGRAM:WORD:h:dir:dist", sent[h], direction(h,m), dist(h,m), l)),
    "UNIGRAM:POS:h:dir:dist": lambda h,m,l: ":".join(("UNIGRAM:POS:h:dir:dist", pos[h], direction(h,m), dist(h,m), l)),
    "UNIGRAM:WORD:m:POS:m:dir:dist": lambda h,m,l: ":".join(("UNIGRAM:WORD:m:POS:m:dir:dist", sent[m], pos[m], direction(h,m), dist(h,m), l)),
    "UNIGRAM:WORD:m:dir:dist": lambda h,m,l: ":".join(("UNIGRAM:WORD:m:dir:dist", sent[m], direction(h,m), dist(h,m), l)),
    "UNIGRAM:POS:m:dir:dist": lambda h,m,l: ":".join(("UNIGRAM:POS:m:dir:dist", pos[m], direction(h,m), dist(h,m), l)),

    "BIGRAM:POS:h:POS:m:dir:dist": lambda h,m,l: ":".join(("BIGRAM:POS:h:POS:m:dir:dist", pos[h], pos[m], direction(h,m), dist(h,m), l)),
    "BIGRAM:WORD:h:WORD:m:dir:dist": lambda h,m,l: ":".join(("BIGRAM:WORD:h:WORD:m:dir:dist", sent[h], sent[m], direction(h,m), dist(h,m), l)),
    "BIGRAM:WORD:h:POS:h:WORD:m:dir:dist" : lambda h,m,l: ":".join(("BIGRAM:WORD:h:POS:h:WORD:m:dir:dist", sent[h], pos[h], sent[m], direction(h,m), dist(h,m), l)),
    "BIGRAM:WORD:h:POS:h:POS:m:dir:dist" : lambda h,m,l: ":".join(("BIGRAM:WORD:h:POS:h:POS:m:dir:dist", sent[h], pos[h], pos[m], direction(h,m), dist(h,m), l)),
    "BIGRAM:WORD:h:WORD:m:POS:m:dir:dist" : lambda h,m,l: ":".join(("BIGRAM:WORD:h:WORD:h:POS:m:dir:dist", sent[h], sent[m], pos[m], direction(h,m), dist(h,m), l)),
    "BIGRAM:POS:h:WORD:m:POS:m:dir:dist" : lambda h,m,l: ":".join(("BIGRAM:POS:h:WORD:m:POS:m:dir:dist", pos[h], sent[h], pos[m], direction(h,m), dist(h,m), l)),
    "BIGRAM:WORD:h:POS:h:WORD:m:POS:m:dir:dist" : lambda h,m,l: ":".join(("BIGRAM:WORD:h:POS:h:WORD:m:POS:m:dir:dist", sent[h], pos[h], sent[m], pos[m], direction(h,m), dist(h,m), l)),

    "SURROUNDING:POS:h:NEXT:h:PREV:m:POS:m:dir:dist": lambda h,m,l: ":".join(("SURROUNDING:POS:h:NEXT:h:PREV:m:POS:m:dir:dist", pos[h], next_pos(h), prev_pos(m), pos[m], direction(h,m), dist(h,m), l)),
    "SURROUNDING:PREV:h:POS:h:PREV:m:POS:m:dir:dist": lambda h,m,l: ":".join(("SURROUNDING:PREV:h:POS:h:PREV:m:POS:m:dir:dist", prev_pos(h), pos[h], prev_pos(m), pos[m], direction(h,m), dist(h,m), l)),
    "SURROUNDING:POS:h:NEXT:h:POS:m:NEXT:m:dir:dist": lambda h,m,l: ":".join(("SURROUNDING:POS:h:NEXT:h:POS:m:NEXT:m:dir:dist", pos[h], next_pos(h), pos[m], next_pos(m), direction(h,m), dist(h,m), l)),
    "SURROUNDING:PREV:h:POS:h:POS:m:NEXT:m:dir:dist": lambda h,m,l: ":".join(("SURROUNDING:PREV:h:POS:h:POS:m:NEXT:m:dir:dist", prev_pos(h), pos[h], pos[m], next_pos(m), direction(h,m), dist(h,m), l)),

    "IN-BETWEEN:POS:h:BETWEEN:pos:POS:m:dir:dist" : lambda h, m,l:  [":".join(("IN-BETWEEN:POS:h:BETWEEN:pos:POS:m:dir:dist", pos[h], between, pos[m], direction(h,m), dist(h,m), l)) for between in in_between_pos(h, m)],
}
