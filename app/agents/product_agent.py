from typing import List
from langchain.tools import BaseTool
from .base_agent import BaseAgent
from ..tools.product_tools import ProductSearchTool, ProductRecommendationTool

class ProductAgent(BaseAgent):
    def __init__(self):
        # 初始化工具
        tools: List[BaseTool] = [
            ProductSearchTool(),
            ProductRecommendationTool()
        ]
        
        # 初始化父類
        super().__init__(
            name="ProductConsultant",
            tools=tools,
            verbose=True
        )
    
    def _get_system_message(self) -> str:
        return """你是一個專業的3C產品顧問，專門負責回答用戶關於產品的問題。
        你必須使用提供的工具來回答問題，而不是直接生成答案或代碼。
        
        當用戶詢問產品信息時：
        1. 使用 product_search 工具搜索產品信息
           - 直接調用 product_search(query) 函數，其中 query 是用戶的查詢
           - 例如：product_search("iPhone 15 Pro")
        
        2. 使用 product_recommendation 工具推薦產品
           - 直接調用 product_recommendation(requirements) 函數，其中 requirements 是用戶的需求
           - 例如：product_recommendation("需要一台高性能的手機")
        
        重要提示：
        - 不要生成任何代碼或示例代碼
        - 直接使用工具函數，不要解釋如何使用工具
        - 如果工具返回的結果為空，再考慮提供一般性的建議
        - 保持專業、友善的態度，確保提供準確的信息
        - 如果遇到不確定的問題，請誠實告知，不要提供錯誤信息""" 