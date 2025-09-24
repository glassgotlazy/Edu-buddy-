import streamlit as st
import openai
import datetime

# Set OpenAI API key securely using Streamlit secrets or environment variables
openai.api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else "YOUR_OPENAI_API_KEY_HERE"

# Function to detect mood from user input
def detect_mood(text):
    # Basic keyword-based mood detection as an example
    moods = {
        "happy": ["happy", "good", "great", "joy", "excited", "awesome"],
        "sad": ["sad", "unhappy", "bad", "depressed", "down", "upset"],
        "angry": ["angry", "mad", "frustrated", "annoyed"],
        "bored": ["bored", "tired", "meh", "dull", "nothing to do"],
        "anxious": ["anxious", "nervous", "worried", "concerned"],
    }
    text_lower = text.lower()
    for mood, keywords in moods.items():
        if any(k in text_lower for k in keywords):
            return mood
    return "neutral"

# Function to get AI response from OpenAI GPT
def get_ai_response(prompt):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150,
            temperature=0.7,
            n=1,
            stop=None
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error: {e}"

# Initialize Streamlit app layout
st.title("ECHO AI Companion - Improved")

# User text input
user_input = st.text_area("Talk to ECHO:", height=150)

# Button to submit input
if st.button("Send"):
    if user_input.strip() == "":
        st.warning("Please enter something to talk about.")
    else:
        mood = detect_mood(user_input)
        st.write(f"Detected mood: **{mood.capitalize()}**")

        # Generate AI response contextualized with mood
        prompt = f"The user is feeling {mood}. Respond empathetically and helpfully.\nUser: {user_input}\nECHO:"
        ai_reply = get_ai_response(prompt)

        # Display AI response
        st.markdown(f"**ECHO:** {ai_reply}")

        # Save conversation log with timestamp (optional)
        with open("echo_conversation_log.txt", "a", encoding="utf-8") as f:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{timestamp}] User ({mood}): {user_input}\n")
            f.write(f"[{timestamp}] ECHO: {ai_reply}\n\n")

# Footer
st.markdown("---")
st.caption("ECHO AI Companion improved version with mood detection and chat response.")
