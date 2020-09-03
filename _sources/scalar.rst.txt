====================
Tracking Variables
====================

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

However, in order to collect the information about the computation path, we need to track the
internal computation of the function. This can be hard to do since
Python does not expose how its inputs are used in the function
directly: all we get is the output only. This doc describes one method
for tracking computation.



Variables and Functions
------------------------

The main trick for tracking computation is surprisingly simple and direct:

1. replace all Python values with proxy classes, known as `Variable`s.
2. replace all mathematical operators with proxy operators, known `Function`s.
3. augment `Variable`s to remember what `Function`s were applied to them in the past.

For notation, we will use capital letters in this section to refer to our new 
Functions and Variables to distringuish them from Python functions and variables.

The goal will be for these Variables and Functions to behave exactly
like Python numbers such that the user cannot tell the
difference. It's a bit hacky, but pretty neat under-the-hood. We
literally just create a generic Variable class

.. autoclass:: minitorch.Variable

As well as a generic Function class.

.. autoclass:: minitorch.FunctionBase


If we have two Variables :math:`x` and :math:`y`, we as a user **cannot** ever
change or manipulate their values directly. We **must** create a
`Function` class that acts on them.


It will be useful to think of these Functions as little boxes. For
instance a one-arg Function would look like

.. image:: figs/Autograd/autograd1.png
           :align: center

Internally the box `unwraps` the content of the variable, manipulates it, and returns a new `wrapped` Variable.


And a two-arg function `unwraps` the content of both Variables,
manipulates them, and returns a new `wrapped` Variable.

.. image:: figs/Autograd/autograd2.png
           :align: center

Scalar Functions
-----------------

To make this whole Variable/Function idea more tangible, let us focus
on the Scalar class, a sub-class of :class:`minitorch.Variable`. It wraps a
single scalar float (which is stored in the `data` attribute).

.. autoclass:: minitorch.Scalar


This Variable has a corresponding Function class that
is a subclass of :class:`FunctionBase`

.. autoclass:: minitorch.ScalarFunction



Let's assume we want to implement a simple function :math:`f(x)` that is from
float-to-float.  We implement it as a class with a static method:
:func:`ScalarFunction.forward`. ::

      class f(ScalarFunction):
          @staticmethod
          def forward(ctx, x):
              # Compute g(x) (ignore ctx for now)
              ...

.. image:: figs/Autograd/autograd1.png
           :align: center

For example, say our function is `TimesFive`, :math:`f(x) = x \times 5` ::


      class TimesFive(ScalarFunction):
          @staticmethod
          def forward(ctx, x):
              return x * 5

Or, say the function is `Mul`, :math:`g(x, y) = x \times y` that multiplies x by y. ::


      class Mul(ScalarFunction):
          @staticmethod
          def forward(ctx, x, y):
              return x * y


.. image:: figs/Autograd/autograd2.png
           :align: center

.. Note::

   Within forward x and y are always numbers (not Variables). Forward is processing
   and returning the unwrapped values.

If we have a scalars :math:`x, y`, applying these Functions is done by  ::

  z = TimesFive.apply(x)
  out = TimesFive.apply(z)
  # or
  out2 = TimesFive.apply(x, y)

Critically, we must not call `forward` but instead `apply`. This is because internally
the apply method is converting variables to floats to call `forward`. It is also
creating a trail of the history and creating a variable for the output. Here `z`, `out`,
and `out2` are all Variables.

.. image:: figs/Autograd/chain1.png
           :align: center

This history is represented by a chain of the previous boxes that we
led to the given point.



Syntactic Sugar
-----------------


There is still one minor issue. This is what our code looks like ::

    out2 = TimesFive.apply(x, y)

It's annoying to write code this way and bug-prone. Also, we promised
that we would have functions that look just like the functions we are
used to writing.

To get around this issue we need to augment the :class:`Scalar` class
to behave normally under standard mathematical operations.  Instead of
calling regular +, Python will call our +.  Once this is done we have
the ability to record and track all the ways that x was used in the
function, while still being able to write ::

    out2 = x * y

To do this the class needs to provide syntax that makes it appear like
a number in its use. To see how this is done be sure to read,
https://docs.python.org/3/reference/datamodel.html#emulating-numeric-types.
