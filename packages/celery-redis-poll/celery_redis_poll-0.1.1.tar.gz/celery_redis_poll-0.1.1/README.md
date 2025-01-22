# Celery Redis Poll Backend

A specialized Redis backend for Celery that replaces the default pub/sub mechanism for task result retrieval with a polling-based approach.

## Why Polling Instead of Pub/Sub?

The default Celery Redis backend uses Redis pub/sub for real-time task result notifications. While pub/sub provides immediate updates, it can face challenges in certain scenarios:

- High memory usage in Redis due to pub/sub channel maintenance
- Connection stability issues in distributed environments
- Potential message loss during network interruptions
- Scaling limitations with large numbers of subscribers

This backend provides a more robust alternative by using a polling mechanism instead.

## Features

- **Polling-Based Results**: Replaces pub/sub with an efficient polling mechanism for task result retrieval
- **Compatible with Existing Code**: Drop-in replacement for the standard Redis backend
- **Configurable Polling**: Adjust polling intervals and timeouts to match your needs
- **Resource Efficient**: Reduces Redis memory usage by eliminating pub/sub channels
- **Network Friendly**: Better handles network interruptions and reconnections

## Installation

```bash
pip install celery-redis-poll
```

## Usage

Configure your Celery application to use the polling backend:

```python
from celery import Celery

from celery_redis_poll import install_redis_poll_backend

# Registers the polling backend
install_redis_poll_backend()

app = Celery('your_app',
             broker='redis://localhost:6379/0',
             backend='redispoll://localhost:6379/0')
```

For clustered Redis, use `redisclusterpoll` instead of `redispoll`.


### Configuration Options

```python
app.conf.update(
    # How often to poll for results (in seconds)
    redis_poll_interval=0.5,
    
    # Maximum time to poll for a result (in seconds)
    redis_poll_timeout=3600,
    
    # Standard Redis options are also supported
    redis_socket_timeout=30.0,
    redis_socket_connect_timeout=30.0,
)
```

## Requirements

- Python >= 3.7
- Celery >= 5.0.0
- Redis >= 4.5.0
- celery-redis-cluster >= 0.1.6

## Development

For development, install extra dependencies:

```bash
pip install celery-redis-poll[dev]
```

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.