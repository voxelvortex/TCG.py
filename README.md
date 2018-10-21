# TCG.py
TCG is a API wrapper for the TCGplayer written in python

Written to allow easier interaction with the TCGplayer api.

## Example

```
from tcg_player import *
api = api.Handler(bearer='bearer_token')
# or
api = api.Handler(public='public_key', private='private_key')
```

## Requirements

- Python 3+

## License

This program is licensed under the MIT license. Read more about that [here](https://opensource.org/licenses/MIT).