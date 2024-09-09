# Environmental Variables

Several environment variables can be used to control the behavior of PyGMT. These
environment variables can be set in your shell or in your Python script using the
`os.environ` dictionary.

Here we list the environment variables that are used by PyGMT. The environment
variables are divided into three categories: system environment variables, GMT/PyGMT
environment variables, and module-specific environment variables.

## System Environment Variables

```{glossary}
TZ
    Specify the time zone for the current calendar time. Refer to the
    [Specifying the Time Zone with TZ](https://www.gnu.org/software/libc/manual/html_node/TZ-Variable.html)
    for the valid format.
```

## GMT/PyGMT Environment Variables

```{glossary}
PYGMT_USE_EXTERNAL_DISPLAY
    Setting this environment variable to `"false"` can disable image preview in
    external viewers. It's useful when running the tests and building the documentation
    to avoid popping up windows.
```

## Module-Specific Environment Variables

```{glossary}
X2SYS_HOME
    Specify the directory where the x2sys-related functions (e.g.,
    {func}`pygmt.x2sys_init`) can keep track of the x2sys settings.
```
