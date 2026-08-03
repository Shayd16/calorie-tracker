import streamlit as st
import pandas as pd
import numpy as np
import datetime
import json
import os
import math

# ==============================================================================
# SECTION 1: PAGE CONFIGURATION & METRIC THEMING
# ==============================================================================
st.set_page_config(
    page_title="FitPulse Pro | Complete Health & Nutrition Suite",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-Contrast Modern Dark CSS Theme
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #0A0D12;
        color: #F0F2F5;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Sidebar Layout */
    section[data-testid="stSidebar"] {
        background-color: #121620;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Container Borders */
    div[data-testid="stVerticalBlock"] > div[data-testid="stBlock"] {
        border-radius: 12px;
    }
    
    /* High-Tech Metric Display Cards */
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
    
    /* Navigation Bar Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        padding-bottom: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 12px 20px;
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
    
    /* Typography Styles */
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

    /* Badge Displays */
    .badge-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 14px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 12px;
        min-height: 120px;
    }
    .badge-card-unlocked {
        background: rgba(0, 230, 118, 0.1);
        border: 1px solid #00E676;
        padding: 14px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 12px;
        min-height: 120px;
    }

    /* Override Streamlit Accent Color */
    .stProgress > div > div > div > div {
        background-color: #00E676;
    }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# SECTION 2: DATA STORAGE ENGINE & INITIALIZATION
# ==============================================================================
DATA_FILE_PATH = "fitpulse_enterprise_data.json"

def initialize_default_system_state():
    """Generates the initial state data object if no saved file exists."""
    return {
        "profile": {
            "name": "Athlete Pro",
            "age": 25,
            "weight_kg": 76.0,
            "height_cm": 178.0,
            "gender": "Male",
            "activity_level": "Moderately Active",
            "goal_type": "Maintain Weight",
            "custom_cal_goal": 2400,
            "custom_water_goal": 10,
            "protein_goal_g": 165,
            "carbs_goal_g": 270,
            "fat_goal_g": 70,
            "fiber_goal_g": 32,
            "sodium_goal_mg": 2300,
            "potassium_goal_mg": 3500,
            "sleep_goal_hrs": 8.0,
            "neck_cm": 38.0,
            "waist_cm": 81.0,
            "hip_cm": 95.0
        },
        "streak_count": 1,
        "last_active_date": str(datetime.date.today()),
        "xp_points": 200,
        "user_level": 1,
        "unlocked_badges": ["Streak Legend 1D", "Hydration Master 8G", "Rank Veteran Lvl 1"],
        "custom_recipes": {},
        "strength_workouts": [],
        "daily_logs": {}
    }

def load_system_data():
    """Reads telemetry from local JSON storage."""
    if os.path.exists(DATA_FILE_PATH):
        try:
            with open(DATA_FILE_PATH, "r") as storage_file:
                return json.load(storage_file)
        except Exception as err:
            st.warning(f"Storage reload error: {err}. Loading default profile.")
            return initialize_default_system_state()
    return initialize_default_system_state()

def commit_system_data():
    """Writes session telemetry to disk storage."""
    persistent_payload = {
        "profile": st.session_state.user_profile,
        "streak_count": st.session_state.streak_count,
        "last_active_date": str(datetime.date.today()),
        "xp_points": st.session_state.xp_points,
        "user_level": st.session_state.user_level,
        "unlocked_badges": st.session_state.unlocked_badges,
        "custom_recipes": st.session_state.custom_recipes,
        "strength_workouts": st.session_state.strength_workouts,
        "daily_logs": st.session_state.history_logs
    }
    try:
        with open(DATA_FILE_PATH, "w") as storage_file:
            json.dump(persistent_payload, storage_file, indent=4)
    except Exception as err:
        st.error(f"Failed to persist state: {err}")

# ==============================================================================
# SECTION 3: COMPREHENSIVE NUTRITION DATABASE
# ==============================================================================
FOOD_LIBRARY = {
    # Meats & Poultry
    "Chicken Breast (Grilled, 6oz)": {"cals": 280, "p": 52, "c": 0, "f": 6, "fiber": 0, "sodium": 120, "potassium": 440},
    "Chicken Thigh (Skinless, 6oz)": {"cals": 330, "p": 42, "c": 0, "f": 18, "fiber": 0, "sodium": 140, "potassium": 380},
    "Lean Ground Turkey 93/7 (6oz)": {"cals": 290, "p": 36, "c": 0, "f": 14, "fiber": 0, "sodium": 115, "potassium": 410},
    "Turkey Breast Slices (4oz)": {"cals": 120, "p": 24, "c": 1, "f": 2, "fiber": 0, "sodium": 650, "potassium": 300},
    "Sirloin Steak (Lean, 6oz)": {"cals": 390, "p": 48, "c": 0, "f": 20, "fiber": 0, "sodium": 105, "potassium": 560},
    "Ground Beef 80/20 (6oz)": {"cals": 430, "p": 43, "c": 0, "f": 28, "fiber": 0, "sodium": 110, "potassium": 490},
    "Pork Chop (Boneless, 6oz)": {"cals": 310, "p": 44, "c": 0, "f": 14, "fiber": 0, "sodium": 85, "potassium": 510},
    "Center Cut Bacon (3 Strips)": {"cals": 130, "p": 9, "c": 0, "f": 10, "fiber": 0, "sodium": 480, "potassium": 160},

    # Fish & Seafood
    "Atlantic Salmon Fillet (6oz)": {"cals": 350, "p": 35, "c": 0, "f": 22, "fiber": 0, "sodium": 95, "potassium": 620},
    "Canned Light Tuna in Water (1 Can)": {"cals": 150, "p": 32, "c": 0, "f": 2, "fiber": 0, "sodium": 360, "potassium": 340},
    "Shrimp (Steamed, 6oz)": {"cals": 160, "p": 36, "c": 1, "f": 2, "fiber": 0, "sodium": 380, "potassium": 310},
    "Cod Fillet (Baked, 6oz)": {"cals": 175, "p": 38, "c": 0, "f": 2, "fiber": 0, "sodium": 110, "potassium": 460},
    "Tilapia Fillet (Baked, 6oz)": {"cals": 210, "p": 44, "c": 0, "f": 4, "fiber": 0, "sodium": 90, "potassium": 520},
    "Wild Halibut (Baked, 6oz)": {"cals": 220, "p": 45, "c": 0, "f": 4, "fiber": 0, "sodium": 115, "potassium": 750},

    # Eggs & Dairy
    "Whole Eggs (Large, 2 Eggs)": {"cals": 140, "p": 12, "c": 1, "f": 10, "fiber": 0, "sodium": 140, "potassium": 125},
    "Liquid Egg Whites (1 Cup)": {"cals": 120, "p": 26, "c": 2, "f": 0, "fiber": 0, "sodium": 400, "potassium": 370},
    "Greek Yogurt Plain 0% (1 Cup)": {"cals": 130, "p": 23, "c": 8, "f": 0, "fiber": 0, "sodium": 85, "potassium": 320},
    "Cottage Cheese 2% (1 Cup)": {"cals": 180, "p": 24, "c": 8, "f": 5, "fiber": 0, "sodium": 700, "potassium": 220},
    "Skim Milk (1 Cup / 8 oz)": {"cals": 90, "p": 8, "c": 12, "f": 0, "fiber": 0, "sodium": 105, "potassium": 380},
    "Whole Milk (1 Cup / 8 oz)": {"cals": 150, "p": 8, "c": 12, "f": 8, "fiber": 0, "sodium": 105, "potassium": 320},
    "Cheddar Cheese (1 oz Slice)": {"cals": 115, "p": 7, "c": 1, "f": 9, "fiber": 0, "sodium": 180, "potassium": 30},

    # Plant-Based Proteins
    "Firm Tofu (1 Cup Cubed)": {"cals": 180, "p": 20, "c": 4, "f": 11, "fiber": 2, "sodium": 20, "potassium": 290},
    "Organic Tempeh (1 Cup)": {"cals": 320, "p": 31, "c": 16, "f": 18, "fiber": 7, "sodium": 15, "potassium": 680},
    "Edamame (Steamed, 1 Cup)": {"cals": 190, "p": 18, "c": 14, "f": 8, "fiber": 8, "sodium": 10, "potassium": 670},
    "Seitan / Wheat Gluten (3 oz)": {"cals": 180, "p": 31, "c": 6, "f": 2, "fiber": 1, "sodium": 300, "potassium": 100},
    "Whey Isolate Powder (1 Scoop)": {"cals": 120, "p": 25, "c": 2, "f": 1, "fiber": 0, "sodium": 130, "potassium": 160},
    "Plant Pea Protein (1 Scoop)": {"cals": 130, "p": 22, "c": 4, "f": 3, "fiber": 3, "sodium": 210, "potassium": 110},

    # Grains & Carbohydrates
    "Jasmine White Rice (Cooked, 1 Cup)": {"cals": 205, "p": 4, "c": 45, "f": 0, "fiber": 1, "sodium": 0, "potassium": 55},
    "Brown Basmati Rice (Cooked, 1 Cup)": {"cals": 215, "p": 5, "c": 45, "f": 2, "fiber": 4, "sodium": 2, "potassium": 85},
    "Rolled Oats (Dry, 1/2 Cup)": {"cals": 150, "p": 5, "c": 27, "f": 3, "fiber": 4, "sodium": 2, "potassium": 145},
    "Quinoa (Cooked, 1 Cup)": {"cals": 220, "p": 8, "c": 39, "f": 4, "fiber": 5, "sodium": 13, "potassium": 320},
    "Sweet Potato (Medium Baked)": {"cals": 103, "p": 2, "c": 24, "f": 0, "fiber": 4, "sodium": 40, "potassium": 540},
    "Russet Potato (Medium Baked)": {"cals": 160, "p": 4, "c": 37, "f": 0, "fiber": 4, "sodium": 15, "potassium": 920},
    "Whole Wheat Bread (2 Slices)": {"cals": 160, "p": 8, "c": 28, "f": 2, "fiber": 4, "sodium": 260, "potassium": 140},
    "Penne Pasta (Cooked, 1 Cup)": {"cals": 220, "p": 8, "c": 43, "f": 1, "fiber": 3, "sodium": 1, "potassium": 60},
    "Plain Bagel (1 Whole)": {"cals": 290, "p": 11, "c": 56, "f": 2, "fiber": 2, "sodium": 430, "potassium": 90},

    # Vegetables & Greens
    "Steamed Broccoli (1 Cup)": {"cals": 55, "p": 4, "c": 11, "f": 0, "fiber": 5, "sodium": 60, "potassium": 460},
    "Raw Baby Spinach (2 Cups)": {"cals": 14, "p": 2, "c": 2, "f": 0, "fiber": 2, "sodium": 45, "potassium": 330},
    "Chopped Kale (Raw, 2 Cups)": {"cals": 66, "p": 4, "c": 12, "f": 1, "fiber": 3, "sodium": 60, "potassium": 580},
    "Asparagus Spears (10 Spears)": {"cals": 30, "p": 3, "c": 5, "f": 0, "fiber": 3, "sodium": 2, "potassium": 270},
    "Grilled Zucchini (1 Cup)": {"cals": 20, "p": 1, "c": 4, "f": 0, "fiber": 1, "sodium": 10, "potassium": 320},
    "White Button Mushrooms (1 Cup)": {"cals": 16, "p": 2, "c": 2, "f": 0, "fiber": 1, "sodium": 5, "potassium": 300},

    # Fruits & Berries
    "Fresh Banana (Medium)": {"cals": 105, "p": 1, "c": 27, "f": 0, "fiber": 3, "sodium": 1, "potassium": 422},
    "Red Apple (Medium)": {"cals": 95, "p": 0, "c": 25, "f": 0, "fiber": 4, "sodium": 1, "potassium": 195},
    "Fresh Blueberries (1 Cup)": {"cals": 85, "p": 1, "c": 21, "f": 1, "fiber": 4, "sodium": 1, "potassium": 115},
    "Fresh Strawberries (1 Cup)": {"cals": 50, "p": 1, "c": 12, "f": 0, "fiber": 3, "sodium": 1, "potassium": 220},
    "Hass Avocado (1 Medium)": {"cals": 240, "p": 3, "c": 12, "f": 22, "fiber": 10, "sodium": 10, "potassium": 700},

    # Nuts & Healthy Oils
    "Raw Almonds (1 oz / 28 nuts)": {"cals": 160, "p": 6, "c": 6, "f": 14, "fiber": 4, "sodium": 0, "potassium": 200},
    "Walnut Halves (1 oz)": {"cals": 185, "p": 4, "c": 4, "f": 18, "fiber": 2, "sodium": 0, "potassium": 125},
    "Natural Peanut Butter (2 tbsp)": {"cals": 190, "p": 8, "c": 7, "f": 16, "fiber": 2, "sodium": 140, "potassium": 210},
    "Extra Virgin Olive Oil (1 tbsp)": {"cals": 120, "p": 0, "c": 0, "f": 14, "fiber": 0, "sodium": 0, "potassium": 0},
    "Chia Seeds (2 tbsp)": {"cals": 140, "p": 5, "c": 12, "f": 9, "fiber": 10, "sodium": 5, "potassium": 115}
}

# ==============================================================================
# SECTION 4: EXERCISE MET DATABASE
# ==============================================================================
EXERCISE_MET_LIBRARY = {
    "Cardio & Endurance": {
        "Running (Slow Pace, 5 mph)": 8.3,
        "Running (Moderate Pace, 6.7 mph)": 10.5,
        "Running (Vigorous Sprint, 8.5+ mph)": 13.3,
        "Outdoor Cycling (Moderate, 12-14 mph)": 6.8,
        "Outdoor Cycling (Vigorous, 16+ mph)": 10.0,
        "Rowing Machine (Moderate)": 7.0,
        "Rowing Machine (Intense)": 8.5,
        "Elliptical Machine (Moderate)": 5.0,
        "Stairmaster / Step Mill": 9.0,
        "Jumping Rope (Moderate Pace)": 11.8,
        "Brisk Walking (3.5 mph)": 3.8
    },
    "Strength & Conditioning": {
        "Bodybuilding Weightlifting (Heavy Sets)": 6.0,
        "High Intensity Circuit Training": 8.0,
        "Calisthenics (Push-ups, Pull-ups)": 5.0,
        "Powerlifting Low Rep Focus": 4.0,
        "Kettlebell Swings & Flow": 9.8,
        "CrossFit Functional WOD": 10.0
    },
    "Sports & Recreation": {
        "Basketball (Full Court Game)": 8.0,
        "Soccer Match (Competitive)": 10.0,
        "Tennis Singles Match": 7.3,
        "Swimming Laps (Moderate Freestyle)": 5.8,
        "Swimming Laps (Vigorous Butterfly/Freestyle)": 9.8,
        "Boxing Sparring / Heavy Bag": 7.8,
        "Indoor Rock Climbing": 8.0,
        "Vinyasa Power Yoga": 3.0,
        "Pilates Mat Work": 3.0
    }
}

# ==============================================================================
# SECTION 5: DYNAMIC 100+ GAMIFICATION BADGE SYSTEM
# ==============================================================================
def generate_badge_database():
    badges = {}

    # Category 1: Streaks & Consistency (15 Badges)
    streak_milestones = [1, 2, 3, 5, 7, 10, 14, 21, 30, 45, 60, 90, 100, 180, 365]
    for days in streak_milestones:
        badges[f"Streak Legend {days}D"] = {
            "desc": f"Logged activity for {days} consecutive day{'s' if days > 1 else ''}.",
            "icon": "⚡",
            "category": "Consistency"
        }

    # Category 2: Level & Experience Milestones (15 Badges)
    level_milestones = [1, 2, 3, 5, 10, 15, 20, 25, 30, 40, 50, 60, 75, 90, 100]
    for lvl in level_milestones:
        badges[f"Rank Veteran Lvl {lvl}"] = {
            "desc": f"Reached Athlete Level {lvl} by earning XP.",
            "icon": "👑",
            "category": "XP Ranks"
        }

    # Category 3: Hydration Mastery (12 Badges)
    water_milestones = [5, 8, 10, 12, 15, 20, 25, 30, 40, 50, 75, 100]
    for glasses in water_milestones:
        badges[f"Hydration Master {glasses}G"] = {
            "desc": f"Logged a single-day total of {glasses} glasses of water.",
            "icon": "💧",
            "category": "Hydration"
        }

    # Category 4: Sleep & Recovery (10 Badges)
    sleep_milestones = [6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0, 12.0]
    for hrs in sleep_milestones:
        badges[f"Sleep Guardian {hrs}h"] = {
            "desc": f"Logged {hrs} hours of restful sleep in a single night.",
            "icon": "🌙",
            "category": "Recovery"
        }

    # Category 5: Calorie Burn & Cardio Intensity (15 Badges)
    burn_milestones = [100, 250, 500, 750, 1000, 1250, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 10000]
    for burn in burn_milestones:
        badges[f"Calorie Burner {burn} kcal"] = {
            "desc": f"Burned {burn} kcal through recorded exercise activities.",
            "icon": "🔥",
            "category": "Cardio"
        }

    # Category 6: Protein Focus & Muscle Building (12 Badges)
    protein_milestones = [50, 75, 100, 120, 140, 160, 180, 200, 225, 250, 275, 300]
    for prot in protein_milestones:
        badges[f"Protein Titan {prot}g"] = {
            "desc": f"Consumed {prot} grams of protein in a single day.",
            "icon": "🥩",
            "category": "Macros"
        }

    # Category 7: Strength & Lifting Sets Logged (12 Badges)
    lifting_milestones = [1, 5, 10, 20, 30, 50, 75, 100, 150, 200, 300, 500]
    for lifts in lifting_milestones:
        badges[f"Iron Lifter {lifts} Sets"] = {
            "desc": f"Logged {lifts} total strength training set{'s' if lifts > 1 else ''}.",
            "icon": "🏋️",
            "category": "Strength"
        }

    # Category 8: Food Database Exploration (10 Badges)
    food_count_milestones = [1, 5, 10, 25, 50, 75, 100, 150, 200, 250]
    for foods in food_count_milestones:
        badges[f"Gourmet Tracker {foods} Meals"] = {
            "desc": f"Recorded {foods} total meal entries in your daily logs.",
            "icon": "🥗",
            "category": "Nutrition"
        }

    return badges

GAMIFICATION_BADGES = generate_badge_database()

MOTIVATIONAL_QUOTES = [
    "“Action is the foundational key to all success.” — Pablo Picasso",
    "“Success starts with self-discipline.” — Dwayne Johnson",
    "“The only bad workout is the one that didn't happen.”",
    "“Small daily improvements over time lead to stunning results.” — Robin Sharma",
    "“Energy flows where attention goes.” — Tony Robbins",
    "“We are what we repeatedly do. Excellence, then, is not an act, but a habit.” — Will Durant"
]

# ==============================================================================
# SECTION 6: SESSION STATE ENGINE
# ==============================================================================
raw_system_state = load_system_data()

if "user_profile" not in st.session_state:
    st.session_state.user_profile = raw_system_state.get("profile", {})
if "streak_count" not in st.session_state:
    st.session_state.streak_count = raw_system_state.get("streak_count", 1)
if "xp_points" not in st.session_state:
    st.session_state.xp_points = raw_system_state.get("xp_points", 200)
if "user_level" not in st.session_state:
    st.session_state.user_level = raw_system_state.get("user_level", 1)
if "unlocked_badges" not in st.session_state:
    st.session_state.unlocked_badges = raw_system_state.get("unlocked_badges", ["Streak Legend 1D", "Hydration Master 8G", "Rank Veteran Lvl 1"])
if "custom_recipes" not in st.session_state:
    st.session_state.custom_recipes = raw_system_state.get("custom_recipes", {})
if "strength_workouts" not in st.session_state:
    st.session_state.strength_workouts = raw_system_state.get("strength_workouts", [])
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
        "potassium_mg": 0,
        "water_glasses": 0,
        "sleep_hours": 0.0,
        "entries": []
    }

