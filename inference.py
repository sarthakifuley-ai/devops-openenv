import os
from env.devops_env import DevOpsEnv 
from graders.easy_grader import grade as grade_easy
from graders.medium_grader import grade_medium
from graders.hard_grader import grade_hard
from tasks.easy_incident import TASK_EASY
from tasks.medium_incident import TASK_MEDIUM
from tasks.hard_incident import TASK_HARD

# Initialize with a default config to satisfy the constructor
env = DevOpsEnv(task_config=TASK_EASY) 

class AIOpsAgent:
    def predict(self, state):
        return mock_decision(state)

def mock_decision(state_dict):
    """Your SRE logic for scaling and restarting."""
    services = state_dict.get('services', {})
    logs = state_dict.get('logs', [])
    log_text = " ".join(logs).lower()

    if "traffic" in log_text or state_dict.get('traffic', 0) > 5000:
        if services.get('api', {}).get('instances', 1) < 3:
            return {"action_type": "scale_service", "target": "api", "value": 3}

    for name, svc in services.items():
        if svc.get('status') == 'crashed':
            return {"action_type": "restart_service", "target": name}

    return {"action_type": "none", "target": "none"}

def evaluate_task(agent, task, grader_func, max_steps=15):
    state = env.reset(task_id=task.get('id', 'easy'))
    total_reward = 0
    
    for _ in range(max_steps):
        action = agent.predict(state)
        result = env.step(action)
        
        # Robust unpacking
        state = result[0]
        reward = result[1]
        done = result[2]
        if len(result) > 4: # Handle Gymnasium 5-tuple
            done = done or result[3]
            
        total_reward += reward
        if done:
            break
            
    return grader_func(state, total_reward)

def run_baseline():
    agent = AIOpsAgent()
    task_suite = [
        ("Easy", TASK_EASY, grade_easy),
        ("Medium", TASK_MEDIUM, grade_medium),
        ("Hard", TASK_HARD, grade_hard),
    ]

    results = []
    for name, task, grader_func in task_suite:
        # CRITICAL: Pass 'agent', not 'name'
        res = evaluate_task(agent, task, grader_func, max_steps=task.get('max_steps', 15))
        results.append(res)
    return results

if __name__ == '__main__':
    run_baseline()