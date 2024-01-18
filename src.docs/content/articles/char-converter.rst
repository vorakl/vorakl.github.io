A converter of a character's case and Ascii codes
#################################################

:summary: An example of using the Constraint Programming for calculating multiple but linked results
:date: 2019-08-08 17:50:05
:category: code
:tags: cs, programming, python, encoding
:slug: char-converter

The constraint programming paradigm is effectively applied for solving a group of problems which can be translated to variables and constraints or represented as a mathematic equation, and so related to the CSP_. Using declarative programming style it describes a general model with certain properties. In contrast to the imperative style, it doesn't tell *how* to achieve something, but rather *what* to achieve. Instead of defining a set of instructions with only one obvious way for computing values, the constraint programming declares relationships between variables within constraints. A final model makes it possible to compute the values of variables regardless of direction or changes. Thus, any change of the value of one variable affects the whole system (all other variables) and to satisfy defined constraints it leads to recomputing the other values.

|

Let's take, for example, Pythagoras' theorem: **a² + b² = c²**. The *constraint* is represented by this equation, which has three *variables* (a, b, and c), and each has a *domain* (non-negative). Using the imperative programming style, to compute any of these variables having other two, we would need to create three different functions (because each variable is computed by a different equation): 

* c = √(a² + b²)
* a = √(c² - b²)
* b = √(c² - a²)

These functions satisfy the main constraint and to check domains, each function should validate the input. Moreover, at least one more function would be needed for choosing an appropriate function accordingly to provided variables. This is one of possible solutions:

.. code-block:: python

    def pythagoras(*, a=None, b=None, c=None):                                      
        ''' Computes a side of a right triangle '''                                                                                                                               
                                                                                    
        # Validate                                                                  
        if len([i for i in (a, b, c) if i is None or i <= 0]) != 1:                 
            raise SystemExit("ERROR: you need to define any of two non-negative variables")
                                                                                    
        # Compute                                                                   
        if a is None:                                                               
            return (c**2 - b**2)**0.5                                               
        elif b is None:                                                             
            return (c**2 - a**2)**0.5                                               
        else:                                                                       
            return (a**2 + b**2)**0.5

To see the difference of the constraint programming approach, I'll show an example of a "problem" with four variables and a constraint that is not represented by a straight mathematic equation. This is a converter that can change a case of the characters (small to/from capital) and return the Ascii codes of both. Hence, at any time the converter is aware of all four values and reacts immediately on any changes. The idea of creating this example was fully inspired by the `Fahrenheit-Celsius converter`_ by John DeNero.

|

Let's take a look on a diagram of a constraint system:

.. image:: {static}/files/char-converter/char-converter.png
   :width: 100%
   :alt: the diagram
   :class: img
   :target: {static}/files/char-converter/char-converter.png


The represented "problem" is translated into a constraint system that consists of nodes (constraint) and connectors (variables). Connectors provide an interface for getting and setting values. They also check the variables' domains. When some value changes, that particular connector notifies all its connected nodes about the change. Nodes, in turn, satisfy constraints, calculate new values and propagate them to other connectors across the system, by "asking" them to set a new value. The propagation is done using the message passing technique that means connectors and nodes get messages (synchronously) and react accordingly. For instance, if the system gets the 'A' letter on the "Capital Letter" connector, all other three connectors provide an appropriate result accordingly to the defined constraint on the nodes: 97, 'a', and 65. And of course, it's not allowed to set on that connector any small letters, e.g. 'b', because each connector has its own domain. 

|

When all connectors are linked to nodes, nodes are defined by constraints, the system is fully set and ready to get values on any of four connectors. Once it's set, the system automatically calculates and sets values on the rest connectors. There is no need to check what a variable was set and which functions should be called, as it was needed in the imperative approach which relatively easy to achieve with a few variables but gets interesting in case of tens or more.

|

The full source code is available in my `Github repo`_. Let's now dig a little bit into details and find out how the system is built.
Firstly, we define our connectors by giving them names and setting domains as a function of one argument:

.. code-block:: python
    
    import constraint_programming as cp

    small_ascii = cp.connector('Small Ascii', lambda x: x >= 97 and x <= 122)
    small_letter = cp.connector('Small Letter', lambda x: x >= 'a' and x <= 'z')
    capital_ascii = cp.connector('Capital Ascii', lambda x: x >= 65 and x <= 90)
    capital_letter = cp.connector('Capital Letter', lambda x: x >= 'A' and x <= 'Z')

Secondly, we link these connectors to nodes. There are two types: *code* (translates letters to Ascii codes and back) and *aA* (translates small letters to capital and back):

.. code-block:: python

    code(small_letter, small_ascii)
    code(capital_letter, capital_ascii)
    aA(small_letter, capital_letter)

These two nodes are different by functions which should be called and they derived from a general constraint function:

.. code-block:: python

    def code(conn1, conn2):
        return cp.constraint(conn1, conn2, ord, chr)

    def aA(conn1, conn2):
        return cp.constraint(conn1, conn2, str.upper, str.lower)

Each node has only two connectors. If an update has occurred on a first connector then a first function is called to calculate a value of another connector (variable). The same happens if a second connector changes its value. For example, if the *code* node gets 'A' on the *conn1* connector, then the function *ord* will be used to get its Ascii code. And, the other way around, if the *aA* node gets 'A' on the *conn2* connector then it needs to use *str.lower* function to get an appropriate small letter on the *conn1*. Every node is responsible for computing new values and "sending" a message to another connector that there is a new value to set. This message is conveyed with the name of a node that is asking to set a new value, and actually a new value.

.. code-block:: python

    def set_value(src_constr, value):
        if (not domain is None) and (not domain(value)):
            raise ValueOutOfDomain(link, value)
        link['value'] = value
        for constraint in constraints:
            if constraint is not src_constr:
                constraint['update'](link)

When a connector receives the "set" message, it runs the "set_value" function to check a domain, sets a new value, and sends the "update" message to another node. It is just a notification that value on that connector has changed.

.. code-block:: python

    def update(src_conn):
        if src_conn is conn1:
            conn2['set'](node, constr1(conn1['value']))
        else:
            conn1['set'](node, constr2(conn2['value']))

Then, the notified node requests this new value on the connector, compute a new value for another connector and so on, until the whole system has changed. That's how the propagation actually work. 

|

But, how is the message passing happening? This is implemented as accessing keys of dictionaries. Both functions (connector and constraint) return a *dispatch dictionary*. Such a dictionary contains *messages* as keys and closures as values. By accessing a key, let's say, "set", a dictionary returns the function "set_value" (closure) that has access to all local names of the "connector" function.

.. code-block:: python

    # A dispatch dictionary
    link = { 'name': name,
             'value': None,
             'connect': connect,
             'set': set_value,
             'constraints': get_constraints }

    return link

Having a dictionary as a return value makes it possible to create multiple closures (functions) with access to the same local state to operate on. Then, these closures are callable by using keys as a sort of messages.

.. Links

.. _CSP: https://vorakl.com/articles/csp/
.. _`Fahrenheit-Celsius converter`: https://www.composingprograms.com/pages/24-mutable-data.html#propagating-constraints
.. _`Github repo`: https://github.com/vorakl/composingprograms.com/tree/master/char_converter

