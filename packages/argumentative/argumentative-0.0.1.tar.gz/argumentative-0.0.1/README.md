# 🗣️ argumentative
simple, opinionated command line parser

## features
- simple, opinionated
- automatically generates help and usage messages
- uses msgspec for structs and type coercion
- secret fourth feature

## usage
```bash
pip install argumentative
```

```python
from argumentative import argumentative

@argumentative
class Args:
    config: str # path to a config file
    verbose: bool = False # whether to print verbose output

args = Args.from_args()
print(args)
```

```bash
python basic.py config.json --verbose
# Args(config='config.json', verbose=True)

python basic.py --help
# basic.py - example of using argumentative
#
# Options:
# --config <str> - path to a config file
# --verbose <bool> - whether to print verbose output
```

## license
[hippocratic license 3.0](LICENSE.md). (c) allura-org