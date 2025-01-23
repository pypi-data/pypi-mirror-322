__version__ = "0.1.6"

from celery_redis_poll_backend.backend import (
    PollingRedisBackend,
    PollingRedisClusterBackend,
)


def install_redis_poll_backend():
    from celery.app.backends import BACKEND_ALIASES

    BACKEND_ALIASES["redispoll"] = "celery_redis_poll.backend:PollingRedisBackend"
    BACKEND_ALIASES["redisclusterpoll"] = (
        "celery_redis_poll.backend:PollingRedisClusterBackend"
    )


__all__ = ["PollingRedisBackend", "PollingRedisClusterBackend"]