active_day = st.session_state.history_logs[current_today_key]

# ==============================================================================
# SECTION 7: BIOMETRIC COMPUTATION ENGINES
# ==============================================================================
def compute_bmi(weight_kg, height_cm):
    """Calculates BMI and returns score + classification."""
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

def compute_navy_body_fat(gender, waist_cm, neck_cm, height_cm, hip_cm=95.0):
    """Calculates US Navy Body Fat Percentage estimate."""
    try:
        if gender == "Male":
            if waist_cm <= neck_cm or height_cm <= 0:
                return 0.0
            bf = 86.010 * math.log10(waist_cm - neck_cm) - 70.041 * math.log10(height_cm) + 36.76
        else:
            if (waist_cm + hip_cm) <= neck_cm or height_cm <= 0:
                return 0.0
            bf = 163.205 * math.log10(waist_cm + hip_cm - neck_cm) - 97.684 * math.log10(height_cm) - 78.387
        return round(max(bf, 3.0), 1)
    except Exception:
        return 0.0

def compute_bmr_mifflin_st_jeor(weight_kg, height_cm, age, gender):
    """Calculates Basal Metabolic Rate using Mifflin-St Jeor formula."""
    if gender == "Male":
        return int(10 * weight_kg + 6.25 * height_cm - 5 * age + 5)
    else:
        return int(10 * weight_kg + 6.25 * height_cm - 5 * age - 161)

