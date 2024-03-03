Turing: thesis, machine, completeness
#####################################

:summary: A formal system in the computability theory
:date: 2019-12-15 15:01:47
:category: note
:tags: cs, mindmap
:slug: turing

Alan Turing is one of the pioneers of the computability theory and logic
formalization. He came up with the hypothesis of which algorithms can be
implemented and computed by machines (`Turing's thesis`_), created an abstract
model of such machine (`Turing machine`_), and described absolutely vital abilities
of any system for being able to realize any logic that can be computed
(`Turing completeness`_).

|

Turing's thesis is only one of the existing formal systems in the computability
theory. There are also λ-calculus, Markov algorithms, but they all were implemented
on the Turing Machine that is used at this time as a general computational model
to classify which real-world systems (mostly programming languages) are able
to compute mathematical functions or implement algorithms.

|

All existing computability theories are defined on discrete values, and
the domain is the set of `Natural numbers`_.

|

I prepared several mindmaps to summarize basic ideas and statements:

- **Turing's thesis**:

.. image:: {static}/files/turing/turing-thesis.png
   :width: 100%
   :alt: Turing's thesis
   :class: img
   :target: {static}/files/turing/turing-thesis.png

|

- **Turing machine**:

.. image:: {static}/files/turing/turing-machine.png
   :width: 100%
   :alt: Turing machine
   :class: img
   :target: {static}/files/turing/turing-machine.png

|

- **Turing completeness**:

.. image:: {static}/files/turing/turing-completeness.png
   :width: 100%
   :alt: Turing completeness
   :class: img
   :target: {static}/files/turing/turing-completeness.png

|

.. Links

.. _`Turing's thesis`: https://en.wikipedia.org/wiki/Church%E2%80%93Turing_thesis
.. _`Turing machine`: https://stackoverflow.com/a/127831/5673383
.. _`Turing completeness`: https://www.youtube.com/watch?v=RPQD7-AOjMI
.. _`Natural numbers`: {filename}/articles/numbers.rst
