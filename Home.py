import streamlit as st
import requests

# --- Add to Home Screen Button for Android Chrome Users ---
st.markdown(
    """
    <script>
    // Only show for Android Chrome
    function isAndroidChrome() {
        return /Android/i.test(navigator.userAgent) && /Chrome/i.test(navigator.userAgent);
    }
    // Check if user already dismissed
    function shouldShowA2HS() {
        return isAndroidChrome() && !localStorage.getItem('a2hs_dismissed');
    }
    window.addEventListener('DOMContentLoaded', function() {
        if (shouldShowA2HS()) {
            document.getElementById('a2hs-btn').style.display = 'block';
        }
    });
    function addToHomeScreen() {
        alert('To add this app to your home screen, tap the browser menu (⋮) and select "Add to Home screen".');
        document.getElementById('a2hs-btn').style.display = 'none';
        localStorage.setItem('a2hs_dismissed', '1');
    }
    </script>
    <style>
    #a2hs-btn {
        display: none;
        background: #ff9800;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-size: 18px;
        margin-bottom: 20px;
        cursor: pointer;
    }
    </style>
    <button id="a2hs-btn" onclick="addToHomeScreen()">➕ Add to Home Screen</button>
    """,
    unsafe_allow_html=True,
)

# ----------------- Page Setup -----------------
st.set_page_config(
    page_title="About & Guide",
    layout="wide",
    page_icon="https://i.postimg.cc/YCSYFC2M/S-Logo-removebg-preview.png"  # Change this URL to your preferred logo
)

st.title("🛠️ Engineering Toolbox - User Guide")

st.markdown(
    """
Welcome to the **Tank & Coil Engineering Toolbox**! This platform is designed to simplify and accelerate your engineering calculations for tanks, coils, and related equipment.
    """
)

# --- In-app navigation links ---
st.markdown("### 🚀 What can you do here?")
st.page_link("pages/Volume_To_Tank_Dimension.py", label="Volume ↔ Dimension conversions", icon="🔄")
st.page_link("pages/Dish_End_Volume.py", label="Dish ends calculations", icon="🥣")
st.page_link("pages/Limpet_Toolbox.py", label="Limpet coil design", icon="🌀")
st.page_link("pages/Arc_Length.py", label="Arc length calculation", icon="📏")
st.page_link("pages/Heat_Exchanger_Area.py", label="Heat exchanger area", icon="🌡️")
st.page_link("pages/Shell_Thk_Calculation.py", label="ASME UG-27 shell thickness check", icon="🛢️")


# The following block is not essential for the core functionality of your app.
# It only provides user guidance and information.
st.markdown(
    """
---
### 🧭 How to use:
- Use the **sidebar** to navigate between tools.
- Each page provides a simple interface for inputting your data and getting instant results.
- Links above will take you directly to the respective tool.

--- 
### 📈 Continuous Improvement
This is just the beginning! The toolbox will become more advanced with upcoming updates. Stay tuned for new features and improvements.

--- 
### ❓ Need Help or Want to Connect?
You can always reach out for support, suggestions, or collaboration.
    """
)


# --- In-app navigation links ---

st.markdown(
    """
    <div style="display: flex; gap: 30px; font-size: 22px; justify-content: flex-start;">
        <a href="https://shubham1996.pythonanywhere.com/" target="_blank">
            <img src="https://i.postimg.cc/YCSYFC2M/S-Logo-removebg-preview.png" width="100" style="vertical-align:middle;">
        </a>
        <a href="https://github.com/Shubhamgopale99" target="_blank">
            <img src="https://i.postimg.cc/wB8xpwGZ/176-1766942-our-github-repos-are-here-github-icon-hd-removebg-preview.png" width="100" style="vertical-align:middle;">
        </a>
        <a href="https://www.linkedin.com/in/shubham-gopale-580899151/" target="_blank">
            <img src="https://i.postimg.cc/zXs0ShM8/linkedin.png" width="100" style="vertical-align:middle;">
        </a>
    </div>
    """,
    unsafe_allow_html=True,
)
st.write("---")
st.subheader("📩 Send me a message")
with st.form("contact_form", clear_on_submit=True):
    full_name = st.text_input("Full Name")
    email = st.text_input("Email Address")
    message = st.text_area("Your Message(Please suggest your thoughts)")
    submit = st.form_submit_button("Send 📨")
if submit:
    if full_name and email and message:
        formspree_url = "https://formspree.io/f/movlzpvz"
        response = requests.post(
            formspree_url,
            data={
                "name": full_name,
                "email": email,
                "message": message
            }
        )
        if response.status_code == 200:
            st.success("✅ Your message has been sent successfully!")
        else:
            st.error(f"❌ Failed to send message. Error code: {response.status_code}")
    else:
        st.warning("⚠️ Please fill in all fields before sending.")
