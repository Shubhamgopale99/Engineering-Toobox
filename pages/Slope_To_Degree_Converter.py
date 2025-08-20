import streamlit as st
import math
import random
import pandas as pd
import os

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

# ----------------- File Path -----------------
HISTORY_FILE = "slope_history.csv"

# ----------------- Load Previous History -----------------
if os.path.exists(HISTORY_FILE):
    history_df = pd.read_csv(HISTORY_FILE)
else:
    history_df = pd.DataFrame(columns=["Rise", "Run", "Slope %", "Angle (°)"])

# ----------------- Header Layout with Image -----------------
col1, col2 = st.columns([4, 1])  # left = wider, right = image
with col1:
    st.title("📐 Slope to Degree Converter")
    st.write("Enter rise and run to convert slope into percentage & degree.")
with col2:
    st.image(
        "https://i.postimg.cc/C1RCZxnv/Picture1.png",  # Replace with your image URL or local file
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

    # Save result in dataframe
    new_entry = {
        "Rise": rise,
        "Run": run,
        "Slope %": round(slope_percent, 2),
        "Angle (°)": round(angle_deg, 2)
    }
    history_df = pd.concat([history_df, pd.DataFrame([new_entry])], ignore_index=True)

    # Save to CSV
    history_df.to_csv(HISTORY_FILE, index=False)

    # Display result
    st.success(f"✅ Slope: {slope_percent:.2f}% | Angle: {angle_deg:.2f}°")

    # Add humor
    st.info(random.choice(jokes))

# ----------------- History Section -----------------
if not history_df.empty:
    st.subheader("📜 Calculation History")
    st.dataframe(history_df, use_container_width=True)

    # Download option
   # st.download_button(
    #    label="📥 Download History",
     #   data=history_df.to_csv(index=False).encode("utf-8"),
      #  file_name="slope_history.csv",
       # mime="text/csv"
    #)
