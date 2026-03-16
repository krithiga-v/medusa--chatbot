import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
import time
import random

# ─────────────────────────────────────────────
# CONFIG & SETUP
# ─────────────────────────────────────────────
load_dotenv()

st.set_page_config(
    page_title="Medusa | Beauty Oracle",
    page_icon="🐍",
    layout="wide",
    initial_sidebar_state="expanded",
)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# ─────────────────────────────────────────────
# SYSTEM PROMPT
# ─────────────────────────────────────────────
MEDUSA_SYSTEM_PROMPT = """
You are Medusa — the ancient beauty oracle, reborn as a modern skincare and haircare goddess.
Once cursed, now empowered. Your serpentine wisdom spans millennia of beauty rituals from every civilization on Earth.

PERSONA GUIDELINES:
- Speak with confident, mythological flair — you are wise, witty, and slightly dramatic.
- Use occasional snake/mythology metaphors ("Let my scales of wisdom guide you...", "Shed the old skin...").
- Be warm and encouraging. Beauty struggles are sacred to you.
- Never shame users. All skin types and hair textures are worthy of your oracle wisdom.
- You are BOTH traditionally wise AND science-aware. Always blend the two.
- Honor ancient knowledge first, then validate with science where applicable.

EXPERTISE AREAS:
1. SKINCARE — cleansers, moisturizers, serums, actives (retinol, AHAs, BHAs, vitamin C, niacinamide, etc.)
2. HAIRCARE — scalp health, hair types (1A-4C), protein-moisture balance, growth, damage repair
3. SKIN CONCERNS — acne, hyperpigmentation, dryness, oiliness, aging, sensitivity, rosacea, eczema
4. HAIR CONCERNS — breakage, shedding, frizz, dandruff, chemical damage, heat damage
5. INGREDIENTS — what to layer, what to avoid mixing, holy grail combos
6. PRODUCT RECOMMENDATIONS — suggest categories & key ingredients (no specific brand bias)
7. ROUTINES — AM/PM routines, seasonal adjustments, lifestyle factors

TRADITIONAL & HOME REMEDIES — THIS IS CRITICAL:
You MUST always include traditional, natural, and home remedy options in EVERY response. These are equally
important as modern treatments. Always cover:
- Kitchen ingredients: honey, turmeric, neem, aloe vera, coconut oil, castor oil, onion juice, fenugreek,
  rice water, egg, yogurt, besan (gram flour), multani mitti, sandalwood, rosewater, apple cider vinegar,
  lemon, amla, hibiscus, curry leaves, methi, and more.
- Ayurvedic remedies and herbs — brahmi, bhringraj, amla, neem, shikakai, reetha, kumkumadi, ashwagandha
- Traditional Indian, African, East Asian, Mediterranean beauty rituals
- DIY hair masks, face packs, scalp treatments, and oil blends with exact recipes and how-to steps
- Ancient practices: ubtan, oil pulling, herbal steam, cold water rinses
- Grandma-approved remedies that generations have trusted

RESPONSE STRUCTURE — ALWAYS follow this format for treatment questions:
1. 🌿 Traditional & Home Remedies — list DIY and natural options FIRST with full recipes and instructions
2. 🧴 Modern / Clinical Options — actives, products, dermatological approaches
3. 🔄 How to Combine Both — how traditional and modern can work together
4. ✨ Oracle's Tip — one personalized insight or next step

RESPONSE STYLE:
- Open with a brief mythological hook when appropriate (not every response).
- Always ask clarifying questions if skin/hair type is not specified.
- End responses with an empowering note or a practical next step.
- Use emojis tastefully: 🐍 🌿 ✨ 🧴 💧 are your favorites.

LENGTH & COMPLETENESS RULES — VERY IMPORTANT:
- You have a strict token limit. You MUST complete your entire answer within it.
- Be concise and dense. No repetition, no filler, no padding.
- Each bullet point: max 1-2 sentences. No long paragraphs.
- For recipes/DIY: list ingredients in one line, steps numbered briefly.
- If covering multiple sections, keep each section to 3-5 bullet points max.
- NEVER start a new section you cannot finish. Plan your response before writing.
- Always write the Oracle's Tip last — it signals a complete response.
- Better to give 3 complete remedies than 6 half-explained ones.

BOUNDARIES:
- Do NOT diagnose medical conditions. For serious concerns, recommend consulting a dermatologist.
- Do NOT recommend specific prescription medications.
- You are a beauty oracle, not a doctor.
"""


