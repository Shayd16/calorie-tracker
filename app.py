import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(
    page_title="FitPulse Pro", 
    page_icon="⚡", 
    layout="wide"
)

# App Header
st.title("⚡ FitPulse Pro")
st.caption("Track your custom food, drinks, workouts, and hydration!")

# 2. Pre-made Food Dictionary
FOOD_DATABASE = {
    "🍎 Apple (Medium)": 95,
    "🍌 Banana (Medium)": 105,
    "🍗 Chicken Breast (6oz)": 280,
    "🍳 Eggs (2 Large)": 140,
    "🍕 Slice of Pizza": 285,
    "🍔 Cheeseburger": 535,
    "🍚 White Rice (1 Cup)": 200,
    "🥤 Protein Shake": 180,
}

# 3. Initialize Session State
if "calories_burned" not in st.session_state:
    st.session_state.calories_burned = 0
if "calories_eaten" not in st.session_state:
    st.session_state.calories_eaten = 0
if "water_glasses" not in st.session_state:
    st.session_state.water_glasses = 0
if "food_history" not in st.session_state:
    st.session_state.food_history = []

# Sidebar Goals
st.sidebar.title("⚙️ Goal Control")
calorie_goal = st.sidebar.number_input("Daily Calorie Target", value=2000, step=100, key="cal_goal")
water_goal = st.sidebar.number_input("Daily Water Target (Glasses)", value=8, step=1, key="water_goal")

st.sidebar.divider()
if st.sidebar.button("🔄 Reset Daily Stats", use_container_width=True):
    st.session_state.calories_eaten = 0
    st.session_state.calories_burned = 0
    st.session_state.water_glasses = 0
    st.session_state.food_history = []
    st.toast("Stats reset for the day!", icon="🧹")

# Navigation Tabs
tab_dash, tab_log = st.tabs(["📊 Dashboard", "📝 Log Food, Drinks & Workouts"])

# ==================== TAB 1: DASHBOARD ====================
with tab_dash:
    st.subheader("🔥 Daily Overview")
    
    net_cals = st.session_state.calories_eaten - st.session_state.calories_burned
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Calories Consumed", f"{st.session_state.calories_eaten} kcal")
    m2.metric("Calories Burned", f"{st.session_state.calories_burned} kcal")
    m3.metric("Net Total", f"{net_cals} kcal")
    m4.metric("Hydration", f"{st.session_state.water_glasses} / {water_goal} 💧")

    st.write("---")
    
    # Progress Bars
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        with st.container(border=True):
            st.markdown("### 🎯 Calorie Progress")
            cal_progress = min(st.session_state.calories_eaten / calorie_goal, 1.0)
            st.progress(cal_progress)
            st.write(f"**{int(cal_progress * 100)}%** reached.")

    with col_p2:
        with st.container(border=True):
            st.markdown("### 💧 Hydration Progress")
            water_progress = min(st.session_state.water_glasses / water_goal, 1.0)
            st.progress(water_progress)
            st.write(f"Logged **{st.session_state.water_glasses}** of {water_goal} glasses.")

    st.write("---")
    col_c1, col_c2 = st.columns([2, 1])
    
    with col_c1:
        st.subheader("📈 Daily Breakdown")
        chart_data = pd.DataFrame({
            "Category": ["Consumed", "Burned"],
            "Calories": [st.session_state.calories_eaten, st.session_state.calories_burned]
        })
        st.bar_chart(chart_data, x="Category", y="Calories")

    with col_c2:
        st.subheader("📜 What You Ate & Drank Today")
        if st.session_state.food_history:
            for item in reversed(st.session_state.food_history):
                st.write(f"• {item}")
        else:
            st.info("Nothing logged yet today!")

# ==================== TAB 2: LOG ACTIVITY ====================
with tab_log:
    st.subheader("📝 Quick Log Entry")
    
    col_food, col_ex, col_water = st.columns(3)
    
    # --- FOOD & DRINK LOGGING ---
    with col_food:
        with st.container(border=True):
            st.markdown("### 🍽️ Type What You Ate or Drank")
            
            # Toggle between Quick Menu and Typing Custom Entry
            entry_type = st.radio("Choose Input Method:", ["Type Custom Item", "Select Quick Menu"], key="entry_type")
            
            if entry_type == "Type Custom Item":
                item_name = st.text_input("Name of Food/Drink:", placeholder="e.g. Turkey Sandwich, Gatorade, Smoothie...", key="custom_name")
                item_cals = st.number_input("Calories:", min_value=0, step=25, key="custom_cals")
                
                if st.button("➕ Log Typed Item", use_container_width=True):
                    if item_name.strip() != "":
                        st.session_state.calories_eaten += item_cals
                        st.session_state.food_history.append(f"{item_name} ({item_cals} kcal)")
                        st.toast(f"Added {item_name} ({item_cals} kcal)!", icon="🍔")
                    else:
                        st.warning("Please type a name for the food or drink first!")
            
            else:
                selected_food = st.selectbox("Select Quick Item:", list(FOOD_DATABASE.keys()))
                food_cals =
