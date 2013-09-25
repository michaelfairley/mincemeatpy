#!/usr/bin/env python
import mincemeat

data = [["Humpty Dumpty sat on a wall",
        "Humpty Dumpty had a great fall",
        "All the King's horses and all the King's men",
        "Couldn't put Humpty together again",
        ]
        ,
        ["Jack and Jill went up the hill",
         "to fetch a pail of water",
         "Jack fell down and broke his crown",
         "and Jill came tumbling after"
        ]]

# The data source can be any dictionary-like object
datasource = dict(enumerate(data))

def mapfn1(k, v):

    import mincemeat

    def mapfn2(k, v):
        for w in v.split():
            yield w, 1

    def reducefn2(k, vs):
        result = sum(vs)
        return result

    s = mincemeat.Server()
    s.datasource = dict(enumerate(v))
    s.mapfn = mapfn2
    s.reducefn = reducefn2

    results = s.run_server(password="changeme2", port=11236)

    for key, value in results.iteritems():
        yield key, value


def reducefn1(k, vs):
    result = sum(vs)
    return result


s = mincemeat.Server()
s.datasource = datasource
s.mapfn = mapfn1
s.reducefn = reducefn1

results = s.run_server(password="changeme1", port=11235)
print results
