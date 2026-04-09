def grade_hard(state):
    cache_fixed = state.services['cache'].status == "running"
    api_scaled = state.services['api'].instances >= 3

    if cache_fixed and api_scaled:
        return 0.95
    return 0.5 if (cache_fixed or api_scaled) else 0.05