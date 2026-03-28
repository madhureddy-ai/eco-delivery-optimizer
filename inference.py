import os
from environment import Env

env = Env()

tasks = ["easy", "medium", "hard"]

for task in tasks:
    state = env.reset(task)
    done = False
    total_reward = 0

    while not done:
        action = {"move": "right"}  # simple baseline
        result = env.step(action)
        total_reward += result["reward"]
        done = result["done"]

    print(f"{task} score:", total_reward)