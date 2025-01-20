# AenoX API
[![](https://img.shields.io/pypi/v/aenox.svg?style=for-the-badge&logo=pypi&color=yellow&logoColor=white)](https://pypi.org/project/aenox/)
[![](https://img.shields.io/pypi/l/aenox?style=for-the-badge&color=5865F2)](https://github.com/aenoxic/aenox-api/blob/main/LICENSE)
[![](https://img.shields.io/readthedocs/aenox-api?style=for-the-badge)](https://aenox-api.readthedocs.io/en/latest/)

## ⚙️ Installation
Python 3.10 or higher is required
```
pip install aenox
```

## 🚀 Example Usage
To be able to perform your API query properly, replace `[YOUR_API_KEY]` with a valid API key.

### Example

```python
from aenox import AenoXAPI

api = AenoXAPI(api_key="[YOUR_API_KEY]")
```


## 🫧 Cooldown
You can send 20 queries per second to the API. If you attempt to send another request before this cooldown has passed, you will receive a `aenox.errors.CooldownError`.

### Example
You cannot run this query twice within 2 seconds:
```python
from aenox import AenoXAPI

api = AenoXAPI(api_key="[YOUR_API_KEY]")

api.get_user_stats(user_id=123)
```

In such cases, use `try/except` to handle the error. For example:

```python
from aenox import CooldownError
from aenox import AenoXAPI

api = AenoXAPI(api_key="[YOUR_API_KEY]")

try:
    api.get_user_stats(user_id=123)
except CooldownError:
    print('Cooldown!')
```

