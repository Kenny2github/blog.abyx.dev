:og:description: The Python iterable protocol is simple and powerful. This has consequences.

.. role:: elixir(code)
    :language: elixir
    :class: highlight

Python Iterables and Functional Programming
===========================================

**Date**: *2022-Dec-25*

It's Christmas Day and I'm thinking about iterables. I came across `this Reddit comment <https://www.reddit.com/r/ProgrammerHumor/comments/ztlduy/comment/j1eeiyz/?context=3>`_ recently and was rather disappointed by it, because it fails to consider the power of Python iterables on their own terms. I will now attempt to explain the full context and why Python is this way.

The Iterable Protocol
---------------------

For an object to be *iterable*, all it needs to do is implement the iterable protocol, which consists of exactly one method: :py:meth:`container.__iter__`. This method must in turn return an *iterator*, implementing the iterator protocol, which must implement two methods: :py:meth:`iterator.__iter__`, which must return itself, and :py:meth:`iterator.__next__`, which must return the next item in the iterator, or raise :py:exc:`StopIteration` if iteration is over.

That's it. I can describe the entire protocol in one paragraph. In practice it's even simpler, because implementing the iterator protocol is usually not necessary; instead :py:meth:`container.__iter__` can simply delegate to an existing iterator type. The example the docs mention is implementing :py:meth:`~container.__iter__` with a generator - i.e. delegating to the generator iterator type. That's probably the easiest way, but :py:meth:`~container.__iter__` could just as easily return something like :python:`iter(self._items)` if :python:`self._items` is, say, a :py:class:`list`.

Example Implementation
**********************

An example in code might look like this, making use of the :python:`yield from` expression to recursively traverse a binary search tree:

.. code-block:: python

    @dataclass
    class LNR_BST:
        """A Binary Search Tree that is traversed in Left-Node-Right order.

        This tree does not enforce itself because it's a contrived example
        for the purposes of demonstrating __iter__().
        """
        value: Any
        left: Optional[LNR_BST]
        right: Optional[LNR_BST]

        def __iter__(self) -> Iterator[Any]:
            """Traverse the tree in Left-Node-Right order."""
            if self.left is not None:
                yield from self.left # implicit .__iter__()
            yield self.value
            if self.right is not None:
                yield from self.right

Which would do something like this in an interactive session:

.. code-block:: python

    >>> tree = LNR_BST(
    ...     4,
    ...     LNR_BST(
    ...         2,
    ...         LNR_BST(1, None, None),
    ...         LNR_BST(3, None, None),
    ...     ),
    ...     LNR_BST(
    ...         6,
    ...         LNR_BST(5, None, None),
    ...         LNR_BST(7, None, None),
    ...     ),
    ... )
    >>> list(tree)
    [1, 2, 3, 4, 5, 6, 7]

Nifty, right? Well, there's more...

Why Not Methods?
----------------

One of the main qualms that the Reddit comment expresses is that Python "has a nasty convention for composing function calls prefix style and nested, [...] when they should be infix style and chained". I will now attempt to outline several reasons that Python either chooses or is forced to go this route.

Many Things Accept Iterables
****************************

Here's a list of Python builtin functions or type constructors that accept iterables as arguments (as of 3.11.1):

* :py:func:`aiter` (only for an :py:term:`asynchronous iterable`)
* :py:func:`all`
* :py:func:`anext` (only for an :py:term:`asynchronous iterator`)
* :py:func:`any`
* :py:class:`bytearray`
* :py:class:`bytes`
* :py:class:`dict`
* :py:func:`enumerate`
* :py:func:`filter`
* :py:class:`frozenset`
* :py:func:`iter` (duh)
* :py:class:`list`
* :py:func:`map`
* :py:func:`max`
* :py:func:`min`
* :py:func:`next` (only if the iterable is an iterator)
* :py:class:`set`
* :py:func:`sorted`
* :py:func:`sum`
* :py:class:`tuple`
* :py:func:`zip`

That's a lot, and that's only the global builtins. Many, many other standard library functions (and 3rd party library functions), in particular those in :py:mod:`itertools`, accept iterables as arguments as well. And the most obvious use, of course, is in :python:`for var in iterable` tokens - any function that directly uses its argument in a :python:`for` loop will take *any* iterable.

If all of these were methods on iterables instead, *every* class wanting to implement the iterable protocol would have to implement all these methods or at the very least inherit them. Besides the hassle, this would introduce a lot of memory overhead from the method descriptors needed for that purpose, when iterators are often intended specifically for saving the memory that a :py:class:`list` would otherwise occupy. That brings me to my next point...

Many Things Return Iterables
****************************

Here's a list of Python builtin functions or type constructors that return iterables or iterators (as of 3.11.1):

* :py:func:`aiter` (returns an :py:term:`asynchronous iterator`)
* :py:class:`dict` *
* :py:func:`enumerate`
* :py:func:`filter`
* :py:class:`frozenset` *
* :py:func:`iter` (duh)
* :py:class:`list` *
* :py:func:`map`
* :py:func:`open` (a :py:term:`file object` iterates over its lines)
* :py:class:`range` *
* :py:func:`reversed`
* :py:class:`set` *
* :py:func:`sorted` (returns a :py:class:`list`, which is iterable)
* :py:class:`str` *
* :py:class:`tuple` *
* :py:func:`vars` (returns a :py:class:`dict`, which is iterable)
* :py:func:`zip`

