from env import TrafficEnv

env = TrafficEnv()

tasks = ["easy", "medium", "hard"]

for task in tasks:
    print(f"[START] task={task}", flush=True)

    state = env.reset(task)

    # choose best action
    best_action = max(state, key=state.get)
    action_index = env.roads.index(best_action)

    next_state, reward, done = env.step(action_index)

    print(f"[STEP] step=1 reward={reward}", flush=True)

    print(f"[END] task={task} score={reward} steps=1", flush=True)
