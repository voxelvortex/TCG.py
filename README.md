# TCG.py
TCG is a API wrapper for the TCG Player API written in python

This library was written to allow easier interaction with the TCG Player API.

## Requirements

- [Python 3+](https://www.python.org/)
- [Git](https://git-scm.com/)
- [requests](https://pypi.org/project/requests/)

## Installation

```
git clone https://github.com/voxelvortex/TCG.py.git
cd TCG.py
python setup.py sdist
cd dist
pip install tcgplayer-1.0.tar.gz
pip install requests
```

## Example

```
from tcg_py.api import Handler
api = Handler(bearer='bearer_token')
# or
api = Handler(public='public_key', private='private_key')
```

Methods are based off of the [TCG Player Docs](docs.tcgplayer.com/reference), but reformatted to be consistent with pep8 formatting.
For example, the parameter "getExtendedFields" was renamed to "get_extended_fields". 

## License

This program is licensed under the MIT license. Read more about that [here](https://opensource.org/licenses/MIT).

