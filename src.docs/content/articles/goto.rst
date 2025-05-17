Structured Programming Paradigm
###############################

:summary: What can cause too much use of "goto statements"
:date: 2019-06-12 16:24:24
:category: note
:tags: cs, programming, mindmap
:slug: goto

There was a time when computer programs were so long and unstructured that
only a few people could logically navigate the source code of huge software
projects. With low-level programming languages, programmers used various
equivalents of "goto" statements for conditional branching, which often
resulted in decreased readability and difficulty maintaining logical context,
especially when jumping too far into another subroutine.

|

A few things happened on the way to a solution that eventually appeared in the
form of the `Structured Programming Paradigm`_. In 1966, *Corrado Böhm* and
*Guiseppe Jacopini* proved a theorem that any computer program that can
be represented as a flowchart can be rewritten using only 3 control structures
(sequence, selection, and iteration).

|

In 1968, *Edsger W. Dijkstra* published the influential article "Go To Statement Considered Harmful",
in which he pointed out that using too many goto statements would make computer
programs harder to read and understand. However, `his intention was unfortunately misunderstood and misused`_
by the almost complete abandonment of the use of "goto" in high-level
programming languages, even at the cost of less readable and vague code.

|

As a result of his work on improving ALGOL, *Niklaus Wirth* designed a new
imperative programming language, Pascal_, which was released in 1970.
It has been widely used for teaching structured programming design to students
for several decades since.

|

.. image:: {static}/files/goto/goto.png
   :width: 100%
   :alt: MindMap
   :class: img
   :target: {static}/files/goto/goto.png

.. Links

.. _`Structured Programming paradigm`: https://en.wikipedia.org/wiki/Structured_programming
.. _theorem: https://en.wikipedia.org/wiki/Structured_program_theorem
.. _Pascal: https://en.wikipedia.org/wiki/Pascal_(programming_language)
.. _`his intention was unfortunately misunderstood and misused`: http://david.tribble.com/text/goto.html
