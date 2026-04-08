import os
from env.devops_env import DevOpsEnv 
from graders.easy_grader import grade as grade_easy
from graders.medium_grader import grade_medium
from graders.hard_grader import grade_hard
from tasks.easy_incident import TASK_EASY
from tasks.medium_incident import TASK_MEDIUM
from tasks.hard_incident import TASK_HARD

# FIX: Pass TASK_EASY (or any valid config) to the constructor
env = DevOpsEnv(task_config=TASK_EASY) 

class AIOpsAgent:
    def predict(self, state):
        return mock_decision(state)

# ... (keep your mock_decision function exactly as it was) ...

def evaluate_task(agent, task, grader_func, max_steps=15):
    # Resetting with the new task_id usually updates the internal config
    state = env.reset(task_id=task.get('id', 'easy'))
    total_reward = 0
    
    for step_num in range(max_steps):
        action = agent.predict(state)
        
        # Safe unpacking for 4 or 5 return values
        result = env.step(action)
        state = result[0]
        reward = result[1]
        done = result[2]
        # Handle cases where the env returns 5 values (Gymnasium style)
        if len(result) > 4:
            done = done or result[3] 
        
        total_reward += reward
        if done:
            break
            
    return grader_func(state, total_reward)

def run_baseline():
    agent = AIOpsAgent()
    task_suite = [
        ("Easy: API Crash", TASK_EASY, grade_easy),
        ("Medium: Database Auth Failure", TASK_MEDIUM, grade_medium),
        ("Hard: Cascading Traffic Flood", TASK_HARD, grade_hard),
    ]

    results = []
    for name, task, grader_func in task_suite:
        # Pass the actual function, not the name string
        result = evaluate_task(agent, task, grader_func, max_steps=task.get('max_steps', 15))
        results.append(result)
    
    return results

if __name__ == '__main__':
    run_baseline()