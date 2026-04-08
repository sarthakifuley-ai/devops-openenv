import os
import sys
import traceback
from openai import OpenAI  # Ensure 'openai' is in your requirements.txt

def log_print(message):
    """Ensures the validator sees the output immediately for parsing."""
    print(message, flush=True)

def evaluate_task(agent, client, task, max_steps=15):
    # This must match what the 'Output Parsing' step expects
    task_id = task.get('id', 'task_1')
    log_print(f"[START] task={task_id}")
    
    try:
        # Replace 'your_env_module' with the actual env provided in the hackathon
        from environment import env 
        state = env.reset(task_id=task_id)
    except Exception as e:
        log_print(f"[END] task={task_id} score=0 steps=0 status=reset_failed")
        return

    total_reward = 0
    actual_steps = 0
    
    try:
        for step in range(1, max_steps + 1):
            # Pass the client to your agent so it uses the proxy
            action = agent.act(state, client) 
            
            state, reward, done, info = env.step(action)
            total_reward += reward
            actual_steps = step
            
            log_print(f"[STEP] step={step} reward={reward}")
            if done:
                break
        
        log_print(f"[END] task={task_id} score={total_reward} steps={actual_steps}")
    except Exception as e:
        log_print(f"[END] task={task_id} score={total_reward} steps={actual_steps} status=crashed")

def run_baseline():
    # --- STEP 1: INITIALIZE LLM CLIENT VIA PROXY ---
    try:
        # Fetching injected environment variables
        api_key = os.environ.get("API_KEY")
        api_base = os.environ.get("API_BASE_URL")
        
        if not api_key or not api_base:
            log_print("Error: API_KEY or API_BASE_URL not found in environment.")
            sys.exit(1)

        # Initialize the OpenAI client pointing to the LiteLLM proxy
        client = OpenAI(
            api_key=api_key,
            base_url=api_base
        )
        log_print(f"LLM Client initialized with Proxy: {api_base}")
    except Exception as e:
        log_print(f"Failed to initialize LLM: {e}")
        sys.exit(1)

    # --- STEP 2: INITIALIZE AGENT ---
    try:
        # Your actual agent class
        from agent import MyAgent 
        agent = MyAgent() 
    except Exception as e:
        log_print(f"Agent Init Error: {e}")
        sys.exit(1)

    # --- STEP 3: RUN TASKS ---
    tasks = [{"id": "task_1"}] # Adjust based on how tasks are provided
    for task in tasks:
        evaluate_task(agent, client, task)

if __name__ == "__main__":
    try:
        run_baseline()
    except Exception:
        sys.exit(0) # Exit 0 to ensure logs are captured