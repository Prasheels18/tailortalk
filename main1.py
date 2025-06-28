import streamlit as st
import os
from dotenv import load_dotenv
from langchain.agents import AgentType, initialize_agent
from langchain_groq import ChatGroq
from composio_langchain import ComposioToolSet

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
COMPOSIO_API_KEY = os.getenv("COMPOSIO_API_KEY")

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
        with st.spinner("Processing your request..."):

            # Initialize LLM and Composio tools
            try:
                llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=GROQ_API_KEY)

                composio_toolset = ComposioToolSet(api_key=COMPOSIO_API_KEY)
                tools = composio_toolset.get_tools(actions=[
                    "GOOGLECALENDAR_CREATE_EVENT",
                    "GOOGLECALENDAR_FIND_FREE_SLOTS",
                    "GOOGLECALENDAR_EVENTS_LIST"
                ])

                agent = initialize_agent(
                    tools,
                    llm,
                    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
                    verbose=True
                )

                response = agent.run(user_input)
                st.success("✅ Done!")
                st.write(response)

            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")


