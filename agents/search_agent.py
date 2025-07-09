from langchain.agents import create_react_agent, AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import SystemMessage
from langchain_core.prompts import PromptTemplate
from typing import List, Dict, Any

class SearchAgent:
    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = tools
        self.memory = self._initialize_memory()
        self.agent = self._create_agent()
        self.executor = self._create_executor()

    def _initialize_memory(self) -> ConversationBufferMemory:
        """Initialize conversation memory with system message."""
        system_message = """You are an advanced research assistant with access to multiple sources of information.
        Your goal is to provide detailed, accurate, and up-to-date information on any topic asked by user."""
        
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        memory.chat_memory.add_message(SystemMessage(content=system_message))
        return memory

    def _create_agent(self):
        """Create the React agent with the specified prompt template."""
        template = '''Answer the following questions as best you can. You have access to the following tools:
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
        Begin!
        Question: {input}
        Thought:{agent_scratchpad}'''
        
        prompt = PromptTemplate.from_template(template)
        return create_react_agent(self.llm, self.tools, prompt)

    def _create_executor(self) -> AgentExecutor:
        """Create the agent executor."""
        return AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True,
            return_intermediate_steps=True,
            # memory=self.memory
        )

    def search(self, query: str) -> Dict[str, Any]:
        """
        Execute a search query using the agent.
        
        Args:
            query: Search query string
            
        Returns:
            Dict containing search results and intermediate steps
        """
        return self.executor.invoke({"input": query})