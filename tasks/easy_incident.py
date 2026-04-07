TASK_EASY = {
    "services": {
        "api": {"name":"api", "status":"crashed", "instances":1, "cpu_usage":0, "memory_usage":0, "error_rate":1.0},
        "database": {"name":"database", "status":"running", "instances":1, "cpu_usage":20, "memory_usage":30, "error_rate":0.0},
        "cache": {"name":"cache", "status":"running", "instances":1, "cpu_usage":10, "memory_usage":10, "error_rate":0.0},
        "worker": {"name":"worker", "status":"running", "instances":1, "cpu_usage":10, "memory_usage":10, "error_rate":0.0}
    },
    "logs": ["API process exited with code 137 (OOM)"],
    "latency": 0, "traffic": 100
}