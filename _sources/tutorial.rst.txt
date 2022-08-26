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

#. The Python/R implementations of all primitives in the library are loaded.
#. The invented primitives are translated.
#. The synthesized programs are translated. The correctness of the translations is verified using the same input-output examples.
#. Results are stored in a JSON file: The entire grammar including Python/R translations and all synthesized programs including the correct translation with the largest posterior probability as well as the incorrect translation with the largest posterior probability, if these exist.
#. Descriptive statistics are computed: How many translations are correct, how many tasks are solved (i.e., have at least 1 correct translation), the min/max/mean/median percentage of correct translations per task.

Please note that the LapsPython repository only contains the dreamcoder files necessary to run the LapsPython functionality. Compiled OCaml solvers and Moses, which are required to run LAPS, are not provided.

Usage
-----

LapsPython is easy to use since all previously described steps are executed by a single :doc:`Pipeline <api/lapspython.pipeline>` object. You can either pass an ECResult object to ``Pipeline.extract_translate()``, or the file name (exclusing the file extension) of a checkpoint to ``Pipeline.from_checkpoint()``. Checkpoints need to be placed into the ``checkpoints`` folder first.

By default, LapsPython translates to Python. Alternatively, translation to R is possible by passing the argument ``mode='R'`` to the two pipeline functions. If you work with a new domain, it will be necessary to manually re-implement the Python primitives in R.

Python primitives can be found found in ``dreamcoder/domains/<name>/<name>Primitives.py``. R primitives require the same path and file name, but the ``.R`` file extension. LapsPython assumes the following conventions when loading primitives:

* Python primitives start with 1 underscore, functions called by Python primitives start with 2 underscores.
* R primitives have the same names as their Python equivalents but without preceding underscores, and they are separated by at least 1 empty line.

LapsPython pipelines :doc:`GrammarParser <api/lapspython.extraction>`, :doc:`ProgramExtractor <api/lapspython.extraction>`, :doc:`Translator <api/lapspython.translation>` and :doc:`Statistics <api/lapspython.stats>` objects. Results will be stored in a ``checkpoints/<name><mode>.json`` where ``<name>`` is the corresponding checkpoint name and ``<mode>`` can be ``python`` or ``r``.

You notice that an invented primitive is translated incorrectly, resulting in many bad translations? You can fix it in the generated JSON file! It will be loaded the next you load the same checkpoint.