def compute_tdee(bmr, activity_level):
    """Multiplies BMR by activity multiplier to estimate TDEE."""
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
        
    commit_system_data()

# ==============================================================================
# SECTION 8: SIDEBAR TELEMETRY CONTROL PANEL
# ==============================================================================
with st.sidebar:
    st.title("⚡ Control Center")
    st.caption(f"Profile: **{st.session_state.user_profile.get('name', 'Athlete Pro')}**")
    
    # User Rank Progress
    st.markdown("### 🏆 Rank Telemetry")
    user_lvl = st.session_state.user_level
    user_xp = st.session_state.xp_points
    next_level_xp = user_lvl * 250
    st.write(f"**Level {user_lvl} Athlete**")
    st.progress(min(user_xp / next_level_xp, 1.0))
    st.caption(f"XP Progress: **{user_xp}** / {next_level_xp}")
    
    st.divider()
    
    # Biometrics Summary
    st.markdown("### 📐 Biometrics")
    w = st.session_state.user_profile.get("weight_kg", 76.0)
    h = st.session_state.user_profile.get("height_cm", 178.0)
    a = st.session_state.user_profile.get("age", 25)
    g = st.session_state.user_profile.get("gender", "Male")
    act = st.session_state.user_profile.get("activity_level", "Moderately Active")
    
    bmi_val, bmi_cat = compute_bmi(w, h)
    bmr_val = compute_bmr_mifflin_st_jeor(w, h, a, g)
    tdee_val = compute_tdee(bmr_val, act)
    
    st.write(f"• **BMI:** {bmi_val} ({bmi_cat})")
    st.write(f"• **BMR:** {bmr_val} kcal")
    st.write(f"• **Est. TDEE:** {tdee_val} kcal")
    
    st.divider()
    
    # Daily Active Target Overrides
    st.markdown("### 🎯 Active Goals")
    c_target = st.session_state.user_profile.get("custom_cal_goal", 2400)
    w_target = st.session_state.user_profile.get("custom_water_goal", 10)
    st.write(f"• **Calorie Goal:** {c_target} kcal")
    st.write(f"• **Water Goal:** {w_target} glasses")
    st.write(f"• **Protein Goal:** {st.session_state.user_profile.get('protein_goal_g', 165)}g")
    
    st.divider()
    
    # Inspiration Quote
    st.markdown("### 💬 Inspiration")
    st.caption(MOTIVATIONAL_QUOTES[hash(current_today_key) % len(MOTIVATIONAL_QUOTES)])
    
    st.divider()
    if st.button("🔄 Reset Today's Log", use_container_width=True, key="reset_today_btn"):
        st.session_state.history_logs[current_today_key] = {
            "calories_eaten": 0,
            "calories_burned": 0,
            "protein_g": 0,
            "carbs_g": 0,
            "fat_g": 0,
            "fiber_g": 0,
            "sodium_mg": 0,
            "potassium_mg": 0,
            "water_glasses": 0,
            "sleep_hours": 0.0,
            "entries": []
        }
        commit_system_data()
        st.toast("Today's log reset!", icon="🧹")
        st.rerun()

