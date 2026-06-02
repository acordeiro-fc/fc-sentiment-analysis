import streamlit as st

st.set_page_config(page_title="Login", layout="centered")

st.title("Survey Dashboard Login")

st.write("Logged in:", st.user.is_logged_in)

if not st.user.is_logged_in:
    if st.button("Login with Google"):
        st.login(provider="google")
    st.stop()

email = st.user.email

if email not in st.secrets["ALLOWED_EMAILS"]:
    st.error("Unauthorized access")
    st.stop()

st.success(f"Welcome {email}")

st.write("You are now authenticated.")
st.write("👉 Go to the main app:")
st.page_link("app.py", label="Open Dashboard")
