# PyJokers

[![Build Status](https://github.com/tianhukj/pyjokers/actions/workflows/publish.yml/badge.svg)](https://github.com/tianhukj/pyjokers/actions)
![License](https://img.shields.io/github/license/tianhukj/pyjokers.svg)
[![PyPI version](https://badge.fury.io/py/pyjokers.svg)](https://badge.fury.io/py/pyjokers)

PyJokers is a simple Python library that generates random jokes. It supports multiple categories of jokes, including cold jokes and programmer jokes.

## Installation

You can install this library using pip:

```bash
pip install pyjokers
```

## For example
```
from pyjokers import PyJokers

joke_gen = PyJokers()
print(joke_gen.get_joke('programmer jokes'))
print(joke_gen.get_joke('cold jokes'))
print(joke_gen.get_joke())  # Random category
```
