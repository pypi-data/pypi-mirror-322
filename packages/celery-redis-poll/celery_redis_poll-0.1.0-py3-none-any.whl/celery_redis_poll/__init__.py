"""
Celery Redis Cluster Backend
~~~~~~~~~~~~~~~~~~~~~~~~~~~

A Redis Cluster backend implementation for Celery.
"""


__version__ = '0.1.0'

# Register the backend
from celery.app.backends import BACKEND_ALIASES

from celery_redis_poll.backend import PollingRedisBackend, PollingRedisClusterBackend

BACKEND_ALIASES['rediscluster+poll'] = 'celery_redis_cluster_backend.backend:RedisClusterBackend'

__all__ = ['PollingRedisBackend', 'PollingRedisClusterBackend']
