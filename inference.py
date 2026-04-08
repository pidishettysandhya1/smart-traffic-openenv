import os
from openai import OpenAI
from env import TrafficEnv

# Use hackathon provided API
client = OpenAI(
    base_url=os.environ["API_BASE_URL"],
    api_key=os.environ["API_KEY"]
)

env = TrafficEnv()

tasks = ["easy", "medium", "hard"]

for task in tasks:
    print(f"[START] task={task}", flush=True)

    state = env.reset(task)

    # Convert state to text
    prompt = f"""
    Traffic State:
    {state}

    Choose the best road among North, South, East, West.
    Return only the road name.
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    action = response.choices[0].message.content.strip()

    if action not in env.roads:
        action = "North"  # fallback

    action_index = env.roads.index(action)

    next_state, reward, done = env.step(action_index)

    print(f"[STEP] step=1 reward={reward}", flush=True)
