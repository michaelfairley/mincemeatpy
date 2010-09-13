#!/usr/bin/env python
import mincemeat

data = ["Humpty Dumpty sat on a wall",
        "Humpty Dumpty had a great fall",
        "All the King's horses and all the King's men",
        "Couldn't put Humpty together again",
        ]

def mapfn(k, v):
    for w in v.split():
        yield w, 1

def reducefn(k, vs):
    result = 0
    for v in vs:
        result += v
    return result

s = mincemeat.Server()

# The data source can be any dictionary-like object
s.datasource = dict((i, data[i]) for i in xrange(len(data)))
s.mapfn = mapfn
s.reducefn = reducefn

results = s.run_server(password="changeme")
print results
