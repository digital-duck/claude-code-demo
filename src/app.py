import streamlit as st
from openai import OpenAI
from typing import List, Dict

st.set_page_config(page_title="OpenRouter Chatbot", page_icon="🤖", layout="wide")

def init_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "api_key" not in st.session_state:
        st.session_state.api_key = ""

def get_available_models():
    return [
        "anthropic/claude-3.5-sonnet",
        "openai/gpt-4o",
        "openai/gpt-4o-mini",
        "meta-llama/llama-3.1-8b-instruct:free",
        "microsoft/wizardlm-2-8x22b",
        "google/gemini-pro-1.5",
        "mistralai/mistral-7b-instruct:free",
        "deepseek/deepseek-chat",
        "deepseek/deepseek-coder",
        "qwen/qwen-2.5-72b-instruct",
        "qwen/qwen-2.5-coder-32b-instruct",
        "01-ai/yi-large",
        "moonshot/moonshot-v1-8k",
        "moonshot/moonshot-v1-32k",
        "zhipuai/glm-4-9b-chat",
        "zhipuai/glm-4-plus"
    ]

def call_openrouter_api(messages: List[Dict], model: str, api_key: str) -> str:
    try:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )
        
        response = client.chat.completions.create(
            model=model,
            messages=messages
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"Error calling API: {str(e)}"

def main():
    init_session_state()
    
    st.title("🤖 OpenRouter Chatbot")
    
    with st.sidebar:
        st.header("Configuration")
        
        api_key = st.text_input(
            "OpenRouter API Key",
            type="password",
            value=st.session_state.api_key,
            help="Enter your OpenRouter API key"
        )
        
        if api_key:
            st.session_state.api_key = api_key
        
        model = st.selectbox(
            "Select Model",
            get_available_models(),
            index=0,
            help="Choose from various AI models including DeepSeek, Qwen, Kimi (Moonshot), and GLM"
        )
        
        st.info(f"Selected model: **{model}**")
        
        if st.button("Clear Chat History"):
            st.session_state.messages = []
            st.rerun()
    
    if not st.session_state.api_key:
        st.warning("Please enter your OpenRouter API key in the sidebar to start chatting.")
        return
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    if prompt := st.chat_input("What would you like to know?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.write(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = call_openrouter_api(
                    st.session_state.messages,
                    model,
                    st.session_state.api_key
                )
            
            st.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()