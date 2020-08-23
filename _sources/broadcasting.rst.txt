===================
Broadcasting
===================

Tensors have one final superpower that makes them convenient and
efficient to use. This comes in handy particularly for `zip` operations.
So far all of our `zip` operations have assumed that we had two
tensors of **exactly** the same size and shape. However there are many
times when it is interesting to `zip` two tensors are different size.

Perhaps the simplest case is when we have one size-3 vector (1-D tensor) and want to add a
scalar constant to every position ::

  # In math notation, vector1 + 10
  vector1 + tensor([10])

We would like for this operation to have the standard vector+scalar
interpretation of adding 10 to each position.  But here we have a
tensor of size 1 and shape (1,) and `vector1` is of shape (3,).
Because of this mismatch, a simple `zip` will fail.


We could ask users to instead create a tensor of this size. However this both
annoying, and more importantly inefficient. ::

  vector1 + tensor([10, 10, 10])


`Broadcasting` is a protocol that lets us interpret the top operation as implying
the bottom one automatically. That is inside `zip` we pretend that 10 is a vector of
shape (3,) when it is zipped with a vector of size 3. Again, we never actually create this tensor. This is just an interpretation.


This gives us our first rule of broadcasting:

.. note::

   **Rule 1**: Any dimension of size 1, can be zipped with dimensions of size n > 1 by assuming the dimension  is copied n times.


Now let's apply this approach to a matrix of shape (4, 3). ::

    matrix1 + tensor([10])


Here we are trying to zip a matrix (2-D) of shape (4, 3) with a vector
(1-D) of shape (1,). Here we are not just off on the shape, but also on
the number of dimensions.

However, recall that adding an extra dimension of shape-1 doesn't change
the size of the tensor. Therefore we can allow our protocol to add
these in.  Here if we add an empty dimension and then apply rule 1
twice we can interpret this statement as an efficient version of ::

    matrix1 + tensor([10] * 12, shape=(4, 3))



.. note::
   **Rule 2**: Extra dimensions of size 1 can be added to a tensor to ensure that the dimensions are the same.


Finally there is a question of where to add the empty dimensions. This
is not an issue in the above case but becomes an issue in more
complicated cases. ::

  # These two lines are equivalent
  matrix1 + vector1
  matrix1 + vector1.view(1, 3)

.. note::
   **Rule 3**: Any extra dimensions of size 1 can only be added on the left-side of the shape.

This rule has the impact of making the process easy to follow and replicate. You always know what the shape of the final
output will be. For instance, ::

  # This will fail (4, 3) (4,)!!
  matrix1 + vector2.view(4)




  
We that we can use the broadcasting rules and many times as we want in a given setting:  ::

  # This will return shape (3, 2)
  tensor1.view(1, 2) + tensor2.view(3, 2)

  
.. image:: figs/Ops/zip\ broad.png
           
.. image:: figs/Ops/zip\ broad\ back.png

You can even have more complicated examples.   ::

  # This will return shape (7, 2, 3, 5)
  tensor1.view(2, 3, 1) + tensor2.view(7, 2, 1, 5)


Finally we end with two notes:

1) Broadcasting is **only** about shapes. It does not take strides into account in any way. It is purely a high-level protocol.

2) Broadcasting has some impact on the backward pass. We discuss some of this in the code base, but it is not required for any of the tasks.

  

