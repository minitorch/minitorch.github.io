====================
Autodifferentiation
====================

.. jupyter-execute::
   :hide-code:

      import sys
      sys.path.append("../")
      sys.path.append("../project/")
      sys.path.append("../project/interface/")
      import minitorch
      from minitorch import ScalarFunction
      sys.path.append("../project/interface/")
      from plots import plot_function
      from drawing import *

In :doc:`scalar`, we have seen that can be used to track the functions
that are used for each variable. We do this by overriding
each function which creates new variables.

We are going to utilize this graph as a way to automatically compute
derivatives of arbitrary python functions. The trick behind this
*autodifferentiation* is to implement the derivative of each invidual function,
and then utilize  the *chain rule*  to compute a derivative for any scale value.


Backward
-----------------------------

In the last section we calculated individual functions `f(x)`.
For each of these functions we are now going to implement a `backward` method
to provide this local derivative information.

The API for backward is to compute :math:`d f'(x)` where :math:`f'(x)` is the
derivative of the function and :math:`d` is a value passed to backward (discussed more below).


For a simple function :math:`f(x) = -x`, we can consult our
derivative rules and get :math:`f'(x) = -1`. Therefore the `backward` is

.. jupyter-execute::

      class Neg(ScalarFunction):
          @staticmethod
          def forward(ctx, x):
              return -x

          @staticmethod
          def backward(ctx, d):
              f_prime = -1
              return f_prime * d


.. jupyter-execute::
   :hide-code:

   draw_boxes(["$d \cdot f'(x)$", "$d$"], [1], lr=False)

Note that `backward` works a bit different than the
mathematical notation. Sometimes the function for the derivative
:math:`f'(x)` depends directly on x; however, `backward` does not take
:math:`x` as an argument. This is where the context arguments `ctx`
comes in.

Consider a function `Sin`, :math:`f(x) = \sin(x)`
which has derivative :math:`f'(x) = \cos(x)`. We need to write it in code as,

.. jupyter-execute::


      class Sin(ScalarFunction):
          @staticmethod
          def forward(ctx, x):
              ctx.save_for_backward(x)
              return math.sin(x)

          @staticmethod
          def backward(ctx, d):
              x, = ctx.saved_values
              f_prime = math.cos(x)
              return f_prime * d


.. jupyter-execute::

   plot_function("f(x) = sin(x)", lambda x: Sin.apply(x).data)


.. jupyter-execute::

   def d_call(x):
        ctx = minitorch.Context()
        Sin.forward(ctx, x)
        return Sin.backward(ctx, 1)

   plot_function("1 * f'(x) = cos(x)", d_call)


For functions that take multiple arguments, `backward` returns
derivatives with respect to each input argument. For example,
if the function computes :math:`f(x, y)`, we need to return
:math:`f'_x(x, y)` and :math:`f'_y(x, y)`

.. jupyter-execute::


      class Mul(ScalarFunction):
          @staticmethod
          def forward(ctx, x, y):
              ctx.save_for_backward(x, y)
              return x * y

          @staticmethod
          def backward(ctx, d):
              # Compute f'_x(x, y) * d, f'_y(x, y) * d
              x, y = ctx.saved_values
              f_x_prime = y
              f_y_prime = x
              return f_x_prime * d, f_y_prime * d

.. jupyter-execute::
   :hide-code:

   draw_boxes([("$d \cdot f_x'(x, y)$", "$d \cdot f_y'(x, y)$"), "$d$"], [1], lr=False)



Chain Rule
-------------

.. note::
   This section discusses implementation of the chain rule for univariate
   differentiation.
   Before reading, review the mathematical definition of `Chain Rule
   <https://en.wikipedia.org/wiki/Chain_rule#Statement>`_ .


Computing backward gives a way to compute the derivative for simple
functions, but what if we have more complex functions? Let's go through
each of the different cases to compute the derivatives.

* One argument
* Two argument
* Same argument


**One argument**


Let us say that we have a complex function :math:`h(x) = f(g(x))`. We
want to compute :math:`h'(x)`. For simplicity we use :math:`z = g(x)`,
and draw :math:`h` as two boxes left to right.

.. jupyter-execute::
   :hide-code:

      draw_boxes(["$x$", "$z = g(x)$", "$f(g(x))$"], [1, 1])


The chain rule tell us how to compute this term. Specifically it gives the
following formula.


.. math::

   \begin{eqnarray*}
   d &=& 1 \cdot f'(z) \\
   h'_x(x) &=&  d \cdot g'(x) \\
   \end{eqnarray*}


The above derivative function tells us to compute the derivative of the
right-most function (:math:`f`), and then multiply it by the derivative of the left function (:math:`g`).

Here is where the perspective of thinking of functions as boxes pays
off. We simply reverse the order.

.. jupyter-execute::
   :hide-code:

      draw_boxes(["$d\cdot g'(x)$", "$f'(z)$", "$1$"], [1, 1], lr=False)


The :math:`d` multiplier passed to `backward` of
the first box (left) should be the value returned by `backward` of the
second box.  The 1 at the end is to start off the chain rule process
with a value for :math:`d_{out}`.

**Two arguments**

Next is the case of a two argument function. We will write this as :math:`h(x, y) = f(g(x, y))` where
:math:`z = g(x,y)`.

.. jupyter-execute::
   :hide-code:

   draw_boxes([("$x$", "$y$"), "$z = g(x, y)$", "$h(x,y))$"], [1, 1])

Applying the chain rule we get the following equations.

.. math::

   \begin{eqnarray*}
   d &=& 1 \cdot f'(z) \\
   h'_x(x, y) &=&  d \cdot g'_x(x, y) \\
   h'_y(x, y) &=&  d \cdot g'_y(x, y) \\
   \end{eqnarray*}


Drawing this again with boxes.

.. jupyter-execute::
   :hide-code:

   draw_boxes([("$d \cdot  g'_x(x, y)$", "$d \cdot g'_y(x, y)$"), "$f'(z)$", "$1$"], [1, 1], lr=False)



Note that this shows that the second box (:math:`f`) does not care how many arguments
the first
box (:math:`g`) has, as long as it passes back :math:`d` which is
enough for the chain rule
to work.

**Multiple Uses**

Finally, what happens when 1 value is used by two future boxes? Next is the case of a two argument function. We will write this as :math:`h(x) = f(z_1, z_2)` where :math:`z_1 = z_2 = g(x)`.


.. jupyter-execute::
   :hide-code:

   draw_boxes(["$x$", ("$z_1 = g(x)$", "$z_2 = g(x)$"), "$h(x))$"], [1, 1])


Derivatives are linear, so the :math:`d` term that comes from the second box is
just the sum of the two individual derivatives.

.. math::

   \begin{eqnarray*}
   d &=& 1 \cdot f'_{z_1}(z_1, z_2) + 1 \cdot f'_{z_2}(z_1, z_2)  \\
   h'_x(x) &=&  d \cdot g'_x(x) \\
   \end{eqnarray*}


Specifically in terms of boxes, this means that if an output is used multiple times,
we should sum together the derivative terms. This rule is important, as it means that we
cannot call backward until we have aggregated together all the values that we need to calculate :math:`d`.

.. jupyter-execute::
   :hide-code:

   draw_boxes(["$d \cdot g'_x(x)$", ("$f'_{z_1}(z_1, z_2)$", "$f'_{z_2}(z_1, z_2)$"), "$h1$"], [1, 1], lr = False)
