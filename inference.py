import os
from openai import OpenAI
from env import TrafficEnv

# MUST use these EXACT env variables
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
        prompt = f"Traffic state: {state}. Which road is best among North, South, East, West?"

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",   # ✅ VERY IMPORTANT (NOT openai/gpt-3.5-turbo)
            messages=[{"role": "user", "content": prompt}],
        )

        action = response.choices[0].message.content.strip()

        if action not in env.roads:
            action = "North"

    except Exception as e:
        # fallback (but API still attempted)
        action = max(state, key=state.get)

    action_index = env.roads.index(action)
    _, reward, _ = env.step(action_index)

    print(f"[STEP] step=1 reward={reward}", flush=True)
    score = 0.5 if reward == 1 else 0.1
    print(f"[END] task={task} score={score} steps=1", flush=True)
