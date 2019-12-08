# Nutmeg Python Class

Access your portfolio through this Python class object.

**Note:**
Currently, this does not support 2FA if it's enabled on your account.

## Installation

Install Python 3

Setup requirements:

```bash
pip3 install -r requirements.txt
```

## Usage

```python
from nutmeg import Nutmeg

api = Nutmeg("your email", "your password")
api.login()

portfolio_values = api.get_values()
```
