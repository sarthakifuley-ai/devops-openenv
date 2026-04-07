def calculate_reward(state):
    """
    Calculates a dense reward:
    - +0.1 for each running service (Partial Progress)
    - -0.05 for each service with >10% error rate (Efficiency Penalty)
    - +1.0 bonus if all services are running AND healthy (Success Signal)
    """
    reward = 0.0
    services = list(state.services.values())
    total_services = len(services)
    
    # 1. Reward for 'Running' status
    running_count = sum(1 for s in services if s.status.lower() == "running")
    reward += (running_count * 0.1)
    
    # 2. Penalty for errors
    for s in services:
        if s.error_rate > 0.1:
            reward -= 0.05
            
    # 3. Full Resolution Bonus
    all_ok = all(s.status.lower() == "running" and s.error_rate < 0.1 for s in services)
    if all_ok:
        reward += 1.0
        
    return round(reward, 2)