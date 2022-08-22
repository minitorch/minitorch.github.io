..
  done

===========================
Property Testing
===========================

Testing and debugging are critical for software engineering in
general, and particularly necessary for framework code that will be
used in unexpected ways. Unfortunately, machine learning code is
notoriously hard to test and debug. Many practitioners seem to just
run models and wait until they are trained before starting the
debugging process.

But how do you effectively test mathematically oriented code?
Unlike many software projects where unit tests can cover
most of the input cases, mathematical functions make this impossible.


For example, let's say you have a function that is meant
to add two numbers (this sounds really silly, but we will see it is
not)::

    def add(a, b):
        "Super-efficient specialized integer add function"
         ...


A (somewhat naive) unit test might look like this::

    def test_add_basic():
        # Check same as slow system add
        assert add(10, 5) == 10 + 5
        # Check that order doesn't matter
        assert add(10, 7) == add(7, 10)

This is fine, and certainly can help catch easy bugs, but it is not
very reassuring. It is particularly devastating when your code
has been running for 20 hours, and then encounters some cases where your
add function fails.

An alternative idea is to test properties instead of specific
cases. That is, check if key aspects of the expected behavior always hold. For
instance, you might imagine directly checking if these properties
hold for every pair of integers: ::

    def test_add_naive():
        for a in range(-10000, 10000):
            for b in range(-10000, 10000)
                 assert add(a, b) == a + b
                 assert add(a, b) == add(b, a)


This provides better coverage, but is also naive and clearly
hopelessly inefficient. Unit tests are supposed to be quick easy
snippets of code that can be run quickly while developing.

A clever middle ground is to use `randomized` property checking. This
method was popularized by a library called QuickCheck
(http://wikipedia.org/wiki/quickcheck). This approach randomly selects
interesting inputs in order to test your codebase's correctness. It
gives you the speed of the first approach and some of the breadth of
the second. Another nice benefit of randomized property checking is that it
actually makes tests shorter and easier to write since it generates
cases for you.

In MiniTorch, we will use a fantastic property checking library in
Python called `Hypothesis`
(https://hypothesis.readthedocs.io/). Hypothesis predefines a whole
set of building block `strategies` that the user can pick from when
writing tests. (You can also write your strategies, which you will
do in the next assignment.)
You can generate integers, floats, lists, strings, etc.
Each test can be `decorated` with values that it operates on::

    from hypothesis.strategies import integers
    from hypothesis import given
    @given(integers(), integers())
    def test_add(a, b):
        # Check same as slow system add
        assert add(a, b) == a + b
        # Check that order doesn't matter
        assert add(a, b) == add(b, a)

