import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(
    page_title="FitPulse Pro", 
    page_icon="⚡", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# App Header
st.title("⚡ FitPulse Pro")
st.caption("Your personal interactive fitness & hydration command center.")

# 2. Food Database
FOOD_DATABASE = {
    "🍎 Apple (Medium)": 95,
    "🍌 Banana (Medium)": 105,
    "🍗 Chicken Breast (6oz)": 280,
    "🍳 Eggs (2 Large)": 140,
    "🍕 Slice of Pizza": 285,
    "🍔 Cheeseburger": 535,
    "🍚 White Rice (1 Cup cooked)": 200,
    "🥣 Oatmeal (1 Cup cooked)": 150,
    "🥤 Protein Shake": 180,
    "🍦 Greek Yogurt (1 Cup)": 130,
    "✏️ Custom Amount (Manual)": 0
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

# Sidebar Goal Controls
st.sidebar.title("⚙️ Goal Control")
calorie_goal = st.sidebar.number_input("Daily Calorie Target", value=2000, step=100, key="cal_goal")
water_goal = st.sidebar.number_input("Daily Water Target (Glasses)", value=8, step=1, key="water_goal")

st.sidebar.divider()
if st.sidebar.button("🔄 Reset All Daily Stats", use_container_width=True):
    st.session_state.calories_eaten = 0
    st.session_state.calories_burned = 0
    st.session_state.water_glasses = 0
    st.session_state.food_history = []
    st.toast("All stats have been reset!", icon="🧹")

# Top Navigation Tabs
tab_dash, tab_log = st.tabs(["📊 Dashboard", "📝 Quick Log"])

# ==================== TAB 1: DASHBOARD ====================
with tab_dash:
    st.subheader("🔥 Daily Overview")
    
    net_cals = st.session_state.calories_eaten - st.session_state.calories_burned
    
    # Hero Metric Cards
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric(label="Calories Eaten", value=f"{st.session_state.calories_eaten} kcal", delta="Food")
    with m2:
        st.metric(label="Calories Burned", value=f"{st.session_state.calories_burned} kcal", delta="Workout")
    with m3:
        st.metric(label="Net Total", value=f"{net_cals} kcal")
    with m4:
        st.metric(label="Hydration", value=f"{st.session_state.water_glasses} / {water_goal} 💧")

    st.write("---")
    
    # Progress Section inside stylish containers
    col_p1, col_p2 = st.columns(2)
    
    with col_p1:
        with st.container(border=True):
            st.markdown("### 🎯 Calorie Goal Progress")
            cal_progress = min(st.session_state.calories_eaten / calorie_goal, 1.0)
            st.progress(cal_progress)
            st.write(f"**{int(cal_progress * 100)}%** of your daily goal reached.")

    with col_p2:
        with st.container(border=True):
            st.markdown("### 💧 Water Goal Progress")
            water_progress = min(st.session_state.water_glasses / water_goal, 1.0)
            st.progress(water_progress)
            if st.session_state.water_glasses >= water_goal:
                st.success("🎉 Hydration goal achieved for today!")
            else:
                st.write(f"Drink **{max(0, water_goal - st.session_state.water_glasses)} more glasses** to hit your goal.")

    # Breakdown Chart & Logged History
    st.write("---")
    col_c1, col_c2 = st.columns([2, 1])
    
    with col_c1:
        st.subheader("📈 Calorie Comparison")
        chart_data = pd.DataFrame({
            "Activity": ["Consumed", "Burned"],
            "Calories": [st.session_state.calories_eaten, st.session_state.calories_burned]
        })
        st.bar_chart(chart_data, x="Activity", y="Calories")

    with col_c2:
        st.subheader("📜 Today's Food Log")
        if st.session_state.food_history:
            for item in reversed(st.session_state.food_history):
                st.write(f"• {item}")
        else:
            st.info("No meals logged yet today!")

# ==================== TAB 2: LOG ACTIVITY ====================
with tab_log:
    st.subheader("🚀 Log Your Activity")
    
    col_food, col_ex, col_water = st.columns(3)
    
    # Food Column
    with col_food:
        with st.container(border=True):
            st.markdown("### 🍎 Log Food")
            selected_food = st.selectbox("Select Item:", list(FOOD_DATABASE.keys()))
            
            if "Manual" in selected_food:
                food_cals = st.number_input("Enter Calories:", min_value=0, step=50, key="custom_food")
            else:
                food_cals = FOOD_DATABASE[selected_food]
                st.info(f"**Calorie Count:** {food_cals} kcal")
            
            if st.button("➕ Log Food Entry", use_container_width=True):
                st.session_state.calories_eaten += food_cals
                st.session_state.food_history.append(f"{selected_food} ({food_cals} kcal)")
                st.toast(f"Logged {selected_food}!", icon="🥗")

    # Workout Column
    with col_ex:
        with st.container(border=True):
            st.markdown("### 🔥 Log Exercise")
            workout_cals = st.number_input("Calories Burned", min_value=0, step=50, key="workout_input")
            if st.button("➕ Log Workout", use_container_width=True):
                st.session_state.calories_burned += workout_cals
                st.toast(f"Logged workout (-{workout_cals} kcal)!", icon="🏃")

    # Water Column
    with col_water:
        with st.container(border=True):
            st.markdown("### 💧 Hydration Station")
            st.markdown(f"#### **{st.session_state.water_glasses}** / {water_goal} Glasses")
            if st.button("🥤 +1 Glass of Water", use_container_width=True):
                st.session_state.water_glasses += 1
                st.toast("Added 1 glass of water!", icon="💧")
            if st.button("➖ Remove 1 Glass", use_container_width=True):
                if st.session_state.water_glasses > 0:
                    st.session_state.water_glasses -= 1
