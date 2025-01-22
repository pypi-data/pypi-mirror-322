from celery.backends.redis import RedisBackend
from typing import Any, Optional
import celery
from celery_redis_cluster_backend import RedisClusterBackend


class PollingRedisBackend(celery.backends.base.SyncBackendMixin, RedisBackend):
    """
    Disables pub/sub for getting task results and instead uses polling.
    """
    def _set(self, key: str, value: str) -> None:
        """
        Simply set value in Redis, do not publish.
        :param key:
        :param value:
        :return:
        """
        if self.expires:
            self.client.setex(key, self.expires, value)
        else:
            self.client.set(key, value)

    def on_task_call(self, *args: Any, **kwargs: Any) -> None:
        pass


class PollingRedisClusterBackend(PollingRedisBackend, RedisClusterBackend):
    """
    Same as PollingRedisBackend but with ReidsCluster for client.
    """
    pass