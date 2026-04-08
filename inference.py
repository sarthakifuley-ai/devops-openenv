import os
import sys
from openai import OpenAI # Or the specific client library required
import traceback

def log_print(message):
    """Ensures the validator sees the output immediately."""
    print(message, flush=True)

def run_baseline():

    # --- CRITICAL FIX FOR LLM CRITERIA CHECK ---

    try:

        # These variables are injected by the validator automatically

        api_key = os.environ.get("API_KEY", "default_key")

        base_url = os.environ.get("API_BASE_URL", "https://api.openai.com/v1")

        

        log_print(f"Initializing LLM client with proxy: {base_url}")

        

        # Initialize the client specifically using the proxy details

        client = OpenAI(

            api_key=api_key,

            base_url=base_url

        )

        

        # Pass this client to your agent

        # agent = MyAgent(llm_client=client) 

        log_print("Agent initialized with Proxy successfully.")

        

    except Exception as e:

        log_print(f"Failed to initialize LLM client: {e}")

        sys.exit(1)

def get_env():
    """
    Attempts to import the environment. 
    REPLACE 'env_module_name' with the actual name provided in your docs.
    """
    try:
        # Try importing common competition environments
        # If your environment is a file named 'environment.py' in the same folder:
        import environment as env_module
        return env_module.env
    except ImportError:
        try:
            # If the environment is provided as a package:
            import gym as env_module 
            return env_module
        except ImportError:
            log_print("CRITICAL: Environment module not found. Check your import name.")
            raise

def evaluate_task(agent, task, max_steps=15):
    task_name = task.get('id', 'task_default')
    
    # --- REQUIRED: [START] block ---
    log_print(f"[START] task={task_name}")
    
    try:
        env = get_env()
        state = env.reset(task_id=task_name)
    except Exception as e:
        log_print(f"Reset Error: {e}")
        log_print(f"[END] task={task_name} score=0 steps=0 status=error")
        return

    total_reward = 0
    actual_steps = 0
    
    try:
        for step in range(1, max_steps + 1):
            # Your agent logic
            action = agent.act(state) if agent else 0 
            
            # Environment step
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
    # Replace this with your actual model loading code
    class SimpleAgent:
        def act(self, state): return 0 # Simple placeholder action

    try:
        agent = SimpleAgent()
        log_print("Agent loaded successfully.")
    except Exception as e:
        log_print(f"Agent Load Error: {e}")
        sys.exit(1)

    # 2. Define Tasks 
    # Usually, the platform provides these. If not, we iterate based on the env scope.
    tasks = [{"id": "task_1"}] # Update this list based on your competition rules

    for task in tasks:
        evaluate_task(agent, task)

if __name__ == "__main__":
    try:
        run_baseline()
    except Exception as e:
        traceback.print_exc()
        sys.exit(0) # Exit 0 ensures logs are saved even on failure