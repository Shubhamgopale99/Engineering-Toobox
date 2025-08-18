import streamlit as st
import pandas as pd
import math
import random

st.set_page_config(page_title="Dish End Calculator", layout="centered")

# -------------------- Humor Bank --------------------
success_jokes = [
    "🎉 Boom! Your dish end is cooked to perfection!",
    "🛢️ Math done! Now go brag to a welder.",
    "📏 Dimensions ready. Time to flex your tank skills.",
    "✅ Numbers aligned! Even ASME would clap."
]

error_jokes = [
    "🤔 Did you forget something? Tanks don’t design themselves!",
    "⚠️ No input, no output. Just like free lunches.",
    "😂 Missing values! I’m good at math, not magic.",
    "🚨 Enter the numbers before the dish collapses!"
]

# ---------------- Layout with image ----------------
col_left, col_right = st.columns([3, 1])

with col_left:
    st.title("Dish End Volume")

with col_right:
    st.image("images/Dish.avif", use_container_width=True)

# -------------------- Helper Functions --------------------
def calculate_torispherical_dish(tank_id_mm, sf_mm, dish_thk_mm):
    crown_radius = tank_id_mm * 1.00
    knuckle_radius = tank_id_mm * 0.10
    dish_blank_dia = tank_id_mm + 0.10 * tank_id_mm + 2 * sf_mm
    dish_end_height = (tank_id_mm * 0.194) + sf_mm + dish_thk_mm
    d3 = tank_id_mm ** 3
    d2 = tank_id_mm ** 2
    volume_m3 = ((0.0847 * d3) + (math.pi * d2 * sf_mm) / 4) * 1e-9
    return crown_radius, knuckle_radius, dish_blank_dia, dish_end_height, volume_m3

def calculate_ellipsoidal_dish(tank_id_mm, sf_mm, dish_thk_mm):
    crown_radius = 0.9 * tank_id_mm
    dish_blank_dia = 1.17 * tank_id_mm + 2 * sf_mm
    dish_end_height = (0.25 * tank_id_mm) + sf_mm + dish_thk_mm
    d3 = tank_id_mm ** 3
    d2 = tank_id_mm ** 2
    volume_m3 = ((math.pi * d3) / 24 + (math.pi * d2 * sf_mm) / 4) * 1e-9
    return crown_radius, dish_blank_dia, dish_end_height, volume_m3

# -------------------- Session State --------------------
if "history" not in st.session_state:
    st.session_state.history = []

if "inputs" not in st.session_state:
    st.session_state.inputs = {"tank_id": "", "sf": "", "dish_thk": ""}

# -------------------- UI --------------------
st.title("🛢️ Dish End Calculator")

# Inputs (blank by default, stored in session_state)
tank_id = st.text_input(
    "Enter Tank ID (mm):",
    value=st.session_state.inputs.get("tank_id", ""),
    key="tank_id_input"
)

sf = st.text_input(
    "Enter Straight Flange (SF) (mm):",
    value=st.session_state.inputs.get("sf", ""),
    key="sf_input"
)

dish_thk = st.text_input(
    "Enter Dish Thickness (mm):",
    value=st.session_state.inputs.get("dish_thk", ""),
    key="thk_input"
)
# Buttons
col1, col2 = st.columns([1,1])
with col1:
    calc_btn = st.button("🔢 Calculate")
with col2:
    reset_btn = st.button("♻️ Reset Inputs")

# Reset (only clears inputs, keeps history)
if reset_btn:
    st.session_state.inputs = {"tank_id": "", "sf": "", "dish_thk": ""}
    st.experimental_rerun()

# Calculation
if calc_btn:
    try:
        tank_id_val = float(tank_id)
        sf_val = float(sf)
        dish_thk_val = float(dish_thk)

        # Save inputs
        st.session_state.inputs = {"tank_id": tank_id, "sf": sf, "dish_thk": dish_thk}

        # Torispherical
        c_r_t, k_r, b_d_t, h_t, vol_t = calculate_torispherical_dish(tank_id_val, sf_val, dish_thk_val)
        df_t = pd.DataFrame([{
            "Type": "Torispherical",
            "Crown Radius (mm)": round(c_r_t,2),
            "Knuckle Radius (mm)": round(k_r,2),
            "Blank Dia (mm)": round(b_d_t,2),
            "Dish End Height (mm)": round(h_t,2),
            "Volume (m³)": round(vol_t,6),
            "Volume (liters)": round(vol_t*1000,3)
        }])

        # Ellipsoidal
        c_r_e, b_d_e, h_e, vol_e = calculate_ellipsoidal_dish(tank_id_val, sf_val, dish_thk_val)
        df_e = pd.DataFrame([{
            "Type": "Ellipsoidal",
            "Crown Radius (mm)": round(c_r_e,2),
            "Knuckle Radius (mm)": "-",
            "Blank Dia (mm)": round(b_d_e,2),
            "Dish End Height (mm)": round(h_e,2),
            "Volume (m³)": round(vol_e,6),
            "Volume (liters)": round(vol_e*1000,3)
        }])

        result_df = pd.concat([df_t, df_e], ignore_index=True)

        st.subheader("📊 Dish End Results")
        st.dataframe(result_df, use_container_width=True)

        # Save to history
        st.session_state.history.append(result_df)

        # Humor
        st.success(random.choice(success_jokes))

    except Exception:
        st.error(random.choice(error_jokes))

# -------------------- History --------------------
if st.session_state.history:
    st.subheader("📜 Calculation History")
    hist_df = pd.concat(st.session_state.history, ignore_index=True)
    st.dataframe(hist_df, use_container_width=True)

   # csv = hist_df.to_csv(index=False).encode("utf-8")
    #st.download_button("⬇️ Download History as CSV", data=csv, file_name="dish_end_history.csv", mime="text/csv")
