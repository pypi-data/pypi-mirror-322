# BingX API Client

This Python client facilitates communication with the BingX API, providing options for both synchronous and asynchronous request handling. It features caching, error management, and automatic request signing to improve your development workflow.

---

## Features

- **Fully Typed**: Utilizes Python's type hints and Pydantic models for enhanced type safety.
- **Caching Support**: Minimizes API calls by caching GET requests. (`temporarily disabled`)
- **Error Handling**: Robust error management with specific exceptions for various API error codes.
- **Request Signing**: Automatically signs requests using your API credentials.
- **Synchronous and Asynchronous**: Capable of handling both synchronous and asynchronous requests.

---

For more details, please check out the [documentation](https://bingx-py.readthedocs.io/en/latest/).

## TODOs

- [ ] Make coverage tests.
- [ ] Add websocket stream support.
- [ ] Refactor models to use Generics for better type hints.
- [ ] Add `use_cache` param for method calls.
- [ ] Add support to async decode response by `msgspec`
- [ ] Prettify documentation

---

## Installation

Install the client using pip:

```bash
pip install bingx-py
```

Or, if you're using Poetry:

```bash
poetry add bingx-py
```

---

## Usage

### Synchronous Client

You can use the client synchronously with a context manager or manually using `try-except-finally`.

#### Using Context Manager

```python
from bingx_py import BingXHttpClient

with BingXHttpClient(api_key="your_api_key", api_secret="your_api_secret", base_url="https://api.bingx.com") as client:
    response = client.spot.query_assets()
    print(response)
```

#### Using `Try-Except-Finally`

```python
from bingx_py import BingXHttpClient, exceptions

client = BingXHttpClient(api_key="your_api_key", api_secret="your_api_secret", base_url="https://api.bingx.com")
try:
    client.connect()
    response = client.spot.query_assets()
    print(response)
except exceptions.APIError as e:
    print("An error occurred:", e)
finally:
    client.close()
```

### Asynchronous Client

You can also use the client asynchronously with an async context manager or manually using `try-except-finally`.

#### Using Async Context Manager

```python
import asyncio
from bingx_py import BingXHttpClient

async def main():
    async with BingXHttpClient(api_key="your_api_key", api_secret="your_api_secret", base_url="https://api.bingx.com") as client:
        response = await client.spot.query_assets()
        print(response)

asyncio.run(main())
```

#### Using `Try-Except-Finally`

```python
import asyncio
from bingx_py import BingXHttpClient, exceptions

async def main():
    client = BingXHttpClient(api_key="your_api_key", api_secret="your_api_secret", base_url="https://api.bingx.com")
    try:
        await client.connect_async()
        response = await client.spot.query_assets()
        print(response)
    except exceptions.APIError as e:
        print("An error occurred:", e)
    finally:
        await client.close_async()

asyncio.run(main())
```

---

## Caching Configuration

The client supports flexible caching configuration. You can set up caching globally or pass a cache instance directly to the client.

### Supported Cache Types

- **AsyncRedisCache**: Asynchronous Redis-based caching (`async-redis`).
- **SyncRedisCache**: Synchronous Redis-based caching (`sync-redis`).
- **AsyncMemoryCache**: Asynchronous in-memory caching (`async-memory`).
- **SyncMemoryCache**: Synchronous in-memory caching (`sync-memory`).

By default, the client uses a synchronous in-memory cache.

### Setting Cache Globally

Use the `set_cache` function to configure the cache globally:

```python
from bingx_py.config import set_cache

# Set up synchronous Redis cache
set_cache(cache_type="sync-redis", host="localhost", port=6379, db=0)

# Set up asynchronous Redis cache
set_cache(cache_type="async-redis", host="localhost", port=6379, db=0)

# Set up synchronous in-memory cache
set_cache(cache_type="sync-memory")

# Set up asynchronous in-memory cache
set_cache(cache_type="async-memory")
```

### Passing Cache to the Client

Alternatively, pass a cache instance directly when initializing the client:

```python
from bingx_py import BingXHttpClient
from bingx_py.caching import SyncMemoryCache

# Create a synchronous in-memory cache
cache = SyncMemoryCache()

# Pass the cache to the client
client = BingXHttpClient(
    api_key="your_api_key",
    api_secret="your_api_secret",
    base_url="https://api.bingx.com",
    cache=cache,
)
```

### Enabling Unsafe Caching

By default, caching is only supported for GET requests. To enable caching for other HTTP methods (e.g., POST, PUT, DELETE), enable unsafe caching globally:

```python
from bingx_py import cache_config

cache_config.enable_unsafe_cache()  # Enable unsafe caching
```

### Example: Using Redis Cache

Here’s an example of setting up and using a Redis cache:

```python
from bingx_py import BingXHttpClient
from bingx_py.config import set_cache

# Set up synchronous Redis cache globally
set_cache(cache_type="sync-redis", host="localhost", port=6379, db=0)

# Initialize the client
client = BingXHttpClient(
    api_key="your_api_key",
    api_secret="your_api_secret",
)

# Make a request with caching
response = client.spot.query_assets(use_cache=True)
print(response)
```

### Example: Using In-Memory Cache

Here’s an example of using an in-memory cache:

```python
from bingx_py import BingXHttpClient
from bingx_py.caching import SyncMemoryCache

# Create a synchronous in-memory cache
cache = SyncMemoryCache()

# Pass the cache to the client
client = BingXHttpClient(
    api_key="your_api_key",
    api_secret="your_api_secret",
    cache=cache,
)

# Make a request with caching
response = client._request("GET", "/api/v1/ping", use_cache=True)
print(response)
```

### Cache Key Generation

Cache keys are generated based on the HTTP method, endpoint, parameters, and an optional unique attribute. For example, a request to `/api/v1/ping` with parameters `{"foo": "bar"}` generates a cache key like: `GET:api/v1/ping:foo=bar`.

You can also provide a `unique_cache_attribute` to customize the cache key:

```python
response = client._request(
    "GET",
    "/api/v1/ping",
    params={"foo": "bar"},
    use_cache=True,
    unique_cache_attribute="custom_key",
)
```

This generates a cache key like: `GET:api/v1/ping:foo=bar:custom_key`.

---

## Error Handling

The client includes comprehensive error handling. If the API returns an error, the client raises a specific exception based on the error code.

```python
try:
    response = client._request("GET", "/api/v1/invalid_endpoint")
except exceptions.NotFoundError as e:
    print(f"Not Found: {e.message}")
except exceptions.APIError as e:
    print(f"API Error: {e.message}")
```

---

## Contributing

### Merge Requests

1. **Branch Naming**: Name your branch according to the feature or bugfix (e.g., `feature/add-new-endpoint` or `bugfix/fix-issue-123`).
2. **Code Style**: Follow the existing code style and ensure your code is fully typed.
3. **Tests**: Include tests for new features or bugfixes.
4. **Documentation**: Update the README or other documentation if necessary.

### Issues

1. **Bug Reports**: Provide a detailed description of the bug, including steps to reproduce and expected vs. actual behavior.
2. **Feature Requests**: Describe the feature you would like to see, including relevant use cases.

---

## Special Thanks

Special thanks to the [Deepseek](https://deepseek.com/) team for developing the AI model that powers a significant portion of this library.

---

## Projects Using This Library

If your project uses this library, let me know by creating an issue, and I’ll add it to this list!

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Feel free to contribute by submitting merge requests or reporting issues. Happy coding! 🚀
