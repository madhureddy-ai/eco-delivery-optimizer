from environment import Env

env = Env()

tasks = ["easy", "medium", "hard"]

def get_action(state):
    agent_x, agent_y = state["position"]

    # take first delivery target
    if len(state["deliveries_left"]) == 0:
        return {"move": "up"}  # no task, just move

    target_x, target_y = state["deliveries_left"][0]

    # move toward target (basic logic)
    if agent_x < target_x:
        return {"move": "down"}
    elif agent_x > target_x:
        return {"move": "up"}
    elif agent_y < target_y:
        return {"move": "right"}
    elif agent_y > target_y:
        return {"move": "left"}
    else:
        return {"move": "up"}  # already at target


for task in tasks:
    state = env.reset(task)
    done = False
    total_reward = 0

    while not done:
        action = get_action(state)

        result = env.step(action)

        state = result["state"]
        total_reward += result["reward"]
        done = result["done"]

    print(f"{task} score:", total_reward)