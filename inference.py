import os
import sys
import traceback
import logging

# Set up logging to help you debug via the 'Participant Log'
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def evaluate_task(agent, task, max_steps=15):
    """
    Evaluates a single task with aggressive error handling.
    """
    from your_env_module import env  # Ensure this matches the competition API
    
    task_id = task.get('id', 'unknown')
    logger.info(f"Starting Task: {task_id}")
    
    try:
        # The crash happened here: we wrap it in a localized try-except
        state = env.reset(task_id=task_id)
    except Exception as e:
        logger.error(f"Failed to reset environment for task {task_id}: {e}")
        return {"task_id": task_id, "score": 0, "status": "reset_failed"}

    total_reward = 0
    try:
        for step in range(max_steps):
            # 1. Get action from agent
            action = agent.act(state)
            
            # 2. Step the environment
            state, reward, done, info = env.step(action)
            total_reward += reward
            
            if done:
                logger.info(f"Task {task_id} completed in {step+1} steps.")
                break
        else:
            logger.warning(f"Task {task_id} reached max steps ({max_steps}).")
            
        return {"task_id": task_id, "score": total_reward, "status": "success"}

    except Exception as e:
        logger.error(f"Error during execution of task {task_id}: {e}")
        traceback.print_exc()
        return {"task_id": task_id, "score": total_reward, "status": "crashed"}

def run_baseline():
    """
    Main entry point for Phase 2.
    """
    # 1. Initialize your model/agent ONCE (outside the loop)
    try:
        # from my_agent import Agent
        # agent = Agent(model_path="weights/best_model.pth")
        agent = type('MockAgent', (), {'act': lambda self, x: 0})() # Placeholder
        logger.info("Agent initialized successfully.")
    except Exception as e:
        logger.critical(f"Failed to initialize Agent: {e}")
        sys.exit(1) # Critical failure: Agent won't load

    # 2. Load tasks (usually provided by the competition framework)
    # This might be env.get_tasks() or a fixed list
    tasks = [{"id": "task_001"}, {"id": "task_002"}] 

    results = []
    for task in tasks:
        result = evaluate_task(agent, task)
        results.append(result)

    # 3. Final summary
    success_count = sum(1 for r in results if r['status'] == 'success')
    logger.info(f"Phase 2 complete. Success: {success_count}/{len(tasks)}")

if __name__ == "__main__":
    try:
        run_baseline()
    except Exception as e:
        logger.error(f"Top-level unhandled exception: {e}")
        # We exit with 0 even on some errors to ensure the platform 
        # registers the logs instead of just a "Process Failed" error.
        sys.exit(0)