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
# Version: 11.0 Enterprise Sovereign Edition
# ==============================================================================

st.set_page_config(
    page_title="Indian GPT - Sovereign Hybrid AI Ecosystem",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# 1. CYBERPUNK & HIGH-CONTRAST GLASSMORPHISM UI STYLING (HIGH BRIGHTNESS BG)
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
# 2. CONNECTIVITY DETECTION & API KEY POOL
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

TAVILY_API_KEY = "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"

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
# 4. MASSIVE SOVEREIGN KNOWLEDGE CORPUS (200+ OFFLINE & HYBRID ENTRIES)
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

    # All 28 States
    "andhra pradesh": "Amaravati is the capital of Andhra Pradesh, known for Kuchipudi classical dance, Tirupati temple, Visakhapatnam port, and a 974 km Bay of Bengal coastline.",
    "arunachal pradesh": "Itanagar is the capital of Arunachal Pradesh, known as the 'Land of the Dawn-Lit Mountains' in Northeast India, home to Tawang Monastery.",
    "assam": "Dispur is the capital of Assam, world-famous for Assam tea, Kaziranga National Park (Great One-Horned Rhinoceros), Majuli river island, and Bihu festival.",
    "bihar": "Patna (ancient Pataliputra) is the capital of Bihar, ancient cradle of Buddhism and Jainism, Maurya and Gupta empires, Nalanda University, and Bodh Gaya.",
    "chhattisgarh": "Raipur is the capital of Chhattisgarh, known for Chitrakote Falls ('Niagara of India'), rich mineral and steel production, and vibrant tribal art.",
    "goa": "Panaji is the capital of Goa, India's smallest state by area, famous for Arabian Sea beaches, Konkani culture, Dudhsagar Falls, and Indo-Portuguese architecture.",
    "gujarat": "Gandhinagar is the capital of Gujarat, birthplace of Mahatma Gandhi and Sardar Vallabhbhai Patel, home to Gir Asiatic Lions, Rann of Kutch, and the 182m Statue of Unity.",
    "haryana": "Chandigarh is the shared capital of Haryana, historically famous for the Kurukshetra war of the Mahabharata and the three decisive Battles of Panipat.",
    "himachal pradesh": "Shimla is the summer capital (Dharamshala winter) of Himachal Pradesh, a Himalayan state famous for Kullu-Manali, Rohtang Pass, and apple orchards.",
    "jharkhand": "Ranchi is the capital of Jharkhand, the 'Land of Forests', rich in coal, iron ore, mica, Jamshedpur steel city, and Hundru Falls.",
    "karnataka": "Bengaluru is the capital of Karnataka and the 'Silicon Valley of India', also renowned for Vijayanagara ruins at Hampi, Mysore Palace, and Coorg coffee.",
    "kerala": "Thiruvananthapuram is the capital of Kerala, 'God's Own Country', celebrated for backwaters, Kathakali, Mohiniyattam, Ayurveda, spices, and India's highest literacy rate.",
    "madhya pradesh": "Bhopal is the capital of Madhya Pradesh, the 'Heart of India', home to Khajuraho temples, Sanchi Stupa, Bhimbetka rock shelters, and Kanha & Bandhavgarh tiger reserves.",
    "maharashtra": "Mumbai is the capital of Maharashtra and India's financial & entertainment capital, also home to Ajanta and Ellora caves and Chhatrapati Shivaji Maharaj's forts.",
    "manipur": "Imphal is the capital of Manipur, the 'Jewel of India', famous for Loktak Lake (floating phumdis), Keibul Lamjao National Park, Manipuri dance, and modern polo.",
    "meghalaya": "Shillong is the capital of Meghalaya, the 'Abode of Clouds', famous for living root bridges, Cherrapunji, and Mawsynram (wettest place on Earth).",
    "mizoram": "Aizawl is the capital of Mizoram, known for its lush blue mountains, bamboo dance (Cheraw), and high literacy.",
    "nagaland": "Kohima is the capital of Nagaland, famous for the annual Hornbill Festival, Dzukou Valley, and rich Naga warrior heritage.",
    "odisha": "Bhubaneswar is the capital of Odisha, renowned for the Konark Sun Temple, Jagannath Temple in Puri, Chilika Lake, Hirakud Dam, and Odissi classical dance.",
    "punjab": "Chandigarh is the shared capital of Punjab, the 'Land of Five Rivers', home to the Golden Temple (Harmandir Sahib) in Amritsar, Jallianwala Bagh, and Bhangra.",
    "rajasthan": "Jaipur (the Pink City) is the capital of Rajasthan, India's largest state by area, famous for the Thar Desert, Amer Fort, Udaipur lakes, and Jodhpur.",
    "sikkim": "Gangtok is the capital of Sikkim, India's first 100% organic state, home to Mount Kangchenjunga (8,586 m, India's highest peak) and Nathu La pass.",
    "tamil nadu": "Chennai is the capital of Tamil Nadu, famed for Chola temples (Brihadeeswarar), Bharatanatyam, classical Sangam literature, Kanyakumari, and Marina Beach.",
    "telangana": "Hyderabad is the capital of Telangana, famous for Charminar, Golconda Fort, Ramoji Film City, Hyderabadi biryani, and major IT & biotech hubs.",
    "tripura": "Agartala is the capital of Tripura, known for Ujjayanta Palace, Neermahal water palace, Unakoti rock carvings, and bamboo crafts.",
    "uttar pradesh": "Lucknow is the capital of Uttar Pradesh, India's most populous state, home to the Taj Mahal in Agra, Varanasi, Ayodhya, Prayagraj, and Mathura.",
    "uttarakhand": "Dehradun is the winter capital (Gairsain summer) of Uttarakhand, known as 'Devbhumi' (Land of the Gods), home to Gangotri, Yamunotri, Kedarnath, Badrinath, and Jim Corbett National Park.",
    "west bengal": "Kolkata is the capital of West Bengal, cultural and intellectual capital of India, home to Rabindranath Tagore, Howrah Bridge, Sundarbans, Darjeeling tea, and Durga Puja.",

    # 8 Union Territories
    "andaman and nicobar": "Port Blair (Sri Vijaya Puram) is the capital of the Andaman and Nicobar Islands in the Bay of Bengal, home to historic Cellular Jail and Barren Island volcano.",
    "chandigarh": "Chandigarh is a Union Territory and the planned shared capital of Punjab and Haryana, designed by Swiss-French architect Le Corbusier.",
    "dadra and nagar haveli": "Daman is the capital of the Union Territory of Dadra and Nagar Haveli and Daman and Diu on India's western Arabian Sea coast.",
    "delhi": "New Delhi is the National Capital Territory (NCT) of India, housing Rashtrapati Bhavan, Parliament House, Supreme Court, India Gate, and Red Fort.",
    "jammu and kashmir": "Srinagar (summer) and Jammu (winter) are the capitals of Jammu and Kashmir, famed for Dal Lake, Mughal gardens, Gulmarg, and Vaishno Devi.",
    "ladakh": "Leh and Kargil are the capitals of Ladakh, a high-altitude trans-Himalayan cold desert known for Pangong Tso, Nubra Valley, and Hemis Monastery.",
    "lakshadweep": "Kavaratti is the capital of Lakshadweep, India's smallest Union Territory comprising 36 coral atolls and islands in the Arabian Sea.",
    "puducherry": "Puducherry is a Union Territory on the Coromandel Coast renowned for its French Quarter, Promenade Beach, Auroville, and Sri Aurobindo Ashram.",

    # National Symbols & Constitutional Facts
    "capital of india": "New Delhi is the capital of India.",
    "national bird": "The Indian Peafowl (Pavo cristatus / Peacock) is the national bird of India.",
    "national animal": "The Royal Bengal Tiger (Panthera tigris tigris) is the national animal of India.",
    "national flower": "The Sacred Lotus (Nelumbo nucifera) is the national flower of India.",
    "national tree": "The Indian Banyan Tree (Ficus benghalensis) is the national tree of India.",
    "national fruit": "The Mango (Mangifera indica) is the national fruit of India.",
    "national river": "The Ganga (Ganges) is the national river of India.",
    "national anthem": "Jana Gana Mana, composed in Bengali by Rabindranath Tagore and adopted on January 24, 1950, is the national anthem of India.",
    "constitution of india": "Drafted by the Constituent Assembly chaired by Dr. B. R. Ambedkar, adopted on November 26, 1949, and enforced on January 26, 1950, the Constitution of India is the world's longest written constitution.",

    # Indian History & Freedom Struggle
    "indus valley civilization": "The Indus Valley Civilization (c. 3300–1300 BCE), also called the Harappan Civilization, was one of the world's earliest urban civilizations, famed for Harappa, Mohenjo-daro, Lothal dockyard, grid city planning, and covered drainage.",
    "vedic period": "The Vedic Period (c. 1500–500 BCE) produced the four Vedas (Rigveda, Samaveda, Yajurveda, Atharvaveda), Upanishads, and the Sanskrit epics Ramayana and Mahabharata.",
    "maurya empire": "Founded by Chandragupta Maurya in 322 BCE with Chanakya's statecraft (Arthashastra), the Maurya Empire peaked under Ashoka the Great, who embraced Buddhism and non-violence after the Kalinga War (261 BCE).",
    "gupta empire": "The Gupta Empire (c. 319–550 CE) is celebrated as the Golden Age of India, producing Aryabhata (zero, decimal place value, $\pi$), Varahamihira, Sushruta/Charaka medical traditions, and poet Kalidasa.",
    "chola dynasty": "The Chola Dynasty of Tamilakam (under Rajaraja Chola I and Rajendra Chola I) ruled a vast maritime empire extending to Sri Lanka and Southeast Asia and built the Brihadeeswarar Temple at Thanjavur.",
    "delhi sultanate": "The Delhi Sultanate (1206–1526 CE) spanned five dynasties: Mamluk (Slave), Khalji, Tughlaq, Sayyid, and Lodi, repelling Mongol invasions and introducing Indo-Islamic architecture.",
    "mughal empire": "Established by Babur in 1526 after the First Battle of Panipat, the Mughal Empire flourished under Akbar the Great, Jahangir, Shah Jahan (Taj Mahal, Red Fort), and Aurangzeb.",
    "maratha empire": "Founded by Chhatrapati Shivaji Maharaj in 1674, the Maratha Empire dismantled Mughal hegemony across India through agile guerrilla tactics (Ganimi Kava) and a strong Konkan navy.",
    "battle of plassey": "On June 23, 1757, British East India Company forces under Robert Clive defeated Nawab Siraj-ud-Daulah of Bengal, laying the foundation of British colonial rule in India.",
    "revolt of 1857": "The Indian Rebellion of 1857 (First War of Independence) erupted in Meerut on May 10, 1857, led by Mangal Pandey, Rani Lakshmibai of Jhansi, Tatya Tope, Nana Sahib, and Bahadur Shah Zafar.",
    "partition of bengal": "Enacted in 1905 by Viceroy Lord Curzon, the Partition of Bengal ignited the Swadeshi and Boycott movements and Rabindranath Tagore's Raksha Bandhan unity campaign until annulled in 1911.",
    "jallianwala bagh": "On April 13, 1919 (Baisakhi), Brigadier-General Reginald Dyer ordered troops to fire on unarmed civilians at Jallianwala Bagh in Amritsar, prompting Rabindranath Tagore to renounce his British knighthood.",
    "non cooperation movement": "Launched by Mahatma Gandhi in 1920, the Non-Cooperation Movement called for peaceful boycott of British institutions, foreign cloth, and courts to attain Swaraj.",
    "dandi march": "From March 12 to April 6, 1930, Mahatma Gandhi marched 240 miles from Sabarmati Ashram to Dandi to make salt from seawater, launching the Civil Disobedience Movement.",
    "quit india movement": "On August 8, 1942, Mahatma Gandhi issued the 'Do or Die' call at Gowalia Tank Maidan in Bombay, launching the Quit India Movement demanding immediate British withdrawal.",
    "netaji subhash chandra bose": "Netaji Subhash Chandra Bose escaped house arrest in Kolkata in 1941, reorganized the Azad Hind Fauj (INA) in 1943, established the Provisional Government of Free India (Azad Hind), and gave the rallying cry 'Jai Hind' and 'Delhi Chalo'.",
    "independence day": "India won independence from British rule at midnight on August 15, 1947, with Jawaharlal Nehru delivering his iconic 'Tryst with Destiny' speech.",
    "republic day": "India became a Sovereign Democratic Republic on January 26, 1950, when the Constitution of India came into effect and Dr. Rajendra Prasad took office as India's first President.",

    # World History & Global Civilizations
    "mesopotamia": "Mesopotamia (between the Tigris and Euphrates rivers in modern Iraq) is the 'Cradle of Civilization', home to Sumerians, Babylonians, cuneiform script, the wheel, and Hammurabi's Code.",
    "ancient egypt": "Ancient Egypt flourished along the Nile for over 3,000 years, famed for the Pyramids of Giza, Sphinx, Pharaohs, hieroglyphics, papyrus, and mummification.",
    "ancient greece": "Ancient Greece birthed Athenian democracy, classical philosophy (Socrates, Plato, Aristotle), Euclidean geometry, Hippocratic medicine, and the Olympic Games.",
    "roman empire": "The Roman Empire (27 BCE–476 CE in the West) governed the Mediterranean basin, leaving a lasting legacy in civil law, Latin, concrete domes, aqueducts, and the Colosseum.",
    "silk road": "The Silk Road was a vast trans-Eurasian trade network linking China and India with Persia, Arabia, and Europe, exchanging silk, spices, paper, gunpowder, and philosophies.",
    "renaissance": "The Renaissance (14th–17th century) was a European cultural and scientific revival starting in Florence, Italy, led by Leonardo da Vinci, Michelangelo, Raphael, Galileo, and Copernicus.",
    "industrial revolution": "Starting in Britain around 1760, the Industrial Revolution mechanized manufacturing via steam engines, textile mills, iron smelting, and railways.",
    "world war 1": "World War I (1914–1918) pitted the Allied Powers against the Central Powers across trench-warfare fronts in Europe, ending with the 1918 Armistice and 1919 Treaty of Versailles.",
    "world war 2": "World War 2 (1939–1945) was the deadliest conflict in human history, fought between the Allies and the Axis powers, ending in 1945 and leading to the founding of the United Nations.",

    # Science, Space & Physics
    "isro": "The Indian Space Research Organisation (ISRO), founded in 1969 by Dr. Vikram Sarabhai and headquartered in Bengaluru, is India's premier space agency famous for PSLV, GSLV, Chandrayaan, Mangalyaan, and Aditya-L1.",
    "chandrayaan 3": "Launched by ISRO on July 14, 2023, Chandrayaan-3's Vikram lander and Pragyan rover successfully soft-landed near the Moon's south pole on August 23, 2023 (celebrated as National Space Day in India).",
    "mangalyaan": "ISRO's Mars Orbiter Mission (Mangalyaan), launched on November 5, 2013, made India the first Asian country to reach Mars orbit and the first nation globally to succeed on its very first attempt.",
    "aditya l1": "Aditya-L1 is India's first solar space observatory mission placed in a halo orbit around the Sun-Earth Lagrange Point 1 (L1) to study solar coronal mass ejections and space weather.",
    "speed of light": "The speed of light in vacuum is an exact universal physical constant: $c = 299,792,458 \text{ m/s}$ ($\approx 3 \times 10^8 \text{ m/s}$).",
    "newton laws": "Newton's Three Laws of Motion: (1) An object remains at rest or uniform motion unless acted upon by a net external force; (2) $F = ma$; (3) Every action has an equal and opposite reaction.",
    "relativity": "Einstein's Special Relativity (1905) established $E = mc^2$ and time dilation, while General Relativity (1915) explained gravity as the geometric curvature of four-dimensional spacetime.",
    "quantum mechanics": "Quantum Mechanics governs matter and energy at atomic scales, featuring Planck's quantization ($E = h\nu$), wave-particle duality, and Heisenberg's Uncertainty Principle.",
    "dna": "Deoxyribonucleic Acid (DNA) is a double-stranded helical polymer of nucleotides encoding genetic instructions for all living organisms.",
    "mitochondria": "Mitochondria are double-membraned eukaryotic organelles known as the 'powerhouse of the cell' because they synthesize ATP via oxidative phosphorylation.",
    "periodic table": "The Modern Periodic Table arranges all 118 chemical elements in order of increasing atomic number ($Z$) across 18 groups and 7 periods.",

    # Computer Science & AI
    "python": "Python is a high-level, interpreted programming language created by Guido van Rossum in 1991, celebrated for readable syntax and dominant ecosystems in AI, machine learning, web apps (Streamlit, Django, FastAPI), and automation.",
    "artificial intelligence": "Artificial Intelligence (AI) is the branch of computer science focused on building systems capable of reasoning, natural language understanding, perception, learning, and autonomous decision-making.",
    "machine learning": "Machine Learning (ML) enables algorithms to learn statistical patterns from training data without hard-coded rules.",
    "deep learning": "Deep Learning uses multi-layered artificial neural networks—including Transformers and CNNs—to achieve state-of-the-art performance in language and vision.",
    "large language model": "A Large Language Model (LLM) is a Transformer-based neural network trained on massive multilingual text corpora to perform reasoning, coding, translation, and text generation.",

    # World Capitals
    "afghanistan capital": "Kabul is the capital of Afghanistan.",
    "australia capital": "Canberra is the capital of Australia.",
    "bangladesh capital": "Dhaka is the capital of Bangladesh.",
    "brazil capital": "Brasília is the capital of Brazil.",
    "canada capital": "Ottawa is the capital of Canada.",
    "china capital": "Beijing is the capital of China.",
    "egypt capital": "Cairo is the capital of Egypt.",
    "france capital": "Paris is the capital of France.",
    "germany capital": "Berlin is the capital of Germany.",
    "japan capital": "Tokyo is the capital of Japan.",
    "russia capital": "Moscow is the capital of Russia.",
    "uk capital": "London is the capital of the United Kingdom.",
    "usa capital": "Washington, D.C. is the capital of the United States of America.",

    # Great Personalities & Scientists
    "aryabhata": "Aryabhata (476–550 CE) was India's pioneering mathematician-astronomer who authored the Aryabhatiya, formalized place-value arithmetic, approximated $\pi \approx 3.1416$, and explained solar and lunar eclipses.",
    "brahmagupta": "Brahmagupta (598–668 CE) was an ancient Indian mathematician who first defined arithmetic rules for zero ($0$) and negative integers in his 628 CE work Brahmasphutasiddhanta.",
    "srinivasa ramanujan": "Srinivasa Ramanujan (1887–1920) was a self-taught Indian mathematical prodigy who discovered thousands of theorems in number theory, infinite series for $\pi$, and partition theory.",
    "cv raman": "Sir C. V. Raman (1888–1970) won the 1930 Nobel Prize in Physics—the first Asian scientist to win a science Nobel—for discovering the Raman Effect.",
    "rabindranath tagore": "Rabindranath Tagore (1861–1941) won the 1913 Nobel Prize in Literature for Gitanjali, founded Visva-Bharati University at Santiniketan, and composed the national anthems of India and Bangladesh.",
    "apj abdul kalam": "Dr. A. P. J. Abdul Kalam (1931–2015), the 'Missile Man of India' and 11th President of India, spearheaded India's SLV-III, Agni, and Prithvi programmes and inspired millions of students.",
    "homi bhabha": "Dr. Homi Jehangir Bhabha (1909–1966) was the visionary architect of India's three-stage nuclear power programme and founding director of TIFR and BARC.",
    "vikram sarabhai": "Dr. Vikram Sarabhai (1919–1971) is celebrated as the Father of the Indian Space Programme and founder of ISRO.",
    "swami vivekananda": "Swami Vivekananda (1863–1902) introduced Vedanta and Yoga to the Western world at the 1893 Parliament of the World's Religions in Chicago and founded the Ramakrishna Mission.",
    "mahatma gandhi": "Mohandas Karamchand Gandhi (1869–1948), the 'Father of the Nation', led India's non-violent freedom struggle through Satyagraha, Non-Cooperation, Dandi Salt March, and Quit India movements.",
    "dr br ambedkar": "Dr. Bhimrao Ramji Ambedkar (1891–1956) served as Chairman of the Constitution Drafting Committee and independent India's first Law Minister.",
    "sardar vallabhbhai patel": "Sardar Vallabhbhai Patel (1875–1950), the 'Iron Man of India' and first Deputy Prime Minister & Home Minister, unified 562 princely states into the Union of India.",
    "isaac newton": "Sir Isaac Newton (1643–1727) formulated classical mechanics, universal gravitation, and differential/integral calculus in his Principia Mathematica.",
    "albert einstein": "Albert Einstein (1879–1955) revolutionized modern physics with Special and General Relativity and won the 1921 Nobel Prize in Physics.",
    "nikola tesla": "Nikola Tesla (1856–1943) pioneered alternating current (AC) electrical power systems, induction motors, and wireless transmission experiments.",
    "alan turing": "Alan Turing (1912–1954) conceptualized the universal Turing Machine, broke the Enigma cipher during WWII, and proposed the Turing Test for artificial intelligence.",

    # Mathematics Formulas
    "quadratic formula": "For any quadratic equation $ax^2 + bx + c = 0$ ($a \neq 0$), the roots are:\n$$x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$$",
    "pythagorean theorem": "In any right-angled triangle with legs $a, b$ and hypotenuse $c$:\n$$a^2 + b^2 = c^2$$",
    "euler identity": "Euler's Identity unites five fundamental mathematical constants:\n$$e^{i\pi} + 1 = 0$$",
    "calculus derivative": "The derivative measures instantaneous rate of change:\n$$f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}, \quad \frac{d}{dx}(x^n) = nx^{n-1}$$",
    "calculus integration": "Indefinite integral power rule:\n$$\int x^n \, dx = \frac{x^{n+1}}{n+1} + C \quad (n \neq -1)$$"
}

