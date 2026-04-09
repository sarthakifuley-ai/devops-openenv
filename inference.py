import os
import sys
import json
import urllib.request

def log_print(message):
    print(message, flush=True)

def call_llm_proxy(api_base, api_key, obs_dict):
    base = api_base.rstrip("/")
    candidate_urls = [
        f"{base}/chat/completions",
        f"{base}/v1/chat/completions",
    ]

    prompt = f"""You are an SRE agent fixing a DevOps incident.

Observation: {json.dumps(obs_dict, indent=2)}

Reply with ONLY a JSON object, no explanation:
{{"action_type": "restart_service", "target": "api", "value": 1}}

action_type: restart_service | scale_service | update_config | none
target: api | database | cache | worker | none
value: integer"""

    payload = json.dumps({
        "model": "gpt-4o",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 50
    }).encode("utf-8")

    for url in candidate_urls:
        try:
            req = urllib.request.Request(
                url, data=payload,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                body = json.loads(resp.read().decode("utf-8"))
                content = body["choices"][0]["message"]["content"].strip()
                content = content.replace("```json", "").replace("```", "").strip()
                log_print(f"[DEBUG] proxy response: {content}")
                return json.loads(content)
        except Exception as e:
            log_print(f"[DEBUG] {url} failed: {e}")

    return {"action_type": "restart_service", "target": "api", "value": 1}


def run_baseline():
    api_key = os.environ.get("API_KEY", "")
    api_base = os.environ.get("API_BASE_URL", "")

    log_print(f"[DEBUG] API_BASE_URL='{api_base}'")
    log_print(f"[DEBUG] API_KEY present: {'yes' if api_key else 'NO - MISSING'}")

    if not api_base:
        log_print("[START] task=task_1")
        log_print("[END] task=task_1 score=0 steps=0 status=no_api_base")
        return

    try:
        from tasks.easy_incident import TASK_EASY
        from env.devops_env import DevOpsEnv
        env = DevOpsEnv(TASK_EASY)
    except Exception as e:
        log_print(f"[DEBUG] env load error: {e}")
        log_print("[START] task=task_1")
        log_print("[END] task=task_1 score=0 steps=0 status=env_load_error")
        return

    task_id = "task_1"
    log_print(f"[START] task={task_id}")

    try:
        obs = env.reset()
        obs_dict = obs.dict()
        total_reward = 0.0
        step = 0

        for step in range(1, 16):
            action = call_llm_proxy(api_base, api_key, obs_dict)
            log_print(f"[DEBUG] step={step} action={action}")

            obs, reward, done, info = env.step(action)
            obs_dict = obs.dict()
            total_reward += reward
            log_print(f"[STEP] step={step} reward={reward}")

            if done:
                break

        log_print(f"[END] task={task_id} score={total_reward} steps={step}")

    except Exception as e:
        log_print(f"[DEBUG] loop error: {e}")
        log_print(f"[END] task={task_id} score=0 steps=0 status=error")


if __name__ == "__main__":
    try:
        run_baseline()
    except Exception as e:
        log_print(f"[DEBUG] top-level crash: {e}")
    sys.exit(0)