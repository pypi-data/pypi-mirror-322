from celery.backends.redis import RedisBackend
from typing import Any, Optional
from celery_redis_cluster_backend import RedisClusterBackend


class PollingRedisBackend(RedisBackend):
    """
    Disables pub/sub for gettign task results and instead using polling.
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

    def wait_for_pending(
        self, result_ids: list[str], timeout: Optional[int] = None, interval: float = 0.5, no_ack: bool = True
    ) -> list[dict]:
        """
        Overrides wait_for_pending to use polling instead of Pub/Sub.
        """
        # Poll Redis for results using pipeline
        start_time = self.app.now()
        while True:
            pipeline = self.client.pipeline()
            for task_id in result_ids:
                pipeline.get(self.get_key_for_task(task_id))
            results = pipeline.execute()

            if all(results):
                return [self.meta_from_decoded(self.decode_result(result)) for result in results]

            if timeout and (self.app.now() - start_time).total_seconds() >= timeout:
                raise TimeoutError("Timeout while waiting for task results.")

            self.app.sleep(interval)


class PollingRedisClusterBackend(PollingRedisBackend, RedisClusterBackend):
    """
    Same as PollingRedisBackend but with ReidsCluster for client.
    """
    pass