# ==============================================================================
# 5. SMART TOKEN-SCORED OFFLINE RETRIEVAL ENGINE
# ==============================================================================
STOPWORDS = {
    "what", "is", "the", "of", "in", "on", "at", "to", "for", "a", "an", "and",
    "or", "who", "was", "were", "are", "tell", "me", "about", "explain", "define",
    "describe", "how", "why", "when", "where", "which", "give", "write", "can", "you",
    "please", "ki", "kake", "bole", "bolo", "somporke", "kya", "hai", "batao", "ke"
}

def tokenize_query(text: str) -> set:
    """Extracts meaningful lowercase content tokens from a query string."""
    words = re.findall(r"[a-z0-9]+", text.lower())
    return {w for w in words if w not in STOPWORDS and len(w) > 1}

def retrieve_from_local_corpus(query_str: str, top_k: int = 2) -> list:
    """Retrieves relevant knowledge entries from LOCAL_CORPUS using token overlap scoring."""
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
            if key_coverage >= 0.5 and score >= 1.8:
                scored_matches.append((key, ans, score))

    scored_matches.sort(key=lambda x: x[2], reverse=True)
    return scored_matches[:top_k]

# ==============================================================================
# 6. OFFLINE SYMBOLIC & NUMERICAL MATH & GEOMETRY ENGINE
# ==============================================================================
def solve_quadratic_equation(a: float, b: float, c: float) -> str:
    """Solves ax^2 + bx + c = 0 with full step-by-step discriminant analysis."""
    if a == 0:
        if b == 0:
            return "Invalid equation: both $a$ and $b$ cannot be zero."
        root = -c / b
        return f"This reduces to a linear equation ($bx + c = 0$). Solution: $x = \mathbf{{{root:.4f}}}$."
    
    discriminant = (b ** 2) - (4 * a * c)
    steps = [
        f"**Step 1: Identify Coefficients**\n$a = {a}$, $b = {b}$, $c = {c}$",
        f"**Step 2: Compute Discriminant ($\Delta = b^2 - 4ac$)**\n$\Delta = ({b})^2 - 4({a})({c}) = \mathbf{{{discriminant:.4f}}}$"
    ]
    
    if discriminant > 0:
        r1 = (-b + math.sqrt(discriminant)) / (2 * a)
        r2 = (-b - math.sqrt(discriminant)) / (2 * a)
        steps.append(
            f"**Step 3: Two Distinct Real Roots ($\Delta > 0$)**\n"
            f"$$x_1 = \frac{{-({b}) + \sqrt{{{discriminant:.4f}}}}}{{2({a})}} = \mathbf{{{r1:.4f}}}$$\n"
            f"$$x_2 = \frac{{-({b}) - \sqrt{{{discriminant:.4f}}}}}{{2({a})}} = \mathbf{{{r2:.4f}}}$$"
        )
    elif discriminant == 0:
        r = -b / (2 * a)
        steps.append(
            f"**Step 3: One Repeated Real Root ($\Delta = 0$)**\n"
            f"$$x = \frac{{-({b})}}{{2({a})}} = \mathbf{{{r:.4f}}}$$"
        )
    else:
        real_part = -b / (2 * a)
        imag_part = math.sqrt(abs(discriminant)) / (2 * a)
        steps.append(
            f"**Step 3: Two Complex Conjugate Roots ($\Delta < 0$)**\n"
            f"$$x_1 = \mathbf{{{real_part:.4f} + {imag_part:.4f}i}}$$\n"
            f"$$x_2 = \mathbf{{{real_part:.4f} - {imag_part:.4f}i}}$$"
        )
    return "\n\n".join(steps)

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

