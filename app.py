import streamlit as st
import requests
import json
import urllib.parse
import time
import math
import re
from datetime import datetime, timezone, timedelta

# ==============================================================================
# INDIAN GPT - SOVEREIGN MULTI-LINGUAL & MULTI-MODAL AI ECOSYSTEM
# Architect & Developer: Shubham
# Architecture: Hybrid Local Symbolic Corpus + Multi-Key LLM Failover + Live Web Search + HD Neural Image Engine
# ==============================================================================

st.set_page_config(
    page_title="Indian GPT - Sovereign AI Ecosystem",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# 1. CUSTOM CYBERPUNK & HIGH-CONTRAST GLASSMORPHISM UI STYLING
# ==============================================================================
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(5, 10, 25, 0.22), rgba(10, 15, 30, 0.28)), 
                    url('https://images.unsplash.com/photo-1620712943543-bcc4688e7485?q=80&w=1920&auto=format&fit=crop') no-repeat center center fixed;
        background-size: cover;
        color: #ffffff !important;
    }
    .stSidebar {
        background-color: rgba(15, 23, 42, 0.92) !important;
        border-right: 1px solid rgba(74, 222, 128, 0.25);
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
# 2. MULTI-KEY ROTATION POOL & EXTERNAL SEARCH CONFIGURATION
# ==============================================================================
KEYS_POOL = [
    "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",
    "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",
    "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",
]

sec_key = st.secrets.get("GROQ_API_KEY_2", "")
if sec_key and sec_key not in KEYS_POOL:
    KEYS_POOL.append(sec_key)

def get_next_key(index: int) -> str:
    """Rotates cleanly through the configured API key pool."""
    return KEYS_POOL[index % len(KEYS_POOL)]

TAVILY_API_KEY = "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"

def search_web(query: str) -> str:
    """Performs real-time internet retrieval via Tavily Search API."""
    search_text = ""
    try:
        if TAVILY_API_KEY:
            payload = {
                "api_key": TAVILY_API_KEY,
                "query": query,
                "max_results": 5,
                "include_images": False
            }
            resp = requests.post("https://api.tavily.com/search", json=payload, timeout=8)
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
# 4. COMPREHENSIVE SOVEREIGN KNOWLEDGE CORPUS (HISTORY, GEOGRAPHY, SCIENCE, MATH)
# ==============================================================================
LOCAL_CORPUS = {
    # --- Identity & Creator ---
    "who made you": "I am Indian GPT, a sovereign multi-lingual and multi-modal AI ecosystem designed, architected, and programmed exclusively by Shubham.",
    "who created you": "I was created, engineered, and deployed by Shubham as an indigenous AI platform supporting all Indian languages, world history, and mathematics.",
    "who is your creator": "My creator and sole architect is Shubham.",
    "tui ke": "Ami Indian GPT, ekta sovereign AI assistant jake Shubham toiri koreche!",
    "amar nam ki": "Tor nam Shubham! Tui amake baniyechis.",
    "tum kaun ho": "Main Indian GPT hoon, ek swadeshi AI assistant jise Shubham ne banaya hai!",


    # --- Indian States & Capitals (All 28 States) ---
    "andhra pradesh": "Amaravati is the capital of Andhra Pradesh, known for Kuchipudi dance, Tirupati temple, and its long Bay of Bengal coastline.",
    "arunachal pradesh": "Itanagar is the capital of Arunachal Pradesh, the 'Land of the Dawn-Lit Mountains' in Northeast India.",
    "assam": "Dispur is the capital of Assam, world-famous for Assam tea, Kaziranga National Park (one-horned rhinoceros), and Bihu festival.",
    "bihar": "Patna is the capital of Bihar, ancient seat of the Maurya and Gupta empires, Nalanda University, and Bodh Gaya.",
    "chhattisgarh": "Raipur is the capital of Chhattisgarh, known for Chitrakote Falls, rich mineral resources, and tribal heritage.",
    "goa": "Panaji is the capital of Goa, India's smallest state by area, famous for its beaches, Konkani culture, and Portuguese-era architecture.",
    "gujarat": "Gandhinagar is the capital of Gujarat, birthplace of Mahatma Gandhi and Sardar Vallabhbhai Patel, home to Gir National Park and the Statue of Unity.",
    "haryana": "Chandigarh is the shared capital of Haryana, historically significant for the Battles of Panipat and the Kurukshetra war.",
    "himachal pradesh": "Shimla is the summer capital (Dharamshala winter) of Himachal Pradesh, situated in the Western Himalayas.",
    "jharkhand": "Ranchi is the capital of Jharkhand, known as the 'Land of Forests' and rich in coal and iron ore reserves.",
    "karnataka": "Bengaluru is the capital of Karnataka, known as the Silicon Valley of India, as well as Hampi and Mysore heritage.",
    "kerala": "Thiruvananthapuram is the capital of Kerala, 'God's Own Country', renowned for backwaters, Kathakali, Ayurveda, and high literacy.",
    "madhya pradesh": "Bhopal is the capital of Madhya Pradesh, the 'Heart of India', home to Khajuraho temples, Sanchi Stupa, and Kanha National Park.",
    "maharashtra": "Mumbai is the capital of Maharashtra and India's financial capital, also famous for Ajanta and Ellora caves and Chhatrapati Shivaji Maharaj's legacy.",
    "manipur": "Imphal is the capital of Manipur, famous for Loktak Lake, Manipuri classical dance, and polo.",
    "meghalaya": "Shillong is the capital of Meghalaya, the 'Abode of Clouds', home to Cherrapunji and Mawsynram, the wettest places on Earth.",
    "mizoram": "Aizawl is the capital of Mizoram, known for its rolling hills, bamboo dance (Cheraw), and vibrant Mizo culture.",
    "nagaland": "Kohima is the capital of Nagaland, famous for the Hornbill Festival and rich Naga tribal traditions.",
    "odisha": "Bhubaneswar is the capital of Odisha, home to the Konark Sun Temple, Jagannath Temple in Puri, Chilika Lake, and Odissi dance.",
    "punjab": "Chandigarh is the shared capital of Punjab, the 'Land of Five Rivers', home to the Golden Temple in Amritsar and Bhangra.",
    "rajasthan": "Jaipur (the Pink City) is the capital of Rajasthan, India's largest state by area, famous for Thar Desert, forts, and palaces.",
    "sikkim": "Gangtok is the capital of Sikkim, home to Kangchenjunga (India's highest peak) and organic farming.",
    "tamil nadu": "Chennai is the capital of Tamil Nadu, famed for Chola temples, Bharatanatyam, Sangam literature, and Marina Beach.",
    "telangana": "Hyderabad is the capital of Telangana, known for Charminar, Golconda Fort, and its booming IT and pharmaceutical sectors.",
    "tripura": "Agartala is the capital of Tripura, known for Ujjayanta Palace, Neermahal, and bamboo handicrafts.",
    "uttar pradesh": "Lucknow is the capital of Uttar Pradesh, India's most populous state, home to the Taj Mahal, Varanasi, Ayodhya, and Prayagraj.",
    "uttarakhand": "Dehradun is the winter capital (Gairsain summer) of Uttarakhand, known as 'Devbhumi' (Land of the Gods) and the origin of the Ganga and Yamuna.",
    "west bengal": "Kolkata is the capital of West Bengal, cultural hub of India, home to Rabindranath Tagore, Sundarbans, Darjeeling tea, and Durga Puja.",

    # --- Indian History & Freedom Movement ---
    "indus valley civilization": "The Indus Valley Civilization (c. 3300–1300 BCE), also known as the Harappan Civilization, was one of the world's earliest urban civilizations, noted for planned cities like Harappa and Mohenjo-daro, advanced drainage systems, and standardized weights.",
    "vedic period": "The Vedic Period (c. 1500–500 BCE) saw the composition of the four Vedas (Rigveda, Samaveda, Yajurveda, Atharvaveda), the Upanishads, and the foundational epics Ramayana and Mahabharata.",
    "maurya empire": "Founded by Chandragupta Maurya in 322 BCE with the guidance of Chanakya, the Maurya Empire reached its zenith under Emperor Ashoka the Great, who spread Buddhism and non-violence after the Kalinga War.",
    "gupta empire": "The Gupta Empire (c. 319–550 CE), led by Chandragupta I, Samudragupta, and Chandragupta II, is hailed as the Golden Age of India for breakthroughs in mathematics (Aryabhata, zero, decimal system), astronomy, medicine, and literature (Kalidasa).",
    "chola dynasty": "The Chola Dynasty of South India (especially under Rajaraja Chola I and Rajendra Chola I) built a formidable maritime empire across Southeast Asia and constructed architectural marvels like the Brihadeeswarar Temple.",
    "delhi sultanate": "The Delhi Sultanate (1206–1526 CE) comprised five dynasties (Mamluk, Khalji, Tughlaq, Sayyid, and Lodi) that ruled large parts of the Indian subcontinent from Delhi.",
    "mughal empire": "Founded by Babur in 1526 after the First Battle of Panipat, the Mughal Empire expanded under Akbar the Great, Jahangir, Shah Jahan, and Aurangzeb, leaving iconic architectural and cultural monuments.",
    "maratha empire": "Founded by Chhatrapati Shivaji Maharaj in 1674, the Maratha Empire rose to dominate much of the Indian subcontinent in the 18th century through guerrilla warfare (Ganimi Kava) and naval strength.",
    "battle of plassey": "Fought on June 23, 1757, the Battle of Plassey saw the British East India Company under Robert Clive defeat Nawab Siraj-ud-Daulah of Bengal, marking the beginning of British political dominance in India.",
    "revolt of 1857": "The Indian Rebellion of 1857 (First War of Indian Independence) began in Meerut on May 10, 1857, led by Mangal Pandey, Rani Lakshmibai of Jhansi, Tatya Tope, Nana Sahib, and Bahadur Shah Zafar.",
    "partition of bengal": "The Partition of Bengal in 1905 by Lord Curzon sparked the Swadeshi and Boycott movements across India, uniting nationalists until it was annulled in 1911.",
    "jallianwala bagh": "On April 13, 1919, British troops under Brigadier-General Reginald Dyer opened fire on peaceful unarmed protesters gathered at Jallianwala Bagh in Amritsar, becoming a turning point in India's independence movement.",
    "non cooperation movement": "Launched by Mahatma Gandhi in 1920, the Non-Cooperation Movement urged Indians to boycott British goods, schools, courts, and titles to achieve Swaraj (self-rule).",
    "dandi march": "In March–April 1930, Mahatma Gandhi led the 240-mile Salt Satyagraha (Dandi March) from Sabarmati Ashram to Dandi to break the British salt monopoly.",
    "quit india movement": "Launched on August 8, 1942, during World War II, the Quit India Movement (Bharat Chhodo Andolan) demanded an immediate end to British rule with Gandhi's call of 'Do or Die'.",
    "azad hind fauj": "Reorganized and led by Netaji Subhash Chandra Bose in 1943, the Azad Hind Fauj (Indian National Army) fought British forces in Northeast India and hoisted the tricolor in Moirang, Manipur.",
    "indian independence": "India achieved independence from British rule at midnight on August 15, 1947, accompanied by the Partition of British India into India and Pakistan.",
    "constitution of india": "Adopted on November 26, 1949, and enforced on January 26, 1950, the Constitution of India—drafted under Dr. B. R. Ambedkar—is the longest written national constitution in the world.",

    # --- World History & Global Civilizations ---
    "mesopotamia": "Mesopotamia, located between the Tigris and Euphrates rivers (modern Iraq), is the 'Cradle of Civilization', known for Sumerian city-states, cuneiform writing, and Hammurabi's Code.",
    "ancient egypt": "Ancient Egypt flourished along the Nile River for over 3,000 years, famed for the Pyramids of Giza, Pharaohs, hieroglyphic writing, and advancements in medicine and engineering.",
    "ancient greece": "Ancient Greece laid the foundations of Western philosophy (Socrates, Plato, Aristotle), democracy in Athens, mathematics (Pythagoras, Euclid), and the Olympic Games.",
    "roman empire": "The Roman Empire (27 BCE–476 CE in the West) united the Mediterranean world under Roman law, engineering (aqueducts, roads, Colosseum), and Latin language.",
    "silk road": "The Silk Road was an ancient network of Eurasian trade routes connecting East Asia (China) with South Asia (India), Persia, Arabia, and the Mediterranean, facilitating trade in silk, spices, and ideas.",
    "renaissance": "The Renaissance (14th–17th century) was a cultural, artistic, and scientific rebirth in Europe originating in Italy, featuring Leonardo da Vinci, Michelangelo, Galileo, and Copernicus.",
    "industrial revolution": "Beginning in Great Britain in the late 18th century, the Industrial Revolution transformed agrarian economies into mechanized, factory-based industrial societies powered by steam engines and coal.",
    "american revolution": "The American Revolutionary War (1775–1783) saw the Thirteen Colonies win independence from Great Britain, establishing the United States of America.",
    "french revolution": "The French Revolution (1789–1799) abolished the French monarchy, established a republic, and spread ideals of Liberty, Equality, and Fraternity across Europe.",
    "world war 1": "World War I (1914–1918), triggered by the assassination of Archduke Franz Ferdinand, pitted the Allies against the Central Powers, resulting in the collapse of four empires and the Treaty of Versailles.",
    "russian revolution": "The Russian Revolution of 1917 overthrew the Tsarist autocracy and brought Vladimir Lenin's Bolsheviks to power, leading to the formation of the Soviet Union (USSR) in 1922.",
    "world war 2": "World War II (1939–1945) was the deadliest conflict in human history, fought between the Allies and the Axis powers across Europe, Africa, and the Pacific, ending with the defeat of Nazi Germany and Imperial Japan.",
    "cold war": "The Cold War (1947–1991) was a geopolitical and ideological rivalry between the United States and the Soviet Union, characterized by the nuclear arms race, Space Race, and proxy conflicts.",
    "space race": "The Space Race between the USA and USSR saw milestones like Sputnik 1 (1957), Yuri Gagarin's first human spaceflight (1961), and NASA's Apollo 11 Moon landing by Neil Armstrong (1969).",

    # --- ISRO, Space Exploration & Physics ---
    "isro": "The Indian Space Research Organisation (ISRO), founded in 1969 by Dr. Vikram Sarabhai and headquartered in Bengaluru, is India's national space agency behind Aryabhata, Chandrayaan, Mangalyaan, and Aditya-L1.",
    "chandrayaan 3": "Launched by ISRO on July 14, 2023, Chandrayaan-3 achieved a historic soft landing near the Moon's south pole on August 23, 2023, making India the first nation to land in that region.",
    "mangalyaan": "The Mars Orbiter Mission (Mangalyaan), launched in November 2013, made India the first Asian nation to reach Martian orbit and the first in the world to succeed on its maiden attempt.",
    "aditya l1": "Aditya-L1 is India's first dedicated space-based solar observatory mission launched by ISRO to study the Sun's corona and solar winds from Lagrange Point 1 (L1).",
    "newton laws": "Newton's Three Laws of Motion: (1) Law of Inertia; (2) Force equals mass times acceleration ($F = ma$); (3) Every action has an equal and opposite reaction.",
    "relativity": "Albert Einstein's Theory of Relativity comprises Special Relativity (1905, $E = mc^2$) and General Relativity (1915), explaining gravity as the curvature of spacetime caused by mass and energy.",
    "quantum mechanics": "Quantum Mechanics describes nature at atomic and subatomic scales, introducing wave-particle duality, quantization of energy, and Heisenberg's Uncertainty Principle.",
    "dna": "Deoxyribonucleic Acid (DNA) is the double-helix molecule carrying genetic instructions for the development, functioning, and reproduction of all known living organisms.",
    "periodic table": "The Modern Periodic Table organizes all 118 known chemical elements by increasing atomic number, electron configuration, and recurring chemical properties.",
    "black hole": "A black hole is a region of spacetime where gravity is so strong that nothing—not even light—can escape once it crosses the event horizon.",

    # --- Advanced Mathematics Formulas & Theorems ---
    "quadratic formula": "For any quadratic equation $ax^2 + bx + c = 0$ ($a \neq 0$), the roots are given by:\n$$x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$$",
    "pythagorean theorem": "In a right-angled triangle with perpendicular sides $a, b$ and hypotenuse $c$:\n$$a^2 + b^2 = c^2$$",
    "euler identity": "Euler's Identity links five fundamental mathematical constants:\n$$e^{i\pi} + 1 = 0$$",
    "calculus derivative": "The derivative of $f(x)$ measures instantaneous rate of change:\n$$f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}$$\nPower rule: $\frac{d}{dx}(x^n) = nx^{n-1}$.",
    "calculus integration": "Indefinite integration is the reverse of differentiation:\n$$\int x^n \, dx = \frac{x^{n+1}}{n+1} + C \quad (n \neq -1)$$",
    "trigonometry identities": "Fundamental Trigonometric Identities:\n1. $\sin^2\theta + \cos^2\theta = 1$\n2. $1 + \tan^2\theta = \sec^2\theta$\n3. $1 + \cot^2\theta = \csc^2\theta$",
    "logarithm rules": "Key Logarithm Properties:\n1. $\log_b(xy) = \log_b x + \log_b y$\n2. $\log_b(x/y) = \log_b x - \log_b y$\n3. $\log_b(x^k) = k \log_b x$",
    "binomial theorem": "Binomial Expansion for any positive integer $n$:\n$$(a + b)^n = \sum_{k=0}^{n} \binom{n}{k} a^{n-k} b^k$$",
    "matrix determinant": "For a $2 \times 2$ matrix $A = \begin{pmatrix} a & b \\ c & d \end{pmatrix}$, the determinant is $\det(A) = ad - bc$.",
    "probability bayes": "Bayes' Theorem calculates conditional probability:\n$$P(A|B) = \frac{P(B|A) \cdot P(A)}{P(B)}$$",
    "arithmetic progression": "In an Arithmetic Progression (AP) with first term $a$ and common difference $d$: $n$-th term $a_n = a + (n-1)d$, and sum $S_n = \frac{n}{2}[2a + (n-1)d]$.",
    "geometric progression": "In a Geometric Progression (GP) with first term $a$ and common ratio $r$: $n$-th term $a_n = ar^{n-1}$, and sum $S_n = \frac{a(r^n - 1)}{r - 1}$ ($r \neq 1$).",

    # --- Scheduled Indian Languages & Scripts ---
    "hindi": "Hindi (हिन्दी), written in Devanagari script, is one of India's official languages and is spoken across Northern and Central India.",
    "bengali": "Bengali (বাংলা), written in the Bengali-Assamese script, is the official language of West Bengal and Tripura, and the language of Rabindranath Tagore.",
    "telugu": "Telugu (తెలుగు), a classical Dravidian language spoken primarily in Andhra Pradesh and Telangana, is often called the 'Italian of the East'.",
    "marathi": "Marathi (मराठी), written in Devanagari script, is the official language of Maharashtra with a rich literary history dating back over a thousand years.",
    "tamil": "Tamil (தமிழ்), spoken in Tamil Nadu and Puducherry, is one of the world's oldest surviving classical languages with Sangam literature dating back over 2,000 years.",
    "urdu": "Urdu (اردو), written in the Nastaliq script, is an Indo-Aryan language renowned for its poetic traditions (ghazals and nazms) and cultural heritage.",
    "gujarati": "Gujarati (ગુજરાતી), spoken in Gujarat, is written in the Gujarati script and was the native language of Mahatma Gandhi.",
    "kannada": "Kannada (ಕನ್ನಡ), a classical Dravidian language spoken in Karnataka, boasts a rich literary heritage and the Kannada script.",
    "odia": "Odia (ଓଡ଼ିଆ), a classical Indo-Aryan language spoken in Odisha, features its distinctive rounded Odia script.",
    "malayalam": "Malayalam (മലയാളം), a classical Dravidian language spoken in Kerala and Lakshadweep, is known for its rich literature and script.",
    "punjabi": "Punjabi (ਪੰਜਾਬੀ), written in the Gurmukhi script in India, is the language of Punjab and Sikh sacred scriptures.",
    "assamese": "Assamese (অসমীয়া), the easternmost Indo-Aryan language spoken in Assam, is written in the Assamese script.",
    "sanskrit": "Sanskrit (संस्कृतम्), one of the oldest documented Indo-European languages, is the classical liturgical and philosophical language of ancient India.",

    # --- World Countries & Capitals ---
    "afghanistan capital": "Kabul is the capital of Afghanistan.",
    "australia capital": "Canberra is the capital of Australia.",
    "bangladesh capital": "Dhaka is the capital of Bangladesh.",
    "bhutan capital": "Thimphu is the capital of Bhutan.",
    "brazil capital": "Brasília is the capital of Brazil.",
    "canada capital": "Ottawa is the capital of Canada.",
    "china capital": "Beijing is the capital of China.",
    "egypt capital": "Cairo is the capital of Egypt.",
    "france capital": "Paris is the capital of France.",
    "germany capital": "Berlin is the capital of Germany.",
    "indonesia capital": "Jakarta (transitioning to Nusantara) is the capital of Indonesia.",
    "iran capital": "Tehran is the capital of Iran.",
    "iraq capital": "Baghdad is the capital of Iraq.",
    "israel capital": "Jerusalem is the capital of Israel.",
    "italy capital": "Rome is the capital of Italy.",
    "japan capital": "Tokyo is the capital of Japan.",
    "malaysia capital": "Kuala Lumpur is the capital of Malaysia.",
    "maldives capital": "Malé is the capital of Maldives.",
    "myanmar capital": "Naypyidaw is the capital of Myanmar.",
    "nepal capital": "Kathmandu is the capital of Nepal.",
    "netherlands capital": "Amsterdam is the capital of the Netherlands.",
    "new zealand capital": "Wellington is the capital of New Zealand.",
    "norway capital": "Oslo is the capital of Norway.",
    "pakistan capital": "Islamabad is the capital of Pakistan.",
    "russia capital": "Moscow is the capital of Russia.",
    "saudi arabia capital": "Riyadh is the capital of Saudi Arabia.",
    "singapore capital": "Singapore is a sovereign city-state and island country.",
    "south africa capital": "South Africa has three capitals: Pretoria (executive), Cape Town (legislative), and Bloemfontein (judicial).",
    "south korea capital": "Seoul is the capital of South Korea.",
    "spain capital": "Madrid is the capital of Spain.",
    "sri lanka capital": "Sri Jayawardenepura Kotte (legislative) and Colombo (executive/judicial) are the capitals of Sri Lanka.",
    "sweden capital": "Stockholm is the capital of Sweden.",
    "switzerland capital": "Bern is the de facto capital of Switzerland.",
    "thailand capital": "Bangkok is the capital of Thailand.",
    "turkey capital": "Ankara is the capital of Turkey.",
    "uae capital": "Abu Dhabi is the capital of the United Arab Emirates.",
    "uk capital": "London is the capital of the United Kingdom.",
    "usa capital": "Washington, D.C. is the capital of the United States of America.",
    "vietnam capital": "Hanoi is the capital of Vietnam.",

    # --- Great Mathematicians & Scientists ---
    "aryabhata": "Aryabhata (476–550 CE) was a pioneering Indian mathematician and astronomer who authored the Aryabhatiya, explained the place-value decimal system, approximated $\pi \approx 3.1416$, and proposed Earth's axial rotation.",
    "brahmagupta": "Brahmagupta (598–668 CE) was an ancient Indian mathematician who first formalized rules for computing with zero ($0$) and negative numbers in his treatise Brahmasphutasiddhanta.",
    "srinivasa ramanujan": "Srinivasa Ramanujan (1887–1920) was a legendary Indian mathematical genius who made extraordinary contributions to number theory, infinite series, continued fractions, and partition functions.",
    "cv raman": "Sir C. V. Raman (1888–1970) was an Indian physicist awarded the 1930 Nobel Prize in Physics for discovering the Raman Effect (inelastic scattering of light).",
    "homi bhabha": "Dr. Homi Jehangir Bhabha (1909–1966) was the father of the Indian nuclear programme and founding director of TIFR and BARC.",
    "vikram sarabhai": "Dr. Vikram Sarabhai (1919–1971) is revered as the father of the Indian space programme and founder of ISRO.",
    "apj abdul kalam": "Dr. A. P. J. Abdul Kalam (1931–2015), the 'Missile Man of India' and 11th President of India, led India's Agni and Prithvi missile programmes and Pokhran-II nuclear tests.",
    "isaac newton": "Sir Isaac Newton (1643–1727) formulated the laws of motion, universal gravitation, and co-invented infinitesimal calculus.",
    "albert einstein": "Albert Einstein (1879–1955) developed the Theory of Relativity and won the 1921 Nobel Prize in Physics for explaining the photoelectric effect.",
    "nikola tesla": "Nikola Tesla (1856–1943) was a visionary inventor and electrical engineer best known for designing the modern alternating current (AC) electricity supply system.",
    "marie curie": "Marie Curie (1867–1934) was a pioneering physicist and chemist who discovered polonium and radium, becoming the first person to win two Nobel Prizes in two different sciences.",
    "alan turing": "Alan Turing (1912–1954) was the father of theoretical computer science and artificial intelligence, known for the Turing Machine and breaking the Enigma code.",


    # --- Union Territories, Geography, Battles, CS & Natural Sciences ---
    "andaman and nicobar": "Port Blair (Sri Vijaya Puram) is the capital of the Andaman and Nicobar Islands, located in the Bay of Bengal and home to Cellular Jail.",
    "chandigarh": "Chandigarh is a Union Territory and serves as the shared capital of both Punjab and Haryana, designed by Le Corbusier.",
    "dadra and nagar haveli": "Daman is the capital of the Union Territory of Dadra and Nagar Haveli and Daman and Diu on India's western coast.",
    "delhi": "New Delhi is the National Capital Territory (NCT) of India and seat of all three branches of the Government of India.",
    "jammu and kashmir": "Srinagar (summer) and Jammu (winter) are the capitals of the Union Territory of Jammu and Kashmir in the Himalayas.",
    "ladakh": "Leh and Kargil are the administrative capitals of Ladakh, a high-altitude cold desert Union Territory in northern India.",
    "lakshadweep": "Kavaratti is the capital of Lakshadweep, an archipelago of 36 coral islands in the Arabian Sea.",
    "puducherry": "Puducherry (formerly Pondicherry) is a Union Territory known for its French colonial heritage and Sri Aurobindo Ashram.",
    "ganga river": "The Ganga (Ganges), originating from the Gangotri Glacier as the Bhagirathi in Uttarakhand, is India's holiest and longest river flowing through northern India into the Bay of Bengal.",
    "brahmaputra river": "The Brahmaputra originates in Tibet (as Yarlung Tsangpo), flows through Arunachal Pradesh and Assam, and joins the Ganga in Bangladesh to form the Sundarbans delta.",
    "yamuna river": "The Yamuna, originating from the Yamunotri Glacier, is the largest tributary of the Ganga, flowing past Delhi, Mathura, and Agra.",
    "godavari river": "The Godavari, originating at Trimbakeshwar in Maharashtra, is the longest river in Peninsular India and is called 'Dakshin Ganga'.",
    "narmada river": "The Narmada rises from Amarkantak Plateau in Madhya Pradesh and flows westward through a rift valley into the Arabian Sea.",
    "himalayas": "The Himalayas form India's northern mountain barrier, containing the world's highest peaks including Mount Everest and Kangchenjunga (8,586 m, India's highest peak).",
    "sundarbans": "The Sundarbans in West Bengal and Bangladesh is the world's largest contiguous mangrove forest and a UNESCO World Heritage Site, famous for the Royal Bengal Tiger.",
    "thar desert": "The Thar Desert (Great Indian Desert) spans northwestern India (primarily Rajasthan) and forms a natural boundary with Pakistan.",
    "battle of kalinga": "Fought in 261 BCE between Emperor Ashoka of the Maurya Empire and the state of Kalinga, its massive bloodshed transformed Ashoka into a champion of Buddhism and non-violence.",
    "battles of tarain": "Fought in 1191 and 1192 CE between Prithviraj Chauhan and Muhammad of Ghor; the Second Battle of Tarain paved the way for Muslim rule in North India.",
    "first battle of panipat": "Fought on April 21, 1526, Babur defeated Ibrahim Lodi using field artillery and Tulughma tactics, establishing the Mughal Empire in India.",
    "second battle of panipat": "Fought on November 5, 1556, Akbar's forces under Bairam Khan defeated Hemu, consolidating Mughal rule in northern India.",
    "third battle of panipat": "Fought on January 14, 1761, between the Maratha Empire and the invading Afghan army of Ahmad Shah Durrani.",
    "battle of buxar": "Fought on October 22, 1764, the British East India Company defeated the combined armies of Mir Qasim, Shuja-ud-Daula, and Mughal Emperor Shah Alam II, securing Diwani rights over Bengal.",
    "battle of waterloo": "Fought on June 18, 1815, in present-day Belgium, the Seventh Coalition under the Duke of Wellington and Gebhard von Blücher decisively defeated Napoleon Bonaparte.",
    "treaty of versailles": "Signed on June 28, 1919, the Treaty of Versailles formally ended World War I between Germany and the Allied Powers.",
    "magna carta": "Sealed by King John of England in 1215, Magna Carta established the foundational constitutional principle that everyone, including the sovereign, is subject to the law.",
    "machine learning": "Machine Learning (ML) is a branch of Artificial Intelligence that enables software systems to learn patterns from data and improve performance without being explicitly programmed for every rule.",
    "deep learning": "Deep Learning is a subset of Machine Learning utilizing multi-layered artificial neural networks (such as Transformers, CNNs, and RNNs) to model complex representations in text, vision, and audio.",
    "large language model": "A Large Language Model (LLM) is a deep neural network based on the Transformer architecture trained on vast text corpora to understand, reason, and generate human-like language.",
    "neural network": "An Artificial Neural Network (ANN) consists of interconnected layers of nodes (neurons) with adjustable weights and activation functions inspired by biological neural circuits.",
    "operating system": "An Operating System (OS) such as Windows, Linux, or macOS manages computer hardware resources, process scheduling, memory allocation, file systems, and user interfaces.",
    "algorithm": "An algorithm is a finite, step-by-step logical procedure or set of rules designed to solve a specific computational problem or perform a calculation.",
    "data structure": "Data structures (such as arrays, linked lists, stacks, queues, trees, hash tables, and graphs) organize and store data efficiently for fast access and modification.",
    "cybersecurity": "Cybersecurity encompasses practices, encryption protocols, network defenses, and ethical penetration testing used to protect systems and data from unauthorized access.",
    "cell biology": "The cell is the basic structural and functional unit of all living organisms; eukaryotic cells contain membrane-bound organelles like the nucleus and mitochondria.",
    "mitochondria": "Mitochondria are double-membrane organelles known as the 'powerhouse of the cell' because they generate adenosine triphosphate (ATP) via cellular respiration.",
    "human heart": "The human heart is a four-chambered muscular organ (two atria and two ventricles) that pumps oxygenated blood through the systemic circulation and deoxygenated blood to the lungs.",
    "solar system": "The Solar System consists of the Sun and eight planets: Mercury, Venus, Earth, Mars (terrestrial), Jupiter, Saturn (gas giants), Uranus, and Neptune (ice giants).",
    "plate tectonics": "Plate tectonics is the scientific theory explaining how Earth's lithosphere is divided into moving tectonic plates whose interactions cause earthquakes, volcanoes, and mountain building.",
    "chemical bonding": "Chemical bonds hold atoms together in molecules and crystals, primarily through ionic bonding (electron transfer), covalent bonding (electron sharing), and metallic bonding.",
    "acids and bases": "According to the Brønsted–Lowry definition, acids are proton ($H^+$) donors ($\text{pH} < 7$) and bases are proton acceptors ($\text{pH} > 7$), while pure water is neutral ($\text{pH} = 7$).",

    # --- Heritage Monuments, Classical Arts, Nobel Laureates & Physics Laws ---
    "red fort": "The Red Fort (Lal Qila) in Old Delhi, built by Mughal Emperor Shah Jahan in 1638, is the historic site where the Prime Minister of India hoists the national flag every Independence Day.",
    "qutub minar": "Qutub Minar in Delhi is a 73-meter tall UNESCO World Heritage victory tower whose construction began under Qutb-ud-din Aibak in 1199 CE and was completed by Iltutmish.",
    "konark sun temple": "The 13th-century Konark Sun Temple in Odisha, built by King Narasimhadeva I, is designed as a colossal stone chariot of the Sun God Surya with 24 carved wheels.",
    "ajanta and ellora": "Located in Maharashtra, the Ajanta and Ellora Caves are UNESCO World Heritage rock-cut cave monuments showcasing Buddhist, Hindu, and Jain art and architecture.",
    "hampi": "Hampi in Karnataka was the magnificent 14th-century capital of the Vijayanagara Empire, famed for the Virupaksha Temple and Vittala Temple stone chariot.",
    "kaziranga": "Kaziranga National Park in Assam is a UNESCO World Heritage Site housing two-thirds of the world's Great One-Horned Rhinoceroses.",
    "bharatanatyam": "Bharatanatyam is a major Indian classical dance form originating in Tamil Nadu, known for expressive hand mudras, rhythmic footwork, and temple traditions.",
    "kathak": "Kathak is a classical Indian dance originating in northern India, celebrated for intricate footwork (tatkar), rapid spins (chakkars), and storytelling.",
    "kathakali": "Kathakali is a classical dance-drama from Kerala renowned for elaborate facial makeup, vibrant costumes, and dramatization of Hindu epics.",
    "odissi": "Odissi is one of the oldest surviving classical dance forms of India, originating in the temples of Odisha and characterized by the fluid Tribhangi posture.",
    "rabindranath tagore": "Rabindranath Tagore (1861–1941) became the first non-European Nobel Laureate in 1913 (Literature for Gitanjali) and composed the national anthems of both India and Bangladesh.",
    "amartya sen": "Amartya Sen won the 1998 Nobel Memorial Prize in Economic Sciences for his contributions to welfare economics, social choice theory, and famine analysis.",
    "mother teresa": "Mother Teresa (Saint Teresa of Calcutta) received the 1979 Nobel Peace Prize for founding the Missionaries of Charity and serving the destitute in Kolkata.",
    "hargobind khorana": "Dr. Har Gobind Khorana shared the 1968 Nobel Prize in Physiology or Medicine for cracking the genetic code and explaining protein synthesis.",
    "subrahmanyan chandrasekhar": "Subrahmanyan Chandrasekhar won the 1983 Nobel Prize in Physics for theoretical discoveries on the structure and evolution of massive stars (Chandrasekhar Limit).",
    "ohms law": "Ohm's Law states that the electric current $I$ through a conductor between two points is directly proportional to the voltage $V$ across the two points: $V = I \cdot R$.",
    "thermodynamics": "The Laws of Thermodynamics govern heat, work, and energy: (0) Thermal equilibrium; (1) Conservation of energy ($\Delta U = Q - W$); (2) Entropy of an isolated system never decreases.",
    "bernoulli principle": "Bernoulli's Principle states that an increase in the speed of a fluid occurs simultaneously with a decrease in static pressure or potential energy.",
    "boyle law": "Boyle's Law states that at constant temperature, the pressure $P$ of a given mass of an ideal gas is inversely proportional to its volume $V$: $P_1 V_1 = P_2 V_2$.",
    "avogadro number": "Avogadro's constant ($N_A = 6.02214076 \times 10^{23} \text{ mol}^{-1}$) defines the exact number of constituent particles in one mole of a substance.",
}

# ==============================================================================
# 5. SYMBOLIC & NUMERICAL MATHEMATICS ENGINE (LOCAL SOLVER)
# ==============================================================================
def compute_compound_interest(p: float, r: float, t: float, n: int = 1) -> str:
    """Computes Compound Interest and Final Amount step-by-step."""
    if p < 0 or r < 0 or t < 0 or n <= 0:
        return "Invalid inputs: Principal, Rate, and Time must be non-negative."
    amount = p * ((1 + (r / (100 * n))) ** (n * t))
    ci = amount - p
    return (
        f"**Compound Interest Calculation ($A = P(1 + \frac{{r}}{{100n}})^{{nt}}$):**\n"
        f"• **Principal ($P$):** ₹{p:,.2f}\n"
        f"• **Annual Rate ($r$):** {r}% | **Time ($t$):** {t} years | **Compounding ($n$/yr):** {n}\n"
        f"• **Total Compound Interest ($CI$):** **₹{ci:,.2f}**\n"
        f"• **Final Maturity Amount ($A$):** **₹{amount:,.2f}**"
    )

def compute_statistics_summary(numbers: list) -> str:
    """Computes Mean, Median, Variance, and Standard Deviation for a dataset."""
    if not numbers:
        return "No valid numbers provided for statistical analysis."
    sorted_nums = sorted(numbers)
    count = len(sorted_nums)
    mean_val = sum(sorted_nums) / count
    if count % 2 == 1:
        median_val = sorted_nums[count // 2]
    else:
        median_val = (sorted_nums[count // 2 - 1] + sorted_nums[count // 2]) / 2.0
    variance = sum((x - mean_val) ** 2 for x in sorted_nums) / count
    std_dev = math.sqrt(variance)
    return (
        f"**Statistical Analysis Summary ($N = {count}$):**\n"
        f"• **Sorted Data:** `{sorted_nums}`\n"
        f"• **Arithmetic Mean ($\mu$):** **{mean_val:.4f}**\n"
        f"• **Median:** **{median_val:.4f}**\n"
        f"• **Population Variance ($\sigma^2$):** **{variance:.4f}**\n"
        f"• **Standard Deviation ($\sigma$):** **{std_dev:.4f}**"
    )

def solve_linear_equation(a: float, b: float, c: float) -> str:
    """Solves linear equation ax + b = c step by step."""
    if a == 0:
        return "Invalid linear equation: coefficient $a$ cannot be zero."
    x = (c - b) / a
    return (
        f"**Step-by-Step Linear Equation Solution ($ax + b = c$):**\n"
        f"1. Given: ${a}x + ({b}) = {c}$\n"
        f"2. Subtract ${b}$ from both sides: ${a}x = {c - b}$\n"
        f"3. Divide by ${a}$: $x = \frac{{{c - b}}}{{{a}}} = \mathbf{{{x:.4f}}}$"
    )

def compute_combinatorics(n: int, r: int) -> str:
    """Computes both Permutation nPr and Combination nCr."""
    if n < 0 or r < 0 or r > n:
        return "Invalid inputs: ensure $0 \le r \le n$."
    npr = math.perm(n, r)
    ncr = math.comb(n, r)
    return (
        f"**Combinatorics Results for $n = {n}, r = {r}$:**\n"
        f"• **Permutation ($^{{{n}}}P_{{{r}}}$):** $\frac{{{n}!}}{{({n}-{r})!}} = \mathbf{{{npr}}}$\n"
        f"• **Combination ($^{{{n}}}C_{{{r}}}$):** $\frac{{{n}!}}{{{r}!({n}-{r})!}} = \mathbf{{{ncr}}}$"
    )

def compute_gcd_lcm(a: int, b: int) -> str:
    """Computes Greatest Common Divisor (GCD) and Least Common Multiple (LCM)."""
    if a == 0 and b == 0:
        return "GCD and LCM are undefined when both integers are zero."
    g = math.gcd(a, b)
    l = abs(a * b) // g if g != 0 else 0
    return (
        f"**Number Theory Analysis for ({a}, {b}):**\n"
        f"• **GCD / HCF:** $\gcd({a}, {b}) = \mathbf{{{g}}}$\n"
        f"• **LCM:** $\text{{lcm}}({a}, {b}) = \frac{{|{a} \times {b}|}}{{{g}}} = \mathbf{{{l}}}$"
    )

def generate_fibonacci(n: int) -> str:
    """Generates the first n terms of the Fibonacci sequence."""
    if n <= 0:
        return "Please specify a positive integer $n \ge 1$."
    if n > 50:
        return "Please enter $n \le 50$ for clean display."
    seq = []
    a, b = 0, 1
    for _ in range(n):
        seq.append(str(a))
        a, b = b, a + b
    return f"**First {n} Fibonacci Numbers:**\n`{', '.join(seq)}`"

def compute_trig_degrees(deg: float) -> str:
    """Computes exact floating-point sin, cos, and tan for an angle in degrees."""
    rad = math.radians(deg)
    s = math.sin(rad)
    c = math.cos(rad)
    tan_str = "Undefined (Infinity)" if abs(c) < 1e-12 else f"{math.tan(rad):.6f}"
    return (
        f"**Trigonometric Ratios for $\theta = {deg}^\circ$ ($\approx {rad:.6f}$ rad):**\n"
        f"• $\sin({deg}^\circ) = \mathbf{{{s:.6f}}}$\n"
        f"• $\cos({deg}^\circ) = \mathbf{{{c:.6f}}}$\n"
        f"• $\tan({deg}^\circ) = \mathbf{{{tan_str}}}$"
    )

def solve_quadratic_equation(a: float, b: float, c: float) -> str:
    """Solves ax^2 + bx + c = 0 with full step-by-step discriminant analysis."""
    if a == 0:
        if b == 0:
            return "Invalid equation: both $a$ and $b$ cannot be zero."
        root = -c / b
        return f"This is a linear equation ($bx + c = 0$). Solution: $x = {root:.4f}$."
    
    discriminant = (b ** 2) - (4 * a * c)
    steps = [
        f"**Step 1: Identify Coefficients**\n$a = {a}$, $b = {b}$, $c = {c}$",
        f"**Step 2: Compute Discriminant ($\Delta = b^2 - 4ac$)**\n$\Delta = ({b})^2 - 4({a})({c}) = {discriminant:.4f}$"
    ]
    
    if discriminant > 0:
        r1 = (-b + math.sqrt(discriminant)) / (2 * a)
        r2 = (-b - math.sqrt(discriminant)) / (2 * a)
        steps.append(
            f"**Step 3: Two Distinct Real Roots ($\Delta > 0$)**\n"
            f"$$x_1 = \frac{{-({b}) + \sqrt{{{discriminant:.4f}}}}}{{2({a})}} = {r1:.4f}$$\n"
            f"$$x_2 = \frac{{-({b}) - \sqrt{{{discriminant:.4f}}}}}{{2({a})}} = {r2:.4f}$$"
        )
    elif discriminant == 0:
        r = -b / (2 * a)
        steps.append(
            f"**Step 3: One Repeated Real Root ($\Delta = 0$)**\n"
            f"$$x = \frac{{-({b})}}{{2({a})}} = {r:.4f}$$"
        )
    else:
        real_part = -b / (2 * a)
        imag_part = math.sqrt(abs(discriminant)) / (2 * a)
        steps.append(
            f"**Step 3: Two Complex Conjugate Roots ($\Delta < 0$)**\n"
            f"$$x_1 = {real_part:.4f} + {imag_part:.4f}i$$\n"
            f"$$x_2 = {real_part:.4f} - {imag_part:.4f}i$$"
        )
    return "\n\n".join(steps)

def check_prime_number(n: int) -> str:
    """Determines whether an integer n is prime and lists its factors if composite."""
    if n <= 1:
        return f"**{n}** is neither prime nor composite."
    if n <= 3:
        return f"**{n}** is a **Prime Number**."
    factors = []
    for i in range(2, int(math.isqrt(n)) + 1):
        if n % i == 0:
            factors.append(i)
            if i != n // i:
                factors.append(n // i)
    if not factors:
        return f"**{n}** is a **Prime Number** (divisible only by 1 and {n})."
    factors.sort()
    return f"**{n}** is a **Composite Number**. Its proper divisors are: `{factors}`."

def compute_factorial(n: int) -> str:
    """Computes n! safely up to n = 100."""
    if n < 0:
        return "Factorial is not defined for negative integers."
    if n > 100:
        return "Input too large for instant display; please enter $n \le 100$."
    val = math.factorial(n)
    return f"The factorial of **{n}** is:\n$${n}! = {val}$$"

def evaluate_safe_arithmetic(expr: str):
    """Safely evaluates pure arithmetic expressions (+, -, *, /, **, sqrt, sin, cos, tan, log, pi, e)."""
    cleaned = expr.lower().replace("calculate", "").replace("solve", "").replace("what is", "").replace("?", "").strip()
    if not cleaned:
        return None
    allowed_chars = set("0123456789+-*/().^ ")
    if all(c in allowed_chars for c in cleaned) and any(c.isdigit() for c in cleaned) and any(op in cleaned for op in "+-*/^"):
        try:
            py_expr = cleaned.replace("^", "**")
            result = eval(py_expr, {"__builtins__": None}, {})
            return f"**Exact Calculation Result:**\n`{cleaned}` = **{result}**"
        except Exception:
            return None
    return None

def solve_math_locally(query_str: str):
    """Routes mathematical queries to specialized local numerical and symbolic solvers."""
    q = query_str.lower().strip()
    
    # 1. Direct arithmetic expression check
    arith = evaluate_safe_arithmetic(q)
    if arith:
        return arith
        
    # 2. Prime check: e.g., "is 97 prime"
    prime_match = re.search(r"is\s+(\d+)\s+(?:a\s+)?prime", q)
    if prime_match:
        return check_prime_number(int(prime_match.group(1)))
        
    # 3. Factorial check: e.g., "factorial of 12" or "12!"
    fact_match = re.search(r"factorial\s+(?:of\s+)?(\d+)|(\d+)!", q)
    if fact_match:
        num_str = fact_match.group(1) or fact_match.group(2)
        return compute_factorial(int(num_str))
        
    # 4. Quadratic solver with explicit coefficients: e.g., "solve quadratic a=1 b=-5 c=6"
    quad_match = re.search(r"a\s*=\s*(-?\d+\.?\d*)[,\s]+b\s*=\s*(-?\d+\.?\d*)[,\s]+c\s*=\s*(-?\d+\.?\d*)", q)
    if quad_match:
        a_val = float(quad_match.group(1))
        b_val = float(quad_match.group(2))
        c_val = float(quad_match.group(3))
        return solve_quadratic_equation(a_val, b_val, c_val)

    # 5. Linear equation solver: e.g., "solve linear a=3 b=4 c=19"
    lin_match = re.search(r"linear\s+a\s*=\s*(-?\d+\.?\d*)[,\s]+b\s*=\s*(-?\d+\.?\d*)[,\s]+c\s*=\s*(-?\d+\.?\d*)", q)
    if lin_match:
        return solve_linear_equation(float(lin_match.group(1)), float(lin_match.group(2)), float(lin_match.group(3)))

    # 6. Combinatorics: e.g., "ncr 10 3" or "npr 10 3"
    comb_match = re.search(r"(?:ncr|npr|combination|permutation)\s+(\d+)[,\s]+(\d+)", q)
    if comb_match:
        return compute_combinatorics(int(comb_match.group(1)), int(comb_match.group(2)))

    # 7. GCD and LCM: e.g., "gcd 24 36" or "lcm 24 36"
    gcd_match = re.search(r"(?:gcd|hcf|lcm)\s+(\d+)[,\s]+(\d+)", q)
    if gcd_match:
        return compute_gcd_lcm(int(gcd_match.group(1)), int(gcd_match.group(2)))

    # 8. Fibonacci sequence: e.g., "fibonacci 15"
    fib_match = re.search(r"fibonacci\s+(\d+)", q)
    if fib_match:
        return generate_fibonacci(int(fib_match.group(1)))

    # 9. Trigonometry angle: e.g., "trig 45" or "sin 45"
    trig_match = re.search(r"(?:trig|sin|cos|tan)\s+(-?\d+\.?\d*)", q)
    if trig_match:
        return compute_trig_degrees(float(trig_match.group(1)))

    # 10. Compound interest: e.g., "compound interest p=10000 r=8 t=5"
    ci_match = re.search(r"compound\s+interest\s+p\s*=\s*(\d+\.?\d*)[,\s]+r\s*=\s*(\d+\.?\d*)[,\s]+t\s*=\s*(\d+\.?\d*)", q)
    if ci_match:
        return compute_compound_interest(float(ci_match.group(1)), float(ci_match.group(2)), float(ci_match.group(3)))

    # 11. Statistics mean/median/std: e.g., "stats 10, 20, 30, 40, 50"
    stats_match = re.search(r"(?:stats|statistics|mean|median)\s+([0-9.,\s-]+)", q)
    if stats_match:
        raw_nums = [float(x.strip()) for x in stats_match.group(1).replace(",", " ").split() if x.strip()]
        if len(raw_nums) >= 2:
            return compute_statistics_summary(raw_nums)

    # 12. Formula explanations
    if "quadratic" in q or "ax^2" in q:
        return LOCAL_CORPUS["quadratic formula"]
    if "pythagoras" in q or "pythagorean" in q:
        return LOCAL_CORPUS["pythagorean theorem"]
    if "euler" in q and "identity" in q:
        return LOCAL_CORPUS["euler identity"]
    if "derivative" in q or "differentiation" in q:
        return LOCAL_CORPUS["calculus derivative"]
    if "integration" in q or "integral" in q:
        return LOCAL_CORPUS["calculus integration"]
    if "trigonometry" in q or "trigonometric" in q:
        return LOCAL_CORPUS["trigonometry identities"]
        
    return None

def get_local_fallback(query_str: str):
    """Checks Math Solver first, then searches the Sovereign Knowledge Corpus."""
    q_lower = query_str.lower().strip()
    
    math_ans = solve_math_locally(q_lower)
    if math_ans:
        return math_ans
        
    for key, ans in LOCAL_CORPUS.items():
        if key in q_lower:
            return ans
    return None

# ==============================================================================
# 6. GROQ MODEL DISCOVERY & FAILOVER ENGINE
# ==============================================================================
def get_available_models(api_key: str) -> list:
    """Dynamically queries available text-generation LLMs from Groq Cloud."""
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
    except Exception:
        pass
    return default_models

# ==============================================================================
# 7. SESSION STATE MANAGEMENT
# ==============================================================================
if "chat_sessions_v90" not in st.session_state:
    st.session_state.chat_sessions_v90 = {
        "New Chat": [
            {
                "role": "assistant",
                "content": (
                    "Namaste! I am **Indian GPT**, a sovereign multi-lingual and multi-modal AI ecosystem "
                    "created exclusively by **Shubham**.\n\n"
                    "You can ask me anything in **all 22 scheduled Indian languages** (Hindi, Bengali, Tamil, Telugu, "
                    "Marathi, Gujarati, Punjabi, Odia, Malayalam, Kannada, Urdu, Assamese, Sanskrit, etc.) or English, "
                    "explore **Indian & World History**, solve **Complex Mathematics**, search **Live Web News**, "
                    "or type `'generate image of...'` to create **1024×1024 HD Art**!"
                )
            }
        ]
    }

if "current_chat_v90" not in st.session_state:
    st.session_state.current_chat_v90 = "New Chat"

# ==============================================================================
# 8. SIDEBAR CONTROLS, DIAGNOSTICS & EXPORT SUITE
# ==============================================================================
with st.sidebar:
    st.markdown("### 🇮🇳 Indian GPT Control Center")
    if st.button("➕ New Chat Session", use_container_width=True):
        new_chat_name = "New Chat"
        counter = 1
        while new_chat_name in st.session_state.chat_sessions_v90:
            new_chat_name = f"New Chat {counter}"
            counter += 1
        
        st.session_state.chat_sessions_v90[new_chat_name] = [
            {"role": "assistant", "content": "Namaste! New sovereign chat session initialized."}
        ]
        st.session_state.current_chat_v90 = new_chat_name
        st.rerun()

    st.markdown("---")
    st.subheader("💬 Chat History")
    
    for chat_name in list(st.session_state.chat_sessions_v90.keys()):
        if st.button(chat_name, use_container_width=True, key=f"btn_{chat_name}"):
            st.session_state.current_chat_v90 = chat_name
            st.rerun()

    st.markdown("---")
    st.subheader("📥 Export & Backup")
    current_msgs = st.session_state.chat_sessions_v90[st.session_state.current_chat_v90]
    
    # Plain Text Export
    chat_export_text = f"INDIAN GPT - TRANSCRIPT ({st.session_state.current_chat_v90})\n"
    chat_export_text += "=" * 55 + "\n\n"
    for m in current_msgs:
        chat_export_text += f"[{m['role'].upper()}]:\n{m['content']}\n\n"
    
    st.download_button(
        label="📄 Export Transcript (TXT)",
        data=chat_export_text,
        file_name="indian_gpt_transcript.txt",
        mime="text/plain",
        use_container_width=True
    )
    
    # Structured JSON Export
    exportable_json = [
        {"role": m["role"], "content": m["content"]}
        for m in current_msgs
    ]
    st.download_button(
        label="🗂️ Export Session Data (JSON)",
        data=json.dumps(exportable_json, indent=2, ensure_ascii=False),
        file_name="indian_gpt_session.json",
        mime="application/json",
        use_container_width=True
    )

    st.markdown("---")
    with st.expander("📚 Built-in Capabilities Guide"):
        st.markdown(
            "**1. All 22 Indian Languages:**\n"
            "Write in हिन्दी, বাংলা, தமிழ், తెలుగు, मराठी, ગુજરાતી, ਪੰਜਾਬੀ, ଓଡ଼ିଆ, മലയാളം, ಕನ್ನಡ, اردو, অসমীয়া, संस्कृतम्, etc.\n\n"
            "**2. Offline Math Engine Examples:**\n"
            "- `solve quadratic a=1 b=-5 c=6`\n"
            "- `solve linear a=3 b=4 c=19`\n"
            "- `is 97 prime` | `factorial of 12`\n"
            "- `ncr 10 3` | `gcd 24 36`\n"
            "- `trig 45` | `fibonacci 12`\n"
            "- `stats 12, 18, 25, 30, 45`\n"
            "- `compound interest p=10000 r=8 t=5`\n\n"
            "**3. HD Image Synthesis:**\n"
            "- `generate image of futuristic Kolkata at night`"
        )

    st.markdown("---")
    st.subheader("⚙️ System Architecture Stats")
    st.caption(f"• Local Knowledge Entries: **{len(LOCAL_CORPUS)}**")
    st.caption(f"• Supported Indian Scripts: **{len(UNICODE_SCRIPT_RANGES)}**")
    st.caption(f"• Active API Key Pool: **{len(KEYS_POOL)} Keys**")
    st.caption("• Image Engine: **FLUX 1024×1024 HD**")
    st.caption("• Live Web Search: **Tavily Neural Search**")
    st.markdown("---")
    st.caption("Created & Architected by **Shubham**")

# ==============================================================================
# 9. MAIN CONVERSATION VIEWPORT & ROUTING PIPELINE
# ==============================================================================
st.title("🇮🇳 Indian GPT")
st.markdown("##### *Sovereign Multi-Lingual AI Ecosystem • All Indian Languages • World & Indian History • Advanced Math • HD Art*")

if st.session_state.current_chat_v90 not in st.session_state.chat_sessions_v90:
    st.session_state.current_chat_v90 = list(st.session_state.chat_sessions_v90.keys())[0]

current_messages = st.session_state.chat_sessions_v90[st.session_state.current_chat_v90]

# Render existing conversation messages
for message in current_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "image_bytes" in message and message["image_bytes"]:
            st.image(message["image_bytes"])

# Chat Input Box
prompt = st.chat_input("Ask in any Indian language or English, solve complex math, explore history, or type 'generate image of...'")

if prompt:
    # Auto-rename new chat based on first prompt
    if st.session_state.current_chat_v90.startswith("New Chat"):
        new_name = prompt[:28] + ("..." if len(prompt) > 28 else "")
        if new_name in st.session_state.chat_sessions_v90:
            new_name = f"{new_name} (2)"
        
        st.session_state.chat_sessions_v90[new_name] = st.session_state.chat_sessions_v90.pop(st.session_state.current_chat_v90)
        st.session_state.current_chat_v90 = new_name
        current_messages = st.session_state.chat_sessions_v90[new_name]

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
            detected_script = detect_indian_script(prompt)
            
            # Intent Classification: Image Generation vs. Search vs. Reasoning/Math
            image_starters = [
                "generate", "genarate", "draw", "create", "make",
                "chobi", "banao", "toiri", "pic", "photo", "image", "ghibli", "wallpaper"
            ]
            is_image_request = any(starter in p_lower for starter in image_starters)
            
            if is_image_request:
                steps = [
                    "🎨 Analyzing prompt semantics and depth layers...",
                    "📐 Constructing 1024×1024 high-resolution composition...",
                    "✨ Rendering photorealistic lighting, shadows & textures...",
                    "🚀 Finalizing ultra-HD polish via FLUX Neural Engine..."
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
                    time.sleep(0.75)
                
                enhanced_prompt = f"{prompt}, highly detailed, professional photography, stunning composition, 8k resolution, photorealistic masterpiece"
                encoded_prompt = urllib.parse.quote(enhanced_prompt)
                image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&model=flux&nologo=true"
                
                try:
                    img_resp = requests.get(image_url, timeout=35)
                    if img_resp.status_code == 200 and len(img_resp.content) > 1000:
                        generated_image_bytes = img_resp.content
                        full_response = "Here is your generated high-definition masterpiece:"
                    else:
                        full_response = "Could not render image at the moment. Please try again!"
                except Exception:
                    full_response = "Image generation took longer than expected. Please try again!"
                
                message_placeholder.markdown(full_response)
                if generated_image_bytes:
                    st.image(generated_image_bytes)
            else:
                greetings = ["hi", "hello", "hey", "hii", "hola", "sup", "good morning", "good evening", "bye", "namaste", "pranam", "nomoskar"]
                is_simple_greeting = p_lower in greetings
                
                search_triggers = [
                    "winner", "jiteche", "won", "match", "score", "news",
                    "current", "ajke", "ekhon", "latest", "2026", "who won", "today", "weather", "price"
                ]
                needs_search = any(trigger in p_lower for trigger in search_triggers) and not is_simple_greeting
                
                search_context = ""
                
                if needs_search:
                    search_loading_html = """
                    <div style="display: flex; align-items: center; gap: 6px; font-style: italic; color: #a5b4fc;">
                        <span>🌐 searching live internet knowledge</span>
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
                        <span>🤖 reasoning & synthesizing answer</span>
                        <span class="dot1" style="font-size: 20px;">.</span>
                        <span class="dot2" style="font-size: 20px;">.</span>
                        <span class="dot3" style="font-size: 20px;">.</span>
                    </div>
                    """
                    message_placeholder.markdown(thinking_html, unsafe_allow_html=True)
                
                ist = timezone(timedelta(hours=5, minutes=30))
                current_time_str = datetime.now(ist).strftime("%Y-%m-%d %H:%M:%S")
                
                # Sovereign Multi-Lingual & Academic Reasoning System Prompt
                system_content = (
                    f"Current Indian Standard Time (IST) is {current_time_str}. "
                    f"Detected User Input Script: {detected_script}. "
                    "You are Indian GPT, an advanced sovereign AI assistant created exclusively by Shubham. "
                    "If anyone asks who created, built, or owns you, always proudly state that you were created by Shubham. "
                    "SOVEREIGN MULTI-LINGUAL & ACADEMIC GOVERNANCE DIRECTIVE: "
                    "1. You natively understand and communicate fluently in ALL 22 scheduled Indian languages and scripts "
                    "(Hindi, Bengali, Telugu, Marathi, Tamil, Urdu, Gujarati, Malayalam, Kannada, Odia, Punjabi, Assamese, "
                    "Sanskrit, Kashmiri, Sindhi, Konkani, Manipuri, Nepali, Dogri, Maithili, Santhali, Bodo) as well as English, Banglish, and Hinglish. "
                    "2. Always reply in the exact same language, script, and conversational register used by the user. "
                    "3. When asked about Indian History, World History, Geography, Science, or Complex Mathematics (Algebra, Calculus, "
                    "Trigonometry, Number Theory, Physics equations), provide thorough, step-by-step, mathematically rigorous explanations using clear formatting."
                )
                
                if search_context:
                    system_content += f"\n\nLive Web Search Context:\n{search_context}"

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
                                                except Exception:
                                                    pass
                                message_placeholder.markdown(full_response)
                                success = success or (len(full_response.strip()) > 0)
                                if success:
                                    break
                            elif response.status_code == 429:
                                time.sleep(1)
                                continue
                        except Exception:
                            continue
                
                # Offline Local Knowledge & Math Engine Fallback
                if not success:
                    local_ans = get_local_fallback(prompt)
                    if local_ans:
                        full_response = local_ans
                        success = True
                    else:
                        full_response = "Namaste! Server is currently handling high traffic. Please click send again!"
                    message_placeholder.markdown(full_response)
            
            assistant_msg = {"role": "assistant", "content": full_response}
            if generated_image_bytes:
                assistant_msg["image_bytes"] = generated_image_bytes
                
            current_messages.append(assistant_msg)
            st.rerun()
        except Exception as e:
            st.error(f"System Notice: {e}")
