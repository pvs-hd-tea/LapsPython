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
  

Contents
--------

.. toctree::

   usage

References
----------

.. [#] Wong, C., Ellis, K., Tenenbaum, J. B., & Andreas, J. (2021). Leveraging Language to Learn Program Abstractions and Search Heuristics. arXiv. `https://doi.org/10.48550/ARXIV.2106.11053 <https://doi.org/10.48550/ARXIV.2106.11053>`_