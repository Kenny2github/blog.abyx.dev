:og:description: Python enum flags are cool, and can mimic sets. What does that even mean?

Python Enum Flags and Basic Set Theory
======================================

**Date**: *2022-Jun-23*

Python's :py:mod:`enum` module does a bunch of nifty tricks to make enumerations. One of its coolest features, though, at least in my opinion, is the :py:class:`~enum.Flag` enum type. For example, you can use it to represent Unix octal permissions:

.. code-block:: python

    >>> class Permission(Flag):
    ...     READ = 0b100
    ...     WRITE = 0b010
    ...     EXECUTE = 0b001

    >>> Permission.READ | Permission.WRITE | Permission.EXECUTE
    <Permission.READ|WRITE|EXECUTE: 7>

Or, using the Python documentation's own example, you can represent a 3-bit color:

.. code-block:: python

    >>> class Color(Flag):
    ...     RED = auto()
    ...     BLUE = auto()
    ...     GREEN = auto()
    ...     WHITE = RED | BLUE | GREEN
    ...
    >>> Color.WHITE
    <Color.WHITE: 7>

However, all of these have a deeper connection: to set theory.

Basic Set Theory
----------------
Let's get some introductories out of the way first. If you know all this, skip to `Python Sets`_.

Please know that I am not a mathematician and may get some things wrong here. Just accept me as incompetent and move on.

Definitions
***********

* A *set* is a collection of unique *objects*. For example, :math:`\{A, B, C\}`, :math:`\{420, Earth\}`, and :math:`\{\{12\}, \{20, 21\}\}` are all sets.

  * Besides by listing their members, sets can also be defined by an unambiguous characteristic of their members: :math:`\{x : x \geq A \land x \leq C\}` is another way to define the first set above, assuming letters can be compared like that.

* An object is a *member* of a set if the set contains the object. For example, if :math:`S = \{A, B, C\}`, :math:`A \in S` (A is in S) but :math:`D \notin S` (D is not in S).
* There are two special sets:

  * The *empty set*, :math:`\emptyset`, which contains no objects (no object is a member of the empty set).
  * The *universe set*, denoted here as :math:`U`, which contains *all* objects (if an object is a member of *any* set, it is a member of the universe set).

Operations
**********
The following examples use the sets :math:`A = \{1, 2, 3\}` and :math:`B = \{2, 3, 4\}`, and the universe :math:`U = \{1, 2, 3, 4, 5\}`. Note that all characteristic-based set definitions here assume the implicit additional criterion that :math:`x \in U`.

* The *union* of two sets is a set such that if an object is a member of *either* set, it is also a member of their union. That is, :math:`A \cup B = \{x : x \in A \lor x \in B\}`. For example, :math:`A \cup B = \{1, 2, 3, 4\}`.
* The *intersection* of two sets is a set such that if an object is a member of *both* sets, it is also a member of their intersection. That is, :math:`A \cap B = \{x : x \in A \land x \in B\}`. For example, :math:`A \cap B = \{2, 3\}`.
* The *complement* of a set is a set such that if an object is a member of the set, it is *not* a member of its complement. However, if an object (*within the universe*) is *not* a member of the set, then it *is* a member of its complement. That is, :math:`A' = \{x : x \notin A\}`. For example, :math:`A' = \{4, 5\}` (remembering the implicit :math:`x \in U` criterion).

These can be used to construct some more operations:

* The *difference* of two sets is a set of objects that are members of the first set but not the second. (Note that "first" and "second" are being used here now; the difference of sets is not commutative.) That is, :math:`A \setminus B = \{x : x \in A \land x \notin B\} = A \cap B'`. For example, :math:`A \setminus B = \{1\}`.

  * You can also use this to think of the complement as :math:`A' = U \setminus A`.

* The *symmetric* or *commutative difference* of two sets is a set of objects that are members of either set but not the other. That is, :math:`A \ominus B = \{x : x \in A \oplus x \in B\} = A' \cup B'`. (Note: I am using the nonstandard notation :math:`\ominus` for symmetric difference and :math:`\oplus` for logical XOR.) For example, :math:`A \ominus B = \{1, 4\}`.

Checks
******

* Two sets are *equal* if every member of either set is also a member of the other set.
* A set is a *subset* of another set if every member of the first set is also a member of the second. For example, :math:`\{1, 2\} \subseteq \{1, 2, 3\}` but :math:`\{1, 2, 4\} \nsubseteq \{1, 2, 3\}`.

  * A set is a *proper subset* of another set if it is a subset of, *but* not equal to the other set. For example, :math:`\{1, 2\} \subset \{1, 2, 3\}` but :math:`\{1, 2, 3\} \not\subset \{1, 2, 3\}` even though :math:`\{1, 2, 3\} \subseteq \{1, 2, 3\}`.
  * You can also use this to think of equality as :math:`A = B \implies A \subseteq B \land B \subseteq A`.