# ==============================================================================
# SECTION 9: APPLICATION TABS INTERFACE
# ==============================================================================
st.title("⚡ FitPulse Pro")
st.caption("Enterprise Health, Nutrition & Biometrics Analytics Suite")

app_tabs = st.tabs([
    "📊 Command Center", 
    "🍽️ Nutrition & Macros", 
    "🍳 Recipe Builder",
    "🏋️ Workout & Lifting", 
    "💧 Hydration & Sleep", 
    "🏆 Badges & Ranks",
    "📈 Analytics & History",
    "👤 Profile & Biometrics"
])

# ==============================================================================
# TAB 1: LIVE COMMAND CENTER
# ==============================================================================
with app_tabs[0]:
    st.markdown("<div class='section-header'>🔥 Real-Time Dashboard</div>", unsafe_allow_html=True)
    
    c_eaten = active_day["calories_eaten"]
    c_burned = active_day["calories_burned"]
    net_cals = c_eaten - c_burned
    target_cals = st.session_state.user_profile.get("custom_cal_goal", 2400)
    target_water = st.session_state.user_profile.get("custom_water_goal", 10)
    remaining_cals = target_cals - net_cals

    # Primary Cards
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    m_col1.metric("Calories Consumed", f"{c_eaten} kcal", delta="Food Intake")
    m_col2.metric("Active Calorie Burn", f"{c_burned} kcal", delta="Workouts", delta_color="inverse")
    m_col3.metric("Net Calorie Balance", f"{net_cals} kcal", delta=f"{remaining_cals} remaining" if remaining_cals >= 0 else f"{abs(remaining_cals)} over limit")
    m_col4.metric("Hydration Intake", f"{active_day['water_glasses']} / {target_water} 💧")

    st.write("---")

    # Progress Bars
    pr_col1, pr_col2 = st.columns(2)
    
    with pr_col1:
        with st.container(border=True):
            st.markdown("<div class='sub-header'>🎯 Daily Calorie Progress</div>", unsafe_allow_html=True)
            cal_ratio = min(c_eaten / target_cals, 1.0) if target_cals > 0 else 0.0
            st.progress(cal_ratio)
            st.caption(f"**{int(cal_ratio * 100)}%** reached of **{target_cals} kcal** target.")

    with pr_col2:
        with st.container(border=True):
            st.markdown("<div class='sub-header'>💧 Hydration Goal Tracker</div>", unsafe_allow_html=True)
            w_ratio = min(active_day["water_glasses"] / target_water, 1.0) if target_water > 0 else 0.0
            st.progress(w_ratio)
            st.caption(f"Logged **{active_day['water_glasses']}** of **{target_water}** daily target glasses.")

    st.write("---")

    # Macro Overview Cards
    st.markdown("<div class='section-header'>🥗 Macronutrient Telemetry</div>", unsafe_allow_html=True)
    mac1, mac2, mac3, mac4, mac5 = st.columns(5)
    
    prot_target = st.session_state.user_profile.get("protein_goal_g", 165)
    carb_target = st.session_state.user_profile.get("carbs_goal_g", 270)
    fat_target = st.session_state.user_profile.get("fat_goal_g", 70)
    fiber_target = st.session_state.user_profile.get("fiber_goal_g", 32)
    sodium_target = st.session_state.user_profile.get("sodium_goal_mg", 2300)

    mac1.metric("Protein", f"{active_day['protein_g']}g / {prot_target}g")
    mac2.metric("Carbohydrates", f"{active_day['carbs_g']}g / {carb_target}g")
    mac3.metric("Fats", f"{active_day['fat_g']}g / {fat_target}g")
    mac4.metric("Dietary Fiber", f"{active_day['fiber_g']}g / {fiber_target}g")
    mac5.metric("Sodium", f"{active_day['sodium_mg']}mg / {sodium_target}mg")

    st.write("---")

    # Lower Section Visualizations
    chart_col, timeline_col = st.columns([2, 1])
    
    with chart_col:
        st.subheader("📈 Energy Balance Chart")
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
    st.markdown("<div class='section-header'>🍽️ Meal & Nutrition Logger</div>", unsafe_allow_html=True)
    
    entry_method = st.radio("Choose Entry Method:", ["Standard Database Search", "Custom Manual Entry", "Saved Recipes"], horizontal=True, key="entry_method_radio")
    
    log_col1, log_col2 = st.columns([2, 1])
    
    with log_col1:
        if entry_method == "Standard Database Search":
            with st.container(border=True):
                st.markdown("<div class='sub-header'>🔎 Search Food Library</div>", unsafe_allow_html=True)
                selected_food = st.selectbox("Select Item:", list(FOOD_LIBRARY.keys()), key="select_food_library")
                serving_qty = st.number_input("Serving Multiplier:", min_value=0.25, max_value=10.0, value=1.0, step=0.25, key="food_serving_qty")
                
                f_data = FOOD_LIBRARY[selected_food]
                calc_cals = int(f_data["cals"] * serving_qty)
                calc_p = int(f_data["p"] * serving_qty)
                calc_c = int(f_data["c"] * serving_qty)
                calc_f = int(f_data["f"] * serving_qty)
                calc_fib = int(f_data["fiber"] * serving_qty)
                calc_sod = int(f_data["sodium"] * serving_qty)
                calc_pot = int(f_data.get("potassium", 0) * serving_qty)
                
                st.caption(f"Calculated Macros: **{calc_cals} kcal** | P: {calc_p}g | C: {calc_c}g | F: {calc_f}g | Fiber: {calc_fib}g | Sodium: {calc_sod}mg | Potassium: {calc_pot}mg")
                
                if st.button("➕ Log Selected Food", use_container_width=True, key="btn_log_selected_food"):
                    active_day["calories_eaten"] += calc_cals
                    active_day["protein_g"] += calc_p
                    active_day["carbs_g"] += calc_c
                    active_day["fat_g"] += calc_f
                    active_day["fiber_g"] += calc_fib
                    active_day["sodium_mg"] += calc_sod
                    active_day["potassium_mg"] += calc_pot
                    
                    log_text = f"Logged: {selected_food} (x{serving_qty}) - {calc_cals} kcal"
                    active_day["entries"].append(log_text)
                    
                    grant_user_xp(15, "Logged Food")
                    st.toast(f"Logged {selected_food}!", icon="🥗")
                    st.rerun()

        elif entry_method == "Custom Manual Entry":
            with st.container(border=True):
                st.markdown("<div class='sub-header'>✏️ Manual Food Entry</div>", unsafe_allow_html=True)
                c_meal_name = st.text_input("Meal / Item Name:", placeholder="e.g. Protein Smoothie", key="custom_meal_name_input")
                
                cc1, cc2, cc3 = st.columns(3)
                with cc1:
                    c_cals = st.number_input("Calories (kcal):", min_value=0, step=10, value=300, key="custom_cals_input")
                    c_prot = st.number_input("Protein (g):", min_value=0, step=1, value=25, key="custom_prot_input")
                with cc2:
                    c_carbs = st.number_input("Carbohydrates (g):", min_value=0, step=1, value=35, key="custom_carbs_input")
                    c_fats = st.number_input("Fats (g):", min_value=0, step=1, value=8, key="custom_fats_input")
                with cc3:
                    c_fiber = st.number_input("Fiber (g):", min_value=0, step=1, value=5, key="custom_fiber_input")
                    c_sod = st.number_input("Sodium (mg):", min_value=0, step=10, value=200, key="custom_sod_input")
                    
                if st.button("➕ Log Custom Entry", use_container_width=True, key="btn_log_custom_entry"):
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
                        st.warning("Please provide an item name!")

        else:
            with st.container(border=True):
                st.markdown("<div class='sub-header'>📖 Saved Custom Recipes</div>", unsafe_allow_html=True)
                if st.session_state.custom_recipes:
                    chosen_recipe = st.selectbox("Select Recipe:", list(st.session_state.custom_recipes.keys()), key="select_custom_recipe")
                    recipe_data = st.session_state.custom_recipes[chosen_recipe]
                    
                    st.caption(f"Recipe Totals: **{recipe_data['cals']} kcal** | P: {recipe_data['p']}g | C: {recipe_data['c']}g | F: {recipe_data['f']}g")
                    
                    if st.button("➕ Log Recipe to Daily Feed", use_container_width=True, key="btn_log_recipe"):
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
                    st.info("No saved recipes yet. Create one in the 'Recipe Builder' tab!")

    with log_col2:
        with st.container(border=True):
            st.markdown("<div class='sub-header'>📊 Today's Micronutrient Summary</div>", unsafe_allow_html=True)
            
            summary_table = pd.DataFrame({
                "Nutrient": ["Protein", "Carbs", "Fats", "Fiber", "Sodium", "Potassium"],
                "Amount": [
                    f"{active_day['protein_g']} g",
                    f"{active_day['carbs_g']} g",
                    f"{active_day['fat_g']} g",
                    f"{active_day['fiber_g']} g",
                    f"{active_day['sodium_mg']} mg",
                    f"{active_day.get('potassium_mg', 0)} mg"
                ]
            })
            st.dataframe(summary_table, use_container_width=True, hide_index=True)