def check_prime_and_factors(n: int) -> str:
    """Checks primality and computes full prime factorization."""
    if n <= 1:
        return f"**{n}** is neither prime nor composite."
    if n <= 3:
        return f"**{n}** is a **Prime Number**."
    
    temp = n
    prime_factors = {}
    d = 2
    while d * d <= temp:
        while temp % d == 0:
            prime_factors[d] = prime_factors.get(d, 0) + 1
            temp //= d
        d += 1
    if temp > 1:
        prime_factors[temp] = prime_factors.get(temp, 0) + 1

    if len(prime_factors) == 1 and list(prime_factors.values())[0] == 1:
        return f"**{n}** is a **Prime Number** (divisible only by 1 and {n})."

    factor_str = " × ".join(
        f"{p}^{exp}" if exp > 1 else f"{p}"
        for p, exp in sorted(prime_factors.items())
    )
    return (
        f"**{n}** is a **Composite Number**.\n"
        f"• **Prime Factorization:** ${n} = {factor_str}$"
    )

def compute_factorial(n: int) -> str:
    """Computes n! safely up to n = 100."""
    if n < 0:
        return "Factorial is not defined for negative integers."
    if n > 100:
        return "Input too large for instant display; please enter $n \le 100$."
    val = math.factorial(n)
    return f"The factorial of **{n}** is:\n$${n}! = {val}$$"

