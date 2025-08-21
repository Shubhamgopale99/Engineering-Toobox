import streamlit as st
import math
import pandas as pd
import random

# -------------------- Humor messages --------------------
humor_success = [
    "🎉 Congrats! You just made the tubes proud.",
    "🔥 Hot stuff! Your calculation is sizzling.",
    "💡 Did you know? Tubes also dream of surface area.",
    "🚀 You just launched a rocket in the heat transfer universe!"
]

humor_error = [
    "😜 Oops! Even Einstein needed numbers, not blanks!",
    "🙈 Empty inputs? Looks like the tubes went on vacation.",
    "⚠️ Numbers missing… Maybe your keyboard is shy?",
    "😂 Try again, tubes can’t handle ghosts of missing data!"
]

# -------------------- Streamlit UI --------------------
st.set_page_config(page_title="Tube Heat Transfer Area Calculator", layout="wide")

st.title("🔧 Tube Heat Transfer Area Calculator")

# -------------------- Session State --------------------
if "heat_exchanger_area_history" not in st.session_state:
    st.session_state.heat_exchanger_area_history = []   # quick list history

if "heat_exchanger_area_detailed_history" not in st.session_state:
    st.session_state.heat_exchanger_area_detailed_history = []   # detailed history with inputs

# -------------------- Inputs --------------------
col1, col2, col3 = st.columns(3)
with col1:
    tube_dia_mm = st.text_input("Tube Diameter (mm)", value="", key="tube_dia_input")
with col2:
    tube_length_m = st.text_input("Tube Length (m)", value="", key="tube_length_input")
with col3:
    no_of_tubes = st.text_input("Number of Tubes", value="", key="tube_count_input")

# Action buttons
colA, colB = st.columns([1,1])
with colA:
    calculate_btn = st.button("🔢 Calculate Heat Exchanger Area")
with colB:
    reset_btn = st.button("♻️ Reset Inputs")

# -------------------- Reset functionality --------------------
if reset_btn:
    st.session_state.tube_dia_input = ""
    st.session_state.tube_length_input = ""
    st.session_state.tube_count_input = ""

# -------------------- Calculation --------------------
if calculate_btn:
    if not tube_dia_mm or not tube_length_m or not no_of_tubes:
        st.warning(random.choice(humor_error))
    else:
        try:
            tube_dia_mm = float(tube_dia_mm)
            tube_length_m = float(tube_length_m)
            no_of_tubes = int(no_of_tubes)

            # Formula: π * d * L * N / 1000 (to convert mm·m → m²)
            result = (math.pi * tube_dia_mm * tube_length_m * no_of_tubes) / 1000

            st.success(
                f"✅ Heat Transfer Area = **{result:.3f} m²**\n\n"
                + random.choice(humor_success)
            )

            # Save in detailed history
            st.session_state.heat_exchanger_area_detailed_history.append({
                "Tube Diameter (mm)": tube_dia_mm,
                "Tube Length (m)": tube_length_m,
                "No. of Tubes": no_of_tubes,
                "Heat Transfer Area (m²)": round(result, 3)
            })

            # Save in quick history
            st.session_state.heat_exchanger_area_history.append(round(result, 3))

        except ValueError:
            st.error("⚠️ Please enter valid numbers only!")

# -------------------- Histories --------------------
if st.session_state.heat_exchanger_area_detailed_history:
    st.subheader("📜 Detailed Heat Exchanger Area History")
    df = pd.DataFrame(st.session_state.heat_exchanger_area_detailed_history)
    st.dataframe(df, use_container_width=True)

if st.session_state.heat_exchanger_area_history:
    st.subheader("📜 Quick Heat Exchanger Area History")
    st.write(st.session_state.heat_exchanger_area_history)
