import random
from fastapi import FastAPI

app = FastAPI()

class TrafficEnv:
    def __init__(self):
        self.roads = ["North", "South", "East", "West"]
        self.current_state = None
        self.weather = None
        self.emergency = None
        self.accident = None

    def reset(self, level="easy"):
        traffic = {}

        for road in self.roads:
            if level == "easy":
                traffic[road] = random.randint(5, 20)
            elif level == "medium":
                traffic[road] = random.randint(10, 35)
            else:
                traffic[road] = random.randint(20, 50)

        self.weather = random.choice(["Clear", "Rain", "Fog"])
        self.emergency = random.choice([None, "North", "South", "East", "West"])
        self.accident = random.choice([None, "North", "South", "East", "West"])

        self.current_state = traffic
        return {
            "traffic": traffic,
            "weather": self.weather,
            "emergency": self.emergency,
            "accident": self.accident
        }

    def step(self, action):
        selected_road = self.roads[action]

        if self.emergency:
            best_road = self.emergency
        else:
            valid_roads = {k:v for k,v in self.current_state.items() if k != self.accident}
            best_road = max(valid_roads, key=valid_roads.get)

        reward = 1 if selected_road == best_road else 0

        return self.current_state, reward, True


env_instance = TrafficEnv()


@app.get("/")
def home():
    return {"message": "Smart Traffic OpenEnv Running"}
