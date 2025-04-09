# ⚛️ Quantum Research Assistant

![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![LangChain](https://img.shields.io/badge/Powered%20by-LangChain-2AA5DC?logo=chainlink&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green.svg)

A sophisticated AI-powered research assistant leveraging language models and real-time web search capabilities, wrapped in an elegant quantum-themed interface.

![Quantum Research Assistant Demo](https://via.placeholder.com/800x450.png?text=Quantum+Research+Assistant+Demo)

## ✨ Features

- **Advanced AI Integration**: Connect to OpenAI's powerful language models or run locally with Ollama
- **Web Search Capability**: Find up-to-date information via Google Search API integration
- **Elegant Themes**: Choose from three visual themes - Quantum Blue, Matrix Green, and Classic
- **Quantum-Inspired UI**: Sleek wave animations and particle effects for a futuristic experience
- **Responsive Design**: Optimized for various screen sizes and devices
- **Configurable Settings**: Easily toggle features and adjust settings through the intuitive sidebar

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- (Optional) Ollama if using local models

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/quantum-research-assistant.git
   cd quantum-research-assistant
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root with your API keys:
   ```
   OPENAI_API_KEY=your_openai_key_here
   GOOGLE_API_KEY=your_google_api_key_here
   GOOGLE_CSE_ID=your_google_cse_id_here
   ```

   > **Note**: The Google Search feature requires both a Google API key and a Custom Search Engine ID.

### Running the App

Launch the application with:

```bash
streamlit run app.py
```

The app will be available at `http://localhost:8501` in your web browser.

## 🔧 Configuration

### AI Engine Options

- **OpenAI**: Uses OpenAI's powerful language models (requires API key)
- **Local (Ollama)**: Uses locally hosted models through Ollama (requires Ollama installation)

### Search Options

- **Google Search**: Toggle on/off to enable web search capabilities
- Requires valid Google API key and CSE ID in your `.env` file

### Visual Themes

- **Quantum Blue**: Futuristic blue theme with quantum wave patterns
- **Matrix Green**: Classic hacker aesthetic with green highlights
- **Classic**: Clean professional interface with purple accents

## 📚 Usage Guide

1. **Select your AI Engine**: Choose between OpenAI or Local (Ollama) in the sidebar
2. **Configure Search**: Toggle Google Search on/off based on your needs
3. **Choose Theme**: Select your preferred visual style
4. **Ask Questions**: Type your research queries in the chat input field
5. **View Responses**: AI responses appear in the chat with search-enhanced information when available
6. **Clear Chat**: Use the "Clear Conversation" button to start fresh

## 🔗 API Keys Setup

### OpenAI API

1. Visit [OpenAI API Keys](https://platform.openai.com/account/api-keys)
2. Create a new API key
3. Add to your `.env` file as `OPENAI_API_KEY`

### Google Search API

1. Create a [Google Programmable Search Engine](https://programmablesearchengine.google.com/about/)
2. Get your Search Engine ID (cx)
3. Set up a [Google API Key with Custom Search API enabled](https://developers.google.com/custom-search/v1/overview)
4. Add both to your `.env` file as `GOOGLE_CSE_ID` and `GOOGLE_API_KEY`

## 💻 Local Development

### Installing Ollama (Optional)

For local model support:

1. Download Ollama from [ollama.ai](https://ollama.ai)
2. Install and follow setup instructions
3. Pull models with `ollama pull gemma3:4b` (or other models of your choice)

### Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- Built with [Streamlit](https://streamlit.io/)
- Powered by [LangChain](https://www.langchain.com/)
- AI functionality through [OpenAI](https://openai.com/) or [Ollama](https://ollama.ai/)

---

<p align="center">
  Made with ❤️ for the advancement of quantum-inspired research tools
</p>