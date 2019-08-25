# boolipy

Scrapy service to access Booli api. To be able to use the service you need to
[request access to the API](https://www.booli.se/api/key).

## DISCLAIMER

This repository contains unofficial code. The author has nothing to do with
Booli.

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

To print the help:
    ```
    boolipy --help
    ```

Search the sold apartments around a given coordinate:
    ```
    boolipy --center "59.334438,18.029522" --dim "400,500" --endpoint sold --limit
1000 --offset 0 --follow
    ```

### Jupyter-notebook

To use jupyter notebook and all the analytics tools, install the dependencies:
```
pip install -e .[analytics]
```

And then execute the `jupyter-notebook`.
