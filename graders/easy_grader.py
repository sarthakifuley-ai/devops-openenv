def grade(state):
    # Graders return 0.0 to 1.0 for the final evaluation
    if state.services['api'].status == "running" and state.services['api'].error_rate < 0.1:
        return 1.0
    return 0.0