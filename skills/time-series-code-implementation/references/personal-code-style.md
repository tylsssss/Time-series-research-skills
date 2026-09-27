# Personal Code Style

This is the shipped `default` profile: **no personal code-style contract is configured.**

Follow `references/research-code-conventions.md` for seeds, configuration, logging,
leakage-safe splits, and checkpoints. Beyond that, prefer the conventions of the library
or codebase you are extending, and be consistent within a project.

## Note on the inline style contract

`SKILL.md` summarizes five style rules in its *Personal Style Contract* section. Those
five rules describe the **`default` profile**, not a universal requirement. When this
file is neutral, the summary is a historical default rather than an instruction: read it
as one reasonable style among several, and prefer these general principles where they
conflict:

* keep each phase of logic readable as a unit — whether that means one method or a few
  well-named ones depends on the language and the codebase;
* do not fragment coherent logic into small private helpers purely to shorten methods,
  and do not compress readable logic into one-liners purely to shorten methods either;
* place input validation at real boundaries (entry points, construction-time invariants,
  external library contracts) rather than scattering defensive checks through a flow;
* comment tensor-shape transformations inline when the framework makes shapes
  non-obvious, and otherwise comment intent rather than restating the code;
* declare search spaces, action lists, and constants as data rather than encoding them
  in branching logic.

## Writing your own style contract

If you fill this file in, make it decisive: state the rules that override generic
conventions, and give an example of the pattern you want and the pattern you do not
want. The implementation skill treats this file as authoritative over
`research-code-conventions.md` and over the inline summary in `SKILL.md`, so an
ambiguous file here produces inconsistent code.