# ==============================================================================
# TAB 3: CUSTOM RECIPE BUILDER
# ==============================================================================
with app_tabs[2]:
    st.markdown("<div class='section-header'>🍳 Custom Recipe & Meal Prep Builder</div>", unsafe_allow_html=True)
    st.caption("Combine ingredients to automatically generate macros and store reusable custom meals.")
    
    rb_col1, rb_col2 = st.columns([2, 1])
    
    with rb_col1:
        with st.container(border=True):
            st.markdown("<div class='sub-header'>🛠️ Create New Recipe</div>", unsafe_allow_html=True)
            recipe_title = st.text_input("Recipe Title:", placeholder="e.g. Chicken & Rice Prep Bowl", key="recipe_title_input")
            
            num_ingredients = st.number_input("Number of Ingredients:", min_value=1, max_value=8, value=3, step=1, key="num_ingredients_input")
            
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
            
            if st.button("💾 Save Recipe to Library", use_container_width=True, key="btn_save_recipe"):
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
                    st.warning("Please provide a title for your recipe!")

    with rb_col2:
        with st.container(border=True):
            st.markdown("<div class='sub-header'>📚 Saved Recipe Library</div>", unsafe_allow_html=True)
            if st.session_state.custom_recipes:
                for r_name, r_info in st.session_state.custom_recipes.items():
                    with st.expander(r_name):
                        st.write(f"**Calories:** {r_info['cals']} kcal")
                        st.write(f"**Macros:** P: {r_info['p']}g | C: {r_info['c']}g | F: {r_info['f']}g")
                        st.write("**Ingredients:**")
                        for ing in r_info["ingredients"]:
                            st.write(f"• {ing}")
            else:
                st.caption("No custom recipes stored yet.")

