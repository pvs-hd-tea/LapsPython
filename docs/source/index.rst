.. LapsPython documentation master file, created by
   sphinx-quickstart on Sun Aug 21 23:00:30 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

LapsPython
======================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Extension of LAPS [#]_ to synthesize Python and R programs
----------------------------------------------------------

Developed within the scope of the advanced software practical **AI Methods and Tools for Programming** offered by the `Parallel and Distributed Systems Group <https://pvs.ifi.uni-heidelberg.de/>`_ at the Institute of Computer Science at Heidelberg University under supervision by Prof. Dr. Artur Andrzejak.

Credits of package **dreamcoder** go to the contributors of `https://github.com/ellisk42/ec <https://github.com/ellisk42/ec/tree/icml_2021_supplement>`_. Changes made to this package:

#. dreamcoder/translation.py: decrease memory allocation from 64 GB to 4 GB (line 341)
#. dreamcoder/domains/re2/re2Primitives.py: fix exception handling in lines 47, 68
#. Added the following files with translations of Python primitives to R:

   * dreamcoder/domains/list/listPrimitives.R
   
   * dreamcoder/domains/re2/re2Primitives.R
   
   * dreamcoder/domains/text/textPrimitives.R
  
The LapsPython repository contains only the files necessary to run the LapsPython functionality. Compiled OCaml solvers and Moses, which are required to run LAPS itself, are system-dependent and not provided. They are not needed to run LapsPython, as it can interact with LAPS checkpoints. These checkpoints are provided.

Accounting
----------

99% of work done by myself. Some issues based on the original project plan created by Enisa Szabo.


Contents
--------

.. toctree::

   quickstart
   tutorial
   metrics
   api/index

.. sidebar-links::

   GitHub Repository <https://github.com/pvs-hd-tea/LapsPython>
   Test Coverage Report <https://pvs-hd-tea.github.io/LapsPython/coverage/>
   Presentations <https://pvs-hd-tea.github.io/LapsPython/presentations/>

References
----------

.. [#] Wong, C., Ellis, K., Tenenbaum, J. B., & Andreas, J. (2021). Leveraging Language to Learn Program Abstractions and Search Heuristics. arXiv. `https://doi.org/10.48550/ARXIV.2106.11053 <https://doi.org/10.48550/ARXIV.2106.11053>`_
