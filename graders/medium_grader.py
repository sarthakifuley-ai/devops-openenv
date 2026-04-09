def grade_medium(state):
    if state.services['database'].status == "running" and state.services['api'].error_rate < 0.1:
        return 0.95
    return 0.2 if state.services['database'].status == "running" else 0.05