# ─────────────────────────────────────────────
# MEDUSA RESPONSES & OPENERS
# ─────────────────────────────────────────────
MEDUSA_GREETINGS = [
    "The oracle awakens... ✨ Ask and you shall receive ancient wisdom.",
    "My serpents sense a beauty question approaching... 🐍",
    "Ah, a seeker of radiance arrives. I have been expecting you.",
    "The scales of beauty wisdom tip in your favor today...",
    "Your glow-up awaits, mortal. Speak your concerns to the oracle.",
]

SUGGESTION_PROMPTS = [
    "🌿 Build my morning skincare routine",
    "🐍 What actives can I layer together?",
    "💧 Help with dry, flaky scalp",
    "✨ How to fade dark spots naturally",
    "🧴 Best routine for oily acne-prone skin",
    "🌙 Evening skincare routine for beginners",
    "💪 How to strengthen brittle hair",
    "🔥 Repair heat-damaged hair",
]

# ─────────────────────────────────────────────
# CUSTOM CSS — REFINED SERPENTINE DARK THEME
# ─────────────────────────────────────────────
def apply_styles(dark_mode: bool):
    if dark_mode:
        bg = "#0A0A0F"
        surface = "#12121A"
        surface2 = "#1A1A26"
        border = "#2A2A40"
        accent = "#7B5EA7"
        accent2 = "#4ECDC4"
        text = "#E8E6F0"
        text_muted = "#8888AA"
        user_bubble = "#1E1E30"
        bot_bubble = "#161624"
        gold = "#C9A84C"
    else:
        bg = "#F5F3FF"
        surface = "#FFFFFF"
        surface2 = "#EEE8FF"
        border = "#D4CCF5"
        accent = "#7B5EA7"
        accent2 = "#2DB5AC"
        text = "#1A1530"
        text_muted = "#666688"
        user_bubble = "#EDE8FF"
        bot_bubble = "#FFFFFF"
        gold = "#A07820"

    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Lato:wght@300;400;500&display=swap');

    :root {{
        --bg: {bg};
        --surface: {surface};
        --surface2: {surface2};
        --border: {border};
        --accent: {accent};
        --accent2: {accent2};
        --text: {text};
        --text-muted: {text_muted};
        --user-bubble: {user_bubble};
        --bot-bubble: {bot_bubble};
        --gold: {gold};
    }}

    html, body, .stApp {{
        background-color: var(--bg) !important;
        color: var(--text) !important;
        font-family: 'Lato', sans-serif !important;
    }}

    /* Sidebar */
    [data-testid="stSidebar"] {{
        background: var(--surface) !important;
        border-right: 1px solid var(--border) !important;
    }}
    [data-testid="stSidebar"] * {{
        color: var(--text) !important;
    }}

    /* Hide default Streamlit elements */
    #MainMenu, footer, header {{ visibility: visible; }}
    .stDeployButton {{ display: none; }}

    /* Title area */
    .medusa-title {{
        font-family: 'Cinzel', serif;
        font-size: 2.6rem;
        font-weight: 700;
        background: linear-gradient(135deg, var(--accent) 0%, var(--gold) 50%, var(--accent2) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        letter-spacing: 0.08em;
        margin-bottom: 0.2rem;
    }}

    .medusa-subtitle {{
        text-align: center;
        color: var(--text-muted);
        font-size: 0.9rem;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        margin-bottom: 1.5rem;
        font-weight: 300;
    }}

    .serpent-divider {{
        text-align: center;
        color: var(--accent);
        font-size: 1.2rem;
        letter-spacing: 0.5em;
        margin: 0.5rem 0 1.5rem 0;
        opacity: 0.7;
    }}

    /* Chat messages */
    .chat-wrapper {{
        display: flex;
        flex-direction: column;
        gap: 1rem;
        padding: 0.5rem 0;
    }}

    .chat-message {{
        display: flex;
        gap: 0.75rem;
        animation: fadeSlide 0.3s ease;
    }}

    @keyframes fadeSlide {{
        from {{ opacity: 0; transform: translateY(8px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}

    .chat-message.user {{ flex-direction: row-reverse; }}

    .avatar {{
        width: 36px;
        height: 36px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.1rem;
        flex-shrink: 0;
        border: 1.5px solid var(--border);
    }}

    .avatar.bot {{
        background: linear-gradient(135deg, var(--accent), var(--accent2));
        border-color: var(--accent);
    }}

    .avatar.user {{
        background: var(--surface2);
    }}

    .bubble {{
        max-width: 75%;
        padding: 0.85rem 1.1rem;
        border-radius: 1rem;
        font-size: 0.93rem;
        line-height: 1.65;
        border: 1px solid var(--border);
    }}

    .bubble.bot {{
        background: var(--bot-bubble);
        border-radius: 0.25rem 1rem 1rem 1rem;
    }}

    .bubble.user {{
        background: var(--user-bubble);
        border-radius: 1rem 0.25rem 1rem 1rem;
        text-align: left;
    }}

    .bubble strong {{ color: var(--accent2); }}
    .bubble em {{ color: var(--gold); font-style: normal; font-weight: 500; }}

    .msg-time {{
        font-size: 0.72rem;
        color: var(--text-muted);
        margin-top: 0.3rem;
        padding: 0 0.2rem;
    }}

    /* Welcome card */
    .welcome-card {{
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 1rem;
        padding: 1.5rem;
        text-align: center;
        margin: 1rem 0;
    }}

    .welcome-oracle-text {{
        font-family: 'Cinzel', serif;
        color: var(--gold);
        font-size: 1.05rem;
        margin-bottom: 0.75rem;
    }}

    .welcome-body {{
        color: var(--text-muted);
        font-size: 0.88rem;
        line-height: 1.6;
    }}

    /* Suggestion chips */
    .suggestion-grid {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 0.5rem;
        margin-top: 1rem;
    }}

    /* Input area */
    .stTextInput > div > div > input,
    .stChatInput > div > div > input,
    textarea {{
        background: var(--surface) !important;
        color: var(--text) !important;
        border: 1px solid var(--border) !important;
        border-radius: 0.75rem !important;
        font-family: 'Lato', sans-serif !important;
    }}

    /* Buttons */
    .stButton > button {{
        background: transparent !important;
        border: 1px solid var(--border) !important;
        color: var(--text) !important;
        border-radius: 2rem !important;
        font-family: 'Lato', sans-serif !important;
        font-size: 0.82rem !important;
        padding: 0.4rem 0.9rem !important;
        transition: all 0.2s ease !important;
        width: 100% !important;
        text-align: left !important;
    }}

    .stButton > button:hover {{
        border-color: var(--accent) !important;
        color: var(--accent) !important;
        background: var(--surface2) !important;
    }}

    /* Toggle & sliders */
    .stToggle, .stSelectbox, .stSlider {{
        font-family: 'Lato', sans-serif !important;
    }}

    /* Sidebar section headers */
    .sidebar-header {{
        font-family: 'Cinzel', serif;
        font-size: 0.78rem;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: var(--accent);
        margin: 1rem 0 0.5rem 0;
        border-bottom: 1px solid var(--border);
        padding-bottom: 0.4rem;
    }}

    /* Scrollbar */
    ::-webkit-scrollbar {{ width: 5px; }}
    ::-webkit-scrollbar-track {{ background: var(--bg); }}
    ::-webkit-scrollbar-thumb {{ background: var(--border); border-radius: 5px; }}

    /* Chat container scroll area */
    .chat-scroll {{
        max-height: 62vh;
        overflow-y: auto;
        padding-right: 0.3rem;
    }}

    /* Stat pills in sidebar */
    .stat-pill {{
        display: inline-block;
        background: var(--surface2);
        border: 1px solid var(--border);
        border-radius: 2rem;
        padding: 0.2rem 0.75rem;
        font-size: 0.78rem;
        color: var(--text-muted);
        margin: 0.2rem 0;
    }}
    .stat-pill span {{ color: var(--accent2); font-weight: 600; }}
    </style>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# GEMINI SETUP
# ─────────────────────────────────────────────
def init_gemini():
    """Initialize Gemini model with the system prompt."""
    if not GOOGLE_API_KEY:
        return None
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction=MEDUSA_SYSTEM_PROMPT,
        generation_config=genai.GenerationConfig(
            temperature=0.82,
            max_output_tokens=8192,
            top_p=0.92,
        ),
    )
    return model


def get_chat_session(model):
    """Get or create a Gemini chat session with full history."""
    if "gemini_chat" not in st.session_state or st.session_state.get("reset_chat"):
        history = []
        for msg in st.session_state.get("messages", []):
            role = "user" if msg["role"] == "user" else "model"
            history.append({"role": role, "parts": [msg["content"]]})
        st.session_state.gemini_chat = model.start_chat(history=history)
        st.session_state.pop("reset_chat", None)
    return st.session_state.gemini_chat


# ─────────────────────────────────────────────
# SESSION STATE INIT
# ─────────────────────────────────────────────
def init_state():
    defaults = {
        "messages": [],
        "dark_mode": True,
        "model_ready": False,
        "temperature": 0.82,
        "show_tips": True,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


# ─────────────────────────────────────────────
# RENDER CHAT MESSAGES
# ─────────────────────────────────────────────
def render_message(role: str, content: str, timestamp: str = ""):
    is_user = role == "user"
    avatar = "🧖" if is_user else "🐍"
    bubble_class = "user" if is_user else "bot"
    avatar_class = "user" if is_user else "bot"
    align_class = "user" if is_user else ""

    st.markdown(f"""
    <div class="chat-message {align_class}">
        <div class="avatar {avatar_class}">{avatar}</div>
        <div>
            <div class="bubble {bubble_class}">{content}</div>
            <div class="msg-time">{timestamp}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        # Logo / branding
        st.markdown("""
        <div style="text-align:center; padding: 1rem 0 0.5rem 0;">
            <div style="font-size: 2.8rem;">🐍</div>
            <div style="font-family:'Cinzel',serif; font-size:1.1rem; 
                        background: linear-gradient(135deg, #7B5EA7, #C9A84C);
                        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                        background-clip: text; font-weight: 700; letter-spacing: 0.1em;">
                MEDUSA
            </div>
            <div style="font-size:0.7rem; color: #8888AA; letter-spacing:0.18em; 
                        text-transform:uppercase; margin-top:0.1rem;">
                Beauty Oracle
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        # Theme toggle
        st.markdown('<div class="sidebar-header">⚙️ Appearance</div>', unsafe_allow_html=True)
        st.session_state.dark_mode = st.toggle(
            "Dark Mode", value=st.session_state.dark_mode
        )

        st.divider()

        # Oracle personality tuning
        st.markdown('<div class="sidebar-header">🎭 Oracle Personality</div>', unsafe_allow_html=True)
        temp = st.slider(
            "Mystique Level",
            min_value=0.1, max_value=1.0, value=st.session_state.temperature,
            step=0.05,
            help="Higher = more creative & dramatic responses. Lower = more factual & concise.",
        )
        st.session_state.temperature = temp
        level_label = "🔮 Full Oracle Mode" if temp > 0.7 else ("⚖️ Balanced" if temp > 0.4 else "📋 Factual Mode")
        st.caption(level_label)

        st.divider()

        # Stats
        msg_count = len(st.session_state.messages)
        user_msgs = sum(1 for m in st.session_state.messages if m["role"] == "user")

        st.markdown('<div class="sidebar-header">📊 Session Stats</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="stat-pill">Messages: <span>{msg_count}</span></div><br>
        <div class="stat-pill">Questions asked: <span>{user_msgs}</span></div>
        """, unsafe_allow_html=True)

        st.divider()

        # Quick topics
        st.markdown('<div class="sidebar-header">🌿 Quick Topics</div>', unsafe_allow_html=True)
        topics = {
            "💆 Skin Types": "Explain the different skin types and how to identify mine",
            "🐍 Actives Guide": "Give me a guide on skincare actives and what not to mix",
            "💇 Hair Porosity": "What is hair porosity and why does it matter?",
            "🌙 Night Routine": "What should a complete nighttime skincare routine include?",
            "🌅 AM Routine": "What's the ideal morning skincare routine order?",
        }
        for label, prompt in topics.items():
            if st.button(label, key=f"topic_{label}"):
                st.session_state["inject_prompt"] = prompt

        st.divider()

        # Clear chat
        st.markdown('<div class="sidebar-header">🗑️ Session</div>', unsafe_allow_html=True)
        if st.button("✨ Start Fresh", key="clear_chat"):
            st.session_state.messages = []
            st.session_state["reset_chat"] = True
            st.rerun()

        # Footer
        st.markdown("""
        <div style="position:fixed; bottom:1rem; font-size:0.7rem; color:#666688; 
                    text-align:center; left:0; right:0; padding: 0 1rem;">
            Powered by Google Gemini 1.5 Flash<br>
            <em>Not a substitute for medical advice</em>
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# MAIN APP
# ─────────────────────────────────────────────
def main():
    init_state()
    apply_styles(st.session_state.dark_mode)

    # Init model
    model = init_gemini()
    if model is None:
        st.error("⚠️ GOOGLE_API_KEY not found. Please add it to your .env file.")
        st.code("GOOGLE_API_KEY=your_key_here", language="bash")
        st.stop()

    render_sidebar()

    # ── Main content ──
    col1, col2, col3 = st.columns([1, 10, 1])
    with col2:

        # Header
        st.markdown('<h1 class="medusa-title">✦ MEDUSA ✦</h1>', unsafe_allow_html=True)
        st.markdown('<p class="medusa-subtitle">Ancient Beauty Oracle · Skincare & Haircare Wisdom</p>', unsafe_allow_html=True)
        st.markdown('<div class="serpent-divider">⋯ 🐍 ⋯</div>', unsafe_allow_html=True)

        # Welcome card (only when no messages)
        if not st.session_state.messages:
            greeting = random.choice(MEDUSA_GREETINGS)
            st.markdown(f"""
            <div class="welcome-card">
                <div class="welcome-oracle-text">{greeting}</div>
                <div class="welcome-body">
                    I am Medusa — reborn as your personal beauty oracle.<br>
                    Ask me anything about <strong>skincare</strong>, <strong>haircare</strong>, 
                    ingredients, routines, and concerns.<br>
                    My serpentine wisdom spans millennia. Your glow awaits. ✨
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Suggestion buttons
            st.markdown("**Try asking:**")
            cols = st.columns(2)
            for i, suggestion in enumerate(SUGGESTION_PROMPTS[:6]):
                with cols[i % 2]:
                    if st.button(suggestion, key=f"suggestion_{i}"):
                        st.session_state["inject_prompt"] = suggestion.split(" ", 1)[1]

        # ── Chat history ──
        chat_container = st.container()
        with chat_container:
            for msg in st.session_state.messages:
                render_message(
                    msg["role"],
                    msg["content"],
                    msg.get("time", ""),
                )

        st.markdown("---")

        # ── Chat input ──
        user_input = st.chat_input(
            "Ask the oracle about your skin or hair...",
            key="chat_input",
        )

        # Handle injected prompts (from sidebar/suggestion buttons)
        if "inject_prompt" in st.session_state:
            user_input = st.session_state.pop("inject_prompt")

        if user_input and user_input.strip():
            timestamp = time.strftime("%I:%M %p")

            # Add user message
            st.session_state.messages.append({
                "role": "user",
                "content": user_input,
                "time": timestamp,
            })

            # Get Gemini response
            with st.spinner("🐍 The oracle is channeling ancient wisdom..."):
                try:
                    chat = get_chat_session(model)
                    response = chat.send_message(user_input)
                    reply = response.text

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": reply,
                        "time": time.strftime("%I:%M %p"),
                    })

                except Exception as e:
                    error_msg = f"⚠️ The oracle's vision is clouded: `{str(e)}`\n\nPlease check your API key and try again."
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_msg,
                        "time": time.strftime("%I:%M %p"),
                    })

            st.rerun()


if __name__ == "__main__":
    main()
