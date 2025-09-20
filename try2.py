import streamlit as st
import os
import time
import numpy as np
import sounddevice as sd
import soundfile as sf

# Import all utility functions
from utils.llm_api import get_ai_response, BASE_SYSTEM_PROMPT
from utils.text_analysis import analyze_text
from utils.crisis_detection import check_crisis
from utils.data_storage import save_entry, plot_trends
from utils.voice_emotion import get_voice_emotion
from utils.face_emotion import analyze_video_stream
from utils.insights import analyze_journal_insights
from utils.goals import get_todays_goals, add_goal, update_goal_status, remove_goal
from utils.resources import RESOURCE_DATA
from utils.memory_vault import add_memory, get_random_memory, load_memories, remove_memory

# --- APP CONFIGURATION ---
st.set_page_config(
    page_title="MindSight - AI Wellness Companion",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- MODERN VIBRANT CSS FOR LIGHT MODE ---
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700;800;900&family=Open+Sans:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Open Sans', sans-serif;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Reduced padding and margins to eliminate white spaces */
    .main {
        padding: 0.5rem 1rem;
        max-width: 1400px;
        margin: 0 auto;
    }
    
    /* Beautiful gradient background with nature-inspired colors */
    .stApp {
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 30%, #bbf7d0 70%, #f0fdf4 100%);
        background-attachment: fixed;
        min-height: 100vh;
    }
    
    /* Reduced padding and margins for cleaner layout */
    .element-container {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 16px;
        padding: 1rem;
        margin-bottom: 0.5rem;
        box-shadow: 0 4px 20px rgba(21, 128, 61, 0.08);
        border: 1px solid rgba(21, 128, 61, 0.1);
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    .element-container:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 30px rgba(21, 128, 61, 0.15);
        border-color: rgba(132, 204, 22, 0.3);
    }
    
    /* Reduced header sizes and margins */
    h1 {
        font-family: 'Montserrat', sans-serif !important;
        color: #15803d !important;
        font-size: 2.2rem !important;
        font-weight: 900 !important;
        margin-bottom: 0.5rem !important;
        text-align: center;
        padding: 0.25rem 0;
        text-shadow: 0 2px 4px rgba(21,128,61,0.1);
    }
    
    h2 {
        font-family: 'Montserrat', sans-serif !important;
        color: #166534 !important;
        font-weight: 700 !important;
        font-size: 1.5rem !important;
        margin-top: 1rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    h3 {
        font-family: 'Montserrat', sans-serif !important;
        color: #15803d !important;
        font-weight: 600 !important;
        font-size: 1.2rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Vibrant sidebar with green theme */
    .css-1d391kg {
        background: linear-gradient(180deg, #f0fdf4 0%, #dcfce7 100%);
        border-right: 2px solid rgba(132, 204, 22, 0.2);
    }
    
    /* Enhanced dropdown/selectbox styling with better visual appeal */
    .stSelectbox > div > div {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(240, 253, 244, 0.9) 100%);
        border-radius: 16px;
        border: 2px solid rgba(132, 204, 22, 0.4);
        padding: 1rem;
        transition: all 0.3s ease;
        font-weight: 600;
        color: #15803d;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 15px rgba(21, 128, 61, 0.1);
        font-size: 1rem;
        font-family: 'Montserrat', sans-serif;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #84cc16;
        box-shadow: 0 6px 20px rgba(132, 204, 22, 0.25);
        transform: translateY(-2px);
        background: linear-gradient(135deg, rgba(255, 255, 255, 1) 0%, rgba(220, 252, 231, 0.95) 100%);
    }
    
    /* Enhanced dropdown options styling */
    .stSelectbox [data-baseweb="select"] {
        border-radius: 16px;
    }
    
    .stSelectbox [role="option"] {
        background: rgba(255, 255, 255, 0.95);
        color: #15803d;
        font-weight: 600;
        padding: 0.75rem 1rem;
        border-radius: 8px;
        margin: 0.25rem;
        transition: all 0.2s ease;
    }
    
    .stSelectbox [role="option"]:hover {
        background: linear-gradient(135deg, #15803d 0%, #84cc16 100%);
        color: white;
        transform: translateX(5px);
    }
    
    /* Vibrant button styling with green theme */
    .stButton > button {
        background: linear-gradient(135deg, #15803d 0%, #84cc16 100%);
        color: white !important;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 700;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 6px 20px rgba(21, 128, 61, 0.3);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-family: 'Montserrat', sans-serif;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(21, 128, 61, 0.4);
        background: linear-gradient(135deg, #166534 0%, #65a30d 100%);
    }
    
    /* Clean input styling */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: rgba(255, 255, 255, 0.95);
        border: 2px solid rgba(132, 204, 22, 0.3);
        border-radius: 12px;
        padding: 1rem;
        font-size: 1rem;
        transition: all 0.3s ease;
        font-family: 'Open Sans', sans-serif;
        color: #374151;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #84cc16;
        box-shadow: 0 0 0 3px rgba(132, 204, 22, 0.2);
    }
    
    /* Enhanced chat styling */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 16px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 15px rgba(21, 128, 61, 0.1);
        border-left: 4px solid #84cc16;
        color: #374151;
        backdrop-filter: blur(5px);
    }
    
    /* Vibrant alert styling */
    .stAlert {
        border-radius: 12px;
        padding: 1rem 1.25rem;
        border: none;
        box-shadow: 0 4px 15px rgba(21, 128, 61, 0.1);
        backdrop-filter: blur(5px);
    }
    
    /* Green progress bar */
    .stProgress > div > div {
        background: linear-gradient(135deg, #15803d 0%, #84cc16 100%);
        border-radius: 8px;
        height: 10px;
    }
    
    /* Reduced padding for metrics to save space */
    [data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 16px;
        padding: 1rem;
        box-shadow: 0 6px 20px rgba(21, 128, 61, 0.1);
        border-left: 4px solid #84cc16;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    [data-testid="metric-container"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(21, 128, 61, 0.15);
    }
    
    /* Vibrant tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.75rem;
        background: rgba(240, 253, 244, 0.8);
        border-radius: 16px;
        padding: 0.5rem;
        backdrop-filter: blur(5px);
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        background: rgba(255, 255, 255, 0.9);
        border: 2px solid transparent;
        transition: all 0.3s ease;
        font-weight: 600;
        color: #374151;
        font-family: 'Montserrat', sans-serif;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        border-color: #84cc16;
        transform: translateY(-1px);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #15803d 0%, #84cc16 100%);
        color: white !important;
        box-shadow: 0 4px 15px rgba(21, 128, 61, 0.3);
    }
    
    /* Clean checkbox styling */
    .stCheckbox {
        padding: 0.75rem;
        border-radius: 12px;
        transition: all 0.3s ease;
        background: rgba(240, 253, 244, 0.5);
        margin-bottom: 0.5rem;
        border: 1px solid rgba(132, 204, 22, 0.2);
    }
    
    .stCheckbox:hover {
        background: rgba(132, 204, 22, 0.1);
        border-color: rgba(132, 204, 22, 0.4);
    }
    
    .stCheckbox label {
        color: #374151 !important;
        font-weight: 500;
    }
    
    /* Green slider styling */
    .stSlider > div > div {
        background: linear-gradient(135deg, #15803d 0%, #84cc16 100%);
    }
    
    /* Smooth animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .element-container {
        animation: fadeInUp 0.4s ease-out;
    }
    
    /* Reduced padding for feature cards to save space */
    .feature-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 8px 25px rgba(21, 128, 61, 0.1);
        transition: all 0.4s ease;
        border: 2px solid rgba(132, 204, 22, 0.1);
        height: 100%;
        position: relative;
        backdrop-filter: blur(10px);
        overflow: hidden;
    }
    
    .feature-card:before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(135deg, #15803d 0%, #84cc16 100%);
        border-radius: 20px 20px 0 0;
    }
    
    .feature-card:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 12px 35px rgba(21, 128, 61, 0.2);
        border-color: #84cc16;
    }
    
    /* Ensure perfect text visibility */
    p, span, div {
        color: #374151 !important;
    }
    
    .css-1d391kg p, .css-1d391kg span, .css-1d391kg div {
        color: #374151 !important;
    }
    
    [data-testid="metric-container"] * {
        color: #374151 !important;
    }
    
    /* More compact layout with reduced spacing */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    
    [data-testid="column"] {
        padding: 0 0.25rem;
    }
    
    /* Remove divider lines for cleaner look */
    hr {
        display: none;
    }
    
    /* Remove extra spacing between sections */
    .stMarkdown {
        margin-bottom: 0.5rem;
    }
    
    /* Compact sidebar styling */
    .css-1d391kg .stSelectbox {
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# --- HELPER FUNCTIONS FOR VIBRANT UI ---
def create_metric_card(title, value, icon, gradient="linear-gradient(135deg, #15803d 0%, #84cc16 100%)", description=""):
    st.markdown(f"""
    <div style="background: rgba(255, 255, 255, 0.95); border-radius: 20px; padding: 2rem; box-shadow: 0 8px 25px rgba(21,128,61,0.1); border-left: 5px solid #84cc16; transition: all 0.4s ease; height: 100%; backdrop-filter: blur(10px);" onmouseover="this.style.transform='translateY(-5px) scale(1.02)'" onmouseout="this.style.transform='translateY(0) scale(1)'">
        <div style="display: flex; align-items: center; justify-content: space-between;">
            <div>
                <p style="color: #15803d; font-size: 0.9rem; margin: 0; font-weight: 600; font-family: 'Montserrat', sans-serif;">{title}</p>
                <p style="font-size: 2.5rem; font-weight: 900; color: #166534; margin: 0.5rem 0; font-family: 'Montserrat', sans-serif;">{value}</p>
                <p style="color: #84cc16; font-size: 0.8rem; margin: 0; font-weight: 500;">{description}</p>
            </div>
            <div style="font-size: 3rem; opacity: 0.8; filter: drop-shadow(0 2px 4px rgba(21,128,61,0.2));">{icon}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_welcome_header(title, subtitle, icon):
    st.markdown(f"""
    <div style="text-align: center; padding: 2rem 1.5rem; background: rgba(255, 255, 255, 0.95); border-radius: 25px; box-shadow: 0 10px 30px rgba(21,128,61,0.1); margin-bottom: 1rem; border: 2px solid rgba(132, 204, 22, 0.1); backdrop-filter: blur(15px); position: relative; overflow: hidden;">
        <div style="position: absolute; top: 0; left: 0; right: 0; height: 5px; background: linear-gradient(135deg, #15803d 0%, #84cc16 100%);"></div>
        <div style="font-size: 3rem; margin-bottom: 0.75rem; filter: drop-shadow(0 4px 8px rgba(21,128,61,0.2));">{icon}</div>
        <h1 style="margin: 0; font-size: 2.2rem; color: #15803d; font-family: 'Montserrat', sans-serif; font-weight: 900;">{title}</h1>
        <p style="color: #166534; font-size: 1.1rem; margin-top: 0.75rem; font-weight: 500; font-family: 'Open Sans', sans-serif;">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)

def create_feature_card(title, description, icon, action_text="Explore"):
    return f"""
    <div class="feature-card">
        <div style="font-size: 3.5rem; margin-bottom: 1.5rem; filter: drop-shadow(0 4px 8px rgba(21,128,61,0.2));">{icon}</div>
        <h3 style="color: #15803d; margin-bottom: 1rem; font-family: 'Montserrat', sans-serif; font-weight: 700; font-size: 1.4rem;">{title}</h3>
        <p style="color: #374151; line-height: 1.6; margin-bottom: 1.5rem; font-size: 1rem; font-weight: 400;">{description}</p>
        <div style="background: linear-gradient(135deg, #15803d 0%, #84cc16 100%); color: white; padding: 0.75rem 1.5rem; border-radius: 25px; display: inline-block; font-size: 0.9rem; font-weight: 700; font-family: 'Montserrat', sans-serif; box-shadow: 0 4px 15px rgba(21,128,61,0.3); transition: all 0.3s ease;" onmouseover="this.style.transform='translateY(-2px)'" onmouseout="this.style.transform='translateY(0)'">{action_text}</div>
    </div>
    """

# --- NAVIGATION ---
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1.5rem 1rem; background: rgba(255, 255, 255, 0.95); border-radius: 20px; margin-bottom: 1rem; border: 2px solid rgba(132, 204, 22, 0.2); backdrop-filter: blur(10px); box-shadow: 0 6px 20px rgba(21,128,61,0.1);">
        <div style="font-size: 2.5rem; margin-bottom: 0.75rem; filter: drop-shadow(0 4px 8px rgba(21,128,61,0.2));">🧠</div>
        <h2 style="margin: 0.25rem 0; color: #15803d; font-family: 'Montserrat', sans-serif; font-weight: 900; font-size: 1.5rem;">MindSight</h2>
        <p style="color: #166534; font-size: 0.85rem; margin: 0; font-weight: 600;">Your AI Wellness Companion</p>
        <div style="margin-top: 0.75rem; display: flex; align-items: center; justify-content: center;">
            <span style="display: inline-block; width: 8px; height: 8px; background: #84cc16; border-radius: 50%; margin-right: 0.5rem; box-shadow: 0 0 10px rgba(132, 204, 22, 0.5);"></span>
            <span style="color: #15803d; font-size: 0.75rem; font-weight: 600;">Online & Ready</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    feature_options = {
        "🏠 Dashboard": "🏠 Dashboard - Overview & Quick Stats",
        "💬 AI Companion": "💬 AI Companion - Chat & Support", 
        "📝 Journal Analysis": "📝 Journal Analysis - Write & Analyze",
        "💡 My Insights": "💡 My Insights - Personal Patterns",
        "🎯 Daily Goals": "🎯 Daily Goals - Track Progress",
        "✨ Memory Vault": "✨ Memory Vault - Happy Moments",
        "📚 Resource Hub": "📚 Resource Hub - Wellness Resources",
        "🧘 Guided Exercises": "🧘 Guided Exercises - Mindfulness",
        "🎤 Voice Emotion": "🎤 Voice Emotion - Voice Analysis",
        "🎥 Facial Emotion": "🎥 Facial Emotion - Face Analysis"
    }
    
    if "app_mode" not in st.session_state:
        st.session_state.app_mode = "🏠 Dashboard"
    
    app_mode = st.selectbox(
        "🎯 Choose Your Wellness Feature",
        list(feature_options.keys()),
        index=list(feature_options.keys()).index(st.session_state.app_mode) if st.session_state.app_mode in feature_options else 0,
        format_func=lambda x: feature_options[x],
        help="Select a feature to explore your mental wellness journey",
        key="sidebar_selectbox"
    )
    
    if app_mode != st.session_state.app_mode:
        st.session_state.app_mode = app_mode
        st.rerun()
    
    # Enhanced stats in sidebar with reduced spacing
    st.markdown("### 📊 Quick Stats")
    goals = get_todays_goals()
    completed = sum(1 for g in goals if g["completed"])
    memories = load_memories()
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Goals", f"{completed}/{len(goals)}", delta=f"{completed} done")
    with col2:
        st.metric("Memories", len(memories), delta="Growing")

# --- DASHBOARD ---
if "🏠" in st.session_state.app_mode:
    create_welcome_header("Welcome to MindSight", "Your personalized mental wellness journey starts here", "🌟")
    
    # Enhanced stats row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        create_metric_card("Daily Streak", "7 days", "🔥", description="Keep it up!")
    with col2:
        create_metric_card("Mood Today", "Great", "😊", description="Feeling positive")
    with col3:
        goals = get_todays_goals()
        completed = sum(1 for g in goals if g["completed"])
        create_metric_card("Goals", f"{completed}/{len(goals)}", "🎯", description="On track")
    with col4:
        memories = load_memories()
        create_metric_card("Memories", str(len(memories)), "✨", description="Precious moments")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Feature showcase
    st.markdown("### 🚀 Quick Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="feature-card">
            <div style="font-size: 3.5rem; margin-bottom: 1.5rem; filter: drop-shadow(0 4px 8px rgba(21,128,61,0.2));">💬</div>
            <h3 style="color: #15803d; margin-bottom: 1rem; font-family: 'Montserrat', sans-serif; font-weight: 700; font-size: 1.4rem;">AI Companion</h3>
            <p style="color: #374151; line-height: 1.6; margin-bottom: 1.5rem; font-size: 1rem; font-weight: 400;">Chat with your personal AI wellness companion for support and guidance</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("💬 Start Chat", key="chat_btn", use_container_width=True):
            st.session_state.app_mode = "💬 AI Companion"
            st.rerun()
    
    with col2:
        st.markdown(f"""
        <div class="feature-card">
            <div style="font-size: 3.5rem; margin-bottom: 1.5rem; filter: drop-shadow(0 4px 8px rgba(21,128,61,0.2));">📝</div>
            <h3 style="color: #15803d; margin-bottom: 1rem; font-family: 'Montserrat', sans-serif; font-weight: 700; font-size: 1.4rem;">Journal Entry</h3>
            <p style="color: #374151; line-height: 1.6; margin-bottom: 1.5rem; font-size: 1rem; font-weight: 400;">Write and analyze your daily thoughts with AI-powered sentiment analysis</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("📝 Write Entry", key="journal_btn", use_container_width=True):
            st.session_state.app_mode = "📝 Journal Analysis"
            st.rerun()
    
    with col3:
        st.markdown(f"""
        <div class="feature-card">
            <div style="font-size: 3.5rem; margin-bottom: 1.5rem; filter: drop-shadow(0 4px 8px rgba(21,128,61,0.2));">🧘</div>
            <h3 style="color: #15803d; margin-bottom: 1rem; font-family: 'Montserrat', sans-serif; font-weight: 700; font-size: 1.4rem;">Mindfulness</h3>
            <p style="color: #374151; line-height: 1.6; margin-bottom: 1.5rem; font-size: 1rem; font-weight: 400;">Practice guided breathing exercises and meditation techniques</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🧘 Start Session", key="mindfulness_btn", use_container_width=True):
            st.session_state.app_mode = "🧘 Guided Exercises"
            st.rerun()

    # Memory of the day with reduced spacing
    random_memory = get_random_memory()
    if random_memory:
        st.markdown("### 💭 Memory of the Day")
        st.markdown(f"""
        <div style="background: rgba(255, 255, 255, 0.95); border-radius: 20px; padding: 1.5rem; box-shadow: 0 8px 25px rgba(21,128,61,0.1); border-left: 5px solid #84cc16; backdrop-filter: blur(10px);">
            <div style="display: flex; align-items: center; margin-bottom: 0.75rem;">
                <span style="font-size: 1.5rem; margin-right: 0.75rem; filter: drop-shadow(0 2px 4px rgba(21,128,61,0.2));">✨</span>
                <h3 style="margin: 0; color: #15803d; font-family: 'Montserrat', sans-serif; font-weight: 700;">A Beautiful Memory</h3>
            </div>
            <p style="font-style: italic; color: #374151; font-size: 1rem; line-height: 1.6; margin: 0; font-weight: 400;">"{random_memory}"</p>
        </div>
        """, unsafe_allow_html=True)

# --- AI COMPANION CHATBOT ---
elif "💬" in st.session_state.app_mode:
    create_welcome_header("AI Wellness Companion", "I'm here to listen and support you", "💬")

    random_memory = get_random_memory()
    if random_memory:
        st.markdown(f"""
        <div style="background: rgba(255, 255, 255, 0.95); border-radius: 16px; padding: 1.5rem; margin-bottom: 2rem; box-shadow: 0 6px 20px rgba(21,128,61,0.1); border-left: 4px solid #84cc16; backdrop-filter: blur(10px);">
            <div style="display: flex; align-items: center; margin-bottom: 0.75rem;">
                <span style="font-size: 1.5rem; margin-right: 0.75rem; filter: drop-shadow(0 2px 4px rgba(21,128,61,0.2));">✨</span>
                <strong style="color: #15803d; font-family: 'Montserrat', sans-serif;">Remember this happy moment?</strong>
            </div>
            <p style="font-style: italic; color: #374151; margin: 0; font-size: 1rem;">"{random_memory}"</p>
        </div>
        """, unsafe_allow_html=True)

    if "messages" not in st.session_state:
            insights = analyze_journal_insights()
            proactive_insight = None
            if insights and "error" not in insights and "message" not in insights:
                # You correctly define the variable here
                first_insight_key = next(iter(insights))
                
                # FIX: Use the correct variable name on this line
                first_insight_text = insights[first_insight_key]
                
                proactive_insight = f"Insight about the user: {first_insight_text}"

            system_prompt = BASE_SYSTEM_PROMPT
            welcome_message = "Hello! I'm MindSight. How are you feeling today?"

            if proactive_insight:
                system_prompt += f"\n\nCONTEXT FOR THIS CONVERSATION:\n- {proactive_insight}\n- Gently and naturally bring this insight up early in the conversation."
                welcome_message = "Hello! I was just reflecting on your recent journal entries and noticed something. How are you doing today?"

            st.session_state.messages = [
                {"role": "system", "content": system_prompt},
                {"role": "assistant", "content": welcome_message}
            ]

    # Enhanced chat container
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("What's on your mind?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = get_ai_response(st.session_state.messages)
                st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})

elif "📝" in st.session_state.app_mode:
    create_welcome_header("Journal Analysis", "Express yourself and track your emotional journey", "📝")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### ✍️ Write Your Entry")
        journal_entry = st.text_area(
            "How are you feeling today?", 
            height=250, 
            placeholder="Today I felt... I experienced... I'm grateful for..."
        )
        
        if st.button("🔍 Analyze Entry", use_container_width=True) and journal_entry.strip():
            with st.spinner("Analyzing your entry..."):
                simple_label, numeric_rating = analyze_text(journal_entry)
                
                # Results display
                col_a, col_b = st.columns(2)
                with col_a:
                    color = "#84cc16" if simple_label == "Positive" else "#be123c" if simple_label == "Negative" else "#f97316"
                    st.markdown(f"""
                    <div style="background: {color}; color: white; padding: 1.5rem; border-radius: 16px; text-align: center; box-shadow: 0 6px 20px rgba(21,128,61,0.2);">
                        <h3 style="margin: 0; color: white; font-family: 'Montserrat', sans-serif;">Sentiment: {simple_label}</h3>
                    </div>
                    """, unsafe_allow_html=True)
                with col_b:
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #15803d 0%, #84cc16 100%); color: white; padding: 1.5rem; border-radius: 16px; text-align: center; box-shadow: 0 6px 20px rgba(21,128,61,0.2);">
                        <h3 style="margin: 0; color: white; font-family: 'Montserrat', sans-serif;">Score: {numeric_rating}/10</h3>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Crisis detection
                crisis, helplines = check_crisis(journal_entry)
                if crisis:
                    st.error("⚠️ **Crisis detected!** Please consider reaching out for help:")
                    for k, v in helplines.items():
                        st.write(f"**{k}:** {v}")
                
                # Save and plot
                log = save_entry(journal_entry, numeric_rating)
                st.plotly_chart(plot_trends(log), use_container_width=True)
    
    with col2:
        st.markdown("""
        <div style="background: rgba(255, 255, 255, 0.95); border-radius: 20px; padding: 2rem; box-shadow: 0 8px 25px rgba(21,128,61,0.1); height: fit-content; backdrop-filter: blur(10px);">
            <h3 style="color: #15803d; font-size: 1.3rem; margin-bottom: 1.5rem; font-family: 'Montserrat', sans-serif; font-weight: 700;">💡 Journaling Tips</h3>
            <ul style="color: #374151; line-height: 1.8; font-weight: 500;">
                <li>Be honest with yourself</li>
                <li>Focus on feelings, not just events</li>
                <li>Write without judgment</li>
                <li>Include gratitude when possible</li>
                <li>Notice patterns over time</li>
            </ul>
            <div style="margin-top: 2rem; padding: 1.5rem; background: rgba(132, 204, 22, 0.1); border-radius: 12px; border-left: 4px solid #84cc16;">
                <p style="color: #15803d; font-weight: 600; margin: 0; font-size: 0.9rem; font-style: italic;">"The act of writing is the act of discovering what you believe." - David Hare</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

elif "💡" in st.session_state.app_mode:
    create_welcome_header("Your Personalized Insights", "Discover patterns in your emotional wellness", "💡")
    
    insights = analyze_journal_insights()
    if "error" in insights or "message" in insights:
        st.warning(insights.get("error") or insights.get("message"))
    else:
        colors = ["#15803d", "#84cc16", "#a3e635", "#d9f99d", "#f0fdf4"]
        icons = ["🎯", "💪", "🌟", "🎨", "🚀"]
        
        cols = st.columns(min(len(insights), 3))
        for i, (category, finding) in enumerate(insights.items()):
            with cols[i % len(cols)]:
                st.markdown(f"""
                <div style="background: rgba(255, 255, 255, 0.95); border-radius: 20px; padding: 2rem; box-shadow: 0 8px 25px rgba(21,128,61,0.1); border-top: 5px solid {colors[i % len(colors)]}; height: 100%; transition: all 0.4s ease; backdrop-filter: blur(10px);" onmouseover="this.style.transform='translateY(-5px) scale(1.02)'" onmouseout="this.style.transform='translateY(0) scale(1)'">
                    <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                        <span style="font-size: 2rem; margin-right: 1rem; filter: drop-shadow(0 2px 4px rgba(21,128,61,0.2));">{icons[i % len(icons)]}</span>
                        <h3 style="color: #15803d; margin: 0; font-size: 1.2rem; font-family: 'Montserrat', sans-serif; font-weight: 700;">{category} Activities</h3>
                    </div>
                    <p style="color: #374151; line-height: 1.6; margin: 0; font-weight: 400;">{finding}</p>
                </div>
                """, unsafe_allow_html=True)

elif "🎯" in st.session_state.app_mode:
    create_welcome_header("Daily Goals & Habits", "Small steps lead to big changes", "🎯")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### ➕ Add New Goal")
        new_goal = st.text_input(
            "What would you like to accomplish today?", 
            placeholder="e.g., Take a 15-minute walk, Call a friend, Read for 20 minutes"
        )
        if st.button("🎯 Add Goal", use_container_width=True) and new_goal:
            add_goal(new_goal)
            st.success("Goal added successfully!")
            st.rerun()

        st.markdown("### 📋 Today's Goals")
        todays_goals = get_todays_goals()
        if not todays_goals:
            st.markdown("""
            <div style="background: rgba(255, 255, 255, 0.95); border-radius: 20px; padding: 2.5rem; text-align: center; box-shadow: 0 8px 25px rgba(21,128,61,0.1); backdrop-filter: blur(10px);">
                <div style="font-size: 3rem; margin-bottom: 1rem; filter: drop-shadow(0 4px 8px rgba(21,128,61,0.2));">🎯</div>
                <h3 style="color: #15803d; font-family: 'Montserrat', sans-serif; font-weight: 700;">No goals set for today</h3>
                <p style="color: #374151; font-weight: 500;">Add your first goal above to get started!</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            for i, goal in enumerate(todays_goals):
                col_a, col_b = st.columns([0.9, 0.1])
                with col_a:
                    is_completed = st.checkbox(
                        goal["text"], 
                        value=goal["completed"], 
                        key=f"goal_{i}"
                    )
                    if is_completed != goal["completed"]:
                        update_goal_status(i, is_completed)
                        st.rerun()
                with col_b:
                    if st.button("❌", key=f"remove_goal_{i}"):
                        remove_goal(i)
                        st.rerun()
    
    with col2:
        completed = sum(1 for g in todays_goals if g["completed"])
        total = len(todays_goals)
        percentage = (completed / total * 100) if total > 0 else 0
        
        st.markdown(f"""
        <div style="background: rgba(255, 255, 255, 0.95); border-radius: 20px; padding: 2rem; text-align: center; box-shadow: 0 8px 25px rgba(21,128,61,0.1); backdrop-filter: blur(10px);">
            <h3 style="color: #15803d; font-family: 'Montserrat', sans-serif; font-weight: 700;">Progress Today</h3>
            <div style="font-size: 3rem; color: #84cc16; font-weight: 900; margin: 0.75rem 0; filter: drop-shadow(0 4px 8px rgba(21,128,61,0.2));">{percentage:.0f}%</div>
            <p style="color: #374151; font-weight: 500;">{completed} of {total} completed</p>
            <div style="background: rgba(132, 204, 22, 0.1); border-radius: 12px; height: 12px; margin: 1rem 0;">
                <div style="background: linear-gradient(135deg, #15803d 0%, #84cc16 100%); height: 100%; border-radius: 12px; width: {percentage}%; transition: width 0.4s ease;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if completed > 0:
            st.balloons()

elif "✨" in st.session_state.app_mode:
    create_welcome_header("Positive Memory Vault", "Collect moments that make you smile", "✨")
    
    st.markdown("### 💾 Add New Memory")
    new_memory = st.text_area(
        "Share a positive memory:", 
        height=120, 
        placeholder="Something that made you happy, proud, or grateful..."
    )
    if st.button("✨ Save Memory", use_container_width=True) and new_memory:
        add_memory(new_memory)
        st.success("✨ Memory saved to your vault!")
        st.balloons()
        st.rerun()

    st.markdown("### 📚 Your Memory Collection")
    all_memories = load_memories()
    if not all_memories:
        st.markdown("""
        <div style="background: rgba(255, 255, 255, 0.95); border-radius: 20px; padding: 2.5rem; text-align: center; box-shadow: 0 8px 25px rgba(21,128,61,0.1); backdrop-filter: blur(10px);">
            <div style="font-size: 3rem; margin-bottom: 1rem; filter: drop-shadow(0 4px 8px rgba(21,128,61,0.2));">✨</div>
            <h3 style="color: #15803d; font-family: 'Montserrat', sans-serif; font-weight: 700;">Your vault is empty</h3>
            <p style="color: #374151; font-weight: 500;">Start collecting happy memories above!</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        for i, mem in enumerate(reversed(all_memories)):
            col1, col2 = st.columns([0.95, 0.05])
            with col1:
                st.markdown(f"""
                <div style="background: rgba(255, 255, 255, 0.95); border-radius: 16px; padding: 1.5rem; margin-bottom: 1rem; box-shadow: 0 6px 20px rgba(21,128,61,0.1); border-left: 4px solid #84cc16; transition: all 0.4s ease; backdrop-filter: blur(10px);" onmouseover="this.style.transform='translateX(5px)'" onmouseout="this.style.transform='translateX(0)'">
                    <div style="display: flex; align-items: flex-start;">
                        <span style="font-size: 1.5rem; margin-right: 1rem; margin-top: 0.2rem; filter: drop-shadow(0 2px 4px rgba(21,128,61,0.2));">💭</span>
                        <p style="color: #374151; margin: 0; font-style: italic; line-height: 1.6; font-weight: 400;">"{mem}"</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                if st.button("❌", key=f"remove_mem_{i}"):
                    remove_memory(mem)
                    st.rerun()

elif "📚" in st.session_state.app_mode:
    create_welcome_header("Mental Wellness Resources", "Curated content for your wellbeing", "📚")
    
    tabs = st.tabs(list(RESOURCE_DATA.keys()))
    for tab, (category, resources) in zip(tabs, RESOURCE_DATA.items()):
        with tab:
            cols = st.columns(2)
            for idx, resource in enumerate(resources):
                with cols[idx % 2]:
                    st.markdown(f"""
                    <div style="background: rgba(255, 255, 255, 0.95); border-radius: 20px; padding: 2rem; margin-bottom: 1rem; box-shadow: 0 8px 25px rgba(21,128,61,0.1); height: 100%; transition: all 0.4s ease; backdrop-filter: blur(10px);" onmouseover="this.style.transform='translateY(-5px) scale(1.02)'" onmouseout="this.style.transform='translateY(0) scale(1)'">
                        <h4 style="color: #15803d; margin-bottom: 1rem; font-family: 'Montserrat', sans-serif; font-weight: 700;">
                            <a href="{resource['url']}" style="text-decoration: none; color: #15803d; display: flex; align-items: center;" target="_blank">
                                {resource['title']} 
                                <span style="margin-left: 0.5rem; font-size: 1rem; filter: drop-shadow(0 2px 4px rgba(21,128,61,0.2));">🔗</span>
                            </a>
                        </h4>
                        <p style="color: #374151; line-height: 1.6; margin: 0; font-weight: 400;">{resource['desc']}</p>
                    </div>
                    """, unsafe_allow_html=True)

elif "🧘" in st.session_state.app_mode:
    create_welcome_header("Mindfulness Exercises", "Take a moment to center yourself", "🧘")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 🫁 Box Breathing Exercise")
        st.markdown("This 4-4-4-4 breathing technique helps calm your nervous system and reduce stress.")
        
        if st.button("▶️ Start Breathing Exercise", use_container_width=True):
            progress_bar = st.progress(0.0)
            status_text = st.empty()
            total_steps = 64  # 4 cycles × 4 phases × 4 seconds
            step_counter = 0
            
            for cycle in range(4):
                # Breathe In
                status_text.markdown("### 🫁 Breathe In...")
                for _ in range(4):
                    time.sleep(1)
                    step_counter += 1
                    progress_bar.progress(step_counter / total_steps)
                
                # Hold
                status_text.markdown("### ⏸️ Hold...")
                for _ in range(4):
                    time.sleep(1)
                    step_counter += 1
                    progress_bar.progress(step_counter / total_steps)
                
                # Breathe Out
                status_text.markdown("### 💨 Breathe Out...")
                for _ in range(4):
                    time.sleep(1)
                    step_counter += 1
                    progress_bar.progress(step_counter / total_steps)
                
                # Hold
                status_text.markdown("### ⏸️ Hold...")
                for _ in range(4):
                    time.sleep(1)
                    step_counter += 1
                    progress_bar.progress(step_counter / total_steps)
            
            progress_bar.progress(1.0)
            status_text.success("✨ Exercise complete! Well done!")
            st.balloons()
    
    with col2:
        st.markdown("""
        <div style="background: rgba(255, 255, 255, 0.95); border-radius: 20px; padding: 2rem; box-shadow: 0 8px 25px rgba(21,128,61,0.1); backdrop-filter: blur(10px);">
            <h3 style="color: #15803d; font-family: 'Montserrat', sans-serif; font-weight: 700;">How it works:</h3>
            <ol style="color: #374151; line-height: 1.8; font-weight: 500;">
                <li>Breathe in for 4 seconds</li>
                <li>Hold for 4 seconds</li>
                <li>Breathe out for 4 seconds</li>
                <li>Hold for 4 seconds</li>
                <li>Repeat 4 times</li>
            </ol>
            <div style="margin-top: 2rem; padding: 1.5rem; background: rgba(132, 204, 22, 0.1); border-radius: 12px; border-left: 4px solid #84cc16;">
                <p style="color: #15803d; font-weight: 600; margin: 0; font-size: 0.9rem; font-style: italic;">💡 Focus on the rhythm and let your mind settle with each breath.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

elif "🎤" in st.session_state.app_mode:
    create_welcome_header("Voice Emotion Analysis", "Understand your emotions through voice", "🎤")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 🎙️ Record Your Voice")
        duration = st.slider("Recording duration (seconds):", 5, 60, 15)
        
        if st.button("🎤 Start Recording", use_container_width=True):
            fs = 16000
            with st.spinner(f"Recording for {duration} seconds... Speak now!"):
                audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
                sd.wait()
            
            st.success("Recording complete! Analyzing...")
            temp_audio_file = "temp_audio.wav"
            sf.write(temp_audio_file, audio, fs)
            
            with st.spinner("Analyzing your voice..."):
                label, confidence = get_voice_emotion(temp_audio_file)
            
            # Display results
            emotion_colors = {
                "happy": "#84cc16",
                "sad": "#be123c", 
                "angry": "#be123c",
                "neutral": "#4b5563",
                "excited": "#f97316"
            }
            color = emotion_colors.get(label.lower(), "#6b7280")
            
            st.markdown(f"""
            <div style="background: {color}; color: white; padding: 1.5rem; border-radius: 16px; text-align: center; margin: 1rem 0; box-shadow: 0 6px 20px rgba(21,128,61,0.2);">
                <h3 style="margin: 0; color: white; font-family: 'Montserrat', sans-serif;">Detected Emotion: {label}</h3>
                <p style="margin: 0.5rem 0 0 0; color: white;">Confidence: {confidence:.1f}%</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: rgba(255, 255, 255, 0.95); border-radius: 20px; padding: 2rem; box-shadow: 0 8px 25px rgba(21,128,61,0.1); backdrop-filter: blur(10px);">
            <h3 style="color: #15803d; font-family: 'Montserrat', sans-serif; font-weight: 700;">💡 Tips for best results:</h3>
            <ul style="color: #374151; line-height: 1.8; font-weight: 500;">
                <li>Speak clearly and naturally</li>
                <li>Find a quiet environment</li>
                <li>Express your genuine feelings</li>
                <li>Try different emotions</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

elif "🎥" in st.session_state.app_mode:
    create_welcome_header("Facial Emotion Analysis", "Understand your emotions through facial expressions", "🎥")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📹 Facial Expression Scan")
        scan_duration = st.slider("Scan duration (seconds):", 3, 10, 5)
        
        if st.button("📹 Start Facial Scan", use_container_width=True):
            with st.spinner(f"Scanning for {scan_duration} seconds... Look at the camera!"):
                dominant_emotion, confidence = analyze_video_stream(duration=scan_duration)
            
            if "Error" in dominant_emotion or "No face" in dominant_emotion:
                st.error(dominant_emotion)
            else:
                st.success("Scan complete!")
                
                # Display results
                emotion_colors = {
                    "happy": "#84cc16",
                    "sad": "#be123c",
                    "angry": "#be123c", 
                    "surprised": "#f97316",
                    "neutral": "#4b5563",
                    "fear": "#be123c",
                    "disgust": "#be123c"
                }
                color = emotion_colors.get(dominant_emotion.lower(), "#6b7280")
                
                st.markdown(f"""
                <div style="background: {color}; color: white; padding: 1.5rem; border-radius: 16px; text-align: center; margin: 1rem 0; box-shadow: 0 6px 20px rgba(21,128,61,0.2);">
                    <h3 style="margin: 0; color: white; font-family: 'Montserrat', sans-serif;">Dominant Emotion: {dominant_emotion}</h3>
                    <p style="margin: 0.5rem 0 0 0; color: white;">Analysis Complete</p>
                </div>
                """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: rgba(255, 255, 255, 0.95); border-radius: 20px; padding: 2rem; box-shadow: 0 8px 25px rgba(21,128,61,0.1); backdrop-filter: blur(10px);">
            <h3 style="color: #15803d; font-family: 'Montserrat', sans-serif; font-weight: 700;">📸 Scan Tips:</h3>
            <ul style="color: #374151; line-height: 1.8; font-weight: 500;">
                <li>Look directly at the camera</li>
                <li>Ensure good lighting</li>
                <li>Keep your face visible</li>
                <li>Express naturally</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("""
<div style="text-align: center; padding: 2rem; background: rgba(255, 255, 255, 0.95); border-radius: 20px; box-shadow: 0 8px 25px rgba(21,128,61,0.1); margin-top: 3rem; backdrop-filter: blur(10px);">
    <p style="color: #15803d; margin: 0; font-weight: 600; font-size: 1.1rem; font-family: 'Montserrat', sans-serif;">Made with ❤️ for your mental wellness journey</p>
    <p style="color: #166534; font-size: 0.9rem; margin: 0.5rem 0 0 0; font-weight: 500;">MindSight - Your AI Wellness Companion</p>
</div>
""", unsafe_allow_html=True)
