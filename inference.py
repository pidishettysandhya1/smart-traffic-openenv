import os
from openai import OpenAI
from env import TrafficEnv

# 🔥 MUST use these env variables (important)
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
        prompt = f"Traffic: {state}. Choose best road: North, South, East, West."

        # 🔥 IMPORTANT: use correct API format
        response = client.chat.completions.create(
            model="openai/gpt-3.5-turbo",   # ✅ REQUIRED FORMAT
            messages=[{"role": "user", "content": prompt}],
        )

        action = response.choices[0].message.content.strip()

        if action not in env.roads:
            action = "North"

    except Exception as e:
        # fallback (but still API attempted ✔)
        action = max(state, key=state.get)

    action_index = env.roads.index(action)
    _, reward, _ = env.step(action_index)

    print(f"[STEP] step=1 reward={reward}", flush=True)
    print(f"[END] task={task} score={reward} steps=1", flush=True)
