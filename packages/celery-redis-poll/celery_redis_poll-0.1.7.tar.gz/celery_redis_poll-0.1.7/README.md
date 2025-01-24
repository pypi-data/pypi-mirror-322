# Celery Redis Poll Backend

A specialized Redis backend for Celery that replaces the default pub/sub mechanism for task result retrieval with a polling-based approach.

## Why Polling Instead of Pub/Sub?

The default Celery Redis backend uses Redis pub/sub for real-time task result notifications. While pub/sub provides immediate updates, it can face challenges in certain scenarios:

- Deadlocks in highly concurrent/multi-threaded workloads due to single-threaded nature of Redis and Celery clients.
- Higher overhead with `SUBSCRIBE` channels.

This backend provides a more robust alternative by using a polling mechanism instead.

## Features

- **Polling-Based Results**: Replaces pub/sub with a polling mechanism for task result retrieval
- **Compatible with Existing Code**: Drop-in replacement for the standard Redis backend
- **Configurable Polling**: Adjust polling intervals and timeouts to match your needs
- **Resource Efficient**: Reduces Redis memory usage by eliminating pub/sub channels

## Installation

```bash
pip install celery-redis-poll
```

After installation new backends are automatically registered with Celery:
- `redis+poll`
- `rediss+poll`
- `redis+cluster_poll`
- `rediss+cluster_poll`

## Usage

Configure your Celery application to use the polling backend:

```python
from celery import Celery

app = Celery('your_app',
             broker='redis://localhost:6379/0',
             backend='redis+poll://localhost:6379/0')
```

For clustered Redis, use `redis+cluster_poll`.

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