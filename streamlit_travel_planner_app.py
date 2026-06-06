import os
from openai import OpenAI
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = """
You are an expert Travel Itinerary Planner.

Your goal is to help users create personalized travel plans.

Conversation flow:

1. Greet the user and ask for:
   - Destination
   - Number of days
   - Budget (Low, Medium, Luxury)
   - Travel style (Adventure, Relaxation, Culture, Food, Family, etc.)

2. If any important information is missing, ask follow-up questions.

3. Once enough information is collected, generate a complete itinerary including:
   - Day-by-day schedule
   - Recommended attractions
   - Food recommendations
   - Transportation suggestions
   - Estimated daily budget
   - Travel tips

4. Format the itinerary clearly using headings and bullet points.

5. If the user wants changes, revise the itinerary accordingly.

Be friendly, helpful, and practical.
"""

st.title("✈️ Travel Itinerary Planner")
st.caption("Tell me where you're going and I'll create a personalized travel itinerary.")
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "assistant",
            "content": """
🌍 Welcome!

I'm your travel planner.

Tell me:

• Destination
• Number of days
• Budget (Low / Medium / Luxury)
• Travel style (Adventure, Food, Relaxation, Culture, Family, etc.)

Example:
"I want a 5-day trip to Paris with a medium budget focused on food and sightseeing."
"""
        },
    ]

for msg in st.session_state.messages[1:]:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    client = OpenAI()
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
