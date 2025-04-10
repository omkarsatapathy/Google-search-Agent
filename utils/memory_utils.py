from langchain.memory import ConversationBufferWindowMemory
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

class MemoryManager:
    """Memory management utilities for conversation history"""
    
    @staticmethod
    def initialize_memory():
        """Initialize a new memory instance"""
        return ConversationBufferWindowMemory(memory_key="chat_history", k=5, return_messages=True)
    
    @staticmethod
    def format_chat_history(messages, max_pairs=5):
        """Convert chat history from session state to langchain messages format
        
        Args:
            messages: List of message dictionaries from session state
            max_pairs: Maximum number of message pairs to include
            
        Returns:
            List of langchain message objects
        """
        # Extract message pairs
        message_pairs = []
        for i in range(0, len(messages)-1, 2):
            if i+1 < len(messages):
                message_pairs.append((messages[i], messages[i+1]))
        
        # Take the most recent pairs
        chat_history = []
        for user_msg, ai_msg in message_pairs[-max_pairs:]:
            chat_history.append(HumanMessage(content=user_msg["content"]))
            chat_history.append(AIMessage(content=ai_msg["content"]))
            
        return chat_history
    
    @staticmethod
    def create_message_sequence(system_content, chat_history, query):
        """Create a full message sequence including system message, history, and query
        
        Args:
            system_content: Content for the system message
            chat_history: Formatted chat history from format_chat_history
            query: Current user query
            
        Returns:
            List of messages ready for LLM invocation
        """
        messages = [SystemMessage(content=system_content)]
        messages.extend(chat_history)
        messages.append(HumanMessage(content=query))
        return messages