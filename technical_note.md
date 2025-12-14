# Technical Note: Math Adventures Adaptive Engine

## 1. Architecture Overview
The system follows a modular architecture separating the User Interface (Streamlit) from the Logic Layer (Adaptive Engine) and Data Layer (Performance Tracker).

**Flow Diagram:**
`User Input` -> `Main UI` -> `Performance Tracker (Log Data)` -> `Adaptive Engine (Calculate State)` -> `Puzzle Generator (New Content)` -> `User Input`

## [cite_start]2. Adaptive Logic Explanation [cite: 86]
I implemented a **Rule-Based Adaptive System** rather than a complex ML model to ensure transparency and immediate feedback for the target audience (children).

**The Algorithm:**
The `AdaptiveEngine` maintains a `correct_streak` and `wrong_streak`.
* **Promotion:** If `correct_streak >= 3` AND `accuracy > 70%`, the difficulty level increments.
* **Demotion:** If `wrong_streak >= 2` OR `accuracy < 40%`, the difficulty level decrements.

[cite_start]**Why this approach?** [cite: 88]
For a prototype targeting ages 5-10, rule-based logic is superior to ML because:
1.  **Cold Start:** It works immediately without requiring a training dataset.
2.  **Predictability:** Teachers/Parents can understand exactly why a child moved up or down a level.

## [cite_start]3. Key Metrics Tracked [cite: 87]
* **Accuracy:** The primary driver for level adjustment.
* **Response Time:** Logged to differentiate between "mastery" (fast & correct) and "struggle" (slow & correct), though currently only accuracy drives the level change.
