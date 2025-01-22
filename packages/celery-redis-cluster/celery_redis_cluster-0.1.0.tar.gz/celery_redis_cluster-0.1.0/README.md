# Celery Redis Cluster Backend

A Redis Cluster backend implementation for Celery. This package allows you to use Redis Cluster as a result backend for Celery tasks, providing better scalability and high availability compared to a single Redis instance.

## Installation

```bash
pip install celery-redis-cluster-backend
```

## Usage

To use the Redis Cluster backend in your Celery application:

```python
from celery import Celery

app = Celery('your_app',
             broker='redis://localhost:6379/0',
             backend='rediscluster://localhost:6379/0')
```

### Configuration

The backend supports the following configuration options:

```python
app.conf.update(
    CELERY_RESULT_BACKEND='rediscluster://localhost:6379/0',
    CELERY_REDIS_CLUSTER_OPTIONS={
        'startup_nodes': [
            {'host': 'localhost', 'port': '6379'},
            # Add more nodes as needed
        ],
        'decode_responses': True,
        'skip_full_coverage_check': True,
    }
)
```

## Features

- Support for Redis Cluster as a Celery result backend
- Automatic handling of cluster node discovery
- Support for key-based sharding across cluster nodes
- Configurable connection settings

## Requirements

- Python >= 3.8
- Celery >= 5.3.0
- redis >= 4.5.0
- redis-py-cluster >= 2.1.0

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
