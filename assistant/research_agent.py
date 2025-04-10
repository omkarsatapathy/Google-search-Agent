from langchain_core.prompts import PromptTemplate
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.messages import SystemMessage, HumanMessage

class ResearchAgent:
    """Manages the research agent functionality"""
    
    @staticmethod
    def create_agent(llm, tools, memory):
        """Create a research agent with the given LLM, tools, and memory
        
        Args:
            llm: The language model
            tools: List of tools available to the agent
            memory: Conversation memory
            
        Returns:
            AgentExecutor instance or None if tools aren't available
        """
        if len(tools) > 0:
            # Define the agent's prompt template with search status
            template = """You are a quantum research assistant with mathematics expertise. Your goal is to help users find information and answer their questions.
            You have access to Google Search. Use it to find the most up-to-date information.
            
            You have access to the following tools:
            {tools}
            
            Use the following format:
            Question: the input question you must answer
            Thought: you should always think about what to do
            Action: the action to take, should be one of [{tool_names}]
            Action Input: the input to the action
            Observation: the result of the action
            ... (this Thought/Action/Action Input/Observation can repeat N times)
            Thought: I now know the final answer
            Final Answer: the final answer to the original input question
            
            Begin! Provide detailed and accurate information to the user, and cite your sources when possible.
            
            Question: {input}
            {agent_scratchpad}
            """
            
            # Create prompt
            prompt = PromptTemplate.from_template(template)
            
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
        return None
    
    @staticmethod
    def run_query(model, query, chat_history=None):
        """Run a research query using either an agent or direct LLM
        
        Args:
            model: Either an AgentExecutor or LLM
            query: The user's query
            chat_history: Formatted chat history for LLM (not used for agent)
            
        Returns:
            Response text
        """
        try:
            if isinstance(model, AgentExecutor):
                # This is the agent with tools
                response = model.invoke({"input": query})
                return response.get("output", "No response generated.")
            else:
                # This is just the LLM (when search is disabled)
                # Create a system message
                system_message = """You are a quantum research assistant with mathematics expertise. 
                You do NOT have access to Google Search, so use only your built-in knowledge to answer questions.
                Provide detailed and accurate information to the user."""
                
                messages = [
                    SystemMessage(content=system_message)
                ]
                
                # Add conversation history if available
                if chat_history:
                    messages.extend(chat_history)
                
                # Add the current query
                messages.append(HumanMessage(content=query))
                
                # Get response from the LLM
                response = model.invoke(messages)
                
                return response.content
        except Exception as e:
            return f"An error occurred: {str(e)}"