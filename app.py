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

# Custom CSS for Cyberpunk Theme & High Brightness AI Chip Background with Crystal Clear Text
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(5, 10, 25, 0.15), rgba(10, 15, 30, 0.20)), 
                    url('https://images.unsplash.com/photo-1620712943543-bcc4688e7485?q=80&w=1920&auto=format&fit=crop') no-repeat center center fixed;
        background-size: cover;
        color: #ffffff !important;
    }
    .stSidebar {
        background-color: rgba(15, 23, 42, 0.85) !important;
    }
    .stSidebar * {
        color: #ffffff !important;
    }
    h1, h2, h3, h4, h5, h6, p, span, label, li {
        color: #ffffff !important;
        opacity: 1 !important;
        text-shadow: 0px 2px 5px rgba(0, 0, 0, 0.98);
    }
    .stMarkdown p, .stMarkdown div {
        color: #ffffff !important;
        text-shadow: 0px 2px 5px rgba(0, 0, 0, 0.98);
    }
    .stSidebar h3, .stSidebar label, .stSidebar span {
        color: #4ade80 !important;
        font-weight: 700 !important;
    }
    .stChatInput textarea {
        color: #0f172a !important;
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

# Optimized models list prioritizing Llama 3 models to prevent language glitches
def get_available_models(api_key):
    return [
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant",
        "mixtral-8x7b-32768"
    ]

# Initialize Session States with a unique key
if "chat_sessions_v12" not in st.session_state:
    st.session_state.chat_sessions_v12 = {
        "New Chat": [{"role": "assistant", "content": "Hello! I am Indian GPT, your personal AI assistant created by Shubham. Ask me anything or tell me to generate an image!"}]
    }

if "current_chat_v12" not in st.session_state:
    st.session_state.current_chat_v12 = "New Chat"

# Sidebar Controls
with st.sidebar:
    if st.button("➕ New Chat", use_container_width=True):
        new_chat_name = "New Chat"
        counter = 1
        while new_chat_name in st.session_state.chat_sessions_v12:
            new_chat_name = f"New Chat {counter}"
            counter += 1
        
        st.session_state.chat_sessions_v12[new_chat_name] = [{"role": "assistant", "content": "Hello! New chat session started."}]
        st.session_state.current_chat_v12 = new_chat_name
        st.rerun()

    st.markdown("---")
    st.subheader("💬 Chat History")
    
    for chat_name in list(st.session_state.chat_sessions_v12.keys()):
        if st.button(chat_name, use_container_width=True, key=f"btn_{chat_name}"):
            st.session_state.current_chat_v12 = chat_name
            st.rerun()

    st.markdown("---")
    st.caption("⚡ Live Web Search & Full Memory Active")
    st.caption("Indian GPT - Cloud Edition by Shubham")

# Main Header
st.title("🇮🇳 Indian GPT")

# Get current messages safely
if st.session_state.current_chat_v12 not in st.session_state.chat_sessions_v12:
    st.session_state.current_chat_v12 = list(st.session_state.chat_sessions_v12.keys())[0]

current_messages = st.session_state.chat_sessions_v12[st.session_state.current_chat_v12]

# Display current chat messages
for message in current_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "image_url" in message and message["image_url"]:
            st.image(message["image_url"])

# Native Streamlit Chat Input (Clean & Full Width)
prompt = st.chat_input("Ask anything or type 'generate image of...' to create one...")

if prompt:
    if st.session_state.current_chat_v12.startswith("New Chat"):
        new_name = prompt[:25] + ("..." if len(prompt) > 25 else "")
        if new_name in st.session_state.chat_sessions_v12:
            new_name = f"{new_name} (2)"
        
        st.session_state.chat_sessions_v12[new_name] = st.session_state.chat_sessions_v12.pop(st.session_state.current_chat_v12)
        st.session_state.current_chat_v12 = new_name
        current_messages = st.session_state.chat_sessions_v12[new_name]

    user_msg = {"role": "user", "content": prompt}
    current_messages.append(user_msg)
    
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        full_response = ""
        generated_image_url = None
        
        try:
            p_lower = prompt.lower().strip()
            image_starters = ["generate image", "genarate image", "draw image", "create image", "make an image", "chobi banao", "chobi toiri koro", "draw a", "generate a picture", "create a picture", "banao ekta chobi"]
            is_image_request = any(p_lower.startswith(starter) or f" {starter}" in p_lower for starter in image_starters)
            
            if is_image_request:
                thinking_html = """
                <div style="display: flex; align-items: center; gap: 6px; font-style: italic; color: #a5b4fc;">
                    <span>🎨 creating high-quality masterpiece</span>
                    <span class="dot1" style="font-size: 20px;">.</span>
                    <span class="dot2" style="font-size: 20px;">.</span>
                    <span class="dot3" style="font-size: 20px;">.</span>
                </div>
                """
                message_placeholder.markdown(thinking_html, unsafe_allow_html=True)
                time.sleep(1)
                
                enhanced_prompt = f"{prompt}, highly detailed, cinematic lighting, 8k resolution, masterpiece, professional digital art, sharp focus"
                img_prompt = urllib.parse.quote(enhanced_prompt)
                generated_image_url = f"https://image.pollinations.ai/prompt/{img_prompt}?width=1024&height=1024&nologo=true"
                
                full_response = "Here is your high-quality generated image:"
                message_placeholder.markdown(full_response)
                st.image(generated_image_url)
            else:
                greetings = ["hi", "hello", "hey", "hii", "hola", "sup", "good morning", "good evening", "bye"]
                is_simple_greeting = prompt.lower().strip() in greetings
                
                search_triggers = ["who won", "news", "score", "weather", "latest", "current", "price", "who is", "what is happening"]
                needs_search = any(trig in p_lower for trig in search_triggers)
                
                search_context = ""
                if not is_simple_greeting and needs_search:
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
                
                ist = timezone(timedelta(hours=5, minutes=30))
                current_time_str = datetime.now(ist).strftime("%Y-%m-%d %H:%M:%S")
                
                system_content = (
                    f"Current Indian Standard Time (IST) is {current_time_str}. "
                    "You are Indian GPT, an advanced AI assistant created exclusively by Shubham. "
                    "If anyone asks who created you or made you, always proudly answer that you were created by Shubham. "
                    "STRICT LANGUAGE LOCK: You must ALWAYS respond in the exact same language, script, and style as the user's latest input message. "
                    "If the user writes in English, reply in English. If the user writes in Romanized Bengali/Hinglish/Banglish (e.g. 'bhai ki korchis' or 'kya hal hai'), reply back in that exact same Romanized style. "
                    "NEVER switch to Arabic, Urdu script, or any other unrequested language under any circumstances."
                )
                
                if search_context:
                    system_content += f"\n\nLive Web Search Results:\n{search_context}"

                messages_payload = [{"role": "system", "content": system_content}]
                for msg in current_messages[:-1]:
                    role = msg["role"]
                    content = msg["content"]
                    if role in ["user", "assistant"]:
                        messages_payload.append({"role": role, "content": content})
                
                messages_payload.append({"role": "user", "content": prompt})

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
                            "messages": messages_payload,
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
                                success = success or (len(full_response.strip()) > 0)
                                if success:
                                    break
                            elif response.status_code == 429:
                                time.sleep(1)
                                continue
                        except:
                            continue
                
                if not success:
                    full_response = "Server is currently busy or rate limited. Please click send again!"
                    message_placeholder.markdown(full_response)
            
            assistant_msg = {"role": "assistant", "content": full_response}
            if generated_image_url:
                assistant_msg["image_url"] = generated_image_url
                
            current_messages.append(assistant_msg)
            st.rerun()    
        except Exception as e:
            st.error(f"Error: {e}")
