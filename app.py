import streamlit as st
import os
import subprocess
import time
import requests
from dotenv import load_dotenv
from langchain_google_community import GoogleSearchAPIWrapper
from langchain_openai import ChatOpenAI
from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain.memory import ConversationBufferWindowMemory

# Load environment variables
load_dotenv()

# Function to check if Ollama server is running
def is_ollama_running():
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        return response.status_code == 200
    except:
        return False

# Function to start Ollama server
def start_ollama_server():
    try:
        import platform
        system = platform.system()
        
        if system == "Windows":
            process = subprocess.Popen(["ollama", "serve"], 
                          stdout=subprocess.PIPE, 
                          stderr=subprocess.PIPE,
                          shell=True)
        else:  # macOS or Linux
            process = subprocess.Popen(["ollama", "serve"], 
                          stdout=subprocess.PIPE, 
                          stderr=subprocess.PIPE)
        
        # Wait for server to start
        for i in range(10):
            if is_ollama_running():
                return True
            time.sleep(1)
        return is_ollama_running()
    except Exception:
        return False

# Define Ollama class dynamic import
try:
    from langchain_ollama.chat_models import ChatOllama
    OLLAMA_CLASS = ChatOllama
    OLLAMA_AVAILABLE = True
except ImportError:
    try:
        from langchain_ollama import Chat as ChatOllama
        OLLAMA_CLASS = ChatOllama
        OLLAMA_AVAILABLE = True
    except ImportError:
        OLLAMA_AVAILABLE = False

# Set up the page configuration with custom theme
st.set_page_config(
    page_title="⚛️ Quantum Research Assistant",
    page_icon="⚛️",
    layout="wide"
)

