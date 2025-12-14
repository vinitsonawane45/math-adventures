import streamlit as st
import time
import pandas as pd
import altair as alt
from puzzle_generator import generate_puzzle
from performance_tracker import PerformanceTracker
from adaptive_engine import AdaptiveEngine

# --- CONFIGURATION & STYLING ---
st.set_page_config(page_title="Math Adventures Pro", page_icon="🧮", layout="wide")

def local_css():
    st.markdown("""
    <style>
        .stApp {
            background-color: #f0f2f6;
        }
        .main-card {
            background-color: white;
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            text-align: center;
        }
        .stat-box {
            background-color: #ffffff;
            border-left: 5px solid #4CAF50;
            padding: 10px;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        .big-font {
            font-size: 3rem !important;
            font-weight: bold;
            color: #333;
        }
        .level-badge {
            font-size: 1.2rem;
            font-weight: bold;
            padding: 5px 15px;
            border-radius: 20px;
            color: white;
            background: linear-gradient(45deg, #1e3c72, #2a5298);
        }
    </style>
    """, unsafe_allow_html=True)

local_css()

# --- INITIALIZATION ---
if "tracker" not in st.session_state:
    st.session_state.tracker = PerformanceTracker()
if "engine" not in st.session_state:
    st.session_state.engine = AdaptiveEngine()
if "xp" not in st.session_state:
    st.session_state.xp = 0

tracker = st.session_state.tracker
engine = st.session_state.engine
level_names = ["Baby", "Easy", "Medium", "Hard", "Master"]

# --- HELPER FUNCTIONS ---
def calculate_xp(level, time_taken, correct):
    if not correct:
        return 0
    base_points = 10 * (level + 1)
    time_bonus = max(0, (10 - time_taken) * 2) # Bonus for answering under 10s
    return int(base_points + time_bonus)

def get_rank(xp):
    if xp < 100: return "Novice"
    elif xp < 300: return "Apprentice"
    elif xp < 600: return "Calculator"
    elif xp < 1000: return "Math Wizard"
    else: return "Grandmaster"

# --- SIDEBAR DASHBOARD ---
with st.sidebar:
    st.title("🧩 Profile")
    if "name" in st.session_state and st.session_state.name:
        st.write(f"**Player:** {st.session_state.name}")
        rank = get_rank(st.session_state.xp)
        st.metric("Current Rank", rank)
        st.metric("Total XP", st.session_state.xp)
        st.divider()
        st.subheader("Session Stats")
        col_s1, col_s2 = st.columns(2)
        col_s1.metric("Streak", f"🔥 {engine.correct_streak}")
        col_s2.metric("Level", level_names[engine.get_level()])
    else:
        st.info("Please sign in to track stats.")

# --- MAIN APP FLOW ---

# 1. Login Screen
if "name" not in st.session_state:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("<div class='main-card'>", unsafe_allow_html=True)
        st.title("Math Adventures")
        st.caption("AI-Powered Adaptive Learning")
        name_input = st.text_input("Enter your hero name:")
        if st.button("Start Adventure 🚀", type="primary", use_container_width=True):
            if name_input.strip():
                st.session_state.name = name_input.strip()
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

