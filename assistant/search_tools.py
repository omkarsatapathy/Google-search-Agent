import os
from langchain_google_community import GoogleSearchAPIWrapper
from langchain.agents import Tool

class SearchTools:
    """Manages search tools for the research assistant"""
    
    @staticmethod
    def get_search_tools():
        """Get search tools if enabled and available
        
        Returns:
            List of tools or empty list if search is not available
        """
        # Only create search tools if search is enabled and API keys are available
        if (os.getenv("GOOGLE_API_KEY") and 
            os.getenv("GOOGLE_CSE_ID") and 
            SearchTools.is_search_enabled()):
            
            search = GoogleSearchAPIWrapper()
            return [
                Tool(
                    name="Google Search",
                    description="Search Google for recent information on a topic",
                    func=search.run
                )
            ]
        return []
    
    @staticmethod
    def is_search_enabled():
        """Check if search functionality is enabled in session state
        
        Returns:
            Boolean indicating if search is enabled
        """
        import streamlit as st
        return st.session_state.get("google_search_enabled", True)
    
    @staticmethod
    def has_search_keys():
        """Check if Google Search API keys are available
        
        Returns:
            Boolean indicating if API keys are available
        """
        return bool(os.getenv("GOOGLE_API_KEY") and os.getenv("GOOGLE_CSE_ID"))