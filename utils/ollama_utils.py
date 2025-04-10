import subprocess
import time
import requests
import platform

class OllamaManager:
    """Utility class to manage Ollama server operations"""
    
    @staticmethod
    def is_ollama_running():
        """Check if Ollama server is running"""
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    @staticmethod
    def start_ollama_server():
        """Start Ollama server"""
        try:
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
                if OllamaManager.is_ollama_running():
                    return True
                time.sleep(1)
            return OllamaManager.is_ollama_running()
        except Exception:
            return False

# Define Ollama class dynamic import
def get_ollama_class():
    """Dynamically import and return the appropriate Ollama class"""
    try:
        from langchain_ollama.chat_models import ChatOllama
        return ChatOllama, True
    except ImportError:
        try:
            from langchain_ollama import Chat as ChatOllama
            return ChatOllama, True
        except ImportError:
            return None, False