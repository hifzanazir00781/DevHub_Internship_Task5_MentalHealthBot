import streamlit as st
from transformers import pipeline, GenerationConfig

# 1. Page Configuration
st.set_page_config(
    page_title="MindCare AI | Hifza Nazir", 
    page_icon="🌱", 
    layout="wide"
)

# --- PREMIUM PROFESSIONAL UI (CSS) ---
st.markdown("""
    <style>
    /* Global Background */
    .stApp {
        background: linear-gradient(135deg, #f5fcf9 0%, #e3f2fd 100%);
    }
    
    /* Top Developer Header */
    .top-dev-line {
        text-align: right;
        font-size: 0.85rem;
        font-weight: 600;
        color: #455A64;
        margin-top: -60px;
        letter-spacing: 1px;
    }

    /* Sidebar Developer Card */
    .sidebar-profile {
        background: linear-gradient(45deg, #2e7d32, #43a047);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.15);
    }

    /* Main UI Header */
    .hero-title {
        font-family: 'Inter', sans-serif;
        color: #1b5e20;
        text-align: center;
        font-size: 3.5rem;
        font-weight: 800;
        margin-top: 10px;
    }

    /* Message Styling */
    .stChatMessage {
        border-radius: 20px !important;
        background: white !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05) !important;
        border: 1px solid #cfd8dc !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Top Minimal Credit
st.markdown("<p class='top-dev-line'>DEVELOPED BY HIFZA NAZIR</p>", unsafe_allow_html=True)

# 3. Sidebar - Profile & Info
with st.sidebar:
    # Developer Profile Card
    st.markdown(f"""
    <div class="sidebar-profile">
        <h3 style="margin:0;">Hifza Nazir</h3>
        <p style="margin:0; font-size: 0.8rem; opacity: 0.9;">AI Engineering Intern</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📘 Task 5: Mental Health Bot")
    st.info("""
    **Objective:** Fine-tuning DistilGPT2 on EmpatheticDialogues to provide supportive responses for emotional wellness.
    """)
    
    st.divider()
    
    if st.button("🗑️ Reset Chat Session", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    st.caption("✨ Built with Streamlit & Hugging Face")

# 4. Model Loading
@st.cache_resource
def load_bot():
    return pipeline("text-generation", model="hifzanazir456/Mental_Health-bot-distilgpt2")

try:
    chat_pipe = load_bot()
except Exception as e:
    st.error(f"Error connecting to AI: {e}")
    st.stop()

# 5. Main UI Content
st.markdown("<h1 class='hero-title'>MindCare AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #455A64; font-size: 1.1rem;'>An Intent-Aware Emotional Support Agent</p>", unsafe_allow_html=True)
st.write("---")

# Session History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am MindCare, your AI companion. I'm here to listen. How are you feeling today?", "avatar": "🌿"}
    ]

# Display Chat
for message in st.session_state.messages:
    avatar = "👤" if message["role"] == "user" else "🌿"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# 6. Chat Logic
prompt = st.chat_input("Tell me what's on your heart...")

if prompt:
    user_input = str(prompt)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)

    with st.chat_message("assistant", avatar="🌿"):
        # Intent Detection
        q_words = ["what", "how", "who", "why", "can you", "tell me"]
        is_question = any(user_input.lower().strip().startswith(w) for w in q_words)
        
        sad_words = ["sad", "upset", "worried", "lost", "lonely", "alone", "failure", "stress", "exam"]
        is_sad = any(word in user_input.lower() for word in sad_words)
        
        # Formatting for the fine-tuned model
        if is_question:
            formatted_input = f"Question: {user_input} Answer:"
        elif is_sad:
            formatted_input = f"Situation: {user_input} Emotional Context: Supportive Response: I hear you and I'm so sorry you're feeling this way."
        else:
            formatted_input = f"Situation: {user_input} Emotional Context: Empathetic Response:"
        
        gen_config = GenerationConfig(
            max_new_tokens=65, 
            do_sample=True,
            temperature=0.4, 
            repetition_penalty=1.5,
            pad_token_id=chat_pipe.tokenizer.eos_token_id
        )
        
        with st.status("Thinking with empathy...", expanded=False) as status:
            result = chat_pipe(formatted_input, generation_config=gen_config)
            full_text = result[0]['generated_text']
            status.update(label="Ready", state="complete")
        
        # Parse Response
        response = full_text.split("Answer:")[-1].split("Response:")[-1].strip()
        
        # Guardrails
        if is_sad and not any(x in response.lower() for x in ["sorry", "support", "listen"]):
            response = "I am so sorry to hear that. I'm here to support you. " + response
            
        response = response.replace("comma", ",").strip()
        if "." in response:
            response = response.rsplit(".", 1)[0] + "."
        
        if len(response) < 10: 
             response = "I'm here for you. Could you tell me more about what's on your mind?"
             
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})