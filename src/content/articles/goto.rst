Structured Programming Paradigm
###############################

:summary: What can cause too much use of "goto statements"
:date: 2019-06-12 16:24:24
:category: note
:tags: cs, mindmap
:slug: goto

There was the time when computer programs were so much long and unstructured
that some times just a few people managed to logically navigate source code
in huge software projects. Having low-level programming languages, programmers
used various equivalents of "goto statements" for conditional branching that
often led to decreasing readability and difficulties in keeping a logical
context, especially jumping too far to another subroutine.

|

A few things happened on the way to a solution that eventually appeared in the
form of `Structured Programming Paradigm`_. In 1966, *Corrado Böhm* and *Guiseppe Jacopini*
proved a theorem_ that any computer program which might be represented as a flow diagram
can be rewritten using only 3 control structures (sequence, selection, iteration).

| 

In 1968, *Edsger W. Dijkstra* published the influential article "`Go To Statement Considered Harmful`_"
where he pointed out that using too many **goto** statements has a negative effect
on the readability and understanding of computer programs. Though, his intention
was, unfortunately, misunderstood and misused by the almost complete abandoning
of using "goto" in high-level programming languages, even at the cost of less
readable and vague code.

| 

As a result of working on the improvement of the ALGOL, *Niklaus Wirth* designed
a new imperative programming language, Pascal_, which was released in 1970.
It was widely used for teaching students the Structured Programming Design for
a few decades since then.

|

.. raw:: html

    <iframe width='853'
            height='480' 
            src='https://embed.coggle.it/diagram/XPp2KiopRH3zRgFT/t/structured-programming-paradigm'
            frameborder='0'
            allowfullscreen>
    </iframe>

Other formats: PDF_, PNG_, TXT_

.. Links

.. _`Structured Programming paradigm`: https://en.wikipedia.org/wiki/Structured_programming
.. _theorem: https://en.wikipedia.org/wiki/Structured_program_theorem
.. _`Go To Statement Considered Harmful`: {static}/files/goto/Dijkstra68.pdf
.. _Pascal: https://en.wikipedia.org/wiki/Pascal_(programming_language)
.. _PDF: {static}/files/goto/goto.pdf
.. _PNG: {static}/files/goto/goto.png
.. _TXT: {static}/files/goto/goto.txt
