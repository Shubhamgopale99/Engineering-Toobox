import streamlit as st
from faker import Faker

# Initialize Faker
fake = Faker()

# Page setup
st.set_page_config(page_title="Fake Data Generator", layout="centered")

st.title("🌀 Fake Data Generator")

count = st.slider("How many fake users do you want?", 1, 10, 3)

if st.button("Generate"):
    for i in range(count):
        st.write(f"👤 Name: {fake.name()}")
        st.write(f"📧 Email: {fake.email()}")
        st.write(f"🏠 Address: {fake.address()}")
        st.markdown("---")
