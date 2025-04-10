import streamlit as st
import os
from dotenv import load_dotenv

# Import component modules
from components import UI, SidebarUI, ThemeManager
from utils import OllamaManager, MemoryManager, get_ollama_class
from assistant import LLMFactory, ResearchAgent, SearchTools

# Load environment variables
load_dotenv()

def main():
    # Initialize application
    initialize_app()
    
    # Setup page
    UI.setup_page_config()
    UI.apply_base_styling()
    UI.render_header()
    
    # Initialize Ollama management and get class information
    ollama_manager = OllamaManager()
    OLLAMA_CLASS, OLLAMA_AVAILABLE = get_ollama_class()
    
    # Render sidebar and get provider selection
    llm_provider = SidebarUI.render_sidebar(ollama_manager)
    
    # Apply selected theme
    ThemeManager.apply_theme(st.session_state.app_theme)
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    query = st.chat_input("Ask a research question...")
    
    if query:
        process_query(query, llm_provider, OLLAMA_CLASS, OLLAMA_AVAILABLE)
    
    # Render footer
    UI.render_footer()

def initialize_app():
    """Initialize application state variables"""
    # Initialize theme
    ThemeManager.initialize_theme()
    
    # Initialize messages if not present
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Initialize memory if not present
    if "memory" not in st.session_state:
        st.session_state.memory = MemoryManager.initialize_memory()
    
    # Initialize Google Search toggle if not present
    if "google_search_enabled" not in st.session_state:
        st.session_state.google_search_enabled = True

def process_query(query, llm_provider, OLLAMA_CLASS, OLLAMA_AVAILABLE):
    """Process a user query and generate a response"""
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": query})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(query)
    
    # Display assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # Determine appropriate loading message
        search_enabled = SearchTools.is_search_enabled()
        has_search_keys = SearchTools.has_search_keys()
        
        if search_enabled and has_search_keys:
            loading_message = "Searching..."
        elif llm_provider == "OpenAI":
            loading_message = "Generating with OpenAI..."
        else:
            loading_message = "Generating with local model..."
        
        # Show the appropriate loading message and generate response
        with st.spinner(loading_message):
            result = generate_response(query, llm_provider, OLLAMA_CLASS, OLLAMA_AVAILABLE)
        
        # Update the message placeholder with the result
        message_placeholder.markdown(result)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": result})
        
        # Update memory with this interaction
        st.session_state.memory.chat_memory.add_user_message(query)
        st.session_state.memory.chat_memory.add_ai_message(result)

def generate_response(query, llm_provider, OLLAMA_CLASS, OLLAMA_AVAILABLE):
    """Generate a response to the user's query"""
    # Get search tools
    tools = SearchTools.get_search_tools()
    
    # Create LLM
    llm = LLMFactory.create_llm(llm_provider, OLLAMA_CLASS, OLLAMA_AVAILABLE)
    
    if llm:
        # Convert chat history to the format needed by LLM
        chat_history = MemoryManager.format_chat_history(st.session_state.messages)
        
        # Create agent if search is enabled and tools are available
        if SearchTools.is_search_enabled() and tools:
            model = ResearchAgent.create_agent(llm, tools, st.session_state.memory)
            return ResearchAgent.run_query(model, query)
        else:
            # Use LLM directly if no search or tools
            return ResearchAgent.run_query(llm, query, chat_history)
    else:
        # Handle error cases
        if llm_provider == "OpenAI" and not os.getenv("OPENAI_API_KEY"):
            return "Please provide your OpenAI API key in the sidebar."
        elif llm_provider == "Local (Ollama)" and not OllamaManager.is_ollama_running():
            return "Ollama server is not running. Please start it using the button in the sidebar."
        else:
            return "Setup failed. Please check your configuration."

if __name__ == "__main__":
    main()