def grade_hard(state):
    # Must fix cache AND scale API to pass
    cache_fixed = state.services['cache'].status == "running"
    api_scaled = state.services['api'].instances >= 3
    
    if cache_fixed and api_scaled:
        return 1.0
    return 0.5 if (cache_fixed or api_scaled) else 0.0