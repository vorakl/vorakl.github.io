Number Classification
#####################

:summary: All number categories, from Complex to Counting
:date: 2019-08-16 12:42:06
:category: note
:tags: math, cs
:slug: numbers

Mathematics is unique. The unique science if everyone could agree that it is a Science. But, it's also hard to argue that it is not Art. Math is absolutely certain, except the cases when it is not ("`as far as the laws of mathematics refer to reality, they are not certain; and as far as they are certain, they do not refer to reality`_"). Still having no one general definition, Math doesn't even bother to have one opinion on such the fundamental building block of Mathematics as Numbers_. Nevertheless, Math is an important part of almost every field of science, engineering, and human life.

|

Here is the most common and well-accepted number classification tree:

.. image:: {static}/files/numbers/numbers.png
   :width: 100%
   :alt: Number classification
   :class: img
   :target: {static}/files/numbers/numbers.png

|

It also shouldn't be a surprise to find slight distinctions in the meaning of the same essences in *Math* and *Computer Science* (CS):

* **Natural numbers**. In Math, they are meant to be *Positive Integers* (1, 2, 3, ...), but in CS they are *non-negative Integers* which include Zero (0, 1, 2, 3 ...)
* **Mantissa**. In Math, it is a *fractional part* of the logarithm. In CS, it is *significant digits* of a floating-point number (thus, quite often are used other definitions in this case, like significand_ and coefficient)

|

There is a quite related topic in terms of the values which a variable can take on. In mathematics, a variable may be two different types: `continuous and discrete`_:

* A variable is **continuous** when it can take on infinitely many, uncountable values. There is always another value in between two others in a non-empty range, no matter how close they are.
* A variable is **discrete** when there is always a positive minimum distance between two values in a non-empty range. The set of numbers is finite or countably infinite (e.g. Natural numbers)

The understanding of the discreteness is crucial in Computer Science as all real-world computers internally work only with discrete data (which makes it challenging to represent Irrational numbers). All existing computability theories (e.g. `Turing thesis, Church thesis`_) are defined on discrete values, and the domain is the set of Natural numbers.

.. Links

.. _`as far as the laws of mathematics refer to reality, they are not certain; and as far as they are certain, they do not refer to reality`: https://en.wikipedia.org/wiki/Mathematics#cite_note-certain-39
.. _Numbers: https://www.mathsisfun.com/numbers/evolution-of-numbers.html
.. _significand: https://en.wikipedia.org/wiki/Significand
.. _`continuous and discrete`: https://en.wikipedia.org/wiki/Continuous_or_discrete_variable
.. _`Turing thesis, Church thesis`: https://en.wikipedia.org/wiki/Church%E2%80%93Turing_thesis