# Custom CSS for math-themed styling
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
        background-image: linear-gradient(rgba(14, 17, 23, 0.8), rgba(14, 17, 23, 0.8)), 
                          url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M10 10L20 20M30 30L40 40M50 50L60 60M70 70L80 80M90 90L95 95' stroke='%233b82f640' stroke-width='1'/%3E%3Cpath d='M20 10L10 20M40 30L30 40M60 50L50 60M80 70L70 80M95 90L90 95' stroke='%233b82f640' stroke-width='1'/%3E%3Cpath d='M30 10C40 20,45 25,50 30' stroke='%234b96ff40' stroke-width='1' fill='none'/%3E%3C/svg%3E");
        color: white !important;
    }
    body {
        background-color: #0e1117;
        color: white;
    }
    .stApp {
        background: none;
    }
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    h1, h2, h3 {
        color: #4b96ff !important;
        font-family: 'Courier New', Courier, monospace;
        text-shadow: 0 0 5px rgba(75, 150, 255, 0.3);
    }
    .stButton>button {
        background-color: #3b82f6;
        color: white;
        border-radius: 8px;
    }
    .stButton>button:hover {
        background-color: #1e40af;
    }
    .stChat {
        border-radius: 12px;
        border: 1px solid #e0e7ff;
    }
    .css-1oe6o3n {
        background-color: #dbeafe;
    }
    .css-1e5imcs {
        background-color: #eff6ff;
    }
    .stSidebar {
        background-color: #0e1117 !important;
        background-image: linear-gradient(rgba(14, 17, 23, 0.95), rgba(14, 17, 23, 0.95)), 
                          url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M10 10L20 20M30 30L40 40M50 50L60 60M70 70L80 80M90 90L95 95' stroke='%233b82f680' stroke-width='1'/%3E%3Cpath d='M20 10L10 20M40 30L30 40M60 50L50 60M80 70L70 80M95 90L90 95' stroke='%233b82f680' stroke-width='1'/%3E%3Cpath d='M30 10C40 20,45 25,50 30' stroke='%234b96ff50' stroke-width='1' fill='none'/%3E%3C/svg%3E");
        color: white !important;
    }
    .stSidebar [data-testid="stMarkdown"] {
        color: white !important;
    }
    .stSidebar h1, .stSidebar h2, .stSidebar h3, .stSidebar .stExpander {
        color: #4b96ff !important;
    }
    .stSidebar .stButton > button {
        background-color: #4b96ff;
        color: white;
    }
    .stSidebar .stSelectbox > div > div {
        background-color: #1e293b;
        color: white;
        border-color: #3b82f6;
    }
    /* Quantum wave patterns across the entire page */
    .quantum-waves {
        position: fixed;
        top: 0;
        left: 0;
        width: calc(100% + 50px);
        height: 100%;
        pointer-events: none;
        z-index: -1;
        background-image: 
            url("data:image/svg+xml,%3Csvg width='100%25' height='100%25' xmlns='http://www.w3.org/2000/svg'%3E%3Cdefs%3E%3ClinearGradient id='grad' x1='0%25' y1='0%25' x2='100%25' y2='0%25'%3E%3Cstop offset='0%25' style='stop-color:%234b96ff;stop-opacity:0.4' /%3E%3Cstop offset='100%25' style='stop-color:%233b82f6;stop-opacity:0.1' /%3E%3C/linearGradient%3E%3C/defs%3E%3Cpath d='M-50 80 Q -25 60, 0 80 T 50 80 T 100 80 T 150 80 T 200 80 T 250 80' stroke='url(%23grad)' stroke-width='1' fill='none' opacity='0.3' /%3E%3Cpath d='M-50 120 Q -25 100, 0 120 T 50 120 T 100 120 T 150 120 T 200 120 T 250 120' stroke='url(%23grad)' stroke-width='1' fill='none' opacity='0.2' /%3E%3Cpath d='M-50 160 Q -25 140, 0 160 T 50 160 T 100 160 T 150 160 T 200 160 T 250 160' stroke='url(%23grad)' stroke-width='1' fill='none' opacity='0.1' /%3E%3C/svg%3E"),
            url("data:image/svg+xml,%3Csvg width='100%25' height='100%25' xmlns='http://www.w3.org/2000/svg'%3E%3Cdefs%3E%3ClinearGradient id='grad2' x1='0%25' y1='0%25' x2='100%25' y2='0%25'%3E%3Cstop offset='0%25' style='stop-color:%234b96ff;stop-opacity:0.3' /%3E%3Cstop offset='100%25' style='stop-color:%233b82f6;stop-opacity:0.1' /%3E%3C/defs%3E%3Cpath d='M-50 40 Q 0 0, 50 40 T 150 40 T 250 40 T 350 40' stroke='url(%23grad2)' stroke-width='1' fill='none' opacity='0.2' /%3E%3Cpath d='M-50 200 Q 0 160, 50 200 T 150 200 T 250 200 T 350 200' stroke='url(%23grad2)' stroke-width='1' fill='none' opacity='0.2' /%3E%3C/svg%3E");
        background-size: 100% 100%, 100% 100%;
        animation: wave-animation 20s linear infinite;
        margin-left: -50px;
    }
    
    @keyframes wave-animation {
        0% { background-position: 0% 0%, 0% 0%; }
        100% { background-position: 100% 0%, -100% 0%; }
    }
    
    /* Quantum particles effect */
    .quantum-particles {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -1;
        background-image: radial-gradient(circle at 10% 20%, rgba(75, 150, 255, 0.1) 0%, transparent 10%),
                          radial-gradient(circle at 30% 70%, rgba(75, 150, 255, 0.1) 0%, transparent 10%),
                          radial-gradient(circle at 60% 30%, rgba(75, 150, 255, 0.1) 0%, transparent 10%),
                          radial-gradient(circle at 80% 80%, rgba(75, 150, 255, 0.1) 0%, transparent 10%),
                          radial-gradient(circle at 90% 10%, rgba(75, 150, 255, 0.1) 0%, transparent 10%);
    }
