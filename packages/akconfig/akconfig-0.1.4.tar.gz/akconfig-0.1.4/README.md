# akconfig

A configuration management for global variables in python projects.
akconfig is a small python class that takes global variables and lets you manipulate them quickly. the advantage can be that you still need manipulations that are to be changed via arguments, or via environment variables. when executing the example file basic.py, it quickly becomes obvious what this is intended for.


## example

`$ poetry run basic`

## get help

```
poetry run basic --help
Usage: basic [OPTIONS]

Options:
  -c, --config <TEXT TEXT>...  Config parameters are: VAR_A, VAR_B, VAR_C,
                               VAR_D, VAR_E, VAR_F, VAR_G, VAR_H, VARS_MASK
  -f, --force-env-vars         Set argument if you want force environment
                               variables
  --help                       Show this message and exit.
```