Items marked with * are iterable because the type is iterable. The others, unless otherwise marked, each return a distinct iterator type of their own. (Again, these are just the builtins. Standard library functions like those in :py:mod:`itertools` also often have distinct iterator types per function.)

Many of the unmarked items above (and some of the marked, like :py:class:`range`) used to return a :py:class:`list` instead of an iterator in Python 2. This was a waste of memory and often time. Python 3 uses iterators liberally to great effect.

However, a consequence of this is that, as mentioned above as well, every single one of these iterable types would have to implement or inherit every single one of the iterable operations, if they were to be done with "infix" style methods instead of "prefix" style functions.

Why Can Other Languages Do It?
******************************

So why can other languages use "infix" style methods? I'll let you in on a secret: most other languages don't use lazy iterables as much as Python does!

Let's use the example that u/eloquent_beaver uses in their comment:

.. code-block:: javascript

    x
        .map(f1)
        .filter(f2)
        .flatMap(f3)
        .filter(f4)
        .length()

But now let's squint a little harder and see what's going on here (comments mine):

.. code-block:: javascript

    x // which has to be an array
        .map(f1) // which returns an array
        .filter(f2) // which returns an array
        .flatMap(f3) // which returns an array
        .filter(f4) // which returns an array
        .length() // which is an array method

Wait, it's all arrays? Always has been. Every method in that chain returns a new array, which has to be constructed in memory before being passed on to the next method. In the best case, assuming every temporary array is garbage collected immediately, the memory usage is the maximum of ``x`` and the results of each method call; in the worst case, if no arrays are collected before the calls complete, the memory required is the *sum* of ``x`` and the results of each method call. In other words, the memory usage is :math:`O(n)`.

Let's now turn to the Python equivalent (comments and indentation mine):

.. code-block:: python

    len(tuple(
        filter(
            f4,
            flat_map(
                f3,
                filter(
                    f2,
                    map(
                        f1,
                        x # which can be any iterable
                    ) # which returns an iterator
                ) # which returns an iterator
            ) # which returns a generator-iterator
        ) # which returns an iterator
    )) # which only now stores the final result for len() to use

    # where flat_map, which doesn't exist in the Python stdlib,
    # is defined as follows:
    def flat_map(func: Callable[[IT], OT], iterable: Iterable[Union[IT, Iterable[IT]]]) -> Iterator[OT]:
        for x in map(func, iterable): # map()
            try:
                yield from x # flat()
            except TypeError: # not iterable
                yield x

(This is corrected slightly from their original version which crashes with a :py:exc:`TypeError` due to :py:class:`filter` objects having no :py:func:`len`.)

Unlike JavaScript, no list is constructed until the end, meaning that the memory used is only that of the last :py:func:`filter` call. In fact, this can be made to take no more memory than the largest iterable item by swapping :python:`len(tuple(...))` for :python:`sum(map(lambda _: 1, ...))` like so:

.. code-block:: python

    sum(map(lambda _: 1, filter(f4, flat_map(f3, filter(f2, map(f1, x))))))

This will *never* have more than one item in memory at a time (i.e. memory usage of :math:`O(1)`) at the cost of it being ~30% slower. (I did some benchmarks in `this StackOverflow answer <https://stackoverflow.com/a/74914941/6605349>`_.)

Comprehensions
--------------

The Reddit comment's criticism about the poor readibility of the "prefix" style function calls does stand. That's (one reason) why Python introduced comprehensions, and in particular (eventually) generator comprehensions. The last example above can be rewritten, albeit less efficiently, as:

.. code-block:: python

    sum(1 for z in flat_map(f3, (f1(y) for y in x if f2(f1(y)))) if f4(z))

Or, if you're willing to reintroduce one :py:func:`map` call:

.. code-block:: python

    sum(1 for z in flat_map(f3, (y for y in map(f1, x) if f2(y))) if f4(z))

This isn't a particularly good example of the power of comprehensions, because of the ``flat_map()`` and the fact that the expressions are just function calls. A better example might be the following Elixir snippet:

.. code-block:: elixir

    all_words
    |> Enum.filter(&(byte_size(&1) == n))
    |> Enum.map(&String.codepoints/1)
    |> Enum.filter(&word_ok(&1, board_t))

In Python you could write it with functions as:

.. code-block:: python

    list(filter(
        lambda chars: word_ok(x, board_t),
        map(
            list,
            filter(
                lambda word: len(word) == n,
                all_words
            )
        )
    ))

Or more readably with comprehensions as:

.. code-block:: python

    [chars for word in all_words
     if len(word) == n and word_ok(chars := list(word), board_t)]

I will concede that in a fair few situations, the chained "infix" syntax can't really be beat by comprehensions. (It's at times like this that I wish Python had Elixir's pipe operator, as demonstrated nicely above.) However, I don't think this is as relevant an issue as u/eloquent_beaver thinks it is, for two reasons:

* Python was not designed as a functional language and while it does its best to support functional programming styles, it is under no obligation to. I value the lazy iterator mechanics more.
* If you're writing something that needs enough chained iterable operations for comprehensions to become unreadable, you're doing something wrong.

Conclusion
----------

I'm not sure what the point of this was. I guess I just sort of wanted to express my enjoyment of Python's iterable mechanics, and defend it against the scorn of those who do not use it. Don't read into this too far. Happy holidays.
