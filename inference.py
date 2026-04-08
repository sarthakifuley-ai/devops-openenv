import os
import sys
import traceback

# 1. FORCED FLUSH PRINT
def log_print(message):
    print(message, flush=True)

def run_baseline():
    # --- STEP 1: IMPORT LIBS MANUALLY TO CATCH ERRORS ---
    try:
        from openai import OpenAI
        # Import your agent and environment files
        # Make sure these files (agent.py, environment.py) are in your ZIP!
        import environment as env_module
        from agent import MyAgent 
    except ImportError as e:
        log_print(f"CRITICAL ERROR: Missing file or library: {e}")
        # If this fails, check your requirements.txt and zip structure
        return

    # --- STEP 2: INITIALIZE LLM WITH PROXY ---
    try:
        client = OpenAI(
            api_key=os.environ.get("API_KEY", "dummy"),
            base_url=os.environ.get("API_BASE_URL")
        )
        agent = MyAgent()
        log_print("Environment, Agent, and LLM Proxy initialized.")
    except Exception as e:
        log_print(f"Initialization failed: {e}")
        return

    # --- STEP 3: THE EVALUATION LOOP ---
    tasks = [{"id": "task_1"}] # Ensure this matches competition task format
    
    for task in tasks:
        task_id = task.get('id')
        log_print(f"[START] task={task_id}")
        
        try:
            state = env_module.env.reset(task_id=task_id)
            
            # Run for max 15 steps
            total_reward = 0
            for step in range(1, 16):
                # Pass the PROXY CLIENT to your agent
                action = agent.act(state, client) 
                
                state, reward, done, info = env_module.env.step(action)
                total_reward += reward
                
                log_print(f"[STEP] step={step} reward={reward}")
                if done: break
            
            log_print(f"[END] task={task_id} score={total_reward} steps={step}")
            
        except Exception as e:
            log_print(f"Task failure: {e}")
            log_print(f"[END] task={task_id} score=0 steps=0 status=failed")

if __name__ == "__main__":
    try:
        run_baseline()
    except Exception:
        traceback.print_exc()
    # Always exit with 0 so the platform can parse the logs
    sys.exit(0)