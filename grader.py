class Grader:

    def __init__(self):
        self.total_reward = 0.0
        self.steps = 0

    def reset(self):
        self.total_reward = 0.0
        self.steps = 0

    def update(self, result):
        reward = float(result.get("reward", 0))
        self.total_reward += reward
        self.steps += 1

    def get_score(self):
        if self.steps == 0:
            return 0.0

        avg_reward = self.total_reward / self.steps
        score = (avg_reward + 1) / 2

        if score < 0:
            score = 0.0
        elif score > 1:
            score = 1.0

        return round(score, 2)