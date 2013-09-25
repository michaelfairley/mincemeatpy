mincemeat.py: MapReduce on Python
=================================

Introduction
------------
mincemeat.py is a Python implementation of the [MapReduce](http://en.wikipedia.org/wiki/Mapreduce) distributed computing framework.

mincemeat.py is:

* Lightweight - All of the code is contained in a single Python file (currently weighing in at <13kB) that depends only on the Python Standard Library. Any computer with Python and mincemeat.py can be a part of your cluster.
* Fault tolerant - Workers (clients) can join and leave the cluster at any time without affecting the entire process.
* Secure - mincemeat.py authenticates both ends of every connection, ensuring that only authorized code is executed.
* Open source - mincemeat.py is distributed under the [MIT License](http://en.wikipedia.org/wiki/Mit_license), and consequently is free for all use, including commercial, personal, and academic, and can be modified and redistributed without restriction.


Download
--------

* Just [mincemeat.py](https://raw.github.com/michaelfairley/mincemeatpy/master/mincemeat.py) (v 0.1.2)
* The [full 0.1.2 release](https://github.com/michaelfairley/mincemeatpy/zipball/v0.1.2) (includes documentation and examples)
* Clone this git repository: `git clone https://github.com/michaelfairley/mincemeatpy.git`

Example
-------

Let's look at the canonical MapReduce example, word counting:

example.py:

```python
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
s.datasource = dict(enumerate(data))
s.mapfn = mapfn
s.reducefn = reducefn

results = s.run_server(password="changeme")
print results
```

Execute this script on the server:

```bash
python example.py
```

Run mincemeat.py as a worker on a client:

```bash
python mincemeat.py -p changeme [server address]
```
And the server will print out:

```python
{'a': 2, 'on': 1, 'great': 1, 'Humpty': 3, 'again': 1, 'wall': 1, 'Dumpty': 2, 'men': 1, 'had': 1, 'all': 1, 'together': 1, "King's": 2, 'horses': 1, 'All': 1, "Couldn't": 1, 'fall': 1, 'and': 1, 'the': 2, 'put': 1, 'sat': 1}
```

This example was overly simplistic, but changing the datasource to be a collection of large files and running the client on multiple machines will work just as well. In fact, mincemeat.py has been used to produce a word frequency lists for many gigabytes of text using a slightly modified version of this code.


Another Example
---------------
Let's look at another MapReduce example of word counting.
This example will show how to nest Servers so you can chain MapReduce operations.

example2.py:

```python
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
```

First, start two workers by running this command in two separate terminal windows:
```bash
python mincemeat.py -p changeme2 [server address] -P 11236
```

The workers will attempt to connect to a server until a server starts or Ctrl+C is pressed.

Second, start another worker by running this command in a separate terminal window:
```bash
python mincemeat.py -p changeme1 [server address] -P 11235
```

Finally, start the master server by running this command in a separate terminal window:
```bash
python example2.py
```

And the server will print out:

```python
{'and': 4, 'all': 1, 'wall': 1, 'Dumpty': 2, 'crown': 1, "King's": 2, 'down': 1, 'sat': 1, 'again': 1, 'had': 1, 'to': 1, 'Jill': 2, 'tumbling': 1, 'hill': 1, 'Jack': 2, 'horses': 1, 'his': 1, 'pail': 1, 'men': 1, 'great': 1, 'water': 1, 'fell': 1, 'broke': 1, 'fall': 1, 'put': 1, 'the': 3, 'after': 1, 'a': 3, 'on': 1, 'All': 1, 'Humpty': 3, 'of': 1, 'up': 1, 'together': 1, "Couldn't": 1, 'went': 1, 'fetch': 1, 'came': 1}
```

What is important to notice here is that mapfn1 starts a server and sends chunks of data to the workers.
This pattern can be repeated to allow for chaining of MapReduce operations.


Imports
-------

One potential gotcha when using mincemeat.py: Your `mapfn` and `reducefn` functions don't have access to their enclosing environment, including imported modules. If you need to use an imported module in one of these functions, be sure to include `import whatever` in the functions themselves.


Python 3 support
-------
[ziyuang](https://github.com/ziyuang/mincemeatpy) has a fork of mincemeat.py that's comptable with python 3: [ziyuang/mincemeatpy](https://github.com/ziyuang/mincemeatpy)
