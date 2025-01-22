"""
Celery Redis Cluster Backend
~~~~~~~~~~~~~~~~~~~~~~~~~~~

A Redis Cluster backend implementation for Celery.
"""

from .backend import RedisClusterBackend

__version__ = '0.1.7'

# Register the backend
def install_redis_cluster_backend():
    from celery.app.backends import BACKEND_ALIASES
    BACKEND_ALIASES['rediscluster'] = 'celery_redis_cluster_backend.backend:RedisClusterBackend'

__all__ = ['RedisClusterBackend', "install_redis_cluster_backend"]
