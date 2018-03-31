# Contributing Guidelines

First off, thank you for considering contributing to GMT/Python!
It is a community-driven project, so it's people like you that make it useful
and successful.

We love contributions from community members, just like you!
There are many ways to contribute:

* Submitting bug reports and feature requests
* Writing tutorials or examples
* Improvements to the documentation
* Writing code which can be incorporated into project for everyone to use

If you get stuck at
any point you can create an
[issue on GitHub](https://github.com/GenericMappingTools/gmt-python/issues)
or contact us at one of the other channels mentioned below.

For more information on contributing to open source projects,
[GitHub's own guide](https://guides.github.com/activities/contributing-to-open-source/)
is a great starting point if you are new to version control.
Also, checkout the
[Zen of Scientific Software Maintenance](https://jrleeman.github.io/ScientificSoftwareMaintenance/)
for some guiding principles on how to create high quality scientific software contributions.


## Ground Rules

The goal is to maintain a diverse community that's pleasant for everyone.
**Please be considerate and respectful of others**.
Everyone must abide by our [Code of Conduct](CODE_OF_CONDUCT.md) and we
encourage all to read it carefully.


## What Can I Do?

* Tackle any [issues](https://github.com/GenericMappingTools/gmt-python/issues)
  you wish! We have a special label for issues that beginners might want to
  try. Have a look at our
  ["good first issues" list](https://github.com/GenericMappingTools/gmt-python/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22).
* Contribute code you already have. It doesn’t need to be perfect! We will help
  you clean things up, test it, etc.
* Make a tutorial or example of how to do something.
* Provide feedback about how we can improve the project or about your
  particular use case.


## How Can I Talk to You?

Discussion often happens in the issue tracker and in pull requests.
In addition, there is
[Gitter chat room](https://gitter.im/GenericMappingTools/gmt-python)
for the project as well.


## Reporting a Bug

When creating a new issue, please be as specific as possible.
This helps us reproduce the bug and track down its cause.
Try to include the following:

* Version of the code you were using
* Operating system
* Python installation (Anaconda, system, ETS)
* Full error messages that you got
* Example code that reproduces the problem

Remember: the more information we have, the easier it will be for us to solve
your problem.


## Pull Requests

**Working on your first Pull Request?**
You can learn how from this *free* video series:

* [How to Contribute to an Open Source Project on GitHub](https://egghead.io/courses/how-to-contribute-to-an-open-source-project-on-github)
* Aaron Meurer's [tutorial on the git workflow](http://www.asmeurer.com/git-workflow/)
* [How to Contribute to Open Source](https://opensource.guide/how-to-contribute/).

General guidelines for Pull Requests:

* Each pull request should consist of a **small** and logical collection of
  changes.
  Larger changes should be broken down into smaller components and integrated
  separately.
  This allows us more chance for discussion and less code to review at each
  time.
  Please submit bug fixes in separate pull requests.
* Describe what your PR changes and why this is a good thing. Be as specific as
  you can. The PR description is how we keep track of the changes made to the
  project over time.
* Do not commit changes to files that are irrelevant to your feature or bugfix
  (eg: .gitignore, IDE project files, etc).
* Write descriptive commit messages.  Chris Beams has written a
  [guide](https://chris.beams.io/posts/git-commit/) on how to write good commit
  messages.
* Be willing to accept criticism and work on improving your code; we don't want
  to break other users' code, so care must be taken not to introduce bugs.
* Be aware that the pull request review process is not immediate, and is
  generally proportional to the size of the pull request.
* **If this is your first contribution**, be sure to add yourself to the
  [list of contributors](AUTHORS.md). We want to make sure we acknowledge the
  hard work you've generously contributed here.


## Setup

We highly recommend using
[Anaconda](https://www.anaconda.com/download/)
and the `conda` package manager.
It will make your life a lot easier!

Once you have forked and clone the repository to your local machine,
create an isolated environment for you to work:

    cd gmt-python
    conda env create

This will install all you need from conda-forge into a `gmt-python`
environment.
Activate it by running:

    source activate gmt-python

The `Makefile` provides rules for installing, running the tests and coverage
analysis, running linters, etc.
If you don't want to use `make`, see the [Makefile](Makefile) and copy the
commands you want to run.

Install the source as a development version (it will only be available
inside the environment and changes to the source will take effect without
reinstalling):

    make develop

Run the tests using:

    make test

and the coverage analysis using:

    make coverage

To check your code for PEP8 style and common errors (runs `flake8` and
`pylint`):

    make check

Finally, to remove all build files from the repository:

    make clean

There is also a `Makefile` for building the documentation in the `doc` folder:

    cd doc
    make html

You can preview the doc pages in your browser by running:

    make serve

This will serve the docs at [http://127.0.0.1:8009](http://127.0.0.1:8009).


## Code Review

Once you've submitted a Pull Request (PR), at this point you're waiting on us.
You should expect to hear at least a comment within a couple of days.
We may suggest some changes or improvements or alternatives.

Some things that will increase the chance that your pull request is accepted
quickly:

* Write a good and detailed description of what the PR does.
* Write tests for the code you wrote/modified.
* Readable code is better than clever code (even with comments).
* Write documentation for your code (docstrings) and leave comments explaining
  the *reason* behind non-obvious things.
* Follow the [PEP8](http://pep8.org) style guide for code and the [numpy
  guide](https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt)
  for documentation.

Pull requests will automatically have tests run by TravisCI.
This includes running both the unit tests as well as the `flake8` and `pylint`
code linters.
Github will show the status of these checks on the pull request.
Try to get them all passing (green).
If you have any trouble, leave a comment asking for help.


## Testing your code

Automated testing helps ensure that our code is as free of bugs as it can be.
It also lets us know immediately if a change we make breaks any other part of
the code.

All of our test code and data are stored in the `gmt/tests` subpackage.
We use the [pytest](https://pytest.org/) framework to run the test suite.

Please write tests for your code so that we can be sure that it won't break any
of the existing functionality.
Tests also help us be confident that we won't break your code in the future.

If you're **new to testing**, see the files in that package for examples of
test code.
**Don't let the tests keep you from submitting code to us!**
If you're not sure how to do this or are having trouble, submit your pull
request anyway.
We will help you create the tests and sort out any kind of problem during code
review.

### Testing plots

We use the [pytest-mpl](https://github.com/matplotlib/pytest-mpl) plugin to
test plot generating code.
Every time the tests are run, pytest-mpl compared the generated plots with
known correct ones stored in `gmt/tests/baseline`.
If you're test created a `gmt.Figure` object, you can test it by adding a
single line of code:

```python
@pytest.mark.mpl_image_compare
def test_my_plotting_case():
    "Test that my plotting function works"
    fig = Figure()
    fig.psbasemap(region=[0, 360, -90, 90], projection='W7i', frame=True,
                  portrait=True)
    return fig
```

Your test function **must** return the `gmt.Figure` object and you can only
test one figure per function.

Before you can run your test, you'll need to generate a *baseline* (a correct
version) of your plot.
Run the following from the repository root:

    py.test --mpl-generate-path=baseline gmt/tests/NAME_OF_TEST_FILE.py

This will create a `baseline` folder with all the plots generated in your test
file.
Visually inspect the one corresponding to your test function.
If it's correct, copy it (and only it) to `gmt/tests/baseline`.
When you run `make test` the next time, your test should be executed and
passing.

Don't forget to commit the baseline image as well.


## Validating input and output values

It's always a good idea to validate your input and output values to make sure
that things fail in a predictable way. The validation shouldn't be too
aggressive (for example, checking the data types of inputs is usually not
necessary), but sometimes inputs must have a given set of properties or be from
a predefined list of values.

In these cases, an exceptions should be raised to signal the invalid
inputs/outputs. We provide custom exceptions for this (see the API reference).
In general, invalid inputs should raise `GMTInvalidInput`. The `gmt.clib`
raises `GMTCLibError` when API functions return invalid status codes.


## Credit

This guide was adapted from the [MetPy Contributing
Guide](https://github.com/Unidata/MetPy/blob/master/CONTRIBUTING.md).
