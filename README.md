# 🔍 VQA Bot — Visual Question Answering

Ask questions about any image using Groq's free vision API + Streamlit.

---

## ⚡ Quick Start (3 steps)

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Get your free Groq API key
Go to → https://console.groq.com  
Sign up → API Keys → Create Key  
Copy the key (starts with `gsk_...`)

### 3. Run the app
```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`  
Paste your Groq API key in the sidebar → upload an image → ask away!

---

## 🧠 Models Used

| Model | Speed | Best for |
|---|---|---|
| `llama-4-scout-17b` | ⚡ Very fast | Diagrams, quick analysis |
| `llama-4-maverick-17b` | 🎯 More capable | Complex troubleshooting |

Both are **free** on Groq's free tier.

---

## 💡 What can it do?

- Explain circuit diagrams and schematics
- Troubleshoot issues from photos (hardware, software errors, etc.)
- Describe charts, graphs, and infographics
- Identify problems in engineering drawings
- Read and explain screenshots with errors
- Answer follow-up questions about the same image (multi-turn chat)

---

## 📁 Project Structure

```
vqa-bot/
├── app.py            ← Main Streamlit app
├── requirements.txt  ← Python dependencies
└── README.md         ← This file
```

---

## 🔧 Customization

- **System prompt**: Edit directly in the sidebar to change bot behavior
- **Model**: Switch between Scout (fast) and Maverick (accurate) in the sidebar
- **Style**: Dark theme by default, all CSS is in the `<style>` block at the top of `app.py`

---

## 🆓 Free Tier Limits (Groq)

Groq's free tier is generous for personal/demo use:
- ~14,400 tokens/minute for LLaMA 4 models
- No credit card required

If you hit rate limits, wait ~30 seconds and retry.
