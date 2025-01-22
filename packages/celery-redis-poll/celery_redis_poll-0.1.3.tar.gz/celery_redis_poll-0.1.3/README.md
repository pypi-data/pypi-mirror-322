# Celery Redis Poll Backend

A specialized Redis backend for Celery that replaces the default pub/sub mechanism for task result retrieval with a polling-based approach.

## Why Polling Instead of Pub/Sub?

The default Celery Redis backend uses Redis pub/sub for real-time task result notifications. While pub/sub provides immediate updates, it can face challenges in certain scenarios:

- Deadlocks in highly concurrent/multi-threaded workloads due to single-threaded nature of Redis and Celery clients.
- Higher overhead with `SUBSCRIBE` channels.

This backend provides a more robust alternative by using a polling mechanism instead.

## Features

- **Polling-Based Results**: Replaces pub/sub with an efficient polling mechanism for task result retrieval
- **Compatible with Existing Code**: Drop-in replacement for the standard Redis backend
- **Configurable Polling**: Adjust polling intervals and timeouts to match your needs
- **Resource Efficient**: Reduces Redis memory usage by eliminating pub/sub channels

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