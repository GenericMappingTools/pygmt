---
myst:
  # Customized URI schemes that are converted to external links
  # References:
  # - https://myst-parser.readthedocs.io/en/latest/syntax/cross-referencing.html#customising-external-url-resolution
  # - https://myst-parser.readthedocs.io/en/latest/configuration.html#frontmatter-local-configuration
  url_schemes:
    http: null
    https: null
    tag:
      url: "https://github.com/GenericMappingTools/pygmt/releases/tag/{{path}}"
      title: "{{path}}"
    doc:
      url: "https://www.pygmt.org/{{path}}"
      title: "Web"
    html:
      url: "https://github.com/GenericMappingTools/pygmt/releases/download/{{path}}/pygmt-docs.zip"
      title: "HTML+ZIP"
    pdf:
      url: "https://github.com/GenericMappingTools/pygmt/releases/download/{{path}}/pygmt-docs.pdf"
      title: "PDF"
---

# Minimum Supported Versions

PyGMT has adopted [SPEC 0](https://scientific-python.org/specs/spec-0000/) alongside the
rest of the scientific Python ecosystem, and will therefore:

- Drop support for Python versions 3 years after their initial release.
- Drop support for core package dependencies (NumPy, pandas, Xarray) 2 years after their
  initial release.

In addition to the above, the PyGMT team has also decided to:

- Drop support for GMT versions 3 years after their initial release, while ensuring at
  least two latest minor versions remain supported.
- Maintain support for [optional dependencies](/ecosystem.md#pygmt-dependencies) for at
  least 1 year after their initial release. Users are encouraged to use the most
  up-to-date optional dependencies where possible.

:::{note}
The SPEC 0 policy is enforced on a best-effort basis, and the PyGMT team may decide to
drop support for core (and optional) package dependencies earlier than recommended for
compatibility reasons.
:::

| PyGMT Version | Documentation | GMT | Python | NumPy | pandas | Xarray |
|---|---|---|---|---|---|---|
| [Dev][]* | [<doc:dev>] [[HTML+ZIP](doc:dev/pygmt-docs.zip)] [[PDF](doc:dev/pygmt-docs.pdf)] | {{ requires.gmt }} | {{ requires.python }} | {{ requires.numpy }} | {{ requires.pandas }} | {{ requires.xarray }} |
| <tag:v0.14.2> | [<doc:v0.14.2>] [<html:v0.14.2>] | >=6.4.0 | >=3.11 | >=1.25 | >=2.0 | >=2023.04 |
| <tag:v0.14.1> | [<doc:v0.14.1>] [<html:v0.14.1>] | >=6.4.0 | >=3.11 | >=1.25 | >=2.0 | >=2023.04 |
| <tag:v0.14.0> | [<doc:v0.14.0>] [<html:v0.14.0>] | >=6.4.0 | >=3.11 | >=1.25 | >=2.0 | >=2023.04 |
| <tag:v0.13.0> | [<doc:v0.13.0>] [<html:v0.13.0>] | >=6.3.0 | >=3.10 | >=1.24 | >=1.5 | >=2022.09 |
| <tag:v0.12.0> | [<doc:v0.12.0>] [<html:v0.12.0>] | >=6.3.0 | >=3.10 | >=1.23 | >=1.5 | >=2022.06 |
| <tag:v0.11.0> | [<doc:v0.11.0>] [<html:v0.11.0>] | >=6.3.0 | >=3.9 | >=1.23 |  |  |
| <tag:v0.10.0> | [<doc:v0.10.0>] [<html:v0.10.0>] | >=6.3.0 | >=3.9 | >=1.22 |  |  |
| <tag:v0.9.0> | [<doc:v0.9.0>] [<html:v0.9.0>] | >=6.3.0 | >=3.8 | >=1.21 |  |  |
| <tag:v0.8.0> | [<doc:v0.8.0>] [<html:v0.8.0>] | >=6.3.0 | >=3.8 | >=1.20 |  |  |
| <tag:v0.7.0> | [<doc:v0.7.0>] [<html:v0.7.0>] | >=6.3.0 | >=3.8 | >=1.20 |  |  |
| <tag:v0.6.1> | [<doc:v0.6.1>] [<html:v0.6.1>] | >=6.3.0 | >=3.8 | >=1.19 |  |  |
| <tag:v0.6.0> | [<doc:v0.6.0>] [<html:v0.6.0>] | >=6.3.0 | >=3.8 | >=1.19 |  |  |
| <tag:v0.5.0> | [<doc:v0.5.0>] [<html:v0.5.0>] | >=6.2.0 | >=3.7 | >=1.18 |  |  |
| <tag:v0.4.1> | [<doc:v0.4.1>] [<html:v0.4.1>] | >=6.2.0 | >=3.7 | >=1.17 |  |  |
| <tag:v0.4.0> | [<doc:v0.4.0>] [<html:v0.4.0>] | >=6.2.0 | >=3.7 | >=1.17 |  |  |
| <tag:v0.3.1> | [<doc:v0.3.1>] [<html:v0.3.1>] | >=6.1.1 | >=3.7 |  |  |  |
| <tag:v0.3.0> | [<doc:v0.3.0>] [<html:v0.3.0>] | >=6.1.1 | >=3.7 |  |  |  |
| <tag:v0.2.1> | [<doc:v0.2.1>] [<html:v0.2.1>] | >=6.1.1 | 3.6 - 3.8 |  |  |  |
| <tag:v0.2.0> | [<doc:v0.2.0>] [<html:v0.2.0>] | >=6.1.1 | 3.6 - 3.8 |  |  |  |
| <tag:v0.1.2> | [<doc:v0.1.2>] [<html:v0.1.2>] | >=6.0.0 | 3.6 - 3.8 |  |  |  |
| <tag:v0.1.1> | [<doc:v0.1.1>] [<html:v0.1.1>] | >=6.0.0 | 3.6 - 3.8 |  |  |  |
| <tag:v0.1.0> | [<doc:v0.1.0>] [<html:v0.1.0>] | >=6.0.0 | 3.6 - 3.8 |  |  |  |

*Dev reflects the main branch and is for the upcoming release.

[Dev]: https://github.com/GenericMappingTools/pygmt/milestones
