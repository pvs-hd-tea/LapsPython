"""A setuptools based setup module.
See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
Modified by Madoshakalaka@Github (dependency links added)
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path

# io.open is needed for projects that support Python 2.7
# It ensures open() defaults to text mode with universal newlines,
# and accepts an argument to specify the text encoding
# Python 3 only projects can skip this import
from io import open

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    # This is the name of your project. The first time you publish this
    # package, this name will be registered for you. It will determine how
    # users can install this project, e.g.:
    #
    # $ pip install sampleproject
    #
    # And where it will live on PyPI: https://pypi.org/project/sampleproject/
    #
    # There are some restrictions on what makes a valid project name
    # specification here:
    # https://packaging.python.org/specifications/core-metadata/#name
    name="lapspython",  # Required
    # Versions should comply with PEP 440:
    # https://www.python.org/dev/peps/pep-0440/
    #
    # For a discussion on single-sourcing the version across setup.py and the
    # project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version="1.0.0",  # Required
    # This is a one-line description or tagline of what your project does. This
    # corresponds to the "Summary" metadata field:
    # https://packaging.python.org/specifications/core-metadata/#summary
    description="Extension of LAPS to synthesize Python and R programs",  # Optional
    # This is an optional longer description of your project that represents
    # the body of text which users will see when they visit PyPI.
    #
    # Often, this is the same as your README, so you can just read it in from
    # that file directly (as we have already done above)
    #
    # This field corresponds to the "Description" metadata field:
    # https://packaging.python.org/specifications/core-metadata/#description-optional
    long_description=long_description,  # Optional
    # Denotes that our long_description is in Markdown; valid values are
    # text/plain, text/x-rst, and text/markdown
    #
    # Optional if long_description is written in reStructuredText (rst) but
    # required for plain-text or Markdown; if unspecified, "applications should
    # attempt to render [the long_description] as text/x-rst; charset=UTF-8 and
    # fall back to text/plain if it is not valid rst" (see link below)
    #
    # This field corresponds to the "Description-Content-Type" metadata field:
    # https://packaging.python.org/specifications/core-metadata/#description-content-type-optional
    long_description_content_type="text/markdown",  # Optional (see note above)
    # This should be a valid link to your project's main homepage.
    #
    # This field corresponds to the "Home-Page" metadata field:
    # https://packaging.python.org/specifications/core-metadata/#home-page-optional
    url="https://github.com/pvs-hd-tea/LapsPython",  # Optional
    # This should be your name or the name of the organization which owns the
    # project.
    author="Christopher Brückner",  # Optional
    # This should be a valid email address corresponding to the author listed
    # above.
    author_email="brueckner@stud.uni-heidelberg.de",  # Optional
    # Classifiers help users find your project by categorizing it.
    #
    # For a list of valid classifiers, see https://pypi.org/classifiers/
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 5 - Production/Stable",
        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        "Topic :: Program Synthesis :: Code-to-Code Translation",
        # Pick your license as you wish
        "License :: MIT License",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        # These classifiers are *not* checked by 'pip install'. See instead
        # 'python_requires' below.
        "Programming Language :: Python :: 3.7",
    ],
    # This field adds keywords for your project which will appear on the
    # project page. What does your project relate to?
    #
    # Note that this is a string of words separated by whitespace, not a list.
    keywords="dreamcoder laps translation lisp python r",  # Optional
    # You can just specify package directories manually here if your project is
    # simple. Or you can use find_packages().
    #
    # Alternatively, if you just want to distribute a single Python file, use
    # the `py_modules` argument instead as follows, which will expect a file
    # called `my_module.py` to exist:
    #
    #   py_modules=["my_module"],
    #
    packages=find_packages(exclude=["docs", "tests"]),  # Required
    # Specify which Python versions you support. In contrast to the
    # 'Programming Language' classifiers above, 'pip install' will check this
    # and refuse to install the project if the version does not match. If you
    # do not support Python 2, you can simplify this to '>=3.5' or similar, see
    # https://packaging.python.org/guides/distributing-packages-using-setuptools/#python-requires
    python_requires="==3.7.*",
    # This field lists other packages that your project depends on to run.
    # Any package you put here will be installed by pip when your project is
    # installed, so they must be valid existing projects.
    #
    # For an analysis of "install_requires" vs pip's requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['appnope==0.1.0', 'attrs==19.3.0', 'backcall==0.1.0', 'bleach==3.1.1', 'box2d-kengz==2.3.3', 'cairocffi==1.0.2', 'certifi==2019.3.9', 'cffi==1.12.3', 'chardet==3.0.4', 'colorama==0.4.1', 'cycler==0.10.0', 'decorator==4.4.1', 'defusedxml==0.6.0', 'dill==0.2.9', 'docopt==0.6.2', 'entrypoints==0.3', 'frozendict==1.2', 'graphviz==0.11', 'idna==2.8', 'imageio==2.6.1', 'importlib-metadata==1.5.0', 'ipykernel==5.1.4', 'ipython==7.12.0', 'ipython-genutils==0.2.0', 'ipywidgets==7.5.1', 'jedi==0.16.0', 'jinja2==2.11.1', 'joblib==0.13.2', 'jsonschema==3.2.0', 'jupyter==1.0.0', 'jupyter-client==6.0.0', 'jupyter-console==6.1.0', 'jupyter-core==4.6.3', 'kiwisolver==1.1.0', 'markupsafe==1.1.1', 'matplotlib==3.1.0', 'mistune==0.8.4', 'multiprocess==0.70.7', 'nbconvert==5.6.1', 'nbformat==5.0.4', 'nltk==3.4.1', 'notebook==6.0.3', 'num2words==0.5.10', 'numpy==1.16.4', 'pandas==1.0.3', 'pandocfilters==1.4.2', 'parso==0.6.1', 'pathos==0.2.3', 'pexpect==4.8.0', 'pickleshare==0.7.5', 'pillow==6.0.0', 'pox==0.2.5', 'ppft==1.6.4.9', 'prometheus-client==0.7.1', 'prompt-toolkit==3.0.3', 'protobuf==3.8.0', 'psutil==5.6.2', 'ptyprocess==0.6.0', 'pycparser==2.19', 'pygame==1.9.6', 'pygments==2.5.2', 'pyparsing==2.4.0', 'pypng==0.0.19', 'pyrsistent==0.15.7', 'python-dateutil==2.8.0', 'pytorch-nlp==0.5.0', 'pytz==2019.1', 'pyzmq==18.0.1', 'qtconsole==4.6.0', 'requests==2.22.0', 'scikit-learn==0.21.2', 'scipy==1.3.0', 'seaborn==0.10.1', 'send2trash==1.5.0', "setuptools==65.3.0; python_version >= '3.7'", 'sexpdata==0.0.3', 'six==1.12.0', 'terminado==0.8.3', 'testpath==0.4.4', 'torch==1.1.0', 'torchvision==0.3.0', 'tornado==6.0.3', 'tqdm==4.40.0', 'traitlets==4.3.3', 'uniplot==0.5.0', 'urllib3==1.25.3', 'wcwidth==0.1.8', 'webencodings==0.5.1', 'widgetsnbextension==3.5.1', 'zipp==3.0.0'],  # Optional
    # List additional groups of dependencies here (e.g. development
    # dependencies). Users will be able to install these using the "extras"
    # syntax, for example:
    #
    #   $ pip install sampleproject[dev]
    #
    # Similar to `install_requires` above, these must be valid existing
    # projects.
    extras_require={"dev": ['alabaster==0.7.12', "apeye==1.2.0; python_full_version >= '3.6.1'", "astor==0.8.1; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'", "astpretty==2.1.0; python_full_version >= '3.6.1'", 'attrs==19.3.0', "autodocsumm==0.2.9; python_version >= '3.7'", "babel==2.10.3; python_version >= '3.6'", "bandit==1.7.4; python_version >= '3.7'", "beautifulsoup4==4.11.1; python_version >= '3.6'", "cachecontrol[filecache]==0.12.11; python_version >= '3.6'", 'cached-property==1.5.2', 'cerberus==1.3.4', 'certifi==2019.3.9', 'chardet==3.0.4', "charset-normalizer==2.1.1; python_version >= '3.6'", 'colorama==0.4.1', "coverage[toml]==6.4.4; python_version >= '3.7'", "cssutils==2.6.0; python_version >= '3.7'", "dict2css==0.3.0; python_version >= '3.6'", 'distlib==0.3.6', "docutils==0.17.1; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'", "domdf-python-tools==3.3.0; python_version >= '3.6'", 'eradicate==2.1.0', 'flake8==4.0.1', "flake8-annotations-complexity==0.0.7; python_version >= '3.7'", 'flake8-awesome==1.3.0', "flake8-bandit==3.0.0; python_version >= '3.6'", "flake8-breakpoint==1.1.0; python_version >= '3.6' and python_version < '4.0'", "flake8-bugbear==22.8.23; python_version >= '3.6'", 'flake8-builtins==1.5.3', "flake8-comprehensions==3.10.0; python_version >= '3.7'", 'flake8-docstrings==1.6.0', "flake8-eradicate==1.3.0; python_version >= '3.6' and python_version < '4.0'", "flake8-expression-complexity==0.0.11; python_version >= '3.7'", "flake8-if-expr==1.0.4; python_version >= '3.6' and python_version < '4.0'", 'flake8-isort==4.2.0', 'flake8-logging-format==0.7.5', "flake8-plugin-utils==1.3.2; python_version >= '3.6' and python_version < '4.0'", 'flake8-polyfill==1.0.2', "flake8-print==5.0.0; python_version >= '3.7'", 'flake8-pytest==1.4', "flake8-pytest-style==1.6.0; python_version < '4.0' and python_full_version >= '3.6.2'", 'flake8-quotes==3.3.1', 'flake8-requirements==1.6.0', "flake8-return==1.1.3; python_version >= '3.6' and python_version < '4.0'", 'flake8-rst-docstrings==0.2.7', 'flake8-simplify==0.19.3', 'flake8-use-fstring==1.4', "gitdb==4.0.9; python_version >= '3.6'", "gitpython==3.1.27; python_version >= '3.7'", "html5lib==1.1; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'", 'idna==2.8', "imagesize==1.4.1; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'", 'importlib-metadata==1.5.0', 'iniconfig==1.1.1', 'isort==5.10.1', 'jinja2==2.11.1', 'lockfile==0.12.2', 'markupsafe==1.1.1', 'mccabe==0.6.1', 'msgpack==1.0.4', 'mypy==0.971', 'mypy-extensions==0.4.3', "natsort==8.1.0; python_version >= '3.6'", 'orderedmultidict==1.0.1', "packaging==20.9; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'", "pbr==5.10.0; python_version >= '2.6'", "pep517==0.13.0; python_version >= '3.6'", "pep8-naming==0.13.2; python_version >= '3.7'", "pip==22.2.2; python_version >= '3.7'", "pip-shims==0.7.3; python_version >= '3.6'", 'pipenv-setup==3.2.0', 'pipfile==0.0.2', "platformdirs==2.5.2; python_version >= '3.7'", "plette[validation]==0.2.3; python_version >= '2.6' and python_version not in '3.0, 3.1, 3.2, 3.3'", "pluggy==1.0.0; python_version >= '3.6'", "py==1.11.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'", "pycodestyle==2.8.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'", "pydocstyle==6.1.1; python_version >= '3.6'", "pyflakes==2.4.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'", 'pygments==2.5.2', 'pyparsing==2.4.0', 'pytest==7.1.2', 'pytest-cov==3.0.0', 'python-dateutil==2.8.0', 'pytz==2019.1', "pyyaml==6.0; python_version >= '3.6'", 'requests==2.22.0', "requirementslib==1.6.9; python_version >= '3.7'", 'restructuredtext-lint==1.4.0', "ruamel.yaml==0.17.21; python_version >= '3'", "ruamel.yaml.clib==0.2.6; python_version < '3.11' and platform_python_implementation == 'CPython'", "setuptools==65.3.0; python_version >= '3.7'", 'six==1.12.0', "smmap==5.0.0; python_version >= '3.6'", 'snowballstemmer==2.2.0', "soupsieve==2.3.2.post1; python_version >= '3.6'", "sphinx==4.3.2; python_version >= '3.6'", "sphinx-autodoc-typehints==1.17.1; python_version >= '3.7'", "sphinx-jinja2-compat==0.1.2; python_version >= '3.6'", 'sphinx-prompt==1.5.0', 'sphinx-rtd-theme==1.0.0', "sphinx-tabs==3.4.0; python_version ~= '3.7'", 'sphinx-toolbox==3.2.0', "sphinxcontrib-applehelp==1.0.2; python_version >= '3.5'", "sphinxcontrib-devhelp==1.0.2; python_version >= '3.5'", "sphinxcontrib-htmlhelp==2.0.0; python_version >= '3.6'", "sphinxcontrib-jsmath==1.0.1; python_version >= '3.5'", "sphinxcontrib-qthelp==1.0.3; python_version >= '3.5'", "sphinxcontrib-serializinghtml==1.1.5; python_version >= '3.5'", "stevedore==3.5.0; python_version >= '3.6'", "tabulate==0.8.10; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'", "toml==0.10.2; python_version >= '2.6' and python_version not in '3.0, 3.1, 3.2, 3.3'", "tomli==2.0.1; python_version < '3.11'", "tomlkit==0.11.4; python_version >= '3.6' and python_version < '4.0'", "typed-ast==1.5.4; python_version < '3.8'", "typing-extensions==4.3.0; python_version >= '3.7'", "typing-inspect==0.8.0; python_version < '3.8'", 'urllib3==1.25.3', "vistir==0.5.6; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'", 'webencodings==0.5.1', "wheel==0.37.1; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'", 'zipp==3.0.0',]},  # Optional
    # If there are data files included in your packages that need to be
    # installed, specify them here.
    #
    # Sometimes you’ll want to use packages that are properly arranged with
    # setuptools, but are not published to PyPI. In those cases, you can specify
    # a list of one or more dependency_links URLs where the package can
    # be downloaded, along with some additional hints, and setuptools
    # will find and install the package correctly.
    # see https://python-packaging.readthedocs.io/en/latest/dependencies.html#packages-not-on-pypi
    #
    dependency_links=[],
    # If using Python 2.6 or earlier, then these have to be included in
    # MANIFEST.in as well.
    # package_data={"sample": ["package_data.dat"]},  # Optional
    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files
    #
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    # data_files=[("my_data", ["data/data_file"])],  # Optional
    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # `pip` to create the appropriate form of executable for the target
    # platform.
    #
    # For example, the following would provide a command called `sample` which
    # executes the function `main` from this package when invoked:
    # entry_points={"console_scripts": ["sample=sample:main"]},  # Optional
    # List additional URLs that are relevant to your project as a dict.
    #
    # This field corresponds to the "Project-URL" metadata fields:
    # https://packaging.python.org/specifications/core-metadata/#project-url-multiple-use
    #
    # Examples listed include a pattern for specifying where the package tracks
    # issues, where the source is hosted, where to say thanks to the package
    # maintainers, and where to support the project financially. The key is
    # what's used to render the link text on PyPI.
    project_urls={  # Optional
        "Bug Reports": "https://github.com/pvs-hd-tea/LapsPython/issues",
        "Source": "https://github.com/pvs-hd-tea/LapsPython",
    },
)