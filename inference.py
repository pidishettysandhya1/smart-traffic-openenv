import os
from openai import OpenAI
from env import TrafficEnv

client = OpenAI(
    base_url=os.environ["API_BASE_URL"],
    api_key=os.environ["API_KEY"]
)

env = TrafficEnv()
tasks = ["easy", "medium", "hard"]

for task in tasks:
    print(f"[START] task={task}", flush=True)

    state = env.reset(task)

    try:
        prompt = f"""
        Analyze this smart traffic scenario:

        Traffic: {state['traffic']}
        Weather: {state['weather']}
        Emergency Vehicle Route: {state['emergency']}
        Accident Blocked Road: {state['accident']}

        Choose the best road from North, South, East, West.
        """

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role":"user","content":prompt}]
        )

        action = response.choices[0].message.content.strip()

        if action not in env.roads:
            action = max(state["traffic"], key=state["traffic"].get)

    except:
        if state["emergency"]:
            action = state["emergency"]
        else:
            action = max(state["traffic"], key=state["traffic"].get)

    action_index = env.roads.index(action)

    _, reward, _ = env.step(action_index)

    score = 0.8 if reward == 1 else 0.3

    print(f"[STEP] step=1 reward={reward}", flush=True)
    print(f"[END] task={task} score={score} steps=1", flush=True)
