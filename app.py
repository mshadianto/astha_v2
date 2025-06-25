"""
Streamlit App dengan Qwen3 via OpenRouter API
Run: streamlit run app.py
"""

import streamlit as st
import requests
import json
import os
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Qwen3 AI Assistant", 
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #FF6B35;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #FF6B35;
    }
    .user-message {
        background-color: #f0f2f6;
        border-left-color: #0066cc;
    }
    .assistant-message {
        background-color: #e8f5e8;
        border-left-color: #00cc66;
    }
    .sidebar-content {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

class QwenAssistant:
    """Qwen3 AI Assistant via OpenRouter"""
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://openrouter.ai/api/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8501",  # Streamlit default
            "X-Title": "Qwen3 Streamlit App"
        }
        
        # Available Qwen models (some free)
        self.models = {
            "qwen2.5-coder-32b": "qwen/qwen2.5-coder-32b-instruct",  # Free tier
            "qwen2-72b": "qwen/qwen2-72b-instruct",
            "qwen2.5-7b": "qwen/qwen2.5-7b-instruct",  # Free tier
            "qwen2.5-14b": "qwen/qwen2.5-14b-instruct"
        }
    
    def get_available_models(self):
        """Get list of available models"""
        try:
            response = requests.get(
                f"{self.base_url}/models",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                models = response.json()
                qwen_models = [
                    model for model in models.get('data', [])
                    if 'qwen' in model.get('id', '').lower()
                ]
                return qwen_models
            return []
        except Exception as e:
            st.error(f"Error fetching models: {e}")
            return []
    
    def chat_completion(self, messages, model="qwen/qwen2.5-coder-32b-instruct", 
                       temperature=0.7, max_tokens=1000, stream=False):
        """Send chat completion request"""
        
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": stream
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                st.error(f"API Error: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.Timeout:
            st.error("Request timed out. Please try again.")
            return None
        except Exception as e:
            st.error(f"Error: {e}")
            return None
    
    def stream_chat_completion(self, messages, model="qwen/qwen2.5-coder-32b-instruct", 
                              temperature=0.7, max_tokens=1000):
        """Stream chat completion for real-time response"""
        
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": True
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                stream=True,
                timeout=30
            )
            
            if response.status_code == 200:
                for line in response.iter_lines():
                    if line:
                        line = line.decode('utf-8')
                        if line.startswith('data: '):
                            data = line[6:]
                            if data == '[DONE]':
                                break
                            try:
                                chunk = json.loads(data)
                                delta = chunk.get('choices', [{}])[0].get('delta', {})
                                content = delta.get('content', '')
                                if content:
                                    yield content
                            except json.JSONDecodeError:
                                continue
            else:
                st.error(f"Streaming Error: {response.status_code}")
                
        except Exception as e:
            st.error(f"Streaming Error: {e}")

def main():
    """Main Streamlit app"""
    
    # Header
    st.markdown('<h1 class="main-header">🤖 Qwen3 AI Assistant</h1>', unsafe_allow_html=True)
    
    # Sidebar for configuration
    with st.sidebar:
        st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
        st.header("⚙️ Configuration")
        
        # API Key input
        api_key = st.text_input(
            "OpenRouter API Key",
            type="password",
            help="Get your free API key from https://openrouter.ai/",
            placeholder="sk-or-..."
        )
        
        if api_key:
            # Initialize assistant
            assistant = QwenAssistant(api_key)
            
            # Model selection
            st.subheader("🎯 Model Selection")
            model_options = {
                "Qwen2.5-Coder-32B (Free)": "qwen/qwen2.5-coder-32b-instruct",
                "Qwen2.5-7B (Free)": "qwen/qwen2.5-7b-instruct", 
                "Qwen2-72B": "qwen/qwen2-72b-instruct",
                "Qwen2.5-14B": "qwen/qwen2.5-14b-instruct"
            }
            
            selected_model_name = st.selectbox(
                "Choose Model",
                options=list(model_options.keys()),
                index=0
            )
            selected_model = model_options[selected_model_name]
            
            # Parameters
            st.subheader("🎛️ Parameters")
            temperature = st.slider("Temperature", 0.0, 2.0, 0.7, 0.1)
            max_tokens = st.slider("Max Tokens", 100, 4000, 1000, 100)
            
            # Streaming option
            use_streaming = st.checkbox("Enable Streaming", value=True)
            
            # Model info
            st.info(f"**Selected:** {selected_model_name}")
            if "Free" in selected_model_name:
                st.success("💰 This model is FREE!")
            else:
                st.warning("💳 This model uses paid credits")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Main chat interface
    if not api_key:
        st.warning("⚠️ Please enter your OpenRouter API Key in the sidebar to continue.")
        st.info("""
        **How to get FREE API access:**
        1. Go to https://openrouter.ai/
        2. Sign up for free account
        3. Get $1-5 free credits
        4. Copy your API key
        5. Paste it in the sidebar
        """)
        return
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "You are Qwen, a helpful AI assistant created by Alibaba Cloud. You are knowledgeable, accurate, and helpful."}
        ]
        st.session_state.chat_history = []
    
    # Display chat history
    for message in st.session_state.chat_history:
        with st.container():
            if message["role"] == "user":
                st.markdown(f'''
                <div class="chat-message user-message">
                    <strong>👤 You:</strong><br>
                    {message["content"]}
                </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                <div class="chat-message assistant-message">
                    <strong>🤖 Qwen:</strong><br>
                    {message["content"]}
                </div>
                ''', unsafe_allow_html=True)
    
    # Chat input
    user_input = st.chat_input("Ask Qwen anything...")
    
    if user_input:
        # Add user message to history
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Display user message
        st.markdown(f'''
        <div class="chat-message user-message">
            <strong>👤 You:</strong><br>
            {user_input}
        </div>
        ''', unsafe_allow_html=True)
        
        # Get AI response
        assistant = QwenAssistant(api_key)
        
        # Response container
        response_container = st.empty()
        
        if use_streaming:
            # Streaming response
            response_text = ""
            for chunk in assistant.stream_chat_completion(
                st.session_state.messages, 
                model=selected_model,
                temperature=temperature,
                max_tokens=max_tokens
            ):
                response_text += chunk
                response_container.markdown(f'''
                <div class="chat-message assistant-message">
                    <strong>🤖 Qwen:</strong><br>
                    {response_text}
                </div>
                ''', unsafe_allow_html=True)
            
            if response_text:
                st.session_state.chat_history.append({"role": "assistant", "content": response_text})
                st.session_state.messages.append({"role": "assistant", "content": response_text})
        
        else:
            # Non-streaming response
            with st.spinner("🤖 Qwen is thinking..."):
                response = assistant.chat_completion(
                    st.session_state.messages,
                    model=selected_model,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                
                if response and 'choices' in response:
                    ai_response = response['choices'][0]['message']['content']
                    
                    # Display AI response
                    response_container.markdown(f'''
                    <div class="chat-message assistant-message">
                        <strong>🤖 Qwen:</strong><br>
                        {ai_response}
                    </div>
                    ''', unsafe_allow_html=True)
                    
                    # Add to history
                    st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
                    st.session_state.messages.append({"role": "assistant", "content": ai_response})
        
        # Auto-scroll to bottom
        st.rerun()
    
    # Footer
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = [st.session_state.messages[0]]  # Keep system message
            st.session_state.chat_history = []
            st.rerun()
    
    with col2:
        if st.button("💾 Export Chat"):
            chat_export = {
                "timestamp": datetime.now().isoformat(),
                "model": selected_model,
                "chat_history": st.session_state.chat_history
            }
            st.download_button(
                "Download Chat JSON",
                data=json.dumps(chat_export, indent=2),
                file_name=f"qwen_chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    with col3:
        st.info(f"💬 Messages: {len(st.session_state.chat_history)}")

if __name__ == "__main__":
    main()