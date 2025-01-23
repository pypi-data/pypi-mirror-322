from typing import Type
from celery import Celery
from celery.backends.redis import RedisBackend

from pytest import mark
import pytest


from celery_redis_poll_backend import (
    PollingRedisBackend,
    PollingRedisClusterBackend,
    install_redis_poll_backend,
)


@mark.parametrize(
    "protocol, expected_backend",
    [
        ("redis", RedisBackend),
        ("redispoll", PollingRedisBackend),
        ("redisclusterpoll", PollingRedisClusterBackend),
    ],
)
def test_redis_cluster_backend_installation(
    protocol: str,
    expected_backend: Type,
):
    install_redis_poll_backend()

    # Initialize Celery app with RedisClusterBackend
    app = Celery(
        "test_app",
        broker="redis://localhost:6379/0",
        backend=f"{protocol}://localhost:6379/0",
    )

    # Check if the backend is set correctly
    assert isinstance(app.backend, expected_backend), (
        f"Backend is not set to {expected_backend}"
    )


if __name__ == "__main__":
    pytest.main()
