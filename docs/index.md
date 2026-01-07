# k3pattern

[![Action-CI](https://github.com/pykit3/k3pattern/actions/workflows/python-package.yml/badge.svg)](https://github.com/pykit3/k3pattern/actions/workflows/python-package.yml)
[![Documentation Status](https://readthedocs.org/projects/k3pattern/badge/?version=stable)](https://k3pattern.readthedocs.io/en/stable/?badge=stable)
[![Package](https://img.shields.io/pypi/pyversions/k3pattern)](https://pypi.org/project/k3pattern)

Find common prefix of strings, tuples, and nested structures.

k3pattern is a component of [pykit3](https://github.com/pykit3) project: a python3 toolkit set.

## Installation

```bash
pip install k3pattern
```

## Quick Start

```python
from k3pattern import common_prefix

# Find common prefix of strings
common_prefix('abc', 'abd')
# 'ab'

# Find common prefix of tuples
common_prefix(('a', 'b', 'c'), ('a', 'b', 'd'))
# ('a', 'b')

# Nested structures (recursive by default)
common_prefix(('a', 'bc', 'x'), ('a', 'bd', 'y'))
# ('a', 'b')

# Disable recursive mode
common_prefix(('a', 'bc', 'x'), ('a', 'bd', 'y'), recursive=False)
# ('a',)
```

## API Reference

::: k3pattern

## License

The MIT License (MIT) - Copyright (c) 2015 Zhang Yanpo (张炎泼)
