# MindSight – AI Mental Wellness Companion

MindSight is an AI-powered mental wellness platform that integrates conversational AI, journal analysis, emotion detection, mood tracking, and guided exercises into a single, intuitive interface. It helps users understand, reflect on, and improve their emotional well-being through technology, data-driven insights, and evidence-based wellness practices.

**Please note:** MindSight is a supportive tool and does not replace professional mental health care.



## 1. Introduction

Mental wellness is a critical component of overall health. Digital tools that combine self-monitoring, reflective practice, and guided interventions have been shown to enhance well-being, reduce stress, and increase emotional resilience. MindSight leverages advances in natural language processing, affective computing, and AI-driven analytics to provide a holistic, user-friendly platform for mental wellness.



## 2. Features

### AI Companion
A real-time AI chatbot powered by the Google Gemini API for empathetic, context-aware conversations.
- Supports reflective dialogue and emotional expression.
- Provides conversational guidance and motivation.

### Journal Analysis
Analyze daily journal entries for sentiment trends, recurring emotional patterns, and potential distress indicators.
- Helps users recognize triggers and monitor emotional well-being.
- Supports early detection of mental health challenges.

### Personalized Insights
Identify correlations between keywords, mood scores, and behavioral patterns.
- Enables informed decision-making and self-regulation.
- Supports behavioral improvement and emotional awareness.

### Daily Goals Tracker
Set, track, and achieve wellness goals.
- Encourages structured behavioral changes.
- Provides measurable progress and motivation.

### Positive Memory Vault
A secure space to store and revisit positive experiences.
- Strengthens emotional resilience and boosts mood.
- Encourages reflective mindfulness practices.

### Voice & Facial Emotion Analysis
AI models analyze voice tone and facial expressions for emotion detection.
- Combines multimodal cues for a richer understanding of emotional state.

### Guided Exercises
Mindfulness exercises, including guided breathing and meditation.
- Supports emotional regulation and relaxation.
- Enhances attention and mental clarity.

### Resource Hub
A curated collection of articles, tips, and self-help materials to guide users in mental wellness practices.



## 3. Technology Stack

| Layer | Technology / Libraries |
|-------|----------------------|
| Frontend | Streamlit (interactive UI) |
| Generative AI | Google Gemini API (empathetic conversation) |
| Local AI Models | Hugging Face Transformers (sentiment & voice), FER (facial emotion recognition) |
| Data & Visualization | Pandas, Plotly |
| Computer Vision | OpenCV |
| Machine Learning | Scikit-learn |



## 4. Installation and Setup

### Step 1: Clone Repository
```bash
git clone https://github.com/014-Jayal/MindSight-Hackathon
cd MindSight-Hackathon
````

### Step 2: Create and Activate Virtual Environment

```bash
python -m venv venv

# Windows
.\venv\Scripts\Activate.ps1

# macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Download spaCy Model

```bash
python -m spacy download en_core_web_sm
```

### Step 5: Set Google Gemini API Key

```bash
# Windows
$env:GOOGLE_API_KEY="YOUR_API_KEY"
```

### Step 6: Run Application

```bash
streamlit run app.py
```

The app will open automatically in your browser.



## 5. Project Structure

```
MindSight/
│
├── app.py                  # Main Streamlit app
├── requirements.txt        # Python dependencies
├── packages.txt            # System-level dependencies
├── README.md               # Project documentation
└── utils/
    ├── crisis_detection.py
    ├── data_storage.py
    ├── face_emotion.py
    ├── generative_ai.py
    ├── goals.py
    ├── insights.py
    ├── llm_api.py
    ├── memory_vault.py
    ├── resources.py
    ├── text_analysis.py
    └── voice_emotion.py
```



## 6. System Architecture

MindSight’s modular architecture integrates multiple AI components:

1. **Input Layer:** Text (journal entries), voice, and facial images.
2. **Processing Layer:**

   * NLP models for sentiment and keyword analysis
   * Voice and facial emotion recognition models
   * Correlation analysis for insights and trends
3. **Output Layer:**

   * AI Companion responses
   * Mood and goal visualizations
   * Personalized insights and guided exercises

This modular design ensures scalability, maintainability, and easy integration of future AI enhancements.



## 7. Impact and Use Cases

MindSight can be used for:

* Daily self-reflection and mood tracking
* Early identification of emotional distress
* Supporting mindfulness and positive habit formation
* Providing accessible AI-based emotional support

It demonstrates how AI can ethically support mental wellness while balancing accuracy, usability, and user privacy.



## 8. Team

This project was brought to life by the collaborative efforts of:

- [Jayal Shah](https://www.linkedin.com/in/jayal-shah04/)
- [Sakshi Makwana](https://www.linkedin.com/in/sakshii125/)
- [Mayank Jangid](https://www.linkedin.com/in/mayank-jangid-0a5207359/)
- [Raj Patel]
- [Vishwas Patel]



## 9. Contributing

We welcome contributions:

1. Fork the repository.
2. Create a new branch: `feature/your-feature`.
3. Commit your changes and push.
4. Submit a Pull Request.



## 10. Acknowledgements

* [Streamlit](https://streamlit.io/) for rapid app development
* [Google AI Studio](https://aistudio.google.com/) for Gemini API
* [Hugging Face](https://huggingface.co/) for open-source NLP & AI models
* [FER](https://github.com/justinshenk/fer) for facial emotion recognition



## 11. Important Note

MindSight is a supportive tool and **not a substitute for professional mental health care**. Users experiencing emotional distress should seek assistance from qualified healthcare professionals.