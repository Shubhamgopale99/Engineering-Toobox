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

# Initialize history
if "history" not in st.session_state:
    st.session_state.history = []

# Input fields (blank by default)
col1, col2, col3 = st.columns(3)
with col1:
    tube_dia_mm = st.text_input("Tube Diameter (mm)", value="")
with col2:
    tube_length_m = st.text_input("Tube Length (m)", value="")
with col3:
    no_of_tubes = st.text_input("Number of Tubes", value="")

# Action buttons
colA, colB, colC = st.columns([1,1,2])
with colA:
    calculate_btn = st.button("Calculate")
with colB:
    reset_btn = st.button("Reset Inputs")

# -------------------- Reset functionality --------------------
if reset_btn:
    st.experimental_rerun()  # clears inputs, but keeps history

# -------------------- Calculation --------------------
if calculate_btn:
    if not tube_dia_mm or not tube_length_m or not no_of_tubes:
        st.warning(random.choice(humor_error))
    else:
        try:
            tube_dia_mm = float(tube_dia_mm)
            tube_length_m = float(tube_length_m)
            no_of_tubes = int(no_of_tubes)

            result = (math.pi * tube_dia_mm * tube_length_m * no_of_tubes) / 1000

            st.success(
                f"✅ Heat Transfer Area = **{result:.3f} m²**\n\n"
                + random.choice(humor_success)
            )

            # Save in history
            st.session_state.history.append({
                "Tube Diameter (mm)": tube_dia_mm,
                "Tube Length (m)": tube_length_m,
                "No. of Tubes": no_of_tubes,
                "Heat Transfer Area (m²)": round(result, 3)
            })

        except ValueError:
            st.error("⚠️ Please enter valid numbers only!")

# -------------------- History Table --------------------
if st.session_state.history:
    st.subheader("📜 Calculation History")
    df = pd.DataFrame(st.session_state.history)
    st.dataframe(df, use_container_width=True)

    # Download button
    #csv = df.to_csv(index=False).encode("utf-8")
    #st.download_button(
    #    "📥 Download History as CSV",
    #    data=csv,
    #    file_name="tube_heat_transfer_history.csv",
    #    mime="text/csv"
    #)
