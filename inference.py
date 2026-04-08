import env
from env.devops_env import DevOpsEnv
from graders.easy_grader import grade as grade_easy
from graders.medium_grader import grade_medium
from graders.hard_grader import grade_hard
from tasks.easy_incident import TASK_EASY
from tasks.medium_incident import TASK_MEDIUM
from tasks.hard_incident import TASK_HARD


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
                "reasoning": "SRE: Traffic spike detected. Scaling API to 3 instances to stabilize load."
            }

    if "auth" in log_text or "access denied" in log_text or services.get('database', {}).get('status') == 'crashed':
        return {
            "action_type": "update_config",
            "target": "database",
            "value": "fix_auth_credentials",
            "reasoning": "SRE: Database authentication failure detected. Updating credentials and restoring service."
        }

    for name, svc in services.items():
        if svc.get('status') == 'crashed':
            return {
                "action_type": "restart_service",
                "target": name,
                "reasoning": f"SRE: {name} is crashed. Restarting the service."
            }

    return {
        "action_type": "none",
        "target": "none",
        "reasoning": "SRE: No action required at this time. System is stable."
    }


def ai_agent_decision(state_dict):
    return mock_decision(state_dict)


def evaluate_task(task_name, task_config, grader, max_steps=15):
    env = DevOpsEnv(task_config)
    state = env.reset()
    rewards = []

    for _ in range(max_steps):
        action = mock_decision(state.model_dump())
        # Unpack all 4 values returned by the OpenEnv step function
        state, reward, done, info = env.step(action)
        rewards.append(reward)
        if env.done:
            break

    final_score = grader(state)
    return {
        "task": task_name,
        "steps": env.step_count,
        "average_reward": round(sum(rewards) / len(rewards), 3) if rewards else 0.0,
        "final_reward": reward,
        "grader_score": final_score,
        "final_state": state.model_dump()
    }


def run_baseline():
    task_suite = [
        ("Easy: API Crash", TASK_EASY, grade_easy),
        ("Medium: Database Auth Failure", TASK_MEDIUM, grade_medium),
        ("Hard: Cascading Traffic Flood", TASK_HARD, grade_hard),
    ]

    results = []
    for name, task, grader in task_suite:
        result = evaluate_task(name, task, grader, max_steps=task.get('max_steps', 15))
        results.append(result)

    overall = round(sum(r['grader_score'] for r in results) / len(results), 3)
    print("\nBaseline Evaluation Summary")
    print("---------------------------")
    for result in results:
        print(f"{result['task']}: steps={result['steps']}, avg_reward={result['average_reward']}, grader={result['grader_score']}")
    print(f"Overall average grader score: {overall}\n")
    return results


if __name__ == '__main__':
    run_baseline()
