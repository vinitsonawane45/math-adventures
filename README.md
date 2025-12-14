# AI-Driven Math Performance Evaluation Pipeline

## 1. Local Setup Instructions
To run this evaluation pipeline locally:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/vinitsonawane45/math-adventures
    cd math-adventures
    ```
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the application:**
    ```bash
    streamlit run main.py
    ```
4.  **Access the Interface:**
    Open your browser to `http://localhost:8501`.

---

## 2. Architecture of the Evaluation Pipeline

The solution implements a modular **Real-Time Human-in-the-Loop Evaluation Architecture**. It consists of three distinct layers:

* **Interaction Layer (`main.py`):** Handles real-time user input and visual feedback. It captures the raw "conversation" (Math Problem ↔ User Answer).
* **Decision Layer (`adaptive_engine.py`):** An algorithmic engine that evaluates user performance against historical windows. It acts as the "Judge," dynamically adjusting the difficulty based on accuracy and latency metrics.
* **Analytics Layer (`performance_tracker.py`):** A data pipeline that logs every interaction (timestamp, latency, correctness) and computes rolling averages and mastery heatmaps for post-session analysis.

---

## 3. Design Decisions (Why this way?)

I chose a **State-Based Modular Architecture** over a monolithic script or a pure LLM approach for several reasons:

1.  **Deterministic Evaluation:** Unlike LLM-based judges which can hallucinate grades, the `PerformanceTracker` uses rigid logic for mathematical verification. This ensures 100% evaluation accuracy.
2.  **Latency Optimization:** By decoupling the *Generator* (`puzzle_generator.py`) from the *Evaluator* (`adaptive_engine.py`), the system can generate the next token/problem in sub-millisecond time.
3.  **Adaptive Feedback Loops:** The architecture is designed specifically for "Assessment for Learning." It doesn't just score; it adapts. This required a stateful engine that persists across the session.

---

## 4. Scaling, Latency, and Cost Optimization

If this script were run at a scale of **millions of daily conversations**, the following strategies ensure viability:

### A. Cost Minimization
* **Algorithmic Generation vs. LLM:** This solution uses procedural generation (`puzzle_generator.py`) rather than querying an LLM API (like GPT-4) for every math problem.
    * *LLM Cost:* ~$10/million tokens.
    * *Our Cost:* **$0.**
    * *Result:* The pipeline remains cost-effective even at massive scale because it relies on CPU logic rather than GPU inference.

### B. Latency Management
* **O(1) Evaluation:** The grading logic in `performance_tracker.py` is constant time. It does not require network calls or vector database lookups.
* **Stateless Scaling Plan:** Currently, the app uses in-memory `session_state`. To scale to millions, we would replace the in-memory tracker with a **Redis Cache**.
    * *Write Path:* User answers are pushed to a Redis Queue (async) so the UI never blocks.
    * *Read Path:* The `AdaptiveEngine` reads difficulty state from Redis (sub-millisecond access).