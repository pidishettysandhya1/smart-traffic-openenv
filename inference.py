from env import TrafficEnv

env = TrafficEnv()

roads = ["North", "South", "East", "West"]

for level in ["easy", "medium", "hard"]:
    print("\n===== LEVEL:", level, "=====")

    state = env.reset(level)

    # Choose best road (your smart logic)
    values = list(state.values())
    action = values.index(max(values))

    next_state, reward, done = env.step(action)

    print("Traffic State:", state)
    print("Selected Road:", roads[action])
    print("Reward:", reward)