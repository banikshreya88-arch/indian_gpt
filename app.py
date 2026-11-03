import streamlit as st
from groq import Groq

# Page configuration
st.set_page_config(
    page_title="Indian GPT",
    page_icon="🤖",
    layout="centered"
)

st.title("🇮🇳 Indian GPT")
st.write("Powered by Groq & Streamlit")

# Initialize Groq client using Streamlit Secrets
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("GROQ_API_KEY secret paowa jacche na! Streamlit Secrets-e key-ta thik bhabe add korechis toh?")
    st.stop()

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are Indian GPT, a helpful and smart AI assistant created by Shubham."}
    ]

# Display prior chat messages (excluding system prompt)
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# User input chat box
if prompt := st.chat_input("Kichu jiggesh koron..."):
    # Append user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate assistant response using Groq
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        try:
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=st.session_state.messages,
                temperature=0.7,
                max_tokens=1024,
            )
            response_text = completion.choices[0].message.content
            message_placeholder.markdown(response_text)
            
            # Append assistant response
            st.session_state.messages.append({"role": "assistant", "content": response_text})
        except Exception as e:
            message_placeholder.error(f"API Error: {str(e)}")
