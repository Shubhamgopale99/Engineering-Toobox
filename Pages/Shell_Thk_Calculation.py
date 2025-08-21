import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="ASME UG-27 Shell Calc", layout="wide")

# ---------------- Humor Bank ----------------
funny_success = [
    "✅ Math says you are safe. Celebrate with coffee ☕!",
    "🎉 Great! Your vessel won’t explode (at least not today).",
    "🛠️ Thickness approved. Your welder will thank you.",
    "🚀 Good news: it passes. Bad news: you still have paperwork."
]

funny_fail = [
    "😅 Oops! Something is missing. Even Einstein couldn’t calculate this.",
    "🙈 Did you forget something? Vessels don’t design themselves!",
    "🤔 Input missing… Are you testing me or yourself?",
    "😂 Nice try! But without all inputs, this vessel is just a dream."
]

# ---------------- Helpers ----------------
def calculate(inputs):
    try:
        t = inputs["t"]
        Ca = inputs["Ca"]
        mill_tol = inputs["mill_tol"]
        Do = inputs["Do"]
        P = inputs["P"]
        E = inputs["E"]
        S = inputs["S"]

        tc = t - Ca - mill_tol
        if tc <= 0:
            return "❌ ERROR: Corroded thickness tc ≤ 0. Check inputs.", None

        R = Do / 2 - tc
        if R <= 0:
            return "❌ ERROR: Inside radius R ≤ 0. Check Do and t/Ca/mill_tol.", None

        denom = S * E - 0.6 * P
        if denom <= 0:
            return "❌ ERROR: S·E − 0.6·P ≤ 0. Increase S/E or reduce P.", None

        t_req = (P * R) / denom
        t_total_req = t_req + Ca + mill_tol
        MAWP = (S * E * tc) / (R + 0.6 * tc)

        result = {
            "Corroded Thickness tc (mm)": round(tc, 3),
            "Inside Radius R (mm)": round(R, 3),
            "Required Thk (uncorroded) (mm)": round(t_req, 3),
            "Total Required Thk (mm)": round(t_total_req, 3),
            "MAWP corroded (MPa)": round(MAWP, 3),
            "status": f"{t:.3f} → {'✅ OK' if t >= t_total_req else '❌ IS NOT ENOUGH!'}"
        }
        return None, result
    except Exception as e:
        return f"❌ Error: {e}", None


# ---------------- Streamlit UI ----------------
st.title("🛢️ ASME UG-27 Shell Thickness Calculator")

# Independent history for this page
if "ug27_history" not in st.session_state:
    st.session_state.ug27_history = []

# Reset inputs function
def reset_inputs():
    for key in ["P", "T", "Material", "Density", "S", "Do", "L", "t", "Ca", "mill_tol", "E"]:
        st.session_state[key] = ""
    st.success("🔄 All inputs cleared!")

# Input form
with st.form("ug27_form"):
    P = st.text_input("Design Pressure P (MPa)", key="P")
    T = st.text_input("Design Temperature (°C)", key="T")
    mat = st.text_input("Material", key="Material")
    rho = st.text_input("Density (kg/m³)", key="Density")
    S = st.text_input("Allowable Stress S (MPa) (From ASME Sec II-D)", key="S")
    Do = st.text_input("Outside Diameter Do (mm)", key="Do")
    L = st.text_input("Tangent-to-Tangent Length L (mm)", key="L")
    t = st.text_input("Nominal Wall Thickness t (mm)", key="t")
    Ca = st.text_input("Corrosion Allowance Ca (mm)", key="Ca")
    mill_tol = st.text_input("Mill Tolerance (mm)", key="mill_tol")
    E = st.text_input("Joint Efficiency E (0-1)", key="E")

    col1, col2 = st.columns([3,1])
    with col1:
        submitted = st.form_submit_button("✅ Calculate")
    with col2:
        reset = st.form_submit_button("🔄 Reset Inputs")

# Handle Reset
if reset:
    reset_inputs()

# Handle Calculation
if submitted:
    if any(x == "" for x in [P, T, mat, rho, S, Do, L, t, Ca, mill_tol, E]):
        st.error(random.choice(funny_fail))
    else:
        calc_inputs = {
            "P": float(P),
            "S": float(S),
            "Do": float(Do),
            "t": float(t),
            "Ca": float(Ca),
            "mill_tol": float(mill_tol),
            "E": float(E)
        }
        error, result = calculate(calc_inputs)

        if error:
            st.error(error)
        else:
            st.success(random.choice(funny_success))
            st.write("### 📊 Results")
            st.json(result)

            # Save to independent history
            row = {
                "P": float(P), "T": float(T), "Material": mat, "rho": float(rho),
                "S": float(S), "Do": float(Do), "L": float(L), "t": float(t),
                "Ca": float(Ca), "mill_tol": float(mill_tol), "E": float(E),
                **result
            }
            st.session_state.ug27_history.append(row)

# Show History
if st.session_state.ug27_history:
    st.write("### 📜 History (until tab close)")
    df = pd.DataFrame(st.session_state.ug27_history)
    st.dataframe(df)
