# PyJokers

[![Build Status](https://github.com/tianhukj/pyjokers/actions/workflows/publish.yml/badge.svg)](https://github.com/tianhukj/pyjokers/actions)
![License](https://img.shields.io/github/license/tianhukj/pyjokers.svg)
![PyPI](https://img.shields.io/pypi/v/pyjokers)
[![Buy Me a Coffee](https://img.shields.io/badge/Donate-Buy%20Me%20A%20Coffee-FF813F.svg?logo=buy-me-a-coffee)](https://www.buymeacoffee.com/tianhukj)
[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://www.python.org/downloads/)

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

## Development
```
git clone https://github.com/tianhukj/pyjokers.git
```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
