import streamlit as st
import pandas as pd
import math
import random

st.set_page_config(page_title="RF Pad Arc Length Calculator", layout="wide")

# ---------------- Humor bank ----------------
success_jokes = [
    "📏 Arc calculated! Even geometry teachers would be proud.",
    "✅ Numbers done! That RF pad won’t escape you.",
    "⚙️ Arc length ready – now your shell feels complete.",
    "📐 Coil arcs and math sparks – calculation successful!"
]

error_jokes = [
    "🤔 Missing inputs? That’s like ordering pizza without cheese!",
    "⚠️ Enter the values please… shells don’t read minds.",
    "😂 Forgot to fill inputs? Even arcs need numbers to bend.",
    "🚨 No inputs? That’s like a circle without a center!"
]

# ---------------- Helper function ----------------
def calculate_arc_length(diameter_mm, angle_deg):
    radius = diameter_mm / 2
    arc_length = 2 * math.pi * radius * (angle_deg / 360)
    return arc_length

# ---------------- Session state ----------------
if "history" not in st.session_state:
    st.session_state.history = []

if "inputs" not in st.session_state:
    st.session_state.inputs = {"diameter": "", "angle": ""}

# ---------------- Layout with image ----------------
col_left, col_right = st.columns([3, 1])

with col_left:
    st.title("🌀 Arc Length Calculator")

with col_right:
    st.image("images/Circle_arc.svg", use_container_width=True)

# Inputs (blank by default)
diameter = st.text_input("Enter Diameter (mm):", value=st.session_state.inputs.get("diameter", ""), key="diameter_input")
angle_deg = st.text_input("Enter Angle (°):", value=st.session_state.inputs.get("angle", ""), key="angle_input")

# Buttons
col1, col2 = st.columns([1,1])
with col1:
    calc_btn = st.button("🔢 Calculate")
with col2:
    reset_btn = st.button("♻️ Reset Inputs")

# Reset inputs only
if reset_btn:
    st.session_state.inputs = {"diameter": "", "angle": ""}
    st.experimental_rerun()

# ---------------- Calculation ----------------
if calc_btn:
    try:
        diameter_val = float(diameter)
        angle_val = float(angle_deg)

        # Save inputs
        st.session_state.inputs = {"diameter": diameter, "angle": angle_deg}

        # Perform calculation
        arc_length = calculate_arc_length(diameter_val, angle_val)

        # Show results
        st.subheader("📊 Arc Length Result")
        st.write(f"**Arc Length of RF pad for {angle_val:.2f}° on {diameter_val:.2f} mm shell = {arc_length:.2f} mm**")

        # Save to history
        result_row = {
            "Diameter (mm)": diameter_val,
            "Angle (°)": angle_val,
            "Arc Length (mm)": round(arc_length, 2)
        }
        st.session_state.history.append(result_row)

        # Humor on success
        st.success(random.choice(success_jokes))

    except Exception:
        st.error(random.choice(error_jokes))

# ---------------- History ----------------
if st.session_state.history:
    st.subheader("📜 Calculation History")
    hist_df = pd.DataFrame(st.session_state.history)
    st.dataframe(hist_df, use_container_width=True)

    # CSV download
   # csv = hist_df.to_csv(index=False).encode("utf-8")
   # st.download_button("⬇️ Download History as CSV", data=csv, file_name="rf_pad_arc_history.csv", mime="text/csv")
