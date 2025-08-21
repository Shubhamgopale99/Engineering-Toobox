import streamlit as st
import math
import random
import pandas as pd

# ----------------- Page Setup -----------------
st.set_page_config(page_title="Slope to Degree Converter", layout="centered")

# ----------------- Humor Bank -----------------
jokes = [
    "🎢 That slope looks steeper than my Monday mornings!",
    "📐 Angles don’t lie... unlike my alarm clock!",
    "🚴 This slope is cycle-approved (unless you hate uphill rides).",
    "🧗 Better grab your climbing gear for this one!",
    "😂 That angle is sharp enough to cut through excuses!"
]

# ----------------- Unique History Key -----------------
if "slope_history" not in st.session_state:
    st.session_state.slope_history = []

# ----------------- Header Layout with Image -----------------
col1, col2 = st.columns([4, 1])
with col1:
    st.title("📐 Slope to Degree Converter")
    st.write("Enter rise and run to convert slope into percentage & degree.")
with col2:
    st.image(
        "https://i.postimg.cc/C1RCZxnv/Picture1.png",
        width=80
    )

# ----------------- User Input -----------------
col1, col2 = st.columns(2)
with col1:
    rise = st.number_input("Slope Rise", min_value=0, step=1, value=0)
with col2:
    run = st.number_input("Slope Run", min_value=1, step=1, value=1)

# ----------------- Calculation -----------------
if st.button("Calculate 🎯"):
    slope_percent = (rise / run) * 100
    angle_deg = math.degrees(math.atan(slope_percent / 100))

    # Save result in session history
    new_entry = {
        "Rise": rise,
        "Run": run,
        "Slope %": round(slope_percent, 2),
        "Angle (°)": round(angle_deg, 2)
    }
    st.session_state.slope_history.append(new_entry)

    # Display result
    st.success(f"✅ Slope: {slope_percent:.2f}% | Angle: {angle_deg:.2f}°")

    # Add humor
    st.info(random.choice(jokes))

# ----------------- History Section -----------------
if st.session_state.slope_history:
    st.subheader("📜 Calculation History")
    hist_df = pd.DataFrame(st.session_state.slope_history)
    st.dataframe(hist_df, use_container_width=True)

    # Download option
    st.download_button(
        label="📥 Download History",
        data=hist_df.to_csv(index=False).encode("utf-8"),
        file_name="slope_history.csv",
        mime="text/csv"
    )
