# Math Adventures - Adaptive Learning Prototype

**A minimal, AI-powered math learning application that adapts difficulty in real-time based on user performance.**

---

## 📌 Project Overview
[cite_start]This prototype demonstrates how AI can personalize learning for children (ages 5-10)[cite: 9]. [cite_start]It uses a rule-based adaptive engine to keep learners in their "optimal challenge zone" by dynamically adjusting math puzzles between **Easy**, **Medium**, and **Hard** levels[cite: 7, 31].

### Key Features
* [cite_start]**Dynamic Difficulty:** Automatically promotes or demotes users based on accuracy streaks[cite: 32].
* [cite_start]**Performance Tracking:** Logs response times and correctness for every attempt[cite: 12].
* [cite_start]**Session Summary:** Visual report of accuracy and speed at the end of the session[cite: 14].

---

## 🛠️ Local Setup Instructions

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/vinitsonawane45/math-adventures.git](https://github.com/vinitsonawane45/math-adventures.git)
    cd math-adventures
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the application:**
    *(Note: The source code is located in the `src` directory)*
    ```bash
    streamlit run src/main.py
    ```

4.  **Access the App:**
    Open your browser to `http://localhost:8501`.

---

## 📂 Repository Structure
[cite_start]This project follows a modular architecture as requested[cite: 34, 47]:

```text
math-adventures/
│
├── README.md               # Project documentation
├── requirements.txt        # Dependencies (streamlit, pandas, etc.)
├── technical_note.md       # Architecture & Logic explanation (Deliverable #2)
└── src/
    ├── main.py             # User Interface (Streamlit)
    ├── adaptive_engine.py  # Logic for difficulty adjustments
    ├── puzzle_generator.py # Procedural math problem generator
    └── performance_tracker.py # Data logging system