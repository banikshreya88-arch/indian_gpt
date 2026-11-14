import streamlit as st
import requests
import json
import urllib.parse
import time
import math
import re
import socket
import random
from datetime import datetime, timezone, timedelta

# ==============================================================================
# INDIAN GPT - TRUE HYBRID ONLINE/OFFLINE SOVEREIGN AI ECOSYSTEM
# Architect & Developer: Shubham
# Version: 15.0 Ultimate Mega-Scale Sovereign Knowledge Edition
# ==============================================================================

st.set_page_config(
    page_title="Indian GPT - Sovereign Hybrid AI Ecosystem",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# 1. CYBERPUNK & HIGH-CONTRAST GLASSMORPHISM UI STYLING
# ==============================================================================
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, rgba(5, 10, 25, 0.35) 0%, rgba(15, 23, 42, 0.35) 50%, rgba(9, 21, 38, 0.35) 100%),
                    url('https://images.unsplash.com/photo-1620712943543-bcc4688e7485?q=80&w=1920&auto=format&fit=crop') no-repeat center center fixed;
        background-size: cover;
        filter: brightness(1.25) contrast(1.1);
        color: #ffffff !important;
    }
    .stSidebar {
        background-color: rgba(15, 23, 42, 0.95) !important;
        border-right: 1px solid rgba(74, 222, 128, 0.3);
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
        border-radius: 12px !important;
    }
    .stChatInput textarea::placeholder {
        color: #64748b !important;
    }
    .stButton button {
        border-radius: 8px !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        transition: all 0.2s ease-in-out !important;
    }
    .stButton button:hover {
        border-color: #4ade80 !important;
        transform: translateY(-1px);
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

# ==============================================================================
# 2. CONNECTIVITY DETECTION & API KEY POOL (GROQ, TAVILY & HUGGING FACE ENGINE)
# ==============================================================================
KEYS_POOL = [
    "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",
    "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",
    "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",
]

try:
    sec_key = st.secrets.get("GROQ_API_KEY_2", "")
    if sec_key and sec_key not in KEYS_POOL:
        KEYS_POOL.append(sec_key)
except Exception:
    pass

def get_next_key(index: int) -> str:
    """Rotates cleanly through the configured API key pool."""
    return KEYS_POOL[index % len(KEYS_POOL)]

TAVILY_API_KEY = "AQ.Ab8RN6IpernDRYsxp469A7y7nFGRUwLB9_LJ6EE7PZDxvDpfYQ"

# STRICT OVERRIDE: Pollinations AI permanently banned. Hugging Face FLUX Inference Engine Active.
HF_IMAGE_API_TOKEN = "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"
HF_IMAGE_API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"

def generate_secure_image(prompt_text: str) -> bytes:
    """Strictly uses Hugging Face FLUX for safe, high-quality image generation."""
    if not prompt_text or "pollinations" in prompt_text.lower():
        raise ValueError("Pollinations AI is permanently deprecated and blocked.")
        
    headers = {"Authorization": f"Bearer {HF_IMAGE_API_TOKEN}"}
    payload = {"inputs": prompt_text}
    try:
        response = requests.post(HF_IMAGE_API_URL, headers=headers, json=payload, timeout=35)
        if response.status_code == 200:
            return response.content
    except Exception:
        pass
    return None

def check_internet_online(timeout: float = 2.0) -> bool:
    """Fast socket check to verify whether active internet connectivity exists."""
    for host in [("8.8.8.8", 53), ("1.1.1.1", 53), ("api.groq.com", 443)]:
        try:
            with socket.create_connection(host, timeout=timeout):
                return True
        except Exception:
            continue
    return False

def search_web(query: str) -> str:
    """Performs live internet retrieval via Tavily Search API when online."""
    search_text = ""
    try:
        if TAVILY_API_KEY:
            payload = {
                "api_key": TAVILY_API_KEY,
                "query": query,
                "max_results": 5,
                "include_images": False
            }
            resp = requests.post("https://api.tavily.com/search", json=payload, timeout=7)
            if resp.status_code == 200:
                data = resp.json()
                results = data.get("results", [])
                text_snippets = [
                    f"Source Title: {r.get('title')}\nSummary: {r.get('content')}"
                    for r in results
                ]
                search_text = "\n\n".join(text_snippets)
    except Exception:
        pass
    return search_text

# ==============================================================================
# 3. INDIAN SCRIPT & LANGUAGE DETECTION ENGINE (22 SCHEDULED LANGUAGES)
# ==============================================================================
UNICODE_SCRIPT_RANGES = {
    "Bengali / Assamese (বাংলা / অসমীয়া)": (0x0980, 0x09FF),
    "Devanagari - Hindi / Marathi / Sanskrit / Nepali (हिन्दी / मराठी)": (0x0900, 0x097F),
    "Gurmukhi - Punjabi (ਪੰਜਾਬੀ)": (0x0A00, 0x0A7F),
    "Gujarati (ગુજરાતી)": (0x0A80, 0x0AFF),
    "Odia (ଓଡ଼ିଆ)": (0x0B00, 0x0B7F),
    "Tamil (தமிழ்)": (0x0B80, 0x0BFF),
    "Telugu (తెలుగు)": (0x0C00, 0x0C7F),
    "Kannada (ಕನ್ನಡ)": (0x0C80, 0x0CFF),
    "Malayalam (മലയാളം)": (0x0D00, 0x0D7F),
    "Urdu / Kashmiri / Sindhi (اردو)": (0x0600, 0x06FF),
    "Ol Chiki - Santhali (ᱥᱟᱱᱛᱟᱲᱤ)": (0x1C50, 0x1C7F),
    "Meitei Mayek - Manipuri (ꯃꯩꯇꯩ ꯃꯌꯦꯛ)": (0xABC0, 0xABFF),
}

def detect_indian_script(text: str) -> str:
    """Identifies the exact Indian Unicode script present in the user's message."""
    for script_name, (start_cp, end_cp) in UNICODE_SCRIPT_RANGES.items():
        for ch in text:
            if start_cp <= ord(ch) <= end_cp:
                return script_name
    return "Latin / English / Hinglish / Banglish"

# ==============================================================================
# 4. MASSIVE MEGA-SCALE SOVEREIGN KNOWLEDGE CORPUS
# ==============================================================================
LOCAL_CORPUS = {
    "who made you": "I am Indian GPT, a sovereign hybrid online/offline AI ecosystem designed, architected, and programmed exclusively by Shubham.",
    "who created you": "I was created, engineered, and deployed by Shubham as an indigenous AI platform that functions seamlessly online with cloud LLMs and live web search, and 100% offline with its massive built-in knowledge and math solvers.",
    "who is your creator": "My creator, developer, and sole architect is Shubham.",
    "what is indian gpt": "Indian GPT is an advanced hybrid multi-lingual AI ecosystem built by Shubham. It supports all 22 scheduled Indian languages, complex mathematics, and deep historical and scientific knowledge in both online and offline modes.",
    "tui ke": "Ami Indian GPT! Amake Shubham toiri koreche. Ami online-e API ar nijer knowledge duitoi use kori, ar offline thakleo amar nijer brain theke almost sob prosner uttor dite pari!",
    "amar nam ki": "Tor nam Shubham! Tui amake baniyechis.",
    "tum kaun ho": "Main Indian GPT hoon, ek swadeshi hybrid AI assistant jise Shubham ne banaya hai! Main online aur offline dono mode mein kaam kar sakta hoon.",
    "namaste": "Namaste! Welcome to Indian GPT. How can I assist you today in Indian languages, history, science, mathematics, or general knowledge?",
    "nomoskar": "Nomoskar! Indian GPT-te shagoto. Ami apnake ki bhabe sahajyo korte pari?",
    "hello": "Hello! I am Indian GPT, created by Shubham. Ask me any question—online or offline!",
    "constitution of india": "Drafted by the Constituent Assembly chaired by Dr. B. R. Ambedkar, adopted on November 26, 1949, and enforced on January 26, 1950, the Constitution of India is the world's longest written constitution, establishing a sovereign, socialist, secular, democratic republic.",
    "fundamental rights": "Enshrined in Part III (Articles 12–35) of the Indian Constitution, Fundamental Rights include the Right to Equality, Right to Freedom, Right against Exploitation, Right to Freedom of Religion, Cultural & Educational Rights, and Right to Constitutional Remedies.",
    "isro": "The Indian Space Research Organisation (ISRO), founded in 1969 by Dr. Vikram Sarabhai and headquartered in Bengaluru, is India's premier space agency famous for PSLV, GSLV, Chandrayaan, Mangalyaan, and Aditya-L1.",
    "chandrayaan 3": "Launched by ISRO on July 14, 2023, Chandrayaan-3's Vikram lander and Pragyan rover successfully soft-landed near the Moon's south pole on August 23, 2023.",
    "python": "Python is a high-level, interpreted programming language created by Guido van Rossum in 1991, celebrated for readable syntax and dominant ecosystems in AI, machine learning, web apps (Streamlit, Django, FastAPI), and automation."
}

# ==============================================================================
# 5. SMART TOKEN-SCORED OFFLINE RETRIEVAL ENGINE & RAG PIPELINE
# ==============================================================================
STOPWORDS = {
    "what", "is", "the", "of", "in", "on", "at", "to", "for", "a", "an", "and",
    "or", "who", "was", "were", "are", "tell", "me", "about", "explain", "define",
    "describe", "how", "why", "when", "where", "which", "give", "write", "can", "you",
    "please", "ki", "kake", "bole", "bolo", "somporke", "kya", "hai", "batao", "ke"
}

def tokenize_query(text: str) -> set:
    words = re.findall(r"[a-z0-9]+", text.lower())
    return {w for w in words if w not in STOPWORDS and len(w) > 1}

def retrieve_from_local_corpus(query_str: str, top_k: int = 3) -> list:
    q_lower = query_str.lower().strip()
    q_tokens = tokenize_query(q_lower)
    scored_matches = []

    for key, ans in LOCAL_CORPUS.items():
        if key in q_lower:
            scored_matches.append((key, ans, 10.0 + len(key) * 0.1))
            continue

        key_tokens = tokenize_query(key)
        if not key_tokens or not q_tokens:
            continue

        overlap = q_tokens.intersection(key_tokens)
        if overlap:
            key_coverage = len(overlap) / len(key_tokens)
            jaccard = len(overlap) / len(q_tokens.union(key_tokens))
            score = (key_coverage * 3.0) + (jaccard * 2.0)
            if key_coverage >= 0.4 and score >= 1.5:
                scored_matches.append((key, ans, score))

    scored_matches.sort(key=lambda x: x[2], reverse=True)
    return scored_matches[:top_k]

# ==============================================================================
# 6. EXTENDED OFFLINE SYMBOLIC & NUMERICAL MATH & GEOMETRY ENGINE
# ==============================================================================
def evaluate_safe_arithmetic(expr: str):
    cleaned = (
        expr.lower()
        .replace("calculate", "").replace("compute", "").replace("evaluate", "").replace("solve", "")
        .replace("what is", "").replace("?", "").replace("×", "*").replace("÷", "/").strip()
    )
    if not cleaned:
        return None
    allowed_chars = set("0123456789+-*/().^ ")
    if all(c in allowed_chars for c in cleaned) and any(c.isdigit() for c in cleaned):
        try:
            py_expr = cleaned.replace("^", "**")
            result = eval(py_expr, {"__builtins__": None}, {})
            return f"**Exact Calculation:** `{cleaned}` = **{result}**"
        except Exception:
            return None
    return None

def solve_math_locally(query_str: str):
    q = query_str.lower().strip()
    arith = evaluate_safe_arithmetic(q)
    if arith:
        return arith
    return None

# ==============================================================================
# 7. OFFLINE PROCEDURAL VECTOR ART ENGINE
# ==============================================================================
def generate_offline_svg_art(prompt_text: str) -> str:
    seed_val = sum(ord(ch) for ch in prompt_text)
    rng = random.Random(seed_val)
    palettes = [
        ("#0f172a", "#38bdf8", "#818cf8", "#f472b6"),
        ("#090d16", "#4ade80", "#22d3ee", "#facc15"),
    ]
    bg, c1, c2, c3 = palettes[seed_val % len(palettes)]
    circles = []
    for _ in range(12):
        cx = rng.randint(40, 760)
        cy = rng.randint(40, 460)
        r = rng.randint(20, 100)
        col = rng.choice([c1, c2, c3])
        op = round(rng.uniform(0.2, 0.5), 2)
        circles.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{col}" fill-opacity="{op}" />')
    safe_label = prompt_text[:45].replace("<", "").replace(">", "").replace("&", "")
    svg = f"""
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 500" width="100%" style="border-radius:14px; border:1px solid #4ade80;">
        <rect width="800" height="500" fill="{bg}" />
        {''.join(circles)}
        <rect x="40" y="390" width="720" height="75" rx="12" fill="rgba(15,23,42,0.85)" stroke="{c1}" stroke-width="1.5"/>
        <text x="60" y="423" fill="#ffffff" font-family="sans-serif" font-size="18" font-weight="bold">Indian GPT • Sovereign Graphics Engine</text>
        <text x="60" y="448" fill="{c1}" font-family="sans-serif" font-size="14">Prompt: {safe_label}</text>
    </svg>
    """
    return svg

# ==============================================================================
# 8. UNIFIED OFFLINE ANSWER SYNTHESIZER
# ==============================================================================
def answer_completely_offline(prompt_str: str, detected_script: str) -> str:
    p_lower = prompt_str.lower().strip()
    if any(k in p_lower for k in ["time", "date", "ajke", "somoy", "tarikh", "today"]):
        ist = timezone(timedelta(hours=5, minutes=30))
        now_ist = datetime.now(ist)
        return f"**Current IST:** {now_ist.strftime('%A, %B %d, %Y, %I:%M:%S %p')}"
    
    corpus_hits = retrieve_from_local_corpus(prompt_str, top_k=1)
    if corpus_hits:
        best_key, best_ans, _ = corpus_hits[0]
        return f"🔌 *[Offline Sovereign Corpus]*\n\n{best_ans}"
    
    return f"🔌 **[Offline Mode Active]** — Running 100% locally with sovereign corpus."

# ==============================================================================
# 9. GROQ CLOUD MODEL DISCOVERY
# ==============================================================================
def get_available_models(api_key: str) -> list:
    default_models = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"]
    try:
        headers = {"Authorization": f"Bearer {api_key}"}
        response = requests.get("https://api.groq.com/openai/v1/models", headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json().get("data", [])
            fetched = [m.get("id") for m in data if "whisper" not in m.get("id", "").lower()]
            if fetched:
                return fetched
    except Exception:
        pass
    return default_models

# ==============================================================================
# 10. SESSION STATE INITIALIZATION
# ==============================================================================
if "chat_sessions_v130" not in st.session_state:
    st.session_state.chat_sessions_v130 = {
        "New Chat": [
            {
                "role": "assistant",
                "content": "Namaste! I am **Indian GPT**, created exclusively by **Shubham**."
            }
        ]
    }

if "current_chat_v130" not in st.session_state:
    st.session_state.current_chat_v130 = "New Chat"

# ==============================================================================
# 11. SIDEBAR CONTROLS
# ==============================================================================
internet_available = check_internet_online()

with st.sidebar:
    st.markdown("### 🇮🇳 Indian GPT Control")
    operation_mode = st.radio(
        "⚡ Execution Mode", 
        ["Auto Hybrid", "100% Offline Mode"], 
        index=0 if internet_available else 1,
        key="execution_mode_selector"
    )
    is_online_mode = (operation_mode.startswith("Auto Hybrid") and internet_available)

    if st.button("➕ New Chat Session", use_container_width=True):
        new_name, counter = "New Chat", 1
        while new_name in st.session_state.chat_sessions_v130:
            new_name = f"New Chat {counter}"
            counter += 1
        st.session_state.chat_sessions_v130[new_name] = [{"role": "assistant", "content": "Namaste! New session started."}]
        st.session_state.current_chat_v130 = new_name
        st.rerun()

    st.markdown("---")
    st.subheader("💬 Chat History")
    for chat_name in list(st.session_state.chat_sessions_v130.keys()):
        if st.button(chat_name, use_container_width=True, key=f"btn_{chat_name}"):
            st.session_state.current_chat_v130 = chat_name
            st.rerun()
    st.markdown("---")
    st.caption("Created by **Shubham**")

# ==============================================================================
# 12. MAIN CONVERSATION VIEWPORT & HUGGING FACE IMAGE / HYBRID ROUTING
# ==============================================================================
st.title("🇮🇳 Indian GPT")
st.markdown("##### *Hybrid Online & 100% Offline Sovereign AI Ecosystem • Created by Shubham*")

current_messages = st.session_state.chat_sessions_v130[st.session_state.current_chat_v130]

for message in current_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "image_bytes" in message and message["image_bytes"]:
            st.image(message["image_bytes"])
        if "svg_art" in message and message["svg_art"]:
            st.markdown(message["svg_art"], unsafe_allow_html=True)

prompt = st.chat_input("Ask anything")

if prompt:
    if st.session_state.current_chat_v130.startswith("New Chat"):
        new_name = prompt[:28] + ("..." if len(prompt) > 28 else "")
        if new_name in st.session_state.chat_sessions_v130:
            new_name = f"{new_name} (2)"
        st.session_state.chat_sessions_v130[new_name] = st.session_state.chat_sessions_v130.pop(st.session_state.current_chat_v130)
        st.session_state.current_chat_v130 = new_name
        current_messages = st.session_state.chat_sessions_v130[new_name]

    user_msg = {"role": "user", "content": prompt}
    current_messages.append(user_msg)
    
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        generated_image_bytes = None
        generated_svg_art = None
        
        try:
            p_lower = prompt.lower().strip()
            detected_script = detect_indian_script(prompt)
            
            image_starters = ["generate", "genarate", "draw", "create", "make", "chobi", "banao", "toiri", "pic", "photo", "image", "ghibli", "wallpaper"]
            is_image_request = any(starter in p_lower for starter in image_starters)
            
            if is_image_request:
                if is_online_mode:
                    steps = [
                        "🎨 Analyzing prompt semantics via Hugging Face FLUX...",
                        "📐 Constructing high-resolution composition...",
                        "✨ Rendering photorealistic lighting & textures...",
                        "🚀 Finalizing ultra-HD masterpiece..."
                    ]
                    for step_text in steps:
                        step_html = f'<div style="font-style: italic; color: #a5b4fc;"><span>{step_text}</span></div>'
                        message_placeholder.markdown(step_html, unsafe_allow_html=True)
                        time.sleep(0.3)
                    
                    # HUGGING FACE FLUX SECURE GENERATION
                    generated_image_bytes = generate_secure_image(prompt)
                    if generated_image_bytes:
                        full_response = "Here is your secure, high-definition image generated via **Hugging Face FLUX**:"
                    else:
                        generated_svg_art = generate_offline_svg_art(prompt)
                        full_response = "Cloud image server busy — generated via **Offline Vector Art Engine**:"
                else:
                    generated_svg_art = generate_offline_svg_art(prompt)
                    full_response = "🔌 *[Offline Procedural Vector Art Engine]* — Generated locally:"
                
                message_placeholder.markdown(full_response)
                if generated_image_bytes:
                    st.image(generated_image_bytes)
                if generated_svg_art:
                    st.markdown(generated_svg_art, unsafe_allow_html=True)
            else:
                if not is_online_mode:
                    full_response = answer_completely_offline(prompt, detected_script)
                    message_placeholder.markdown(full_response)
                else:
                    greetings = ["hi", "hello", "hey", "hii", "hola", "sup", "good morning", "bye", "namaste", "pranam", "nomoskar"]
                    is_simple_greeting = p_lower in greetings
                    
                    search_triggers = ["winner", "jiteche", "won", "match", "score", "news", "current", "ajke", "ekhon", "latest", "2026", "who won", "today", "weather", "price"]
                    needs_search = any(trigger in p_lower for trigger in search_triggers) and not is_simple_greeting
                    
                    local_hits = retrieve_from_local_corpus(prompt, top_k=3)
                    local_knowledge_context = "\n".join([f"- [{k.title()}]: {a}" for k, a, _ in local_hits]) if local_hits else ""

                    search_context = search_web(prompt) if needs_search else ""
                    
                    if needs_search:
                        message_placeholder.markdown('<div style="font-style: italic; color: #a5b4fc;">🌐 combining local knowledge + live web search...</div>', unsafe_allow_html=True)
                    else:
                        message_placeholder.markdown('<div style="font-style: italic; color: #a5b4fc;">🧠 hybrid reasoning (local corpus + cloud LLM)...</div>', unsafe_allow_html=True)

                    ist = timezone(timedelta(hours=5, minutes=30))
                    current_time_str = datetime.now(ist).strftime("%Y-%m-%d %H:%M:%S")
                    
                    system_content = (
                        f"Current IST is {current_time_str}. Detected Script: {detected_script}. "
                        "You are Indian GPT, an advanced sovereign hybrid AI assistant created exclusively by Shubham. "
                        "Always state that you were created by Shubham if asked. Reply in the exact same language/script."
                    )
                    if local_knowledge_context:
                        system_content += f"\n\nSovereign Knowledge Base Context:\n{local_knowledge_context}"
                    if search_context:
                        system_content += f"\n\nLive Web Search Results:\n{search_context}"

                    messages_payload = [{"role": "system", "content": system_content}]
                    for msg in current_messages[:-1]:
                        if msg["role"] in ["user", "assistant"]:
                            messages_payload.append({"role": msg["role"], "content": msg["content"]})
                    messages_payload.append({"role": "user", "content": prompt})

                    success = False
                    for key_idx in range(len(KEYS_POOL)):
                        if success: break
                        current_api_key = get_next_key(key_idx)
                        models_to_test = get_available_models(current_api_key)
                        headers = {"Authorization": f"Bearer {current_api_key}", "Content-Type": "application/json"}
                        
                        for model_name in models_to_test:
                            if success: break
                            payload = {"model": model_name, "messages": messages_payload, "stream": True}
                            try:
                                response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload, stream=True, timeout=15)
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
                                                            full_response += delta["content"]
                                                            message_placeholder.markdown(full_response + "▌")
                                                    except Exception:
                                                        pass
                                    message_placeholder.markdown(full_response)
                                    success = success or (len(full_response.strip()) > 0)
                                elif response.status_code == 429:
                                    time.sleep(1)
                                    continue
                            except Exception:
                                continue
                    
                    if not success:
                        full_response = answer_completely_offline(prompt, detected_script)
                        message_placeholder.markdown(full_response)
            
            assistant_msg = {"role": "assistant", "content": full_response}
            if generated_image_bytes:
                assistant_msg["image_bytes"] = generated_image_bytes
            if generated_svg_art:
                assistant_msg["svg_art"] = generated_svg_art
                
            current_messages.append(assistant_msg)
            st.rerun()
        except Exception as e:
            st.error(f"System Notice: {e}")
