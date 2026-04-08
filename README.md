# 🛠️ AIOps OpenEnv Dashboard
---
title: DevOps OpenEnv
emoji: 🛡️
colorFrom: blue
colorTo: green
sdk: docker
app_port: 8000
---

An AI-native DevOps simulation for incident response, where an agent acts as a Site Reliability Engineer (SRE) handling API, database, cache, and worker incidents.

## ✅ What is implemented
- Real-world AIOps task simulation, not a game or toy.
- Full OpenEnv manifest at `openenv.yaml`.
- Typed observation models using `pydantic` in `env/models.py`.
- `DevOpsEnv` supports `reset()`, `step(action)`, and `state()`.
- Three graded scenarios: easy, medium, hard.
- Meaningful partial reward signals and final grader scores.
- Baseline inference script with reproducible scoring in `inference.py`.
- Dockerized Streamlit deployment via `Dockerfile`.

## 📦 Environment overview
- `env/devops_env.py`: simulation engine
- `env/actions.py`: mapping actions to state changes
- `env/reward.py`: reward shaping with partial progress
- `tasks/*.py`: scenario definitions
- `graders/*.py`: per-task grader logic
- `dashboard.py`: Streamlit UI
- `inference.py`: reproducible baseline evaluation
- `openenv.yaml`: OpenEnv environment manifest

## 🧠 Action space
- `action_type`: `restart_service`, `scale_service`, `update_config`, `none`
- `target`: `api`, `database`, `cache`, `worker`, `none`
- `value`: integer or string payload for scaling/config updates

## 👁️ Observation space
- `services`: per-service status, instances, cpu_usage, memory_usage, error_rate
- `logs`: system log messages
- `latency`: current request latency
- `traffic`: request rate in rps

## 🎯 Tasks and grading
- Easy: Recover a crashed API service (`graders.easy_grader.grade`).
- Medium: Repair database auth failure and reduce API errors (`graders.medium_grader.grade_medium`).
- Hard: Recover cache and scale API during a traffic flood (`graders.hard_grader.grade_hard`).

Each grader returns a score between `0.0` and `1.0`.

## 🧮 Reward function
- Reward is calculated from running service count, service error rates, and latency.
- Values are clamped to `[0.0, 1.0]` to provide stable feedback.
- Partial progress is visible through intermediate rewards.

## ▶️ Run the baseline inference
```bash
pip install -r requirements.txt
python inference.py
```

This prints per-task step counts, average reward, and final grader scores.

## 🛠️ Run the dashboard locally
```bash
pip install -r requirements.txt
streamlit run dashboard.py
```

## 🐳 Docker deployment
Build and run:
```bash
docker build -t devops-openenv .
docker run -p 8501:8501 devops-openenv
```

## ☁️ Hugging Face Spaces
The app is deployable on Hugging Face Spaces using this repository and `Dockerfile`.

## 📄 Manifest
`openenv.yaml` documents the environment, action/observation spaces, scenario definitions, and metrics.

## 🔧 Notes
- `requirements.txt` includes `streamlit`, `pydantic`, and `pyyaml`.
- The code is designed for a reproducible baseline and can be extended with LLM-driven policy logic.
