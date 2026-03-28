class Grader:
    def __init__(self):
        self.score = 0

    def reset(self):
        self.score = 0

    def update(self, result):
        self.score += result["reward"]

    def get_score(self):
        return round(self.score, 2)