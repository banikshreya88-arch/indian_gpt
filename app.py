import streamlit as st
import requests
import json
import urllib.parse
import time
import math
from datetime import datetime, timezone, timedelta

# ==========================================
# PAGE CONFIGURATION & METADATA
# ==========================================
st.set_page_config(
    page_title="Indian GPT - Advanced Multi-Modal AI Ecosystem",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# CYBERPUNK & PROFESSIONAL UI STYLING
# ==========================================
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(5, 10, 25, 0.20), rgba(10, 15, 30, 0.25)), 
                    url('https://images.unsplash.com/photo-1620712943543-bcc4688e7485?q=80&w=1920&auto=format&fit=crop') no-repeat center center fixed;
        background-size: cover;
        color: #ffffff !important;
    }
    .stSidebar {
        background-color: rgba(15, 23, 42, 0.90) !important;
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

# ==========================================
# API KEYS POOL & CONFIGURATION
# ==========================================
KEYS_POOL = [
    "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",
    "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",
    "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",
]

sec_key = st.secrets.get("GROQ_API_KEY_2", "")
if sec_key and sec_key not in KEYS_POOL:
    KEYS_POOL.append(sec_key)

def get_next_key(index):
    return KEYS_POOL[index % len(KEYS_POOL)]

TAVILY_API_KEY = "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"

def search_web(query):
    search_text = ""
    try:
        if TAVILY_API_KEY:
            payload = {
                "api_key": TAVILY_API_KEY,
                "query": query,
                "max_results": 4,
                "include_images": False
            }
            resp = requests.post("https://api.tavily.com/search", json=payload, timeout=8)
            if resp.status_code == 200:
                data = resp.json()
                results = data.get("results", [])
                text_snippets = [f"Title: {r.get('title')}\nContent: {r.get('content')}" for r in results]
                search_text = "\n\n".join(text_snippets)
    except:
        pass
    return search_text

# ==========================================
# MASSIVE KNOWLEDGE CORPUS & MATH SOLVER ENGINE
# ==========================================
LOCAL_CORPUS = {
    # Identity & Creator
    "who made you": "I am Indian GPT, an advanced conversational AI ecosystem designed, developed, and deployed exclusively by Shubham.",
    "who created you": "I was created, coded, and built by Shubham as a high-performance sovereign AI system.",
    "tui ke": "Ami Indian GPT, ekta AI assistant jake Shubham toiri koreche!",
    "amar nam ki": "Tor nam Shubham! Tui amake baniyechis.",
    
    # India Geography & Symbols
    "india capital": "New Delhi is the capital of India.",
    "capital of india": "New Delhi is the capital of India.",
    "national bird of india": "The Indian Peafowl (Pavo cristatus), commonly known as the peacock, is the national bird of India.",
    "national animal of india": "The Royal Bengal Tiger is the national animal of India.",
    "national flower of india": "Lotus (Nelumbo nucifera) is the national flower of India.",
    "national tree of india": "Banyan Tree (Ficus benghalensis) is the national tree of India.",
    "national fruit of india": "Mango (Mangifera indica) is the national fruit of India.",
    "national anthem": "Jana Gana Mana, penned by Nobel laureate Rabindranath Tagore, is the national anthem of India.",
    "national song": "Vande Mataram, composed by Bankim Chandra Chatterjee, is the national song of India.",
    
    # Indian History & Freedom Struggle
    "history of india": "Indian history spans over five millennia, beginning with the Indus Valley Civilization (Harappan Civilization), moving through the Vedic period, powerful Maurya and Gupta empires, medieval sultanates and the Mughal Empire, British colonial rule, and historic independence in 1947.",
    "independence day": "India gained freedom from British colonial rule on August 15, 1947.",
    "republic day": "India became a Sovereign Democratic Republic on January 26, 1950, when the Constitution of India came into force.",
    "constitution of india": "The Constitution of India is the supreme law, drafted by a constituent assembly chaired by Dr. B. R. Ambedkar, and adopted on January 26, 1950.",
    "freedom fighters": "India's independence movement was shaped by legends including Netaji Subhash Chandra Bose, Mahatma Gandhi, Bhagat Singh, Sardar Vallabhbhai Patel, Rani Lakshmibai, Subhash Chandra Bose, Khudiram Bose, and Chandra Shekhar Azad.",
    "netaji": "Netaji Subhash Chandra Bose formed the Azad Hind Fauj (Indian National Army) and gave the immortal battle cry: 'Tum mujhe khoon do, main tumhe azadi dunga!'",
    "taj mahal": "The Taj Mahal in Agra is an ivory-white marble mausoleum built by Mughal Emperor Shah Jahan for his wife Mumtaz Mahal, recognized as one of the New Seven Wonders of the World.",
    
    # World History & Civilizations
    "world history": "World history encompasses the study of human past from ancient civilizations (Mesopotamia, Ancient Egypt, Indus Valley, Ancient China, Ancient Greece, Roman Empire) through the Middle Ages, Renaissance, Age of Discovery, Industrial Revolution, World Wars I and II, to the modern digital age.",
    "world war 1": "World War I (1914–1918) was a global conflict centered in Europe, fought between the Allied Powers (Great Britain, France, Russia, Italy, Japan, and later the US) and the Central Powers (Germany, Austria-Hungary, Ottoman Empire, and Bulgaria).",
    "world war 2": "World War II (1939–1945) was a devastating global war involving over 30 countries, pitting the Allies (Britain, Soviet Union, US, China) against the Axis powers (Germany, Japan, Italy).",
    "ancient civilizations": "Major cradles of ancient civilization include Mesopotamia (Tigris-Euphrates valley), Ancient Egypt (Nile valley), Indus Valley Civilization (Indus river basin), and Ancient China (Yellow River basin).",
    "french revolution": "The French Revolution (1789–1799) was a watershed period in European and world history that overthrew the absolute monarchy, established a republic, and championed principles of Liberty, Equality, and Fraternity.",
    
    # Science, Physics & Space
    "speed of light": "The speed of light in a vacuum is exactly $c = 299,792,458 \\text{ meters per second}$ (approximately $3 \\times 10^8 \\text{ m/s}$).",
    "gravity": "Acceleration due to gravity on Earth is approximately $9.81 \\text{ m/s}^2$ near the Earth's surface, as described by Newton's law of universal gravitation.",
    "einstein mass energy": "Albert Einstein's mass-energy equivalence formula is $E = mc^2$, stating that energy equals mass multiplied by the speed of light squared.",
    "chandrayaan": "Chandrayaan is India's historic lunar exploration programme managed by ISRO. Chandrayaan-3 successfully landed near the lunar south pole in August 2023.",
    "photosynthesis": "Photosynthesis is the biochemical process by which green plants, algae, and some bacteria convert light energy into chemical energy, producing glucose and oxygen from carbon dioxide and water.",
    
    # Computer Science & Mathematics
    "python": "Python is a high-level, interpreted, general-purpose programming language created by Guido van Rossum, known for dynamic typing, garbage collection, and extensive libraries for AI and web engineering.",
    "streamlit": "Streamlit is an open-source Python library that enables data scientists and developers to construct interactive web applications quickly using pure Python scripts.",
    "quadratic formula": "The roots of a quadratic equation $ax^2 + bx + c = 0$ are given by the quadratic formula: $x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}$."
}

def solve_math_locally(query_str):
    q = query_str.lower()
    try:
        if "quadratic" in q or ("ax^2" in q) or ("roots" in q):
            return "To solve a quadratic equation of the form $ax^2 + bx + c = 0$, use the quadratic formula:\n$$x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}$$\nHere, the discriminant $\\Delta = b^2 - 4ac$ determines the nature of the roots: if $\\Delta > 0$ (two distinct real roots), $\\Delta = 0$ (one repeated real root), and $\\Delta < 0$ (complex conjugate roots)."
        elif "pythagoras" in q or "right angle triangle" in q:
            return "According to Pythagorean theorem for a right-angled triangle with legs $a$ and $b$ and hypotenuse $c$:\n$$a^2 + b^2 = c^2$$\nThus, $c = \\sqrt{a^2 + b^2}$."
        elif "area of circle" in q:
            return "The area $A$ of a circle with radius $r$ is calculated as:\n$$A = \\pi r^2$$"
        elif "area of triangle" in q:
            return "The area of a triangle with base $b$ and height $h$ is:\n$$A = \\frac{1}{2} \\times b \\times h$$"
    except:
        pass
    return None

def get_local_fallback(query_str):
    q_lower = query_str.lower().strip()
    
    # Check Math solver first
    math_ans = solve_math_locally(q_lower)
    if math_ans:
        return math_ans
        
    # Check knowledge corpus
    for key, ans in LOCAL_CORPUS.items():
        if key in q_lower:
            return ans
    return None

# ==========================================
# GROQ MODEL DISCOVERY & UTILITIES
# ==========================================
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
                if not any(k in m_id.lower() for k in ["whisper", "guard", "orpheus", "audio"]):
                    fetched.append(m_id)
            if fetched:
                return fetched
    except:
        pass
    return default_models

# ==========================================
# SESSION STATE INITIALIZATION
# ==========================================
if "chat_sessions_v80" not in st.session_state:
    st.session_state.chat_sessions_v80 = {
        "New Chat": [{"role": "assistant", "content": "Namaste! I am Indian GPT, your sovereign multi-lingual AI assistant created by Shubham. Ask me anything in any Indian language or world topic, or type 'generate image of...' for HD art!"}]
    }

if "current_chat_v80" not in st.session_state:
    st.session_state.current_chat_v80 = "New Chat"

# ==========================================
# SIDEBAR INTERFACE & CONTROLS
# ==========================================
with st.sidebar:
    if st.button("➕ New Chat", use_container_width=True):
        new_chat_name = "New Chat"
        counter = 1
        while new_chat_name in st.session_state.chat_sessions_v80:
            new_chat_name = f"New Chat {counter}"
            counter += 1
        
        st.session_state.chat_sessions_v80[new_chat_name] = [{"role": "assistant", "content": "Hello! New sovereign chat session started."}]
        st.session_state.current_chat_v80 = new_chat_name
        st.rerun()

    st.markdown("---")
    st.subheader("💬 Active Sessions")
    
    for chat_name in list(st.session_state.chat_sessions_v80.keys()):
        if st.button(chat_name, use_container_width=True, key=f"btn_{chat_name}"):
            st.session_state.current_chat_v80 = chat_name
            st.rerun()

    st.markdown("---")
    
    # Export Chat to TXT Feature
    current_msgs = st.session_state.chat_sessions_v80[st.session_state.current_chat_v80]
    chat_export_text = ""
    for m in current_msgs:
        chat_export_text += f"{m['role'].upper()}: {m['content']}\n\n"
    
    st.download_button(
        label="📥 Export Chat (TXT)",
        data=chat_export_text,
        file_name="indian_gpt_session.txt",
        mime="text/plain",
        use_container_width=True
    )

    st.markdown("---")
    st.caption("🌐 Multi-Lingual & Multi-Modal Engine")
    st.caption("Indian GPT - Sovereign Edition by Shubham")

# ==========================================
# MAIN APP HEADER & CHAT INTERFACE
# ==========================================
st.title("🇮🇳 Indian GPT")
st.markdown("##### *Sovereign Multi-Lingual AI Ecosystem supporting Indian Languages, World History & Complex Mathematics*")

if st.session_state.current_chat_v80 not in st.session_state.chat_sessions_v80:
    st.session_state.current_chat_v80 = list(st.session_state.chat_sessions_v80.keys())[0]

current_messages = st.session_state.chat_sessions_v80[st.session_state.current_chat_v80]

# Render message history
for message in current_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "image_bytes" in message and message["image_bytes"]:
            st.image(message["image_bytes"])

# Native Streamlit Chat Input
prompt = st.chat_input("Ask anything in any Indian language or world topic, solve math, or type 'generate image of...'...")

if prompt:
    if st.session_state.current_chat_v80.startswith("New Chat"):
        new_name = prompt[:25] + ("..." if len(prompt) > 25 else "")
        if new_name in st.session_state.chat_sessions_v80:
            new_name = f"{new_name} (2)"
        
        st.session_state.chat_sessions_v80[new_name] = st.session_state.chat_sessions_v80.pop(st.session_state.current_chat_v80)
        st.session_state.current_chat_v80 = new_name
        current_messages = st.session_state.chat_sessions_v80[new_name]

    user_msg = {"role": "user", "content": prompt}
    current_messages.append(user_msg)
    
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        full_response = ""
        generated_image_bytes = None
        
        try:
            p_lower = prompt.lower().strip()
            image_starters = ["generate", "genarate", "draw", "create", "make", "chobi", "banao", "toiri", "pic", "photo", "image", "ghibli"]
            is_image_request = any(starter in p_lower for starter in image_starters)
            
            if is_image_request:
                steps = [
                    "🎨 Analyzing visual prompt and multi-layered depth...",
                    "📐 Constructing high-resolution composition layout...",
                    "✨ Rendering hyper-realistic lighting, textures & details...",
                    "🚀 Finalizing ultra-HD masterpiece via Neural Engine..."
                ]
                
                for step_text in steps:
                    step_html = f"""
                    <div style="display: flex; align-items: center; gap: 6px; font-style: italic; color: #a5b4fc;">
                        <span>{step_text}</span>
                        <span class="dot1" style="font-size: 20px;">.</span>
                        <span class="dot2" style="font-size: 20px;">.</span>
                        <span class="dot3" style="font-size: 20px;">.</span>
                    </div>
                    """
                    message_placeholder.markdown(step_html, unsafe_allow_html=True)
                    time.sleep(0.8)
                
                enhanced_prompt = f"{prompt}, highly detailed, professional photography, stunning composition, 8k resolution, photorealistic masterpiece"
                encoded_prompt = urllib.parse.quote(enhanced_prompt)
                image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&model=flux&nologo=true"
                
                try:
                    img_resp = requests.get(image_url, timeout=35)
                    if img_resp.status_code == 200 and len(img_resp.content) > 1000:
                        generated_image_bytes = img_resp.content
                        full_response = "Here is your generated high-definition masterpiece:"
                    else:
                        full_response = "Could not render image. Please try again!"
                except:
                    full_response = "Image generation took longer than expected. Please try again!"
                
                message_placeholder.markdown(full_response)
                if generated_image_bytes:
                    st.image(generated_image_bytes)
            else:
                greetings = ["hi", "hello", "hey", "hii", "hola", "sup", "good morning", "good evening", "bye", "namaste", "pranam"]
                is_simple_greeting = p_lower in greetings
                
                search_triggers = ["winner", "jiteche", "won", "match", "score", "news", "current", "ajke", "ekhon", "latest", "2026", "who won"]
                needs_search = any(trigger in p_lower for trigger in search_triggers) and not is_simple_greeting
                
                search_context = ""
                
                if needs_search:
                    search_loading_html = """
                    <div style="display: flex; align-items: center; gap: 6px; font-style: italic; color: #a5b4fc;">
                        <span>🌐 searching live web info</span>
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
                
                # ==========================================
                # ADVANCED MULTI-LINGUAL GOVERNANCE SYSTEM PROMPT
                # ==========================================
                system_content = (
                    f"Current Indian Standard Time (IST) is {current_time_str}. "
                    "You are Indian GPT, an advanced sovereign AI assistant created exclusively by Shubham. "
                    "If anyone asks who created you or made you, always proudly answer that you were created by Shubham. "
                    "SOVEREIGN MULTI-LINGUAL GOVERNANCE DIRECTIVE (CRITICAL & NON-NEGOTIABLE): "
                    "1. You are fully capable of understanding, processing, and generating responses in ALL scheduled Indian languages and scripts "
                    "(including Bengali, Hindi, Telugu, Marathi, Tamil, Urdu, Gujarati, Malayalam, Kannada, Odia, Punjabi, Assamese, Sanskrit, Kashmiri, Sindhi, Konkani, Manipuri, Nepali, Dogri, Maithili, Santhali, Bodo) "
                    "along with English, Banglish, and Hinglish. "
                    "2. You must ALWAYS match and reply in the exact same language, script, and regional style as the user's input. "
                    "3. Provide deep, accurate, and intellectual explanations for world history, Indian history, complex mathematics, science, and technology."
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

                success = False
                for key_idx in range(len(KEYS_POOL)):
                    if success:
                        break
                    current_api_key = get_next_key(key_idx)
                    models_to_test = get_available_models(current_api_key)
                    headers = {
                        "Authorization": f"Bearer {current_api_key}",
                        "Content-Type": "application/json"
                    }
                    
                    for model_name in models_to_test:
                        if success:
                            break
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
                
                # Fallback to massive local corpus if API fails
                if not success:
                    local_ans = get_local_fallback(prompt)
                    if local_ans:
                        full_response = local_ans
                        success = True
                    else:
                        full_response = "Namaste! Server is currently processing high volume. Please click send again!"
                    message_placeholder.markdown(full_response)
            
            assistant_msg = {"role": "assistant", "content": full_response}
            if generated_image_bytes:
                assistant_msg["image_bytes"] = generated_image_bytes
                
            current_messages.append(assistant_msg)
            st.rerun()    
        except Exception as e:
            st.error(f"Error: {e}")
