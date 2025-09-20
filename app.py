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
st.set_page_config(layout="wide")

# --- NAVIGATION ---
st.sidebar.title("Navigation")
app_mode = st.sidebar.selectbox(
    "Choose a feature",
    ["AI Companion", "Journal Analysis", "My Insights", "Daily Goals", "Memory Vault", "Resource Hub", "Guided Exercises", "Voice Emotion", "Facial Emotion"]
)

# --- AI COMPANION CHATBOT ---
if app_mode == "AI Companion":
    st.title("MindSight - AI Wellness Companion 💬")

    random_memory = get_random_memory()
    if random_memory:
        st.info(f"✨ **Remember this happy moment?**\n\n*'{random_memory}'*")

    if "messages" not in st.session_state:
        insights = analyze_journal_insights()
        proactive_insight = None
        if insights and "error" not in insights and "message" not in insights:
            first_insight_key = next(iter(insights))
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

# --- JOURNAL ANALYSIS & MOOD TRENDING ---
elif app_mode == "Journal Analysis":
    st.title("Analyze Your Journal Entry 📝")
    st.info("Write about your day, and the AI will analyze the sentiment and track your mood over time.")
    journal_entry = st.text_area("Write your entry here:", height=250)
    if st.button("Analyze Entry") and journal_entry.strip() != "":
        simple_label, numeric_rating = analyze_text(journal_entry)
        st.subheader("Analysis Results")
        st.write(f"Detected Sentiment: **{simple_label}**")
        crisis, helplines = check_crisis(journal_entry)
        if crisis:
            st.error("⚠️ Crisis detected! Please consider reaching out for help:")
            for k, v in helplines.items():
                st.write(f"{k}: {v}")
        log = save_entry(journal_entry, numeric_rating)
        st.plotly_chart(plot_trends(log))

# --- PERSONALIZED INSIGHTS ---
elif app_mode == "My Insights":
    st.title("Your Personalized Insights 💡")
    st.info("Discover patterns in your mood by analyzing your past journal entries.")
    insights = analyze_journal_insights()
    if "error" in insights or "message" in insights:
        st.warning(insights.get("error") or insights.get("message"))
    else:
        for category, finding in insights.items():
            st.success(f"**{category} Activities:** {finding}")

# --- DAILY GOALS ---
elif app_mode == "Daily Goals":
    st.title("Daily Goals & Habit Tracker 🎯")
    st.info("Set small, achievable goals for today to build positive habits.")
    
    new_goal = st.text_input("Add a new goal for today:", key="new_goal_input")
    if st.button("Add Goal") and new_goal:
        add_goal(new_goal)
        st.rerun()

    st.subheader("Today's Goals")
    todays_goals = get_todays_goals()
    if not todays_goals:
        st.write("No goals set for today. Add one above!")
    else:
        for i, goal in enumerate(todays_goals):
            col1, col2 = st.columns([0.9, 0.1])
            with col1:
                is_completed = st.checkbox(
                    goal["text"], 
                    value=goal["completed"], 
                    key=f"goal_{i}"
                )
                if is_completed != goal["completed"]:
                    update_goal_status(i, is_completed)
                    st.rerun()
            with col2:
                if st.button("❌", key=f"remove_goal_{i}"):
                    remove_goal(i)
                    st.rerun()

# --- MEMORY VAULT ---
elif app_mode == "Memory Vault":
    st.title("Positive Memory Vault ✨")
    st.info("Save happy memories, accomplishments, or things you're grateful for.")
    
    new_memory = st.text_area("Add a positive memory to your vault:", height=150)
    if st.button("Save Memory") and new_memory:
        add_memory(new_memory)
        st.success("Memory saved!")
        st.rerun()

    st.subheader("Your Saved Memories")
    all_memories = load_memories()
    if not all_memories:
        st.write("Your vault is empty. Add a memory above!")
    else:
        for i, mem in enumerate(reversed(all_memories)):
            col1, col2 = st.columns([0.9, 0.1])
            with col1:
                st.markdown(f"- *{mem}*")
            with col2:
                if st.button("❌", key=f"remove_mem_{i}"):
                    remove_memory(mem) 
                    st.rerun()

# --- RESOURCE HUB ---
elif app_mode == "Resource Hub":
    st.title("Mental Wellness Resource Hub 📚")
    for category, resources in RESOURCE_DATA.items():
        with st.expander(f"**{category}**"):
            for resource in resources:
                st.markdown(f"#### [{resource['title']}]({resource['url']})")
                st.write(resource['desc'])

# --- GUIDED EXERCISES ---
elif app_mode == "Guided Exercises":
    st.title("Mindfulness & Guided Exercises 🧘")
    st.write("Take a moment to center yourself with a guided activity.")
    st.subheader("1-Minute Box Breathing")
    st.write("This simple exercise can help calm your nervous system and reduce stress.")
    if st.button("Start Breathing Exercise"):
        progress_bar = st.progress(0.0)
        status_text = st.empty()
        total_steps = 60
        step_counter = 0
        for _ in range(4):
            status_text.write("### Breathe In...")
            for _ in range(4):
                time.sleep(1)
                step_counter += 1
                progress_bar.progress(step_counter / total_steps)
            status_text.write("### Hold...")
            for _ in range(4):
                time.sleep(1)
                step_counter += 1
                progress_bar.progress(step_counter / total_steps)
            status_text.write("### Breathe Out...")
            for _ in range(4):
                time.sleep(1)
                step_counter += 1
                progress_bar.progress(step_counter / total_steps)
            if step_counter < total_steps - 4:
                status_text.write("### Hold...")
                for _ in range(4):
                    time.sleep(1)
                    step_counter += 1
                    progress_bar.progress(step_counter / total_steps)
        progress_bar.progress(1.0)
        status_text.success("Exercise complete! Well done. ✨")
        
# --- VOICE EMOTION ---
elif app_mode == "Voice Emotion":
    st.title("Analyze Voice Emotion 🎤")
    st.subheader("Record your thoughts, and the AI will detect the primary emotion in your voice.")
    duration = st.slider("Select recording duration (seconds):", 5, 60, 15)
    if st.button("Start Recording"):
        fs = 16000
        with st.spinner(f"Recording for {duration} seconds..."):
            audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
            sd.wait()
        st.success("Recording complete! Analyzing...")
        temp_audio_file = "temp_audio.wav"
        sf.write(temp_audio_file, audio, fs)
        label, confidence = get_voice_emotion(temp_audio_file)
        st.write(f"Detected Voice Emotion: **{label}** (Confidence: {confidence:.2f}%)")

# --- FACIAL EMOTION ---
elif app_mode == "Facial Emotion":
    st.title("Analyze Facial Emotion 🎥")
    st.subheader("Scan your facial expression to find the dominant emotion.")
    
    # Add a slider to select the scan duration
    scan_duration = st.slider("Select scan duration (seconds):", 3, 10, 5)
    
    if st.button("Start Scan"):
        with st.spinner(f"Scanning for {scan_duration} seconds... Please look at the camera."):
            dominant_emotion, _ = analyze_video_stream(duration=scan_duration)
        
        if "Error" in dominant_emotion or "No face" in dominant_emotion:
            st.error(dominant_emotion)
        else:
            st.success("Scan complete!")
            st.write(f"Dominant Facial Emotion: **{dominant_emotion}**")