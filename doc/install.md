---
file_format: mystnb
---

# Installing

## Quickstart

The fastest way to install PyGMT is with the [mamba](https://mamba.readthedocs.io/en/latest/)
or [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/index.html)
package manager which takes care of setting up a virtual environment, as well as the
installation of GMT and all the dependencies PyGMT depends on:

:::: {tab-set}
::: {tab-item} mamba
:sync: mamba
```
mamba create --name pygmt --channel conda-forge pygmt
```
:::

::: {tab-item} conda
:sync: conda
```
conda create --name pygmt --channel conda-forge pygmt
```
:::
::::

To activate the virtual environment, you can do:

:::: {tab-set}
::: {tab-item} mamba
:sync: mamba
```
mamba activate pygmt
```
:::

::: {tab-item} conda
:sync: conda
```
conda activate pygmt
```
:::
::::

After this, check that everything works by running the following in a Python interpreter
(e.g., in a Jupyter notebook):

```{code-cell} ipython
---
tags: [hide-output]
---

import pygmt
pygmt.show_versions()
```

You are now ready to make your first figure! Start by looking at our [Intro](intro/index.rst),
[Tutorials](tutorials/index.rst), and [Gallery](gallery/index.rst). Good luck!

:::{note}
The sections below provide more detailed, step by step instructions to install and test
PyGMT for those who may have a slightly different setup or want to install the latest
development version.
:::

## Which Python?

PyGMT is tested to run on Python {{ requires.python }}.

We recommend using the [Miniforge](https://github.com/conda-forge/miniforge#miniforge3)
Python distribution to ensure you have all dependencies installed and
the [mamba](https://mamba.readthedocs.io/en/stable/user_guide/mamba.html) package manager
in the base environment. Installing Miniforge does not require administrative rights to
your computer and doesn't interfere with any other Python installations on your system.

## Which GMT?

PyGMT requires Generic Mapping Tools (GMT) {{ requires.gmt }} since there are many
changes being made to GMT itself in response to the development of PyGMT.

Compiled conda packages of GMT for Linux, macOS and Windows are provided through
[conda-forge](https://anaconda.org/conda-forge/gmt). Advanced users can also
[build GMT from source](https://github.com/GenericMappingTools/gmt/blob/master/BUILDING.md)
instead.

We recommend following the instructions further on to install GMT 6.

## Dependencies

PyGMT requires the following packages to be installed:

- [NumPy](https://numpy.org)
- [pandas](https://pandas.pydata.org)
- [Xarray](https://xarray.dev/)
- [packaging](https://packaging.pypa.io)

:::{note}
For the minimum supported versions of the dependencies, please see [](minversions.md).
:::

:::{note}
Some optional dependencies (e.g., [IPython](https://ipython.readthedocs.io/en/stable/),
[GeoPandas](https://geopandas.org/en/stable/)) add more functionality to PyGMT.
For a complete list of the optional dependencies, refer to [](ecosystem.md).
:::

## Installing GMT and other dependencies

Before installing PyGMT, we must install GMT itself along with the other dependencies.
The easiest way to do this is via the `mamba` or `conda` package manager. We recommend
working in an isolated
[virtual environment](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)
to avoid issues with conflicting versions of dependencies.

First, we must configure conda to get packages from the [conda-forge channel](https://conda-forge.org/):
```
conda config --prepend channels conda-forge
```

Now we can create a new virtual environment with Python and all our dependencies
installed (we'll call it `pygmt` but feel free to change it to whatever you want):

:::: {tab-set}
::: {tab-item} mamba
:sync: mamba
```
mamba create --name pygmt python=3.12 numpy pandas xarray packaging gmt
```
:::

::: {tab-item} conda
:sync: conda
```
conda create --name pygmt python=3.12 numpy pandas xarray packaging gmt
```
:::
::::

Activate the environment by running the following (**do not forget this step!**):

:::: {tab-set}
::: {tab-item} mamba
:sync: mamba
```
mamba activate pygmt
```
:::

::: {tab-item} conda
:sync: conda
```
conda activate pygmt
```
:::
::::

From now on, all commands will take place inside the virtual environment called `pygmt`
and won't affect your default `base` installation.

::::: {tip}
You can also enable more PyGMT functionality by installing PyGMT's optional dependencies in the environment.
:::: {tab-set}
::: {tab-item} mamba
:sync: mamba
```
mamba install contextily geopandas ipython pyarrow rioxarray
```
:::

::: {tab-item} conda
:sync: conda
```
conda install contextily geopandas ipython pyarrow rioxarray
```
:::
::::
:::::

## Installing PyGMT

Now that you have GMT installed and your virtual environment activated, you can install
PyGMT using any of the following methods.

### Using mamba/conda (recommended)

This installs the latest stable release of PyGMT from [conda-forge](https://anaconda.org/conda-forge/pygmt):

:::: {tab-set}
::: {tab-item} mamba
:sync: mamba
```
mamba install pygmt
```
:::

::: {tab-item} conda
:sync: conda
```
conda install pygmt
```
:::
::::

This upgrades the installed PyGMT version to be the latest stable release:

:::: {tab-set}
::: {tab-item} mamba
:sync: mamba
```
mamba update pygmt
```
:::

::: {tab-item} conda
:sync: conda
```
conda update pygmt
```
:::
::::

### Using pip

This installs the latest stable release from [PyPI](https://pypi.org/project/pygmt):
```
python -m pip install pygmt
```

::: {tip}
You can also run `python -m pip install pygmt[all]` to install PyGMT with all of its
optional dependencies.
:::

Alternatively, you can install the latest development version from
[TestPyPI](https://test.pypi.org/project/pygmt):
```
python -m pip install --pre --extra-index-url https://test.pypi.org/simple/ pygmt
```

To upgrade the installed stable release or development version to be the latest one,
just add `--upgrade` to the corresponding command above.

Any of the above methods (mamba/conda/pip) should allow you to use the PyGMT package
from Python.

## Testing your install

To ensure that PyGMT and its dependencies are installed correctly, run the following
in your Python interpreter:

```{code-cell} ipython
---
tags: [hide-output]
---

import pygmt
pygmt.show_versions()
```

```{code-cell} ipython
fig = pygmt.Figure()
fig.coast(projection="N15c", region="g", frame=True, land="tan", water="lightblue")
fig.text(position="MC", text="PyGMT", font="80p,Helvetica-Bold,red@75")
fig.show()
```

You should see a global map with land and water masses colored in tan and lightblue
respectively. On top, there should be the semi-transparent text "PyGMT". If the
semi-transparency does not show up, there is probably an incompatibility between your
GMT and Ghostscript versions. For details, please run `pygmt.show_versions()` and see
[Not working transparency](#not-working-transparency).

## Common installation issues

If you have any issues with the installation, please check out the following common
problems and solutions.

### "Error loading GMT shared library at ..."

Sometimes, PyGMT will be unable to find the correct version of the GMT shared library
(`libgmt`). This can happen if you have multiple versions of GMT installed.

You can tell PyGMT exactly where to look for `libgmt` by setting the environment
variable {term}`GMT_LIBRARY_PATH` to the directory where `libgmt.so`, `libgmt.dylib` or
`gmt.dll` can be found on Linux, macOS or Windows, respectively.

For Linux/macOS, add the following line to your shell configuration file (usually
`~/.bashrc` for Bash on Linux and `~/.zshrc` for Zsh on macOS):
```
export GMT_LIBRARY_PATH=$HOME/miniforge3/envs/pygmt/lib
```

For Windows, add the environment variable {term}`GMT_LIBRARY_PATH` following these
[instructions](https://www.wikihow.com/Create-an-Environment-Variable-in-Windows-10)
and set its value to a path like:
```
C:\Users\USERNAME\Miniforge3\envs\pygmt\Library\bin\
```

### `ModuleNotFoundError` in Jupyter notebook environment

If you can successfully import PyGMT in a Python interpreter or IPython, but get a
`ModuleNotFoundError` when importing PyGMT in Jupyter, you may need to activate your
`pygmt` virtual environment (using `mamba activate pygmt` or `conda activate pygmt`)
and install a `pygmt` kernel following the commands below:
```
python -m ipykernel install --user --name pygmt  # install virtual environment properly
jupyter kernelspec list --json
```

After that, you need to restart Jupyter, open your notebook, select the `pygmt` kernel
and then import pygmt.


### Not working transparency

It is known that some combinations of GMT and Ghostscript versions cause issues,
especially regarding transparency. If the transparency doesn't work in your figures,
please check your GMT and Ghostscript versions (you can run `pygmt.show_versions()`).
We recommend:

- Ghostscript 9.53-9.56 for GMT 6.4.0 (or below)
- Ghostscript 10.03 or later for GMT 6.5.0
