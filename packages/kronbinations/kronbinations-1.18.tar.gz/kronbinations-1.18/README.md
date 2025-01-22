# kronbinations
[![Python package](https://github.com/Ntropic/kronbinations/actions/workflows/python-package.yml/badge.svg)](https://github.com/Ntropic/kronbinations/actions/workflows/python-package.yml)  [![Coverage Status](https://coveralls.io/repos/github/Ntropic/kronbinations/badge.svg?branch=main)](https://coveralls.io/github/Ntropic/kronbinations?branch=main)

Install via 
`pip install kronbinations`

Import via
`from kronbinations import *`

## Description
**kronbinations** is used to *remove nested loops*, to perform *multidimensional parameter sweeps* and to generate arrays to store results of such sweeps. When adding parameters to a simulation, the involved loops and arrays for storing results don't need to be updated, kronbinations takes care of this. This makes the code more *readable* and *adaptable* to changes.

#### Recent Addition:
Now supports *lazy array execution*, that only calculats elements when needed, and saves the results in a Cache folder, to avoid recomputing the same elements. 
- This can be particular useful in Jupyter notebooks, so as to not recalculate cells that have already been executed,
- or for partial parameter sweeps, that are then expanded upon to cover a larger part of the parameter landscape. 
 
### Usage: 
This package is built around two classes: `kronbinations` and `JIT_kronbinations`, the latter of which supports lazy array execution. The two methods work in a similar way, we will first explore the usage of `kronbinations`, and then highlight the slight difference for `JIT_kronbinations`. We will separate the usage into three steps:
1. Define the kronbinations object via the parameters to iterate over,
2. Define the arrays to store the results in,
3. Define the iteration loop.

#### 1. Define the kronbinations object
For every parameter we want to iterate over we need to pass an array or list of its possible values to the kronbinations constructor. 
```
k = kronbinations([1,2,3], array(['a','b','c','d']), array([False,True]))
```
Alternatively we can pass a dictionary, where the keys are the names of the parameters, and the values are the arrays or lists of the possible values, passing a dictionary is recommended, as this allows us toquery the current value, index or changing of a parameter by its name within the iteration loop (this can be useful for conditional executions).
```
k = kronbinations({'integers': [1,2,3], 'letters': array(['a','b','c','d']), 'bools': array([False,True])})
```
In this example the kronbination object `k` then allows us to iterate over all combinations of integers, letters and bools.
#### 2. Define the arrays to store the results in
The results of computations are stored in appropriately sized arrays, that can be constructed via `k.empty()`, `k.ones()`, `k.zeros()` and `k.full(fill_value)`.  (and pass the corresponding numpy arguments , eg. `k.zeros(dtype=int)`). If a vector needs to be stored for every combination, the array can be constructed with an extra axis, eg. `A = k.empty((n,))` for $n$ values per combination. The arrays will usually behave exactly like numpy arrays as they inherit from them, but they can contain extra information, that matters for unconventional access to its elements, this is the case for use with `matplotlib`. To access the underlying numpy array, use `A.array()` or access specific subarrays via `A[indexes]`, which will return a regular numpy array.  
#### 3. Define the iteration loop
After this initialization, the iteration loop can be constructed. The kronbinations object `k` aids in this by providing a couple of useful functions:
- `k.kronprod()` returns a generator which yields the index, value and change of each parameter for every combination. it accepts the following arguments:
    - `index=bool [default=True]` to toggle the return of the index of the current combination,
    - `value=bool [default=True]` to toggle the return of the value of the current combination,
    - `change=bool [default=True]` to toggle the return of the change of the current combination,
    - `progress=bool [default=False]` to toggle the printing of a progress bar for the loop. 
- `k.index()` returns the indexes of the current combination, or a specific index specified by an index or a string (if `k` was initialized with a dictionary).
- `k.value()` returns the values of the current combination, or a specific value specified by an index or a string (if `k` was initialized with a dictionary).
- `k.change()` returns the change of the current combination, or a specific change specified by an index or a string (if `k` was initialized with a dictionary).
```
for index, values, changed in k.kronprod(index=True, change=True, progress=True):
    # Demonstrating a few of the functions here
    if changed[0]:
        print('First value changed')
        g = fun2(values[0])
    x[index] = fun(values, g)
```
### JIT_kronbinations
For `JIT_kronbinations` the usage is similar, but the iteration loop is passed to the generator, which parses the function handle, to make the execution predictable. For random number generators use `rng` as name of the numpy random number generator object. Here's an example of how to use `JIT_kronbinations`:
```
from kronbinations import *
import numpy as np
import matplotlib.pyplot as plt

a = np.linspace(0, 1, 5)
b = np.linspace(0, 1, 5)
c = 1.0

def gridspace(k, A, B):
    for i, v in k.kronprod(change=False):
        A[i] = v[0]+v[1]+v[2]
        B[i] = v[0]-v[1]
    return A, B

k = JIT_kronbinations(a, b, c, func=gridspace, redo=False, progress=True) 
A = k.zeros()
B = k.zeros()
plt.imshow(A.array())
```

### Tricks
You can use `k.tqdm(iterator)` in subloops which will lead to subiterations getting recognized und updated in the progress bar. 
NEW: `k.p_tqdm` can be used for parallel loop execution.

## Authors: 
By Michael Schilling