def compute_combinatorics(n: int, r: int) -> str:
    """Computes Permutation nPr and Combination nCr."""
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
    """Computes GCD and LCM."""
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
    """Computes trigonometric ratios in degrees."""
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

def compute_compound_interest(p: float, r: float, t: float, n: int = 1) -> str:
    """Computes Compound Interest and Final Amount."""
    if p < 0 or r < 0 or t < 0 or n <= 0:
        return "Invalid inputs: Principal, Rate, and Time must be non-negative."
    amount = p * ((1 + (r / (100 * n))) ** (n * t))
    ci = amount - p
    return (
        f"**Compound Interest Calculation ($A = P(1 + \frac{{r}}{{100n}})^{{nt}}$):**\n"
        f"• **Principal ($P$):** ₹{p:,.2f}\n"
        f"• **Annual Rate ($r$):** {r}% | **Time ($t$):** {t} years\n"
        f"• **Total Compound Interest ($CI$):** **₹{ci:,.2f}**\n"
        f"• **Final Maturity Amount ($A$):** **₹{amount:,.2f}**"
    )

def compute_statistics_summary(numbers: list) -> str:
    """Computes Mean, Median, Variance, and Standard Deviation."""
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

def compute_geometry_metrics(shape: str, nums: list) -> str:
    """Computes area, perimeter, and volume for geometric shapes."""
    if shape == "circle" and len(nums) >= 1:
        r = nums[0]
        area = math.pi * (r ** 2)
        circ = 2 * math.pi * r
        return f"**Circle Geometry ($r = {r}$):**\n• **Area ($\pi r^2$):** **{area:.4f}**\n• **Circumference ($2\pi r$):** **{circ:.4f}**"
    elif shape == "sphere" and len(nums) >= 1:
        r = nums[0]
        vol = (4.0 / 3.0) * math.pi * (r ** 3)
        surf = 4 * math.pi * (r ** 2)
        return f"**Sphere Geometry ($r = {r}$):**\n• **Volume ($\frac{{4}}{{3}}\pi r^3$):** **{vol:.4f}**\n• **Surface Area ($4\pi r^2$):** **{surf:.4f}**"
    elif shape == "rectangle" and len(nums) >= 2:
        l, w = nums[0], nums[1]
        return f"**Rectangle Geometry ($l = {l}, w = {w}$):**\n• **Area ($l \times w$):** **{l * w:.4f}**\n• **Perimeter ($2(l + w)$):** **{2 * (l + w):.4f}**"
    elif shape == "triangle" and len(nums) >= 2:
        b, h = nums[0], nums[1]
        return f"**Triangle Geometry (base $b = {b}$, height $h = {h}$):**\n• **Area ($\frac{{1}}{{2}}bh$):** **{0.5 * b * h:.4f}**"
    return ""

