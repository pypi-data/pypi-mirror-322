# Bugs
## cli
1. `Config` has `REPO_ROOT` going to `debug` property (that's a bug)

## pylib
1. line 120 `list[str]` should be `str` (the `*args` implies `list`)


# Notes
`Dml[...]` => invoke

Should we not sleep between polling? line 221?

Dag.import_


OP IN BUILTINS vs start_fn with None adapter and string for op...