</style>
<div class="quantum-waves"></div>
<div class="quantum-particles"></div>
""", unsafe_allow_html=True)

# Set up Streamlit app
st.title("⚛️ Quantum Research Assistant", anchor=False)
st.markdown("<div style='text-align: center; margin-top: -15px; margin-bottom: 30px;'><em>Explore the universe of knowledge with quantum-powered search</em></div>", unsafe_allow_html=True)

# Initialize session states
if "google_search_enabled" not in st.session_state:
    st.session_state.google_search_enabled = True

if "app_theme" not in st.session_state:
    st.session_state.app_theme = "Quantum Blue"

# Sidebar for model selection
with st.sidebar:
    st.markdown("""
    <div style="display: flex; justify-content: center; margin-bottom: 10px;">
        <svg width="160" height="80" viewBox="0 0 160 80" xmlns="http://www.w3.org/2000/svg">
            <path d="M0 40 C 20 10, 35 10, 40 40 S 60 70, 80 40 S 100 10, 120 40 S 140 70, 160 40" 
                  stroke="#4b96ff" stroke-width="2" fill="none" />
            <circle cx="40" cy="40" r="3" fill="#4b96ff" />
            <circle cx="80" cy="40" r="3" fill="#4b96ff" />
            <circle cx="120" cy="40" r="3" fill="#4b96ff" />
            <text x="80" y="75" text-anchor="middle" fill="#4b96ff" font-family="monospace" font-size="10">QUANTUM WAVES</text>
        </svg>
    </div>
    """, unsafe_allow_html=True)
    st.title("⚙️ Settings")
    
    # LLM provider selection
    llm_provider = st.selectbox(
        "Select AI Engine",
        options=["OpenAI", "Local (Ollama)"],
        index=0
    )
    
    # Display model-specific information in a cleaner way
    with st.expander("Connection Status"):
        if llm_provider == "OpenAI":
            api_key_status = "Connected" if os.getenv("OPENAI_API_KEY") else "Not Connected"
            st.info(f"OpenAI API: {api_key_status}")
            
            if not os.getenv("OPENAI_API_KEY"):
                st.text_input("Enter OpenAI API Key", type="password", key="openai_api_key", 
                            on_change=lambda: os.environ.update({"OPENAI_API_KEY": st.session_state.openai_api_key}))
        else:
            ollama_status = "Running" if is_ollama_running() else "Not Running"
            st.info(f"Ollama Server: {ollama_status}")
            
            if not is_ollama_running() and OLLAMA_AVAILABLE:
                if st.button("Start Ollama Server"):
                    with st.spinner("Starting Ollama server..."):
                        if start_ollama_server():
                            st.success("Ollama server started successfully!")
                            st.rerun()
                        else:
                            st.error("Failed to start server. Please start it manually.")
            elif not OLLAMA_AVAILABLE:
                st.error("Ollama integration not available")
                st.markdown("Install with: `pip install -U langchain_ollama`")
    
    # Google API key status in expander 
    with st.expander("Search Capability"):
        google_api_key = os.getenv("GOOGLE_API_KEY") and os.getenv("GOOGLE_CSE_ID")
        api_status = "Available" if google_api_key else "Not Available"
        st.info(f"Google Search: {api_status}")
        
        # Define theme-based color for styling
        toggle_theme_color = "#3b82f6"  # Default Quantum Blue
        if st.session_state.app_theme == "Matrix Green":
            toggle_theme_color = "#00cc00"
        elif st.session_state.app_theme == "Classic":
            toggle_theme_color = "#A9A9A9"
        
        # Apply custom CSS to style the toggle switch based on theme
        st.markdown(f"""
        <style>
            /* Style the toggle switch based on theme */
            .stToggle > div > div:hover {{
                color: {toggle_theme_color} !important;
            }}
            .stToggle > div[data-baseweb="toggle"] > div {{
                background-color: {toggle_theme_color} !important;
            }}
            .stToggle > div[data-baseweb="toggle"] > div > div:last-child {{
                background-color: white !important;
            }}
        </style>
        """, unsafe_allow_html=True)
        
        # Create a container for the toggle with the custom class
        toggle_container = st.container()
        
        # Add the "stToggle" class to apply our custom styling
        with toggle_container:
            st.markdown('<div class="stToggle">', unsafe_allow_html=True)
            google_search_enabled = st.toggle("Enable Google Search", 
                                          value=st.session_state.google_search_enabled,
                                          help="Toggle to enable or disable Google Search functionality")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Update session state if toggle changes
        if google_search_enabled != st.session_state.google_search_enabled:
            st.session_state.google_search_enabled = google_search_enabled
            st.rerun()
        
        # Show appropriate status message
        if not st.session_state.google_search_enabled:
            st.warning("Google Search is disabled. The assistant will rely only on its knowledge.")
        elif not google_api_key:
            st.error("Google Search is enabled but API keys are missing.")
        else:
            st.success("Google Search is enabled and ready to use.")
    
    # Add theme selector
    selected_theme = st.selectbox(
        "Theme", 
        ["Quantum Blue", "Matrix Green", "Classic"],
        index=0
    )
    
    # Update theme in session state if changed
    if selected_theme != st.session_state.app_theme:
        st.session_state.app_theme = selected_theme
        st.rerun()
    
    # Apply selected theme
    if st.session_state.app_theme == "Matrix Green":
        st.markdown("""
        <style>
            .main { background-color: #0a190a !important; }
            h1, h2, h3 { color: #00cc00 !important; text-shadow: 0 0 5px rgba(0, 204, 0, 0.5); }
            .stButton>button { background-color: #00cc00 !important; }
            .stButton>button:hover { background-color: #009900 !important; }
            .quantum-waves {
                background-image: 
                    url("data:image/svg+xml,%3Csvg width='100%25' height='100%25' xmlns='http://www.w3.org/2000/svg'%3E%3Cdefs%3E%3ClinearGradient id='grad' x1='0%25' y1='0%25' x2='100%25' y2='0%25'%3E%3Cstop offset='0%25' style='stop-color:%2300cc00;stop-opacity:0.4' /%3E%3Cstop offset='100%25' style='stop-color:%23009900;stop-opacity:0.1' /%3E%3C/linearGradient%3E%3C/defs%3E%3Cpath d='M-50 80 Q -25 60, 0 80 T 50 80 T 100 80 T 150 80 T 200 80 T 250 80' stroke='url(%23grad)' stroke-width='1' fill='none' opacity='0.3' /%3E%3Cpath d='M-50 120 Q -25 100, 0 120 T 50 120 T 100 120 T 150 120 T 200 120 T 250 120' stroke='url(%23grad)' stroke-width='1' fill='none' opacity='0.2' /%3E%3Cpath d='M-50 160 Q -25 140, 0 160 T 50 160 T 100 160 T 150 160 T 200 160 T 250 160' stroke='url(%23grad)' stroke-width='1' fill='none' opacity='0.1' /%3E%3C/svg%3E"),
                    url("data:image/svg+xml,%3Csvg width='100%25' height='100%25' xmlns='http://www.w3.org/2000/svg'%3E%3Cdefs%3E%3ClinearGradient id='grad2' x1='0%25' y1='0%25' x2='100%25' y2='0%25'%3E%3Cstop offset='0%25' style='stop-color:%2300cc00;stop-opacity:0.3' /%3E%3Cstop offset='100%25' style='stop-color:%23009900;stop-opacity:0.1' /%3E%3C/defs%3E%3Cpath d='M-50 40 Q 0 0, 50 40 T 150 40 T 250 40 T 350 40' stroke='url(%23grad2)' stroke-width='1' fill='none' opacity='0.2' /%3E%3Cpath d='M-50 200 Q 0 160, 50 200 T 150 200 T 250 200 T 350 200' stroke='url(%23grad2)' stroke-width='1' fill='none' opacity='0.2' /%3E%3C/svg%3E") !important;
            }
            .quantum-particles {
                background-image: radial-gradient(circle at 10% 20%, rgba(0, 204, 0, 0.1) 0%, transparent 10%),
                                radial-gradient(circle at 30% 70%, rgba(0, 204, 0, 0.1) 0%, transparent 10%),
                                radial-gradient(circle at 60% 30%, rgba(0, 204, 0, 0.1) 0%, transparent 10%),
                                radial-gradient(circle at 80% 80%, rgba(0, 204, 0, 0.1) 0%, transparent 10%),
                                radial-gradient(circle at 90% 10%, rgba(0, 204, 0, 0.1) 0%, transparent 10%) !important;
            }
            .stSidebar [data-testid="stMarkdown"] svg path { stroke: #00cc00 !important; }
            .stSidebar [data-testid="stMarkdown"] svg text { fill: #00cc00 !important; }
            .stSidebar [data-testid="stMarkdown"] { color: #00cc00 !important; }
            .stSidebar h1, .stSidebar h2, .stSidebar h3, .stSidebar .stExpander { color: #00cc00 !important; }
            .stSidebar .stButton > button { background-color: #00cc00 !important; }
        </style>
        """, unsafe_allow_html=True)
    elif st.session_state.app_theme == "Classic":
        st.markdown("""
        <style>
            .main { background-color: #252a34 !important; }
            h1, h2, h3 { color: #ffffff !important; text-shadow: none; font-family: sans-serif; }
            .stButton>button { background-color: #A9A9A9 !important; }
            .stButton>button:hover { background-color: #3949ab !important; }
            .quantum-waves {
                background-image: 
                    url("data:image/svg+xml,%3Csvg width='100%25' height='100%25' xmlns='http://www.w3.org/2000/svg'%3E%3Cdefs%3E%3ClinearGradient id='grad' x1='0%25' y1='0%25' x2='100%25' y2='0%25'%3E%3Cstop offset='0%25' style='stop-color:%23757de8;stop-opacity:0.4' /%3E%3Cstop offset='100%25' style='stop-color:%233949ab;stop-opacity:0.1' /%3E%3C/linearGradient%3E%3C/defs%3E%3Cpath d='M-50 80 Q -25 60, 0 80 T 50 80 T 100 80 T 150 80 T 200 80 T 250 80' stroke='url(%23grad)' stroke-width='1' fill='none' opacity='0.3' /%3E%3Cpath d='M-50 120 Q -25 100, 0 120 T 50 120 T 100 120 T 150 120 T 200 120 T 250 120' stroke='url(%23grad)' stroke-width='1' fill='none' opacity='0.2' /%3E%3Cpath d='M-50 160 Q -25 140, 0 160 T 50 160 T 100 160 T 150 160 T 200 160 T 250 160' stroke='url(%23grad)' stroke-width='1' fill='none' opacity='0.1' /%3E%3C/svg%3E"),
                    url("data:image/svg+xml,%3Csvg width='100%25' height='100%25' xmlns='http://www.w3.org/2000/svg'%3E%3Cdefs%3E%3ClinearGradient id='grad2' x1='0%25' y1='0%25' x2='100%25' y2='0%25'%3E%3Cstop offset='0%25' style='stop-color:%23757de8;stop-opacity:0.3' /%3E%3Cstop offset='100%25' style='stop-color:%233949ab;stop-opacity:0.1' /%3E%3C/defs%3E%3Cpath d='M-50 40 Q 0 0, 50 40 T 150 40 T 250 40 T 350 40' stroke='url(%23grad2)' stroke-width='1' fill='none' opacity='0.2' /%3E%3Cpath d='M-50 200 Q 0 160, 50 200 T 150 200 T 250 200 T 350 200' stroke='url(%23grad2)' stroke-width='1' fill='none' opacity='0.2' /%3E%3C/svg%3E") !important;
            }
            .quantum-particles {
                background-image: radial-gradient(circle at 10% 20%, rgba(117, 125, 232, 0.1) 0%, transparent 10%),
                                radial-gradient(circle at 30% 70%, rgba(117, 125, 232, 0.1) 0%, transparent 10%),
                                radial-gradient(circle at 60% 30%, rgba(117, 125, 232, 0.1) 0%, transparent 10%),
                                radial-gradient(circle at 80% 80%, rgba(117, 125, 232, 0.1) 0%, transparent 10%),
                                radial-gradient(circle at 90% 10%, rgba(117, 125, 232, 0.1) 0%, transparent 10%) !important;
            }
            .stSidebar [data-testid="stMarkdown"] svg path { stroke: #757de8 !important; }
            .stSidebar [data-testid="stMarkdown"] svg text { fill: #757de8 !important; }
            .stSidebar [data-testid="stMarkdown"] { color: #ffffff !important; }
            .stSidebar h1, .stSidebar h2, .stSidebar h3, .stSidebar .stExpander { color: #757de8 !important; }
            .stSidebar .stButton > button { background-color: #A9A9A9 !important; }
        </style>
        """, unsafe_allow_html=True)
    
    # Clear conversation button at the bottom of sidebar
    if st.button("Clear Conversation", key="clear_chat"):
        st.session_state.messages = []
        st.rerun()

# Initialize the research assistant function
def setup_research_assistant(llm_choice):
    # Set up the Google Search API tool
    tools = []
    
    # Only add Google Search tool if enabled in the UI and API keys are available
    if (os.getenv("GOOGLE_API_KEY") and os.getenv("GOOGLE_CSE_ID") and 
            st.session_state.get("google_search_enabled", True)):
        search = GoogleSearchAPIWrapper()
        tools = [
            Tool(
                name="Google Search",
                description="Search Google for recent information on a topic",
                func=search.run
            )
        ]
    
    # Choose LLM based on selection
    if llm_choice == "OpenAI":
        if not os.getenv("OPENAI_API_KEY"):
            return None
        llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
    else:  # Local (Ollama)
        if not OLLAMA_AVAILABLE or not is_ollama_running():
            return None
        
        try:
            llm = OLLAMA_CLASS(model="gemma3:4b")
        except Exception:
            return None
    
    # Define the agent's prompt template
    search_enabled = st.session_state.get("google_search_enabled", True)
    if search_enabled and len(tools) > 0:
        search_status = "You have access to Google Search. Use it to find the most up-to-date information."
        
        template = f"""You are a quantum research assistant with mathematics expertise. Your goal is to help users find information and answer their questions.
        {search_status}
        
        You have access to the following tools:
        {{tools}}
        
        Use the following format:
        Question: the input question you must answer
        Thought: you should always think about what to do
        Action: the action to take, should be one of [{{tool_names}}]
        Action Input: the input to the action
        Observation: the result of the action
        ... (this Thought/Action/Action Input/Observation can repeat N times)
        Thought: I now know the final answer
        Final Answer: the final answer to the original input question
        
        Begin! Provide detailed and accurate information to the user, and cite your sources when possible.
        
        Question: {{input}}
        {{agent_scratchpad}}
        """
        
        # Create prompt and memory
        prompt = PromptTemplate.from_template(template)
        memory = ConversationBufferWindowMemory(memory_key="chat_history", k=5, return_messages=True)
        
        # Create the agent
        agent = create_react_agent(llm, tools, prompt)
        agent_executor = AgentExecutor.from_agent_and_tools(
            agent=agent,
            tools=tools,
            memory=memory,
            verbose=False,
            handle_parsing_errors=True
        )
        
        return agent_executor
    else:
        # If search is disabled or no tools are available, just use the LLM directly
        return llm


# Function to run the research assistant query
def research_assistant(query, llm_choice):
    search_enabled = st.session_state.get("google_search_enabled", True)
    has_search_keys = os.getenv("GOOGLE_API_KEY") and os.getenv("GOOGLE_CSE_ID")
    
    # Dynamic loading message
    if search_enabled and has_search_keys:
        loading_message = "Searching the web and generating response..."
    else:
        loading_message = "Generating response from existing knowledge..."
    
    model = setup_research_assistant(llm_choice)
    
    if model:
        try:
            if isinstance(model, AgentExecutor):
                # This is the agent with tools
                response = model.invoke({"input": query})
                return response.get("output", "No response generated.")
            else:
                # This is just the LLM (when search is disabled)
                system_message = """You are a quantum research assistant with mathematics expertise. 
                You do NOT have access to Google Search, so use only your built-in knowledge to answer questions.
                Provide detailed and accurate information to the user."""
                
                response = model.invoke(f"System: {system_message}\n\nUser: {query}")
                return response.content
            
        except Exception as e:
            return f"An error occurred: {str(e)}"
    else:
        if llm_choice == "OpenAI" and not os.getenv("OPENAI_API_KEY"):
            return "Please provide your OpenAI API key in the sidebar."
        elif llm_choice == "Local (Ollama)" and not is_ollama_running():
            return "Ollama server is not running. Please start it using the button in the sidebar."
        else:
            return "Setup failed. Please check your configuration."

# Initialize session state variables if they don't exist
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history with enhanced styling
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
query = st.chat_input("Ask a research question...")

if query:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": query})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(query)
    
    # Display assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # Get dynamic loading message based on current state
        search_enabled = st.session_state.get("google_search_enabled", True)
        has_search_keys = os.getenv("GOOGLE_API_KEY") and os.getenv("GOOGLE_CSE_ID")
        
        if search_enabled and has_search_keys:
            loading_message = "Searching..."
        elif llm_provider == "OpenAI":
            loading_message = "Generating with OpenAI..."
        else:
            loading_message = "Generating with local model..."
        
        # Show the appropriate loading message
        with st.spinner(loading_message):
            result = research_assistant(query, llm_provider)
        
        # Update the message placeholder with the result
        message_placeholder.markdown(result)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": result})

# Add a footer
st.markdown("""
---
<div style="text-align: center; color: #4b96ff; font-size: 0.8em;">
    Powered by artificial intelligence
</div>
""", unsafe_allow_html=True)