# ==============================================================================
# TAB 4: WORKOUT & STRENGTH LOGGING
# ==============================================================================
with app_tabs[3]:
    st.markdown("<div class='section-header'>🏋️ Workout Studio & Strength Log</div>", unsafe_allow_html=True)
    
    workout_mode = st.radio("Select Mode:", ["MET Calorie Burn Calculator", "Strength Set & Rep Logger"], horizontal=True, key="workout_mode_radio")
    
    if workout_mode == "MET Calorie Burn Calculator":
        ex_category = st.selectbox("Category:", list(EXERCISE_MET_LIBRARY.keys()), key="met_category_select")
        
        w_col1, w_col2 = st.columns(2)
        
        with w_col1:
            with st.container(border=True):
                st.markdown("<div class='sub-header'>⚡ MET Calorie Calculator</div>", unsafe_allow_html=True)
                selected_ex = st.selectbox("Activity:", list(EXERCISE_MET_LIBRARY[ex_category].keys()), key="met_activity_select")
                duration_minutes = st.number_input("Duration (Minutes):", min_value=5, max_value=300, value=30, step=5, key="met_duration_input")
                
                u_weight = st.session_state.user_profile.get("weight_kg", 76.0)
                met_value = EXERCISE_MET_LIBRARY[ex_category][selected_ex]
                
                est_burn = int((met_value * 3.5 * u_weight / 200) * duration_minutes)
                
                st.info(f"🔥 Estimated Energy Burn: **{est_burn} kcal** ({duration_minutes} mins)")
                
                if st.button("🔥 Log Calorie Burn", use_container_width=True, key="btn_log_met_burn"):
                    active_day["calories_burned"] += est_burn
                    entry_log_msg = f"Workout ({ex_category}): {selected_ex} ({duration_minutes} mins) - {est_burn} kcal"
                    active_day["entries"].append(entry_log_msg)
                    
                    grant_user_xp(30, "Logged Exercise")
                    st.toast(f"Logged {selected_ex}!", icon="🏃")
                    st.rerun()

        with w_col2:
            with st.container(border=True):
                st.markdown("<div class='sub-header'>✏️ Manual Calorie Burn</div>", unsafe_allow_html=True)
                custom_ex_name = st.text_input("Workout Title:", placeholder="e.g. Heavy Deadlifts", key="custom_ex_name_input")
                custom_ex_burn = st.number_input("Calories Burned (kcal):", min_value=0, step=25, value=200, key="custom_ex_burn_input")
                
                if st.button("🔥 Log Manual Burn", use_container_width=True, key="btn_log_manual_burn"):
                    if custom_ex_burn > 0:
                        active_day["calories_burned"] += custom_ex_burn
                        label = custom_ex_name if custom_ex_name.strip() else "Workout"
                        entry_log_msg = f"Workout: {label} - {custom_ex_burn} kcal"
                        active_day["entries"].append(entry_log_msg)
                        
                        grant_user_xp(25, "Logged Manual Workout")
                        st.toast(f"Logged {label}!", icon="🔥")
                        st.rerun()

    else:
        st.markdown("### 📝 Log Sets, Reps & Weight")
        s_col1, s_col2 = st.columns([2, 1])
        
        with s_col1:
            with st.container(border=True):
                exercise_title = st.text_input("Lift Name:", placeholder="e.g. Barbell Bench Press", key="lift_title_input")
                sets_count = st.number_input("Sets:", min_value=1, max_value=10, value=3, key="lift_sets_input")
                reps_count = st.number_input("Reps:", min_value=1, max_value=50, value=10, key="lift_reps_input")
                weight_lifted = st.number_input("Weight (kg):", min_value=0.0, max_value=500.0, value=60.0, step=2.5, key="lift_weight_input")
                
                if st.button("🏋️ Save Strength Entry", use_container_width=True, key="btn_save_strength_entry"):
                    if exercise_title.strip():
                        lift_entry = {
                            "date": current_today_key,
                            "exercise": exercise_title,
                            "sets": sets_count,
                            "reps": reps_count,
                            "weight": weight_lifted
                        }
                        st.session_state.strength_workouts.append(lift_entry)
                        
                        active_day["entries"].append(f"Strength Lifted: {exercise_title} - {sets_count}x{reps_count} @ {weight_lifted}kg")
                        
                        grant_user_xp(35, "Logged Lifting Set")
                        st.toast(f"Logged {exercise_title}!", icon="🏋️")
                        st.rerun()

        with s_col2:
            with st.container(border=True):
                st.markdown("<div class='sub-header'>📋 Lift History</div>", unsafe_allow_html=True)
                if st.session_state.strength_workouts:
                    st_df = pd.DataFrame(st.session_state.strength_workouts)
                    st.dataframe(st_df[["date", "exercise", "sets", "reps", "weight"]], use_container_width=True, hide_index=True)
                else:
                    st.caption("No strength workouts recorded yet.")

# ==============================================================================
# TAB 5: HYDRATION & SLEEP RECOVERY
# ==============================================================================
with app_tabs[4]:
    st.markdown("<div class='section-header'>💧 Hydration & Recovery Monitor</div>", unsafe_allow_html=True)
    
    wat_col1, wat_col2 = st.columns(2)
    
    with wat_col1:
        with st.container(border=True):
            st.markdown("<div class='sub-header'>🥤 Fluid Intake Monitor</div>", unsafe_allow_html=True)
            st.markdown(f"## **{active_day['water_glasses']}** Glasses Logged Today")
            
            b1, b2 = st.columns(2)
            with b1:
                if st.button("🥤 +1 Glass (250 ml)", use_container_width=True, key="btn_add_1_water"):
                    active_day["water_glasses"] += 1
                    active_day["entries"].append("💧 Drank 1 glass of water (250 ml)")
                    grant_user_xp(5, "Water Intake")
                    commit_system_data()
                    st.rerun()
            with b2:
                if st.button("🥤 +2 Glasses (500 ml)", use_container_width=True, key="btn_add_2_water"):
                    active_day["water_glasses"] += 2
                    active_day["entries"].append("💧 Drank 2 glasses of water (500 ml)")
                    grant_user_xp(10, "Water Intake")
                    commit_system_data()
                    st.rerun()
                    
            if st.button("➖ Remove 1 Glass", use_container_width=True, key="btn_sub_1_water"):
                if active_day["water_glasses"] > 0:
                    active_day["water_glasses"] -= 1
                    commit_system_data()
                    st.rerun()

    with wat_col2:
        with st.container(border=True):
            st.markdown("<div class='sub-header'>🌙 Sleep Recovery Tracker</div>", unsafe_allow_html=True)
            st.markdown(f"## **{active_day.get('sleep_hours', 0.0)}** Hours Recorded")
            
            sleep_input = st.number_input("Log Sleep Duration (Hours):", min_value=0.0, max_value=16.0, value=7.5, step=0.5, key="sleep_hours_input")
            
            if st.button("🌙 Record Sleep", use_container_width=True, key="btn_record_sleep"):
                active_day["sleep_hours"] = sleep_input
                active_day["entries"].append(f"🌙 Slept for {sleep_input} hours")
                
                grant_user_xp(20, "Logged Sleep")
                commit_system_data()
                st.toast("Sleep telemetry updated!", icon="😴")
                st.rerun()

