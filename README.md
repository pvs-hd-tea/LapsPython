# LapsPython
## Extension of LAPS[^1] to synthesize Python and R programs
Developed within the scope of the advanced software practical "AI Methods and Tools for Programming" offered by the [Parallel and Distributed Systems Group](https://pvs.ifi.uni-heidelberg.de) at the Institute of Computer Science at Heidelberg University under supervision by Prof. Dr. Artur Andrzejak.

Credits of package `dreamcoder` go to the contributors of [https://github.com/ellisk42/ec](https://github.com/ellisk42/ec/tree/icml_2021_supplement). Changes made to this package:

- `dreamcoder/translation.py`: decrease memory allocation from 64 GB to 4 GB (line 341)
- `dreamcoder/domains/re2/re2Primitives.py`: fix exception handling in lines 47, 68
- Added the following files with translations of Python primitives to R:
  - `dreamcoder/domains/list/listPrimitives.R`
  - `dreamcoder/domains/re2/re2Primitives.R`
  - `dreamcoder/domains/text/textPrimitives.R`
  
**This repository currently contains only the files required to run the LapsPython functionality! If you want to run LAPS itself, refer to the LapsTrans project which provides binaries compiled for Ubuntu 20.04.**

[^1]: Wong, C., Ellis, K., Tenenbaum, J. B., & Andreas, J. (2021). Leveraging Language to Learn Program Abstractions and Search Heuristics. arXiv. https://doi.org/10.48550/ARXIV.2106.11053 

## 1-Click-Demo
**Requirements: Conda, bash**

Simply run the script `1-click-demo.sh`. It will execute the following steps:

1. Setup and activate a Conda environment `lapspython` running on Python 3.7
2. Install Pipenv in the Conda environment (used to resolve dependencies and manage scripts)
3. Setup a local Pipenv environment in `.venv`
4. Install all LAPS requirements and used dev packages in the local Pipenv environment
5. Run CI scripts for
   - Linting
   - Static Typechecking
   - Unit Tests
6. Run a demo script launching the LapsPython pipeline for LAPS checkpoints in Python mode and in R mode

A test coverage report will be created in `LapsPython/coverage/index.html`. Delete the Pipenv environment (~1.8 GB) by removing the contents of `.venv`. Delete the Conda environment (~218 MB) by running the command `conda env remove --name lapspython`.

Alternatively, `requirements.txt` (necessary) and `requirements-dev.txt` (CI) with the same package versions are provided to install all dependencies in an environment of your choice. I do not not ensure that this will work, since it does not on my machine. 

### Pipenv scripts

The four aforementioned scripts can be run using the following commands:

- `pipenv run linting`
- `pipenv run typechecks`
- `pipenv run tests`
- `pipenv run demo`

A Python shell in the Pipenv environment can be launched with `pipenv run python`. For the sake of illustration, the demo program can also be launched with `pipenv run python demo.py`.

### Why a virtual environment inside a virtual environment?

Since all LAPS requirements are taken from different requirements.txt files which can only be installed recursively through pip, Conda is not able to resolve all dependencies. Pipenv is wrapped around pip, but resolves package dependencies better and ensures that the virtual environment can be reproduced using the portable `Pipfile.lock` file. This environment can be setup directly in the project directory, making it easy to find. Moreover, the custom scripts make it simple to run different complex workflows such as CI from a single entry point.

However, I know for sure that Conda is installed on the IWR servers and it is able to install Python 3.7 and swig (both required by LAPS), which would otherwise require apt-get and therefore superuser rights.
