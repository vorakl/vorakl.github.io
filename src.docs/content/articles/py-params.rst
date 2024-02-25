A little mess with function parameters in Python
################################################

:summary: A variety of ways to define function parameters 
:date: 2024-02-17 11:03:29
:category: tutorial
:tags: python, programming
:slug: py-params

`TLDR: quick summary of the article`_

|

At first glance, Python functions look like those in most other languages, and they behave just as you'd expect. They take arguments, have default values, and can also return a value. This is intentional, of course. But once you dive deeper, you'll see how many specific nuances are hidden internally, providing a programmer with a number of features that make using functions in Python a much more powerful experience. Knowing the differences is critical to understanding why they behave the way they do, so you can get the most out of them.

|

One of the key feature is that functions in Python are objects that are created as soon as they are defined. This allows you to use functions as arguments in other functions or as return values, just like any other Python object. Functions lifetime is different from the execution time, and they exist even after execution has finished. Functions, being objects, also have a set of predefined attributes that can be extended at any time, and their state is maintained outside of the execution. Parameters become local variables, which are completely different entities from function attributes, which exist only at execution time. Default values in the function definition can also be expressions, but they are evaluated only once. Function arguments are always passed by value, but the values they contain are references. This is why they're sometimes called pass-by-object-references. This also means that parameters, like any other variable in Python, are untyped, and contain a copy of a reference to an object. Changing a parameter (a local variable) generally doesn't change an object (passed as an argument) itself, but only stores a reference to another object. However, there is still a way to change an object that is passed as an argument, if it is a mutable object and the change is made directly to it rather than to a variable. For example, updating elements of a list or a dictionary.

|

This tutorial will focus only on parameters, their different types, and various ways to define them. Let's start with the most common: a function definition with 4 parameters (a, b, c, d). No types, just names, with a lifetime during function execution, i.e. they are created on the stack as local variables only during function execution. When the function is called, it gets 4 arguments (w, x, y, z), which are also local variables (live on a stack), but in the calling environment, and contain references to some objects. Python takes these references stored in the arguments (w, x, y, z) and copies them into parameters (a, b, c, d) that live as local variables on a stack in the called environment:

.. code-block:: python

    def myfunc(a, b, c, d):
        print(a, b, c, d)

    def caller():
        w, x, y, z = 10, 20, 30, 40
        myfunc(w, x, y, z)          # 10 20 30 40

    caller()

|

When you call *myfunc* this way, references to objects stored in arguments are copied as values to parameters according to their position, e.g. the value of *w* is copied to *a*, the value of *x* is copied to *b*, and so on. This is why such parameters are also called **positional parameters** - their position defines the value they get. However, you can assign values to parameters in any order by using **keyword arguments**, i.e. parameter_name=argument:

.. code-block:: python

    def myfunc(a, b, c, d):
        print(a, b, c, d)

    def caller():
        w, x, y, z = 10, 20, 30, 40
        myfunc(a=z, b=y, c=x, d=w)  # 40 30 20 10

    caller()

|

Although, all 4 parameters must to be defined each time the function is called. This can be avoided by setting default values for the parameters in the function definition. Keyword pairs must always be defined after positional parameters:

.. code-block:: python

    def myfunc(a, b, c, d=2):
        print(a, b, c, d)

    def caller():
        w, x, y, z = 10, 20, 30, 40
        myfunc(w, c=x, b=y)         # 10 30 20 2
        myfunc(w, z, y)             # 10 40 30 2

    caller()

|

Default values of parameters are stored in the **__defaults__** object attribute. Python allows you to do neat tricks, because this attribute is mutable, and you can assign default values directly to the attribute. This is even possible for the parameters that don't have default values in the function definition and normally need to be set on the function call:

.. code-block:: python

    def myfunc(a, b, c, d=2):
        print(a, b, c, d)
    
    print(myfunc.__defaults__)      # (2,)
    
    myfunc.__defaults__ = (100, 200, 300, 400)
    print(myfunc.__defaults__)      # (100, 200, 300, 400)

    # note that arguments are not passed at all!
    myfunc()                        # 100 200 300 400

|

Default values can also be expressions, but are evaluated only once. For example, if a list is assigned as a default value, its object is created and its reference is assigned each time a default value is used. This may not be the behavior you expect, since a mutated list on a previous function call will still be passed as the default parameter value on the next call:

.. code-block:: python

    def myfunc(a, b, c, d=[]):
        d.extend((a, b, c))
        print(a, b, c, d)

    myfunc(1, 2, 3)                 # 1 2 3 [1, 2, 3]
    myfunc(10, 20, 30)              # 10 20 30 [1, 2, 3, 10, 20, 30]

|

A possible workaround for having an empty list as the default value is to use *None* instead. This is a singleton, there is always only one instance. Check a parameter for equivalence to None in the code and assign an empty list during a function execution:

.. code-block:: python

    def myfunc(a, b, c, d=None):
        if d is None:
            d = []
        d.extend((a, b, c))
        print(a, b, c, d)

    myfunc(1, 2, 3)                 # 1 2 3 [1, 2, 3]
    myfunc(10, 20, 30)              # 10 20 30 [10, 20, 30]

|

*Positional* and *keyword* parameters can easily coexist in a relatively free form, with the caveat that keyword parameters are always defined after positional parameters. In general, when calling a function, arguments can be passed in a variety of combinations of positional or keyword types, or omitted with a default value:

.. code-block:: python

    def myfunc(a, b, c=1, d=2):
        print(a, b, c, d)

    myfunc(3, b=30, c=20)             # 3 30 20 2

|

