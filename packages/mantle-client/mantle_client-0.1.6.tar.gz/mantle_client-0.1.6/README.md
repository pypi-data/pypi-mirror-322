# Mantle Client

A Python client for interacting with the Mantle API.

## Installation

```bash
pip install mantle-client
```

## Usage

```python
from mantle_client import Client

# Initialize client
client = Client("http://your-mantle-server.com")

# Register a new user
client.register("user@example.com", "password123")

# Login
client.login("user@example.com", "password123")

# Get current user
user = client.get_current_user()
print(user)
```
