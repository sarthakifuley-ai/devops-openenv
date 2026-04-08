import os
import sys
import traceback
import logging

# Use flush=True globally for all prints to ensure the validator sees them immediately
def log_print(message):
    print(message, flush=True)

def evaluate_task(agent, task, max_steps=15):
    from your_env_module import env 
    
    task_name = task.get('id', 'task_default')
    
    # --- REQUIRED: [START] block ---
    log_print(f"[START] task={task_name}")
    
    try:
        state = env.reset(task_id=task_name)
    except Exception as e:
        # If reset fails, we still need to [END] or the parser hangs
        log_print(f"[END] task={task_name} score=0 steps=0 status=error")
        return

    total_reward = 0
    actual_steps = 0
    
    try:
        for step in range(1, max_steps + 1):
            action = agent.act(state)
            state, reward, done, info = env.step(action)
            total_reward += reward
            actual_steps = step
            
            # --- REQUIRED: [STEP] block ---
            log_print(f"[STEP] step={step} reward={reward}")
            
            if done:
                break
        
        # --- REQUIRED: [END] block ---
        log_print(f"[END] task={task_name} score={total_reward} steps={actual_steps}")

    except Exception as e:
        log_print(f"[END] task={task_name} score={total_reward} steps={actual_steps} status=crashed")

def run_baseline():
    # 1. Initialize Agent
    try:
        # Replace with your actual agent loading logic
        # from my_agent import Agent
        # agent = Agent(model_path="model.pth")
        agent = type('Mock', (), {'act': lambda self, x: 0})() 
    except Exception as e:
        sys.exit(1)

    # 2. Get Tasks (ensure this list comes from the correct source)
    tasks = [{"id": "task_1"}, {"id": "task_2"}] 

    # 3. Loop through tasks
    for task in tasks:
        evaluate_task(agent, task)

if __name__ == "__main__":
    run_baseline()
    sys.exit(0)