def evaluate_safe_arithmetic(expr: str):
    """Safely evaluates arithmetic expressions."""
    cleaned = (
        expr.lower()
        .replace("calculate", "")
        .replace("compute", "")
        .replace("evaluate", "")
        .replace("solve", "")
        .replace("what is", "")
        .replace("?", "")
        .replace("×", "*")
        .replace("÷", "/")
        .strip()
    )
    if not cleaned:
        return None
    allowed_chars = set("0123456789+-*/().^ ")
    if all(c in allowed_chars for c in cleaned) and any(c.isdigit() for c in cleaned) and any(op in cleaned for op in "+-*/^"):
        try:
            py_expr = cleaned.replace("^", "**")
            result = eval(py_expr, {"__builtins__": None}, {})
            return f"**Exact Mathematical Calculation:**\n`{cleaned}` = **{result}**"
        except Exception:
            return None
    return None

def solve_math_locally(query_str: str):
    """Routes mathematical queries to specialized offline solvers."""
    q = query_str.lower().strip()
    arith = evaluate_safe_arithmetic(q)
    if arith:
        return arith

    sqrt_match = re.search(r"(?:sqrt|square\s+root\s+(?:of\s+)?)(\d+\.?\d*)", q)
    if sqrt_match:
        val = float(sqrt_match.group(1))
        if val >= 0:
            return f"**Square Root Result:**\n$$\sqrt{{{val}}} = \mathbf{{{math.sqrt(val):.6f}}}$$"

    prime_match = re.search(r"(?:is\s+(\d+)\s+(?:a\s+)?prime|factorize\s+(\d+)|prime\s+factors\s+(?:of\s+)?(\d+))", q)
    if prime_match:
        num_s = prime_match.group(1) or prime_match.group(2) or prime_match.group(3)
        return check_prime_and_factors(int(num_s))

    fact_match = re.search(r"factorial\s+(?:of\s+)?(\d+)|(\d+)!", q)
    if fact_match:
        num_str = fact_match.group(1) or fact_match.group(2)
        return compute_factorial(int(num_str))

    quad_match = re.search(r"a\s*=\s*(-?\d+\.?\d*)[,\s]+b\s*=\s*(-?\d+\.?\d*)[,\s]+c\s*=\s*(-?\d+\.?\d*)", q)
    if quad_match and "linear" not in q:
        return solve_quadratic_equation(float(quad_match.group(1)), float(quad_match.group(2)), float(quad_match.group(3)))

    lin_match = re.search(r"linear\s+a\s*=\s*(-?\d+\.?\d*)[,\s]+b\s*=\s*(-?\d+\.?\d*)[,\s]+c\s*=\s*(-?\d+\.?\d*)", q)
    if lin_match:
        return solve_linear_equation(float(lin_match.group(1)), float(lin_match.group(2)), float(lin_match.group(3)))

    comb_match = re.search(r"(?:ncr|npr|combination|permutation)\s+(\d+)[,\s]+(\d+)", q)
    if comb_match:
        return compute_combinatorics(int(comb_match.group(1)), int(comb_match.group(2)))

    gcd_match = re.search(r"(?:gcd|hcf|lcm)\s+(\d+)[,\s]+(\d+)", q)
    if gcd_match:
        return compute_gcd_lcm(int(gcd_match.group(1)), int(gcd_match.group(2)))

    fib_match = re.search(r"fibonacci\s+(\d+)", q)
    if fib_match:
        return generate_fibonacci(int(fib_match.group(1)))

    trig_match = re.search(r"(?:trig|sin|cos|tan)\s+(-?\d+\.?\d*)", q)
    if trig_match:
        return compute_trig_degrees(float(trig_match.group(1)))

    ci_match = re.search(r"compound\s+interest\s+p\s*=\s*(\d+\.?\d*)[,\s]+r\s*=\s*(\d+\.?\d*)[,\s]+t\s*=\s*(\d+\.?\d*)", q)
    if ci_match:
        return compute_compound_interest(float(ci_match.group(1)), float(ci_match.group(2)), float(ci_match.group(3)))

    stats_match = re.search(r"(?:stats|statistics|mean|median)\s+([0-9.,\s-]+)", q)
    if stats_match:
        raw_nums = [float(x.strip()) for x in stats_match.group(1).replace(",", " ").split() if x.strip()]
        if len(raw_nums) >= 2:
            return compute_statistics_summary(raw_nums)

    for shape in ["circle", "sphere", "rectangle", "triangle"]:
        if shape in q:
            nums = [float(x) for x in re.findall(r"-?\d+\.?\d*", q)]
            geo_res = compute_geometry_metrics(shape, nums)
            if geo_res:
                return geo_res

    return None

