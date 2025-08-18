import streamlit as st
import pandas as pd
import math
import random

st.set_page_config(page_title="Tank L/D Ratio Calculator", layout="centered")

# -------------------- Humor bank --------------------
success_jokes = [
    "🎉 Boom! Numbers don't lie, but tanks sometimes do!",
    "🛢️ Tank dimensions calculated. Now don’t try storing Coke in it!",
    "📏 Math done! Even Einstein would be proud.",
    "✅ Another tank born. Somewhere, an engineer smiled."
]

error_jokes = [
    "🤔 Umm… did you forget something? Even tanks need all inputs!",
    "⚠️ No input, no output. That’s math 101!",
    "😂 You expect me to guess the numbers? I'm smart, not psychic!",
    "🚨 Missing values! The tank union is not happy."
]

# -------------------- Helper functions --------------------
def calculate_dimensions(volume, min_ratio, max_ratio):
    results = []
    for ratio in (min_ratio, max_ratio):
        diameter = ((4 * volume) / (math.pi * ratio)) ** (1 / 3)
        height = ratio * diameter
        results.append({
            "L/D Ratio": ratio,
            "Diameter (m)": round(diameter, 3),
            "Height (m)": round(height, 3)
        })
    return results

# -------------------- Session state --------------------
if "history" not in st.session_state:
    st.session_state.history = []

if "inputs" not in st.session_state:
    st.session_state.inputs = {
        "volume": "",
        "min_ratio": "",
        "max_ratio": "",
        "margin_input": ""
    }

# -------------------- UI --------------------
st.title("🛢️ Tank L/D Ratio Calculator")

# Input fields (managed via session state)
volume = st.text_input("Enter operating tank volume (m³):", value=st.session_state.inputs["volume"])
min_ratio = st.text_input("Enter minimum L/D ratio [default 1.25]:", value=st.session_state.inputs["min_ratio"])
max_ratio = st.text_input("Enter maximum L/D ratio [default 2.0]:", value=st.session_state.inputs["max_ratio"])
margin_input = st.text_input("Enter volume margin to add (%) [blank for none]:", value=st.session_state.inputs["margin_input"])

# Action buttons
col1, col2 = st.columns([1,1])
with col1:
    calc_btn = st.button("🔢 Calculate")
with col2:
    reset_btn = st.button("♻️ Reset Inputs")

# Reset logic (only inputs)
if reset_btn:
    st.session_state.inputs = {
        "volume": "",
        "min_ratio": "",
        "max_ratio": "",
        "margin_input": ""
    }
    st.experimental_rerun()

# Calculation logic
if calc_btn:
    try:
        # Convert inputs
        volume_val = float(volume)
        min_val = float(min_ratio) if min_ratio else 1.25
        max_val = float(max_ratio) if max_ratio else 2.0
        margin_percent = float(margin_input) if margin_input else None

        # Save inputs back into session_state
        st.session_state.inputs = {
            "volume": volume,
            "min_ratio": min_ratio,
            "max_ratio": max_ratio,
            "margin_input": margin_input
        }

        # Operating volume results
        op_results = calculate_dimensions(volume_val, min_val, max_val)
        df_op = pd.DataFrame(op_results)
        st.subheader("Operating Volume Results")
        st.write(df_op)

        # Append to history
        for r in op_results:
            r.update({"Volume (m³)": round(volume_val, 3), "Type": "Operating"})
            st.session_state.history.append(r)

        # Gross volume results
        if margin_percent is not None:
            gross_volume = volume_val * (1 + margin_percent / 100)
            gross_results = calculate_dimensions(gross_volume, min_val, max_val)
            df_gross = pd.DataFrame(gross_results)
            st.subheader(f"Gross Volume Results (+{margin_percent}%)")
            st.write(df_gross)

            for r in gross_results:
                r.update({"Volume (m³)": round(gross_volume, 3), "Type": "Gross"})
                st.session_state.history.append(r)

        # Random success humor
        st.success(random.choice(success_jokes))

    except Exception:
        st.error(random.choice(error_jokes))

# -------------------- History --------------------
if st.session_state.history:
    st.subheader("📜 Calculation History")
    hist_df = pd.DataFrame(st.session_state.history)
    st.dataframe(hist_df, use_container_width=True)

    # Download option
    #csv = hist_df.to_csv(index=False).encode('utf-8')
    #st.download_button("⬇️ Download History as CSV", data=csv, file_name="tank_history.csv", mime="text/csv")
