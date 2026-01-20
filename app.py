import streamlit as st
import pandas as pd
import plotly.express as px
import time
from datetime import datetime

st.set_page_config(page_title="Demon Back Pro", layout="centered")

# --- DATA STORAGE ---
if 'logs' not in st.session_state:
    st.session_state.logs = pd.DataFrame(columns=["Date", "Split", "Exercise", "Weight", "Reps", "1RM"])

# --- SIDEBAR: TOOLS ---
st.sidebar.title("👹 Demon Menu")
current_split = st.sidebar.selectbox("Today's Session", [
    "Rest Day", "Push (Chest/Tri/Shoulder)", "Pull (Back/Bi/Traps/Rear Delt)", 
    "Legs", "Back & Chest (Heavy Volume)", "Arms"
])

# 1-REP MAX CALCULATOR (Brzycki Formula)
st.sidebar.divider()
st.sidebar.subheader("🧮 1-Rep Max Predictor")
calc_w = st.sidebar.number_input("Weight Lifted", value=0.0, step=2.5)
calc_r = st.sidebar.number_input("Reps Performed", value=0, step=1)
if calc_r > 0:
    one_rm = calc_w / (1.0278 - (0.0278 * calc_r))
    st.sidebar.metric("Estimated 1RM", f"{round(one_rm, 1)} kg")

# REST TIMER
st.sidebar.divider()
st.sidebar.subheader("⏲️ Rest Timer")
t_input = st.sidebar.number_input("Seconds", value=60, step=5)
if st.sidebar.button("Start Timer"):
    msg = st.sidebar.empty()
    for i in range(int(t_input), 0, -1):
        msg.metric("Rest Remaining", f"{i}s")
        time.sleep(1)
    st.sidebar.success("GO! Next Set!")
    st.balloons()

# --- MAIN WORKOUT LOG ---
st.header(f"🏋️ {current_split}")

if current_split != "Rest Day":
    with st.form("log_form", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        ex = c1.text_input("Exercise")
        wt = c2.number_input("Weight (kg)", step=1.25)
        rp = c3.number_input("Reps", step=1)
        
        if st.form_submit_button("Log Set"):
            # Calculate 1RM for this set
            current_1rm = wt / (1.0278 - (0.0278 * rp)) if rp > 0 else 0
            new_row = pd.DataFrame([[datetime.now().date(), current_split, ex, wt, rp, round(current_1rm, 1)]], 
                                   columns=["Date", "Split", "Exercise", "Weight", "Reps", "1RM"])
            st.session_state.logs = pd.concat([st.session_state.logs, new_row], ignore_index=True)
            st.success(f"Set saved! Est. 1RM: {round(current_1rm, 1)}kg")

# --- PROGRESS CHART ---
if not st.session_state.logs.empty:
    st.divider()
    st.subheader("📈 Strength History")
    all_ex = st.session_state.logs["Exercise"].unique()
    target_ex = st.selectbox("Select Exercise to Track", all_ex)
    
    chart_data = st.session_state.logs[st.session_state.logs["Exercise"] == target_ex]
    fig = px.line(chart_data, x="Date", y="1RM", markers=True, title=f"{target_ex} (Estimated 1RM Over Time)")
    st.plotly_chart(fig, use_container_width=True)

# --- NUTRITION ---
st.divider()
st.subheader("🥗 Daily Protein (Target: 160g)")
p_items = st.multiselect("Check what you ate:", ["Whey (25g)", "Tofu (38g)", "Soya (50g)", "Paneer (28g)"])
current_p = sum([int(i.split('(')[1].replace('g)', '')) for i in p_items])
st.progress(min(current_p/160, 1.0))
st.write(f"Total: {current_p}g / 160g")

if current_split == "Rest Day":
    st.warning("⚠️ REMINDER: Half rice at lunch, NO rice at dinner.")
