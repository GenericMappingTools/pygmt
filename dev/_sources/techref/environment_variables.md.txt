# Environment Variables

PyGMT's behavior can be controlled through various environment variables. These variables
can be set either in your shell environment or within your Python script using the
{py:data}`os.environ` dictionary.

Here we list the environment variables used by PyGMT which are categorized into three groups:

1. System environment variables
2. GMT/PyGMT environment variables
3. Module-specific environment variables

## System Environment Variables

```{glossary}
TZ
    Specify the time zone for the current calendar time. It can be set to a string that
    defines the timezone, such as `"UTC"`, `"America/New_York"`, or `"Europe/London"`.
    Refer to [Specifying the Time Zone with TZ](https://www.gnu.org/software/libc/manual/html_node/TZ-Variable.html)
    for the valid format. If not set, the system's default timezone is used.
```

## GMT/PyGMT Environment Variables

```{glossary}
GMT_LIBRARY_PATH
    Specify the directory where the GMT shared library is located. This is useful when
    GMT is installed in a non-standard location or when you want to use a specific
    version of GMT. If not set, PyGMT will attempt to find the GMT library in standard
    system locations.

PYGMT_USE_EXTERNAL_DISPLAY
    Whether to use external viewers for displaying images. If set to `"false"`, PyGMT
    will not attempt to open images in external viewers. This can be useful when running
    tests or building the documentation to avoid popping up windows.
```

## Module-Specific Environment Variables

```{glossary}
X2SYS_HOME
    Specify the directory where x2sys databases and related settings will be stored.
    This environment variable is used by x2sys-related functions (e.g.,
    {func}`pygmt.x2sys_init`) to manage and access x2sys data. If not set, these
    functions will use a default directory or prompt for a location.
```
