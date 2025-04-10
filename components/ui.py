import streamlit as st
import os
from .themes import ThemeManager
from utils.memory_utils import MemoryManager

class UI:
    """UI component management for the application"""
    
    @staticmethod
    def setup_page_config():
        """Set up initial page configuration"""
        st.set_page_config(
            page_title="⚛️ Quantum Research Assistant",
            page_icon="⚛️",
            layout="wide"
        )
    
    @staticmethod
    def apply_base_styling():
        """Apply base styling to the application"""
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
    
    @staticmethod
    def render_header():
        """Render the application header"""
        st.title("⚛️ Quantum Research Assistant", anchor=False)
        st.markdown("<div style='text-align: center; margin-top: -15px; margin-bottom: 30px;'><em>Explore the universe of knowledge with quantum-powered search</em></div>", unsafe_allow_html=True)
    
    @staticmethod
    def render_footer():
        """Render the application footer"""
        st.markdown("""
        ---
        <div style="text-align: center; color: #4b96ff; font-size: 0.8em;">
            Powered by artificial intelligence
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_sidebar_logo():
        """Render the logo in the sidebar"""
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
    
    @staticmethod
    def style_toggle_switch(theme_color):
        """Style the toggle switch based on the current theme color"""
        st.markdown(f"""
        <style>
            /* Style the toggle switch based on theme */
            .stToggle > div > div:hover {{
                color: {theme_color} !important;
            }}
            .stToggle > div[data-baseweb="toggle"] > div {{
                background-color: {theme_color} !important;
            }}
            .stToggle > div[data-baseweb="toggle"] > div > div:last-child {{
                background-color: white !important;
            }}
        </style>
        """, unsafe_allow_html=True)

class SidebarUI:
    """Manages the sidebar UI components"""
    
    @staticmethod
    def render_sidebar(ollama_manager):
        """Render the complete sidebar with all components"""
        with st.sidebar:
            UI.render_sidebar_logo()
            st.title("⚙️ Configuration")
            
            # LLM provider selection
            llm_provider = st.selectbox(
                "Select AI Engine",
                options=["OpenAI", "Local (Ollama)"],
                index=0
            )
            
            # Connection status expander
            SidebarUI.render_connection_status(llm_provider, ollama_manager)
            
            # Search capability expander
            SidebarUI.render_search_capability()
            
            # Theme selector
            SidebarUI.render_theme_selector()
            
            # Clear conversation button at the bottom of sidebar
            if st.button("Clear Conversation", key="clear_chat"):
                st.session_state.messages = []
                st.session_state.memory = MemoryManager.initialize_memory()
                st.rerun()
                
        return llm_provider
    
    @staticmethod
    def render_connection_status(llm_provider, ollama_manager):
        """Render the connection status expander"""
        with st.expander("Connection Status"):
            if llm_provider == "OpenAI":
                api_key_status = "Connected" if os.getenv("OPENAI_API_KEY") else "Not Connected"
                st.info(f"OpenAI API: {api_key_status}")
                
                if not os.getenv("OPENAI_API_KEY"):
                    st.text_input("Enter OpenAI API Key", type="password", key="openai_api_key", 
                                on_change=lambda: os.environ.update({"OPENAI_API_KEY": st.session_state.openai_api_key}))
            else:
                ollama_status = "Running" if ollama_manager.is_ollama_running() else "Not Running"
                st.info(f"Ollama Server: {ollama_status}")
                
                # Import the function directly from utils
                from utils.ollama_utils import get_ollama_class
                OLLAMA_CLASS, OLLAMA_AVAILABLE = get_ollama_class()
                
                if not ollama_manager.is_ollama_running() and OLLAMA_AVAILABLE:
                    if st.button("Start Ollama Server"):
                        with st.spinner("Starting Ollama server..."):
                            if ollama_manager.start_ollama_server():
                                st.success("Ollama server started successfully!")
                                st.rerun()
                            else:
                                st.error("Failed to start server. Please start it manually.")
                elif not OLLAMA_AVAILABLE:
                    st.error("Ollama integration not available")
                    st.markdown("Install with: `pip install -U langchain_ollama`")
    
    @staticmethod
    def render_search_capability():
        """Render the search capability expander"""
        with st.expander("Search Capability"):
            google_api_key = os.getenv("GOOGLE_API_KEY") and os.getenv("GOOGLE_CSE_ID")
            api_status = "Available" if google_api_key else "Not Available"
            st.info(f"Google Search API: {api_status}")
            
            # Get theme color
            theme_color = ThemeManager.get_theme_color(st.session_state.app_theme)
            
            # Apply custom CSS to style the toggle switch based on theme
            UI.style_toggle_switch(theme_color)
            
            # Initialize search state if not present
            if "google_search_enabled" not in st.session_state:
                st.session_state.google_search_enabled = True
            
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
    
    @staticmethod
    def render_theme_selector():
        """Render the theme selector"""
        selected_theme = st.selectbox(
            "Theme", 
            ThemeManager.THEMES,
            index=ThemeManager.THEMES.index(st.session_state.app_theme)
        )
        
        # Update theme in session state if changed
        if selected_theme != st.session_state.app_theme:
            st.session_state.app_theme = selected_theme
            st.rerun()