import random

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
