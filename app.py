import streamlit as st
import pandas as pd

# 1. Page Configuration (Full-width layout with custom tab title)
st.set_page_config(
    page_title="FitPulse Pro | Fitness & Hydration", 
    page_icon="⚡", 
    layout="wide"
)

# Custom Styling using Streamlit's built-in CSS containers
st.markdown("""
    <style>
    .main {
        padding-top: 1rem;
    }
    stMetric {
        background-color: #1E222A;
        padding: 15px;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# App Title Header
st.title("⚡ FitPulse Pro")
st.caption("Your daily command center for nutrition, activity, and hydration.")

# 2. Food & Drink Quick Database
FOOD_DATABASE = {
    "🍎 Apple (Medium)": 95,
    "🍌 Banana (Medium)": 105,
    "🍗 Chicken Breast (6oz)": 280,
    "🍳 Eggs (2 Large)": 140,
    "🍕 Slice of Pizza": 285,
    "🍔 Cheeseburger": 535,
    "🍚 White Rice (1 Cup)": 200,
    "🥤 Protein Shake": 180,
    "🥪 Turkey Sandwich": 320,
    "🥗 Caesar Salad": 220
}

# 3. Session State Initialization
if "calories_burned" not in st.session_state:
    st.session_state.calories_burned = 0
if "calories_eaten" not in st.session_state:
    st.session_state.calories_eaten = 0
if "water_glasses" not in st.session_state:
    st.session_state.water_glasses = 0
if "food_history" not in st.session_state:
    st.session_state.food_history = []

# Sidebar Goal Controls
st.sidebar.title("⚙️ Personal Goals")
calorie_goal = st.sidebar.number_input("Daily Calorie Target", value=2000, step=100, key="cal_goal")
water_goal = st.sidebar.number_input("Daily Water Target (Glasses)", value=8, step=1, key="water_goal")

st.sidebar.divider()
if st.sidebar.button("🔄 Reset Today's Data", use_container_width=True):
    st.session_state.calories_eaten = 0
    st.session_state.calories_burned = 0
    st.session_state.water_glasses = 0
    st.session_state.food_history = []
    st.toast("Cleared all daily progress!", icon="🧹")

# App Navigation Tabs
tab_dash, tab_log = st.tabs(["📊 Live Dashboard", "📝 Add Food, Drinks & Workouts"])

# ==================== TAB 1: REALISTIC DASHBOARD ====================
with tab_dash:
    net_cals = st.session_state.calories_eaten - st.session_state.calories_burned
    cals_remaining = calorie_goal - net_cals
    
    # Header Status Banner
    if net_cals > calorie_goal:
        st.warning(f"⚠️ You've exceeded your daily target by {abs(cals_remaining)} kcal.")
    elif net_cals == 0:
        st.info("👋 Welcome! Start logging your meals or workouts for today.")
    else:
        st.success(f"🎯 You have **{cals_remaining} kcal remaining** for today.")

    # 4 Metric Cards Across the Screen
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    with col_m1:
        st.metric(label="Food Consumed", value=f"{st.session_state.calories_eaten} kcal", delta="Eaten")
    with col_m2:
        st.metric(label="Active Calories", value=f"{st.session_state.calories_burned} kcal", delta="Burned", delta_color="inverse")
    with col_m3:
        st.metric(label="Net Calories", value=f"{net_cals} kcal")
    with col_m4:
        st.metric(label="Hydration", value=f"{st.session_state.water_glasses} / {water_goal} 💧")

    st.write("---")

    # Progress Indicators
    col_p1, col_p2 = st.columns(2)
    
    with col_p1:
        with st.container(border=True):
            st.markdown("### 🎯 Calorie Goal Meter")
            cal_ratio = min(st.session_state.calories_eaten / calorie_goal, 1.0) if calorie_goal > 0 else 0
            st.progress(cal_ratio)
            st.caption(f"Progress: **{int(cal_ratio * 100)}%** of your {calorie_goal} kcal goal.")

    with col_p2:
        with st.container(border=True):
            st.markdown("### 💧 Hydration Tracker")
            water_ratio = min(st.session_state.water_glasses / water_goal, 1.0) if water_goal > 0 else 0
            st.progress(water_ratio)
            st.caption(f"Progress: **{st.session_state.water_glasses}** of {water_goal} glasses logged.")

    st.write("---")
    
    # Chart and Activity Log
    col_c1, col_c2 = st.columns([2, 1])
    
    with col_c1:
        st.subheader("📈 Daily Energy Balance")
        chart_data = pd.DataFrame({
            "Category": ["Food Consumed", "Workout Burned"],
            "Calories": [st.session_state.calories_eaten, st.session_state.calories_burned]
        })
        st.bar_chart(chart_data, x="Category", y="Calories")

    with col_c2:
        st.subheader("📜 Today's Log History")
        if st.session_state.food_history:
            for item in reversed(st.session_state.food_history):
                st.write(f"• {item}")
        else:
            st.info("No activity logged yet today.")

# ==================== TAB 2: ENTRY FORM ====================
with tab_log:
    st.subheader("📝 Quick Log Entry")
    
    col_food, col_ex, col_water = st.columns(3)
    
    # Food & Drink Logging
    with col_food:
        with st.container(border=True):
            st.markdown("### 🍽️ Log Food or Drink")
            
            entry_type = st.radio("Mode:", ["Type Custom Name", "Quick Select Menu"], key="entry_type")
            
            if entry_type == "Type Custom Name":
                item_name = st.text_input("Item Name:", placeholder="e.g., Protein Bar, Iced Tea...", key="custom_name")
                item_cals = st.number_input("Calories (kcal):", min_value=0, step=25, key="custom_cals")
                
                if st.button("➕ Log Typed Item", use_container_width=True):
                    if item_name.strip() != "":
                        st.session_state.calories_eaten += item_cals
                        st.session_state.food_history.append(f"{item_name} (+{item_cals} kcal)")
                        st.toast(f"Logged {item_name}!", icon="🍔")
                    else:
                        st.warning("Please type an item name first!")
            else:
                selected_food = st.selectbox("Select Item:", list(FOOD_DATABASE.keys()))
                food_cals = FOOD_DATABASE[selected_food]
                st.info(f"**Calories:** {food_cals} kcal")
                
                if st.button("➕ Log Menu Item", use_container_width=True):
                    st.session_state.calories_eaten += food_cals
                    st.session_state.food_history.append(f"{selected_food} (+{food_cals} kcal)")
                    st.toast(f"Logged {selected_food}!", icon="🥗")

    # Exercise Logging
    with col_ex:
        with st.container(border=True):
            st.markdown("### 🔥 Log Workout")
            workout_name = st.text_input("Workout Type:", placeholder="e.g., Basketball, Running...", key="ex_name")
            workout_cals = st.number_input("Calories Burned:", min_value=0, step=25, key="ex_cals")
            
            if st.button("➕ Log Workout", use_container_width=True):
                if workout_cals > 0:
                    st.session_state.calories_burned += workout_cals
                    label = workout_name if workout_name.strip() != "" else "Workout"
                    st.session_state.food_history.append(f"🏃 {label} (-{workout_cals} kcal)")
                    st.toast(f"Logged {label}!", icon="🔥")

    # Water Logging
    with col_water:
        with st.container(border=True):
            st.markdown("### 💧 Hydration Station")
            st.markdown(f"#### **{st.session_state.water_glasses}** / {water_goal} Glasses")
            
            if st.button("🥤 +1 Glass of Water", use_container_width=True):
                st.session_state.water_glasses += 1
                st.toast("Logged 1 glass of water!", icon="💧")
                
            if st.button("➖ Remove 1 Glass", use_container_width=True):
                if st.session_state.water_glasses > 0:
                    st.session_state.water_glasses -= 1
