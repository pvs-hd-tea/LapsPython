Tutorial
========

.. _functionality:

Functionality
-------------

LapsPython extends the pipeline of LAPS, a program synthesizer for input-output examples, with a translation from LISP-like code to Python and R. To put this into a more comprehensible context, let's take a look what exactly happens in the LAPS pipeline:

#. A library of primitives, i.e., simple functions implemented in Python, is loaded for a given domain such as string editing. Internally, this library is called **grammar**.
#. For a set of input-output examples with natural language annotations, primitives from the current library are pieced together to a small program. This set of examples is called a **task** and it is solved if the synthesized program produces the correct outputs for all given inputs. Synthesization is guided by a neural network ("recognition model") as well as a statistical machine translation system (`Moses <http://www2.statmt.org/moses/>`_). Internally, a task is also called **frontier**.
#. New concepts are learned: Small subprograms that appear in many task-solving programs are added to the library as "invented primitives".
#. Synthesized programs are compressed by substituting the beforementioned subprograms with the corresponding invented primitives.
#. The result of the current iteration are stored in a single checkpoint: The new grammar, all synthesized programs, and the posterior probabilities of all such programs. A larger probability means that a program provides a more generalizable solution. Internally, the largest posterior probability is called **best posterior** which leads to interesting results when you google it.

This is where LapsPython comes into play. It can either be injected directly into the LAPS code and work with the constructed "ECResult" object, or simply load an arbitrary checkpoint. It will execute the following analoguous steps:

#. The Python/R implementations of all pre-implemented primitives in the grammar are parsed.
#. A translator is initialized using the parsed implementations as "backend" and translates the invented primitives.
#. The synthesized programs are extracted and translated. The correctness of these translations is verified using the same input-output examples.
#. Results are stored in a JSON file: The entire grammar including Python/R translations and all synthesized programs including the correct translation with the largest posterior probability as well as the incorrect translation with the largest posterior probability, if these exist.
#. Descriptive statistics are computed: How many translations are correct, how many tasks are solved (i.e., have at least 1 correct translation), the min/max/mean/median percentage of correct translations per task.


Basic Usage
-----------

LapsPython is easy to use since all previously described steps are executed by a single :doc:`Pipeline <api/lapspython.pipeline>` object. You can either pass an ECResult object to ``Pipeline.extract_translate()``, or the file name (excluding the file extension) of a checkpoint to ``Pipeline.from_checkpoint()``. Checkpoints need to be placed into the ``checkpoints`` folder first.

By default, LapsPython translates to Python. Alternatively, translation to R is possible by passing the argument ``mode='r'``. If you want to work with a new domain, it will be necessary to manually re-implement the required Python primitives in R.

Python primitives can be found found in ``dreamcoder/domains/<domain>/<domain>Primitives.py``. R primitives require the same path and file name but the **.R** file extension. LapsPython assumes the following conventions when parsing primitives:

* Python primitives start with 1 underscore. Functions called by Python primitives start with 2 underscores.
* R primitives have the same names as their Python equivalents but without preceding underscores. They are separated by at least 1 empty line. The left brace **{** is in the same line as the function header.

LapsPython pipelines :doc:`GrammarParser <api/lapspython.extraction>`, :doc:`Translator <api/lapspython.translation>`, :doc:`ProgramExtractor <api/lapspython.extraction>` and :doc:`Statistics <api/lapspython.stats>` objects. Results are saved in ``checkpoints/<checkpoint>_<mode>.json`` where **<checkpoint>** is the corresponding checkpoint name and **<mode>** can be ``python`` or ``r``.

You notice that an invented primitive is translated incorrectly, resulting in many bad translations? You can fix it in the generated JSON file! It will be loaded the next you load the same checkpoint.

Development
-----------

Most classes can be found in the :doc:`lapspython.types <api/lapspython.types>` module:

* The parsing of Python and R primitives is handled by ``ParsedPrimitive`` and ``ParsedRPrimitive``.
* In analogy, invented primitives are parsed by ``ParsedInvented`` and ``ParsedRInvented``.
* ``ParsedGrammar``, ``ParsedProgram``, ``ParsedRProgram``, ``CompactFrontier`` and ``CompactResult`` are mostly data classes and store important information from both LAPS and LapsPython in a more concise and usable format.

The :doc:`lapspython.extraction <api/lapspython.extraction>` module handles the extraction of grammars and synthesized programs. It works on data taken from an ``ECResult`` object which is saved as a checkpoint by LAPS.

* ``GrammarParser`` takes a grammar and a mode (``'python'`` or ``'r'``) as arguments and returns a ``ParsedGrammar``, containing all parsed primitives in the given language.
* ``ProgramExtractor`` takes an ``ECResult`` and a ``Translator`` as arguments and returns a ``CompactResult``. It contains all synthesized programs, their translations and their task descriptions, categorized in HIT/MISS frontiers (MISS frontiers are tasks not solved by LAPS) and working/buggy translations, sorted by their best posterior probabilities.

Since the translation is still flawed, a good entry-point to continue the development is the ``Translator`` class in the :doc:`lapspython.translation <api/lapspython.translation>` module. A ``Translator`` takes a ``ParsedGrammar`` object as argument which it will base its translation on. It returns a ``ParsedProgram`` or ``ParsedRProgram`` object, depending on the language of the passed grammar.

One further entry-point can be the :doc:`ParsedRProgram <api/lapspython.types>` class since it currently does not verify the correctness of R translations. The Python code verification in ``ParsedProgram`` can be used as a reference, interaction with an R interpreter is necessary.

An extension to any language is possible by translating the Python primitives to this language. The LapsPython code itself could be extended by either adding more modes to the ``mode`` argument (currently supporting ``'python'`` and ``'r'`` as values) or by replacing it with a ``file_extension`` argument.