However, there are ways to force some parameters to be strictly positional, and others to be keyword only. The first is made possible by another nice feature - a variable number of parameters. Python supports *packing* and *unpacking* of arguments during a function call, which can be used to pass an arbitrary number of positional and keyword parameters. It has a special syntax for both cases: positional arguments are packed into *tuples* if there is a parameter prefixed with an asterisk, e.g. ***params**, and keyword parameters are packed into *dictionaries* if there is a parameter prefixed with a double asterisk, e.g. ****kwparams**. Note that keyword parameters or a `**kwparams` parameter, if defined, should always follow any positional parameters or a `*params`, if it's defined:

.. code-block:: python

    def myfunc(a, b, *params, c=1, d=2, **kwparams):
        print(a, b, c, d)           # 1 2 20 30
        print(params)               # (3, 4)
        print(kwparams)             # {'e': 50, 'f': 60}

    myfunc(1, 2, 3, 4, c=20, d=30, e=50, f=60)

|

Also note that the *params* tuple and the *kwparams* dictionary are both used without asterisks in the code. It even works in the other way around. If you have a tuple or a dictionary with some values, you can easily pass them to a function that takes positional or keyword arguments. Just keep an eye on the number of elements:

.. code-block:: python

    def myfunc(a, b, c=3, d=4):
        print(a, b, c, d)

    args = (1, 2, 10)
    kwargs = {'b': 20, 'c': 30, 'd': 40}

    myfunc(*args, 40)               # 1 2 10 40
    myfunc(1, **kwargs)             # 1 20 30 40

|

To define a unified function that can take any number of arguments of any type, it should have a definition that packs all types of parameters, e.g. *myfunc(*params, **kwparams)*. In addition, this syntax strictly separates keyword and positional parameters. If a function has any number of unaggregated keyword parameters after aggregating of positional parameters, then they are considered as *keyword-only parameters* with default values. The equivalent attribute with default values is called **__kwdefaults__**:

.. code-block:: python

    def myfunc(a, b, *params, c=1, d=2, **kwparams):
        pass

    print(myfunc.__defaults__)      # None
    print(myfunc.__kwdefaults__)    # {'c': 1, 'd': 2}

|

This syntax makes it possible to have a simpler function definition in case there is no need in an arbitrary number of parameters. Just put an asterisk between positional and keyword parameters:

.. code-block:: python

    def myfunc(a, b, *, c=1, d=2):
        print(a, b, c, d)

    # this doesn't work anymore
    # myfunc(1, 3, 4, 5)

    myfunc(1, 3, d=2, c=1)          # 1 3 1 2

|

Nevertheless, there is some room for improvisation. Positional arguments can still be passed as keywords:

.. code-block:: python

    def myfunc(a, b, *, c=10, d=20):
        print(a, b, c, d)

    myfunc(b=3, a=4, d=2, c=1)      # 4 3 1 2
    myfunc(a=4, b=3, c=1)           # 4 3 1 20
    myfunc(4, b=3, d=2)             # 4 3 10 2
    myfunc(4, 3)                    # 4 3 10 20

|

Fortunately, Python has the syntax to strictly separate positional-only parameters (which cannot be passed as a keyword) from positional parameters (which can either be passed by a value or a keyword). Both can have default values, by the way. Just put a slash between them:

.. code-block:: python

    def myfunc(a, /,  b=30, *, c=10, d=20):
        print(a, b, c, d)

    # this doesn't work anymore
    # myfunc(a=1, b=2, c=4, d=3)

    myfunc(4, b=3, d=2, c=1)        # 4 3 1 2
    myfunc(4, 3, d=2, c=1)          # 4 3 1 2
    myfunc(4, c=1, d=2)             # 4 30 1 2
    myfunc(4)                       # 4 30 10 20

    print(myfunc.__defaults__)      # (30,)
    print(myfunc.__kwdefaults__)    # {'c': 10, 'd': 20}

|

As a good example, let's take a look at a prototype of the built-in *sorted* function:

.. code-block:: python

    sorted(iterable, /, *, key=None, reverse=False)

|

This means that the first argument should always be passed as a positional-only argument. You can't pass it as `iterable=<something>` keyword. However, all subsequent arguments should always be defined as keywords-only. This also means that the order of these arguments, as well as how many of them are passed, is not important.

|

Another good example is the *pop* method of the *list* class:

.. code-block:: python

    list.pop(index=-1, /)

|

*index* is a positional-only parameter, but if omitted, -1 will be passed by default.

|

Summary
-------

* Functions in Python are objects that are created when defined, allowing them to be used as arguments or return values like any other object.
* Parameters become local variables during function execution, while function attributes exist outside of execution.
* Arguments are passed by value, but parameters contain a copy of the reference. Changing a parameter doesn't change the original object, but changing a mutable object passed as an argument does.
* Parameters can be defined positionally or by keyword. Expressions as the default values are evaluated only once at definition.
* The *__defaults__* attribute stores default values of positional parameters and is mutable, allowing direct assignment.
* An asterisk followed by a name (`*var`) packs positional arguments into a tuple, while a double asterisk followed by a name (`**kwvar`) packs keyword arguments into a dictionary.
* Keyword arguments always follow positional arguments, with defaults filling in omitted values.
* A slash as a parameter, separates positional-only parameters that cannot be passed by keyword from other positional parameters.
* An asterisk as a parameter, separates positional parameters with default values from keyword-only parameters.
* The *__kwdefaults__* attribute stores default values of keyword-only parameters that defiend after the asterisk.

.. Links
.. _`TLDR: quick summary of the article`: Summary_
