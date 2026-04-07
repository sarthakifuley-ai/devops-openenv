TASK_HARD = {
    "services": {
        "api": {"name":"api", "status":"running", "instances":1, "cpu_usage":98, "memory_usage":90, "error_rate":0.6},
        "database": {"name":"database", "status":"running", "instances":1, "cpu_usage":85, "memory_usage":70, "error_rate":0.1},
        "cache": {"name":"cache", "status":"crashed", "instances":1, "cpu_usage":0, "memory_usage":0, "error_rate":1.0},
        "worker": {"name":"worker", "status":"running", "instances":2, "cpu_usage":30, "memory_usage":30, "error_rate":0.0}
    },
    "logs": [
        "ALERT: Ingress traffic spike detected: 15,000 req/s",
        "CACHE: Connection refused - service down",
        "API: Upstream request timeout (504)"
    ],
    "latency": 1500, 
    "traffic": 15000
}