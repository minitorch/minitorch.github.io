
.. raw:: html

   <link rel="stylesheet" href="_static/revealjs/css/theme/white.css">
   <link rel="stylesheet" href="_static/default.css">


Machine Learning Engineering
=============================================

 


Lecture 2
------------

  Beginnings


Survey
---------

.. revealjs_fragments::

   * Thanks so much for filling out the survey
   * Link: https://forms.gle/MZQ9akwr18PpR1zD9
   * Please fill out this week!

Today's Class
----------------

.. revealjs_fragments::

   * Module 0
   * Development Setup
   * Testing and Hypothesis
   * Functional Python

The Guidebook
--------------

.. revealjs_fragments::

   * https://minitorch.github.io/
   * Full description of the material


Module 0: Fundamentals
-----------------------

Learning Goals:

.. revealjs_fragments::

   * Basic functions (start slow)
   * Testing
   * Visualization
   * No ML yet! We'll get to it.

Code Setup: Interactive
=========================
     
GitHub
---------

.. revealjs_fragments::

   * http://github.com/
   * Important: Link your Cornell email to your Github.  
  


Base Repo Template
--------------------

.. revealjs_fragments::
   
   * Each repo starts with a template 
   * https://github.com/minitorch/Module-0


Tour of Repo
------------------

.. revealjs_fragments::

   * minitorch/
   * tests/
   * project/



     
GitHub Classroom
------------------

.. revealjs_fragments::

   * First assignment link
   * https://classroom.github.com/a/BQeMj6RP


       

Recommendations 
-------------------------


* PyCharm
* Sublime
* Emacs
* Repl.it
     

   

Contributing Guidelines
=========================

Style
------

* Configure your development environment to check for style errors ::

   >>> black minitorch/ tests/ project/

* Corrects and formats your code


Continuous Integration
--------------------------


* Runs behind the scenes on every commit.

.. image:: https://classroom.github.com/images/help/autograding/actions-logs.png
     
Documentation
-----------------

Doc style (`Google <https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html>`_) ::

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

  

Q&A
======
