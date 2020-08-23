
====================
Tensor Variables
====================

Next we consider autodifferentiation in the tensor framework. We have
now moved from scalars and derivatives to vector, matrices, and
tensors.  This means `multivariate calculus` and can bring into play
somewhat scary terminology. However, most of what we actually need to
do will not require complicated terminology or much technical math. In
fact, excepting some name changes, we have already built almost
everything we need in :doc:`module1`.

The key idea is that just as we had `Scalar` and `ScalarFunction`, we need to
construct a `Tensor` and `TensorFunction` (which we just call `Function`).
These new objects behave very similar to their counterparts:

a) Tensors cannot be operated on directly, but need to be transformed through a Function.
b) Functions must implement both a forward method and also a backward method.
c) These transformations are tracked, which allow backpropagation through the chain-rule. 

All of this machinery should work out of the box. 


The main new terminology to know is `gradient`. Just as a tensor is a
multidimensional array of scalars, a gradient is a multidimensional
array of derivatives for these scalars. ::


  # Assignment 1 notation
  out = f(a, b, c)
  out.backward()
  (a.derivative, b.derivative, c.derivative)


  # Assignment 2 notation
  tensor1 = tensor(a, b, c)
  out = g(tensor1)
  out.backward()

  # shape (3,)
  tensor1.grad

The gradient of `tensor1` is a tensor that holds the derivatives of
each of its values. The other place that gradients come into play is
that backward no longer takes :math:`d_{out}` as an argument, but now
takes :math:`grad_{out}`. Again, this is just a tensor of all the
:math:`d_{out}` corresponding to the output tensor.


.. note::
   (You will find lots of different notation for
   gradients and multivariate terminology. For this assignment, I ask
   that you ignore it and stick to everything you know about derivatives.
   It turns out that you can do most of machine learning without ever
   thinking in higher dimensions.)

If you think about a gradient and :math:`grad_{out}` in this way (tensor of derivatives :math:`d_{out}`),
you can then see how we can easily compute the gradient of each tensor
operations be using univariate rules.
   

1) **map**. Given a tensor, map applies a univariate operation to each scalar
   position individually. For a scalar :math:`x`, it computes
   :math:`g(x)`.  Therefore, from assignment 1, we know that the
   derivative :math:`f(g(x))` is equal to :math:`g'(x) \times d_{out}`. This
   means to compute the backward gradient, we only need to compute the
   derivative for each position and apply a `mul` map.


.. image:: figs/Ops/map\ back.png
           :align: center
                   
2) **zip**. Given two tensors, zip applies a fixed operation to each
   scalar position as a pair. For two scalars :math:`x` and
   :math:`y`, it computes :math:`g(x, y)`.  Therefore, from assignment
   1, we know that the derivative :math:`f(g(x, y))` is equal to
   :math:`g_x'(x, y) \times d_{out}` and :math:`g_y'(x, y) \times d_{out}`. This
   means to compute the gradient, we only need to compute the
   derivative for each position and `mul` map.

.. image:: figs/Ops/zip\ back.png
           :align: center
                   
3) **reduce**. Given a tensor, reduce applies a fixed aggregation
   operation to one dimension. For simplicity, let's consider sum-based
   reductions.  For scalars :math:`x_1` to :math:`x_n`, it computes
   :math:`x_1 + x_2 + \ldots`.  For any :math:`x` value this
   yields 1. Therefore, the derivative for any position is simply the
   derivative passed backward :math:`d_{out}`. This means to compute the
   gradient, we only need to send the derivative to each
   position. (For other reduce operations such as `product`, you get
   different expansions, but these can be calculated just by taking
   derivatives).

.. image:: figs/Ops/reduce\ back.png
           :align: center
