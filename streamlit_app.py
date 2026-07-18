import streamlit as st
import time
from dotenv import load_dotenv

load_dotenv()

from src.rag.rag_pipeline import chat
from src.utils.voice_handler import speech_to_text, text_to_speech

# Page configuration
st.set_page_config(
    page_title="Store Assistant AI",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom premium styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Background and containers */
    .stApp {
        background: linear-gradient(135deg, #0f1123 0%, #151932 100%);
        color: #ffffff;
    }
    
    /* Title and Header */
    .title-text {
        font-weight: 800;
        font-size: 3rem;
        background: linear-gradient(90deg, #4f46e5 0%, #06b6d4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    
    .subtitle-text {
        color: #94a3b8;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    /* Chat bubbles styling */
    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 1rem;
        padding: 1rem;
    }
    
    .chat-bubble {
        padding: 1rem 1.25rem;
        border-radius: 1.25rem;
        max-width: 75%;
        margin-bottom: 0.5rem;
        font-size: 1.05rem;
        line-height: 1.5;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    
    .user-bubble {
        align-self: flex-end;
        background: linear-gradient(135deg, #4f46e5 0%, #3b82f6 100%);
        color: white;
        border-bottom-right-radius: 0.25rem;
    }
    
    .assistant-bubble {
        align-self: flex-start;
        background: rgba(30, 41, 59, 0.7);
        color: #f1f5f9;
        border-bottom-left-radius: 0.25rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }
    
    /* Glowing sidebar cards */
    .product-card {
        background: rgba(30, 41, 59, 0.5);
        border: 1px solid rgba(79, 70, 229, 0.3);
        padding: 1.25rem;
        border-radius: 1rem;
        backdrop-filter: blur(5px);
        box-shadow: 0 0 15px rgba(79, 70, 229, 0.15);
        margin-bottom: 1.5rem;
    }
    
    .product-header {
        font-weight: 800;
        font-size: 1.2rem;
        color: #818cf8;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        padding-bottom: 0.5rem;
        margin-bottom: 0.75rem;
    }
    
    .product-item {
        font-size: 0.95rem;
        margin-bottom: 0.4rem;
        display: flex;
        justify-content: space-between;
    }
    
    .product-label {
        color: #94a3b8;
    }
    
    .product-value {
        font-weight: 600;
        color: #f8fafc;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "Welcome! Ask me if a product is available (e.g. 'Is Whole Wheat Atta available?'), and I'll find it, tell you the price, expiry date, and store location."}
    ]

if "active_product" not in st.session_state:
    st.session_state.active_product = None

# Sidebar Content
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3081/3081559.png", width=80)
    st.markdown("<h3 style='margin-bottom: 0.5rem;'>Voice Assistant</h3>", unsafe_allow_html=True)
    
    # Speak Button
    if st.button("🎙️ Speak / Voice Input", use_container_width=True, help="Click to speak your question directly"):
        with st.spinner("🎙️ Listening... Speak now."):
            spoken_text = speech_to_text()
            
        if spoken_text.startswith("Error"):
            st.error(spoken_text)
        else:
            # Add user query to chat history
            st.session_state.chat_history.append({"role": "user", "content": spoken_text})
            
            # Process query
            with st.spinner("Processing your query..."):
                response = chat(spoken_text, state=st.session_state)
            
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            
            # Speak the response
            text_to_speech(response)
            st.rerun()

    st.markdown("---")
    
    # Selected Product Status Card
    if st.session_state.active_product:
        prod = st.session_state.active_product
        st.markdown(f"""
        <div class="product-card">
            <div class="product-header">📦 Selected Product</div>
            <div class="product-item">
                <span class="product-label">Name:</span>
                <span class="product-value">{prod.get('Name', 'N/A')}</span>
            </div>
            <div class="product-item">
                <span class="product-label">Category:</span>
                <span class="product-value">{prod.get('Category', 'N/A')}</span>
            </div>
            <div class="product-item">
                <span class="product-label">Price:</span>
                <span class="product-value">{prod.get('Price/RS', '0')} RS</span>
            </div>
            <div class="product-item">
                <span class="product-label">Expiry:</span>
                <span class="product-value">{prod.get('Expiry Date', 'N/A')}</span>
            </div>
            <div class="product-item">
                <span class="product-label">Location:</span>
                <span class="product-value">Block {prod.get('Block Name', 'N/A')}, Rack {prod.get('Rack No', 'N/A')}</span>
            </div>
            <div class="product-item">
                <span class="product-label">Section:</span>
                <span class="product-value">{prod.get('Session', 'N/A')}</span>
            </div>
            <div class="product-item">
                <span class="product-label">Stock Status:</span>
                <span class="product-value" style="color: {'#10b981' if int(prod.get('Stock Quantity', 0)) > 10 else '#ef4444'};">
                    {prod.get('Stock Quantity', '0')} left ({'In Stock' if int(prod.get('Stock Quantity', 0)) > 10 else 'Low Stock'})
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="product-card" style="border-style: dashed; border-color: rgba(255,255,255,0.2);">
            <div class="product-header" style="color: #94a3b8;">📦 No Product Selected</div>
            <p style="color: #94a3b8; font-size: 0.9rem; margin-bottom: 0;">Ask about a product's availability to view its specs here.</p>
        </div>
        """, unsafe_allow_html=True)

    # Admin Redirect (just text to help navigation)
    st.markdown("---")
    st.markdown("🔒 **Admin Access**")
    st.markdown("To manage inventory, switch over to the Admin App.")


# Main App Layout
st.markdown("<div class='title-text'>Smart Store Assistant</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle-text'>Your voice and chat-based shopping companion</div>", unsafe_allow_html=True)

# Render Chat History
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
for msg in st.session_state.chat_history:
    role_class = "user-bubble" if msg["role"] == "user" else "assistant-bubble"
    st.markdown(f'<div class="chat-bubble {role_class}">{msg["content"]}</div>', unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Text Chat Input
if prompt := st.chat_input("Ask a question about store products..."):
    # Add user message to chat history
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    
    # Process query
    with st.spinner("Analyzing..."):
        response = chat(prompt, state=st.session_state)
        
    st.session_state.chat_history.append({"role": "assistant", "content": response})
    
    # Speak response in background thread/blocking
    text_to_speech(response)
    st.rerun()