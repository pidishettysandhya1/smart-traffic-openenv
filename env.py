import random
from fastapi import FastAPI

app = FastAPI()

class TrafficEnv:

    def __init__(self):
        self.roads = ["North", "South", "East", "West"]
        self.current_state = None

    def reset(self, level="easy"):
        traffic = {}

        for road in self.roads:
            if level == "easy":
                traffic[road] = random.randint(5, 20)
            elif level == "medium":
                traffic[road] = random.randint(10, 35)
            else:
                traffic[road] = random.randint(5, 50)

        self.current_state = traffic
        return self.current_state

    def step(self, action):
        selected_road = self.roads[action]
        traffic = self.current_state

        best_road = max(traffic, key=traffic.get)

        reward = 1 if selected_road == best_road else 0
        done = True

        return self.current_state, reward, done

    def state(self):
        return self.current_state


# -------- API PART (for Phase 1 runtime) --------

env = TrafficEnv()

@app.post("/reset")
def reset(level: str = "easy"):
    return {"state": env.reset(level)}

@app.post("/step")
def step():
    best_action = max(env.current_state, key=env.current_state.get)
    action_index = env.roads.index(best_action)
    state, reward, done = env.step(action_index)
    return {"reward": reward}

@app.get("/state")
def state():
    return {"state": env.state()}
