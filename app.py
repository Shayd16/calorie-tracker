import streamlit as st

st.title("🏋️ Calorie & Exercise Tracker")

# Sidebar navigation
menu = st.sidebar.selectbox("Choose a Feature", ["Log Activity", "View Summary"])

# Initialize storage in session
if "calories_burned" not in st.session_state:
    st.session_state.calories_burned = 0
if "calories_eaten" not in st.session_state:
    st.session_state.calories_eaten = 0

if menu == "Log Activity":
    st.header("Log Your Day")
    
    # Food Input
    st.subheader("Add Food")
    food_cals = st.number_input("Calories Consumed", min_value=0, step=50)
    if st.button("Add Calories"):
        st.session_state.calories_eaten += food_cals
        st.success(f"Added {food_cals} calories!")

    st.divider()

    # Exercise Input
    st.subheader("Add Exercise")
    workout_cals = st.number_input("Calories Burned", min_value=0, step=50)
    if st.button("Log Workout"):
        st.session_state.calories_burned += workout_cals
        st.success(f"Logged {workout_cals} burned calories!")

elif menu == "View Summary":
    st.header("Daily Summary")
    
    net = st.session_state.calories_eaten - st.session_state.calories_burned
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Eaten", f"{st.session_state.calories_eaten} kcal")
    col2.metric("Burned", f"{st.session_state.calories_burned} kcal")
    col3.metric("Net Total", f"{net} kcal")
