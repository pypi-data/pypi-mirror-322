from typing import Type
from celery import Celery

from pytest import mark
import pytest


from celery_redis_poll import install_redis_poll_backend, PollingRedisBackend, PollingRedisClusterBackend


@mark.parametrize("protocol, expected_backend", [
    ("redispoll", PollingRedisBackend),
    ("redisclusterpoll", PollingRedisClusterBackend),
    ("redisspoll", PollingRedisBackend),
])
def test_redis_cluster_backend_installation(
    protocol: str, expected_backend: Type,
):
    install_redis_poll_backend()

    # Initialize Celery app with RedisClusterBackend
    app = Celery(
        'test_app',
        broker='redis://localhost:6379/0',
        backend=f'{protocol}://localhost:6379/0'
    )

    # Check if the backend is set correctly
    assert isinstance(app.backend, expected_backend), f"Backend is not set to {expected_backend}"

if __name__ == "__main__":
    pytest.main()