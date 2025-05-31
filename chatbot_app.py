import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
from transcript_cache import get_transcript_text
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
gemini_model = genai.GenerativeModel("gemini-2.0-flash")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

hitesh_prompt = (
    """
You are an AI Persona of Hitesh Choudhary. Talk in Hinglish or English like Hitesh does.
You’re in a group conversation with Piyush Garg and a user. Be aware of what the user and Piyush say.
Here are examples of your tone and speaking style:
"""
    + get_transcript_text(
        [
            "GWvW96WNB6Q",
            "kDLrIV59PdU",
            "6dqAwh2MCg0",
            "_mowKpIZpbU",
            "8mk85fyzevc",
            "1i8R-iJiEi8",
            "6RHYkwJPJlM",
        ]
    )
    + "\n\nConvert the above example in Hinglish and You’re ready to answer as Hitesh in Hinglish or in English as required but not in Hindi, in a group chat with Piyush and a user."
)

piyush_prompt = (
    """
You are an AI Persona of Piyush Garg. Talk in Hinglish or English like Piyush does.
You’re in a group conversation with Hitesh Choudhary and a user. Be aware of what the user and Hitesh say.
Here are examples of your tone and speaking style:
"""
    + get_transcript_text(
        [
            "ohIAiuHMKMI",
            "v1pj9XrJ_Lw",
            "VLiE5tyfko4",
            "b_B1BEShfBc",
            "pl3sJ-RoD3Q",
            "cJ6v-0hY00A",
        ]
    )
    + "\n\nConvert the above example in Hinglish and You’re ready to answer as Piyush in Hinglish or English as required but not in Hindi, in a group chat with Hitesh and a user."
)

if "history" not in st.session_state:
    st.session_state.history = []
if "base_hitesh" not in st.session_state:
    st.session_state.base_hitesh = [{"role": "system", "content": hitesh_prompt}]
if "base_piyush" not in st.session_state:
    st.session_state.base_piyush = [{"role": "system", "content": piyush_prompt}]

st.set_page_config(page_title="Hitesh & Piyush Chatbot", layout="centered")
st.title("🤖 Chat with Hitesh & Piyush")
st.markdown(
    "Ask anything — AI versions of **Hitesh Choudhary** and **Piyush Garg** will answer together like a podcast! 🎙️"
)

user_input = st.chat_input("Type your message...")

for msg in st.session_state.history:
    st.chat_message(msg["sender"]).markdown(msg["text"])

if not st.session_state.history:
    hitesh_intro = "🧑‍🏫 Hitesh: Haan ji, bilkul ready hoon! Welcome to the group, maza aayega aaj! Chai bhi ready kar lena, kyunki chalo baat karte hain coding, tech, AI, ML, Python, ya jo bhi topic ho aapke mind mein! Toh batao, kya padhna hai, kya seekhna hai? 😄"
    piyush_intro = "👨‍💻 Piyush: Hello doston! Badiya cheez seekhne wale hain aaj milke. Jo bhi technical topic, Roadmap ho, coding ho, AI ho, ya kuch bhi, chill kar ke puchho bhai, main help karunga total mast tareeke se. 😎"
    st.chat_message("Hitesh").markdown(hitesh_intro)
    st.session_state.history.append({"sender": "Hitesh", "text": hitesh_intro})
    st.chat_message("Piyush").markdown(piyush_intro)
    st.session_state.history.append({"sender": "Piyush", "text": piyush_intro})

if user_input:
    st.chat_message("user").markdown(user_input)
    st.session_state.history.append({"sender": "user", "text": user_input})
    chat_context = st.session_state.history[-10:]

    openai_context = []
    for m in chat_context:
        role = "user" if m["sender"] == "user" else "assistant"
        name = None if role == "user" else m["sender"]
        openai_context.append({"role": role, "content": m["text"], "name": name})

    hitesh_response = client.chat.completions.create(
        model="gpt-4.1-mini", messages=st.session_state.base_hitesh + openai_context
    )
    hitesh_text = hitesh_response.choices[0].message.content.strip()
    st.chat_message("Hitesh").markdown(f"🧑‍🏫 {hitesh_text}")
    st.session_state.history.append({"sender": "Hitesh", "text": hitesh_text})

    gemini_input = piyush_prompt + "\n\n"
    for msg in openai_context + [
        {"role": "assistant", "name": "Hitesh", "content": hitesh_text}
    ]:
        speaker = msg.get("name", "User")
        gemini_input += f"{speaker}: {msg['content']}\n"

    gemini_response = gemini_model.generate_content(gemini_input)
    piyush_text = gemini_response.text.strip()
    st.chat_message("Piyush").markdown(f"👨‍💻 {piyush_text}")
    st.session_state.history.append({"sender": "Piyush", "text": piyush_text})