* A set is a *superset* (:math:`\supseteq`) of another set if the other set is a subset of the set.

  * A set is a *proper superset* (:math:`\supset`) of another set if the other set is a proper subset of the set.

Python Sets
-----------
Python implements most of the set operations described above:

.. code-block:: python

    >>> {1, 2, 3} # set definition by listing members
    {1, 2, 3}
    >>> set() # the empty set
    set()
    >>> 1 in {1, 2, 3} # membership
    True
    >>> A = {1, 2, 3}
    >>> B = {2, 3, 4}
    >>> A | B # union (like OR)
    {1, 2, 3, 4}
    >>> A & B # intersection (like AND)
    {2, 3}
    >>> A - B # difference
    {1}
    >>> A ^ B # symmetric difference (like XOR)
    {1, 4}
    >>> {1, 2, 3} == {1, 2, 3} # equality, duh
    True
    >>> {1, 2} <= {1, 2, 3} # subset
    True
    >>> {1, 2} < {1, 2, 3} # proper subset
    True
    >>> {1, 2, 3} <= {1, 2, 3}
    True
    >>> {1, 2, 3} < {1, 2, 3}
    False
    >>> {1, 2, 4} <= {1, 2, 3}
    False
    >>> # flip sign and arguments for superset and proper superset

A notable omission from the Python :py:class:`set` class, though, is the concept of a universe set. Furthermore, without a universe, there can be no complement, which would otherwise be :python:`~A # like NOT`.

.. admonition:: Technicality

    You could consider Python's set comprehensions, like :python:`{x for x in range(5) if x % 2 == 1}`, to be characteristic-based set definitions, where :python:`x % 2 == 1` is the characteristic. In that case, you could reasonably say that :python:`range(5)` is the universe. However, Python sets don't support universes in any other context, so the complement is still missing as a result.

However, *drumroll...*

Flag Instances as Sets
----------------------
:py:class:`~enum.Flag` instances do what Python sets cannot! Namely, the subclass defines the universe. Because of this, flag instances support the complement, in addition to other set operations:

.. code-block:: python

    >>> class U(Flag):
    ...     """Definition of the universe"""
    ...     def __repr__(self) -> str:
    ...         """Hide the unimportant numeric enum value."""
    ...         return super().__repr__().split(':', 1)[0] + '>'
    ...     A = auto()
    ...     B = auto()
    ...     C = auto()
    ...     D = auto()
    ...     E = auto()
    ...
    >>> U.A | U.B | U.C # set definition by listing members
    <U.C|B|A>
    >>> U(0) # the empty set
    <U.0>
    >>> U.A in U.A | U.B | U.C # membership
    True
    >>> X = U.A | U.B | U.C
    >>> Y = U.B | U.C | U.D
    >>> X | Y # union
    <U.D|C|B|A>
    >>> X & Y # intersection
    <U.C|B>
    >>> ~(U.A | U.B) # complement! :D
    <U.E|D|C>
    >>> X ^ Y # symmetric difference
    <U.D|A>
    >>> U.A | U.B | U.C == U.A | U.B | U.C # equality
    True

However, using :py:class:`~enum.Flag` instances as set stand-ins has its own drawbacks:

* Some set operations are missing (but see `this gist`_ for an implementation of them):

  * Asymmetric difference (can't do :python:`X - Y`)
  * Superset and subset (can't do :python:`X < Y` or :python:`X > Y`)

* Obviously, you're limited to the universe you define. Regular :py:class:`set` instances can hold any hashable object. (That would make :py:class:`collections.abc.Hashable` the universe if it was enumerable.)
* :py:class:`set` instances are mutable; :py:class:`~enum.Flag` instances are not.
* :py:class:`set` instances can be nested; :py:class:`~enum.Flag` instances cannot. Notably, each enum member is both a singleton set and the single member of that set at the same time.

So consider yourself informed.

Conclusion
----------
Regular Python :py:class:`set` instances are mutable, nestable, and not bound to a universe, but as a consequence do not support the set complement. On the other hand, using :py:class:`enum.Flag` to mimic sets does support the complement, since the enum definition is the universe, but native :py:class:`enum.Flag` doesn't support sub/super-set or asymmetric differences. (Again, see `this gist`_ for a custom subclass that does support those operations.)

To use an example from the original context in which I came up with this, Python sets are good for storing the groups/roles that a user belongs to / holds, while set-like flags are good for representing the permissions that a user has, possibly due to their groups/roles.

Do with this information what you will!

.. _this gist: https://gist.github.com/Kenny2github/28239983d923c75bf61b5e7682f6f63c
