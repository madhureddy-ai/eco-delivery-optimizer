import requests

BASE_URL = "http://localhost:8000"


def move_towards(current, target):
    if current[0] < target[0]:
        return "down"
    elif current[0] > target[0]:
        return "up"
    elif current[1] < target[1]:
        return "right"
    elif current[1] > target[1]:
        return "left"
    return "up"


def run_task(task):
    print(f"\nRunning task: {task}")

    res = requests.post(f"{BASE_URL}/reset", json={"task": task})
    state = res.json()

    done = False

    while not done:
        pos = state.get("position", [0, 0])
        deliveries = state.get("deliveries_left", [])

        if deliveries:
            target = deliveries[0]
            move = move_towards(pos, target)
        else:
            move = "up"

        res = requests.post(f"{BASE_URL}/step", json={"move": move})
        data = res.json()

        state = data.get("state", {})
        done = data.get("done", True)

    res = requests.get(f"{BASE_URL}/grader")
    score = res.json().get("score", 0)

    print(f"Score for {task}: {score}")
    return score


if __name__ == "__main__":
    tasks = ["easy", "medium", "hard"]
    scores = []

    for t in tasks:
        scores.append(run_task(t))

    print("\nFinal Scores:", scores)