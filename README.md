# 🌿 MindSight – AI Mental Wellness Companion

MindSight is a comprehensive, multi-feature **Streamlit application** designed to support mental wellness.  
It combines **real-time conversational AI, journal analysis, mood tracking, personalized insights, and guided exercises** into a single, easy-to-use platform.

---

## ✨ Features

- **🤖 AI Companion**  
  A real-time, empathetic chatbot powered by the **Google Gemini API** for supportive conversations.

- **📔 Journal Analysis**  
  Analyze journal entries for **sentiment**, track **mood trends**, and detect potential crises.

- **📊 Personalized Insights**  
  Discover correlations between **keywords** in your journal and **mood scores**.

- **🎯 Daily Goals Tracker**  
  Set, track, and manage daily wellness goals.

- **💎 Positive Memory Vault**  
  Save and revisit positive memories to boost mental well-being.

- **🎤 Voice & Facial Emotion Analysis**  
  AI-powered emotion detection from **voice** and **facial expressions**.

- **🧘 Guided Exercises**  
  Simple mindfulness activities, including a **guided breathing exercise**.

- **📚 Resource Hub**  
  A curated library of **articles and resources** for mental wellness.

---

## ⚙️ Tech Stack

- **Frontend:** [Streamlit](https://streamlit.io/)  
- **Generative AI:** Google Gemini API  
- **Local AI Models:** Hugging Face Transformers (sentiment & voice), [`fer`](https://github.com/justinshenk/fer) (facial emotion recognition)  
- **Core Libraries:** Pandas, Plotly, OpenCV, Scikit-learn  

---

## 🛠️ Installation & Setup

Follow these steps to run **MindSight** on your local machine:

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd MindSight_Project
```

Or download the ZIP and extract it manually.

---

### 2. Create and Activate a Virtual Environment

It’s recommended to use a **virtual environment** to avoid dependency conflicts.

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# On macOS/Linux
source venv/bin/activate
```

When activated, you should see `(venv)` in your terminal prompt.

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This may take several minutes since large libraries (TensorFlow, PyTorch, etc.) will be installed.

---

### 4. Download spaCy Language Model

```bash
python -m spacy download en_core_web_sm
```

---

### 5. Set Google Gemini API Key

The AI Companion requires a **Google Gemini API Key**.

- Get a key from [Google AI Studio](https://aistudio.google.com/).
- Set it as an **environment variable** (do not hardcode in code).

```powershell
# On Windows (PowerShell)
$env:GOOGLE_API_KEY="AIzaSyA-tQtWlDenTH6tBYoBC9rOhtWlbDH52Kw"

```

⚠️ **Note:** You’ll need to set this variable each time you open a new terminal.

---

### 6. Run the Application

```bash
streamlit run app.py
```

The app will open automatically in your browser 🎉

---

## 📂 Project Structure

```
MindSight/
│
├── app.py                 # Main Streamlit app
├── requirements.txt       # Dependencies
├── utils/
│   ├── text_analysis.py   # Journal sentiment & analysis
│   ├── generative_ai.py   # GPT/Gemini API integration
│   ├── voice_emotion.py   # Voice emotion detection
│   ├── face_emotion.py    # Facial emotion detection
│   └── data_storage.py    # Data persistence & utilities
└── README.md              # Project documentation
```

---

## 🤝 Contributing

We welcome contributions!  
- Fork the repo  
- Create a new branch (`feature/your-feature`)  
- Commit changes and push  
- Submit a Pull Request 🚀  

---

## 📜 License

This project is licensed under the **MIT License**.  
See [LICENSE](LICENSE) for details.

---

## 💡 Acknowledgements

- [Streamlit](https://streamlit.io/) for rapid app development  
- [Google AI Studio](https://aistudio.google.com/) for Gemini API  
- [Hugging Face](https://huggingface.co/) for open-source NLP & AI models  
- [FER](https://github.com/justinshenk/fer) for facial emotion recognition  

---

## 🌟 Final Note

MindSight is not a replacement for professional mental health care.  
If you’re struggling, please seek help from a qualified professional.
