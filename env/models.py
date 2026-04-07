from pydantic import BaseModel
from typing import Dict, List, Optional

class ServiceState(BaseModel):
    name: str
    status: str
    instances: int
    cpu_usage: float
    memory_usage: float
    error_rate: float

class SystemState(BaseModel):
    services: Dict[str, ServiceState]
    logs: List[str]
    latency: float
    traffic: int