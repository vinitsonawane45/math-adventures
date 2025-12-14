# adaptive_engine.py
class AdaptiveEngine:
    def __init__(self):
        self.level = 1  # Start at Easy
        self.correct_streak = 0
        self.wrong_streak = 0

    def update(self, was_correct: bool, accuracy: float):
        if was_correct:
            self.correct_streak += 1
            self.wrong_streak = 0
        else:
            self.correct_streak = 0
            self.wrong_streak += 1

        # Adaptive Rules
        if self.correct_streak >= 3 and accuracy >= 0.7 and self.level < 4:
            self.level += 1
            self.correct_streak = 0 
        elif self.wrong_streak >= 2 or accuracy <= 0.4:
            if self.level > 0:
                self.level -= 1
            self.wrong_streak = 0

    def get_level(self):
        return self.level