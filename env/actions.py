# env/actions.py

def execute_action(state, action):
    atype = action.get("action_type")
    target = action.get("target")
    value = action.get("value")

    # FIX FOR HARD TASK: Scaling
    if atype == "scale_service" and target == "api":
        state.services[target].instances = int(value)
        # If we scale to 3 or more, the error rate should drop
        if int(value) >= 3:
            state.services[target].error_rate = 0.05
            state.logs.append(f"EXEC: Scaled API to {value} instances. Traffic load balanced.")

    # FIX FOR EASY/HARD TASK: Restarting
    elif atype == "restart_service":
        if target in state.services:
            state.services[target].status = "running"
            state.services[target].error_rate = 0.0
            state.logs.append(f"EXEC: {target} restarted and healthy.")

    # FIX FOR MEDIUM TASK: Config/Auth
    elif atype == "update_config":
        if target == "database":
            state.services[target].status = "running"
            state.services[target].error_rate = 0.0
            state.logs.append("EXEC: Database credentials updated. Connection restored.")

    return state