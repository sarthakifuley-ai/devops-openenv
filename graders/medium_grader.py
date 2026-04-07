def grade_medium(state):
    # Success if DB is running and API errors dropped
    if state.services['database'].status == "running" and state.services['api'].error_rate < 0.1:
        return 1.0
    return 0.2 if state.services['database'].status == "running" else 0.0