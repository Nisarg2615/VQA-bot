# 🔍 VQA Bot — Visual Question Answering

Ask questions about any image using **Google Gemini's free vision API** + **Streamlit**.  
Explain diagrams, troubleshoot photos, analyze charts — all in a clean dark-themed chat UI.

---

## ⚡ Quick Start (3 steps)

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Get your free Gemini API key
- Go to → https://aistudio.google.com
- Sign in with your Google account
- Click **Get API key** → **Create API key**
- Copy the key (starts with `AIza...`)

### 3. Paste the key in `app.py`
Open `app.py` and find line 11:
```python
GEMINI_API_KEY = "your_gemini_api_key_here"   # ← paste your key here
```
Replace `your_gemini_api_key_here` with your actual key.

### 4. Run the app
```bash
streamlit run app.py
```
Opens at `http://localhost:8501` — upload an image and start asking!

---

## 🧠 Models

| Model | Speed | Best For |
|---|---|---|
| `gemini-2.5-flash` | ⚡ Fast | Complex diagrams, detailed analysis |
| `gemini-2.5-flash-lite-preview-06-17` | 🚀 Faster | Quick questions, lighter tasks |

Switch between them anytime from the sidebar — no restart needed.

---

## 💡 What Can It Do?

- Explain circuit diagrams and schematics
- Troubleshoot hardware/software issues from photos
- Read and interpret charts, graphs, and infographics
- Identify problems in engineering drawings
- Analyze screenshots with errors or warnings
- Multi-turn chat — ask follow-up questions about the same image

---

## 🖥️ App Layout

```
┌─────────────────┬──────────────────────────┐
│   Sidebar       │   Left Panel             │
│                 │   • Image upload         │
│  • Model select │   • Image preview        │
│  • System prompt│   • Quick question       │
│  • Session stats│     buttons              │
│  • Clear chat   ├──────────────────────────┤
│                 │   Right Panel            │
│                 │   • Chat history         │
│                 │   • Question input       │
│                 │   • Analyze button       │
└─────────────────┴──────────────────────────┘
```

---

## ⚙️ How the System Prompt Works

The system prompt is passed to Gemini on **every API call** via a dedicated `system_instruction` field — separate from the chat messages. This means:

- It applies to every single response automatically
- You can edit it mid-conversation and it takes effect immediately on the next message
- The full conversation history is also re-sent each call (Gemini is stateless)

---

## 📁 Project Structure

```
vqa-bot/
├── app.py            ← Main Streamlit app (all-in-one)
├── requirements.txt  ← Python dependencies
└── README.md         ← This file
```

---

## 🆓 Free Tier Limits (Gemini)

Gemini's free tier via AI Studio is generous and **never expires**:

| Model | Free RPM | Free TPM |
|---|---|---|
| Gemini 2.5 Flash | 10 | 250,000 |
| Gemini 2.5 Flash Lite | 30 | 1,000,000 |

If you hit rate limits, wait ~30 seconds and retry.  
No credit card required.

---

