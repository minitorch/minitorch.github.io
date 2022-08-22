=============
Contributing
=============


*The Minitorch codebase is structured to mimic the experience of
contributing to a real open-source project. It is not sufficient to
implement functions correctly; the code itself needs to meet the specific
contributor requirements. These are checked by the system automatically before
acceptance.*

Style
------

It is required to keep your code organized and clean to make it easier
to debug, optimize, and document. To help with this process, we
utilize required formatting on all assignments.

Fixing style bugs can be an annoying process. However, there are now tools
to fix most formatting issues automatically. We use `black` to automatically
reformat
all of your code to fit most of the requirements (see
https://github.com/psf/black for
more details):

>>> black .

Black will fix many of your issues, but cannot check for aspects
like using unknown variables.  You will also need to run the `flake8`
linter in your directory to check for remaining issues:

>>> flake8


We recommend setting up your editor or IDE to highlight other style
issues. Many developers utilize VSCode with plugins to check for these
issues as they code.



Testing
--------------

Each assignment has a series of tests that require your code to pass.
These tests are in the `tests/` directory and are in the `pytest`
format (https://docs.pytest.org/en/stable/). Any function in that
directory starting with `test_`  is run as part of the test
suite.

>>> pytest

Each assignment has 4 task groups that you will need to pass. To run
individual task groups you can use the `-m` option.

>>> pytest -m task0_0

In addition to running a full task which runs all of the tests, you can run
tests in a single file with:

>>> pytest tests/test_operators.py

Or even a particular test with:

>>> pytest tests/test_operators.py -k test_sum

Note: Pytest will hide all print statements unless a test fails. If you want to
see output for a given tests you may need to cause an assertion failure.


Documentation
--------------

Throughout the codebase, we require to document all functions in a
standardized style. Documentation is critical for our Python codebase, and
we use it to convey requirements on many functions.
Functions should have docstrings in the following form (known as Google
docstyle): ::


  def index(ls, i):
      """
      List indexing.

      Args:
          ls (list): A list of any type.
          i (int): An index into the list

      Returns:
          Value at ls[i].
      """
      ...


A full description of this docstyle is listed here
https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html.

The project also requires that you keep documentation up-to-standard
throughout.  Lint errors will be thrown by `flake8` if your documentation is in
the incorrect format.

Type Checking
--------------





Continuous Integration (CI)
-----------------------------

In addition to local testing, the project is set up such that on each
code push,
tests are automatically run and checked on the server. You are able to see
how well you are doing on the assignment by committing your code, pushing
to the server,
and then logging in to GitHub. This process takes several minutes, but it
is an easy way to
keep track of your progress as you go.

Specifically, you can run:

>>> git commit -am "First commit"
>>> git push origin master

Then go to your GitHub and click on "Pull requests". Clicking on the
request itself gives a link to show the current progress of your
work.
