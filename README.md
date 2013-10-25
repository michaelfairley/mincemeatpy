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

* Just [mincemeat.py](https://raw.github.com/michaelfairley/mincemeatpy/v0.1.4/mincemeat.py) (v 0.1.4)
* The [full 0.1.4 release](https://github.com/michaelfairley/mincemeatpy/zipball/v0.1.4) (includes documentation and examples)
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
# The data source can be any dictionary-like object
datasource = dict(enumerate(data))

def mapfn(k, v):
    for w in v.split():
        yield w, 1

def reducefn(k, vs):
    result = sum(vs)
    return result

s = mincemeat.Server()
s.datasource = datasource
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

Clients
-------

You can run the client manually from within other Python scripts (rather than running mincemeat.py directly):

```python
import mincemeat

client = mincemeat.Client()
client.password	= "changeme"
client.conn("localhost", mincemeat.DEFAULT_PORT)
```

[Shepherd.py](https://github.com/jpmec/shepherdpy) provides more sophisticated ways to run clients, including having client that poll or are forked on the same machine.

Imports
-------

One potential gotcha when using mincemeat.py: Your `mapfn` and `reducefn` functions don't have access to their enclosing environment, including imported modules. If you need to use an imported module in one of these functions, be sure to include `import whatever` in the functions themselves.


Python 3 support
-------
[ziyuang](https://github.com/ziyuang/mincemeatpy) has a fork of mincemeat.py that's comptable with python 3: [ziyuang/mincemeatpy](https://github.com/ziyuang/mincemeatpy)
