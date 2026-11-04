import streamlit as st
import requests
import json
import urllib.parse
import time
import random
from datetime import datetime, timezone, timedelta
from duckduckgo_search import DDGS

# Page Config
st.set_page_config(page_title="Indian GPT", page_icon="🇮🇳", layout="wide")

# Custom CSS for Cyberpunk Theme & Green Sidebar Accents
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(5, 10, 25, 0.85), rgba(10, 15, 30, 0.95)), 
                    url('https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=1920&auto=format&fit=crop') no-repeat center center fixed;
        background-size: cover;
        color: #ffffff;
    }
    .stSidebar {
        background-color: rgba(15, 23, 42, 0.95) !important;
    }
    .stSidebar * {
        color: #ffffff !important;
    }
    h1, h2, h3, p, label {
        color: #ffffff !important;
    }
    .stSidebar h3, .stSidebar label, .stSidebar span {
        color: #22c55e !important;
        font-weight: 700 !important;
    }
    .stChatInput textarea {
        color: #2563eb !important;
        background-color: #f8fafc !important;
        font-weight: 600 !important;
    }
    .stChatInput textarea::placeholder {
        color: #64748b !important;
    }
    @keyframes bounce {
        0%, 80%, 100% { transform: translateY(0); }
        40% { transform: translateY(-8px); }
    }
    .dot1 { animation: bounce 1.4s infinite ease-in-out both; animation-delay: -0.32s; }
    .dot2 { animation: bounce 1.4s infinite ease-in-out both; animation-delay: -0.16s; }
    .dot3 { animation: bounce 1.4s infinite ease-in-out both; }
    </style>