# ==============================================================================
# 7. OFFLINE PROCEDURAL VECTOR ART ENGINE
# ==============================================================================
def generate_offline_svg_art(prompt_text: str) -> str:
    """Generates procedural SVG artwork offline."""
    seed_val = sum(ord(ch) for ch in prompt_text)
    rng = random.Random(seed_val)
    palettes = [
        ("#0f172a", "#38bdf8", "#818cf8", "#f472b6"),
        ("#090d16", "#4ade80", "#22d3ee", "#facc15"),
        ("#1e1b4b", "#fb923c", "#f43f5e", "#a78bfa"),
    ]
    bg, c1, c2, c3 = palettes[seed_val % len(palettes)]
    circles = []
    for _ in range(14):
        cx = rng.randint(60, 740)
        cy = rng.randint(60, 440)
        r = rng.randint(25, 110)
        col = rng.choice([c1, c2, c3])
        op = round(rng.uniform(0.18, 0.55), 2)
        circles.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{col}" fill-opacity="{op}" />')
    safe_label = prompt_text[:45].replace("<", "").replace(">", "").replace("&", "")
    svg = f"""
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 500" width="100%" style="border-radius:14px; border:1px solid #4ade80;">
        <rect width="800" height="500" fill="{bg}" />
        {''.join(circles)}
        <rect x="40" y="390" width="720" height="75" rx="12" fill="rgba(15,23,42,0.82)" stroke="{c1}" stroke-width="1.5"/>
        <text x="60" y="423" fill="#ffffff" font-family="sans-serif" font-size="18" font-weight="bold">Indian GPT • Offline Procedural Art Engine</text>
        <text x="60" y="448" fill="{c1}" font-family="sans-serif" font-size="14">Prompt: {safe_label}</text>
    </svg>
    """
    return svg

