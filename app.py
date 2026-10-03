import re
from chatbot import get_bot_response
from github_store import sync_to_github
from models import load_json, save_json
import pandas as pd
import streamlit as st
from utils import normalize_phone, sanitize_csv_field
import urllib.parse
import json
import os

# --- 1. PAGE CONFIG ---
st.set_page_config(
    page_title="Sir Abdullah Academy | Premier CAIE Portal",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- 2. ULTRA-VIBRANT OBSIDIAN, NEON CRIMSON & STEEL THEME ---
st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    /* Hide Default Streamlit Chrome */
    #MainMenu, footer, header { visibility: hidden !important; }

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    /* Deep Obsidian & Vibrant Neon Crimson Ambient Background */
    .stApp {
        background: radial-gradient(circle at 50% -10%, #291118 0%, #0c0a09 60%, #030303 100%) !important;
        color: #f5f5f4 !important;
    }

    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 3rem !important;
        max-width: 1200px;
    }

    /* Professional Teacher "SA Academy" Shield Logo */
    .brand-logo-container {
        display: flex;
        align-items: center;
        gap: 16px;
    }

    .brand-shield {
        width: 52px;
        height: 52px;
        background: linear-gradient(135deg, #181214 0%, #0c0a09 100%);
        border: 2px solid #f43f5e;
        border-radius: 12px 18px 12px 18px;
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
        box-shadow: 0 0 25px rgba(244, 63, 94, 0.4), inset 0 2px 4px rgba(255, 255, 255, 0.15);
    }

    .brand-shield-inner {
        display: flex;
        align-items: baseline;
        justify-content: center;
        gap: 1px;
    }

    .brand-letter-s {
        font-size: 1.15rem;
        font-weight: 900;
        color: #ffffff;
        letter-spacing: -1px;
    }

    .brand-letter-a {
        font-size: 1.15rem;
        font-weight: 900;
        background: linear-gradient(135deg, #fb7185 0%, #f43f5e 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -1px;
    }

    .brand-shield-badge {
        position: absolute;
        bottom: -5px;
        right: -6px;
        background: #f43f5e;
        color: #ffffff;
        font-size: 0.55rem;
        font-weight: 800;
        padding: 1px 5px;
        border-radius: 4px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        box-shadow: 0 0 10px #f43f5e;
    }

    .brand-text-wrapper {
        display: flex;
        flex-direction: column;
        line-height: 1.1;
    }

    .brand-text {
        font-size: 1.25rem;
        font-weight: 800;
        background: linear-gradient(135deg, #ffffff 0%, #d6d3d1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.3px;
    }

    .brand-subtext {
        font-size: 0.65rem;
        font-weight: 800;
        letter-spacing: 2px;
        color: #fb7185;
        text-transform: uppercase;
    }

    /* Navigation & Global Buttons Override */
    div.stButton > button {
        border-radius: 12px !important;
        font-weight: 700 !important;
        font-size: 0.9rem !important;
        padding: 0.6rem 1.4rem !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        border: 1px solid transparent !important;
    }

    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #f43f5e 0%, #be123c 100%) !important;
        color: #ffffff !important;
        box-shadow: 0 0 20px rgba(244, 63, 94, 0.5) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
    }
    div.stButton > button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        background: linear-gradient(135deg, #fb7185 0%, #e11d48 100%) !important;
        box-shadow: 0 0 30px rgba(244, 63, 94, 0.8) !important;
    }

    div.stButton > button[kind="secondary"] {
        background: rgba(255, 255, 255, 0.06) !important;
        color: #ffffff !important;
        border: 1px solid rgba(244, 63, 94, 0.35) !important;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    div.stButton > button[kind="secondary"]:hover {
        background: rgba(244, 63, 94, 0.15) !important;
        border-color: #f43f5e !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 0 20px rgba(244, 63, 94, 0.4) !important;
    }

    div[data-testid="stColumn"] button[kind="tertiary"] {
        color: #d6d3d1 !important;
        font-weight: 600 !important;
        background: transparent !important;
    }
    div[data-testid="stColumn"] button[kind="tertiary"]:hover {
        color: #fb7185 !important;
        background: rgba(244, 63, 94, 0.08) !important;
    }

    /* Typography Headers */
    h1, h2, h3 {
        color: #ffffff !important;
        letter-spacing: -0.5px;
    }
    .vibrant-title {
        text-align: center;
        font-weight: 800;
        font-size: 2.6rem;
        background: linear-gradient(135deg, #ffffff 20%, #fb7185 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.4rem;
        text-shadow: 0 0 30px rgba(244, 63, 94, 0.3);
    }
    .vibrant-subtitle {
        text-align: center;
        color: #d6d3d1;
        font-size: 1.05rem;
        font-weight: 500;
        margin-bottom: 2rem;
    }

    /* Glass Cards */
    .glass-card {
        background: linear-gradient(135deg, rgba(30, 24, 27, 0.85) 0%, rgba(18, 15, 17, 0.95) 100%);
        border: 1px solid rgba(244, 63, 94, 0.25);
        border-radius: 18px;
        padding: 1.75rem;
        backdrop-filter: blur(16px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.1);
        transition: transform 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease;
    }
    .glass-card:hover {
        border-color: #f43f5e;
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.7), 0 0 25px rgba(244, 63, 94, 0.3);
        transform: translateY(-3px);
    }

    .course-card-img {
        width: 100%;
        height: 160px;
        object-fit: cover;
        border-radius: 12px;
        margin-bottom: 0.5rem;
        border: 1px solid rgba(244, 63, 94, 0.3);
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }

    .stat-box {
        background: linear-gradient(180deg, rgba(45, 20, 28, 0.6) 0%, rgba(20, 15, 17, 0.9) 100%);
        border: 1px solid rgba(244, 63, 94, 0.3);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.15);
    }

    .stat-value {
        font-size: 2.4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #ffffff 0%, #fb7185 50%, #f43f5e 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 20px rgba(244, 63, 94, 0.5);
    }

    .stat-lbl {
        font-size: 0.82rem;
        color: #d6d3d1;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-top: 0.3rem;
    }

    /* Badges */
    .badge-tag {
        display: inline-block;
        font-weight: 800;
        font-size: 0.72rem;
        padding: 0.35rem 0.8rem;
        border-radius: 8px;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }
    .badge-combo {
        background: rgba(244, 63, 94, 0.2);
        color: #fb7185;
        border: 1px solid rgba(244, 63, 94, 0.5);
        box-shadow: 0 0 12px rgba(244, 63, 94, 0.25);
    }
    .badge-standard {
        background: rgba(168, 162, 158, 0.2);
        color: #ffffff;
        border: 1px solid rgba(168, 162, 158, 0.4);
    }

    /* Admission Form Customization */
    div[data-testid="stForm"] {
        background: linear-gradient(135deg, rgba(28, 20, 24, 0.9) 0%, rgba(12, 10, 11, 0.95) 100%) !important;
        border: 1px solid rgba(244, 63, 94, 0.4) !important;
        border-radius: 20px !important;
        padding: 2.2rem !important;
        backdrop-filter: blur(16px) !important;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.7), 0 0 30px rgba(244, 63, 94, 0.15) !important;
    }

    div[data-testid="stForm"] label p {
        color: #fb7185 !important;
        font-weight: 700 !important;
        font-size: 0.92rem !important;
        letter-spacing: 0.3px !important;
        margin-bottom: 0.3px !important;
    }

    div[data-testid="stTextInput"] input, div[data-testid="stSelectbox"] div[role="combobox"] {
        background-color: rgba(10, 8, 9, 0.95) !important;
        color: #ffffff !important;
        border: 1px solid rgba(244, 63, 94, 0.3) !important;
        border-radius: 12px !important;
        padding: 0.75rem 1rem !important;
        font-size: 0.95rem !important;
    }

    div[data-testid="stTextInput"] input::placeholder {
        color: #78716c !important;
    }

    div[data-testid="stTextInput"] input:focus, div[data-testid="stSelectbox"] div[role="combobox"]:focus {
        border-color: #f43f5e !important;
        box-shadow: 0 0 15px rgba(244, 63, 94, 0.5) !important;
    }

    div[data-testid="stForm"] button[type="submit"] {
        background: linear-gradient(135deg, #f43f5e 0%, #be123c 100%) !important;
        color: #ffffff !important;
        font-weight: 800 !important;
        font-size: 1.05rem !important;
        padding: 0.8rem 2rem !important;
        border-radius: 12px !important;
        box-shadow: 0 0 25px rgba(244, 63, 94, 0.6) !important;
        margin-top: 1rem !important;
        width: 100% !important;
    }

    div[data-testid="stForm"] button[type="submit"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 0 35px rgba(244, 63, 94, 0.9) !important;
    }

    /* AI Chatbot Customizations */
    div[data-testid="stChatMessage"] {
        background: linear-gradient(135deg, rgba(28, 20, 24, 0.8) 0%, rgba(15, 12, 14, 0.9) 100%) !important;
        border: 1px solid rgba(244, 63, 94, 0.3) !important;
        border-radius: 16px !important;
        padding: 1.2rem 1.4rem !important;
        margin-bottom: 1rem !important;
        backdrop-filter: blur(12px) !important;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4) !important;
    }

    div[data-testid="stChatMessage"] div[data-testid="stMarkdownContainer"] p {
        color: #ffffff !important;
        font-size: 0.98rem !important;
        line-height: 1.6 !important;
        font-weight: 400 !important;
    }

    div[data-testid="stChatMessageAvatarUser"] {
        background: linear-gradient(135deg, #57534e 0%, #292524 100%) !important;
        border-radius: 10px !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }

    div[data-testid="stChatMessageAvatarAssistant"] {
        background: linear-gradient(135deg, #f43f5e 0%, #be123c 100%) !important;
        border-radius: 10px !important;
        color: #ffffff !important;
        box-shadow: 0 0 15px rgba(244, 63, 94, 0.7) !important;
    }

    div[data-testid="stChatInput"] {
        border-radius: 16px !important;
        border: 1px solid rgba(244, 63, 94, 0.5) !important;
        background-color: rgba(10, 8, 9, 0.95) !important;
        backdrop-filter: blur(16px) !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.7), 0 0 20px rgba(244, 63, 94, 0.2) !important;
    }

    div[data-testid="stChatInput"] textarea {
        color: #ffffff !important;
        font-size: 0.95rem !important;
    }

    div[data-testid="stChatInput"] textarea::placeholder {
        color: #78716c !important;
    }

    div[data-testid="stChatInput"] button {
        background: linear-gradient(135deg, #f43f5e 0%, #be123c 100%) !important;
        border-radius: 10px !important;
        color: white !important;
        box-shadow: 0 0 15px rgba(244, 63, 94, 0.5);
    }

    .chat-status-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(244, 63, 94, 0.18);
        color: #fb7185;
        font-size: 0.78rem;
        font-weight: 700;
        padding: 0.35rem 0.85rem;
        border-radius: 20px;
        border: 1px solid rgba(244, 63, 94, 0.4);
        margin-bottom: 1rem;
        box-shadow: 0 0 15px rgba(244, 63, 94, 0.2);
    }

    .pulse-dot {
        width: 8px;
        height: 8px;
        background-color: #fb7185;
        border-radius: 50%;
        box-shadow: 0 0 12px #fb7185;
    }
</style>
""",
    unsafe_allow_html=True,
)

# --- 3. CONFIG & DATA ---
ADMIN_PASSWORD = st.secrets.get("ADMIN_PASSWORD", "osmanibhai112233")

SPECIAL_COMBOS = [
    {
        "id": "combo_med",
        "title": "Pre-Medical Master Bundle",
        "badge": "Special Bundle",
        "fee": "PKR 16,000 / mo",
        "category": "Combos",
        "duration": "Online Live Classes",
        "image": "https://images.unsplash.com/photo-1532187863486-abf9dbad1b69?auto=format&fit=crop&w=800&q=80",
        "desc": "Complete 4-subject package for Biology, Physics, Chemistry, and Mathematics. Includes full syllabus coverage, topical solved past papers, and ATP practical preparation.",
        "highlights": [
            "Save PKR 4,000/mo",
            "Full 4-Subject Coverage",
            "Weekly Mocks & Past Papers",
        ],
    },
    {
        "id": "combo_cs",
        "title": "Pre-Engineering & CS Bundle",
        "badge": "Special Bundle",
        "fee": "PKR 16,000 / mo",
        "category": "Combos",
        "duration": "Online Live Classes",
        "image": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?auto=format&fit=crop&w=800&q=80",
        "desc": "Complete 4-subject package: Computer Science, Physics, Chemistry, and Math. Practice pseudocode, logic gates, and calculation strategies.",
        "highlights": [
            "Save PKR 4,000/mo",
            "Full CS & Engineering Prep",
            "Marking Scheme Drills",
        ],
    },
    {
        "id": "combo_core",
        "title": "O1 / O2 Core Subjects Combo",
        "badge": "Core Bundle",
        "fee": "PKR 4,500 / mo",
        "category": "Combos",
        "duration": "Online Live Classes",
        "image": "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?auto=format&fit=crop&w=800&q=80",
        "desc": "Dual-subject bundle for Islamiat (2058) and Pakistan Studies (2059). Complete Paper 1 & Paper 2 coverage with structured exam notes.",
        "highlights": [
            "Save PKR 500/mo",
            "Islamiat & PST Dual Prep",
            "Topical Past Paper Revision",
        ],
    },
]

O_LEVEL_COURSES = [
    {
        "id": "cs",
        "title": "O Level / IGCSE Computer Science",
        "badge": "CAIE 2210 / 0478",
        "fee": "PKR 5,000 / mo",
        "category": "Sciences",
        "duration": "Online Live Classes",
        "image": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=800&q=80",
        "desc": "Master Theory & Paper 2 Problem Solving. Practice pseudocode, algorithms, flowcharts, and hardware theory.",
        "highlights": [
            "10+ Yrs Past Papers",
            "Pseudocode Practice",
            "Paper 1 & 2 Focus",
        ],
    },
    {
        "id": "math",
        "title": "O Level / IGCSE Mathematics",
        "badge": "CAIE 4024 / 0580",
        "fee": "PKR 5,000 / mo",
        "category": "Sciences",
        "duration": "Online Live Classes",
        "image": "https://images.unsplash.com/photo-1509228468518-180dd4864904?auto=format&fit=crop&w=800&q=80",
        "desc": "Step-by-step conceptual clarity across Algebra, Trigonometry, Vectors, and Statistics with exam speed drills.",
        "highlights": [
            "Topical Worksheets",
            "Speed & Accuracy Drills",
            "Weekly Assessments",
        ],
    },
    {
        "id": "phy",
        "title": "O Level / IGCSE Physics",
        "badge": "CAIE 5054 / 0625",
        "fee": "PKR 5,000 / mo",
        "category": "Sciences",
        "duration": "Online Live Classes",
        "image": "https://images.unsplash.com/photo-1636466497217-26a8cbeaf0aa?auto=format&fit=crop&w=800&q=80",
        "desc": "In-depth Physics coverage: Mechanics, Electricity, Magnetism, Waves, Space Physics, and ATP Paper 4 techniques.",
        "highlights": ["Formula Sheets", "ATP Preparation", "MCQ Strategies"],
    },
    {
        "id": "chem",
        "title": "O Level / IGCSE Chemistry",
        "badge": "CAIE 5070 / 0620",
        "fee": "PKR 5,000 / mo",
        "category": "Sciences",
        "duration": "Online Live Classes",
        "image": "https://images.unsplash.com/photo-1532187863486-abf9dbad1b69?auto=format&fit=crop&w=800&q=80",
        "desc": "Build deep clarity in Stoichiometry, Organic Chemistry, Chemical Energetics, and Electrochemistry with ATP practice.",
        "highlights": [
            "Stoichiometry Drills",
            "Organic Chemistry Maps",
            "ATP Practical Prep",
        ],
    },
    {
        "id": "bio",
        "title": "O Level / IGCSE Biology",
        "badge": "CAIE 5090 / 0610",
        "fee": "PKR 5,000 / mo",
        "category": "Sciences",
        "duration": "Online Live Classes",
        "image": "https://images.unsplash.com/photo-1530026405186-ed1f139313f8?auto=format&fit=crop&w=800&q=80",
        "desc": "Cell Biology, Plant Physiology, Genetics, and Human Systems with exact examiner keywords to ensure full marks.",
        "highlights": [
            "Examiner Keyword Mastery",
            "Diagram Drills",
            "Past Paper Packs",
        ],
    },
    {
        "id": "isl",
        "title": "O Level / IGCSE Islamiat",
        "badge": "CAIE 2058 / 0493",
        "fee": "PKR 2,500 / mo",
        "category": "Humanities",
        "duration": "Online Live Classes",
        "image": "https://images.unsplash.com/photo-1584551246679-0daf3d275d0f?auto=format&fit=crop&w=800&q=80",
        "desc": "Structured preparation for Paper 1 & Paper 2: Quranic Passages, Seerah, Caliphates, and Hadith references with complete notes.",
        "highlights": [
            "Answer Outlines",
            "Quranic References",
            "Topical Answer Practice",
        ],
    },
    {
        "id": "pst",
        "title": "O Level / IGCSE Pakistan Studies",
        "badge": "CAIE 2059 / 0448",
        "fee": "PKR 2,500 / mo",
        "category": "Humanities",
        "duration": "Online Live Classes",
        "image": "https://images.unsplash.com/photo-1524492412937-b28074a5d7da?auto=format&fit=crop&w=800&q=80",
        "desc": "Complete history timelines & geography case studies with level-of-response answer templates and map skills.",
        "highlights": [
            "Chronological Timelines",
            "Map Skills",
            "Source-Based Questions",
        ],
    },
]


def is_valid_email(email: str) -> bool:
    return bool(re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email))


if "selected_course_for_enrollment" not in st.session_state:
    st.session_state.selected_course_for_enrollment = SPECIAL_COMBOS[0]["title"]

if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Home"

# --- 4. TOP NAVBAR (Simplified to 5 core professional tabs) ---
col_logo, col_nav, col_cta = st.columns([2.0, 3.5, 1.2])

with col_logo:
    st.markdown(
        """
    <div class="brand-logo-container">
        <div class="brand-shield">
            <div class="brand-shield-inner">
                <span class="brand-letter-s">S</span>
                <span class="brand-letter-a">A</span>
            </div>
            <div class="brand-shield-badge">EST</div>
        </div>
        <div class="brand-text-wrapper">
            <span class="brand-text">Sir Abdullah</span>
            <span class="brand-subtext">Academy</span>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

with col_nav:
    n1, n2, n3, n4, n5 = st.columns(5)
    with n1:
        if st.button("Home", key="nav_home", type="primary" if st.session_state.active_tab == "Home" else "tertiary"):
            st.session_state.active_tab = "Home"
            st.rerun()
    with n2:
        if st.button("Courses", key="nav_courses", type="primary" if st.session_state.active_tab == "Courses" else "tertiary"):
            st.session_state.active_tab = "Courses"
            st.rerun()
    with n3:
        if st.button("Admission", key="nav_admission", type="primary" if st.session_state.active_tab == "Admission" else "tertiary"):
            st.session_state.active_tab = "Admission"
            st.rerun()
    with n4:
        if st.button("AI Tutor", key="nav_ai", type="primary" if st.session_state.active_tab == "Assistant" else "tertiary"):
            st.session_state.active_tab = "Assistant"
            st.rerun()
    with n5:
        if st.button("Admin", key="nav_admin", type="primary" if st.session_state.active_tab == "Admin" else "tertiary"):
            st.session_state.active_tab = "Admin"
            st.rerun()

with col_cta:
    if st.button("Enroll Now 🚀", key="nav_enroll_btn", type="secondary", use_container_width=True):
        st.session_state.active_tab = "Admission"
        st.rerun()

st.markdown(
    "<hr style='border: none; border-bottom: 1px solid rgba(244,63,94,0.2); margin: 1.2rem 0 2rem 0;'>",
    unsafe_allow_html=True,
)

# --- 5. PAGE ROUTING ---

# PAGE: HOME
if st.session_state.active_tab == "Home":
    hero_left, hero_right = st.columns([1.3, 1])

    with hero_left:
        st.markdown(
            """
        <div style="display: inline-flex; align-items: center; gap: 8px; background: rgba(244, 63, 94, 0.15); color: #fb7185; font-size: 0.8rem; font-weight: 800; padding: 0.4rem 1rem; border-radius: 30px; border: 1px solid rgba(244, 63, 94, 0.4); box-shadow: 0 0 20px rgba(244, 63, 94, 0.25); margin-bottom: 1.2rem;">⚡ CAIE O & A LEVEL EXCELLENCE</div>
        <div style="font-size: 3.2rem; font-weight: 800; line-height: 1.15; letter-spacing: -1.2px; margin-bottom: 1.2rem; background: linear-gradient(135deg, #ffffff 20%, #fb7185 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-shadow: 0 0 30px rgba(244, 63, 94, 0.25);">Premier Online Academy for O & A Level</div>
        <div style="font-size: 1.05rem; color: #d6d3d1; line-height: 1.6; margin-bottom: 2rem;">
            Unlock academic distinction through interactive live sessions, topical past paper mastery, examiner keyword strategies, and targeted mentorship.
        </div>
        """,
            unsafe_allow_html=True,
        )

        cta1, cta2 = st.columns([1, 1])
        with cta1:
            if st.button("Explore Courses", key="hero_explore", type="primary", use_container_width=True):
                st.session_state.active_tab = "Courses"
                st.rerun()

        with cta2:
            if st.button("Apply Admission", key="hero_apply", type="secondary", use_container_width=True):
                st.session_state.active_tab = "Admission"
                st.rerun()

    with hero_right:
        st.markdown(
            """
        <div class="glass-card" style="padding: 1.2rem;">
            <img src="https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=800&q=80" style="width: 100%; height: 180px; object-fit: cover; border-radius: 12px; margin-bottom: 1.2rem; border: 1px solid rgba(244, 63, 94, 0.3); box-shadow: 0 0 20px rgba(244, 63, 94, 0.3);" alt="Academy Banner" />
            <div style="font-size: 0.75rem; font-weight: 800; color: #fb7185; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.5rem;">
                LIVE ACADEMY PORTAL
            </div>
            <h3 style="font-size: 1.3rem; font-weight: 800; color: #ffffff; margin-bottom: 0.8rem;">Interactive Live Classes</h3>
            <p style="font-size: 0.88rem; color: #d6d3d1; margin-bottom: 1.25rem; line-height: 1.5;">Direct interactive sessions with Sir Abdullah focusing on core concept building and past paper solving.</p>
            <div style="background: rgba(244, 63, 94, 0.1); padding: 0.85rem; border-radius: 10px; border: 1px solid rgba(244, 63, 94, 0.25); font-size: 0.85rem; color: #ffffff; margin-bottom: 0.6rem;">
                ✓ Interactive Whiteboard & Instant Doubt Resolution
            </div>
            <div style="background: rgba(244, 63, 94, 0.1); padding: 0.85rem; border-radius: 10px; border: 1px solid rgba(244, 63, 94, 0.25); font-size: 0.85rem; color: #ffffff;">
                ✓ 10+ Years Topical Solved Past Papers
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("<br><br>", unsafe_allow_html=True)

    s1, s2, s3 = st.columns(3)
    with s1:
        st.markdown(
            '<div class="stat-box"><div class="stat-value">10+ Yrs</div><div class="stat-lbl">Topical Past Paper Bank</div></div>',
            unsafe_allow_html=True,
        )
    with s2:
        st.markdown(
            '<div class="stat-box"><div class="stat-value">100%</div><div class="stat-lbl">Syllabus Coverage</div></div>',
            unsafe_allow_html=True,
        )
    with s3:
        st.markdown(
            '<div class="stat-box"><div class="stat-value">24/7</div><div class="stat-lbl">AI Learning Support</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown("<br><br>", unsafe_allow_html=True)

    f1, f2, f3, f4 = st.columns(4)
    features = [
        ("Live Interactive Classes", "Engage directly with expert faculty with immediate doubt resolution during live sessions."),
        ("Topical Past Papers", "10+ years of topical past paper practice fully aligned with CAIE marking schemes."),
        ("Keyword Mastery", "Learn exact subject-specific examiner keywords required for top grade boundaries."),
        ("Parent Tracking", "Regular attendance updates, test feedback, and personal student performance reports."),
    ]
    for col, (title, desc) in zip([f1, f2, f3, f4], features):
        with col:
            st.markdown(
                f"""
            <div class="glass-card" style="padding: 1.25rem; height: 100%;">
                <h4 style="font-weight: 800; color: #ffffff; margin-bottom: 0.5rem; font-size: 1rem;">{title}</h4>
                <p style="font-size: 0.82rem; color: #d6d3d1; line-height: 1.5; margin: 0;">{desc}</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

# PAGE: COURSES
elif st.session_state.active_tab == "Courses":
    st.markdown('<div class="vibrant-title">Explore Academic Courses</div>', unsafe_allow_html=True)
    st.markdown('<div class="vibrant-subtitle">Select an individual subject or discount combo package below.</div>', unsafe_allow_html=True)

    f_col1, f_col2 = st.columns([2.5, 1.2])
    with f_col1:
        cat_filter = st.radio(
            "Category Filter",
            ["All", "Combos", "Sciences", "Humanities"],
            horizontal=True,
            label_visibility="collapsed",
        )
    with f_col2:
        search_txt = st.text_input(
            "Search subject...",
            placeholder="Search subject or bundle...",
            label_visibility="collapsed",
        )

    combined_courses = []
    for c in SPECIAL_COMBOS:
        combined_courses.append({**c, "is_combo": True})
    for c in O_LEVEL_COURSES:
        combined_courses.append({**c, "is_combo": False})

    filtered = combined_courses
    if cat_filter != "All":
        filtered = [c for c in filtered if c["category"] == cat_filter]
    if search_txt:
        filtered = [
            c
            for c in filtered
            if search_txt.lower() in c["title"].lower() or search_txt.lower() in c["desc"].lower()
        ]

    st.markdown("<br>", unsafe_allow_html=True)

    for item in filtered:
        badge_class = "badge-combo" if item["is_combo"] else "badge-standard"

        with st.container():
            c_img, c_main, c_side = st.columns([1, 2.2, 1.1])

            with c_img:
                st.markdown(f'<img src="{item["image"]}" class="course-card-img" alt="{item["title"]}" />', unsafe_allow_html=True)

            with c_main:
                st.markdown(
                    f"""
                <span class="badge-tag {badge_class}">{item['badge']}</span>
                <h3 style="font-weight: 800; color: #ffffff; margin-top: 0.5rem; margin-bottom: 0.4rem; font-size: 1.25rem;">{item['title']}</h3>
                <p style="color: #d6d3d1; font-size: 0.88rem; line-height: 1.5; margin-bottom: 0.6rem;">{item['desc']}</p>
                <p style="color: #fb7185; font-size: 0.82rem; font-weight: 700; margin: 0;">Highlights: {' • '.join(item['highlights'])}</p>
                """,
                    unsafe_allow_html=True,
                )

            with c_side:
                st.markdown(
                    f"""
                <div style="text-align: right;">
                    <p style="color: #a8a29e; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; margin: 0;">Monthly Fee</p>
                    <div style="font-size: 1.4rem; font-weight: 800; color: #ffffff; text-shadow: 0 0 15px rgba(244,63,94,0.4);">{item['fee']}</div>
                    <p style="color: #d6d3d1; font-size: 0.78rem; margin-bottom: 0.8rem;">{item['duration']}</p>
                </div>
                """,
                    unsafe_allow_html=True,
                )

                if st.button("Apply For Course", key=f"btn_enroll_{item['id']}", type="primary", use_container_width=True):
                    st.session_state.selected_course_for_enrollment = item["title"]
                    st.session_state.active_tab = "Admission"
                    st.rerun()

                wa_msg = urllib.parse.quote(f"Hello Sir Abdullah Academy, I am interested in enrolling in {item['title']}. Please guide me.")
                st.markdown(
                    f'<a href="https://wa.me/923001234567?text={wa_msg}" target="_blank" style="display:block; text-align:center; margin-top:0.4rem; font-size:0.75rem; font-weight:700; color:#fb7185; text-decoration:none; border:1px solid rgba(244,63,94,0.3); border-radius:8px; padding:4px;">💬 Chat on WhatsApp</a>',
                    unsafe_allow_html=True
                )

        st.markdown("<hr style='border: none; border-bottom: 1px solid rgba(244,63,94,0.2); margin: 1.2rem 0;'>", unsafe_allow_html=True)

# PAGE: ADMISSION
elif st.session_state.active_tab == "Admission":
    st.markdown('<div class="vibrant-title">Online Admission Form</div>', unsafe_allow_html=True)
    st.markdown('<div class="vibrant-subtitle">Reserve your seat for the upcoming CAIE academic session.</div>', unsafe_allow_html=True)

    all_options = [c["title"] for c in SPECIAL_COMBOS] + [c["title"] for c in O_LEVEL_COURSES]
    default_idx = 0
    if st.session_state.selected_course_for_enrollment in all_options:
        default_idx = all_options.index(st.session_state.selected_course_for_enrollment)

    col_l, col_center, col_r = st.columns([0.15, 0.7, 0.15])

    with col_center:
        with st.form("vibrant_admission_form", clear_on_submit=False):
            st.markdown("### Student & Guardian Details")
            student_name = st.text_input("Full Student Name *", placeholder="e.g. Ali Khan")
            guardian_name = st.text_input("Parent / Guardian Name *", placeholder="e.g. Ahmed Khan")
            email = st.text_input("Email Address *", placeholder="student@example.com")
            phone = st.text_input("WhatsApp / Contact Number *", placeholder="e.g. 03001234567")
            
            selected_course = st.selectbox(
                "Select Course / Bundle *",
                options=all_options,
                index=default_idx
            )
            
            city = st.text_input("City / Location", placeholder="e.g. Karachi")
            notes = st.text_input("Additional Notes or Queries (Optional)", placeholder="Any specific requirements...")

            submit_btn = st.form_submit_button("Submit Application 🚀")

            if submit_btn:
                if not student_name or not guardian_name or not email or not phone:
                    st.error("Please fill in all required fields (*).")
                elif not is_valid_email(email):
                    st.error("Please enter a valid email address.")
                else:
                    normalized_ph = normalize_phone(phone)
                    admission_data = {
                        "student_name": sanitize_csv_field(student_name),
                        "guardian_name": sanitize_csv_field(guardian_name),
                        "email": sanitize_csv_field(email),
                        "phone": sanitize_csv_field(normalized_ph),
                        "course": sanitize_csv_field(selected_course),
                        "city": sanitize_csv_field(city),
                        "notes": sanitize_csv_field(notes),
                    }
                    
                    try:
                        if os.path.exists("admissions.json"):
                            with open("admissions.json", "r") as f:
                                existing_data = json.load(f)
                        else:
                            existing_data = []
                        existing_data.append(admission_data)
                        with open("admissions.json", "w") as f:
                            json.dump(existing_data, f, indent=4)
                        sync_to_github("admissions.json")
                    except Exception as e:
                        pass

                    st.success("🎉 Admission application submitted successfully! Sir Abdullah's team will contact you shortly via WhatsApp.")
                    st.balloons()

# PAGE: AI ASSISTANT / TUTOR
elif st.session_state.active_tab == "Assistant":
    st.markdown('<div class="vibrant-title">Sir Abdullah AI Tutor</div>', unsafe_allow_html=True)
    st.markdown('<div class="vibrant-subtitle">Ask questions about CAIE syllabi, past papers, concepts, or academy schedules 24/7.</div>', unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I am your AI academic tutor for Sir Abdullah Academy. How can I help you with your O & A Level preparation today?"}
        ]

    st.markdown('<div class="chat-status-badge"><div class="pulse-dot"></div> AI Tutor Online & Ready</div>', unsafe_allow_html=True)

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask a question about Math, Physics, Computer Science, Chemistry..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = get_bot_response(prompt, st.session_state.messages)
                st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

# PAGE: ADMIN PORTAL
elif st.session_state.active_tab == "Admin":
    st.markdown('<div class="vibrant-title">Admin Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="vibrant-subtitle">Manage student admissions and view application records.</div>', unsafe_allow_html=True)

    if "admin_logged_in" not in st.session_state:
        st.session_state.admin_logged_in = False

    if not st.session_state.admin_logged_in:
        col_l, col_c, col_r = st.columns([1, 1.5, 1])
        with col_c:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            pass_input = st.text_input("Enter Admin Password", type="password", placeholder="Enter password...")
            if st.button("Login to Admin", type="primary", use_container_width=True):
                if pass_input == ADMIN_PASSWORD:
                    st.session_state.admin_logged_in = True
                    st.rerun()
                else:
                    st.error("Incorrect password.")
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.success("🔓 Logged in as Administrator")
        if st.button("Log Out"):
            st.session_state.admin_logged_in = False
            st.rerun()

        st.markdown("### 📋 Submitted Student Applications")
        
        if os.path.exists("admissions.json"):
            with open("admissions.json", "r") as f:
                admissions = json.load(f)
        else:
            admissions = []
        
        if not admissions:
            st.info("No admission applications received yet.")
        else:
            df = pd.DataFrame(admissions)
            st.dataframe(df, use_container_width=True)
            
            csv_data = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Applications as CSV",
                data=csv_data,
                file_name="academy_admissions.csv",
                mime="text/csv",
                type="secondary"
            )
