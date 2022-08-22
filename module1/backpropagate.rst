======================
Backpropagation
======================

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


The `backward` function tells us how to compute the derivative of one
operation.  The chain rule tells us how to compute the derivative of two
sequential operations.  In this section, we show how to use these to
compute the derivative for an arbitrary series of operations.

Practically this looks like re-running our graph in reverse order from
right-to-left. However, we need to ensure that we do this in the
correct order. The key implementation challenge of backpropagation is
to make sure that we process each node in the correct order, i.e.
we have first processed every node that uses a Variable before that
varible itself.


Running Example
---------------


Assume we have Variables :math:`x,y` and a Function :math:`h(x,y)`. We want
to compute the derivatives :math:`h'_x(x, y)` and :math:`h'_y(x, y)`.

.. math::

   \begin{eqnarray*}
   h(x, y) &=& \log(z) + \exp(z) \\
      \text{where} && z = x \times y \\
   \end{eqnarray*}

We assume x, +, log, and exp are all implemented as simple
functions. This means that the final output Variable has constructed a
graph of its history that looks like this:

.. jupyter-execute::
   :hide-code:

   draw_boxes([("$x$", "$y$"), "", "", "$h(x, y)$"], [1, 2, 1], lr=True)

Here, starting from the left, the first arrows represent inputs
:math:`x,y`, the left node outputs :math:`z`, the top node
:math:`\log(z)`, the bottom node :math:`\exp(z)` and the final right
node :math:`h(x, y)`. Forward computation proceeds left-to-right.


The chain rule tells us methods for propagating the derivatives. We
can use the rules from the previous section right-to-left until we reach
the initial Variables :math:`x,y`, i.e. the `leaf` Variables.





Topological Sort
-----------------

We could just apply these rules randomly and process each nodes as they
come aggregating the resulted values. However this can be quite inefficient.
It is better to wait to call `backward` until we have accumulated all the
values we will need.


To handle this issue, we will process the nodes in `topological
order`.  We first note that our graph is directed and that acyclic.
Directionality comes from the `backward` function, and the lack of
cycles is a consequence of the choice that every Function must create a
new variable.

The topological ordering of a directed acyclic graph is an ordering
that ensures no node is processed after its ancestor, e.g. in our
example that the left node cannot be processed before the top or
bottom node. The ordering may not be unique, and it does not tell us
whether to process the top or bottom node first.

There are several easy-to-implement algorithms for topological sorting.
As graph algorithms are beyond the scope of this document, we recommend
using the depth-first search algorithm described in pseudocode section of
`Topological Sorting <http://wikipedia.org/wiki/Topological_sorting>`_.


Backprop
----------

Once we have the order defined, we process each node one at a time in order.
We start the rightmost node (:math:`h(x,y)`) with red arrow
in the graph below. The starting derivative is an argument given to us.

.. jupyter-execute::
   :hide-code:

   backprop(1)



We then process the Function with the chain rule. This calls
`backward` of +, and gives the derivative for the two red Variables
(which correspond to :math:`\log(z), \exp(z)` from the `forward`
pass). You need to track these intermediate red derivative values in a
dictionary.


.. jupyter-execute::
   :hide-code:

   backprop(2)


Let us assume the next Variable in the order is the top node. We have
just computed and stored the necessary derivative :math:`d_{out}`, so
we can apply the chain rule. This produces a new derivative (corresponding to
:math:`z`: left red arrow below) for us to store.


.. jupyter-execute::
   :hide-code:

   backprop(3)

The next Variable in the order is the bottom node. Here we have an
interesting result. We have a new arrow, but it corresponds to the
same Variable (:math:`z`) that we just computed. It is is a useful
exercise to show that as a consequence of the two argument chain rule
that the derivative for this Variable is the sum of each of these
derivatives. Practically this means just adding it to your dictionary.

.. jupyter-execute::
   :hide-code:

   backprop(4)


After working on this Variable, at this point, all that is left in the
is our input leaf Variables.


.. jupyter-execute::
   :hide-code:

   backprop(5)


When we reach the leaf Variables in our order, for example
:math:`x`, we store the derivative with that Variable.
Since each step of this process is an application of the chain rule, we can
show that this final value
is :math:`h'_x(x, y)`. The next and last step is to compute :math:`h'_y(x, y)`.


.. jupyter-execute::
   :hide-code:

   backprop(6)


By convention, the variables :math:`x, y` have their derivatives stored as::

  x.derivative, y.derivative




Algorithm
----------

As illustrated in the graph for the above example, each of the red
arrows represents a constructed derivative which eventually passed to
:math:`d_{out}` in the chain rule.  Starting from the rightmost arrow,
which is passed in as an argument, backpropagate should run the
following algorithm:


0. Call topological sort to get an ordered queue
1. Create a dictionary of Variables and current derivatives
2. For each node in backward order, pull a completed Variable and
   derivative from the queue:

   a. if the Variable is a leaf, add its final derivative (`accumulate_derivative`)
      and loop to (1)
   b. if the Variable is not a leaf,

      1) call `.backprop_step` on the last function that created it with
         derivative as :math:`d_{out}`
      2) loop through all the Variables+derivative produced by the chain
         rule
      3) accumulate derivatives for the Variable in a dictionary
         (check `.unique_id`)


Final note: only leaf Variables should ever have non-None
`.derivative` value. All intermediate Variables should only keep
their current derivative values in the dictionary. This is a
bit annoying, but it follows the behavior of PyTorch.
