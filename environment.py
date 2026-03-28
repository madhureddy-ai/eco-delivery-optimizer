class Env:
    def __init__(self):
        self.grid_size = 5

    def reset(self, task="easy"):
        from tasks import TASKS
        self.agent_pos = [0, 0]
        self.deliveries = TASKS[task]["deliveries"]
        self.fuel = TASKS[task]["fuel"]
        self.done = False

        return self._get_state()

    def step(self, action):
        if self.done:
            return {"state": self._get_state(), "reward": 0, "done": True}

        move = action["move"]

        if move == "up":
            self.agent_pos[0] = max(0, self.agent_pos[0] - 1)
        elif move == "down":
            self.agent_pos[0] = min(self.grid_size - 1, self.agent_pos[0] + 1)
        elif move == "left":
            self.agent_pos[1] = max(0, self.agent_pos[1] - 1)
        elif move == "right":
            self.agent_pos[1] = min(self.grid_size - 1, self.agent_pos[1] + 1)

        self.fuel -= 1

        reward = -0.1

        # Check delivery
        if tuple(self.agent_pos) in self.deliveries:
            self.deliveries.remove(tuple(self.agent_pos))
            reward += 1

        if self.fuel <= 0 or len(self.deliveries) == 0:
            self.done = True

        return {"state": self._get_state(), "reward": reward, "done": self.done}

    def _get_state(self):
        return {
            "position": self.agent_pos,
            "fuel": self.fuel,
            "deliveries_left": self.deliveries
        }