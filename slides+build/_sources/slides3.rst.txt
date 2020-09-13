.. raw:: html

   <link rel="stylesheet" href="_static/revealjs/css/theme/white.css">
   <link rel="stylesheet" href="_static/default.css">


Machine Learning Engineering
=============================================


Lecture 3
------------

  Testing and Functions


Today's Class
----------------

.. revealjs_fragments::

   * Development Setup
   * Testing and Hypothesis
   * Functional Python


Getting Setup
---------------

.. revealjs_fragments::

   * First assignment link
   * https://classroom.github.com/a/BQeMj6RP
   * Due Wednesday

Setup QAs
------------

.. revealjs_fragments::

   * Everyone should be setup
   * Git Links

   
The Guidebook
--------------

.. revealjs_fragments::

   * https://minitorch.github.io/
   * Full description of the material

 
  
Testing
==================

Running Tests
----------------

Run tests ::

  >>> python -m pytest tests/

Or per task ::

  >>> python run_tests.py
  
PyTest
-------------

* Finds files that begin with `test`
* Finds functions that begin with `test`
* Select based on filters


Gotchas
-------------

.. revealjs_fragments::
   
   * Test output is verbose
   * Read tests
   * Protip: minimize testing speed

Helpful Filters
------------------

Specific task ::
  
  >>> python -m pytest tests/ -m task0_1

Specific test ::

  >>> python -m pytest tests/ -k test_sum

How do unit tests work?
------------------------

.. revealjs_fragments::
   
   * Tries to run code
   * If there is a False assert it fails 
   * Only prints if test fails!
   * `assert` and `assert_close`

Module 0 Functions
-------------------

Implement ::

  def relu(x):
    """
    :math:`f(x) =` x if x is greater than 0, else 0

    (See `<https://en.wikipedia.org/wiki/Rectifier_(neural_networks)>`_ .)
    """

.. revealjs_fragments::
   
   * Pretty basic function.
   * How do we know it works?

    
Standard Unit Test
--------------------


Test for values with given inputs ::

  def test_relu():
      assert operators.relu(10.0) == 10.0
      assert operators.relu(-10.0) == 0.0

.. revealjs_fragments::
   
   * (PyTest succeeds if no assertions are called)


Ideal: Property Test
---------------------


Test that all values satisfy property ::

  def test_relu():
      for a in range(0, 1e9):
          assert operators.relu(a) == a

      for a in range(-1e9, 0):
          assert operators.relu(a) == 0.0
          

.. revealjs_fragments::
   
   * Intractable

QuickCheck (Hypothesis)
------------

* https://en.wikipedia.org/wiki/QuickCheck
* https://hypothesis.readthedocs.io/en/latest/
     
Compromise: Randomized Property Test
--------------------------------------


Test that randomly selected values satisfy property.

.. code:: python

  @given(floats())
  def test_relu(a):
      value = operators.relu(a)
      if a >= 0:
          assert value == a
      else:
          assert value == 0.0
          
.. revealjs_fragments::
   
   * Greater coverage with less code

Custom Generators
--------------------------------------

.. revealjs_fragments::
   
   * Can provide your own randomized generators
   * Future assignments will utilize this feature.


Functional Python
==================

Functional Programming
------------------------

* Style of programming where functions can be passed and used like other objects.
* One of several programming styles supported in Python.
* Good paradigm for mathematical programming

Functional Python
-----------------------

Functions as Arguments ::


  def combine3(fn, a, b, c):
     return fn(fn(a, b), c)

  def add3(a, b, c):
     return combine3(add, a, b, c)

  def mul3(a, b, c):
     return combine3(mul, a, b, c)

  add3(1, 3, 5) # 9

     
Functional Python
-----------------------

Functions as Returns ::


  def combine3(fn):
     def apply(a, b, c):
        return fn(fn(a, b), c)
     return apply

  add3 = combine3(add)
  mul3 = combine3(mul)

  add3(1, 3, 5) # 9
  combine3(add)(1, 3, 5) # 9

  def combine3(fn):
     return lambda a, b, c: fn(fn(a, b), c)
     

  
Higher-order Filter
-----------------------

Extended example::
   
  def filter(fn):
     def apply(ls):
        ret = []
        for x in ls:
           if fn(x):
               ret.append(x)
        return ret
     return apply

  def more_than_4(x):
      return x > 4
     
  filter_for_more_than_4 = filter(more_than_4)
  filter_for_more_than_4([1, 10, 3, 5]) # [10, 5]

Module-0 Functions
-------------------

.. autofunction:: minitorch.operators.map

Module-0 Functions
-------------------

.. autofunction:: minitorch.operators.zipWith

Module-0 Functions
-------------------

.. autofunction:: minitorch.operators.reduce

                  
Functional Python
------------------

Rules of Thumbs

.. revealjs_fragments::

   * Can get confusing.
   * When in doubt, write out defs


Visualization
===============


Main Idea
----------

* Show properties of the code and training as you code.
* https://playground.tensorflow.org/


Library: Visdom
---------------

* Code ::

    >>> visdom &

Code Snippet
-------------

Visdom windows ::

    import visdom
    vis = visdom.Visdom()
    vis.text('Hello, world!', win="hello")
    
    
Demo
-------



Q&A
======
  
