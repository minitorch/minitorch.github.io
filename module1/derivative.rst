=============
Derivatives
=============

Let's begin by discussing derivatives in the setting of
programming. We assume that you have not seen derivatives in a while,
so we will start slow and develop some notation first.


Symbolic Derivatives
---------------------

.. jupyter-execute::
   :hide-code:

   import sys
   sys.path.append("../")
   import minitorch
   sys.path.append("../project/interface/")
   from plots import plot_function, plot_function3D
   import math
   from chalk import *

   def function(f, l=-1., r=1.):
       x = [l + (r - l) * i / 100 for i in range(100)]
       xy = [(i, -f(i)) for i in x]
       q = make_path(xy).line_width(0.05)
       return q

Assume we are given a function,

.. math ::

   f(x) = \sin(2 x)

.. jupyter-execute::

   def f(x):
      return math.sin(2 * x)

   plot_function("f(x) = sin(2x)", f)


We can compute a function for its derivative by applying rules from univariate
calculus.
We will use "Lagrange" notation where the derivative of a one-argument
function :math:`f'`
as is denoted :math:`f'`. To compute :math:`f'` we can apply standard univariate
derivative rules.

.. math ::

    f'(x) = 2 \times \cos(2 x)

.. jupyter-execute::

   def d_f(x):
      return 2 * math.cos(2 * x)

   plot_function("f'(x) = 2 cos(2x)", d_f)

We also will work with two-argument functions.


.. math ::

   \begin{eqnarray*}
   f(x, y) &=& \sin(x) + 2 \cos(y) \\
   \end{eqnarray*}



.. jupyter-execute::

   def f(x, y):
      return math.sin(x) + 2 * math.cos(y)

   plot_function3D("f(x, y) = sin(x) + 2 * cos(y)", f)

We use a subscript notation to indicate which argument we are taking
a derivative with respect to.

.. math ::

   \begin{eqnarray*}
   f'_x(x, y) &=& \cos(x)\\
   f'_y(x, y) &=& -2 \sin(y) \\
   \end{eqnarray*}


.. jupyter-execute::

   def d_f_x(x, y):
      return math.cos(x)

   plot_function3D("f'_x(x, y) = cos(x)", d_f_x)

In general, we will refer to this process of mathematical
transformation as the `symbolic` derivative of the function. When
available symbolic derivatives are ideal, they tell us everything we
need to know about the derivative of the function.

Numerical Derivatives
---------------------

Visually, derivative functions correspond to slopes of tangent lines in
2D. Let's
start with this simple function:

.. math ::

   f(x) = x^2 + 1


.. jupyter-execute::

   def f(x):
      return x * x + 1.0

   plot_function("f(x)", f)



Its derivative at an arbitrary input is the slope of the line tangent to
that input.

.. math ::

   f'(x) = 2x

.. jupyter-execute::

   def d_f(x):
      return 2 * x

   def tangent_line(slope, x, y):
      def line(x_):
         return slope * (x_ - x) + y
      return line

   plot_function("f(x) vs f'(2)", f, fn2=tangent_line(d_f(2), 2, f(2)))


The above visual representation motivates an alternative
approach to estimate a `numerical` derivative. The underlying
assumption is that we assume we do not know the symbolic form of the
function, and instead want to estimate it by querying specific values.


Recall one definition of the derivative function is this slope as we approach to a tangent line:

    .. math ::

        f'(x) = \lim_{\epsilon \rightarrow 0} \frac{f(x + \epsilon) -
        f(x)}{\epsilon}


If we set :math:`epsilon` to be very small, we get an approximation of the
derivative function:

    .. math ::

         f'(x) \approx  \frac{f(x + \epsilon) - f(x)}{\epsilon}


Alternatively, you could imagine approaching x from the other side, which
would yield a different derivative function:

    .. math ::

        f'(x) = \lim_{\epsilon \rightarrow 0} \frac{f(x) - f(x-
        \epsilon)}{\epsilon}


You can show that doing both simultaneously yields a better approximation
(you probably proved this in high school!):


    .. math ::

         f'(x) \approx  \frac{f(x + \epsilon) - f(x-\epsilon)}{2\epsilon}


.. image:: figs/Grad/approx.png
           :align: center


.. jupyter-execute::

   eps = 1e-5
   slope = (f(2 + eps) - f(2 - eps)) / (2 * eps)
   plot_function("f(x) vs f'(2)", f, fn2=tangent_line(slope, 2, f(2)))



This formula is known as the `central difference`, and is a
specific case of `finite differences <https://en.wikipedia.org/wiki/Finite_difference>`_.


When working with functions of multiple arguments. The each derivative corresponds to the slope of one dimension of the tangent plane. The central difference approach can only tell us one of these slope at a time.

Specifically we would need to compute,

.. math ::

   \begin{eqnarray*}
    f'_x(x, y) &\approx&  \frac{f(x + \epsilon, y) - f(x-\epsilon, y)}{2\epsilon} \\
    f'_y(x, y) &\approx&  \frac{f(x,  y + \epsilon) - f(x, y -\epsilon)}{2\epsilon}
   \end{eqnarray*}

The more variables we have, the more function calls we need to make.


Implementing Numerical Approximations
---------------------------------------

The key benefit of the `numerical` approach is that we do not need to
know everything about the function: all we need is to able to compute
its value under a given input. From a programming sense, this means we
can approximate the derivative for any black-box function. Note, we
did not need to actually know the specifics of the function to compute
this derivative.


In implementation, it means we can write a `higher-order function` of the
following form::

    def central_difference(f, x):
        ...


Assume we are just given an arbitrary python function::

      def f(x):
          "Compute some unknown function of x."
          ...

we can call central_difference(f,x) to immediately approximate the derivative
of this function f on input x.

We will see that this approach is not a great way to train machine learning
models, but
it provides a generic alternative approach to check if your derivative
functions are correct, e.g. free :doc:`property_testing`.


Here are some examples of Module-0 functions with central difference applied. It is important to know what derivatives of these important functions look like.

.. jupyter-execute::

   plot_function("sigmoid", minitorch.operators.sigmoid)

.. jupyter-execute::

   def d_sigmoid(x):
       return minitorch.central_difference(minitorch.operators.sigmoid, x)

   plot_function("Derivative of sigmoid", d_sigmoid)


.. jupyter-execute::

   plot_function("exp", minitorch.operators.exp)

.. jupyter-execute::

   def d_exp(x):
       return minitorch.central_difference(minitorch.operators.exp, x)

   plot_function("Derivative of exp", d_exp)



.. jupyter-execute::

   plot_function("ReLU", minitorch.operators.relu)

.. jupyter-execute::

   def d_relu(x):
       return minitorch.central_difference(minitorch.operators.relu, x)

   plot_function("Derivative of ReLU", d_relu)
