import os
from openenv import RemoteEnvClient 

# 1. Initialize the Environment Client (Connects to your Hugging Face Space)
API_BASE_URL = os.getenv("API_BASE_URL", "https://sarthaki-19-devops-openenv.hf.space")
env = RemoteEnvClient(api_base_url=API_BASE_URL)

# Import your local task/grader logic
from graders.easy_grader import grade as grade_easy
from graders.medium_grader import grade_medium
from graders.hard_grader import grade_hard
from tasks.easy_incident import TASK_EASY
from tasks.medium_incident import TASK_MEDIUM
from tasks.hard_incident import TASK_HARD

class AIOpsAgent:
    """Wrapper to make your decision function compatible with the predict() call."""
    def predict(self, state):
        return mock_decision(state)

def mock_decision(state_dict):
    """Priority-based baseline: scale, repair, restart, otherwise idle."""
    services = state_dict.get('services', {})
    logs = state_dict.get('logs', [])
    log_text = " ".join(logs).lower()

    if "traffic" in log_text or "req/s" in log_text or state_dict.get('traffic', 0) > 5000:
        api_svc = services.get('api', {})
        if api_svc.get('instances', 1) < 3:
            return {
                "action_type": "scale_service",
                "target": "api",
                "value": 3,
                "reasoning": "SRE: Traffic spike detected. Scaling API."
            }

    if "auth" in log_text or "access denied" in log_text or services.get('database', {}).get('status') == 'crashed':
        return {
            "action_type": "update_config",
            "target": "database",
            "value": "fix_auth_credentials",
            "reasoning": "SRE: Database authentication failure detected."
        }

    for name, svc in services.items():
        if svc.get('status') == 'crashed':
            return {
                "action_type": "restart_service",
                "target": name,
                "reasoning": f"SRE: {name} is crashed. Restarting."
            }

    return {"action_type": "none", "target": "none", "reasoning": "System stable."}

def evaluate_task(agent, task, grader, max_steps=15):
    if env is None:
        raise Exception("Environment not initialized.")

    task_id = task.get('id', 'easy')
    state = env.reset(task_id=task_id)
    total_reward = 0
    
    for step_num in range(max_steps):
        # Use the agent's predict method
        action = agent.predict(state)
        
        # Unpack the 4 values returned by RemoteEnvClient
        state, reward, done, info = env.step(action)
        total_reward += reward
        
        if done:
            break
            
    return grader(state, total_reward) # Call the grader function directly

def run_baseline():
    # Initialize our agent wrapper
    agent = AIOpsAgent()
    
    task_suite = [
        ("Easy: API Crash", TASK_EASY, grade_easy),
        ("Medium: Database Auth Failure", TASK_MEDIUM, grade_medium),
        ("Hard: Cascading Traffic Flood", TASK_HARD, grade_hard),
    ]

    results = []
    for name, task, grader_func in task_suite:
        print(f"Running baseline for: {name}")
        # PASS THE AGENT OBJECT, NOT THE NAME STRING
        result = evaluate_task(agent, task, grader_func, max_steps=task.get('max_steps', 15))
        results.append(result)

    print("\nBaseline Evaluation Summary Complete.")
    return results

if __name__ == '__main__':
    run_baseline()