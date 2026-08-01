import streamlit as st
import pandas as pd
import numpy as np
import datetime
import json
import os
import math

# ==============================================================================
# SECTION 1: PAGE CONFIGURATION & GLOBAL STYLES
# ==============================================================================
st.set_page_config(
    page_title="FitPulse Pro | Complete Health & Nutrition Suite",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-Contrast Modern Theme CSS
st.markdown("""
    <style>
    /* Global App Background */
    .stApp {
        background-color: #0A0D12;
        color: #F0F2F5;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Sidebar Background Override */
    section[data-testid="stSidebar"] {
        background-color: #121620;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Container Border Enhancements */
    div[data-testid="stVerticalBlock"] > div[data-testid="stBlock"] {
        border-radius: 12px;
    }
    
    /* High-Tech Metric Cards */
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 18px;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    
    div[data-testid="stMetric"]:hover {
        border-color: rgba(0, 230, 118, 0.4);
        transform: translateY(-2px);
    }
    
    /* Custom Navigation Tab Design */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        padding-bottom: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 12px 24px;
        border-radius: 8px;
        background-color: rgba(255, 255, 255, 0.03);
        color: #A0AAB8;
        font-weight: 600;
        border: 1px solid transparent;
        transition: all 0.2s ease-in-out;
    }
    .stTabs [aria-selected="true"] {
        background-color: #00E676 !important;
        color: #000000 !important;
        font-weight: 700 !important;
        border-color: #00E676 !important;
        box-shadow: 0 0 15px rgba(0, 230, 118, 0.3);
    }
    
    /* Section Titles */
    .section-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: #00E676;
        margin-top: 10px;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .sub-header {
        font-size: 1.1rem;
        font-weight: 600;
        color: #E0E6ED;
        margin-bottom: 10px;
    }

    /* Custom Badges */
    .badge-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 12px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 10px;
    }
    .badge-card-unlocked {
        background: rgba(0, 230, 118, 0.1);
        border: 1px solid #00E676;
        padding: 12px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 10px;
    }

    /* Custom Progress Bar Override */
    .stProgress > div > div > div > div {
        background-color: #00E676;
    }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# SECTION 2: DATA PERSISTENCE & FILE STORAGE ENGINE
# ==============================================================================
DATA_FILE_PATH = "fitpulse_enterprise_data.json"

def initialize_default_system_state():
    """Generates the initial state tree if no local storage file exists."""
    return {
        "profile": {
            "name": "Athlete Pro",
            "age": 24,
            "weight_kg": 75.0,
            "height_cm": 178.0,
            "gender": "Male",
            "activity_level": "Moderately Active",
            "goal_type": "Maintain Weight",
            "custom_cal_goal": 2300,
            "custom_water_goal": 10,
            "protein_goal_g": 160,
            "carbs_goal_g": 260,
            "fat_goal_g": 70,
            "fiber_goal_g": 30,
            "sodium_goal_mg": 2300
        },
        "streak_count": 1,
        "last_active_date": str(datetime.date.today()),
        "xp_points": 150,
        "user_level": 1,
        "unlocked_badges": ["First Step", "Hydration Starter"],
        "custom_recipes": {},
        "daily_logs": {}
    }

def load_system_data():
    """Reads stored JSON telemetry from local storage."""
    if os.path.exists(DATA_FILE_PATH):
        try:
            with open(DATA_FILE_PATH, "r") as storage_file:
                return json.load(storage_file)
        except Exception as err:
            st.warning(f"Storage reload error: {err}. Reverting to defaults.")
            return initialize_default_system_state()
    return initialize_default_system_state()

def commit_system_data():
    """Writes session state telemetry to disk."""
    persistent_payload = {
        "profile": st.session_state.user_profile,
        "streak_count": st.session_state.streak_count,
        "last_active_date": str(datetime.date.today()),
        "xp_points": st.session_state.xp_points,
        "user_level": st.session_state.user_level,
        "unlocked_badges": st.session_state.unlocked_badges,
        "custom_recipes": st.session_state.custom_recipes,
        "daily_logs": st.session_state.history_logs
    }
    try:
        with open(DATA_FILE_PATH, "w") as storage_file:
            json.dump(persistent_payload, storage_file, indent=4)
    except Exception as err:
        st.error(f"Failed to persist state: {err}")

# ==============================================================================
# SECTION 3: EXTENDED NUTRITION, MICRONUTRIENT & EXERCISE LIBRARIES
# ==============================================================================
FOOD_LIBRARY = {
    # Meats, Poultry & Fish
    "Chicken Breast (Grilled, 6oz)": {"cals": 280, "p": 52, "c": 0, "f": 6, "fiber": 0, "sodium": 120},
    "Chicken Thigh (Skinless, 6oz)": {"cals": 330, "p": 42, "c": 0, "f": 18, "fiber": 0, "sodium": 140},
    "Salmon Fillet (Baked, 6oz)": {"cals": 340, "p": 34, "c": 0, "f": 22, "fiber": 0, "sodium": 90},
    "Sirloin Steak (6oz)": {"cals": 410, "p": 46, "c": 0, "f": 24, "fiber": 0, "sodium": 100},
    "Ground Turkey 93% (6oz)": {"cals": 290, "p": 36, "c": 0, "f": 14, "fiber": 0, "sodium": 115},
    "Canned Tuna in Water (1 Can)": {"cals": 150, "p": 32, "c": 0, "f": 2, "fiber": 0, "sodium": 350},
    "Shrimp (Cooked, 6oz)": {"cals": 160, "p": 36, "c": 1, "f": 2, "fiber": 0, "sodium": 380},
    "Ground Beef 80/20 (6oz)": {"cals": 430, "p": 43, "c": 0, "f": 28, "fiber": 0, "sodium": 110},
    "Pork Chop (Lean, 6oz)": {"cals": 310, "p": 44, "c": 0, "f": 14, "fiber": 0, "sodium": 85},

    # Eggs, Dairy & Plant Proteins
    "Eggs (Large, 2 Whole)": {"cals": 140, "p": 12, "c": 1, "f": 10, "fiber": 0, "sodium": 140},
    "Egg Whites (1 Cup)": {"cals": 120, "p": 26, "c": 2, "f": 0, "fiber": 0, "sodium": 400},
    "Tofu (Firm, 1 Cup)": {"cals": 180, "p": 20, "c": 4, "f": 11, "fiber": 2, "sodium": 20},
    "Tempeh (1 Cup)": {"cals": 320, "p": 31, "c": 16, "f": 18, "fiber": 7, "sodium": 15},
    "Whey Protein Powder (1 Scoop)": {"cals": 120, "p": 24, "c": 3, "f": 2, "fiber": 1, "sodium": 130},
    "Plant Protein Powder (1 Scoop)": {"cals": 130, "p": 22, "c": 5, "f": 3, "fiber": 3, "sodium": 200},
    "Greek Yogurt 0% (1 Cup)": {"cals": 130, "p": 22, "c": 8, "f": 0, "fiber": 0, "sodium": 85},
    "Cottage Cheese 2% (1 Cup)": {"cals": 180, "p": 24, "c": 8, "f": 5, "fiber": 0, "sodium": 700},

    # Rice, Grains & Starchy Carbs
    "White Rice (Cooked, 1 Cup)": {"cals": 205, "p": 4, "c": 45, "f": 0, "fiber": 1, "sodium": 0},
    "Brown Rice (Cooked, 1 Cup)": {"cals": 215, "p": 5, "c": 45, "f": 2, "fiber": 4, "sodium": 2},
    "Sweet Potato (Medium, Baked)": {"cals": 103, "p": 2, "c": 24, "f": 0, "fiber": 4, "sodium": 40},
    "White Potato (Medium, Baked)": {"cals": 160, "p": 4, "c": 37, "f": 0, "fiber": 4, "sodium": 15},
    "Oatmeal (Cooked, 1 Cup)": {"cals": 160, "p": 6, "c": 28, "f": 3, "fiber": 4, "sodium": 2},
    "Quinoa (Cooked, 1 Cup)": {"cals": 220, "p": 8, "c": 39, "f": 4, "fiber": 5, "sodium": 13},
    "Whole Wheat Bread (2 Slices)": {"cals": 160, "p": 8, "c": 28, "f": 2, "fiber": 4, "sodium": 260},
    "Pasta (Cooked, 1 Cup)": {"cals": 220, "p": 8, "c": 43, "f": 1, "fiber": 3, "sodium": 1},
    "Bagel (Plain, 1 Whole)": {"cals": 290, "p": 11, "c": 56, "f": 2, "fiber": 2, "sodium": 430},

    # Fruits & Vegetables
    "Apple (Medium Whole)": {"cals": 95, "p": 0, "c": 25, "f": 0, "fiber": 4, "sodium": 1},
    "Banana (Medium Whole)": {"cals": 105, "p": 1, "c": 27, "f": 0, "fiber": 3, "sodium": 1},
    "Blueberries (1 Cup Fresh)": {"cals": 85, "p": 1, "c": 21, "f": 1, "fiber": 4, "sodium": 1},
    "Strawberries (1 Cup Fresh)": {"cals": 50, "p": 1, "c": 12, "f": 0, "fiber": 3, "sodium": 1},
    "Avocado (Medium Whole)": {"cals": 240, "p": 3, "c": 12, "f": 22, "fiber": 10, "sodium": 10},
    "Broccoli (Steamed, 1 Cup)": {"cals": 55, "p": 4, "c": 11, "f": 0, "fiber": 5, "sodium": 60},
    "Spinach (Raw, 2 Cups)": {"cals": 14, "p": 2, "c": 2, "f": 0, "fiber": 2, "sodium": 45},
    "White Mushrooms (1 Cup)": {"cals": 15, "p": 2, "c": 2, "f": 0, "fiber": 1, "sodium": 5},
    "Asparagus (10 Spears)": {"cals": 30, "p": 3, "c": 5, "f": 0, "fiber": 3, "sodium": 2},

    # Nuts, Seeds & Healthy Fats
    "Almonds (1 oz / ~28 Nuts)": {"cals": 160, "p": 6, "c": 6, "f": 14, "fiber": 4, "sodium": 0},
    "Walnuts (1 oz)": {"cals": 185, "p": 4, "c": 4, "f": 18, "fiber": 2, "sodium": 0},
    "Peanut Butter (2 tbsp)": {"cals": 190, "p": 8, "c": 7, "f": 16, "fiber": 2, "sodium": 140},
    "Olive Oil (1 tbsp)": {"cals": 120, "p": 0, "c": 0, "f": 14, "fiber": 0, "sodium": 0},
    "Chia Seeds (2 tbsp)": {"cals": 140, "p": 5, "c": 12, "f": 9, "fiber": 10, "sodium": 5},

    # Convenience, Meals & Snacks
    "Slice of Pepperoni Pizza": {"cals": 290, "p": 12, "c": 32, "f": 12, "fiber": 2, "sodium": 680},
    "Cheeseburger (Fast Food)": {"cals": 535, "p": 30, "c": 40, "f": 28, "fiber": 2, "sodium": 1050},
    "Protein Bar (Chocolate Crunch)": {"cals": 210, "p": 20, "c": 22, "f": 7, "fiber": 10, "sodium": 200},
    "Sushi Roll (California Roll)": {"cals": 255, "p": 9, "c": 38, "f": 7, "fiber": 6, "sodium": 500},
    "Burrito Bowl (Chicken & Rice)": {"cals": 650, "p": 45, "c": 68, "f": 21, "fiber": 12, "sodium": 1250}
}

EXERCISE_MET_LIBRARY = {
    "Cardio": {
        "Running (Moderate, 5 mph)": 8.3,
        "Running (Vigorous, 7.5 mph)": 11.8,
        "Running (Sprint Interval)": 14.5,
        "Cycling (Moderate, 12-14 mph)": 6.8,
        "Cycling (Vigorous, 16+ mph)": 10.0,
        "Rowing Machine (Moderate)": 7.0,
        "Rowing Machine (Intense)": 8.5,
        "Elliptical Machine": 5.0,
        "Stairmaster / Step Mill": 9.0,
        "Jumping Rope (Moderate)": 11.8,
        "Brisk Walking (3.5 mph)": 3.8
    },
    "Strength Training": {
        "Bodybuilding (Heavy Weightlifting)": 6.0,
        "Circuit Training (High Intensity)": 8.0,
        "Calisthenics (Push-ups, Pull-ups)": 5.0,
        "Powerlifting (Low Reps, Heavy Rest)": 4.0,
        "Kettlebell Swings / Flow": 9.8,
        "CrossFit WOD": 10.0
    },
    "Sports & Recreation": {
        "Basketball (Competitive Game)": 8.0,
        "Soccer (Full Pitch Match)": 10.0,
        "Tennis (Singles Match)": 7.3,
        "Swimming (Freestyle Moderate)": 5.8,
        "Swimming (Laps Vigorous)": 9.8,
        "Volleyball (Beach or Indoor)": 4.0,
        "Boxing (Sparring or Heavy Bag)": 7.8,
        "Rock Climbing": 8.0,
        "Yoga / Vinyasa Flow": 3.0,
        "Pilates Mat Work": 3.0
    }
}

GAMIFICATION_BADGES = {
    "First Step": {"desc": "Logged your first activity on FitPulse Pro.", "icon": "🥉"},
    "Hydration Starter": {"desc": "Logged at least 8 glasses of water in a day.", "icon": "💧"},
    "Macro Master": {"desc": "Hit your exact protein target within 5%.", "icon": "🥩"},
    "Calorie Precision": {"desc": "Stayed within 50 kcal of your daily target.", "icon": "🎯"},
    "Iron Lifter": {"desc": "Logged 3 or more strength workouts.", "icon": "🏋️"},
    "Cardio Machine": {"desc": "Burned 500+ kcal in exercise in a single day.", "icon": "🔥"},
    "Streak Legend": {"desc": "Maintained a 7-day active usage streak.", "icon": "⚡"},
    "Centurion": {"desc": "Earned over 1,000 total XP points.", "icon": "👑"}
}

MOTIVATIONAL_QUOTES = [
    "“Action is the foundational key to all success.” — Pablo Picasso",
    "“Success starts with self-discipline.” — Dwayne Johnson",
    "“The only bad workout is the one that didn't happen.”",
    "“Small daily improvements over time lead to stunning results.” — Robin Sharma",
    "“Energy flows where attention goes.” — Tony Robbins"
]

# ==============================================================================
# SECTION 4: SESSION STATE INITIALIZATION & ROUTING
# ==============================================================================
raw_system_state = load_system_data()

if "user_profile" not in st.session_state:
    st.session_state.user_profile = raw_system_state.get("profile", {})
if "streak_count" not in st.session_state:
    st.session_state.streak_count = raw_system_state.get("streak_count", 1)
if "xp_points" not in st.session_state:
    st.session_state.xp_points = raw_system_state.get("xp_points", 150)
if "user_level" not in st.session_state:
    st.session_state.user_level = raw_system_state.get("user_level", 1)
if "unlocked_badges" not in st.session_state:
    st.session_state.unlocked_badges = raw_system_state.get("unlocked_badges", ["First Step", "Hydration Starter"])
if "custom_recipes" not in st.session_state:
    st.session_state.custom_recipes = raw_system_state.get("custom_recipes", {})
if "history_logs" not in st.session_state:
    st.session_state.history_logs = raw_system_state.get("daily_logs", {})

current_today_key = str(datetime.date.today())

if current_today_key not in st.session_state.history_logs:
    st.session_state.history_logs[current_today_key] = {
        "calories_eaten": 0,
        "calories_burned": 0,
        "protein_g": 0,
        "carbs_g": 0,
        "fat_g": 0,
        "fiber_g": 0,
        "sodium_mg": 0,
        "water_glasses": 0,
        "entries": []
    }

active_day = st.session_state.history_logs[current_today_key]

# ==============================================================================
# SECTION 5: MATHEMATICAL CALCULATIONS (BMI, BMR, TDEE, MACROS)
# ==============================================================================
def compute_bmi(weight_kg, height_cm):
    """Calculates Body Mass Index (BMI) and returns score + classification."""
    if height_cm <= 0:
        return 0.0, "Invalid Height"
    meters = height_cm / 100.0
    bmi = round(weight_kg / (meters * meters), 1)
    if bmi < 18.5:
        category = "Underweight"
    elif 18.5 <= bmi < 25.0:
        category = "Normal Weight"
    elif 25.0 <= bmi < 30.0:
        category = "Overweight"
    else:
        category = "Obese"
    return bmi, category

def compute_bmr_mifflin_st_jeor(weight_kg, height_cm, age, gender):
    """Calculates Basal Metabolic Rate using Mifflin-St Jeor formula."""
    if gender == "Male":
        return int(10 * weight_kg + 6.25 * height_cm - 5 * age + 5)
    else:
        return int(10 * weight_kg + 6.25 * height_cm - 5 * age - 161)

def compute_tdee(bmr, activity_level):
    """Multiplies BMR by activity multiplier to estimate total daily energy expenditure."""
    multipliers = {
        "Sedentary": 1.2,
        "Lightly Active": 1.375,
        "Moderately Active": 1.55,
        "Very Active": 1.725,
        "Extra Active": 1.9
    }
    return int(bmr * multipliers.get(activity_level, 1.2))

def grant_user_xp(points, context_message=""):
    """Adds XP points and handles level ups and badge triggers."""
    st.session_state.xp_points += points
    threshold_xp = st.session_state.user_level * 250
    
    if st.session_state.xp_points >= threshold_xp:
        st.session_state.user_level += 1
        st.balloons()
        st.toast(f"🎉 LEVEL UP! You reached Level {st.session_state.user_level}!", icon="🏆")
        
    if "Centurion" not in st.session_state.unlocked_badges and st.session_state.xp_points >= 1000:
        st.session_state.unlocked_badges.append("Centurion")
        st.toast("🏅 Unlocked Badge: Centurion!", icon="👑")
        
    commit_system_data()

# ==============================================================================
# SECTION 6: SIDEBAR CONTROL PANEL & PROFILE TELEMETRY
# ==============================================================================
with st.sidebar:
    st.title("⚡ Control Center")
    st.caption(f"Profile: **{st.session_state.user_profile.get('name', 'Athlete Pro')}**")
    
    # User XP & Level Card
    st.markdown("### 🏆 Rank Telemetry")
    user_lvl = st.session_state.user_level
    user_xp = st.session_state.xp_points
    next_level_xp = user_lvl * 250
    st.write(f"**Level {user_lvl} Fitness Enthusiast**")
    st.progress(min(user_xp / next_level_xp, 1.0))
    st.caption(f"Progress: **{user_xp}** / {next_level_xp} XP")
    
    st.divider()
    
    # Biometric Summary Box
    st.markdown("### 📐 Biometric Metrics")
    w = st.session_state.user_profile.get("weight_kg", 75.0)
    h = st.session_state.user_profile.get("height_cm", 178.0)
    a = st.session_state.user_profile.get("age", 24)
    g = st.session_state.user_profile.get("gender", "Male")
    act = st.session_state.user_profile.get("activity_level", "Moderately Active")
    
    bmi_val, bmi_cat = compute_bmi(w, h)
    bmr_val = compute_bmr_mifflin_st_jeor(w, h, a, g)
    tdee_val = compute_tdee(bmr_val, act)
    
    st.write(f"• **BMI:** {bmi_val} ({bmi_cat})")
    st.write(f"• **Basal Metabolic Rate:** {bmr_val} kcal")
    st.write(f"• **Est. Maintenance (TDEE):** {tdee_val} kcal")
    
    st.divider()
    
    # Daily Target Overrides
    st.markdown("### 🎯 Active Goals")
    c_target = st.session_state.user_profile.get("custom_cal_goal", 2300)
    w_target = st.session_state.user_profile.get("custom_water_goal", 10)
    st.write(f"• **Calorie Target:** {c_target} kcal")
    st.write(f"• **Hydration Target:** {w_target} glasses")
    st.write(f"• **Protein Target:** {st.session_state.user_profile.get('protein_goal_g', 160)}g")
    
    st.divider()
    
    # Quote of the Session
    st.markdown("### 💬 Daily Inspiration")
    st.caption(MOTIVATIONAL_QUOTES[hash(current_today_key) % len(MOTIVATIONAL_QUOTES)])
    
    st.divider()
    if st.button("🔄 Reset Today's Log", use_container_width=True):
        st.session_state.history_logs[current_today_key] = {
            "calories_eaten": 0,
            "calories_burned": 0,
            "protein_g": 0,
            "carbs_g": 0,
            "fat_g": 0,
            "fiber_g": 0,
            "sodium_mg": 0,
            "water_glasses": 0,
            "entries": []
        }
        commit_system_data()
        st.toast("Today's telemetry reset!", icon="🧹")
        st.rerun()

# ==============================================================================
# SECTION 7: MAIN HEADER & MULTI-TAB ARCHITECTURE
# ==============================================================================
st.title("⚡ FitPulse Pro")
st.caption("Enterprise-Grade Fitness, Macro-Nutrition, Telemetry & Biometrics Suite")

app_tabs = st.tabs([
    "📊 Live Command Center", 
    "🍽️ Nutrition & Macros", 
    "🍳 Recipe Builder",
    "🏃 Workout Studio", 
    "💧 Hydration Tracker", 
    "🏆 Gamification & Badges",
    "📈 Analytics & History",
    "👤 Profile & Biometrics"
])

# ==============================================================================
# TAB 1: LIVE COMMAND CENTER
# ==============================================================================
with app_tabs[0]:
    st.markdown("<div class='section-header'>🔥 Real-Time Health Dashboard</div>", unsafe_allow_html=True)
    
    c_eaten = active_day["calories_eaten"]
    c_burned = active_day["calories_burned"]
    net_cals = c_eaten - c_burned
    target_cals = st.session_state.user_profile.get("custom_cal_goal", 2300)
    target_water = st.session_state.user_profile.get("custom_water_goal", 10)
    remaining_cals = target_cals - net_cals

    # Top Metric Banner Cards
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    m_col1.metric("Calories Consumed", f"{c_eaten} kcal", delta="Food Intake")
    m_col2.metric("Active Calorie Burn", f"{c_burned} kcal", delta="Workouts", delta_color="inverse")
    m_col3.metric("Net Calorie Balance", f"{net_cals} kcal", delta=f"{remaining_cals} remaining" if remaining_cals >= 0 else f"{abs(remaining_cals)} over limit")
    m_col4.metric("Hydration Telemetry", f"{active_day['water_glasses']} / {target_water} 💧")

    st.write("---")

    # Visual Progress Section
    pr_col1, pr_col2 = st.columns(2)
    
    with pr_col1:
        with st.container(border=True):
            st.markdown("<div class='sub-header'>🎯 Daily Calorie Progress</div>", unsafe_allow_html=True)
            cal_ratio = min(c_eaten / target_cals, 1.0) if target_cals > 0 else 0.0
            st.progress(cal_ratio)
            st.caption(f"**{int(cal_ratio * 100)}%** reached of your **{target_cals} kcal** target.")

    with pr_col2:
        with st.container(border=True):
            st.markdown("<div class='sub-header'>💧 Hydration Tracker</div>", unsafe_allow_html=True)
            w_ratio = min(active_day["water_glasses"] / target_water, 1.0) if target_water > 0 else 0.0
            st.progress(w_ratio)
            st.caption(f"Logged **{active_day['water_glasses']}** of **{target_water}** daily target glasses.")

    st.write("---")

    # Macronutrient Overview Cards
    st.markdown("<div class='section-header'>🥗 Macronutrient Telemetry</div>", unsafe_allow_html=True)
    mac1, mac2, mac3, mac4, mac5 = st.columns(5)
    
    prot_target = st.session_state.user_profile.get("protein_goal_g", 160)
    carb_target = st.session_state.user_profile.get("carbs_goal_g", 260)
    fat_target = st.session_state.user_profile.get("fat_goal_g", 70)
    fiber_target = st.session_state.user_profile.get("fiber_goal_g", 30)
    sodium_target = st.session_state.user_profile.get("sodium_goal_mg", 2300)

    mac1.metric("Protein", f"{active_day['protein_g']}g / {prot_target}g")
    mac2.metric("Carbohydrates", f"{active_day['carbs_g']}g / {carb_target}g")
    mac3.metric("Fats", f"{active_day['fat_g']}g / {fat_target}g")
    mac4.metric("Dietary Fiber", f"{active_day['fiber_g']}g / {fiber_target}g")
    mac5.metric("Sodium", f"{active_day['sodium_mg']}mg / {sodium_target}mg")

    st.write("---")

    # Lower Section: Chart Visualizer & Activity Feed
    chart_col, timeline_col = st.columns([2, 1])
    
    with chart_col:
        st.subheader("📈 Energy Balance Visualizer")
        balance_df = pd.DataFrame({
            "Category": ["Food Consumed", "Calories Burned"],
            "Calories": [c_eaten, c_burned]
        })
        st.bar_chart(balance_df, x="Category", y="Calories")

    with timeline_col:
        st.subheader("📜 Today's Event Feed")
        if active_day["entries"]:
            for entry_item in reversed(active_day["entries"]):
                st.info(f"• {entry_item}")
        else:
            st.caption("No entries recorded yet today.")

# ==============================================================================
# TAB 2: NUTRITION & MACROS
# ==============================================================================
with app_tabs[1]:
    st.markdown("<div class='section-header'>🍽️ Nutrition & Meal Logger</div>", unsafe_allow_html=True)
    
    entry_method = st.radio("Choose Entry Mode:", ["Standard Database", "Custom Item Input", "Saved Recipes"], horizontal=True)
    
    log_col1, log_col2 = st.columns([2, 1])
    
    with log_col1:
        if entry_method == "Standard Database":
            with st.container(border=True):
                st.markdown("<div class='sub-header'>🔎 Search Database</div>", unsafe_allow_html=True)
                selected_food = st.selectbox("Select Food Item:", list(FOOD_LIBRARY.keys()))
                serving_qty = st.number_input("Servings / Quantity Multiplier:", min_value=0.25, max_value=10.0, value=1.0, step=0.25)
                
                f_data = FOOD_LIBRARY[selected_food]
                calc_cals = int(f_data["cals"] * serving_qty)
                calc_p = int(f_data["p"] * serving_qty)
                calc_c = int(f_data["c"] * serving_qty)
                calc_f = int(f_data["f"] * serving_qty)
                calc_fib = int(f_data["fiber"] * serving_qty)
                calc_sod = int(f_data["sodium"] * serving_qty)
                
                st.caption(f"Macros: **{calc_cals} kcal** | P: {calc_p}g | C: {calc_c}g | F: {calc_f}g | Fiber: {calc_fib}g | Sodium: {calc_sod}mg")
                
                if st.button("➕ Log Food Entry", use_container_width=True):
                    active_day["calories_eaten"] += calc_cals
                    active_day["protein_g"] += calc_p
                    active_day["carbs_g"] += calc_c
                    active_day["fat_g"] += calc_f
                    active_day["fiber_g"] += calc_fib
                    active_day["sodium_mg"] += calc_sod
                    
                    log_text = f"Logged: {selected_food} (x{serving_qty}) - {calc_cals} kcal"
                    active_day["entries"].append(log_text)
                    
                    grant_user_xp(15, "Logged Food")
                    st.toast(f"Logged {selected_food}!", icon="🥗")
                    st.rerun()

        elif entry_method == "Custom Item Input":
            with st.container(border=True):
                st.markdown("<div class='sub-header'>✏️ Custom Meal Input</div>", unsafe_allow_html=True)
                c_meal_name = st.text_input("Meal / Beverage Name:", placeholder="e.g. Protein Smoothie")
                
                cc1, cc2, cc3 = st.columns(3)
                with cc1:
                    c_cals = st.number_input("Calories (kcal):", min_value=0, step=10, value=250)
                    c_prot = st.number_input("Protein (g):", min_value=0, step=1, value=20)
                with cc2:
                    c_carbs = st.number_input("Carbohydrates (g):", min_value=0, step=1, value=30)
                    c_fats = st.number_input("Fats (g):", min_value=0, step=1, value=5)
                with cc3:
                    c_fiber = st.number_input("Fiber (g):", min_value=0, step=1, value=4)
                    c_sod = st.number_input("Sodium (mg):", min_value=0, step=10, value=150)
                    
                if st.button("➕ Log Custom Item", use_container_width=True):
                    if c_meal_name.strip():
                        active_day["calories_eaten"] += c_cals
                        active_day["protein_g"] += c_prot
                        active_day["carbs_g"] += c_carbs
                        active_day["fat_g"] += c_fats
                        active_day["fiber_g"] += c_fiber
                        active_day["sodium_mg"] += c_sod
                        
                        log_text = f"Logged Custom: {c_meal_name} - {c_cals} kcal"
                        active_day["entries"].append(log_text)
                        
                        grant_user_xp(20, "Logged Custom Food")
                        st.toast(f"Logged {c_meal_name}!", icon="🍔")
                        st.rerun()
                    else:
                        st.warning("Please type an item name first!")

        else:
            with st.container(border=True):
                st.markdown("<div class='sub-header'>📖 Saved Custom Recipes</div>", unsafe_allow_html=True)
                if st.session_state.custom_recipes:
                    chosen_recipe = st.selectbox("Select Recipe:", list(st.session_state.custom_recipes.keys()))
                    recipe_data = st.session_state.custom_recipes[chosen_recipe]
                    
                    st.caption(f"Recipe Totals: **{recipe_data['cals']} kcal** | P: {recipe_data['p']}g | C: {recipe_data['c']}g | F: {recipe_data['f']}g")
                    
                    if st.button("➕ Log Recipe to Daily Feed", use_container_width=True):
                        active_day["calories_eaten"] += recipe_data["cals"]
                        active_day["protein_g"] += recipe_data["p"]
                        active_day["carbs_g"] += recipe_data["c"]
                        active_day["fat_g"] += recipe_data["f"]
                        
                        log_text = f"Logged Recipe: {chosen_recipe} - {recipe_data['cals']} kcal"
                        active_day["entries"].append(log_text)
                        
                        grant_user_xp(25, "Logged Recipe")
                        st.toast(f"Logged {chosen_recipe}!", icon="🍲")
                        st.rerun()
                else:
                    st.info("No custom recipes created yet. Use the 'Recipe Builder' tab!")

    with log_col2:
        with st.container(border=True):
            st.markdown("<div class='sub-header'>📊 Today's Macro Distribution</div>", unsafe_allow_html=True)
            p_val = active_day["protein_g"]
            c_val = active_day["carbs_g"]
            f_val = active_day["fat_g"]
            
            summary_table = pd.DataFrame({
                "Nutrient": ["Protein (g)", "Carbs (g)", "Fats (g)", "Fiber (g)", "Sodium (mg)"],
                "Amount": [p_val, c_val, f_val, active_day["fiber_g"], active_day["sodium_mg"]]
            })
            st.dataframe(summary_table, use_container_width=True, hide_index=True)

# ==============================================================================
# TAB 3: RECIPE BUILDER
# ==============================================================================
with app_tabs[2]:
    st.markdown("<div class='section-header'>🍳 Custom Recipe Builder</div>", unsafe_allow_html=True)
    st.caption("Combine ingredients from the database to calculate total meal macros and save for future quick-logging.")
    
    rb_col1, rb_col2 = st.columns([2, 1])
    
    with rb_col1:
        with st.container(border=True):
            st.markdown("<div class='sub-header'>🛠️ Create New Recipe</div>", unsafe_allow_html=True)
            recipe_title = st.text_input("Recipe Title:", placeholder="e.g. High-Protein Meal Prep Bowl")
            
            num_ingredients = st.number_input("Number of Ingredients:", min_value=1, max_value=8, value=3, step=1)
            
            recipe_ingredients = []
            tot_rec_cals = 0
            tot_rec_p = 0
            tot_rec_c = 0
            tot_rec_f = 0
            
            for i in range(int(num_ingredients)):
                st.markdown(f"**Ingredient #{i+1}**")
                ing_col1, ing_col2 = st.columns([3, 1])
                with ing_col1:
                    ing_item = st.selectbox(f"Select Item #{i+1}:", list(FOOD_LIBRARY.keys()), key=f"rec_ing_{i}")
                with ing_col2:
                    ing_qty = st.number_input(f"Qty #{i+1}:", min_value=0.25, max_value=10.0, value=1.0, step=0.25, key=f"rec_qty_{i}")
                
                f_stats = FOOD_LIBRARY[ing_item]
                tot_rec_cals += int(f_stats["cals"] * ing_qty)
                tot_rec_p += int(f_stats["p"] * ing_qty)
                tot_rec_c += int(f_stats["c"] * ing_qty)
                tot_rec_f += int(f_stats["f"] * ing_qty)
                recipe_ingredients.append(f"{ing_item} (x{ing_qty})")
            
            st.write("---")
            st.markdown(f"### Totals for **'{recipe_title if recipe_title else 'New Recipe'}'**:")
            st.write(f"• **Calories:** {tot_rec_cals} kcal")
            st.write(f"• **Protein:** {tot_rec_p}g | **Carbs:** {tot_rec_c}g | **Fat:** {tot_rec_f}g")
            
            if st.button("💾 Save Recipe", use_container_width=True):
                if recipe_title.strip():
                    st.session_state.custom_recipes[recipe_title] = {
                        "cals": tot_rec_cals,
                        "p": tot_rec_p,
                        "c": tot_rec_c,
                        "f": tot_rec_f,
                        "ingredients": recipe_ingredients
                    }
                    commit_system_data()
                    st.toast(f"Recipe '{recipe_title}' saved!", icon="💾")
                    st.rerun()
                else:
                    st.warning("Please enter a recipe title!")

    with rb_col2:
        with st.container(border=True):
            st.markdown("<div class='sub-header'>📚 Saved Recipes Library</div>", unsafe_allow_html=True)
            if st.session_state.custom_recipes:
                for r_name, r_info in st.session_state.custom_recipes.items():
                    with st.expander(r_name):
                        st.write(f"**Calories:** {r_info['cals']} kcal")
                        st.write(f"**Macros:** P: {r_info['p']}g | C: {r_info['c']}g | F: {r_info['f']}g")
                        st.write("**Ingredients:**")
                        for ing in r_info["ingredients"]:
                            st.write(f"• {ing}")
            else:
                st.caption("No custom recipes saved yet.")

# ==============================================================================
# TAB 4: WORKOUT STUDIO
# ==============================================================================
with app_tabs[3]:
    st.markdown("<div class='section-header'>🏃 Workout & Exercise Studio</div>", unsafe_allow_html=True)
    
    ex_category = st.radio("Workout Category:", list(EXERCISE_MET_LIBRARY.keys()), horizontal=True)
    
    w_col1, w_col2 = st.columns(2)
    
    with w_col1:
        with st.container(border=True):
            st.markdown("<div class='sub-header'>⚡ MET Calorie Burn Calculator</div>", unsafe_allow_html=True)
            selected_ex = st.selectbox("Select Activity:", list(EXERCISE_MET_LIBRARY[ex_category].keys()))
            duration_minutes = st.number_input("Duration (Minutes):", min_value=5, max_value=300, value=30, step=5)
            
            u_weight = st.session_state.user_profile.get("weight_kg", 75.0)
            met_value = EXERCISE_MET_LIBRARY[ex_category][selected_ex]
            
            # Calorie Burn Formula: (MET * 3.5 * weight_kg / 200) * minutes
            est_burn = int((met_value * 3.5 * u_weight / 200) * duration_minutes)
            
            st.info(f"🔥 Estimated Burn: **{est_burn} kcal** ({duration_minutes} mins)")
            
            if st.button("🔥 Log Calorie Burn", use_container_width=True):
                active_day["calories_burned"] += est_burn
                entry_log_msg = f"Workout ({ex_category}): {selected_ex} ({duration_minutes} mins) - {est_burn} kcal"
                active_day["entries"].append(entry_log_msg)
                
                grant_user_xp(30, "Logged Exercise")
                st.toast(f"Logged {selected_ex}!", icon="🏃")
                st.rerun()

    with w_col2:
        with st.container(border=True):
            st.markdown("<div class='sub-header'>✏️ Manual Exercise Input</div>", unsafe_allow_html=True)
            custom_ex_name = st.text_input("Exercise Name:", placeholder="e.g. Heavy Deadlifts")
            custom_ex_burn = st.number_input("Calories Burned (kcal):", min_value=0, step=25, value=200)
            
            if st.button("🔥 Log Manual Workout", use_container_width=True):
                if custom_ex_burn > 0:
                    active_day["calories_burned"] += custom_ex_burn
                    label = custom_ex_name if custom_ex_name.strip() else "Workout"
                    entry_log_msg = f"Workout: {label} - {custom_ex_burn} kcal"
                    active_day["entries"].append(entry_log_msg)
                    
                    grant_user_xp(25, "Logged Manual Exercise")
                    st.toast(f"Logged {label}!", icon="🔥")
                    st.rerun()

# ==============================================================================
# TAB 5: HYDRATION TRACKER
# ==============================================================================
with app_tabs[4]:
    st.markdown("<div class='section-header'>💧 Hydration Telemetry & Reminders</div>", unsafe_allow_html=True)
    
    wat_col1, wat_col2 = st.columns([1, 2])
    
    with wat_col1:
        with st.container(border=True):
            st.markdown("<div class='sub-header'>🥤 Water Input</div>", unsafe_allow_html=True)
            st.markdown(f"## **{active_day['water_glasses']}** Glasses")
            
            if st.button("🥤 +1 Glass (250 ml)", use_container_width=True):
                active_day["water_glasses"] += 1
                active_day["entries"].append("💧 Drank 1 glass of water (250 ml)")
                grant_user_xp(5, "Water Intake")
                commit_system_data()
                st.rerun()
                
            if st.button("🥤 +2 Glasses (500 ml)", use_container_width=True):
                active_day["water_glasses"] += 2
                active_day["entries"].append("💧 Drank 2 glasses of water (500 ml)")
                grant_user_xp(10, "Water Intake")
                commit_system_data()
                st.rerun()
                
            if st.button("➖ Remove 1 Glass", use_container_width=True):
                if active_day["water_glasses"] > 0:
                    active_day["water_glasses"] -= 1
                    commit_system_data()
                    st.rerun()

    with wat_col2:
        with st.container(border=True):
            st.markdown("<div class='sub-header'>💡 Hydration Strategy & Status</div>", unsafe_allow_html=True)
            h_target = st.session_state.user_profile.get("custom_water_goal", 10)
            h_current = active_day["water_glasses"]
            
            if h_current >= h_target:
                st.success("🎉 **Hydration Goal Reached!** Excellent fluid intake today.")
                if "Hydration Starter" not in st.session_state.unlocked_badges:
                    st.session_state.unlocked_badges.append("Hydration Starter")
                    st.toast("🏅 Badge Unlocked: Hydration Starter!", icon="💧")
            else:
                st.info(f"Target remaining: **{h_target - h_current} glasses** to complete daily goal.")
                
            st.write("""
            * **Peak Mental Focus:** Mild dehydration (1-2% loss of body water) negatively affects reaction time and mood.
            * **Athletic Performance:** Muscle tissue is approximately 75% water; hydration is critical for strength and endurance.
            * **Metabolic Rate:** Drinking cold water stimulates thermogenesis as your body warms the liquid to body temperature.
            """)

# ==============================================================================
# TAB 6: GAMIFICATION & BADGES
# ==============================================================================
with app_tabs[5]:
    st.markdown("<div class='section-header'>🏆 Gamification & Achievements</div>", unsafe_allow_html=True)
    
    g_col1, g_col2 = st.columns([1, 2])
    
    with g_col1:
        with st.container(border=True):
            st.markdown("<div class='sub-header'>👑 Level & Status</div>", unsafe_allow_html=True)
            st.write(f"**Level {st.session_state.user_level} Athlete**")
            st.write(f"**Total XP:** {st.session_state.xp_points} XP")
            st.write(f"**Active Streak:** {st.session_state.streak_count} Days ⚡")
            st.write(f"**Badges Unlocked:** {len(st.session_state.unlocked_badges)} / {len(GAMIFICATION_BADGES)}")

    with g_col2:
        st.markdown("### 🏅 Achievement Badges")
        
        badge_cols = st.columns(2)
        idx = 0
        for b_title, b_info in GAMIFICATION_BADGES.items():
            col_target = badge_cols[idx % 2]
            with col_target:
                if b_title in st.session_state.unlocked_badges:
                    st.markdown(f"""
                        <div class='badge-card-unlocked'>
                            <h3>{b_info['icon']} {b_title}</h3>
                            <p>{b_info['desc']}</p>
                            <small><b>UNLOCKED</b></small>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                        <div class='badge-card'>
                            <h3>🔒 {b_title}</h3>
                            <p>{b_info['desc']}</p>
                            <small>LOCKED</small>
                        </div>
                    """, unsafe_allow_html=True)
            idx += 1

# ==============================================================================
# TAB 7: ADVANCED ANALYTICS & HISTORY
# ==============================================================================
with app_tabs[6]:
    st.markdown("<div class='section-header'>📈 Analytics & Multi-Day Telemetry</div>", unsafe_allow_html=True)
    
    st.markdown("### 📅 Weekly Trend Simulation")
    
    trend_dates = [(datetime.date.today() - datetime.timedelta(days=i)).strftime("%a %d") for i in range(6, -1, -1)]
    
    analytics_df = pd.DataFrame({
        "Day": trend_dates,
        "Calories Consumed": [2100, 2250, 1900, 2300, 2050, 2150, active_day["calories_eaten"]],
        "Calories Burned": [350, 400, 250, 500, 300, 450, active_day["calories_burned"]],
        "Water Glasses": [8, 9, 7, 10, 8, 9, active_day["water_glasses"]]
    })
    
    st.line_chart(analytics_df, x="Day", y=["Calories Consumed", "Calories Burned"])
    st.bar_chart(analytics_df, x="Day", y="Water Glasses")
    
    st.divider()
    
    st.markdown("### 📄 Export Telemetry Report")
    csv_bytes = analytics_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Historical Report (CSV)",
        data=csv_bytes,
        file_name="fitpulse_analytics_report.csv",
        mime="text/csv",
        use_container_width=True
    )

# ==============================================================================
# TAB 8: USER PROFILE & BIOMETRICS SETTINGS
# ==============================================================================
with app_tabs[7]:
    st.markdown("<div class='section-header'>👤 Profile, Goals & Biometrics Engine</div>", unsafe_allow_html=True)
    
    p_data = st.session_state.user_profile
    
    with st.form("enterprise_profile_form"):
        pf_col1, pf_col2 = st.columns(2)
        
        with pf_col1:
            st.markdown("<div class='sub-header'>📋 Personal Info</div>", unsafe_allow_html=True)
            in_name = st.text_input("Name:", value=p_data.get("name", "Athlete Pro"))
            in_age = st.number_input("Age:", min_value=12, max_value=100, value=p_data.get("age", 24))
            in_gender = st.selectbox("Gender:", ["Male", "Female"], index=0 if p_data.get("gender") == "Male" else 1)
            in_weight = st.number_input("Weight (kg):", min_value=30.0, max_value=250.0, value=p_data.get("weight_kg", 75.0), step=0.5)
            in_height = st.number_input("Height (cm):", min_value=100.0, max_value=230.0, value=p_data.get("height_cm", 178.0), step=1.0)
            in_activity = st.selectbox("Activity Level:", ["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extra Active"], index=2)
            
        with pf_col2:
            st.markdown("<div class='sub-header'>🎯 Nutrition & Fluid Targets</div>", unsafe_allow_html=True)
            in_cal_goal = st.number_input("Calorie Target (kcal):", min_value=1000, max_value=6000, value=p_data.get("custom_cal_goal", 2300), step=50)
            in_water_goal = st.number_input("Water Target (Glasses):", min_value=4, max_value=25, value=p_data.get("custom_water_goal", 10), step=1)
            in_prot_goal = st.number_input("Protein Target (g):", min_value=20, max_value=400, value=p_data.get("protein_goal_g", 160), step=5)
            in_carb_goal = st.number_input("Carbs Target (g):", min_value=20, max_value=600, value=p_data.get("carbs_goal_g", 260), step=5)
            in_fat_goal = st.number_input("Fat Target (g):", min_value=10, max_value=200, value=p_data.get("fat_goal_g", 70), step=5)
            in_fiber_goal = st.number_input("Fiber Target (g):", min_value=10, max_value=100, value=p_data.get("fiber_goal_g", 30), step=2)
            
        save_btn = st.form_submit_button("💾 Save Settings", use_container_width=True)
        
        if save_btn:
            st.session_state.user_profile = {
                "name": in_name,
                "age": in_age,
                "gender": in_gender,
                "weight_kg": in_weight,
                "height_cm": in_height,
                "activity_level": in_activity,
                "custom_cal_goal": in_cal_goal,
                "custom_water_goal": in_water_goal,
                "protein_goal_g": in_prot_goal,
                "carbs_goal_g": in_carb_goal,
                "fat_goal_g": in_fat_goal,
                "fiber_goal_g": in_fiber_goal,
                "sodium_goal_mg": p_data.get("sodium_goal_mg", 2300)
            }
            commit_system_data()
            st.toast("Profile settings updated successfully!", icon="✅")
            st.rerun()

# ==============================================================================
# SECTION 8: AUTOMATIC STATE PERSISTENCE
# ==============================================================================
commit_system_data()
