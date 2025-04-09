# Research Assistant with clean output
from langchain_google_community import GoogleSearchAPIWrapper
from langchain_openai import ChatOpenAI
from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain.memory import ConversationBufferWindowMemory
import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Initialize the LLM silently
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")

try:
    # Set up the Google Search API tool
    search = GoogleSearchAPIWrapper()
    tools = [
        Tool(
            name="Google Search",
            description="Search Google for recent information on a topic",
            func=search.run
        )
    ]

    # Define the agent's prompt template
    template = """You are a research assistant. Your goal is to help users find information and answer their questions.
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
    
    Begin! Remember to provide as much detailed and elaorated and accurate information to the user, and cite your sources when possible.
    
    Question: {input}
    {agent_scratchpad}
    """
    
    # Create a proper PromptTemplate
    prompt = PromptTemplate.from_template(template)
    
    # Set up the memory with a window size
    memory = ConversationBufferWindowMemory(memory_key="chat_history", k=5, return_messages=True)
    
    # Create the agent with verbose=False to suppress intermediate output
    agent = create_react_agent(llm, tools, prompt)
    agent_executor = AgentExecutor.from_agent_and_tools(
        agent=agent, 
        tools=tools, 
        memory=memory,
        verbose=False,  # Set to False to suppress intermediate output
        handle_parsing_errors=True
    )

    # Run the agent
    def research_assistant(query):
        try:
            response = agent_executor.invoke({"input": query})
            return response.get("output", "No response generated.")
        except Exception as e:
            return f"An error occurred: {str(e)}"

    # Example usage
    if __name__ == "__main__":        
        while True:
            # Get user input
            query = input("""
Research Assistant from google
---------------------------------------------------------------
Enter your question: (type 'exit' to quit): """)
            
            if query.lower() in ["exit", "quit", "bye"]:
                break
                
            # Run the research assistant and only print the final result
            result = research_assistant(query)
            print('\n\nLLM Output :: \n\n',result)

except Exception as e:
    print(f"Setup error: {str(e)}")