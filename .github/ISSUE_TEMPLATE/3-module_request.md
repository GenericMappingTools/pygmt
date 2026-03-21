---
name: Wrapper for a GMT module
about: Track the progress of wrapping a GMT module. [For project maintainers only!]
title: "Wrapper: Description of the module"
labels: ["feature request"]

---

*This issue serves as the central place for discussing and tracking the implementation of the `<wrapper>` method in PyGMT. The issue will be closed when the initial implementation is complete. Progress is tracked at https://github.com/orgs/GenericMappingTools/projects/3.*

## Documentation

- GMT: https://docs.generic-mapping-tools.org/dev/<module>.html
- GMT.jl: https://www.generic-mapping-tools.org/GMTjl_doc/documentation/modules/<module>
- PyGMT: https://www.pygmt.org/dev/api/generated/<wrapper>.html

## GMT Option Flags and Modifiers

☑️: *Implemented*; ⬜: *To be implemented/discussed*; ~~Strikethrough~~: *Won't implement*.

- [ ] `-B`: `frame`
- [ ] `-J`: `projection`
- [ ] `-R`: `region`
- [ ] ...
- [ ] ~~`-U`~~: Use `Figure.timestamp` instead.
- [ ] `-V`: `verbose`
- [ ] ~~`-X`/`-Y`~~: Use `Figure.shift_origin` instead.
- [ ] ~~`--PAR=value`~~: Use `pygmt.config` instead.

## Related GMT configurations

*List any related GMT configurations that may affect the behavior.*

## Notes on Input Formats

*Add any notes on the input formats, especially the meaning of columns.*

## Linked Pull Requests

- [ ] Initial feature implementation
- [ ] Add a tutorial or gallery example

## Related Issues and Discussions

*Add links to related wrapper discussions, API design threads, or upstream GMT changes here.*
