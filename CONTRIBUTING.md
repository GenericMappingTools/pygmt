# Contributing Guidelines

:tada: **First off, thank you for considering contributing to our project!** :tada:

This is a community-driven project, so it's people like you that make it useful and
successful.
These are some of the many ways to contribute:

* :bug: Submitting bug reports and feature requests
* :memo: Writing tutorials or examples
* :mag: Fixing typos and improving the documentation
* :bulb: Writing code for everyone to use
* :people_holding_hands: Community engagement and outreach

If you get stuck at any point you can create an
[issue](https://github.com/GenericMappingTools/pygmt/issues) on GitHub or contact
us at one of the other channels [mentioned below](#how-can-i-talk-to-you).

For more information on contributing to open source projects,
[GitHub's own guide](https://opensource.guide/how-to-contribute)
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
  - [Example code standards](#example-code-standards)
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
* Make a tutorial or gallery example of how to do something.
* Provide feedback about how we can improve the project or about your particular use
  case.
* Contribute code you already have. It doesn't need to be perfect! We will help you
  clean things up, test it, etc.


## How Can I Talk to You?

Discussion often happens in the issues and pull requests.
In addition, there is a
[Discourse forum](https://forum.generic-mapping-tools.org/c/questions/pygmt-q-a) for
the project where you can ask questions.


## Reporting a Bug

Find the *Issues* tab on the top of the GitHub repository and click *New Issue*.
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
  `doc/` folder or a `.py` file in the `examples/` folder) on GitHub for editing online
  (you'll need a GitHub account).
* Make your desired changes.
* When you're done, scroll to the bottom of the page.
* Fill out the two fields under "Commit changes": the first is a short title describing
  your fixes; the second is a more detailed description of the changes. Try to be as
  detailed as possible and describe *why* you changed something.
* Choose "Create a new branch for this commit and start a pull request" and
  click on the "Propose changes" button to open a pull request.
* The pull request will run the GMT automated tests and make a preview deployment.
  You can see how your change looks in the PyGMT documentation by clicking the
  "View deployment" button after the Vercel bot has finished (usually 5-10 minutes
  after the pull request was created).
* We'll review your pull request, recommend changes if necessary, and then merge
  them in if everything is OK.
* Done :tada::beer:

Alternatively, you can make the changes offline to the files in the `doc` folder or the
example scripts. See [Contributing Code](#contributing-code) for instructions.

### Gallery plots

The gallery and tutorials are managed by
[sphinx-gallery](https://sphinx-gallery.readthedocs.io/).
The source files for the example gallery are `.py` scripts in `examples/gallery/` that
generate one or more figures. They are executed automatically by sphinx-gallery when
the [documentation is built](#documentation). The output is gathered and assembled
into the gallery.

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
  Mercator projection and make the plot 15 centimeters wide*. Bad: *Draw coastlines and
  plot the data*.
* Describe the feature that you're showcasing and link to other relevant parts of the
  documentation.
* SI units should be used in the example code for gallery plots.

### Tutorials

The tutorials (the User Guide in the docs) are also built by sphinx-gallery from the
`.py` files in the `examples/tutorials` folder of the repository. To add a new tutorial:

* Include a `.py` file in the `examples/tutorials` folder on the base of the repository.
* Write the tutorial in "notebook" style with code mixed with paragraphs explaining what
  is being done. See the other tutorials for the format.
* Include the tutorial in the table of contents of the documentation (side bar). Do this
  by adding a line to the User Guide `toc` directive in `doc/index.rst`. Notice that the
  file included is the `.rst` generated by sphinx-gallery.
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

Note that the `Figure.show()` function needs to be called for a plot to be inserted into
the documentation.

### Example code standards

When editing documentation, use the following standards to demonstrate the example code:

1. Python arguments, such as import statements, Boolean expressions, and function
   arguments should be wrapped as ``code`` by using \`\` on both sides of the code.
   Examples: \`\`import pygmt\`\` results in ``import pygmt``, \`\`True\`\` results in `True`,
    \`\`style="v"\`\` results in `style="v"`.
2. Literal GMT arguments should be **bold** by wrapping the arguments with \*\*
   (two asterisks) on both sides. The argument description should be in *italicized*
   with \* (single asterisk) on both sides.
   Examples: `**+l**\ *label*` results in **+l***label*, `**05m**` results in **05m**.
3. Optional arguments are placed wrapped with [ ] (square brackets).
4. Arguments that are mutually exclusive are separated with a | (bar) to denote "or".

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
* Use underscores for all Python (*.py) files as per [PEP8](https://www.python.org/dev/peps/pep-0008/),
  not hyphens. Directory names should also use underscores instead of hyphens.
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
Once you have forked and cloned the repository to your local machine, you can
use this file to create an isolated environment on which you can work.
Run the following on the base of the repository:

```bash
conda env create
```

Before building and testing the project, you have to activate the environment:

```bash
conda activate pygmt
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

We use some tools:

- [Black](https://github.com/psf/black)
- [blackdoc](https://github.com/keewis/blackdoc)
- [docformatter](https://github.com/myint/docformatter)
- [isort](https://pycqa.github.io/isort/)

to format the code so we don't have to think about it.
Black and blackdoc loosely follows the [PEP8](http://pep8.org) guide but with a few differences.
Regardless, you won't have to worry about formatting the code yourself.
Before committing, run it to automatically format your code:

```bash
make format
```

For consistency, we also use UNIX-style line endings (`\n`) and file permission
644 (`-rw-r--r--`) throughout the whole project.
Don't worry if you forget to do it. Our continuous integration systems will
warn us and you can make a new commit with the formatted code.
Even better, you can just write `/format` in the first line of any comment in a
Pull Request to lint the code automatically.

We also use [flake8](http://flake8.pycqa.org/en/latest/) and
[pylint](https://www.pylint.org/) to check the quality of the code and quickly catch
common errors.
The [`Makefile`](Makefile) contains rules for running both checks:

```bash
make check   # Runs black, blackdoc, docformatter, flake8 and isort (in check mode)
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

When writing tests, don't test everything that the GMT function already tests, such as
the every unique combination arguments. An exception to this would be the most popular
modules, such as `plot` and `basemap`. The highest priority for tests should be the
Python-specific code, such as numpy, pandas, and xarray objects and the virtualfile
mechanism.

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

### Testing plots

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

Don't forget to commit the baseline image as well!
The images should be pushed up into a remote repository using `dvc` (instead of
`git`) as will be explained in the next section.

#### Using data version control ([dvc](https://dvc.org)) to manage test images

As the baseline images are quite large blob files that can change often (e.g.
with new GMT versions), it is not ideal to store them in `git` (which is meant
for tracking plain text files). Instead, we will use [`dvc`](https://dvc.org)
which is like `git` but for data. What `dvc` does is to store the hash (md5sum)
of a file. For example, given an image file like `test_logo.png`, `dvc` will
generate a `test_logo.png.dvc` plain text file containing the hash of the
image. This `test_logo.png.dvc` file can be stored as usual on GitHub, while
the `test_logo.png` file can be stored separately on our `dvc` remote at
https://dagshub.com/GenericMappingTools/pygmt.

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
https://dagshub.com/user/settings/tokens after creating a DAGsHub account
(can be linked to your GitHub account). Once you have an account set up, please
ask one of the PyGMT maintainers to add you as a collaborator at
https://dagshub.com/GenericMappingTools/pygmt/settings/collaboration before
proceeding with the next steps.

The entire workflow for generating or modifying baseline test images can be
summarized as follows:

    # Sync with both git and dvc remotes
    git pull
    dvc pull

    # Generate new baseline images
    pytest --mpl-generate-path=baseline pygmt/tests/test_logo.py
    mv baseline/*.png pygmt/tests/baseline/

    # Generate hash for baseline image and stage the *.dvc file in git
    git rm -r --cached 'pygmt/tests/baseline/test_logo.png'  # only run if migrating existing image from git to dvc
    dvc status  # check which files need to be added to dvc
    dvc add pygmt/tests/baseline/test_logo.png
    git add pygmt/tests/baseline/test_logo.png.dvc

    # Commit changes and push to both the git and dvc remotes
    git commit -m "Add test_logo.png into DVC"
    git push
    dvc push

#### Using check_figures_equal

This approach draws the same figure using two different methods (the reference
method and the tested method), and checks that both of them are the same.
It takes two `pygmt.Figure` objects ('fig_ref' and 'fig_test'), generates a png
image, and checks for the Root Mean Square (RMS) error between the two.
Here's an example:

```python
@check_figures_equal()
def test_my_plotting_case():
  "Test that my plotting function works"
  fig_ref, fig_test = Figure(), Figure()
  fig_ref.grdimage("@earth_relief_01d_g", projection="W120/15c", cmap="geo")
  fig_test.grdimage(grid, projection="W120/15c", cmap="geo")
  return fig_ref, fig_test
```

### Documentation

#### Building the documentation

Most documentation sources are in the `doc` folder.
We use [sphinx](http://www.sphinx-doc.org/) to build the web pages from these sources.
To build the HTML files:

```bash
cd doc
make all
```

This will build the HTML files in `doc/_build/html`.
Open `doc/_build/html/index.html` in your browser to view the pages.

#### Cross-referencing with Sphinx

The API reference is manually assembled in `doc/api/index.rst`.
The *autodoc* sphinx extension will automatically create pages for each
function/class/module listed there.

You can reference functions, classes, methods, and modules from anywhere
(including docstrings) using:

- <code>:func:\`package.module.function\`</code>
- <code>:class:\`package.module.class\`</code>
- <code>:meth:\`package.module.method\`</code>
- <code>:mod:\`package.module\`</code>

An example would be to use
<code>:meth:\`pygmt.Figure.grdview\`</code> to link
to https://www.pygmt.org/latest/api/generated/pygmt.Figure.grdview.html.
PyGMT documentation that is not a class, method,
or module can be linked with <code>:doc:\`Any Link Text </path/to/the/file>\`</code>.
For example, <code>:doc:\`Install instructions \</install\>\`</code> links
to https://www.pygmt.org/latest/install.html.

Linking to the GMT documentation and GMT configuration parameters can be done using:

- <code>:gmt-docs:\`page_name.html\`</code>
- <code>:gmt-term:\`GMT_PARAMETER\`</code>

An example would be using
<code>:gmt-docs:\`makecpt.html\`</code> to link to
https://docs.generic-mapping-tools.org/latest/makecpt.html.
For GMT configuration parameters, an example is
<code>:gmt-term:\`COLOR_FOREGROUND\`</code> to link to
https://docs.generic-mapping-tools.org/latest/gmt.conf.html#term-COLOR_FOREGROUND.

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

Pull requests will automatically have tests run by GitHub Actions.
This includes running both the unit tests as well as code linters.
GitHub will show the status of these checks on the pull request.
Try to get them all passing (green).
If you have any trouble, leave a comment in the PR or
[get in touch](#how-can-i-talk-to-you).
