Organizing Unstructured Data
############################

:summary: Managing data complexity using types, structures, ADTs, and objects
:date: 2019-08-21 17:08:40
:category: note
:tags: cs, programming
:slug: data-structure

Topics
------

* Type_
* `Data Structure`_
* `Abstract Data Type (ADT)`_
* Object_

|

The main, if not the only, purpose of the Computer is computing information. It doesn't always have to be a computation of mathematic formulas. In general, it is a transformation of one chunk of information to another. Computers work only with such information that can be represented as discrete data. The input and output for the compute engine is always `Natural numbers`_ or text (a sequence of symbols from a dictionary which corresponds to certain natural numbers).

.. image:: {static}/files/data-structure/compute.png
   :width: 100%
   :alt: computation diagram
   :class: img
   :target: {static}/files/data-structure/compute.png

While data is *unstructured*, it's hard to recognize some sense in it. But once data gets any *structured* form, it becomes meaningful and suitable for further transformation.

|

Type
----

The simplest form of data organization is **Type**. In general, a *Data Type* determines a set of values with certain characteristics. Usually, it defines a size in bytes. A **Primitive Data Type** is *an ordered group of bytes*. When a variable of some primitive data type has only one value (holds only one piece of information), it's called a **Scalar** and a type - **Scalar Data Type**. Well-known examples are *integer*, *float*, *pointer*, and *string*. A *collection of primitive data types* is known as **Structured Data Type** and it makes possible to store multiple values. Good examples of this type are *array*, *struct*, *record*, and *file*. The key property is the ordered byte's group. The internal organization is straightforward and all actions (e.g. reading, modifying) are performed directly on the data, accordingly to a hardware architecture that defines the byte order in memory (Little-/Big- Endian).

|

Data Structure
--------------

The next layer of data abstraction is called  **Data Structure**. It brings more complexity but also more flexibility in making the right choice between an access speed, an ability to grow, a modification speed, etc. Internally, it's represented by a collection of the scalar or structured data types. The main focus is on *details of the internal organization and a set of rules for controlling this organization*. There are two types of data structures which come from a difference in a location in memory of underlying elements: 

* **Array Data Structures** (static), based on physically contiguous elements in memory, with no gaps in between.
* **Linked Data Structures** (dynamic), based on elements, dynamically allocated in memory and linked in a linear structure using pointers (usually, one or two)

Well-known examples are *linked list*, *hash* (*dictionary*), *set*, *list*.
The internal organization is still open and all actions on data are also performed directly.

|

Abstract Data Type (ADT)
------------------------

A higher level of data abstraction is represented by **Abstract Data Type (ADT)** which shifts the main focus from "*how to store data*" to "*how to work with data*". An ADT is defined by *operations* (functions) for manipulating data and controlling its consistency, and *data structure* for actually storing information. The internal data representation is hidden from users, and should not be accessible directly (by design). All interactions with data are done via an *interface* (operations exposed to users). Usually, for every ADT there are defined a few *primitive operations*, like

* **create** - a constructor of a new instance
* **destroy** - a destructor of an existing instance
* **add**, **get** - the set-get functions for adding and removing elements of an instance
* **is_empty**, **size** - useful functions for managing existing data in an instance

The most known examples of ADTs are *stack* and *queue*. Both of these ADTs can be implemented using either array or linked data structures and both have certain rules for adding and removing elements. All these specifics are abstracted as functions, which in turn, do appropriate actions on internal data. Dividing an ADT into operations and data structure creates an *abstraction barrier* and allows to keep a solid interface with the flexibility for changing internals with no side-effects on code which uses this ADT.

|

Object
------

A more comprehensive way to abstract data is represented by **Objects**. An object can be thought of like a container for a chunk of data that has some certain properties. Similarly to the ADT, this data is not accessible directly (known as *encapsulation* or isolation), but instead each object has a group of tightly attached *Methods*, applicable to operate on its data to produce an expected behavior for this object (known as *polymorphism*). All such methods, in fact, are simply functions which are collected under a *Class*, but they become methods when are called to operate on a certain object. Methods can also be *inherited* from another class which in this case is called a *superclass*. In contrast to an ADT, an object doesn't represent one particular type of data, but it's rather an essence that has a number of *Attributes* and behaves as it's supposed to when its methods are invoked. Attributes are nothing more than variables of any types (including ADTs), and they are also collected under a class. Formally speaking, classes act as specifications of all object's attributes and methods which may be called to deal with those attributes.

The **Object-Oriented Programming** paradigm (OOP) uses objects as the central element of program design. In contrast to the **Procedural Programming** paradigm, where the main focus is on splitting projects up into mostly independent tasks, in OOP, programs are composed of a number of objects. Each object is seen as an instance of some class which defines its behavior. In general OOP design, objects are used to:

- store the program's data as their isolated attributes
- keep the program's logic as their methods
- achieve the main program's goal in the way of interacting objects with each other via message passing (by calling objects' methods).

|

.. image:: {static}/files/data-structure/data-organization.png
   :width: 100%
   :alt: Data Organization
   :class: img
   :target: {static}/files/data-structure/data-organization.png


.. Links
.. _`Natural numbers`: https://vorakl.com/articles/numbers/
