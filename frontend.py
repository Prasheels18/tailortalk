import streamlit as st
import requests

# Streamlit UI
st.set_page_config(page_title="Google Calendar Assistant", page_icon="📅")
st.title("📅 Google Calendar Assistant")
st.write("Describe what you want to do with your calendar:")

# User input area
user_input = st.text_area(
    "Enter your request:",
    placeholder=(
        "Examples:\n"
        "- Create a meeting called Project Sync tomorrow from 2 PM to 3 PM\n"
        "- Show me free time slots tomorrow\n"
        "- List all my events for this week"
    ),
    height=150
)

# Run button
if st.button("Execute"):
    if not user_input.strip():
        st.warning("Please enter a valid description or request.")
    else:
        with st.spinner("Contacting backend and processing your request..."):
            try:
                response = requests.post("https://tailortalk-3.onrender.com/run", json={"prompt": user_input})
                result = response.json()

                if response.status_code == 200:
                    st.success("✅ Done!")
                    st.write(result["response"])
                else:
                    st.error(f"❌ Error: {result.get('detail', 'Unknown error')}")
            except Exception as e:
                st.error(f"❌ Failed to reach the backend: {e}")
