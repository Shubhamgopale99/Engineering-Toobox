import streamlit as st
import numpy as np
import math

# ----------------- Page Setup -----------------
st.set_page_config(page_title="Ellipse Perimeter Calculator", layout="wide")

# ----------------- Layout -----------------
col1, col2 = st.columns([3, 1])

with col2:
    st.image(
        "https://www.mathsisfun.com/geometry/images/ellipse-axes.svg",
    )

with col1:
    st.title("⬭ Ellipse Perimeter Calculator")

    # ----------------- Inputs -----------------
    st.markdown("### ✏️ Enter Ellipse Dimensions")
    a = st.number_input("Semi-Major Axis (a)", min_value=1.0, value=500.0)
    b = st.number_input("Semi-Minor Axis (b)", min_value=1.0, value=300.0)

    st.markdown("""
    **a** and **b** are measured from the center, so they are like "radius" measures.
    """)

    # ----------------- Calculations -----------------
    h = ((a - b) ** 2) / ((a + b) ** 2)

    # Eccentricity
    e = math.sqrt(1 - (b**2) / (a**2))

    # Approximation 1
    P1 = 2 * math.pi * math.sqrt((a**2 + b**2) / 2)

    # Approximation 2 (Ramanujan)
    P2 = math.pi * (3*(a+b) - math.sqrt((3*a+b)*(a+3*b)))

    # Approximation 3 (Ramanujan with h)
    P3 = math.pi * (a+b) * (1 + (3*h) / (10 + math.sqrt(4 - 3*h)))

    # Final Approximation (Ramanujan mysterious)
    P_final = math.pi * ((a+b) + 
                         (3*(a-b)**2) / (10*(a+b) + math.sqrt(a**2 + 14*a*b + b**2)) +
                         (3*a*math.exp(20))/(2**36))

    # ----------------- Numerical Integration (no scipy) -----------------
    def integrand(theta, e):
        return np.sqrt(1 - (e**2) * (np.sin(theta))**2)

    def simpson_integration(func, a, b, n=10000):
        if n % 2 == 1:  # Simpson’s rule needs even number of intervals
            n += 1
        h = (b - a) / n
        x = np.linspace(a, b, n + 1)
        y = func(x)
        S = y[0] + y[-1] + 4 * np.sum(y[1:-1:2]) + 2 * np.sum(y[2:-2:2])
        return S * h / 3

    integral_val = simpson_integration(lambda t: integrand(t, e), 0, math.pi/2, n=10000)
    P_exact = 4 * a * integral_val

    # ----------------- Results Display -----------------
    st.subheader("📊 Results")
    st.write(f"**Approximation 1:** {P1:.6f}")
    st.write(f"**Approximation 2 (Ramanujan):** {P2:.6f}")
    st.write(f"**Approximation 3 (Ramanujan, h-method):** {P3:.6f}")
    st.write(f"**Final Approximation (Ramanujan mysterious):** {P_final:.6f}")
    st.write(f"**Highly Accurate (Elliptic Integral):** {P_exact:.6f}")

# ----------------- Explanation (Collapsible) -----------------
with st.expander("📖 Show Explanation"):
    # ---------------- Approximation 1 ----------------
    st.markdown(r"""
    ### Approximation 1  
    This approximation is within about 5% of the true value, so long as a is not more than 3 times longer than b (in other words, the ellipse is not too "squashed")  
    """)
    st.image("images/Approx1.png", use_container_width=True)

    # ---------------- Approximation 2 ----------------
    st.markdown(r"""
    ### Approximation 2  
    The famous Indian mathematician **Ramanujan** came up with this better approximation:  
    """)
    st.image("images/Approx2.png", use_container_width=True)

    # ---------------- Approximation 3 ----------------
    st.markdown(r"""
    ### Approximation 3  
    Ramanujan also gave this one. First calculate:  
    """)
    st.image("images/Approx3h.png", use_container_width=True)
    st.markdown("Then use:")
    st.image("images/Approx3.png", use_container_width=True)

    # ---------------- Final Approximation ----------------
    st.markdown(r"""
    ### Final Approximation  
    Ramanujan’s “mysterious” formula:  
    """)
    st.image("images/Approxfinal.png", use_container_width=True)
    st.markdown(r"""
    where  
    """)
    st.image("images/Approxfinal1.png", use_container_width=True)

    # ---------------- Highly-accurate (Integral) ----------------
    st.markdown(r"""
    ### Highly-accurate perimeter  
    There is a perfect formula using an integral:
    """)
    st.image("images/Highaccurate.png", use_container_width=True)
    st.markdown(r"""
    Note : e is the "eccentricity" not Euler's number "e" 
    """)
    st.image("images/Eccentricity.png", use_container_width=True)
