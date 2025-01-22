# pysgconnect

Python package to interact with SGConnect

## Install

You can install this package by using Pypi:

```sh
pip install pysgconnect
```

## Usage

### Protect HTTP requests

```python
from pysgconnect import SGConnectAuth
from requests import Session

session = Session()
# Do not hardcode your credential directly in your scripts, use a secure Vault solution instead
client_id = 
client_secret =

session.auth = SGConnectAuth(client_id, client_secret, scopes=['myscope'], env='PRD')

request = session.get('https://api.sgmarkets.com/foo/v1/bar')
```

#### Corporate proxy

By default, no proxies are configured.

```python
proxies = {'https': '...', 'http': '...'}
session.auth = SGConnectAuth(client_id, client_secret, scopes=['...'], proxies=proxies)
```

### Development

```sh
pip install -e .
```
