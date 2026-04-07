TASK_MEDIUM = {
    "name": "Database Auth Failure",
    "services": {
        "api": {"name": "api", "status": "running", "instances": 2, "cpu_usage": 15, "memory_usage": 40, "error_rate": 0.9},
        "database": {"name": "database", "status": "crashed", "instances": 1, "cpu_usage": 0, "memory_usage": 0, "error_rate": 1.0},
        "cache": {"name": "cache", "status": "running", "instances": 1, "cpu_usage": 10, "memory_usage": 10, "error_rate": 0.0},
        "worker": {"name": "worker", "status": "running", "instances": 1, "cpu_usage": 5, "memory_usage": 10, "error_rate": 0.0}
    },
    "logs": ["API: Connection pool exhausted", "DB: Access denied for user 'admin'@'%'"],
    "latency": 500, "traffic": 1200
}