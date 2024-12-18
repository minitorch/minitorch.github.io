..
  done

================================
Autodiff
================================

This module shows how to build the first version of MiniTorch using
only simple values and functions. This covers key aspects of
auto-differentiation: the key technique in the system. Then you will
use your code to train a preliminary model.

All starter code is available in https://github.com/minitorch/Module-1.
Module 1 is built upon the previous Module 0, so make sure to pull your
files from Assignment 0
to your new repo. Please continue to follow the :doc:`contributing` guideline.

**Guides**

.. toctree::
   :maxdepth: 1
   :glob:


   derivative
   scalar
   chainrule
   backpropagate

Tasks
******


Task 1.1: Numerical Derivatives
==================================

.. note:: This task requires basic familiarity with derivatives.
   Be sure to review `differentiation rules
   <https://en.wikipedia.org/wiki/Differentiation_rules>`_
   and the notation for derivatives.
   Then carefully read the Guide on
   :doc:`derivative`.

.. todo::
   Complete the following function in `minitorch/scalar.py` and pass tests
   marked as `task1_1`.

.. autofunction:: minitorch.scalar.central_difference



Task 1.2: Scalars
========================

.. note::

   This task requires familiarity with the :class:`minitorch.Scalar` class.
   Be sure to first carefully read the Guide on
   :doc:`scalar` and to refresh your memory on `Python numerical overrides
   <https://docs.python.org/3/reference/datamodel.html#emulating-numeric-types/>`_.

Implement the overridden mathematical functions required for the
:class:`minitorch.Scalar` class.
Each of these requires wiring the internal Python operator to the correct
:func:`minitorch.Function.forward` call.


Read the example ScalarFunctions that we have implemented for guidelines. You
may find it useful to reuse the operators from Module 0.


We have built a debugging tool for you to observe the workings of your
expressions to see how the graph is built. You can run it in the
`Autodiff Sandbox`.  You can alter the expression at the top of the
file and then run the code to create a graph in `Streamlit`::

>>> streamlit run app.py -- 1


.. todo::
   Complete the following functions in `minitorch/scalar_functions.py`.


.. autofunction:: minitorch.scalar_functions.Mul.forward
.. autofunction:: minitorch.scalar_functions.Inv.forward
.. autofunction:: minitorch.scalar_functions.Neg.forward
.. autofunction:: minitorch.scalar_functions.Sigmoid.forward
.. autofunction:: minitorch.scalar_functions.ReLU.forward
.. autofunction:: minitorch.scalar_functions.Exp.forward
.. autofunction:: minitorch.scalar_functions.LT.forward
.. autofunction:: minitorch.scalar_functions.EQ.forward

.. todo:: Complete the following function in `minitorch/scalar.py`, and pass
   tests marked as `task1_2`.
   See `Python numerical overrides
   <https://docs.python.org/3/reference/datamodel.html#emulating-numeric-types/>`_
   for the interface of these methods. All of these functions should return
   :class:`minitorch.Scalar` arguments.


.. autofunction:: minitorch.Scalar.__lt__
.. autofunction:: minitorch.Scalar.__gt__
.. autofunction:: minitorch.Scalar.__sub__
.. autofunction:: minitorch.Scalar.__neg__
.. autofunction:: minitorch.Scalar.__add__

.. autofunction:: minitorch.Scalar.log
.. autofunction:: minitorch.Scalar.exp
.. autofunction:: minitorch.Scalar.sigmoid
.. autofunction:: minitorch.Scalar.relu




Task 1.3: Chain Rule
========================

.. note::  This task is quite tricky, so be sure you
   understand the chain rule, Variables, and Functions.
   Be sure to first read the Guide on
   :doc:`chainrule` very carefully and read the code for other ScalarFunctions.


Implement the `chain_rule` function in Scalar for functions of arbitrary
arguments.
This function should be able to backward process a function by passing it in
a context and :math:`d_{out}` and then collecting the local derivatives. It
should then pair these with the right variables and return them. This function
is also where we filter out constants that were used on the forward pass,
but do not need derivatives.

.. todo::
   Complete the following function in `minitorch/scalar.py`, and pass
   tests marked as `task1_3`.


.. autofunction:: minitorch.Scalar.chain_rule



Task 1.4: Backpropagation
==========================

.. note::
   Be sure to first read the Guide on
   :doc:`backpropagate` very carefully and read the code for other
   ScalarFunctions.


Implement backpropagation. Each of these requires wiring the internal Python
operator to the correct
:func:`minitorch.Function.backward` call.


Read the example ScalarFunctions that we have implemented for
guidelines. Feel free to also consult `differentiation rules
<https://en.wikipedia.org/wiki/Differentiation_rules>`_ if you forget how
these identities work.



.. todo::
   Complete the following functions in `minitorch/autodiff.py` and
   `minitorch/scalar.py`,
   and pass tests marked as `task1_4`.

.. autofunction:: minitorch.topological_sort
.. autofunction:: minitorch.backpropagate

.. autofunction:: minitorch.scalar_functions.Mul.backward
.. autofunction:: minitorch.scalar_functions.Inv.backward
.. autofunction:: minitorch.scalar_functions.Neg.backward
.. autofunction:: minitorch.scalar_functions.Sigmoid.backward
.. autofunction:: minitorch.scalar_functions.ReLU.backward
.. autofunction:: minitorch.scalar_functions.Exp.backward



Task 1.5: Training
========================

If your code works, you should now be able to run the training script.
Study the code in `project/run_scalar.py` carefully to understand what
the neural network is doing.

You will also need Module code to implement the parameters `Network`
and for `Linear`.
You can modify the dataset and the module with
the parameters at the bottom of the file. Start with this simple config::

  PTS = 50
  DATASET = minitorch.datasets["Simple"](PTS)
  HIDDEN = 2
  RATE = 0.5


You can then move up to something more complex, for instance::

  PTS = 50
  DATASET = minitorch.datasets["Xor"](PTS)

  HIDDEN = 10
  RATE = 0.5


If your code is successful, you should be able to run the full visualization:

>>> streamlit run app.py -- 1



.. todo::
   Train a scalar model for each of the 4 main datasets.

   Add the output training logs and final images to your README file.
