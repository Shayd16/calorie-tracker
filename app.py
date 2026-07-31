import streamlit as st
import pandas as pd

# 1. Page Config (Adds tab icon and full-width layout)
st.set_page_config(page_title="FitPulse Tracker", page_icon="⚡", layout="wide")

st.title("⚡ FitPulse | Calorie & Exercise Tracker")
st.caption("Track your daily nutrition and workouts with real-time stats.")

# Sidebar Settings
st.sidebar.header("🎯 Daily Goals")
calorie_goal = st.sidebar.number_input("Daily Calorie Target", value=2000, step=100)

menu = st.sidebar.radio("Navigation", ["Dashboard", "Log Activity"])

# Initialize storage in session
if "calories_burned" not in st.session_state:
    st.session_state.calories_burned = 0
if "calories_eaten" not in st.session_state:
    st.session_state.calories_eaten = 0

if menu == "Dashboard":
    st.subheader("📊 Today's Overview")
    
    net_cals = st.session_state.calories_eaten - st.session_state.calories_burned
    progress = min(st.session_state.calories_eaten / calorie_goal, 1.0)
    
    # Visual Cards
    col1, col2, col3 = st.columns(3)
    col1.metric("Consumed", f"{st.session_state.calories_eaten} kcal", delta=f"{calorie_goal - st.session_state.calories_eaten} remaining")
    col2.metric("Burned", f"{st.session_state.calories_burned} kcal", delta="Active")
    col3.metric("Net Total", f"{net_cals} kcal")

    st.write("---")
    
    # Progress Bar
    st.write("**Goal Progress**")
    st.progress(progress)
    
    # Dynamic Chart
    st.subheader("📈 Quick Breakdown")
    chart_data = pd.DataFrame({
        "Category": ["Consumed", "Burned"],
        "Calories": [st.session_state.calories_eaten, st.session_state.calories_burned]
    })
    st.bar_chart(chart_data, x="Category", y="Calories")

elif menu == "Log Activity":
    st.subheader("📝 Quick Entry")
    
    col_food, col_ex = st.columns(2)
    
    with col_food:
        with st.container(border=True):
            st.markdown("### 🍎 Food Entry")
            food_cals = st.number_input("Calories Consumed", min_value=0, step=50, key="food")
            if st.button("➕ Log Food", use_container_width=True):
                st.session_state.calories_eaten += food_cals
                st.toast(f"Added {food_cals} calories!", icon="🥗")

    with col_ex:
        with st.container(border=True):
            st.markdown("### 🔥 Workout Entry")
            workout_cals = st.number_input("Calories Burned", min_value=0, step=50, key="workout")
            if st.button("➕ Log Exercise", use_container_width=True):
                st.session_state.calories_burned += workout_cals
                st.toast(f"Logged {workout_cals} burned calories!", icon="🏃")
