---
file_format: mystnb
---

```{code-cell}
---
tags: [remove-input]
---
from IPython.display import display, Markdown
from pygmt.encodings import charset


def get_charset_mdtable(name):
    """
    Create a markdown table for a charset.
    """
    mappings = charset[name]

    text = "| Octal | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |\n"
    text += "|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|\n"
    for i in range(0o00, 0o400, 8):
        chars = [mappings.get(j) for j in range(i, i + 8)]
        if all(v is None for v in chars):  # All characters in this row are undefined
            continue
        row = f"\\{i:03o}"[:-1] + "x"
        chars = [f"&#x{ord(char):04x};" for char in chars]
        text += f"| **{row}** | {' | '.join(chars)} |\n"
    text += "\n"
    return Markdown(text)
```

# Supported Encodings and Non-ASCII Characters

PyGMT supports a number of encodings and each encoding contains a set of ASCII and
non-ASCII characters. In PyGMT, you can use any of these ASCII and non-ASCII characters
in arguments and text strings. When using non-ASCII characters in PyGMT, the easiest way
is to copy and paste the character from the encoding tables below.

**Note**: The special character &#xfffd; (REPLACEMENT CHARACTER) is used to indicate
that the character is undefined in the encoding.

## Adobe ISOLatin1+ Encoding

```{code-cell}
---
tags: [remove-input]
---
display(get_charset_mdtable("ISOLatin1+"))
```

## Adobe Symbol Encoding

```{code-cell}
---
tags: [remove-input]
---
display(get_charset_mdtable("Symbol"))
```

**Note**: The octal code `\140` represents the RADICAL EXTENDER character, which is not
available in the Unicode character set.

## Adobe ZapfDingbats Encoding

```{code-cell}
---
tags: [remove-input]
---
display(get_charset_mdtable("ZapfDingbats"))
```

## ISO/IEC 8859

PyGMT also supports the ISO/IEC 8859 standard for 8-bit character encodings. Refer to
[ISO/IEC 8859](https://en.wikipedia.org/wiki/ISO/IEC_8859) for descriptions of the
different parts of the standard.

For a list of the characters in each part of the standard, refer to the following links:

- [ISO/IEC 8859-1](https://en.wikipedia.org/wiki/ISO/IEC_8859-1)
- [ISO/IEC 8859-2](https://en.wikipedia.org/wiki/ISO/IEC_8859-2)
- [ISO/IEC 8859-3](https://en.wikipedia.org/wiki/ISO/IEC_8859-3)
- [ISO/IEC 8859-4](https://en.wikipedia.org/wiki/ISO/IEC_8859-4)
- [ISO/IEC 8859-5](https://en.wikipedia.org/wiki/ISO/IEC_8859-5)
- [ISO/IEC 8859-6](https://en.wikipedia.org/wiki/ISO/IEC_8859-6)
- [ISO/IEC 8859-7](https://en.wikipedia.org/wiki/ISO/IEC_8859-7)
- [ISO/IEC 8859-8](https://en.wikipedia.org/wiki/ISO/IEC_8859-8)
- [ISO/IEC 8859-9](https://en.wikipedia.org/wiki/ISO/IEC_8859-9)
- [ISO/IEC 8859-10](https://en.wikipedia.org/wiki/ISO/IEC_8859-10)
- [ISO/IEC 8859-11](https://en.wikipedia.org/wiki/ISO/IEC_8859-11)
- [ISO/IEC 8859-13](https://en.wikipedia.org/wiki/ISO/IEC_8859-13)
- [ISO/IEC 8859-14](https://en.wikipedia.org/wiki/ISO/IEC_8859-14)
- [ISO/IEC 8859-15](https://en.wikipedia.org/wiki/ISO/IEC_8859-15)
- [ISO/IEC 8859-16](https://en.wikipedia.org/wiki/ISO/IEC_8859-16)
