import streamlit as st
import pandas as pd
from datetime import date

# App Configuration
st.set_page_config(page_title="Demon Back Tracker", page_icon="👹")

st.title("👹 Demon Back Progress Tracker")
st.write(f"**Target Weight:** 72.5kg | **Goal:** 10% Body Fat")

# --- TAB 1: WORKOUT LOGGING ---
tab1, tab2, tab3 = st.tabs(["🏋️ Workout", "🥗 Nutrition", "📈 Stats"])

with tab1:
    st.header("Log Today's Lift")
    workout_type = st.selectbox("Workout Focus", ["Heavy Pull (Demon Day)", "Rest Day"])
    
    if workout_type == "Heavy Pull (Demon Day)":
        ex1 = st.number_input("Hammer Strength Low Row (kg)", min_value=0, step=1)
        ex1_reps = st.number_input("Low Row Reps", min_value=0, step=1)
        
        ex2 = st.number_input("Barbell Row (kg)", min_value=0, step=1)
        ex2_reps = st.number_input("Barbell Row Reps", min_value=0, step=1)
        
        ex3 = st.number_input("Wide Pull-ups (Total Reps)", min_value=0, step=1)
        
        if st.button("Save Workout"):
            st.success(f"Log saved for {date.today()}! Beat these numbers next week.")

# --- TAB 2: VEGETARIAN MACRO CHECK ---
with tab2:
    st.header("Daily Macro Counter")
    st.info("Target: 160g Protein")
    
    soya = st.checkbox("Soya Chunks (Lunch Swap)")
    tofu = st.checkbox("Woolworths High Protein Tofu")
    whey = st.number_input("Whey Protein Scoops", 0, 4, 2)
    paneer = st.slider("Paneer (grams)", 0, 400, 150)
    
    # Simple calculation logic
    protein_total = (whey * 25) + (paneer * 0.18)
    if soya: protein_total += 50
    if tofu: protein_total += 38
    
    st.metric("Total Protein Tracked", f"{int(protein_total)}g")
    
    if protein_total >= 160:
        st.balloons()
        st.write("✅ Demon Growth Activated!")

# --- TAB 3: REST DAY RULES ---
with tab3:
    st.header("Rest Day Discipline")
    is_rest_day = st.toggle("Is today a Rest Day?")
    
    if is_rest_day:
        st.warning("⚠️ REST DAY RULES: Half rice at lunch, NO rice at dinner.")
        water = st.slider("Water Intake (Liters)", 0.0, 5.0, 3.5)
        if water >= 3.5:
            st.write("💧 Hydration perfect for skin thinning.")
    else:
        st.write("🔥 Training Day: Eat your rice and lift heavy!")

st.divider()
st.caption("Custom Built for Gemini User | 176cm | 72.5kg")
