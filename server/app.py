from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from env.devops_env import DevOpsEnv
from tasks.easy_incident import TASK_EASY
from tasks.medium_incident import TASK_MEDIUM
from tasks.hard_incident import TASK_HARD

app = FastAPI()

# Enable CORS for the hackathon portal
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global environment instance
env = None

@app.post("/reset")
async def reset(payload: dict = Body(default=None)):
    global env
    # Handle cases where payload might be None or empty
    task_id = "easy"
    if payload and "task_id" in payload:
        task_id = payload["task_id"]
    
    task_map = {"easy": TASK_EASY, "medium": TASK_MEDIUM, "hard": TASK_HARD}
    config = task_map.get(task_id.lower(), TASK_EASY)
        
    env = DevOpsEnv(config)
    obs = env.reset()
    return obs.dict()

@app.post("/step")
async def step(action: dict = Body(...)):
    global env
    if env is None:
        return {"error": "Environment not initialized. Call /reset first."}
        
    obs, reward, done, info = env.step(action)
    return {
        "observation": obs.dict(),
        "reward": reward,
        "done": done,
        "info": info
    }

@app.get("/state")
async def state():
    if env is None: return {}
    return env.state_data.dict()

def main():
    import uvicorn
    uvicorn.run("server.app:app", host="0.0.0.0", port=8000)