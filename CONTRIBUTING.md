# Contributing Guidelines

:tada: **First off, thank you for considering contributing to our project!** :tada:

This is a community-driven project, so it's people like you that make it useful and
successful.
These are some of the many ways to contribute:

* :bug: Submitting bug reports and feature requests
* :memo: Writing tutorials or examples
* :mag: Fixing typos and improving to the documentation
* :bulb: Writing code for everyone to use

If you get stuck at any point you can create an issue on GitHub (look for the *Issues*
tab in the repository) or contact us at one of the other channels mentioned below.

For more information on contributing to open source projects,
[GitHub's own guide](https://guides.github.com/activities/contributing-to-open-source/)
is a great starting point if you are new to version control.
Also, checkout the
[Zen of Scientific Software Maintenance](https://jrleeman.github.io/ScientificSoftwareMaintenance/)
for some guiding principles on how to create high quality scientific software
contributions.


## Ground Rules

The goal is to maintain a diverse community that's pleasant for everyone.
**Please be considerate and respectful of others**.
Everyone must abide by our [Code of Conduct](CODE_OF_CONDUCT.md) and we encourage all to
read it carefully.


## Contents

* [What Can I Do?](#what-can-i-do)
* [How Can I Talk to You?](#how-can-i-talk-to-you)
* [Reporting a Bug](#reporting-a-bug)
* [Editing the Documentation](#editing-the-documentation)
  - [Gallery plots](#gallery-plots)
  - [Tutorials](#tutorials)
* [Contributing Code](#contributing-code)
  - [General guidelines](#general-guidelines)
  - [Setting up your environment](#setting-up-your-environment)
  - [Code style](#code-style)
  - [Testing your code](#testing-your-code)
  - [Testing plots](#testing-plots)
  - [Documentation](#documentation)
  - [Code Review](#code-review)


## What Can I Do?

* Tackle any issue that you wish! Some issues are labeled as **"good first issues"** to
  indicate that they are beginner friendly, meaning that they don't require extensive
  knowledge of the project.
* Make a tutorial or example of how to do something.
* Provide feedback about how we can improve the project or about your particular use
  case.
* Contribute code you already have. It doesn't need to be perfect! We will help you
  clean things up, test it, etc.


## How Can I Talk to You?

Discussion often happens in the issues and pull requests.
In addition, there is a [Discourse forum](https://forum.generic-mapping-tools.org)
for the project where you can ask questions.


## Reporting a Bug

Find the *Issues* tab on the top of the Github repository and click *New Issue*.
You'll be prompted to choose between different types of issue, like bug reports and
feature requests.
Choose the one that best matches your need.
The Issue will be populated with one of our templates.
**Please try to fillout the template with as much detail as you can**.
Remember: the more information we have, the easier it will be for us to solve your
problem.


## Editing the Documentation

If you're browsing the documentation and notice a typo or something that could be
improved, please consider letting us know by [creating an issue](#reporting-a-bug) or
submitting a fix (even better :star2:).

You can submit fixes to the documentation pages completely online without having to
download and install anything:

* On each documentation page, there should be an "Improve This Page" link at the very
  top.
* Click on that link to open the respective source file (usually an `.rst` file in the
  `doc` folder) on Github for editing online (you'll need a Github account).
* Make your desired changes.
* When you're done, scroll to the bottom of the page.
* Fill out the two fields under "Commit changes": the first is a short title describing
  your fixes; the second is a more detailed description of the changes. Try to be as
  detailed as possible and describe *why* you changed something.
* Click on the "Commit changes" button to open a
  [pull request (see below)](#pull-requests).
* We'll review your changes and then merge them in if everything is OK.
* Done :tada::beer:

Alternatively, you can make the changes offline to the files in the `doc` folder or the
example scripts. See [Contributing Code](#contributing-code) for instructions.

### Gallery plots

The gallery and tutorials are managed by
[sphinx-gallery](https://sphinx-gallery.readthedocs.io/).
The source files for the example gallery are `.py` scripts in `examples/gallery/` that
generate one or more figures. They are executed automatically by sphinx-gallery when the
documentation is built. The output is gathered and assembled into the gallery.

You can **add a new** plot by placing a new `.py` file in one of the folders inside the
`examples/gallery` folder of the repository. See the other examples to get an idea for the
format.

General guidelines for making a good gallery plot:

* Examples should highlight a single feature/command. Good: *how to add a label to
  a colorbar*. Bad: *how to add a label to the colorbar and use two different CPTs and
  use subplots*.
* Try to make the example as simple as possible. Good: use only commands that are
  required to show the feature you want to highlight. Bad: use advanced/complex Python
  features to make the code smaller.
* Use a sample dataset from `pygmt.datasets` if you need to plot data. If a suitable
  dataset isn't available, open an issue requesting one and we'll work together to add
  it.
* Add comments to explain things are aren't obvious from reading the code. Good: *Use a
  Mercator projection and make the plot 6 inches wide*. Bad: *Draw coastlines and plot
  the data*.
* Describe the feature that you're showcasing and link to other relevant parts of the
  documentation.

### Tutorials

The tutorials (the User Guide in the docs) are also built by sphinx-gallery from the
`.py` files in the `examples/tutorials` folder of the repository. To add a new tutorial:

* Include a `.py` file in the `examples/tutorials` folder on the base of the repository.
* Write the tutorial in "notebook" style with code mixed with paragraphs explaining what
  is being done. See the other tutorials for the format.
* Include the tutorial in the table of contents of the documentation (side bar). Do this
  by adding a line to the User Guide `toc` directive in `doc/index.rst`. Notice that the
  file included is the `.rst` generated by sphinx-gallery.

Guidelines for a good tutorial:

* Each tutorial should focus on a particular set of tasks that a user might want to
  accomplish: plotting grids, interpolation, configuring the frame, projections, etc.
* The tutorial code should be as simple as possible. Avoid using advanced/complex Python
  features or abbreviations.
* Explain the options and features in as much detail as possible. The gallery has
  concise examples while the tutorials are detailed and full of text.

Note that the `Figure.plot` function needs to be called for a plot to be inserted into
the documentation.


## Contributing Code

**Is this your first contribution?**
Please take a look at these resources to learn about git and pull requests (don't
hesitate to [ask questions](#how-can-i-talk-to-you)):

* [How to Contribute to Open Source](https://opensource.guide/how-to-contribute/).
* Aaron Meurer's [tutorial on the git workflow](http://www.asmeurer.com/git-workflow/)
* [How to Contribute to an Open Source Project on GitHub](https://egghead.io/courses/how-to-contribute-to-an-open-source-project-on-github)

### General guidelines

We follow the [git pull request workflow](http://www.asmeurer.com/git-workflow/) to
make changes to our codebase.
Every change made goes through a pull request, even our own, so that our
[continuous integration](https://en.wikipedia.org/wiki/Continuous_integration) services
have a change to check that the code is up to standards and passes all our tests.
This way, the *master* branch is always stable.

General guidelines for pull requests (PRs):

* **Open an issue first** describing what you want to do. If there is already an issue
  that matches your PR, leave a comment there instead to let us know what you plan to
  do.
* Each pull request should consist of a **small** and logical collection of changes.
* Larger changes should be broken down into smaller components and integrated
  separately.
* Bug fixes should be submitted in separate PRs.
* Describe what your PR changes and *why* this is a good thing. Be as specific as you
  can. The PR description is how we keep track of the changes made to the project over
  time.
* Do not commit changes to files that are irrelevant to your feature or bugfix (eg:
  `.gitignore`, IDE project files, etc).
* Write descriptive commit messages. Chris Beams has written a
  [guide](https://chris.beams.io/posts/git-commit/) on how to write good commit
  messages.
* Be willing to accept criticism and work on improving your code; we don't want to break
  other users' code, so care must be taken not to introduce bugs.
* Be aware that the pull request review process is not immediate, and is generally
  proportional to the size of the pull request.

### Setting up your environment

We highly recommend using [Anaconda](https://www.anaconda.com/download/) and the `conda`
package manager to install and manage your Python packages.
It will make your life a lot easier!

The repository includes a conda environment file `environment.yml` with the
specification for all development requirements to build and test the project.
Once you have forked and clone the repository to your local machine, you use this file
to create an isolated environment on which you can work.
Run the following on the base of the repository:

```bash
conda env create
```

Before building and testing the project, you have to activate the environment:

```bash
source activate ENVIRONMENT_NAME
```

You'll need to do this every time you start a new terminal.

See the [`environment.yml`](environment.yml) file for the list of dependencies and the
environment name.

We have a [`Makefile`](Makefile) that provides commands for installing, running the
tests and coverage analysis, running linters, etc.
If you don't want to use `make`, open the `Makefile` and copy the commands you want to
run.

To install the current source code into your testing environment, run:

```bash
make install
```

This installs your project in *editable* mode, meaning that changes made to the source
code will be available when you import the package (even if you're on a different
directory).

### Code style

We use [Black](https://github.com/ambv/black) to format the code so we don't have to
think about it.
Black loosely follows the [PEP8](http://pep8.org) guide but with a few differences.
Regardless, you won't have to worry about formatting the code yourself.
Before committing, run it to automatically format your code:

```bash
make format
```

Don't worry if you forget to do it.
Our continuous integration systems will warn us and you can make a new commit with the
formatted code.

We also use [flake8](http://flake8.pycqa.org/en/latest/) and
[pylint](https://www.pylint.org/) to check the quality of the code and quickly catch
common errors.
The [`Makefile`](Makefile) contains rules for running both checks:

```bash
make check   # Runs flake8 and black (in check mode)
make lint    # Runs pylint, which is a bit slower
```

#### Docstrings

**All docstrings** should follow the
[numpy style guide](https://numpydoc.readthedocs.io/en/latest/format.html#docstring-standard).
All functions/classes/methods should have docstrings with a full description of all
arguments and return values.

While the maximum line length for code is automatically set by *Black*, docstrings
must be formatted manually. To play nicely with Jupyter and IPython, **keep docstrings
limited to 79 characters** per line.

### Testing your code

Automated testing helps ensure that our code is as free of bugs as it can be.
It also lets us know immediately if a change we make breaks any other part of the code.

All of our test code and data are stored in the `tests` subpackage.
We use the [pytest](https://pytest.org/) framework to run the test suite.

Please write tests for your code so that we can be sure that it won't break any of the
existing functionality.
Tests also help us be confident that we won't break your code in the future.

If you're **new to testing**, see existing test files for examples of things to do.
**Don't let the tests keep you from submitting your contribution!**
If you're not sure how to do this or are having trouble, submit your pull request
anyway.
We will help you create the tests and sort out any kind of problem during code review.

Run the tests and calculate test coverage using:

    make test

The coverage report will let you know which lines of code are touched by the tests.
**Strive to get 100% coverage for the lines you changed.**
It's OK if you can't or don't know how to test something.
Leave a comment in the PR and we'll help you out.

### Testing plots

We use the [pytest-mpl](https://github.com/matplotlib/pytest-mpl) plug-in to test plot
generating code.
Every time the tests are run, `pytest-mpl` compares the generated plots with known
correct ones stored in `pygmt/tests/baseline`.
If your test created a `pygmt.Figure` object, you can test it by adding a *decorator* and
returning the `pygmt.Figure` object:

```python
@pytest.mark.mpl_image_compare
def test_my_plotting_case():
    "Test that my plotting function works"
    fig = Figure()
    fig.basemap(region=[0, 360, -90, 90], projection='W7i', frame=True)
    return fig
```

Your test function **must** return the `pygmt.Figure` object and you can only
test one figure per function.

Before you can run your test, you'll need to generate a *baseline* (a correct
version) of your plot.
Run the following from the repository root:

```bash
pytest --mpl-generate-path=baseline pygmt/tests/NAME_OF_TEST_FILE.py
```

This will create a `baseline` folder with all the plots generated in your test
file.
Visually inspect the one corresponding to your test function.
If it's correct, copy it (and only it) to `pygmt/tests/baseline`.
When you run `make test` the next time, your test should be executed and
passing.

Don't forget to commit the baseline image as well.

### Documentation

Most documentation sources are in the `doc` folder.
We use [sphinx](http://www.sphinx-doc.org/) to build the web pages from these sources.
To build the HTML files:

```bash
cd doc
make all
```

This will build the HTML files in `doc/_build/html`.
Open `doc/_build/html/index.html` in your browser to view the pages.

The API reference is manually assembled in `doc/api/index.rst`.
The *autodoc* sphinx extension will automatically create pages for each
function/class/module listed there.

You can reference classes, functions, and modules from anywhere (including docstrings)
using <code>:func:\`package.module.function\`</code>,
<code>:class:\`package.module.class\`</code>, or
<code>:mod:\`package.module\`</code>.
Sphinx will create a link to the automatically generated page for that
function/class/module.

**All docstrings** should follow the
[numpy style guide](https://numpydoc.readthedocs.io/en/latest/format.html).
All functions/classes/methods should have docstrings with a full description of all
arguments and return values.

### Code Review

After you've submitted a pull request, you should expect to hear at least a comment
within a couple of days.
We may suggest some changes or improvements or alternatives.

Some things that will increase the chance that your pull request is accepted quickly:

* Write a good and detailed description of what the PR does.
* Write tests for the code you wrote/modified.
* Readable code is better than clever code (even with comments).
* Write documentation for your code (docstrings) and leave comments explaining the
  *reason* behind non-obvious things.
* Include an example of new features in the gallery or tutorials.
* Follow the [PEP8](http://pep8.org) style guide for code and the
  [numpy guide](https://numpydoc.readthedocs.io/en/latest/format.html)
  for documentation.

Pull requests will automatically have tests run by TravisCI.
This includes running both the unit tests as well as code linters.
Github will show the status of these checks on the pull request.
Try to get them all passing (green).
If you have any trouble, leave a comment in the PR or
[get in touch](#how-can-i-talk-to-you).
