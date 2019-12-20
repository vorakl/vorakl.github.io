Algorithm is...
###############

:summary: Common properties of algorithms
:date: 2019-12-15 16:58:11
:category: note
:tags: cs, mindmap
:slug: algorithm

Despite the obvious expectation to find some sort of a definition of the term
*"Algorithm"* here, I have to disappoint you, as there isn't any general or
well-accepted definition. But, it's not a unique situation! Take mathematics,
for example. Although there are plenty of different "definitions" that can be
found in the literature, they all are just oversimplified attempts to explain
what an algorithm really means.

|

In general, an algorithm is a way of describing the logic. And that's why it's
so hard to cover all possible forms of it in terms of common rules or
definitions. Most prominent mathematicians began seriously thinking about
computability and what can be computed at the beginning of the 20th century.
But it was so hard to generalize all the cases that eventually they had to limit
the consideration by functions defined only on the set of `Natural numbers`_. 

|

The most famous works were done by `Alan Turing`_ (related to algorithms) and
`Alonzo Church`_ (related to computable functions). Alan Turing came up with the
thesis which basically says, that if a function is computable then it has
an algorithm, and if so, then it can be implemented on the Turing machine (TM).
In other words, `Turing's thesis`_ makes it clear what can be computed and what
is needed to get computed.

|

`Turing machine`_ is an abstract system that has a finite set of states and
symbols, a few certain operations, and an endless tape (consisted of cells).
The behavior of a TM is controlled by a program that defines a state transition
and a next tape movement depending on a symbol that was read. Although, there
is no a real-world analog of the TM as it is unlikely possible to have infinite
memory. So, to get it more realistic, for a real analog of TM, it means two things:

1. to have enough memory, at least, as much as needed (analog of the tape)
2. to have a conditional branching, some sort of if/else and goto statements
   (analog of state transitions)

|

All algorithms share the same properties:

- deterministic (produces the same result for the same input)
- discrete (works with discrete data, like texts, integers, rational numbers)
- finite (represented by a finite text)

|

.. image:: {static}/files/algorithm/algorithm-properties.png
   :width: 100%
   :alt: Turing completeness
   :class: img
   :target: {static}/files/algorithm/algorithm-properties.png

|

.. Links

.. _`Alan Turing`: https://en.wikipedia.org/wiki/Church%E2%80%93Turing_thesis
.. _`Alonzo Church`: https://en.wikipedia.org/wiki/Church%E2%80%93Turing_thesis
.. _`Turing machine`: https://www.youtube.com/watch?v=dNRDvLACg5Q
.. _`Natural numbers`: https://vorakl.com/articles/numbers/
.. _`Turing's thesis`: https://vorakl.com/articles/turing/
