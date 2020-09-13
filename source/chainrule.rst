====================
Autodifferentiation
====================

So far, we have seen that  :class:`ScalarFunction`  can be used to
implement functions on variables. We do this by calling `apply` on
variables, which then calls the underlying `forward` method of
the function.


Now, we include additional information on the class that gives the
derivative of the individual function. The trick behind autodifferentiation
is to use this  `chain` of function calls to compute a derivative.
Just like forward calculates the function `f(x)`, we need a function backward
to provide this local derivative information.



Backward
-----------------------------

For every Function, we need to provide a backward method to compute its derivative
information. Specifically backward will compute :math:`f'(x) \times d_{out}` where
:math:`d_{out}` is an argument passed in (discussed below).

For the simple function :math:`f(x) = x \times 5`, we can consult our
derivative rules and get that :math:`f'(x) = 5`. Therefore the backward
function is ::


      class TimesFive(ScalarFunction):
          @staticmethod
          def forward(ctx, x):
              return x * 5

          @staticmethod
          def backward(ctx, d_out):
              f_prime = 5
              return f_prime * d_out


.. image:: figs/Autograd/autograd3.png
           :align: center


For functions that take multiple arguments, we return
multiple backward arguments for each of the inputs. If the function computes
:math:`f(x, y)`, we need to return :math:`f'_x(x, y)` and :math:`f'_y(x, y)` ::

      class GFunction(ScalarFunction):
          @staticmethod
          def forward(ctx, x, y):
              # Compute f(x, y)
              ...

          @staticmethod
          def backward(ctx, d):
              # Compute f'_x(x, y) * d, f'_y(x, y) * d,
              ...

.. image:: figs/Autograd/autograd4.png
           :align: center

For example for :math:`f(x, y) = x + 2 \times y`, we can consult our
derivative rules and get that :math:`f'_x(x, y) = 1` and :math:`f'_y(x, y) = 2`. Therefore the backward
function is ::


      class AddTimes2(ScalarFunction):
          @staticmethod
          def forward(ctx, x, y):
              return x + 2 * y

          @staticmethod
          def backward(ctx, d_out):
              return d_out, 2 * d_out


Note though that `backward` works a bit different than the
mathematical notation. Sometimes the function for the derivative
:math:`f'(x)` depends directly on x; however, `backward` does not take
:math:`x` as an argument. This was not a problem for the functions
above, but things get a bit more interesting when the derivative also
depends on :math:`x` itself. This is where the context arguments `ctx`
comes in.

Consider a function `Square`, :math:`f(x) = x^2` that squares x.
Its derivative :math:`f'(x) = 2x` which we write as ::


      class Square(ScalarFunction):
          @staticmethod
          def forward(ctx, x):
              ctx.save_for_backward(x)
              return x * x

          @staticmethod
          def backward(ctx, d_out):
              x = ctx.saved_values
              f_prime = 2 * x
              return f_prime * d_out

This function style requires that we explicitly save anything that in
the `forward` function we save anything we might need for the backward
function explicitly. This is an optimization that limits the amount of
storage this process requires.


Chain Rule
-------------

.. note::
   This section discusses implementation of the chain rule for univariate differentiation.
   Before reading, review the mathematical definition of the `Chain Rule <https://en.wikipedia.org/wiki/Chain_rule#Statement>`_ .


The above section gives the formula for running backwards on one function.
But we need to run backward on two functions in sequence.

.. image:: figs/Autograd/chain1.png
           :align: center

We can do this using the univariate chain rule, given by,


.. math ::

    f'_x(g(x)) = g'(x) \times f'_{g(x)}(g(x))


Our notation gets a bit hard to follow here, it may be easier to
understand if we name each part.

.. math::

   \begin{eqnarray*}
   y &=& g(x) \\
   d_{out} &=& f'(y) \\
   f'_x(g(x)) &=&  g'(x) \times d_{out} \\
   \end{eqnarray*}


This function tells us that to compute the derivative of the first function,
times the  derivative of the second function with respect to the output the
first function.

Here's where the perspective of the boxes comes in handy:

.. image:: figs/Autograd/chain2.png
           :align: center

This shows that the :math:`d_{out}` multiplier passed to backwards of the
first box, should be the value returned by backwards of the second box.


A similar approach works for  functions two variables,

.. math::

   \begin{eqnarray*}
  f'_x(g(x, y)) &=& g_x'(x, y) \times f'_{g(x, y)}(g(x, y)) \\
  f'_y(g(x, y)) &=& g_y'(x, y) \times f'_{g(x, y)}(g(x, y))
  \end{eqnarray*}

Or

.. math::

   \begin{eqnarray*}
   z &=& g(x, y) \\
   d_{out} &=& f'(z) \\
   f'_x(g(x, y)) &=& d_{out} \times g_x'(x, y) \\
   f'_y(g(x, y)) &=& d_{out} \times g_y'(x, y)
   \end{eqnarray*}

This shows that the second box does not care how many arguments the first
box had, as long as it passes back :math:`d_{out}` that is enough for the chain rule
to work.
