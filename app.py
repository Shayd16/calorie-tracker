import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(
    page_title="FitPulse Pro | Modern Health Dashboard", 
    page_icon="⚡", 
    layout="wide"
)

# 2. Modern Glassmorphism & Custom CSS
st.markdown("""
    <style>
    .stApp {
        background-color: #0B0E14;
    }
    div[data-testid="stVerticalBlock"] > div[data-testid="stBlock"] {
        border-radius: 12px;
    }
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 16px;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px;
        border-radius: 8px;
        background-color: rgba(255, 255, 255, 0.03);
    }
    </style>
""", unsafe_allow_html=True)

# 3. Quick Database
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

# 4. Session State Setup
if "calories_burned" not in st.session_state:
    st.session_state.calories_burned = 0
if "calories_eaten" not in st.session_state:
    st.session_state.calories_eaten = 0
if "water_glasses" not in st.session_state:
    st.session_state.water_glasses = 0
if "activity_log" not in st.session_state:
    st.session_state.activity_log = []

# Sidebar Goal Center
with st.sidebar:
    st.title("⚡ Control Center")
    st.caption("Personalized Targets")
    
    calorie_goal = st.number_input("Daily Calorie Target", value=2000, step=100, key="cal_goal")
    water_goal = st.number_input("Water Target (Glasses)", value=8, step=1, key="water_goal")
    
    st.divider()
    
    # Progress Summary Box
    st.markdown("### 📊 Daily Summary")
    net_cals = st.session_state.calories_eaten - st.session_state.calories_burned
    cals_left = calorie_goal - net_cals
    
    st.write(f"• **Net Total:** {net_cals} / {calorie_goal} kcal")
    st.write(f"• **Water Intake:** {st.session_state.water_glasses} / {water_goal} glasses")
    
    st.divider()
    if st.button("🔄 Reset Today's Data", use_container_width=True):
        st.session_state.calories_eaten = 0
        st.session_state.calories_burned = 0
        st.session_state.water_glasses = 0
        st.session_state.activity_log = []
        st.toast("Dashboard reset completely!", icon="🧹")

# Header Section
st.title("⚡ FitPulse Pro")
st.caption("Modern real-time fitness, workout, and hydration telemetry.")

# App Navigation Tabs
tab_dash, tab_log, tab_stats = st.tabs(["📊 Live Command Center", "📝 Quick Entry", "📈 Analytics"])

# ==================== TAB 1: LIVE DASHBOARD ====================
with tab_dash:
    # Top Headline Banner
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Calories Consumed", f"{st.session_state.calories_eaten} kcal", delta="Food Intake")
    with c2:
        st.metric("Calories Burned", f"{st.session_state.calories_burned} kcal", delta="Workouts", delta_color="inverse")
    with c3:
        st.metric("Net Calorie Total", f"{net_cals} kcal", delta=f"{cals_left} remaining" if cals_left >= 0 else f"{abs(cals_left)} over limit")
    with c4:
        st.metric("Hydration Level", f"{st.session_state.water_glasses} Glasses", delta=f"Goal: {water_goal}")

    st.write("---")

    # Interactive Progress Cards
    col_p1, col_p2 = st.columns(2)
    
    with col_p1:
        with st.container(border=True):
            st.markdown("### 🎯 Nutrition Progress")
            cal_ratio = min(st.session_state.calories_eaten / calorie_goal, 1.0) if calorie_goal > 0 else 0
            st.progress(cal_ratio)
            st.caption(f"**{int(cal_ratio * 100)}%** of target reached ({st.session_state.calories_eaten} / {calorie_goal} kcal)")

    with col_p2:
        with st.container(border=True):
            st.markdown("### 💧 Hydration Tracker")
            water_ratio = min(st.session_state.water_glasses / water_goal, 1.0) if water_goal > 0 else 0
            st.progress(water_ratio)
            if st.session_state.water_glasses >= water_goal:
                st.caption("🎉 **Daily hydration goal completed!** Excellent work.")
            else:
                st.caption(f"Logged **{st.session_state.water_glasses}** of {water_goal} glasses ({water_goal - st.session_state.water_glasses} to go).")

    st.write("---")

    # Bottom Dashboard Split: Chart + Activity Timeline
    col_chart, col_timeline = st.columns([2, 1])
    
    with col_chart:
        st.subheader("📈 Energy Balance Visualizer")
        chart_data = pd.DataFrame({
            "Category": ["Food Consumed", "Calories Burned"],
            "Calories": [st.session_state.calories_eaten, st.session_state.calories_burned]
        })
        st.bar_chart(chart_data, x="Category", y="Calories", color="Category")

    with col_timeline:
        st.subheader("📜 Timeline Feed")
        if st.session_state.activity_log:
            for item in reversed(st.session_state.activity_log):
                st.info(item)
        else:
            st.caption("No entries logged yet today. Use the 'Quick Entry' tab to get started!")

# ==================== TAB 2: QUICK ENTRY ====================
with tab_log:
    st.subheader
