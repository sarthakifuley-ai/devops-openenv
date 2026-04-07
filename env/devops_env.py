from .models import SystemState, ServiceState
from .reward import calculate_reward
from .actions import execute_action

class DevOpsEnv:
    def __init__(self, task_config):
        self.config = task_config
        self.current_reward = 0.0
        self.reset()

    def reset(self):
        # Convert dictionary config to Pydantic models
        services = {k: ServiceState(**v) for k, v in self.config['services'].items()}
        self.state_data = SystemState(
            services=services,
            logs=list(self.config['logs']),
            latency=self.config['latency'],
            traffic=self.config['traffic']
        )
        self.current_reward = calculate_reward(self.state_data)
        return self.state_data

    def step(self, action):
        # 1. Apply AI action to the state
        self.state_data = execute_action(self.state_data, action)
        
        # 2. Update the reward based on the new state
        self.current_reward = calculate_reward(self.state_data)
        
        # 3. OpenEnv Spec: return (observation, reward, done, info)
        return self.state_data, self.current_reward, False, {}