Metrics
=======

.. _quality:

Code Quality
------------

**Lines of Code**

Total lines of code, excluding comments, docstrings and blank lines:

* main code: 775
* tests: 430
* ratio of main code to test code: 1.80

**Test Coverage**

A detailed coverage report can be found `here <./coverage/index.html>`_
and will be updated locally each time the :ref:`unit test workflow <ci>` is executed.

In a total of 50 test cases, 94% coverage is achieved with module-wise scores ranging from 88% to 100%. Out of 666 statements,
only 43 are not covered by tests, most of which handle special cases not present in the current dataset or exceptions not raised by the current version.

**Clean Code**

The code achieves a PEP-8 score of 100% according to `Flake8 <https://flake8.pycqa.org/en/latest/>`_ used with a large 
selection of extensions for stricter linting in compliance with modern Python standards and Clean Code conventions.
In addition, `Mypy <http://www.mypy-lang.org/>`_ and `Bandit <https://bandit.readthedocs.io/en/latest/>`_
verify the absence of typing and security issues.

Results
-------

LapsPython is evaluated on 2 different checkpoints of the **re2** (string editing) domain:

* **re2_test**: A small checkpoint saved after 3 iterations of LAPS, including 75 synthesized programs in 18 tasks.
* **re2_best_dsl_language**: A large checkpoint provided by the developers of LAPS, including 1646 synthesized programs in 346 tasks.

The **re2_test** checkpoint is 100% solved by LapsPython, providing bug-free translations for all synthesized programs.

In the **re2_best_dsl_language** checkpoint, 8% of tasks are solved, i.e., contain at least one program with a 100% bug-free translation.
Present bugs are commonly a wrong resolution of variables: Invented primitives are called with wrong arguments or a wrong number of arguments.

These values are taken from the Python translations since code verification is not implemented for R. Judging by manual observation of a large sample of R translations, everything that works for Python also works for R.

Example (Flawed Translation)
++++++++++++++++++++++++++++

**Task:** if there is any letter, add v after that

**Program:** ``(lambda (#(lambda (lambda (_rflatten (map $0 (_rsplit _rdot $1))))) $0 (lambda (_rconcat $0 _v))))``

**Generated Translation:**

.. code-block:: python

    import re

    def f8(arg1, arg2):
        rsplit_1 = __regex_split('.', arg2)
        map_1 = list(map(arg1, rsplit_1))
        return "".join(map_1)

    def __regex_split(s1, s2):
        # Splits s2 on regex s1 as delimiter, including the matches
        try:
            # Special case -- we override splitting on "" to be splitting on "."
            # to match OCaml.
            if len(s1) == 0: s1 = "."
            ret = []
            remaining = s2
            m = re.search(re.compile(s1), remaining)
            while m is not None:
                prefix = remaining[0:m.start()]
                if len(prefix) > 0:
                    ret.append(prefix)
                ret.append(remaining[m.start():m.end()])
                remaining = remaining[m.end():]
                m = re.search(re.compile(s1), remaining)
            if len(remaining) > 0:
                ret.append(remaining)
            return ret        
        except:
            return [s2]

    def re2_train_41_if_there_is_any_letter_add_v_after_that(arg1):
        rconcat_1 = arg1 + 'v'
        return f8(f8_0, arg1, lambda lx: lx + 'v')

**Fixed Translation:**

.. code-block:: python

    # [...]

    def re2_train_41_if_there_is_any_letter_add_v_after_that(arg1):
        return f8(lambda lx: lx + 'v', arg1)
