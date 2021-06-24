# Authorship guidelines for academic papers and software archives

First of all, we are deeply thankful to everyone who has helped make PyGMT
what it is today. Our goal for this document is to establish guidelines
for giving credit to contributors for their work.
To do so, we will attempt to define:

- Fair and diverse ways of providing recognition for contributors' efforts.
- Define _contributions_ in a broad way: writing code and/or documentation,
  providing ideas, fostering the community, etc.

The following are the ways in which individuals who have contributed will be
recognized.

> **Note**: These policies are not set in stone and may be changed to
> accommodate the growth of the project or the preferences of the community.

## The `AUTHORS.md` file

Anyone who has contributed a pull request to the project is welcome to add
themselves to the `AUTHORS.md` file. This file lives in the repository and is
packaged with distributions. This is an optional process.

## Changelog for each release

Every time we make a release, everyone who has made a commit to the repository
since the previous release will be mentioned in the changelog entry. If their
full name is available on GitHub, we will use it. Otherwise, we will use the
GitHub handle. This is a way of saying "Thank you".

## Authorship on Zenodo archives of releases

Anyone who has contributed to the repository (i.e., appears on `git log`) will
be invited to be an author on the Zenodo archive of new releases.

To be included as an author, you *must* add the following to the `AUTHORS.md`
file of the repository:

1. Full name (and a link to your website or GitHub page)
2. [ORCID](https://orcid.org) (optional)
3. Affiliation (if omitted, we will use "Unaffiliated")

The order of authors will be defined by the number of commits to the repository
(`git shortlog -sne`). The order can also be changed on a case-by-case basis.
The most common reasons for case-by-case changes are contributions to the PyGMT
project that due not relate to commit numbers, including developing PyGMT
lessons such as the [ROSES unit](https://www.youtube.com/watch?v=SSIGJEe0BIk),
organizing workshops/sprints such as the
[FOSS4G Workshop](https://github.com/GenericMappingTools/foss4g2019oceania),
the 2020 and 2021 SciPy sprints, writing grants/proposals to support PyGMT,
and team programming efforts (including reviewing PRs).

If you have contributed and do not wish to be included in Zenodo archives,
there are a few options:

1. Don't add yourself to `AUTHORS.md`
2. Remove yourself from `AUTHORS.md`
3. Indicate next to your name on `AUTHORS.md` that you do not wish to be
   included with something like `(not included in Zenodo)`.

## Scientific publications (papers)

We aim to write academic papers for most of our software packages. Ideally, we
will publish updated papers for major changes or significant new components of
the package.

To be included as an author on the paper, you *must* satisfy the following
criteria:

1. Have made multiple and regular contributions to the repository, or the GMT
   repository, in numerous facets, such as wrapping functions, testing, and/or
   writing documentation.
2. Have made non-coding contributions, including project administration and
   decision making.
3. Have participated in the writing and reviewing of the paper.
4. Add your full name, affiliation, and (optionally) ORCID to the paper. These
   can be submitted on pull requests to the corresponding paper repository.
5. Write and/or read and review the manuscript in a timely manner and provide
   comments on the paper (even if it's just an "OK", but preferably more).

The order of authors will be defined by the number of commits made since the
previous major release that has an associated paper (`git shortlog
vX.0.0...HEAD -sne`). The order of any author who hasn't made any commits will
be decided by all authors. The order can also be changed on a case-by-case
basis.
