from fastapi import FastAPI, Body
from env.devops_env import DevOpsEnv
from tasks.easy_incident import TASK_EASY
from tasks.medium_incident import TASK_MEDIUM
from tasks.hard_incident import TASK_HARD

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows the hackathon portal to connect
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global environment instance
# The validator starts by calling /reset
env = None

@app.post("/reset")
async def reset(task_id: str = Body(default="easy", embed=True)):
    global env
    task_map = {"easy": TASK_EASY, "medium": TASK_MEDIUM, "hard": TASK_HARD}
    config = task_map.get(task_id.lower(), TASK_EASY)
    
    env = DevOpsEnv(config)
    obs = env.reset()
    # Return observation as dict for the validator
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