# ==============================================================================
# 8. UNIFIED OFFLINE ANSWER SYNTHESIZER
# ==============================================================================
def answer_completely_offline(prompt_str: str, detected_script: str) -> str:
    """Generates authoritative answers using 100% local engines."""
    p_lower = prompt_str.lower().strip()

    if any(k in p_lower for k in ["time", "date", "ajke", "somoy", "tarikh", "today"]):
        ist = timezone(timedelta(hours=5, minutes=30))
        now_ist = datetime.now(ist)
        return (
            f"**Current Indian Standard Time (IST - Offline System Clock):**\n"
            f"• **Date:** {now_ist.strftime('%A, %B %d, %Y')}\n"
            f"• **Time:** {now_ist.strftime('%I:%M:%S %p')} IST"
        )

    math_result = solve_math_locally(prompt_str)
    if math_result:
        return f"🔌 *[Offline Sovereign Math Engine]*\n\n{math_result}"

    corpus_hits = retrieve_from_local_corpus(prompt_str, top_k=2)
    if corpus_hits:
        best_key, best_ans, best_score = corpus_hits[0]
        response_blocks = [f"🔌 *[Offline Sovereign Knowledge Base — Topic: {best_key.title()}]*\n\n{best_ans}"]
        if len(corpus_hits) > 1 and corpus_hits[1][2] >= 2.5:
            sec_key, sec_ans, _ = corpus_hits[1]
            response_blocks.append(f"**Related Context ({sec_key.title()}):**\n{sec_ans}")
        return "\n\n---\n\n".join(response_blocks)

    return (
        f"🔌 **[Offline Sovereign Mode Active]**\n\n"
        f"I am currently running **100% offline without internet** (Detected Script: *{detected_script}*). "
        f"My built-in offline corpus and math engines can immediately answer queries on Indian States, UTs, History, Science, Capitals, and Mathematics!"
    )

# ==============================================================================
# 9. GROQ CLOUD MODEL DISCOVERY
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
# 10. SESSION STATE INITIALIZATION
# ==============================================================================
if "chat_sessions_v110" not in st.session_state:
    st.session_state.chat_sessions_v110 = {
        "New Chat": [
            {
                "role": "assistant",
                "content": (
                    "Namaste! I am **Indian GPT**, a true **Hybrid Online + Offline Sovereign AI Ecosystem** "
                    "created exclusively by **Shubham**.\n\n"
                    "• **When Online:** I combine my built-in Sovereign Knowledge Base with Cloud LLMs, API keys, Live Web Search, and 1024×1024 FLUX HD Art.\n"
                    "• **When Offline (No Internet):** I automatically switch to 100% Offline Mode—answering Indian & World History, Geography, Science, Complex Math, and generating procedural vector art without needing any API key or internet!"
                )
            }
        ]
    }

if "current_chat_v110" not in st.session_state:
    st.session_state.current_chat_v110 = "New Chat"

# ==============================================================================
# 11. SIDEBAR CONTROLS (CLEANED OF UNNECESSARY STATS/BADGES)
# ==============================================================================
internet_available = check_internet_online()

with st.sidebar:
    st.markdown("### 🇮🇳 Indian GPT Control")

    operation_mode = st.radio(
        "⚡ Execution Mode",
        options=["Auto Hybrid", "100% Offline Mode"],
        index=0 if internet_available else 1
    )
    is_online_mode = (operation_mode.startswith("Auto Hybrid") and internet_available)

    st.markdown("")
    if st.button("➕ New Chat Session", use_container_width=True):
        new_chat_name = "New Chat"
        counter = 1
        while new_chat_name in st.session_state.chat_sessions_v110:
            new_chat_name = f"New Chat {counter}"
            counter += 1
        
        st.session_state.chat_sessions_v110[new_chat_name] = [
            {"role": "assistant", "content": "Namaste! New chat session started."}
        ]
        st.session_state.current_chat_v110 = new_chat_name
        st.rerun()

    st.markdown("---")
    st.subheader("💬 Chat History")
    
    for chat_name in list(st.session_state.chat_sessions_v110.keys()):
        if st.button(chat_name, use_container_width=True, key=f"btn_{chat_name}"):
            st.session_state.current_chat_v110 = chat_name
            st.rerun()

    st.markdown("---")
    st.subheader("📥 Export & Backup")
    current_msgs = st.session_state.chat_sessions_v110[st.session_state.current_chat_v110]
    
    chat_export_text = f"INDIAN GPT - TRANSCRIPT ({st.session_state.current_chat_v110})\n\n"
    for m in current_msgs:
        chat_export_text += f"[{m['role'].upper()}]: {m['content']}\n\n"
    
    st.download_button(
        label="📄 Export Transcript (TXT)",
        data=chat_export_text,
        file_name="indian_gpt_transcript.txt",
        mime="text/plain",
        use_container_width=True
    )
    
    st.markdown("---")
    st.caption("Created & Architected by **Shubham**")

