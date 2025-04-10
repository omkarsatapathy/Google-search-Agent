import streamlit as st

class ThemeManager:
    """Manages application themes and styling"""
    
    THEMES = ["Quantum Blue", "Matrix Green", "Classic"]
    
    @staticmethod
    def initialize_theme():
        """Initialize theme in session state if not present"""
        if "app_theme" not in st.session_state:
            st.session_state.app_theme = "Quantum Blue"
    
    @staticmethod
    def get_theme_color(theme_name):
        """Get primary color for the given theme"""
        if theme_name == "Quantum Blue":
            return "#3b82f6"
        elif theme_name == "Matrix Green":
            return "#00cc00"
        else:  # Classic
            return "#A9A9A9"
    
    @staticmethod
    def apply_theme(theme_name):
        """Apply the selected theme CSS to the application"""
        if theme_name == "Matrix Green":
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
        elif theme_name == "Classic":
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