# 🐍 Medusa — Ancient Beauty Oracle

> *"Shed the old skin. Embrace your radiance."*

Medusa is an **AI-powered skincare & haircare assistant** built with **Streamlit** and **Google Gemini 1.5 Flash**. She responds as the mythological oracle reborn — blending ancient mystique with science-backed beauty advice.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🐍 **Medusa Persona** | Playful mythological voice — wise, witty, never preachy |
| 🧴 **Skincare Expertise** | Actives, routines, skin types, concerns, ingredient science |
| 💇 **Haircare Wisdom** | Hair porosity, textures, damage repair, scalp health |
| 🎭 **Mystique Slider** | Tune the oracle's personality from factual to full dramatic mode |
| 🌓 **Dark / Light Mode** | Toggle between themes in the sidebar |
| 💬 **Persistent Chat** | Full conversation history within your session |
| ⚡ **Quick Topics** | Pre-built sidebar shortcuts for common questions |
| 🗑️ **Clear Chat** | Start a fresh session anytime |

---

## 🛠️ Tech Stack

- **UI** — [Streamlit](https://streamlit.io/) with custom CSS (Cinzel + Lato fonts)
- **AI** — [Google Gemini 1.5 Flash](https://ai.google.dev/) via `google-generativeai`
- **Config** — `python-dotenv` for secure API key management

---

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/krithiga-v/medusa--chatbot.git
cd medusa--chatbot
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up your API key
Create a `.env` file in the project root:
```
GOOGLE_API_KEY=your_google_gemini_api_key_here
```
Get your key: [Google AI Studio](https://aistudio.google.com/app/apikey)

### 4. Run the app
```bash
streamlit run Medusa.py
```

Open `http://localhost:8501` in your browser.

---

## 💡 Usage Tips

- **Ask specific questions** — mention your skin type, hair texture, or specific concerns for tailored advice
- **Use the Mystique Slider** to tune between factual responses and dramatic oracle mode
- **Quick Topics** in the sidebar give instant access to common guides
- **Suggestion chips** on the welcome screen help you get started fast

---

## ⚠️ Disclaimer

Medusa is a beauty wellness assistant, not a medical professional. For serious skin or scalp conditions, please consult a licensed dermatologist.

---

## 📁 Project Structure

```
medusa--chatbot/
├── Medusa.py          # Main Streamlit app
├── requirements.txt   # Python dependencies
├── .env               # API key (not committed — add to .gitignore)
└── README.md
```

---

*Built with 🐍 and a touch of ancient magic.*
