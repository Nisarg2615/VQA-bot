import streamlit as st
import base64
from google import genai
from google.genai import types
from PIL import Image
import io
import time

# ── API KEY ────────────────────────────────────────────────────────────────────
GEMINI_API_KEY = ""   # ← paste your key here

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="VQA Bot — Visual Question Answering",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .stApp { background-color: #0f1117; }
    section[data-testid="stSidebar"] {
        background-color: #161b27;
        border-right: 1px solid #2a2f3e;
    }
    .user-bubble {
        background: linear-gradient(135deg, #1e3a5f, #1a3352);
        border: 1px solid #2a4a7f;
        border-radius: 16px 16px 4px 16px;
        padding: 14px 18px;
        margin: 8px 0;
        color: #e8f0fe;
        font-size: 15px;
        max-width: 85%;
        margin-left: auto;
    }
    .bot-bubble {
        background: #1a1f2e;
        border: 1px solid #2a2f3e;
        border-radius: 16px 16px 16px 4px;
        padding: 14px 18px;
        margin: 8px 0;
        color: #d4d8e8;
        font-size: 15px;
        max-width: 90%;
        line-height: 1.7;
    }
    .pill-green {
        background: #0d3321; border: 1px solid #196c3d;
        color: #3fb950; border-radius: 20px;
        padding: 3px 12px; font-size: 12px; font-weight: 600; display: inline-block;
    }
    .vqa-header { text-align: center; padding: 24px 0 8px 0; border-bottom: 1px solid #2a2f3e; margin-bottom: 24px; }
    .vqa-header h1 { font-size: 28px; font-weight: 700; color: #e8f0fe; margin: 0; }
    .vqa-header p  { color: #8b9ab8; font-size: 14px; margin-top: 6px; }
    .stButton > button {
        background: #1a1f2e; border: 1px solid #2a2f3e; color: #8b9ab8;
        border-radius: 8px; font-size: 13px; padding: 6px 12px;
        transition: all 0.2s; width: 100%; text-align: left;
    }
    .stButton > button:hover { border-color: #4a7fd4; color: #7eb8f7; background: #1e2a3d; }
    .stTextInput > div > div > input, .stTextArea textarea {
        background: #1a1f2e !important; border: 1px solid #2a2f3e !important;
        color: #e8f0fe !important; border-radius: 10px !important;
    }
    .stSelectbox > div > div { background: #1a1f2e !important; border-color: #2a2f3e !important; color: #e8f0fe !important; }
    [data-testid="stMetric"] { background: #1a1f2e; border: 1px solid #2a2f3e; border-radius: 10px; padding: 12px 16px; }
    [data-testid="stMetricLabel"] { color: #8b9ab8 !important; font-size: 12px !important; }
    [data-testid="stMetricValue"] { color: #e8f0fe !important; font-size: 20px !important; }
    hr { border-color: #2a2f3e; }
    .stSuccess { background: #0d3321 !important; border: 1px solid #196c3d !important; }
    .stError   { background: #3d0d0d !important; border: 1px solid #6c1919 !important; }
    .stWarning { background: #3d2a0d !important; border: 1px solid #6c4f1f !important; }
</style>
""", unsafe_allow_html=True)

# ── Session state ──────────────────────────────────────────────────────────────
for k, v in {
    "messages": [], "total_queries": 0,
    "current_image": None, "current_image_b64": None, "current_image_mime": None
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Helpers ────────────────────────────────────────────────────────────────────
def image_to_base64(img_bytes: bytes) -> str:
    return base64.b64encode(img_bytes).decode("utf-8")

def get_mime(uploaded_file) -> str:
    ext = uploaded_file.name.split(".")[-1].lower()
    return {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png",
            "webp": "image/webp", "bmp": "image/bmp"}.get(ext, "image/jpeg")

def get_image_info(img_bytes: bytes) -> dict:
    img = Image.open(io.BytesIO(img_bytes))
    return {"size": f"{img.width} × {img.height}", "mode": img.mode}

def ask_gemini(api_key: str, model: str, image_b64: str, mime: str,
               question: str, history: list, system_prompt: str) -> str:
    client = genai.Client(api_key=api_key)

    # Build conversation: past text turns + current image+question
    contents = []
    for msg in history[:-1]:
        role = "user" if msg["role"] == "user" else "model"
        contents.append(types.Content(role=role, parts=[types.Part(text=msg["content"])]))

    # Current turn with the image
    img_part  = types.Part(inline_data=types.Blob(mime_type=mime, data=base64.b64decode(image_b64)))
    text_part = types.Part(text=question)
    contents.append(types.Content(role="user", parts=[img_part, text_part]))

    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.4,
            max_output_tokens=1024,
        ),
    )
    return response.text

# ── SIDEBAR ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    api_key = GEMINI_API_KEY
    st.markdown('<span class="pill-green">✓ Gemini API key loaded</span>', unsafe_allow_html=True)

    st.markdown("---")

    model = st.selectbox(
        "Gemini Model",
        options=[
            "gemini-2.5-flash",
            "gemini-2.5-flash-lite-preview-06-17",
        ],
        index=0,
        help="2.5 Flash = best free vision model. Flash-Lite = faster & lighter.",
    )

    st.markdown("---")

    system_prompt = st.text_area(
        "System prompt",
        value=(
            "You are an expert visual analyst and troubleshooting assistant. "
            "When shown an image, analyze it carefully and answer the user's question in detail. "
            "For diagrams: explain components, relationships, and flow. "
            "For technical photos: identify issues, explain what you see, and provide actionable advice. "
            "Be structured, clear, and thorough."
        ),
        height=140,
    )

    st.markdown("---")
    st.markdown("### 📊 Session Stats")
    c1, c2 = st.columns(2)
    c1.metric("Queries", st.session_state.total_queries)
    c2.metric("Messages", len(st.session_state.messages))

    st.markdown("---")
    if st.button("🗑️ Clear conversation", use_container_width=True):
        for k in ["messages", "total_queries", "current_image", "current_image_b64", "current_image_mime"]:
            st.session_state[k] = [] if k == "messages" else (0 if k == "total_queries" else None)
        st.rerun()

# ── MAIN ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="vqa-header">
  <h1>🔍 Visual Question Answering Bot</h1>
  <p>Powered by Google Gemini · Upload any image and ask anything about it</p>
</div>
""", unsafe_allow_html=True)

col_img, col_chat = st.columns([1, 1.6], gap="large")

# ── Left: Image Panel ──────────────────────────────────────────────────────────
with col_img:
    st.markdown("#### 🖼️ Upload Image")
    uploaded = st.file_uploader("Drop an image here", type=["jpg","jpeg","png","webp","bmp"],
                                label_visibility="collapsed")

    if uploaded:
        img_bytes = uploaded.read()
        st.session_state.current_image      = img_bytes
        st.session_state.current_image_b64  = image_to_base64(img_bytes)
        st.session_state.current_image_mime = get_mime(uploaded)
        st.image(img_bytes, use_container_width=True)
        info = get_image_info(img_bytes)
        c1, c2 = st.columns(2)
        c1.caption(f"📐 {info['size']} px")
        c2.caption(f"📄 {uploaded.name}")
    elif st.session_state.current_image:
        st.image(st.session_state.current_image, use_container_width=True)
        st.caption("Previously uploaded image — still active")
    else:
        st.markdown("""
        <div style="border:2px dashed #2a2f3e;border-radius:12px;padding:40px 20px;text-align:center;color:#4a5568;">
            <div style="font-size:40px;margin-bottom:12px;">📷</div>
            <div style="font-size:14px;">Upload a JPG, PNG, or WEBP</div>
            <div style="font-size:12px;margin-top:6px;color:#3a4258;">Diagrams, circuit boards, screenshots,<br>machine photos, charts — anything visual</div>
        </div>
        """, unsafe_allow_html=True)

    if st.session_state.current_image:
        st.markdown("---")
        st.markdown("**💡 Quick questions**")
        for preset in [
            "📋 Describe everything you see",
            "⚠️ Identify any problems or issues",
            "🔧 Explain how this works",
            "📊 Summarize the key information",
            "🔍 What should I focus on?",
        ]:
            if st.button(preset, key=f"p_{preset[:15]}"):
                st.session_state["prefill"] = preset[2:].strip()
                st.rerun()

# ── Right: Chat Panel ──────────────────────────────────────────────────────────
with col_chat:
    st.markdown("#### 💬 Ask About the Image")

    chat_container = st.container(height=420)
    with chat_container:
        if not st.session_state.messages:
            st.markdown("""
            <div style="text-align:center;padding:60px 20px;color:#4a5568;">
                <div style="font-size:36px;margin-bottom:12px;">🤖</div>
                <div style="font-size:15px;color:#6b7a99;">Upload an image and ask me anything!</div>
            </div>
            """, unsafe_allow_html=True)
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f'<div class="user-bubble">🧑 {msg["content"]}</div>', unsafe_allow_html=True)
            else:
                with st.chat_message("assistant"):
                    st.markdown(msg["content"])

    st.markdown("---")
    prefill = st.session_state.pop("prefill", "")
    question = st.text_input("Your question", value=prefill,
                             placeholder="e.g. What does this diagram show?",
                             label_visibility="collapsed")

    send_col, clear_col = st.columns([3, 1])
    with send_col:
        send = st.button("🔍 Analyze", type="primary", use_container_width=True)
    with clear_col:
        if st.button("↺ Reset", use_container_width=True):
            st.session_state.messages = []
            st.session_state.total_queries = 0
            st.rerun()

    if send and question:
        if not st.session_state.current_image_b64:
            st.error("📷 Please upload an image first.")
        else:
            st.session_state.messages.append({"role": "user", "content": question})
            st.session_state.total_queries += 1
            try:
                with st.spinner("🧠 Gemini is analyzing..."):
                    t0 = time.time()
                    answer = ask_gemini(
                        api_key=api_key,
                        model=model,
                        image_b64=st.session_state.current_image_b64,
                        mime=st.session_state.current_image_mime,
                        question=question,
                        history=st.session_state.messages,
                        system_prompt=system_prompt,
                    )
                    elapsed = time.time() - t0
                st.session_state.messages.append({"role": "assistant", "content": answer})
                st.caption(f"⚡ {elapsed:.1f}s · {model}")
                st.rerun()
            except Exception as e:
                err = str(e)
                if "API_KEY" in err or "api key" in err.lower() or "403" in err:
                    st.error("🔑 Invalid API key. Get yours free at aistudio.google.com")
                elif "quota" in err.lower() or "429" in err:
                    st.warning("⏳ Rate limit hit. Wait a moment and retry (free tier limit).")
                elif "SAFETY" in err:
                    st.warning("⚠️ Gemini blocked this due to safety filters. Try rephrasing.")
                else:
                    st.error(f"❌ {err}")