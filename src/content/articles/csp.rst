Constraint Satisfaction Problem (CSP)
#####################################

:summary: A mathematical question that is defined by variables, domains, and constraints
:date: 2019-07-22 12:05:21
:category: note
:tags: cs, programming, ai
:slug: csp

`Constraint Satisfaction Problem`_ (CSP) is a class of problems that can be used to represent a large set of real-world problems. In particular, it is widely used in Artificial Intelligent (AI) as finding a solution for a formulated CSP may be used in decision making. There are `a few adjacent areas`_ in terms that for solving problems they all involve *constraints*: `SAT (Boolean satisfiability problem), and the SMT (satisfiability modulo theories)`_.

|

Generally speaking, the complexity of finding a solution for CSP is `NP-Complete`_ (takes exponential time), because a solution can be guessed and *verified* relatively fast (in polynomial time), and the SAT problem (`NP-Hard`_) can be translated into a CSP problem. But, it also means, there is no known polynomial-time *solution*. Thus, the `development of efficient algorithms and techniques for solving CSPs is crucial`_ and appears as a subject in many scientific pieces of research.

|

`The simplest kind of CSPs`_ are defined by a set of *discrete variables* (e.g. X, Y), *finite non-empty domains* (e.g.  0<X<=4, Y<10), and a set of *constraints* (e.g. Y=X^2, X<>3) which involve some of the variables. There are distinguished two related terms: the *Possible World* (or the *Complete Assignment*) of a CSP is an assignment of values to all variables and the *Model* (or the *Solution* to a CSP) is a possible world that satisfies all the constraints.

|

Within the topic, there is a programming paradigm - `Constraint Programming`_. It allows building a `Constraint Bases System`_ where relations between variables are stated in a form of constraints. Hence, this defines certain specifics: 

- the paradigm doesn't tell a certain sequence of steps to execute to find a solution, but rather declares the solution's properties.
- it's usually characterized by non-directional computation when to satisfy constraints, computations are propagated through a system accordingly to changed conditions or variables' values.

|

A CSP can be applied in solving many real-world problems in a number of areas like mappings, assignments, planning and scheduling, games (e.g. sudoku), solving system of equations, etc. There are also a few software frameworks, like `python-constraint`_ and `Google OR-Tools`_, just to name a few.

.. Links

.. _`Constraint Satisfaction Problem`: https://en.wikipedia.org/wiki/Constraint_satisfaction_problem
.. _`development of efficient algorithms and techniques for solving CSPs is crucial`: http://www.cs.toronto.edu/~fbacchus/Papers/liu.pdf
.. _`NP-Complete`: https://stackoverflow.com/a/127831/5673383
.. _`NP-Hard`: https://stackoverflow.com/a/313523/5673383
.. _`a few adjacent areas`: http://crest.cs.ucl.ac.uk/readingGroup/satSolvingTutorial-Justyna.pdf
.. _`SAT (Boolean satisfiability problem), and the SMT (satisfiability modulo theories)`: https://yurichev.com/writings/SAT_SMT_by_example.pdf
.. _`The simplest kind of CSPs`: http://aima.cs.berkeley.edu/newchap05.pdf
.. _`Constraint Programming`: https://en.wikipedia.org/wiki/Constraint_programming
.. _`Constraint Bases System`: https://composingprograms.com/pages/24-mutable-data.html#propagating-constraints
.. _`python-constraint`: https://labix.org/python-constraint
.. _`Google OR-Tools`: https://developers.google.com/optimization/