else:
    # 2. Game Area
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown(f"<div class='main-card'>", unsafe_allow_html=True)
        
        # Generate Problem Logic
        if "problem" not in st.session_state:
            current_level = engine.get_level()
            q, ans, op, lvl, name = generate_puzzle(current_level)
            st.session_state.problem = (q, ans, op)
            st.session_state.current_lvl_idx = lvl
            st.session_state.start_time = time.time()
            # Force UI update if needed
        
        question, answer, op = st.session_state.problem
        current_lvl_idx = st.session_state.get('current_lvl_idx', 0)
        
        st.markdown(f"<span class='level-badge'>{level_names[current_lvl_idx]} Mode</span>", unsafe_allow_html=True)
        st.markdown(f"<p class='big-font'>{question} = ?</p>", unsafe_allow_html=True)

        # Input Form (Allows 'Enter' key submission)
        with st.form(key='answer_form', clear_on_submit=True):
            user_ans = st.text_input("Answer here:", autocomplete="off")
            submit_btn = st.form_submit_button("Submit Answer", type="primary", use_container_width=True)

        if submit_btn and user_ans:
            time_taken = time.time() - st.session_state.start_time
            correct = tracker.log(question, user_ans, answer, time_taken, current_lvl_idx, op)
            
            # Logic Update
            old_level = current_lvl_idx
            engine.update(correct, tracker.get_accuracy())
            new_level = engine.get_level()
            
            # Visual Feedback & XP
            if correct:
                earned_xp = calculate_xp(current_lvl_idx, time_taken, True)
                st.session_state.xp += earned_xp
                st.success(f"✅ Correct! (+{earned_xp} XP)")
                if new_level > old_level:
                    st.balloons()
                    st.toast(f"Level Up! Welcome to {level_names[new_level]}!", icon="🎉")
            else:
                st.error(f"❌ Wrong! The answer was {answer}")
                st.toast("Keep trying!", icon="💪")
            
            # Reset for next question
            del st.session_state.problem
            time.sleep(1.0) # Slight pause to see result
            st.rerun()
            
        st.markdown("</div>", unsafe_allow_html=True)

    # 3. Quick Stats Column
    with col2:
        accuracy = tracker.get_accuracy()
        st.markdown("### Accuracy")
        st.progress(accuracy)
        st.caption(f"{accuracy:.0%} Global Accuracy")
        
        if st.button("🛑 End Session", use_container_width=True):
            st.session_state.show_summary = True

# --- ANALYTICS DASHBOARD (After Session) ---
if st.session_state.get("show_summary"):
    st.divider()
    st.header("📊 Mission Report")
    
    # Get Data
    summary = tracker.get_summary()
    history = tracker.history
    
    if not history:
        st.warning("No data to show yet!")
    else:
        # Metrics Row
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Problems", summary['total_questions'])
        m2.metric("Final Accuracy", f"{summary['overall_accuracy']:.1%}")
        m3.metric("Avg Speed", f"{summary['average_time']:.2f}s")
        m4.metric("Total XP", st.session_state.xp)

        # Create DataFrame for Charts
        df = pd.DataFrame(history)
        df['Question Number'] = range(1, len(df) + 1)
        df['Status'] = df['correct'].apply(lambda x: "Correct" if x else "Wrong")

        # Chart 1: Performance Timeline
        c1, c2 = st.columns(2)
        
        with c1:
            st.subheader(" reaction Time Analysis")
            chart_time = alt.Chart(df).mark_circle(size=60).encode(
                x='Question Number',
                y='time_taken',
                color=alt.Color('Status', scale=alt.Scale(domain=['Correct', 'Wrong'], range=['green', 'red'])),
                tooltip=['question', 'time_taken', 'level']
            ).interactive()
            st.altair_chart(chart_time, use_container_width=True)

        with c2:
            st.subheader("Accuracy by Difficulty")
            mastery = tracker.get_mastery_heatmap()
            # Prepare data for simple bar chart
            level_data = []
            for lvl, ops in mastery.items():
                avg_acc = sum(ops.values()) / len(ops) if ops else 0
                level_data.append({"Level": level_names[lvl], "Accuracy": avg_acc})
            
            df_levels = pd.DataFrame(level_data)
            chart_levels = alt.Chart(df_levels).mark_bar().encode(
                x='Level',
                y=alt.Y('Accuracy', scale=alt.Scale(domain=[0, 1])),
                color='Level'
            )
            st.altair_chart(chart_levels, use_container_width=True)
            
    if st.button("Start New Session"):
        st.session_state.clear()
        st.rerun()
