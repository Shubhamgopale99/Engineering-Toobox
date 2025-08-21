import streamlit as st
import math
import pandas as pd

# Streamlit app configuration
st.set_page_config(page_title="Limpet Coil Calculator", layout="centered")

st.title("🐍 Limpet Coil Length, Weight & Heat Transfer Area Calculator")
st.markdown("Get your coil numbers right... and your smile brighter 😄")

# ---------------- Layout with image ----------------
col_left, col_right = st.columns([3, 1])

with col_left:
    st.title("🌀 Arc Length of RF Pad Calculator")

with col_right:
    st.image("images/Circle_arc.svg", use_container_width=True)

# ---------------- Session State ----------------
if "limpet_coil_history" not in st.session_state:
    st.session_state.limpet_coil_history = []   # quick list (Heat Transfer Area only)

if "limpet_coil_detailed_history" not in st.session_state:
    st.session_state.limpet_coil_detailed_history = []   # detailed history with inputs

# ---------------- Reset Function ----------------
def reset_inputs():
    st.session_state.shell_id = None
    st.session_state.shell_height = None
    st.session_state.shell_thk = None
    st.session_state.limpet_od = None
    st.session_state.limpet_thk = None
    st.session_state.limpet_pitch = None
    st.session_state.coil_coverage = None
    st.session_state.density = None

# ---------------- Inputs ----------------
shell_id = st.number_input("1️⃣ Shell ID (mm)", value=st.session_state.get("shell_id", None), step=1.0, key="shell_id")
shell_height = st.number_input("2️⃣ Shell Height (mm)", value=st.session_state.get("shell_height", None), step=1.0, key="shell_height")
shell_thk = st.number_input("3️⃣ Shell Thickness (mm)", value=st.session_state.get("shell_thk", None), step=0.1, key="shell_thk")
limpet_od = st.number_input("4️⃣ Limpet OD (mm)", value=st.session_state.get("limpet_od", None), step=0.1, key="limpet_od")
limpet_thk = st.number_input("5️⃣ Limpet Thickness (mm)", value=st.session_state.get("limpet_thk", None), step=0.1, key="limpet_thk")
limpet_pitch = st.number_input("6️⃣ Limpet Pitch (mm)", value=st.session_state.get("limpet_pitch", None), step=0.1, key="limpet_pitch")
coil_coverage = st.number_input("7️⃣ Limpet Coil Coverage (%)", value=st.session_state.get("coil_coverage", None), step=0.1, key="coil_coverage")
density = st.number_input("8️⃣ Density of Material (kg/m³)", value=st.session_state.get("density", None), step=0.1, key="density")

col1, col2 = st.columns(2)
with col1:
    calculate = st.button("💡 Calculate")
with col2:
    reset = st.button("🔄 Reset", on_click=reset_inputs)

# ---------------- Calculation ----------------
if calculate:
    try:
        # --- Limpet Coil Length & Weight ---
        single_turn_length = (((shell_id + shell_thk*2) + (2*limpet_thk)) * math.pi) * 10**-3  # m

        no_of_turns = (shell_height * (coil_coverage / 100)) / limpet_pitch

        total_length = single_turn_length * no_of_turns

        limpet_weight = (
            ((shell_id + shell_thk*2) + (2*limpet_thk)) * math.pi *
            (math.pi * limpet_od * 1.04 / 2)
        ) * (limpet_thk * density) * 10**-9  # kg

        Total_limpet_weight = limpet_weight * no_of_turns

        total_length_m = math.pi * shell_id * no_of_turns / 1000  # m
        heat_transfer_area = math.pi * (limpet_od / 1000) * total_length_m  # m²

        # Save results
        result = {
            "Shell ID (mm)": shell_id,
            "Shell Height (mm)": shell_height,
            "Single Turn Length (m)": round(single_turn_length, 3),
            "Number of Turns": round(no_of_turns, 2),
            "Total Coil Length (m)": round(total_length, 3),
            "Single Turn Limpet Weight (kg)": round(limpet_weight, 3),
            "Total Limpet Weight (kg)": round(Total_limpet_weight, 3),
            "Heat Transfer Area (m²)": round(heat_transfer_area, 3)
        }
        st.session_state.limpet_coil_detailed_history.append(result)
        st.session_state.limpet_coil_history.append(round(heat_transfer_area, 3))

        # Display results
        st.success("✅ Calculations Completed!")
        st.write(f"📏 **Single Turn Length:** {single_turn_length:.3f} m")
        st.write(f"🔄 **Number of Turns:** {no_of_turns:.2f}")
        st.write(f"🌀 **Total Coil Length:** {total_length:.3f} m")
        st.write(f"⚖️ **Limpet Weight:** {limpet_weight:.3f} kg")
        st.write(f"⚖️ **Total Limpet Weight:** {Total_limpet_weight:.3f} kg")
        st.write(f"🔥 **Heat Transfer Area:** {heat_transfer_area:.3f} m²")

        # Humor section
        st.markdown("---")
        st.markdown("💬 *Fun Fact:* If coils were noodles, you’d now be the chef of the year 🍜.")
        st.markdown("🚀 *Engineering wisdom:* Measure twice, cut once… unless it’s Monday morning ☕.")

    except ZeroDivisionError:
        st.error("Oops! Your limpet pitch is zero. Even in engineering, dividing by zero is bad math 😅")

# ---------------- Histories ----------------
if st.session_state.limpet_coil_detailed_history:
    st.markdown("---")
    st.subheader("📜 Detailed Limpet Coil Calculation History")
    df = pd.DataFrame(st.session_state.limpet_coil_detailed_history)
    st.dataframe(df, use_container_width=True)

if st.session_state.limpet_coil_history:
    st.subheader("📜 Quick Heat Transfer Area History")
    st.write(st.session_state.limpet_coil_history)
