# TCG.py
TCG is a API wrapper for the TCGplayer API written in python

This library was written to allow easier interaction with the TCGplayer API.

## Example

```
from tcg_py.api import Handler
api = Handler(bearer='bearer_token')
# or
api = Handler(public='public_key', private='private_key')
```

## Requirements

- Python 3+

## License

This program is licensed under the MIT license. Read more about that [here](https://opensource.org/licenses/MIT).
