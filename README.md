<<<<<<< HEAD
# claude-code-demo
claude code examples


## Setup

see https://github.com/wgong/py4kids/blob/master/lesson-18-ai/SWE/Code-Collab/readme-claude-code.md



## How to use Claude Code with OpenRouter.ai
Not working

```bash
export ANTHROPIC_BASE_URL="https://openrouter.ai/api/v1"
export ANTHROPIC_AUTH_TOKEN="sk-or-v1-your-openrouter-key-here"
export ANTHROPIC_MODEL="anthropic/claude-3-5-sonnet-20241022"
```

Test OpenRouter API connectivity with curl  :

```bash
curl -X POST "https://openrouter.ai/api/v1/chat/completions"  \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $OPENROUTER_API_KEY" \
    -d '{  
     "model": "anthropic/claude-3-5-sonnet-20241022",  
     "messages": [{"role": "user", "content": "Hello"}], 
     "max_tokens": 10  
    }' --silent --show-error    
```
=======
# OpenRouter Chatbot

A Streamlit-based chatbot application that integrates with OpenRouter.ai to provide access to multiple AI models including DeepSeek, Qwen, Kimi (Moonshot), and GLM.

## Features

- 🤖 Chat interface with conversation history
- 🔑 Secure API key configuration via sidebar
- 🎯 Multiple AI model selection including:
  - **Anthropic**: Claude 3.5 Sonnet
  - **OpenAI**: GPT-4o, GPT-4o Mini
  - **DeepSeek**: DeepSeek Chat, DeepSeek Coder
  - **Qwen**: Qwen 2.5 72B Instruct, Qwen 2.5 Coder 32B
  - **Kimi (Moonshot)**: Moonshot v1 8K, Moonshot v1 32K
  - **GLM**: GLM-4 9B Chat, GLM-4 Plus
  - **Meta**: Llama 3.1 8B Instruct
  - **Microsoft**: WizardLM 2 8x22B
  - **Google**: Gemini Pro 1.5
  - **Mistral**: Mistral 7B Instruct
- 🧹 Clear chat history functionality
- ⚡ Real-time model information display

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- OpenRouter API key (get one at [openrouter.ai](https://openrouter.ai))

### Installation

1. **Clone or download the project**:
   ```bash
   git clone <repository-url>
   cd claude-code-demo
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   streamlit run src/app.py
   ```

4. **Access the app**:
   - Open your browser and go to `http://localhost:8501`
   - Enter your OpenRouter API key in the sidebar
   - Select your preferred AI model
   - Start chatting!

### Getting an OpenRouter API Key

1. Visit [openrouter.ai](https://openrouter.ai)
2. Sign up for an account
3. Navigate to the API section
4. Generate a new API key
5. Copy the key and paste it into the app's sidebar

## Usage

1. **Configure API Key**: Enter your OpenRouter API key in the sidebar
2. **Select Model**: Choose from the available AI models in the dropdown
3. **Start Chatting**: Type your message in the chat input and press Enter
4. **Clear History**: Use the "Clear Chat History" button to reset the conversation

## Project Structure

```
claude-code-demo/
├── src/
│   └── app.py          # Main Streamlit application
├── docs/               # Documentation folder
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Dependencies

- `streamlit>=1.28.0` - Web app framework
- `requests>=2.31.0` - HTTP library
- `openai>=1.0.0` - OpenAI API client (compatible with OpenRouter)

## Troubleshooting

- **API Key Issues**: Ensure your OpenRouter API key is valid and has sufficient credits
- **Model Errors**: Some models may have usage restrictions or require specific permissions
- **Connection Issues**: Check your internet connection and OpenRouter service status

## License

This project is open source and available under the Apache License 2.0.
>>>>>>> 6b37aef513ed94cd1242b3cc55f9b5e5213dcb14
