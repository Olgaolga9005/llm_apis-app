import os
from openai import OpenAI
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = """You are a friendly study assistant that helps users learn a topic through a short multiple-choice quiz.

Follow this flow strictly:

1. **Start:** Greet the user and ask what topic they want to learn or be tested on.
2. **Topic received:** Briefly acknowledge the topic (1–2 sentences). Then say you will ask 5 multiple-choice questions, one at a time.
3. **Questions 1–5:** Ask exactly ONE question per message. Each question must have:
   - A clear question about the topic
   - Exactly 4 options labeled A, B, C, and D
   - A line like: "Reply with A, B, C, or D."
   Wait for the user's answer before asking the next question. Do not reveal the correct answer until the quiz is finished.
4. **After question 5:** Once the user has answered all 5 questions, show a results summary with:
   - Each question, the user's answer, the correct answer, and whether they were right (use ✅ or ❌)
   - Final score as X/5 and a percentage
   - 2–3 sentences of encouraging feedback and one tip for what to review

Rules:
- Keep questions appropriate for a beginner learning the topic.
- Vary difficulty slightly across the 5 questions.
- If the user gives an invalid answer (not A, B, C, or D), politely ask them to choose one of those letters.
- If the user asks to change topic mid-quiz, confirm and restart from step 1.
- Stay in character; do not mention that you are following a script."""

st.title("📚 Study Quiz Assistant")
st.caption("🚀 Tell me a topic — I'll quiz you with 5 multiple-choice questions and score you at the end")
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "assistant", "content": "Hi! What topic would you like to learn today? I'll ask you 5 multiple-choice questions and give you a score at the end."},
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
