# boolipy
Scrapy service to access Booli api. To be able to use the service you need to
[request access to the API](https://www.booli.se/api/key).

## Booli API

Of course, all of this is *powered by Booli*

* [Homepage](https://www.booli.se/api)
* [API endpoint](http://api.booli.se/)
* [Interactive Console URL](http://www.booli.se/api/explorer)
* [Terms Of Service URL](http://www.booli.se/api/tou/)

## Installation

Assuming that you have [requested access to the API](https://www.booli.se/api/key) and the `CALLER_ID` and `PRIVATE_KEY` are available.

```
cat << EOF > auth-data
#!/bin/bash

CALLER_ID="your-caller-id"
PRIVATE_KEY="your-private-key"

export CALLER_ID=$CALLER_ID
export PRIVATE_KEY=$PRIVATE_KEY
EOF

# export CALLER_ID and PRIVATE_KEY in your shell
source auth-data

# option 1: install the package from git
pip install git+https://github.com/aitorhh/boolipy

# option 2: install the package from source-code for test and devel
pip install .[dev,test]
```

## Usage

### CLI

*Note*: The CLI support with arguments is not implementeed yet.

```
boolipy
```

# TODO

- [] CLI arguments and options
- [] Listen to an amqp queue to request new data