""", unsafe_allow_html=True)

# Hardcoded Groq API Key & Optional Secondary Secret Key Support
PRIMARY_KEY = "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"
SECONDARY_KEY = st.secrets.get("GROQ_API_KEY_2", "")
AVAILABLE_KEYS = [k for k in [PRIMARY_KEY, SECONDARY_KEY] if k.strip() != ""]

def get_active_key():
    return random.choice(AVAILABLE_KEYS) if AVAILABLE_KEYS else PRIMARY_KEY

# Live Web Search Function (DuckDuckGo Grounding)
def search_web(query):
    try:
        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=3):
                results.append(f"Source: {r.get('title')}\nContent: {r.get('body')}")
        if results:
            return "\n\n".join(results)
    except:
        pass
    return ""

# Function to dynamically fetch and auto-find available models from Groq API
def get_available_models(api_key):
    default_models = [
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant",
        "mixtral-8x7b-32768",
        "gemma2-9b-it"
    ]
    try:
        headers = {"Authorization": f"Bearer {api_key}"}
        response = requests.get("https://api.groq.com/openai/v1/models", headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json().get("data", [])
            fetched = []
            for m in data:
                m_id = m.get("id", "")
                if not any(k in m_id.lower() for k in ["whisper", "guard", "orpheus", "vision", "audio"]):
                    fetched.append(m_id)
            if fetched:
                return fetched
    except:
        pass
    return default_models

# Initialize Session States
if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = {
        "New Chat": [{"role": "assistant", "content": "Hi bro i am your personal chatbot Indian GPT with IST Time & Universal Web Search!"}]
    }

if "current_chat" not in st.session_state:
    st.session_state.current_chat = "New Chat"

# Sidebar
with st.sidebar:
    if st.button("➕ New Chat", use_container_width=True):
        new_chat_name = "New Chat"
        counter = 1
        while new_chat_name in st.session_state.chat_sessions:
            new_chat_name = f"New Chat {counter}"
            counter += 1
        
        st.session_state.chat_sessions[new_chat_name] = [{"role": "assistant", "content": "Hi bro i am your personal chatbot Indian GPT with IST Time & Universal Web Search!"}]
        st.session_state.current_chat = new_chat_name
        st.rerun()

    st.markdown("---")
    st.subheader("📁 Upload Image")
    uploaded_image = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg"], label_visibility="collapsed")

    st.markdown("---")
    st.subheader("💬 Chat History")
    
    for chat_name in list(st.session_state.chat_sessions.keys()):
        if st.button(chat_name, use_container_width=True, key=f"btn_{chat_name}"):
            st.session_state.current_chat = chat_name
            st.rerun()

    st.markdown("---")
    st.caption("⚡ IST Time & Universal Google Search Active")
    st.caption("Indian GPT - Cloud Edition by Shubham")

# Main Header
st.title("🇮🇳 Indian GPT")

# Get current messages safely
if st.session_state.current_chat not in st.session_state.chat_sessions:
    st.session_state.current_chat = list(st.session_state.chat_sessions.keys())[0]

current_messages = st.session_state.chat_sessions[st.session_state.current_chat]

# Display current chat messages
for message in current_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "image_url" in message and message["image_url"]:
            st.image(message["image_url"])
        elif "image" in message and message["image"]:
            st.image(message["image"])

# Native Streamlit Chat Input
prompt = st.chat_input("Ki jante chas? (Ask anything or ask to generate an image...)")

if prompt:
    if st.session_state.current_chat.startswith("New Chat"):
        new_name = prompt[:25] + ("..." if len(prompt) > 25 else "")
        if new_name in st.session_state.chat_sessions:
            new_name = f"{new_name} (2)"
        
        st.session_state.chat_sessions[new_name] = st.session_state.chat_sessions.pop(st.session_state.current_chat)
        st.session_state.current_chat = new_name
        current_messages = st.session_state.chat_sessions[new_name]

    user_msg = {"role": "user", "content": prompt}
    if uploaded_image:
        user_msg["image"] = uploaded_image
    
    current_messages.append(user_msg)
    
    with st.chat_message("user"):
        st.markdown(prompt)
        if uploaded_image:
            st.image(uploaded_image)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        full_response = ""
        generated_image_url = None
        
        try:
            is_image_request = any(keyword in prompt.lower() for keyword in ["generate image", "draw", "picture of", "create an image", "chobi banao", "photo banao"])
            
            if is_image_request:
                thinking_html = """
                <div style="display: flex; align-items: center; gap: 6px; font-style: italic; color: #a5b4fc;">
                    <span>🎨 creating your image</span>
                    <span class="dot1" style="font-size: 20px;">.</span>
                    <span class="dot2" style="font-size: 20px;">.</span>
                    <span class="dot3" style="font-size: 20px;">.</span>
                </div>
                """
                message_placeholder.markdown(thinking_html, unsafe_allow_html=True)
                time.sleep(1)
                img_prompt = urllib.parse.quote(prompt)
                generated_image_url = f"https://image.pollinations.ai/prompt/{img_prompt}"
                full_response = f"Elo bhai, tor instructions moto chobi toiri kore diyechi:"
                message_placeholder.markdown(full_response)
                st.image(generated_image_url)
            else:
                # Universal smart check: triggers web search for anything except basic greetings
                greetings = ["hi", "hello", "hey", "hii", "hola", "sup", "good morning", "good evening", "bye"]
                is_simple_greeting = prompt.lower().strip() in greetings
                
                search_context = ""
                if not is_simple_greeting:
                    search_loading_html = """
                    <div style="display: flex; align-items: center; gap: 6px; font-style: italic; color: #a5b4fc;">
                        <span>🌐 searching in the google</span>
                        <span class="dot1" style="font-size: 20px;">.</span>
                        <span class="dot2" style="font-size: 20px;">.</span>
                        <span class="dot3" style="font-size: 20px;">.</span>
                    </div>
                    """
                    message_placeholder.markdown(search_loading_html, unsafe_allow_html=True)
                    search_context = search_web(prompt)
                else:
                    thinking_html = """
                    <div style="display: flex; align-items: center; gap: 6px; font-style: italic; color: #a5b4fc;">
                        <span>🤖 thinking your answer</span>
                        <span class="dot1" style="font-size: 20px;">.</span>
                        <span class="dot2" style="font-size: 20px;">.</span>
                        <span class="dot3" style="font-size: 20px;">.</span>
                    </div>
                    """
                    message_placeholder.markdown(thinking_html, unsafe_allow_html=True)
                
                # Indian Standard Time (IST - UTC+5:30)
                ist = timezone(timedelta(hours=5, minutes=30))
                current_time_str = datetime.now(ist).strftime("%Y-%m-%d %H:%M:%S")
                
                system_content = (
                    f"Current Indian Standard Time (IST) is {current_time_str}. "
                    "You are Indian GPT, an advanced AI search and assistant created by Shubham. "
                    "If anyone asks who created you or made you, always proudly answer that you were created by Shubham."
                )
                
                if search_context:
                    system_content += f"\n\nLive Web Search Results:\n{search_context}"

                current_api_key = get_active_key()
                models_to_test = get_available_models(current_api_key)
                headers = {
                    "Authorization": f"Bearer {current_api_key}",
                    "Content-Type": "application/json"
                }
                
                success = False
                for attempt in range(2):
                    if success:
                        break
                    for model_name in models_to_test:
                        payload = {
                            "model": model_name,
                            "messages": [
                                {"role": "system", "content": system_content},
                                {"role": "user", "content": prompt}
                            ],
                            "stream": True
                        }
                        
                        try:
                            response = requests.post(
                                "https://api.groq.com/openai/v1/chat/completions",
                                headers=headers,
                                json=payload,
                                stream=True,
                                timeout=15
                            )
                            
                            if response.status_code == 200:
                                for line in response.iter_lines():
                                    if line:
                                        line_str = line.decode("utf-8")
                                        if line_str.startswith("data: "):
                                            json_str = line_str[6:]
                                            if json_str != "[DONE]":
                                                try:
                                                    body = json.loads(json_str)
                                                    delta = body["choices"][0]["delta"]
                                                    if "content" in delta and delta["content"]:
                                                        resp_chunk = delta["content"]
                                                        full_response += resp_chunk
                                                        message_placeholder.markdown(full_response + "▌")
                                                except:
                                                    pass
                                message_placeholder.markdown(full_response)
                                success = True
                                break
                            elif response.status_code == 429:
                                time.sleep(1)
                                continue
                        except:
                            continue
                
                if not success:
                    full_response = "Server ekhon ektu busy ache ba limit cross hoyeche. Ektu por abar 'send' e click koro bhai!"
                    message_placeholder.markdown(full_response)
            
            assistant_msg = {"role": "assistant", "content": full_response}
            if generated_image_url:
                assistant_msg["image_url"] = generated_image_url
                
            current_messages.append(assistant_msg)
            st.rerun()    
        except Exception as e:
            st.error(f"Error: {e}")
