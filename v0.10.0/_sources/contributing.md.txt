# Contributors Guide

This is a community driven project and everyone is welcome to contribute.

The project is hosted at the
[PyGMT GitHub repository](https://github.com/GenericMappingTools/pygmt).

The goal is to maintain a diverse community that's pleasant for everyone.
**Please be considerate and respectful of others**. Everyone must abide by our
[Code of Conduct](https://github.com/GenericMappingTools/.github/blob/main/CODE_OF_CONDUCT.md)
and we encourage all to read it carefully.

## Ways to Contribute

### Ways to Contribute Documentation and/or Code

* Tackle any issue that you wish! Some issues are labeled as **"good first issue"** to
  indicate that they are beginner friendly, meaning that they don't require extensive
  knowledge of the project.
* Make a tutorial or gallery example of how to do something.
* Improve the API documentation.
* Contribute code! This can be code that you already have and it doesn't need to be
  perfect! We will help you clean things up, test it, etc.

### Ways to Contribute Feedback

* Provide feedback about how we can improve the project or about your particular use
  case. Open an [issue](https://github.com/GenericMappingTools/pygmt/issues) with
  feature requests or bug fixes, or post general comments/questions on the
  [forum](https://forum.generic-mapping-tools.org).
* Help triage issues, or give a "thumbs up" on issues that others reported which are
  relevant to you.

### Ways to Contribute to Community Building

* Participate and answer questions on the [PyGMT forum Q&A](https://forum.generic-mapping-tools.org/c/questions/pygmt-q-a/11).
* Participate in discussions at the quarterly PyGMT Community Meetings, which are
  announced on the [forum governance page](https://forum.generic-mapping-tools.org/c/governance/9).
* Cite PyGMT when using the project.
* Spread the word about PyGMT or star the project!

## Providing Feedback

### Reporting a Bug

* Find the [*Issues*](https://github.com/GenericMappingTools/pygmt/issues) tab on the
top of the GitHub repository and click *New issue*.
* Click on *Get started* next to *Bug report*.
* **Please try to fill out the template with as much detail as you can**.
* After submitting your bug report, try to answer any follow up questions about the bug
  as best as you can.

#### Reporting Upstream Bugs

If you are aware that a bug is caused by an upstream GMT issue rather than a
PyGMT-specific issue, you can optionally take the following steps to help resolve
the problem:

* Add the line `pygmt.config(GMT_VERBOSE="d")` after your import statements, which
  will report the equivalent GMT commands as one of the debug messages.
* Either append all messages from running your script to your GitHub issue, or
  filter the messages to include only the GMT-equivalent commands using a command
  such as:

      python <test>.py 2>&1 | awk -F': ' '$2=="GMT_Call_Command string" {print $3}'

  where `<test>` is the name of your test script. Note that this script works only with GMT>=6.4
* If the bug is produced when passing an in-memory data object (e.g., a
  pandas.DataFrame or xarray.DataArray) to a PyGMT function, try writing the
  data to a file (e.g., a netCDF or ASCII txt file) and passing the data file
  to the PyGMT function instead. In the GitHub issue, please share the results
  for both cases along with your code.

### Submitting a Feature Request

* Find the [*Issues*](https://github.com/GenericMappingTools/pygmt/issues) tab on the
  top of the GitHub repository and click *New issue*.
* Click on *Get started* next to *Feature request*.
* **Please try to fill out the template with as much detail as you can**.
* After submitting your feature request, try to answer any follow up questions as best
  as you can.

### Submitting General Comments/Questions

There are several pages on the [Community Forum](https://forum.generic-mapping-tools.org/)
where you can submit general comments and/or questions:

* For questions about using PyGMT, select *New Topic* from the
  [PyGMT Q&A Page](https://forum.generic-mapping-tools.org/c/questions/pygmt-q-a/11).
* For general comments, select *New Topic* from the
  [Lounge Page](https://forum.generic-mapping-tools.org/c/lounge/6).
* To share your work, select *New Topic* from the
  [Showcase Page](https://forum.generic-mapping-tools.org/c/Show-your-nice-example-script/10).

## General Guidelines

### Resources for New Contributors

Please take a look at these resources to learn about Git and pull requests (don't
hesitate to [ask questions](contributing.md#getting-help)):

* [How to Contribute to Open Source](https://opensource.guide/how-to-contribute/).
* [Git Workflow Tutorial](http://www.asmeurer.com/git-workflow/) by Aaron Meurer.
* [How to Contribute to an Open Source Project on GitHub](https://egghead.io/courses/how-to-contribute-to-an-open-source-project-on-github).

### Getting Help

Discussion often happens on GitHub issues and pull requests. In addition, there is a
[Discourse forum](https://forum.generic-mapping-tools.org/c/questions/pygmt-q-a) for
the project where you can ask questions.

### Pull Request Workflow

We follow the [git pull request workflow](http://www.asmeurer.com/git-workflow)
to make changes to our codebase. Every change made goes through a pull request, even
our own, so that our
[continuous integration](https://en.wikipedia.org/wiki/Continuous_integration)
services have a chance to check that the code is up to standards and passes all
our tests. This way, the *main* branch is always stable.

#### General Guidelines for Making a Pull Request (PR):

* What should be included in a PR
  - Have a quick look at the titles of all the existing issues first. If there
    is already an issue that matches your PR, leave a comment there to let us
    know what you plan to do. Otherwise, **open an issue** describing what you
    want to do.
  - Each pull request should consist of a **small** and logical collection of
    changes; larger changes should be broken down into smaller parts and
    integrated separately.
  - Bug fixes should be submitted in separate PRs.
* How to write and submit a PR
  - Use underscores for all Python (*.py) files as per
    [PEP8](https://www.python.org/dev/peps/pep-0008/), not hyphens. Directory
    names should also use underscores instead of hyphens.
  - Describe what your PR changes and *why* this is a good thing. Be as
    specific as you can. The PR description is how we keep track of the changes
    made to the project over time.
  - Do not commit changes to files that are irrelevant to your feature or
    bugfix (e.g.: `.gitignore`, IDE project files, etc).
  - Write descriptive commit messages. Chris Beams has written a
    [guide](https://chris.beams.io/posts/git-commit/) on how to write good
    commit messages.
* PR review
  - Be willing to accept criticism and work on improving your code; we don't
    want to break other users' code, so care must be taken not to introduce
    bugs.
  - Be aware that the pull request review process is not immediate, and is
    generally proportional to the size of the pull request.

#### General Process for Pull Request Review:

After you've submitted a pull request, you should expect to hear at least a
comment within a couple of days. We may suggest some changes, improvements or
alternative implementation details.

To increase the chances of getting your pull request accepted quickly, try to:

* Submit a friendly PR
  - Write a good and detailed description of what the PR does.
  - Write some documentation for your code (docstrings) and leave comments
    explaining the *reason* behind non-obvious things.
  - Write tests for the code you wrote/modified if needed.
    Please refer to [Testing your code](contributing.md#testing-your-code) or
    [Testing plots](contributing.md#testing-plots).
  - Include an example of new features in the gallery or tutorials.
    Please refer to [Gallery plots](contributing.md#contributing-gallery-plots)
    or [Tutorials](contributing.md#contributing-tutorials).
* Have a good coding style
  - Use readable code, as it is better than clever code (even with comments).
  - Follow the [PEP8](http://pep8.org) style guide for code and the
    [NumPy style guide](https://numpydoc.readthedocs.io/en/latest/format.html)
    for docstrings. Please refer to [Code style](contributing.md#code-style).

Pull requests will automatically have tests run by GitHub Actions.
This includes running both the unit tests as well as code linters.
GitHub will show the status of these checks on the pull request.
Try to get them all passing (green).
If you have any trouble, leave a comment in the PR or
[get in touch](contributing.md#getting-help).

## Setting up your Environment

These steps for setting up your environment are necessary for
[editing the documentation locally](contributing.md#editing-the-documentation-locally) and
[contributing code](contributing.md#contributing-code). A local PyGMT development environment
is not needed for [editing the documentation on GitHub](contributing.md#editing-the-documentation-on-github).

We highly recommend using [Mambaforge](https://github.com/conda-forge/miniforge#mambaforge/)
and the `mamba` package manager to install and manage your Python packages.
It will make your life a lot easier!

The repository includes a virtual environment file `environment.yml` with the
specification for all development requirements to build and test the project.
In particular, these are some of the key development dependencies you will need
to install to build the documentation and run the unit tests locally:

- git (for cloning the repo and tracking changes in code)
- dvc (for downloading baseline images used in tests)
- pytest-mpl (for checking that generated plots match the baseline)
- sphinx-gallery (for building the gallery example page)

See the [`environment.yml`](https://github.com/GenericMappingTools/pygmt/blob/main/environment.yml)
file for the full list of dependencies and the environment name (`pygmt`).
Once you have forked and cloned the repository to your local machine, you can
use this file to create an isolated environment on which you can work.
Run the following on the base of the repository to create a new conda
environment from the `environment.yml` file:

```bash
mamba env create --file environment.yml
```

Before building and testing the project, you have to activate the environment
(you'll need to do this every time you start a new terminal):

```bash
mamba activate pygmt
```

We have a [`Makefile`](https://github.com/GenericMappingTools/pygmt/blob/main/Makefile)
that provides commands for installing, running the tests and coverage analysis,
running linters, etc. If you don't want to use `make`, open the `Makefile` and
copy the commands you want to run.

To install the current source code into your testing environment, run:

```bash
make install  # on Linux/macOS
python -m pip install --no-deps -e .  # on Windows
```

This installs your project in *editable* mode, meaning that changes made to the source
code will be available when you import the package (even if you're on a different
directory).

## Contributing Documentation

### PyGMT Documentation Overview

There are four main components to PyGMT's documentation:

* Gallery examples, with source code in Python `*.py` files under the
  `examples/gallery/` folder.
* Tutorial examples, with source code in Python `*.py` files under the
  `examples/tutorials/` folder.
* API documentation, with source code in the docstrings in Python `*.py`
  files under the `pygmt/src/` and `pygmt/datasets/` folders.
* Getting started/developer documentation, with source text in ReST `*.rst`
  and markdown `*.md` files under the `doc/` folder.

The documentation is written primarily in
[reStructuredText](https://docutils.sourceforge.io/rst.html) and built by
[Sphinx](http://www.sphinx-doc.org/). Please refer to
{gmt-docs}`reStructuredText Cheatsheet <devdocs/rst-cheatsheet.html>`
if you are new to reStructuredText. When contributing documentation, be sure to
follow the general guidelines in the [pull request workflow](contributing.md#pull-request-workflow)
section.

There are two primary ways to edit the PyGMT documentation:
- For simple documentation changes, you can easily
  [edit the documentation on GitHub](contributing.md#editing-the-documentation-on-github).
  This only requires you to have a GitHub account.
- For more complicated changes, you can
  [edit the documentation locally](contributing.md#editing-the-documentation-locally).
  In order to build the documentation locally, you first need to
  [set up your environment](contributing.md#setting-up-your-environment).

### Editing the Documentation on GitHub

If you're browsing the documentation and notice a typo or something that could be
improved, please consider letting us know by [creating an issue](contributing.md#reporting-a-bug) or
(even better) submitting a fix.

You can submit fixes to the documentation pages completely online without having to
download and install anything:

1. On each documentation page, there should be an "Improve This Page" link at the very
  top.
2. Click on that link to open the respective source file (usually an `.rst` file in the
  `doc/` folder or a `.py` file in the `examples/` folder) on GitHub for editing online
  (you'll need a GitHub account).
3. Make your desired changes.
4. When you're done, scroll to the bottom of the page.
5. Fill out the two fields under "Commit changes": the first is a short title describing
  your fixes; the second is a more detailed description of the changes. Try to be as
  detailed as possible and describe *why* you changed something.
6. Choose "Create a new branch for this commit and start a pull request" and
  click on the "Propose changes" button to open a pull request.
7. The pull request will run the GMT automated tests and make a preview deployment.
  You can see how your change looks in the PyGMT documentation by clicking the
  "Details" button of the "docs/readthedocs.org:pygmt-dev" status check,
  after the building has finished (usually 10-15 minutes after the pull request was created).
8. We'll review your pull request, recommend changes if necessary, and then merge
  them in if everything is OK.
9. Done!

Alternatively, you can make the changes offline to the files in the `doc` folder or the
example scripts. See [editing the documentation locally](contributing.md#editing-the-documentation-locally)
for instructions.

### Editing the Documentation Locally

For more extensive changes, you can edit the documentation in your cloned repository
and build the documentation to preview changes before submitting a pull request. First,
follow the [setting up your environment](contributing.md#setting-up-your-environment) instructions.
After making your changes, you can build the HTML files from sources using:

```bash
cd doc
make all
```

This will build the HTML files in `doc/_build/html`.
Open `doc/_build/html/index.html` in your browser to view the pages. Follow the
[pull request workflow](contributing.md#pull-request-workflow) to submit your changes for review.

### Adding example code

Many of the PyGMT functions have example code in their documentation. To contribute an
example, add an "Example" header and put the example code below it. Have all lines
begin with `>>>`.  To keep this example code from being run during testing, add the code
`__doctest_skip__ = [function name]` to the top of the module.

**Inline code example**

Below the import statements at the top of the file

``
__doctest_skip__ = ["module_name"]
``

At the end of the function's docstring

    Example
    -------
    >>> import pygmt
    >>> # Comment describing what is happening
    >>> Code example


### Contributing Gallery Plots

The gallery and tutorials are managed by
[sphinx-gallery](https://sphinx-gallery.readthedocs.io/).
The source files for the example gallery are `.py` scripts in `examples/gallery/` that
generate one or more figures. They are executed automatically by sphinx-gallery when
the [documentation is built](contributing.md#editing-the-documentation-locally). The output is gathered and
assembled into the gallery.

You can **add a new** plot by placing a new `.py` file in one of the folders inside the
`examples/gallery` folder of the repository. See the other examples to get an idea for the
format.

General guidelines for making a good gallery plot:

* Examples should highlight a single feature/command. Good: *how to add a label to
  a colorbar*. Bad: *how to add a label to the colorbar and use two different CPTs and
  use subplots*.
* Try to make the example as simple as possible. Good: *use only commands that are
  required to show the feature you want to highlight*. Bad: *use advanced/complex Python
  features to make the code smaller*.
* Use a sample dataset from `pygmt.datasets` if you need to plot data. If a suitable
  dataset isn't available, open an issue requesting one and we'll work together to add
  it.
* Add comments to explain things that aren't obvious from reading the code. Good: *Use a
  Mercator projection and make the plot 15 centimeters wide*. Bad: *Draw coastlines and
  plot the data*.
* Describe the feature that you're showcasing and link to other relevant parts of the
  documentation.
* SI units should be used in the example code for gallery plots.

### Contributing Tutorials

The tutorials (the User Guide in the docs) are also built by sphinx-gallery from the
`.py` files in the `examples/tutorials` folder of the repository. To add a new tutorial:

* Create a `.py` file in the `examples/tutorials/advanced` folder.
* Write the tutorial in "notebook" style with code mixed with paragraphs explaining what
  is being done. See the other tutorials for the format.
* Choose the most representative figure as the thumbnail figure by adding a comment line
  `# sphinx_gallery_thumbnail_number = <fig_number>` to any place (usually at the top)
  in the tutorial. The *fig_number* starts from 1.

Guidelines for a good tutorial:

* Each tutorial should focus on a particular set of tasks that a user might want to
  accomplish: plotting grids, interpolation, configuring the frame, projections, etc.
* The tutorial code should be as simple as possible. Avoid using advanced/complex Python
  features or abbreviations.
* Explain the options and features in as much detail as possible. The gallery has
  concise examples while the tutorials are detailed and full of text.
* SI units should be used in the example code for tutorial plots.

Note that the <code>pygmt.Figure.show</code> method needs to be called for a plot
to be inserted into the documentation.


### Editing the API Documentation

The API documentation is built from the docstrings in the Python `*.py` files under
the `pygmt/src/` and `pygmt/datasets/` folders. **All docstrings** should follow the
[NumPy style guide](https://numpydoc.readthedocs.io/en/latest/format.html#docstring-standard).
All functions/classes/methods should have docstrings with a full description of all
arguments and return values.

While the maximum line length for code is automatically set by Black, docstrings
must be formatted manually. To play nicely with Jupyter and IPython, **keep docstrings
limited to 79 characters** per line.

### Standards for Example Code

When editing documentation, use the following standards to demonstrate the example code:

1. Python arguments, such as import statements, Boolean expressions, and function
   arguments should be wrapped as ``code`` by using \`\` on both sides of the code.
   Examples: \`\`import pygmt\`\` results in ``import pygmt``, \`\`True\`\` results in `True`,
    \`\`style="v"\`\` results in `style="v"`.
2. Literal GMT arguments should be **bold** by wrapping the arguments with \*\*
   (two asterisks) on both sides. The argument description should be in *italicized*
   with \* (single asterisk) on both sides.
   Examples: `**+l**\ *label*` results in **+l***label*, `**05m**` results in **05m**.
3. Optional arguments are wrapped with [ ] (square brackets).
4. Arguments that are mutually exclusive are separated with a | (bar) to denote "or".
5. Default arguments for parameters and configuration settings are wrapped
   with [ ] (square brackets) with the prefix "Default is". Example: [Default is
   **p**].

### Cross-referencing with Sphinx

The API reference is manually assembled in `doc/api/index.rst`.
The *autodoc* sphinx extension will automatically create pages for each
function/class/module/method listed there.

You can reference functions, classes, modules, and methods from anywhere
(including docstrings) using:

- <code>:func:\`package.module.function\`</code>
- <code>:class:\`package.module.class\`</code>
- <code>:meth:\`package.module.method\`</code>
- <code>:mod:\`package.module\`</code>

An example would be to use
<code>:meth:\`pygmt.Figure.grdview\`</code> to link
to [https://www.pygmt.org/latest/api/generated/pygmt.Figure.grdview.html](https://www.pygmt.org/latest/api/generated/pygmt.Figure.grdview.html).
PyGMT documentation that is not a class, method,
or module can be linked with <code>:doc:\`Any Link Text </path/to/the/file>\`</code>.
For example, <code>:doc:\`Install instructions \</install\>\`</code> links
to [https://www.pygmt.org/latest/install.html](https://www.pygmt.org/latest/install.html).

Linking to the GMT documentation and GMT configuration parameters can be done using:

- <code>:gmt-docs:\`page_name.html\`</code>
- <code>:gmt-term:\`GMT_PARAMETER\`</code>

An example would be using
<code>:gmt-docs:\`makecpt.html\`</code> to link to {gmt-docs}`makecpt.html`.
For GMT configuration parameters, an example is
<code>:gmt-term:\`COLOR_FOREGROUND\`</code> to link to
{gmt-term}`https://docs.generic-mapping-tools.org/latest/gmt.conf#term-COLOR_FOREGROUND <COLOR_FOREGROUND>`.

Sphinx will create a link to the automatically generated page for that
function/class/module/method.

## Contributing Code

### PyGMT Code Overview

The source code for PyGMT is located in the `pygmt/` directory. When contributing
code, be sure to follow the general guidelines in the
[pull request workflow](contributing.md#pull-request-workflow) section.

### Code Style

We use some tools to format the code so we don't have to think about it:

- [Black](https://github.com/psf/black)
- [blackdoc](https://github.com/keewis/blackdoc)
- [docformatter](https://github.com/myint/docformatter)
- [isort](https://pycqa.github.io/isort/)

Black and blackdoc loosely follows the [PEP8](http://pep8.org) guide but with a few
differences. Regardless, you won't have to worry about formatting the code yourself.
Before committing, run it to automatically format your code:

```bash
make format
```

For consistency, we also use UNIX-style line endings (`\n`) and file permission
644 (`-rw-r--r--`) throughout the whole project.
Don't worry if you forget to do it. Our continuous integration systems will
warn us and you can make a new commit with the formatted code.
Even better, you can just write `/format` in the first line of any comment in a
pull request to lint the code automatically.

When wrapping a new alias, use an underscore to separate words bridged by vowels
(aeiou), such as `no_skip` and `z_only`. Do not use an underscore to separate
words bridged only by consonants, such as `distcalc`, and `crossprofile`. This
convention is not applied by the code checking tools, but the PyGMT maintainers
will comment on any pull requests as needed.

We also use [flakeheaven](https://flakeheaven.readthedocs.io) and
[pylint](https://pylint.pycqa.org/) to check the quality of the code and quickly catch
common errors.
The [`Makefile`](https://github.com/GenericMappingTools/pygmt/blob/main/Makefile)
contains rules for running both checks:

```bash
make check   # Runs black, blackdoc, docformatter, flakeheaven and isort (in check mode)
make lint    # Runs pylint, which is a bit slower
```

### Testing your Code

Automated testing helps ensure that our code is as free of bugs as it can be.
It also lets us know immediately if a change we make breaks any other part of the code.

All of our test code and data are stored in the `tests` subpackage.
We use the [pytest](https://pytest.org/) framework to run the test suite.

Please write tests for your code so that we can be sure that it won't break any of the
existing functionality.
Tests also help us be confident that we won't break your code in the future.

When writing tests, don't test everything that the GMT function already tests, such as
the every unique combination arguments. An exception to this would be the most popular
methods, such as <code>pygmt.Figure.plot</code> and <code>pygmt.Figure.basemap</code>.
The highest priority for tests should be the Python-specific code, such as numpy,
pandas, and xarray objects and the virtualfile mechanism.

If you're **new to testing**, see existing test files for examples of things to do.
**Don't let the tests keep you from submitting your contribution!**
If you're not sure how to do this or are having trouble, submit your pull request
anyway.
We will help you create the tests and sort out any kind of problem during code review.

Pull the baseline images, run the tests, and calculate test coverage using:

    dvc status  # should report any files 'not_in_cache'
    dvc pull  # pull down files from DVC remote cache (fetch + checkout)
    make test

The coverage report will let you know which lines of code are touched by the tests.
If all the tests pass, you can view the coverage reports by opening `htmlcov/index.html`
in your browser. **Strive to get 100% coverage for the lines you changed.**
It's OK if you can't or don't know how to test something.
Leave a comment in the PR and we'll help you out.

You can also run tests in just one test script using:

    pytest pygmt/tests/NAME_OF_TEST_FILE.py

or run tests which contain names that match a specific keyword expression:

    pytest -k KEYWORD pygmt/tests

### Testing Plots

Writing an image-based test is only slightly more difficult than a simple test.
The main consideration is that you must specify the "baseline" or reference
image, and compare it with a "generated" or test image. This is handled using
the *decorator* functions `@pytest.mark.mpl_image_compare` and `@check_figures_equal`
whose usage are further described below.

#### Using mpl_image_compare

> **This is the preferred way to test plots whenever possible.**

This method uses the [pytest-mpl](https://github.com/matplotlib/pytest-mpl)
plug-in to test plot generating code.
Every time the tests are run, `pytest-mpl` compares the generated plots with known
correct ones stored in `pygmt/tests/baseline`.
If your test created a `pygmt.Figure` object, you can test it by adding a *decorator* and
returning the `pygmt.Figure` object:

```python
@pytest.mark.mpl_image_compare
def test_my_plotting_case():
    "Test that my plotting method works"
    fig = Figure()
    fig.basemap(region=[0, 360, -90, 90], projection="W15c", frame=True)
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

Don't forget to commit the baseline image as well!
The images should be pushed up into a remote repository using `dvc` (instead of
`git`) as will be explained in the next section.

#### Using Data Version Control ([dvc](https://dvc.org)) to Manage Test Images

As the baseline images are quite large blob files that can change often (e.g.
with new GMT versions), it is not ideal to store them in `git` (which is meant
for tracking plain text files). Instead, we will use [`dvc`](https://dvc.org)
which is like `git` but for data. What `dvc` does is to store the hash (md5sum)
of a file. For example, given an image file like `test_logo.png`, `dvc` will
generate a `test_logo.png.dvc` plain text file containing the hash of the
image. This `test_logo.png.dvc` file can be stored as usual on GitHub, while
the `test_logo.png` file can be stored separately on our `dvc` remote at
[https://dagshub.com/GenericMappingTools/pygmt](https://dagshub.com/GenericMappingTools/pygmt).

To **pull** or sync files from the `dvc` remote to your local repository, use
the commands below. Note how `dvc` commands are very similar to `git`.

    dvc status  # should report any files 'not_in_cache'
    dvc pull  # pull down files from DVC remote cache (fetch + checkout)

Once the sync/download is complete, you should notice two things. There will be
images stored in the `pygmt/tests/baseline` folder (e.g. `test_logo.png`) and
these images are technically reflinks/symlinks/copies of the files under the
`.dvc/cache` folder. You can now run the image comparison test suite as per
usual.

    pytest pygmt/tests/test_logo.py  # run only one test
    make test  # run the entire test suite

To **push** or sync changes from your local repository up to the `dvc` remote
at DAGsHub, you will first need to set up authentication using the commands
below. This only needs to be done once, i.e. the first time you contribute a
test image to the PyGMT project.

    dvc remote modify upstream --local auth basic
    dvc remote modify upstream --local user "$DAGSHUB_USER"
    dvc remote modify upstream --local password "$DAGSHUB_PASS"

The configuration will be stored inside your `.dvc/config.local` file. Note
that the $DAGSHUB_PASS token can be generated at
[https://dagshub.com/user/settings/tokens](https://dagshub.com/user/settings/tokens)
after creating a DAGsHub account (can be linked to your GitHub account). Once
you have an account set up, please ask one of the PyGMT maintainers to add you
as a collaborator at
[https://dagshub.com/GenericMappingTools/pygmt/settings/collaboration](https://dagshub.com/GenericMappingTools/pygmt/settings/collaboration)
before proceeding with the next steps.

The entire workflow for generating or modifying baseline test images can be
summarized as follows:

    # Sync with both git and dvc remotes
    git pull
    dvc pull

    # Generate new baseline images
    pytest --mpl-generate-path=baseline pygmt/tests/test_logo.py
    mv baseline/*.png pygmt/tests/baseline/

    # Generate hash for baseline image and stage the *.dvc file in git
    dvc status  # check which files need to be added to dvc
    dvc add pygmt/tests/baseline/test_logo.png
    git add pygmt/tests/baseline/test_logo.png.dvc

    # Commit changes and push to both the git and dvc remotes
    git commit -m "Add test_logo.png into DVC"
    dvc status --remote upstream  # Report which files will be pushed to the dvc remote
    dvc push  # Run before git push to enable automated testing with the new images
    git push

#### Using check_figures_equal

This approach draws the same figure using two different methods (the reference
method and the tested method), and checks that both of them are the same.
It takes two `pygmt.Figure` objects ('fig_ref' and 'fig_test'), generates a png
image, and checks for the Root Mean Square (RMS) error between the two.
Here's an example:

```python
@check_figures_equal()
def test_my_plotting_case():
  "Test that my plotting method works"
  fig_ref, fig_test = Figure(), Figure()
  fig_ref.grdimage("@earth_relief_01d_g", projection="W120/15c", cmap="geo")
  fig_test.grdimage(grid, projection="W120/15c", cmap="geo")
  return fig_ref, fig_test
```
