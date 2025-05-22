from typing import List, Dict, Any, Optional
from langchain.agents import AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain.schema import BaseMessage
from langchain.tools import BaseTool
from langchain_community.llms import Ollama
from langchain.agents.openai_functions_agent.base import OpenAIFunctionsAgent
from langchain.prompts import MessagesPlaceholder
import os
from dotenv import load_dotenv

# 加載環境變量
load_dotenv()

class BaseAgent:
    def __init__(
        self,
        name: str,
        tools: List[BaseTool],
        llm: Optional[Ollama] = None,
        memory: Optional[ConversationBufferMemory] = None,
        verbose: bool = True
    ):
        self.name = name
        self.tools = tools
        
        # 使用 Ollama 本地模型
        self.llm = llm or Ollama(
            model=os.getenv("MODEL_NAME", "mistral"),  # 使用 Mistral 模型
            temperature=float(os.getenv("TEMPERATURE", "0.7")),
        )
        
        self.memory = memory or ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        self.verbose = verbose
        
        # 創建Agent
        self.agent = OpenAIFunctionsAgent.from_llm_and_tools(
            llm=self.llm,
            tools=self.tools,
            system_message=self._get_system_message(),
            extra_prompt_messages=[
                MessagesPlaceholder(variable_name="chat_history")
            ]
        )
        
        # 創建Agent執行器
        self.agent_executor = AgentExecutor.from_agent_and_tools(
            agent=self.agent,
            tools=self.tools,
            memory=self.memory,
            verbose=self.verbose,
            handle_parsing_errors=True
        )
    
    def _get_system_message(self) -> str:
        """返回Agent的系統提示信息"""
        return f"""你是一個專業的3C產品電商助手 {self.name}。
        你的職責是幫助用戶解決關於3C產品的問題，包括產品諮詢、訂單查詢、售後服務等。
        請始終保持專業、友善的態度，並確保提供準確的信息。"""
    
    async def run(self, input_text: str) -> Dict[str, Any]:
        """運行Agent並返回結果"""
        try:
            response = await self.agent_executor.ainvoke({"input": input_text})
            return {
                "status": "success",
                "response": response["output"],
                "agent_name": self.name
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "agent_name": self.name
            }
    
    def get_memory(self) -> List[BaseMessage]:
        """獲取對話歷史"""
        return self.memory.chat_memory.messages 