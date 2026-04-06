import random

class TrafficEnv:

    def __init__(self):
        self.roads = ["North", "South", "East", "West"]
        self.current_state = None

    # ---- Reset Environment ----
    def reset(self, level="easy"):
        traffic = {}

        for road in self.roads:
            if level == "easy":
                traffic[road] = random.randint(5, 20)
            elif level == "medium":
                traffic[road] = random.randint(10, 35)
            else:  # hard
                traffic[road] = random.randint(5, 50)

        self.current_state = traffic
        return self.current_state

    # ---- Step Function ----
    def step(self, action):
        """
        action: 0 → North, 1 → South, 2 → East, 3 → West
        """

        selected_road = self.roads[action]
        traffic = self.current_state

        # Emergency logic (from your code)
        emergency_road = random.choice(self.roads + [None])

        if emergency_road:
            best_road = emergency_road
        else:
            # Smart logic (max traffic)
            best_road = max(traffic, key=traffic.get)

        # Reward (0 to 1)
        if selected_road == best_road:
            reward = 1
        else:
            reward = 0

        done = True

        return self.current_state, reward, done

    # ---- Get Current State ----
    def state(self):
        return self.current_state