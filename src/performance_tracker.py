# performance_tracker.py
from datetime import datetime
from collections import defaultdict, deque
import numpy as np

class PerformanceTracker:
    def __init__(self, recent_window=10):
        self.history = []  # full log of all attempts
        self.recent = deque(maxlen=recent_window)

    def log(self, question, user_answer, correct_answer, time_taken, level, operation, confidence=None):
        correct = str(user_answer).strip() == str(correct_answer)

        self.history.append({
            'question': question,
            'user_answer': user_answer,
            'correct_answer': correct_answer,
            'correct': correct,
            'time_taken': time_taken,
            'level': level,
            'operation': operation,
            'confidence': confidence if confidence is not None else 1.0,
            'timestamp': datetime.now()
        })

        self.recent.append(1 if correct else 0)
        return correct

    def get_accuracy(self):
        """Weighted overall accuracy."""
        if not self.history:
            return 0.5
        weighted_correct = sum(h['correct'] * h['confidence'] for h in self.history)
        total_confidence = sum(h['confidence'] for h in self.history)
        return weighted_correct / total_confidence if total_confidence else 0.5

    def get_summary(self):
        total = len(self.history)
        correct = sum(h['correct'] for h in self.history)
        avg_time = np.mean([h['time_taken'] for h in self.history]) if self.history else 0
        return {
            'total_questions': total,
            'total_correct': correct,
            'overall_accuracy': correct / total if total else 0,
            'average_time': avg_time
        }

    def get_mastery_heatmap(self):
        """Returns accuracy organized by level and operation"""
        counts = defaultdict(lambda: defaultdict(lambda: {'correct': 0, 'total': 0}))
        for h in self.history:
            lvl = h['level']
            op = h['operation']
            counts[lvl][op]['total'] += 1
            if h['correct']:
                counts[lvl][op]['correct'] += 1

        mastery = {}
        for lvl, ops in counts.items():
            mastery[lvl] = {op: v['correct']/v['total'] if v['total'] else 0 for op, v in ops.items()}
        return mastery