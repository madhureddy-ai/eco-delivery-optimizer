from tasks import TASKS


class Env:
    def __init__(self):
        self.grid_size = 5
        self.reset()

    def reset(self, task="easy"):
        config = TASKS.get(task, TASKS["easy"])

        self.pos = [0, 0]
        self.fuel = config["fuel"]
        self.deliveries = [tuple(d) for d in config["deliveries"]]
        self.steps = 0

        return self.state()

    def state(self):
        return {
            "position": self.pos,
            "fuel": self.fuel,
            "deliveries_left": self.deliveries
        }

    def step(self, action):
        move = action.get("move", "up")

        old_pos = self.pos.copy()

        if move == "up":
            self.pos[0] -= 1
        elif move == "down":
            self.pos[0] += 1
        elif move == "left":
            self.pos[1] -= 1
        elif move == "right":
            self.pos[1] += 1

        if not (0 <= self.pos[0] < self.grid_size and 0 <= self.pos[1] < self.grid_size):
            self.pos = old_pos
            reward = -0.5
        else:
            reward = -0.1

        self.fuel -= 1
        self.steps += 1

        if tuple(self.pos) in self.deliveries:
            self.deliveries.remove(tuple(self.pos))
            reward += 1.0

        done = (self.fuel <= 0) or (len(self.deliveries) == 0)

        if self.fuel < 0:
            self.fuel = 0

        return {
            "state": self.state(),
            "reward": reward,
            "done": done
        }