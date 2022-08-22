====================
Tracking Operations
====================

.. jupyter-execute::
   :hide-code:


   import sys
   sys.path.append("../")
   sys.path.append("../project/")
   sys.path.append("../project/interface/")
   import minitorch
   from minitorch import ScalarFunction
   from show_expression import make_graph
   from drawing import *
   from IPython.display import SVG, display


In :doc:`derivative`, we discussed two ways to compute derivatives.
`Symbolic` derivatives require access to the full symbolic function,
whereas `numerical` derivatives require only a black-box
function. The first is precise but rigid, whereas the second is
imprecise but more flexible. This module introduces a third
approach known as `autodifferentiation` which is a tradeoff between
symbolic and numerical methods.

We will see that autodifferentiation works by collecting information about the
computation path used within the function, and then transforming this
information into a procedure for computing derivatives. Unlike the
black-box method, autodifferentiation will allow us to use this information to
compute each step more precisely.

However, in order to collect the information about the computation path,
we need to track the
internal computation of the function. This can be hard to do since
Python does not expose how its inputs are used in the function
directly: all we get is the output only. This doc describes one method
for tracking computation.



Overriding Numbers
------------------

Since we do not have access to the underlying language interpreter,
we are going to build a system to track the mathematical operations
applied to each number.


1. Replace all numbers with proxy a class, which we will call `Scalar`
2. Replace all mathematical functions with proxy operators.
3. Remember what operators were applied to each Scalar.


Consider the following code which shows the result of this approach.

.. jupyter-execute::
   :hide-code:

   x = minitorch.Scalar(10)
   y = x + x
   y.history



Scalar should behave exactly
like numbers. The goal is that the user cannot tell the
difference. But we will utilize the extra information
to implement the operations we need.


Functions
-----------

When working with these new number we restrict ourselves to
use a small set of mathematical functions :math:`f` of one or
two arguments.
Graphically, we will think of functions as little boxes. For
example, a one-argument function would look like this,

.. jupyter-execute::
   :hide-code:

   draw_boxes(["$x$", "$f(x)$"], [1])


Internally, the box `unwraps` the content of :math:`x`,
manipulates it, and returns a new value with the saved history. We can chain
together two of these functions to produce more complex functions.


.. jupyter-execute::
   :hide-code:

   draw_boxes(["$x$", "$g(x)$", "$f(g(x))$"], [1, 1])


Similarly, a two-argument function `unwraps` the content of both inputs
:math:`x` and :math:`y`, manipulates them, and returns a new wrapped version:

.. jupyter-execute::
   :hide-code:

   draw_boxes([("$x$", "$y$"), "$f(x, y)$"], [1])


Finally we can create more complex functions that chain these together in
various ways.

.. jupyter-execute::
   :hide-code:

    draw_boxes([("", ""), "", "", ""], [1, 2, 1], lr=True)


Implementation
-----------------

We will implement tracking using the :class:`minitorch.Scalar` class. It wraps a
single number (which is stored in the `data` attribute) and its history.

.. jupyter-execute::
   :hide-code:

   x = minitorch.Scalar(10)


To implement functions there is a corresponding class :class:`minitorch.ScalarFunction`.
We will need to reimplement each mathematical function that we would like to use by inheriting
from this class.

For example, say our function is `Neg`, :math:`g(x) = -x`

.. jupyter-execute::

      class Neg(ScalarFunction):

          @staticmethod
          def forward(ctx, x):
              return -x

Or, say the function is `Mul`, :math:`f(x, y) = x \times y` that multiplies
x by y

.. jupyter-execute::

      class Mul(ScalarFunction):
          @staticmethod
          def forward(ctx, x, y):
              return x * y

.. Note::

   Within the forward function, x and y are always unwrapped numbers. Forward
   function processes and returns unwrapped values.

If we have scalars :math:`x, y`, we can apply the above function by

.. jupyter-execute::

   z = Neg.apply(x)
   out = Neg.apply(z)

   # or
   out2 = Mul.apply(x, z)


Note, that we do not call `forward` directly a special method `apply`.
Internally 'apply'  converts the inputs to standard numbers to call `forward`,
and then wraps the output float with the history it needs.

.. jupyter-execute::

   print(out.history)

Here `out` has remembered the graph that led to its creation.

.. jupyter-execute::
   :hide-code:

   draw_boxes(["$x$", "$g(x)$", "$f(g(x))$"], [1, 1])


Minitorch includes a library to allow you to draw these box diagrams
for arbitrarily complex functions.


.. jupyter-execute::

   out.name = "out"
   SVG(make_graph(out, lr=True))


.. jupyter-execute::

   out2.name = "out"
   SVG(make_graph(out2, lr=True))


Operators
-----------------


There is still one minor issue. This is what our code looks like to use `Mul`,

.. jupyter-execute::

    out2 = Mul.apply(x, y)

It is a bit annoying to write code this way. Also, we promised
that we would have functions that look just like the Python operators we are
used to writing.

To get around this issue, we need to augment the :class:`minitorch.Scalar`
class
so that it can behave normally under standard mathematical operations.
Instead of
calling regular *, Python will call our *.  Once this is achieved, we will
have the ability
to record and track how :math:`x` is used in the
Function, while still being able to write

.. jupyter-execute::

    out2 = x * y

To achieve this, the :class:`minitorch.Scalar` class needs to provide syntax
that makes it appear like
a number when in use. You can read `emulating numeric types
<https://docs.python.org/3/reference/datamodel.html#emulating-numeric-types>`_
to learn how this could be done.
