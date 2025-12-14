# tracker.py
from datetime import datetime

class PerformanceTracker:
    def __init__(self):
        self.history = []  # list of dicts: {'question', 'user_answer', 'correct', 'time_taken', 'difficulty', 'timestamp'}

    def log_attempt(self, question, user_answer, correct_answer, time_taken, difficulty):
        correct = str(user_answer).strip() == str(correct_answer)
        self.history.append({
            'question': question,
            'user_answer': user_answer,
            'correct_answer': correct_answer,
            'correct': correct,
            'time_taken': time_taken,
            'difficulty': difficulty,
            'timestamp': datetime.now()
        })
        return correct

    def get_accuracy_last_n(self, n=5):
        recent = self.history[-n:]
        if not recent:
            return 0.5
        return sum(1 for r in recent if r['correct']) / len(recent)

    def get_streak(self):
        streak = 0
        for entry in reversed(self.history):
            if entry['correct']:
                streak += 1
            else:
                break
        return streak

    def get_summary(self):
        if not self.history:
            return "No attempts yet."
        
        total = len(self.history)
        correct = sum(1 for h in self.history if h['correct'])
        accuracy = correct / total
        avg_time = sum(h['time_taken'] for h in self.history) / total
        
        return {
            'total_problems': total,
            'correct': correct,
            'accuracy': accuracy,
            'avg_time': avg_time,
            'current_streak': self.get_streak(),
            'last_difficulty': self.history[-1]['difficulty'] if self.history else "Easy"
        }