# ==============================================================================
# TAB 6: GAMIFICATION & 100+ BADGES SHOWCASE
# ==============================================================================
with app_tabs[5]:
    st.markdown("<div class='section-header'>🏆 Ranks & Achievements</div>", unsafe_allow_html=True)
    
    g_col1, g_col2 = st.columns([1, 3])
    
    with g_col1:
        with st.container(border=True):
            st.markdown("<div class='sub-header'>👑 Rank Telemetry</div>", unsafe_allow_html=True)
            st.write(f"**Level {st.session_state.user_level} Athlete**")
            st.write(f"**Total XP:** {st.session_state.xp_points}")
            st.write(f"**Current Streak:** {st.session_state.streak_count} Days ⚡")
            
            unlocked_cnt = len(st.session_state.unlocked_badges)
            total_cnt = len(GAMIFICATION_BADGES)
            st.write(f"**Badges Unlocked:** {unlocked_cnt} / {total_cnt}")
            st.progress(min(unlocked_cnt / total_cnt, 1.0))

    with g_col2:
        st.markdown("### 🏅 Achievements Showcase (100+ Badges)")
        
        # Category Filter Bar
        categories = ["All"] + sorted(list(set(b["category"] for b in GAMIFICATION_BADGES.values())))
        selected_cat = st.selectbox("Filter Badges by Category:", categories, key="badge_category_filter")
        
        search_query = st.text_input("🔎 Search Badges:", placeholder="e.g. 100 kcal, Hydration, Streak", key="badge_search_input")
        
        # Filter Logic
        filtered_badges = {}
        for b_name, b_data in GAMIFICATION_BADGES.items():
            matches_cat = (selected_cat == "All") or (b_data["category"] == selected_cat)
            matches_search = (search_query.lower() in b_name.lower()) or (search_query.lower() in b_data["desc"].lower())
            if matches_cat and matches_search:
                filtered_badges[b_name] = b_data

        st.caption(f"Showing **{len(filtered_badges)}** badges")
        
        # Render Badges in 3 Grid Columns
        badge_cols = st.columns(3)
        for idx, (b_title, b_info) in enumerate(filtered_badges.items()):
            col_target = badge_cols[idx % 3]
            is_unlocked = b_title in st.session_state.unlocked_badges
            
            with col_target:
                if is_unlocked:
                    st.markdown(f"""
                        <div class='badge-card-unlocked'>
                            <h4>{b_info['icon']} {b_title}</h4>
                            <p style='font-size:0.85rem;'>{b_info['desc']}</p>
                            <small><b>✅ UNLOCKED</b></small>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                        <div class='badge-card'>
                            <h4>🔒 {b_title}</h4>
                            <p style='font-size:0.85rem; color:#888;'>{b_info['desc']}</p>
                            <small style='color:#666;'>LOCKED</small>
                        </div>
                    """, unsafe_allow_html=True)

# ==============================================================================
# TAB 7: ADVANCED ANALYTICS & HISTORY
# ==============================================================================
with app_tabs[6]:
    st.markdown("<div class='section-header'>📈 Analytics & Historical Trends</div>", unsafe_allow_html=True)
    
    trend_dates = [(datetime.date.today() - datetime.timedelta(days=i)).strftime("%a %d") for i in range(6, -1, -1)]
    
    analytics_df = pd.DataFrame({
        "Day": trend_dates,
        "Calories Consumed": [2150, 2300, 1950, 2400, 2100, 2250, active_day["calories_eaten"]],
        "Calories Burned": [350, 420, 280, 510, 320, 480, active_day["calories_burned"]],
        "Water Glasses": [8, 9, 7, 10, 8, 9, active_day["water_glasses"]],
        "Sleep Hours": [7.5, 8.0, 6.5, 8.5, 7.0, 8.0, active_day.get("sleep_hours", 7.0)]
    })
    
    st.line_chart(analytics_df, x="Day", y=["Calories Consumed", "Calories Burned"])
    
    c_chart1, c_chart2 = st.columns(2)
    with c_chart1:
        st.caption("Daily Hydration Intake (Glasses)")
        st.bar_chart(analytics_df, x="Day", y="Water Glasses")
    with c_chart2:
        st.caption("Daily Sleep Duration (Hours)")
        st.bar_chart(analytics_df, x="Day", y="Sleep Hours")
    
    st.divider()
    
    st.markdown("### 📄 Export Data")
    csv_bytes = analytics_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Telemetry Report (CSV)",
        data=csv_bytes,
        file_name="fitpulse_analytics_report.csv",
        mime="text/csv",
        use_container_width=True,
        key="btn_download_csv"
    )

