..
  done

========
Modules
========

.. jupyter-execute::
   :hide-code:

      import sys
      sys.path.append("../")

Researchers often disagree on exactly what the term `deep` learning
means, but one aspect that everyone agrees on is that deep
models are big and complex.  Common models can include hundreds of
millions of learned `parameters` that span over hundreds of informal
`module` groups.  In order to work with such complex systems, it is
important to have data structures which abstract away the complexity
so that it is easier to access and manipulate specific components, and
group together shared regions.


On the programming side, `Modules` have become a popular paradigm to
group parameters together to make them easy to manage, access, and
address.  There is nothing specific to machine learning about this
setup (and everything in MiniTorch could be done without modules), but they
make life easier and code more organized.

First, let's define a Parameter. For now, we will just think of Parameter
as a holder. It is just a special object that stores a value.


.. autoclass:: minitorch.Parameter



Parameters become more interesting when they are grouped with
`Modules`. Modules provide a way of storing and finding these
parameters. Let's look at the `Module` class to see how this works.


Modules are a recursive tree-shaped data structure. Each module can
store three things: 1) parameters, 2) non-parameter data, 3) other
modules. Internally, the user stores each of these directly on `self`,
but the module spies under the hood to determine the type of each
assignment.

Here is an example of the simplest usage of a module

.. jupyter-execute::

      from minitorch import *
      class OtherModule(Module):
          pass

      class MyModule(Module):
          def __init__(self, arg):
              # Initialize the super-class (so it can spy)
              super().__init__()

              # A parameter member (subclass of Parameter)
              self.parameter1 = Parameter(15)

              # A non-parameter member
              self.data = 25

              # A module member (subclass of Module)
              self.sub_module = OtherModule(arg, arg+10)

.. warning::
   All subclasses must begin their initialization by calling ::

     super().__init__()

   This allows the module to capture any members of type :class:`Module`
   or :class:`Parameter`
   and store them in a special dictionary.


Internally, parameters (type 1) are stored in :attr:`_parameters`, data
(type 2)
is stored on `self`, modules (type 3) are stored in :attr:`_modules`.


The main benefit of this infrastructure is that it allows us to
`flatten` a module to get out all of its parameters using
:func:`named_parameters`. This returns a dictionary of all of the
parameters in the module and in all descendent sub-modules. The names
here refer to the keys in the dictionary which give the path to each
parameter in the tree (similar to python dot notation). Critically
this function does not just return the current module's parameters, but
recursively
collects parameters from all the modules below as well.


Here is an example of how you can create a tree of modules and then
extract the flattened parameters

.. jupyter-execute::

      class Module1(Module):
          def __init__(self):
              super().__init__()
              self.p1 = Parameter(5)
              self.a = Module2()
              self.b = Module3()

      class Module2(Module):
          def __init__(self):
              super().__init__()
              self.p2 = Parameter(10)

      class Module3(Module):
          def __init__(self):
              super().__init__()
              self.c = Module4()

      class Module4(Module):
          def __init__(self):
              super().__init__()
              self.p3 = Parameter(15)

      np = dict(Module1().named_parameters())
      assert np["b.c.p3"].value == 15

.. image:: figs/Module/module.png

Additionally, a module can have a :attr:`mode` indicating how it is
currently operated. The mode should propagate to all of its
child modules. For simplicity, we only consider the train and eval mode.

.. autoclass:: minitorch.Module
