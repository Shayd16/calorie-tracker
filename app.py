import streamlit as st
import pandas as pd
import numpy as np
import datetime
import json
import os

# ==============================================================================
# 1. PAGE CONFIGURATION & GLOBAL STYLES
# ==============================================================================
st.set_page_config(
    page_title="FitPulse Pro | Complete Health Suite",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Glassmorphism & High-Contrast UI
st.markdown("""
    <style>
    /* Dark Theme Background */
    .stApp {
        background-color: #0A0D12;
        color: #F0F2F5;
    }
    
    /* Custom Card Containers */
    div[data-testid="stVerticalBlock"] > div[data-testid="stBlock"] {
        border-radius: 12px;
    }
    
    /* Metric Cards Styling */
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 18px;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 12px 24px;
        border-radius: 8px;
        background-color: rgba(255, 255, 255, 0.03);
        color: #A0AAB8;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #00E676 !important;
        color: #000000 !important;
    }
    
    /* Custom Section Headers */
    .section-header {
        font-size: 1.4rem;
        font-weight: 700;
        color: #00E676;
        margin-bottom: 12px;
    }
    
    /* Progress Bar Color */
    .stProgress > div > div > div > div {
        background-color: #00E676;
    }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. LOCAL DATA PERSISTENCE ENGINE
# ==============================================================================
DATA_FILE = "fitpulse_user_data.json"

def load_stored_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "profile": {
            "name": "Athlete",
            "age": 20,
            "weight_kg": 70.0,
            "height_cm": 175.0,
            "gender": "Male",
            "activity_level": "Moderately Active",
            "goal_type": "Maintain Weight",
            "custom_cal_goal": 2200,
            "custom_water_goal": 8,
            "protein_goal_g": 140,
            "carbs_goal_g": 250,
            "fat_goal_g": 70
        },
        "streak": 1,
        "last_login": str(datetime.date.today()),
        "xp": 100,
        "level": 1,
        "daily_logs": {}
    }

def save_stored_data():
    data_to_save = {
        "profile": st.session_state.user_profile,
        "streak": st.session_state.streak_count,
        "last_login": str(datetime.date.today()),
        "xp": st.session_state.xp_points,
        "level": st.session_state.user_level,
        "daily_logs": st.session_state.history_logs
    }
    with open(DATA_FILE, "w") as f:
        json.dump(data_to_save, f, indent=4)

# ==============================================================================
# 3. EXPANDED NUTRITION & EXERCISE LIBRARIES
# ==============================================================================
EXTENDED_FOOD_DATABASE = {
    # Proteins & Meats
    "Chicken Breast (Grilled, 6oz)": {"cals": 280, "protein": 52, "carbs": 0, "fat": 6},
    "Salmon Fillet (Baked, 6oz)": {"cals": 340, "protein": 34, "carbs": 0, "fat": 22},
    "Sirloin Steak (6oz)": {"cals": 410, "protein": 46, "carbs": 0, "fat": 24},
    "Ground Turkey 93% (6oz)": {"cals": 290, "protein": 36, "carbs": 0, "fat": 14},
    "Eggs (Large, 2 whole)": {"cals": 140, "protein": 12, "carbs": 1, "fat": 10},
    "Egg Whites (1 Cup)": {"cals": 120, "protein": 26, "carbs": 2, "fat": 0},
    "Tofu (Firm, 1 Cup)": {"cals": 180, "protein": 20, "carbs": 4, "fat": 11},
    "Whey Protein Scoop": {"cals": 120, "protein": 24, "carbs": 3, "fat": 2},
    
    # Carbs & Grains
    "White Rice (Cooked, 1 Cup)": {"cals": 205, "protein": 4, "carbs": 45, "fat": 0},
    "Brown Rice (Cooked, 1 Cup)": {"cals": 215, "protein": 5, "carbs": 45, "fat": 2},
    "Sweet Potato (Medium, Baked)": {"cals": 103, "protein": 2, "carbs": 24, "fat": 0},
    "Oatmeal (Cooked, 1 Cup)": {"cals": 160, "protein": 6, "carbs": 28, "fat": 3},
    "Whole Wheat Bread (2 Slices)": {"cals": 160, "protein": 8, "carbs": 28, "fat": 2},
    "Quinoa (Cooked, 1 Cup)": {"cals": 220, "protein": 8, "carbs": 39, "fat": 4},
    "Pasta (Cooked, 1 Cup)": {"cals": 220, "protein": 8, "carbs": 43, "fat": 1},

    # Fruits & Vegetables
    "Apple (Medium)": {"cals": 95, "protein": 0, "carbs": 25, "fat": 0},
    "Banana (Medium)": {"cals": 105, "protein": 1, "carbs": 27, "fat": 0},
    "Blueberries (1 Cup)": {"cals": 85, "protein": 1, "carbs": 21, "fat": 1},
    "Avocado (Medium Whole)": {"cals": 240, "protein": 3, "carbs": 12, "fat": 22},
    "Broccoli (Steamed, 1 Cup)": {"cals": 55, "protein": 4, "carbs": 11, "fat": 0},
    "Spinach (Raw, 2 Cups)": {"cals": 14, "protein": 2, "carbs": 2, "fat": 0},
    "Mixed Greens Salad": {"cals": 45, "protein": 2, "carbs": 9, "fat": 0},

    # Snacks & Convenience
    "Greek Yogurt (Plain, 1 Cup)": {"cals": 130, "protein": 22, "carbs": 8, "fat": 0},
    "Almonds (1 oz / ~28 nuts)": {"cals": 160, "protein": 6, "carbs": 6, "fat": 14},
    "Peanut Butter (2 tbsp)": {"cals": 190, "protein": 8, "carbs": 7, "fat": 16},
    "Slice of Pepperoni Pizza": {"cals": 290, "protein": 12, "carbs": 32, "fat": 12},
    "Cheeseburger": {"cals": 535, "protein": 30, "carbs": 40, "fat": 28},
    "Protein Bar": {"cals": 210, "protein": 20, "carbs": 22, "fat": 7}
}

WORKOUT_MET_DATABASE = {
    "Running (Moderate, 5 mph)": 8.3,
    "Running (Vigorous, 7.5 mph)": 11.8,
    "Cycling (Moderate)": 6.8,
    "Weightlifting (General)": 3.5,
    "Weightlifting (Intense Bodybuilding)": 6.0,
    "Basketball (Game)": 8.0,
    "Soccer (Match)": 10.0,
    "Swimming (Freestyle Moderate)": 5.8,
    "HIIT / Circuit Training": 8.0,
    "Walking (Brisk, 3.5 mph)": 3.8,
    "Yoga / Stretching": 2.5,
    "Jump Rope": 12.3
}

# ==============================================================================
# 4. SESSION STATE INITIALIZATION
# ==============================================================================
raw_data = load_stored_data()

if "user_profile" not in st.session_state:
    st.session_state.user_profile = raw_data.get("profile", {})
if "streak_count" not in st.session_state:
    st.session_state.streak_count = raw_data.get("streak", 1)
if "xp_points" not in st.session_state:
    st.session_state.xp_points = raw_data.get("xp", 100)
if "user_level" not in st.session_state:
    st.session_state.user_level = raw_data.get("level", 1)
if "history_logs" not in st.session_state:
    st.session_state.history_logs = raw_data.get("daily_logs", {})

today_str = str(datetime.date.today())

if today_str not in st.session_state.history_logs:
    st.session_state.history_logs[today_str] = {
        "calories_eaten": 0,
        "calories_burned": 0,
        "protein_g": 0,
        "carbs_g": 0,
        "fat_g": 0,
        "water_glasses": 0,
        "entries": []
    }

current_day_data = st.session_state.history_logs[today_str]

# ==============================================================================
# 5. HELPER CALCULATIONS (BMR & TDEE)
# ==============================================================================
def calculate_bmr(weight, height, age, gender):
    if gender == "Male":
        return int(10 * weight + 6.25 * height - 5 * age + 5)
    else:
        return int(10 * weight + 6.25 * height - 5 * age - 161)

def calculate_tdee(bmr, activity):
    multipliers = {
        "Sedentary": 1.2,
        "Lightly Active": 1.375,
        "Moderately Active": 1.55,
        "Very Active": 1.725,
        "Extra Active": 1.9
    }
    return int(bmr * multipliers.get(activity, 1.2))

def add_xp(points):
    st.session_state.xp_points += points
    needed_xp = st.session_state.user_level * 200
    if st.session_state.xp_points >= needed_xp:
        st.session_state.user_level += 1
        st.balloons()
        st.toast(f"🎉 LEVEL UP! You are now Level {st.session_state.user_level}!", icon="🏆")
    save_stored_data()

# ==============================================================================
# 6. SIDEBAR - PROFILE & CONTROL PANEL
# ==============================================================================
with st.sidebar:
    st.title("⚡ Control Center")
    st.caption(f"Logged in as: **{st.session_state.user_profile.get('name', 'User')}**")
    
    # XP Level Progress Card
    st.markdown("### 🏆 User Rank")
    cur_lvl = st.session_state.user_level
    cur_xp = st.session_state.xp_points
    next_xp = cur_lvl * 200
    st.write(f"**Level {cur_lvl} Athlete**")
    st.progress(min(cur_xp / next_xp, 1.0))
    st.caption(f"{cur_xp} / {next_xp} XP to Level {cur_lvl + 1}")
    
    st.divider()
    
    # Target Goals Quick Override
    st.markdown("### 🎯 Goals Overview")
    calc_bmr = calculate_bmr(
        st.session_state.user_profile.get("weight_kg", 70),
        st.session_state.user_profile.get("height_cm", 175),
        st.session_state.user_profile.get("age", 20),
        st.session_state.user_profile.get("gender", "Male")
    )
    calc_tdee = calculate_tdee(calc_bmr, st.session_state.user_profile.get("activity_level", "Moderately Active"))
    
    st.write(f"• **Est. BMR:** {calc_bmr} kcal")
    st.write(f"• **Est. TDEE:** {calc_tdee} kcal")
    st.write(f"• **Daily Cal Target:** {st.session_state.user_profile.get('custom_cal_goal', 2000)} kcal")
    st.write(f"• **Water Target:** {st.session_state.user_profile.get('custom_water_goal', 8)} glasses")
    
    st.divider()
    
    if st.button("🔄 Reset Today's Progress", use_container_width=True):
        st.session_state.history_logs[today_str] = {
            "calories_eaten": 0,
            "calories_burned": 0,
            "protein_g": 0,
            "carbs_g": 0,
            "fat_g": 0,
            "water_glasses": 0,
            "entries": []
        }
        save_stored_data()
        st.toast("Today's stats reset!", icon="🧹")
        st.rerun()

# ==============================================================================
# 7. MAIN APP HEADER & TAB NAVIGATION
# ==============================================================================
st.title("⚡ FitPulse Pro")
st.caption("Advanced Real-time Fitness, Macro-Nutrition & Telemetry Dashboard")

tabs = st.tabs([
    "📊 Live Dashboard", 
    "🍽️ Nutrition & Macros", 
    "🏃 Workout Studio", 
    "💧 Hydration", 
    "📈 Advanced Analytics",
    "👤 User Profile & Settings"
])

# ==============================================================================
# TAB 1: LIVE DASHBOARD
# ==============================================================================
with tabs[0]:
    st.markdown("<div class='section-header'>🔥 Daily Overview</div>", unsafe_allow_html=True)
    
    c_eaten = current_day_data["calories_eaten"]
    c_burned = current_day_data["calories_burned"]
    net_cals = c_eaten - c_burned
    target_cals = st.session_state.user_profile.get("custom_cal_goal", 2000)
    target_water = st.session_state.user_profile.get("custom_water_goal", 8)
    rem_cals = target_cals - net_cals

    # Top Headline Banner
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Calories Consumed", f"{c_eaten} kcal", delta="Food")
    m2.metric("Calories Burned", f"{c_burned} kcal", delta="Workouts", delta_color="inverse")
    m3.metric("Net Total", f"{net_cals} kcal", delta=f"{rem_cals} remaining" if rem_cals >= 0 else f"{abs(rem_cals)} over target")
    m4.metric("Hydration Status", f"{current_day_data['water_glasses']} / {target_water} 💧")

    st.write("---")

    # Progress Bars Section
    p_col1, p_col2 = st.columns(2)
    with p_col1:
        with st.container(border=True):
            st.markdown("### 🎯 Calorie Goal Meter")
            c_ratio = min(c_eaten / target_cals, 1.0) if target_cals > 0 else 0
            st.progress(c_ratio)
            st.caption(f"**{int(c_ratio * 100)}%** reached of your {target_cals} kcal target.")

    with p_col2:
        with st.container(border=True):
            st.markdown("### 💧 Hydration Progress")
            w_ratio = min(current_day_data['water_glasses'] / target_water, 1.0) if target_water > 0 else 0
            st.progress(w_ratio)
            st.caption(f"**{current_day_data['water_glasses']}** of {target_water} glasses logged today.")

    st.write("---")

    # Interactive Macro Targets Summary
    st.markdown("<div class='section-header'>🥗 Macronutrient Breakdown</div>", unsafe_allow_html=True)
    mc1, mc2, mc3 = st.columns(3)
    
    p_goal = st.session_state.user_profile.get("protein_goal_g", 140)
    c_goal = st.session_state.user_profile.get("carbs_goal_g", 250)
    f_goal = st.session_state.user_profile.get("fat_goal_g", 70)

    mc1.metric("Protein", f"{current_day_data['protein_g']}g / {p_goal}g")
    mc2.metric("Carbohydrates", f"{current_day_data['carbs_g']}g / {c_goal}g")
    mc3.metric("Healthy Fats", f"{current_day_data['fat_g']}g / {f_goal}g")

    st.write("---")

    # Dashboard Split: Quick Chart + Activity Feed
    ch_col, feed_col = st.columns([2, 1])
    
    with ch_col:
        st.subheader("📈 Energy Balance Visualizer")
        chart_df = pd.DataFrame({
            "Category": ["Food Consumed", "Calories Burned"],
            "Calories": [c_eaten, c_burned]
        })
        st.bar_chart(chart_df, x="Category", y="Calories")

    with feed_col:
        st.subheader("📜 Today's Activity Log")
        if current_day_data["entries"]:
            for log_item in reversed(current_day_data["entries"]):
                st.info(f"• {log_item}")
        else:
            st.caption("No entries logged yet today.")

# ==============================================================================
# TAB 2: NUTRITION & MACROS
# ==============================================================================
with tabs[1]:
    st.markdown("<div class='section-header'>🍽️ Nutrition & Meal Logger</div>", unsafe_allow_html=True)
    
    entry_mode = st.radio("Choose Entry Mode:", ["Select from Database", "Custom Item Entry"], horizontal=True)
    
    col_input, col_display = st.columns([2, 1])
    
    with col_input:
        if entry_mode == "Select from Database":
            with st.container(border=True):
                selected_food_key = st.selectbox("Search Common Database:", list(EXTENDED_FOOD_DATABASE.keys()))
                servings = st.number_input("Servings / Quantities:", min_value=0.25, max_value=10.0, value=1.0, step=0.25)
                
                food_stats = EXTENDED_FOOD_DATABASE[selected_food_key]
                scaled_cals = int(food_stats["cals"] * servings)
                scaled_p = int(food_stats["protein"] * servings)
                scaled_c = int(food_stats["carbs"] * servings)
                scaled_f = int(food_stats["fat"] * servings)
                
                st.caption(f"Estimated Impact: **{scaled_cals} kcal** | P: {scaled_p}g | C: {scaled_c}g | F: {scaled_f}g")
                
                if st.button("➕ Log Database Item", use_container_width=True):
                    current_day_data["calories_eaten"] += scaled_cals
                    current_day_data["protein_g"] += scaled_p
                    current_day_data["carbs_g"] += scaled_c
                    current_day_data["fat_g"] += scaled_f
                    
                    entry_text = f"Logged: {selected_food_key} (x{servings}) - {scaled_cals} kcal"
                    current_day_data["entries"].append(entry_text)
                    
                    add_xp(15)
                    st.toast(f"Added {selected_food_key}!", icon="🥗")
                    st.rerun()

        else:
            with st.container(border=True):
                custom_name = st.text_input("Meal / Drink Name:", placeholder="e.g. Homemade Smoothie")
                cc_1, cc_2 = st.columns(2)
                with cc_1:
                    custom_cals = st.number_input("Calories (kcal):", min_value=0, step=10)
                    custom_p = st.number_input("Protein (g):", min_value=0, step=1)
                with cc_2:
                    custom_c = st.number_input("Carbs (g):", min_value=0, step=1)
                    custom_f = st.number_input("Fat (g):", min_value=0, step=1)
                
                if st.button("➕ Log Custom Meal", use_container_width=True):
                    if custom_name.strip() != "":
                        current_day_data["calories_eaten"] += custom_cals
                        current_day_data["protein_g"] += custom_p
                        current_day_data["carbs_g"] += custom_c
                        current_day_data["fat_g"] += custom_f
                        
                        entry_text = f"Logged: {custom_name} - {custom_cals} kcal"
                        current_day_data["entries"].append(entry_text)
                        
                        add_xp(20)
                        st.toast(f"Added {custom_name}!", icon="🍔")
                        st.rerun()
                    else:
                        st.warning("Please type a meal name first!")

    with col_display:
        with st.container(border=True):
            st.markdown("### 📊 Macro Ratio Today")
            p = current_day_data["protein_g"]
            c = current_day_data["carbs_g"]
            f = current_day_data["fat_g"]
            
            macro_df = pd.DataFrame({
                "Macro": ["Protein", "Carbs", "Fat"],
                "Grams": [p, c, f]
            })
            st.dataframe(macro_df, use_container_width=True, hide_index=True)

# ==============================================================================
# TAB 3: WORKOUT STUDIO
# ==============================================================================
with tabs[2]:
    st.markdown("<div class='section-header'>🏃 Workout & Activity Studio</div>", unsafe_allow_html=True)
    
    w_col1, w_col2 = st.columns(2)
    
    with w_col1:
        with st.container(border=True):
            st.markdown("### ⚡ MET Calorie Burn Calculator")
            selected_workout = st.selectbox("Select Activity:", list(WORKOUT_MET_DATABASE.keys()))
            duration_mins = st.number_input("Duration (Minutes):", min_value=5, max_value=300, value=30, step=5)
            
            user_weight = st.session_state.user_profile.get("weight_kg", 70.0)
            met_val = WORKOUT_MET_DATABASE[selected_workout]
            
            # Calorie Calculation Formula: (MET * 3.5 * weight_kg / 200) * duration
            calculated_burn = int((met_val * 3.5 * user_weight / 200) * duration_mins)
            
            st.info(f"🔥 Estimated Burn: **{calculated_burn} kcal** ({duration_mins} mins)")
            
            if st.button("🔥 Log Calculated Workout", use_container_width=True):
                current_day_data["calories_burned"] += calculated_burn
                entry_text = f"Workout: {selected_workout} ({duration_mins} mins) - {calculated_burn} kcal"
                current_day_data["entries"].append(entry_text)
                
                add_xp(30)
                st.toast(f"Logged {selected_workout}!", icon="🏃")
                st.rerun()

    with w_col2:
        with st.container(border=True):
            st.markdown("### ✏️ Quick Manual Workout")
            manual_ex_name = st.text_input("Exercise Name:", placeholder="e.g. Heavy Squats")
            manual_burn = st.number_input("Calories Burned:", min_value=0, step=25, value=150)
            
            if st.button("🔥 Log Manual Workout", use_container_width=True):
                if manual_burn > 0:
                    current_day_data["calories_burned"] += manual_burn
                    name_tag = manual_ex_name if manual_ex_name.strip() != "" else "Workout"
                    entry_text = f"Workout: {name_tag} - {manual_burn} kcal"
                    current_day_data["entries"].append(entry_text)
                    
                    add_xp(25)
                    st.toast(f"Logged {name_tag}!", icon="🔥")
                    st.rerun()

# ==============================================================================
# TAB 4: HYDRATION STATION
# ==============================================================================
with tabs[3]:
    st.markdown("<div class='section-header'>💧 Hydration Tracker & Reminders</div>", unsafe_allow_html=True)
    
    h_col1, h_col2 = st.columns([1, 2])
    
    with h_col1:
        with st.container(border=True):
            st.markdown("### 🥤 Log Water")
            st.markdown(f"## **{current_day_data['water_glasses']}** Glasses logged")
            
            if st.button("🥤 +1 Glass (250ml)", use_container_width=True):
                current_day_data["water_glasses"] += 1
                current_day_data["entries"].append("💧 Drank 1 glass of water")
                add_xp(5)
                save_stored_data()
                st.rerun()
                
            if st.button("🥤 +2 Glasses (500ml)", use_container_width=True):
                current_day_data["water_glasses"] += 2
                current_day_data["entries"].append("💧 Drank 2 glasses of water")
                add_xp(10)
                save_stored_data()
                st.rerun()
                
            if st.button("➖ Remove 1 Glass", use_container_width=True):
                if current_day_data["water_glasses"] > 0:
                    current_day_data["water_glasses"] -= 1
                    save_stored_data()
                    st.rerun()

    with h_col2:
        with st.container(border=True):
            st.markdown("### 💡 Hydration Tips & Consistency")
            target_w = st.session_state.user_profile.get("custom_water_goal", 8)
            curr_w = current_day_data["water_glasses"]
            
            if curr_w >= target_w:
                st.success("🎉 You've reached your daily hydration target! Great job!")
            else:
                st.info(f"Drink **{target_w - curr_w} more glasses** to complete your daily goal.")
                
            st.write("""
            * **Morning Boost:** Drink 1 glass right after waking up to kickstart metabolism.
            * **Workout Hydration:** Drink 1-2 extra glasses during intense exercise.
            * **Cognitive Focus:** Mild dehydration can reduce concentration and energy levels.
            """)

# ==============================================================================
# TAB 5: ADVANCED ANALYTICS & HISTORY
# ==============================================================================
with tabs[4]:
    st.markdown("<div class='section-header'>📈 Trends & Historical Telemetry</div>", unsafe_allow_html=True)
    
    st.markdown("### 📅 Weekly Performance Simulation")
    
    # Generate 7-day trend data
    days = [(datetime.date.today() - datetime.timedelta(days=i)).strftime("%a %d") for i in range(6, -1, -1)]
    history_df = pd.DataFrame({
        "Day": days,
        "Calories Consumed": [1950, 2100, 1850, 2200, 1900, 2050, current_day_data["calories_eaten"]],
        "Calories Burned": [300, 450, 250, 500, 350, 400, current_day_data["calories_burned"]],
        "Water Glasses": [8, 7, 9, 8, 6, 8, current_day_data["water_glasses"]]
    })
    
    st.line_chart(history_df, x="Day", y=["Calories Consumed", "Calories Burned"])
    st.bar_chart(history_df, x="Day", y="Water Glasses")
    
    st.divider()
    
    # Data Exporter
    st.markdown("### 📄 Export Your Health Data")
    csv_data = history_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Weekly Telemetry Report (CSV)",
        data=csv_data,
        file_name="fitpulse_weekly_report.csv",
        mime="text/csv",
        use_container_width=True
    )

# ==============================================================================
# TAB 6: USER PROFILE & SETTINGS
# ==============================================================================
with tabs[5]:
    st.markdown("<div class='section-header'>👤 Profile Settings & Goal Tuning</div>", unsafe_allow_html=True)
    
    prof = st.session_state.user_profile
    
    with st.form("profile_form"):
        col_p1, col_p2 = st.columns(2)
        
        with col_p1:
            u_name = st.text_input("Name:", value=prof.get("name", "Athlete"))
            u_age = st.number_input("Age:", min_value=10, max_value=100, value=prof.get("age", 20))
            u_gender = st.selectbox("Gender:", ["Male", "Female"], index=0 if prof.get("gender") == "Male" else 1)
            u_weight = st.number_input("Weight (kg):", min_value=30.0, max_value=250.0, value=prof.get("weight_kg", 70.0), step=0.5)
            u_height = st.number_input("Height (cm):", min_value=100.0, max_value=230.0, value=prof.get("height_cm", 175.0), step=1.0)
            
        with col_p2:
            u_act = st.selectbox("Activity Level:", ["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extra Active"])
            u_cal_target = st.number_input("Daily Calorie Target (kcal):", min_value=1000, max_value=6000, value=prof.get("custom_cal_goal", 2000), step=100)
            u_water_target = st.number_input("Daily Water Target (Glasses):", min_value=4, max_value=20, value=prof.get("custom_water_goal", 8))
            
            u_prot_target = st.number_input("Protein Goal (g):", min_value=20, max_value=400, value=prof.get("protein_goal_g", 140))
            u_carb_target = st.number_input("Carbs Goal (g):", min_value=20, max_value=600, value=prof.get("carbs_goal_g", 250))
            u_fat_target = st.number_input("Fat Goal (g):", min_value=10, max_value=200, value=prof.get("fat_goal_g", 70))
            
        submit_profile = st.form_submit_button("💾 Save Profile Changes", use_container_width=True)
        
        if submit_profile:
            st.session_state.user_profile = {
                "name": u_name,
                "age": u_age,
                "gender": u_gender,
                "weight_kg": u_weight,
                "height_cm": u_height,
                "activity_level": u_act,
                "custom_cal_goal": u_cal_target,
                "custom_water_goal": u_water_target,
                "protein_goal_g": u_prot_target,
                "carbs_goal_g": u_carb_target,
                "fat_goal_g": u_fat_target
            }
            save_stored_data()
            st.toast("Profile settings updated successfully!", icon="✅")
            st.rerun()

# ==============================================================================
# END OF CODE (SAVE STATE AUTOMATICALLY)
# ==============================================================================
save_stored_data()
