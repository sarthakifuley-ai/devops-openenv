def grade(state):
    if state.services['api'].status == "running" and state.services['api'].error_rate < 0.1:
        return 0.95
    return 0.05