# ==============================================================================
# 12. MAIN CONVERSATION VIEWPORT & HYBRID ROUTING PIPELINE
# ==============================================================================
st.title("🇮🇳 Indian GPT")
st.markdown("##### *Hybrid Online & 100% Offline Sovereign AI Ecosystem • Created by Shubham*")

if st.session_state.current_chat_v110 not in st.session_state.chat_sessions_v110:
    st.session_state.current_chat_v110 = list(st.session_state.chat_sessions_v110.keys())[0]

current_messages = st.session_state.chat_sessions_v110[st.session_state.current_chat_v110]

for message in current_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "image_bytes" in message and message["image_bytes"]:
            st.image(message["image_bytes"])
        if "svg_art" in message and message["svg_art"]:
            st.markdown(message["svg_art"], unsafe_allow_html=True)

# Chat input with placeholder set strictly to "Ask anything"
prompt = st.chat_input("Ask anything")

if prompt:
    if st.session_state.current_chat_v110.startswith("New Chat"):
        new_name = prompt[:28] + ("..." if len(prompt) > 28 else "")
        if new_name in st.session_state.chat_sessions_v110:
            new_name = f"{new_name} (2)"
        
        st.session_state.chat_sessions_v110[new_name] = st.session_state.chat_sessions_v110.pop(st.session_state.current_chat_v110)
        st.session_state.current_chat_v110 = new_name
        current_messages = st.session_state.chat_sessions_v110[new_name]

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
            
            image_starters = [
                "generate", "genarate", "draw", "create", "make",
                "chobi", "banao", "toiri", "pic", "photo", "image", "ghibli", "wallpaper"
            ]
            is_image_request = any(starter in p_lower for starter in image_starters)
            
            if is_image_request:
                if is_online_mode:
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
                        time.sleep(0.7)
                    
                    enhanced_prompt = f"{prompt}, highly detailed, professional photography, stunning composition, 8k resolution, photorealistic masterpiece"
                    encoded_prompt = urllib.parse.quote(enhanced_prompt)
                    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&model=flux&nologo=true"
                    
                    try:
                        img_resp = requests.get(image_url, timeout=35)
                        if img_resp.status_code == 200 and len(img_resp.content) > 1000:
                            generated_image_bytes = img_resp.content
                            full_response = "Here is your generated high-definition masterpiece:"
                        else:
                            generated_svg_art = generate_offline_svg_art(prompt)
                            full_response = "Cloud image server busy — generated via **Offline Procedural Vector Art Engine**:"
                    except Exception:
                        generated_svg_art = generate_offline_svg_art(prompt)
                        full_response = "Switched to **Offline Procedural Vector Art Engine**:"
                else:
                    generated_svg_art = generate_offline_svg_art(prompt)
                    full_response = "🔌 *[Offline Procedural Vector Art Engine]* — Generated locally with zero internet:"
                
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
                    greetings = ["hi", "hello", "hey", "hii", "hola", "sup", "good morning", "good evening", "bye", "namaste", "pranam", "nomoskar"]
                    is_simple_greeting = p_lower in greetings
                    
                    search_triggers = [
                        "winner", "jiteche", "won", "match", "score", "news",
                        "current", "ajke", "ekhon", "latest", "2026", "who won", "today", "weather", "price"
                    ]
                    needs_search = any(trigger in p_lower for trigger in search_triggers) and not is_simple_greeting
                    
                    local_hits = retrieve_from_local_corpus(prompt, top_k=2)
                    local_math_hint = solve_math_locally(prompt)
                    
                    local_knowledge_context = ""
                    if local_hits:
                        local_knowledge_context += "\n".join([f"- [{k.title()}]: {a}" for k, a, _ in local_hits])
                    if local_math_hint:
                        local_knowledge_context += f"\n- [Local Math Verification]: {local_math_hint}"

                    search_context = ""
                    if needs_search:
                        search_loading_html = """
                        <div style="display: flex; align-items: center; gap: 6px; font-style: italic; color: #a5b4fc;">
                            <span>🌐 combining local knowledge + live web search</span>
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
                            <span>🧠 hybrid reasoning (local corpus + cloud LLM)</span>
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
                        f"Detected User Input Script: {detected_script}. "
                        "You are Indian GPT, an advanced sovereign hybrid AI assistant created exclusively by Shubham. "
                        "If anyone asks who created, built, or owns you, always proudly state that you were created by Shubham. "
                        "HYBRID KNOWLEDGE & MULTI-LINGUAL DIRECTIVE: "
                        "1. You natively understand and reply fluently in ALL 22 scheduled Indian languages and scripts as well as English, Banglish, and Hinglish. "
                        "2. Always reply in the exact same language, script, and conversational register used by the user. "
                        "3. Integrate any verified facts provided below from Indian GPT's built-in Sovereign Knowledge Base with your own deep reasoning."
                    )
                    
                    if local_knowledge_context:
                        system_content += f"\n\nIndian GPT Built-in Sovereign Knowledge Base Context:\n{local_knowledge_context}"
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