# ==============================================================================
# TAB 8: USER PROFILE & GOALS ENGINE
# ==============================================================================
with app_tabs[7]:
    st.markdown("<div class='section-header'>👤 Profile, Biometrics & Target Configuration</div>", unsafe_allow_html=True)
    
    p_data = st.session_state.user_profile
    
    with st.form("profile_configuration_form"):
        pf_col1, pf_col2 = st.columns(2)
        
        with pf_col1:
            st.markdown("<div class='sub-header'>📋 Personal Details</div>", unsafe_allow_html=True)
            in_name = st.text_input("Name:", value=p_data.get("name", "Athlete Pro"), key="profile_name_input")
            in_age = st.number_input("Age:", min_value=12, max_value=100, value=p_data.get("age", 25), key="profile_age_input")
            in_gender = st.selectbox("Gender:", ["Male", "Female"], index=0 if p_data.get("gender") == "Male" else 1, key="profile_gender_select")
            in_weight = st.number_input("Weight (kg):", min_value=30.0, max_value=250.0, value=p_data.get("weight_kg", 76.0), step=0.5, key="profile_weight_input")
            in_height = st.number_input("Height (cm):", min_value=100.0, max_value=230.0, value=p_data.get("height_cm", 178.0), step=1.0, key="profile_height_input")
            in_activity = st.selectbox("Activity Level:", ["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extra Active"], index=2, key="profile_activity_select")
            
        with pf_col2:
            st.markdown("<div class='sub-header'>🎯 Daily Targets</div>", unsafe_allow_html=True)
            in_cal_goal = st.number_input("Calorie Goal (kcal):", min_value=1000, max_value=6000, value=p_data.get("custom_cal_goal", 2400), step=50, key="profile_cal_goal_input")
            in_water_goal = st.number_input("Water Goal (Glasses):", min_value=4, max_value=25, value=p_data.get("custom_water_goal", 10), step=1, key="profile_water_goal_input")
            in_prot_goal = st.number_input("Protein Goal (g):", min_value=20, max_value=400, value=p_data.get("protein_goal_g", 165), step=5, key="profile_prot_goal_input")
            in_carb_goal = st.number_input("Carbs Goal (g):", min_value=20, max_value=600, value=p_data.get("carbs_goal_g", 270), step=5, key="profile_carb_goal_input")
            in_fat_goal = st.number_input("Fat Goal (g):", min_value=10, max_value=200, value=p_data.get("fat_goal_g", 70), step=5, key="profile_fat_goal_input")
            in_fiber_goal = st.number_input("Fiber Goal (g):", min_value=10, max_value=100, value=p_data.get("fiber_goal_g", 32), step=2, key="profile_fiber_goal_input")
            
        st.markdown("<div class='sub-header'>📏 Circumference Measurements (Navy Body Fat Calculator)</div>", unsafe_allow_html=True)
        m_c1, m_c2, m_c3 = st.columns(3)
        with m_c1:
            in_neck = st.number_input("Neck Circumference (cm):", min_value=20.0, max_value=70.0, value=p_data.get("neck_cm", 38.0), step=0.5, key="profile_neck_input")
        with m_c2:
            in_waist = st.number_input("Waist Circumference (cm):", min_value=40.0, max_value=200.0, value=p_data.get("waist_cm", 81.0), step=0.5, key="profile_waist_input")
        with m_c3:
            in_hip = st.number_input("Hip Circumference (cm - Females):", min_value=40.0, max_value=200.0, value=p_data.get("hip_cm", 95.0), step=0.5, key="profile_hip_input")

        save_btn = st.form_submit_button("💾 Save Profile Configuration", use_container_width=True)
        
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
                "sodium_goal_mg": p_data.get("sodium_goal_mg", 2300),
                "potassium_goal_mg": p_data.get("potassium_goal_mg", 3500),
                "neck_cm": in_neck,
                "waist_cm": in_waist,
                "hip_cm": in_hip
            }
            commit_system_data()
            st.toast("Profile settings updated!", icon="✅")
            st.rerun()

    navy_bf = compute_navy_body_fat(
        st.session_state.user_profile.get("gender", "Male"),
        st.session_state.user_profile.get("waist_cm", 81.0),
        st.session_state.user_profile.get("neck_cm", 38.0),
        st.session_state.user_profile.get("height_cm", 178.0),
        st.session_state.user_profile.get("hip_cm", 95.0)
    )
    st.info(f"📊 **US Navy Estimated Body Fat Percentage:** {navy_bf}%")

# ==============================================================================
# SECTION 10: AUTO-PERSISTENCE
# ==============================================================================
commit_system_data()
import sqlite3
from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)
DB_NAME = 'tracker.db'

# Initialize database and create table if it doesn't exist
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            activity TEXT NOT NULL,
            calories INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fitness & Calorie Tracker</title>
    <style>
        * { box-sizing: border-box; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 0; }
        body { background-color: #0f172a; color: #f8fafc; display: flex; justify-content: center; padding: 40px 20px; }
        .container { width: 100%; max-width: 500px; background: #1e293b; padding: 30px; border-radius: 16px; box-shadow: 0 10px 25px rgba(0,0,0,0.3); }
        h1 { text-align: center; font-size: 1.8rem; margin-bottom: 20px; color: #38bdf8; }
        .stat-card { background: #334155; padding: 15px; border-radius: 12px; text-align: center; margin-bottom: 25px; }
        .stat-card h2 { font-size: 2rem; color: #4ade80; }
        form { display: flex; flex-direction: column; gap: 12px; margin-bottom: 25px; }
        input { padding: 12px; border-radius: 8px; border: 1px solid #475569; background: #0f172a; color: #fff; font-size: 1rem; }
        input:focus { outline: none; border-color: #38bdf8; }
        button { padding: 12px; border-radius: 8px; border: none; background: #38bdf8; color: #0f172a; font-weight: bold; font-size: 1rem; cursor: pointer; transition: 0.2s; }
        button:hover { background: #7dd3fc; }
        ul { list-style: none; display: flex; flex-direction: column; gap: 10px; }
        li { background: #334155; padding: 12px 16px; border-radius: 8px; display: flex; justify-content: space-between; align-items: center; }
        .calories-eaten { color: #f87171; font-weight: bold; }
        .calories-burned { color: #4ade80; font-weight: bold; }
        .delete-btn { color: #94a3b8; text-decoration: none; font-size: 0.8rem; margin-left: 10px; }
        .delete-btn:hover { color: #f87171; }
    </style>
</head>
<body>
    <div class="container">
        <h1>⚡ Calorie Tracker</h1>
        
        <div class="stat-card">
            <p style="font-size: 0.9rem; color: #94a3b8;">Net Calories</p>
            <h2>{{ total_calories }} kcal</h2>
        </div>

        <form action="/add" method="POST">
            <input type="text" name="activity" placeholder="Activity or Food (e.g. Apple, Running)" required>
            <input type="number" name="calories" placeholder="Calories (+ for food, - for exercise)" required>
            <button type="submit">Add Log</button>
        </form>

        <h3>Activity Log</h3>
        <br>
        <ul>
            {% for item in logs %}
                <li>
                    <span>{{ item[1] }}</span>
                    <div>
                        <span class="{{ 'calories-eaten' if item[2] > 0 else 'calories-burned' }}">
                            {{ '+' if item[2] > 0 else '' }}{{ item[2] }} kcal
                        </span>
                        <a href="/delete/{{ item[0] }}" class="delete-btn">✕</a>
                    </div>
                </li>
            {% else %}
                <p style="color: #64748b; text-align: center;">No logs saved yet.</p>
            {% endfor %}
        </ul>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT id, activity, calories FROM logs')
    logs = cursor.fetchall()
    conn.close()

    total_calories = sum(item[2] for item in logs)
    return render_template_string(HTML_TEMPLATE, logs=logs, total_calories=total_calories)

@app.route('/add', methods=['POST'])
def add():
    activity = request.form.get('activity')
    try:
        calories = int(request.form.get('calories'))
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO logs (activity, calories) VALUES (?, ?)', (activity, calories))
        conn.commit()
        conn.close()
    except ValueError:
        pass
    return redirect(url_for('home'))

@app.route('/delete/<int:log_id>')
def delete(log_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM logs WHERE id = ?', (log_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
    
