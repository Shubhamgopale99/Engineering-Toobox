import streamlit as st

# ----------------- Page Setup -----------------
st.set_page_config(page_title="Rectangle Area Calculator", layout="centered")

# ----------------- Title -----------------
st.title("⬛ Rectangle Area Calculator")

# ----------------- Inputs -----------------
st.markdown("### ✏️ Enter Rectangle Dimensions")
length = st.number_input("Length", min_value=0.0, value=10.0)
width = st.number_input("Width", min_value=0.0, value=5.0)

# ----------------- Calculation -----------------
area = length * width

# ----------------- Result -----------------
st.subheader("📊 Result")
st.write(f"**Area of Rectangle:** {area:.2f} square units")

# ----------------- Explanation -----------------
with st.expander("📖 Show Formula"):
    st.latex(r" \text{Area} = \text{Length} \times \text{Width} ")
