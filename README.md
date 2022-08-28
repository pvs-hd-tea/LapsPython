# LapsPython
## Extension of LAPS[^1] to synthesize Python and R programs

**Full documentation: https://pvs-hd-tea.github.io/LapsPython/**

Developed within the scope of the advanced software practical "AI Methods and Tools for Programming" offered by the [Parallel and Distributed Systems Group](https://pvs.ifi.uni-heidelberg.de) at the Institute of Computer Science at Heidelberg University under supervision by Prof. Dr. Artur Andrzejak.

Credits of package `dreamcoder` go to the contributors of [https://github.com/ellisk42/ec](https://github.com/ellisk42/ec/tree/icml_2021_supplement).

This repository contains only the files necessary to run the LapsPython functionality. Compiled OCaml solvers and Moses, which are required to run LAPS itself, are system-dependent and not provided.

[^1]: Wong, C., Ellis, K., Tenenbaum, J. B., & Andreas, J. (2021). Leveraging Language to Learn Program Abstractions and Search Heuristics. arXiv. https://doi.org/10.48550/ARXIV.2106.11053 

## 1-Click-Demo
**Requirements: Conda, bash**

Simply run the script `1-click-demo.sh`. It serves as a setup script that will also run tests and the main functionality in a virtual environment. In detail, it executes the following steps:

1. Create and activate a Conda environment `lapspython` running on Python 3.7
2. Install all LAPS requirements and used dev packages in a local Pipenv environment
3. Run CI scripts
   - Linting
   - Static Typechecking
   - Unit Tests
6. Run a demo script launching the LapsPython pipeline for LAPS checkpoints in the re2 domain in Python mode and in R mode

Delete the Pipenv environment (~1.8 GB) by removing the contents of `LapsPython/.venv`. Delete the Conda environment (~218 MB) by running the command `conda env remove --name lapspython`.
