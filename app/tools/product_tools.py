from typing import Dict, List, Any
from langchain.tools import BaseTool
import json
from pathlib import Path
from pydantic import Field

class ProductSearchTool(BaseTool):
    name: str = "product_search"
    description: str = "搜索產品信息，可以根據產品名稱、類別或規格進行搜索"
    products: List[Dict[str, Any]] = Field(default_factory=list)
    
    def __init__(self, **data):
        super().__init__(**data)
        self.products = self._load_products()
    
    def _load_products(self) -> List[Dict[str, Any]]:
        """加載產品數據"""
        products_file = Path(__file__).parent.parent / "data" / "documents" / "products.json"
        with open(products_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data["products"]
    
    def _run(self, query: str) -> str:
        """執行產品搜索"""
        query = query.lower()
        results = []
        
        # 處理特殊查詢
        if "有哪些" in query or "列出" in query or "所有" in query:
            # 提取類別關鍵詞
            category_keywords = {
                "耳機": "耳機",
                "手機": "手機",
                "筆記本": "筆記型電腦",
                "筆電": "筆記型電腦",
                "電腦": "筆記型電腦",
                "筆記型電腦": "筆記型電腦"
            }
            
            # 檢查是否包含類別關鍵詞
            found_category = False
            target_category = None
            
            # 首先檢查是否包含類別關鍵詞
            for keyword, category in category_keywords.items():
                if keyword in query:
                    target_category = category
                    found_category = True
                    break
            
            # 如果找到類別關鍵詞，搜索該類別的所有產品
            if found_category and target_category:
                print(f"Searching for category: {target_category}")  # 調試輸出
                for product in self.products:
                    print(f"Checking product: {product['name']}, category: {product['category']}")  # 調試輸出
                    if product["category"] == target_category:
                        results.append(product)
            else:
                # 如果沒有找到特定類別關鍵詞，返回所有產品
                results = self.products
        else:
            # 常規搜索邏輯
            for product in self.products:
                # 搜索產品名稱
                if query in product["name"].lower():
                    results.append(product)
                    continue
                
                # 搜索產品類別
                if query in product["category"].lower():
                    results.append(product)
                    continue
                
                # 搜索產品描述
                if query in product["description"].lower():
                    results.append(product)
                    continue
                
                # 搜索產品規格
                for spec_key, spec_value in product["specs"].items():
                    if isinstance(spec_value, str) and query in spec_value.lower():
                        results.append(product)
                        break
        
        if not results:
            return "未找到相關產品"
        
        # 格式化結果
        formatted_results = []
        for product in results:
            formatted_result = f"""
產品名稱: {product['name']}
類別: {product['category']}
價格: NT${product['price']}
描述: {product['description']}
規格:
"""
            for key, value in product["specs"].items():
                formatted_result += f"- {key}: {value}\n"
            
            formatted_results.append(formatted_result)
        
        return "\n".join(formatted_results)

class ProductRecommendationTool(BaseTool):
    name: str = "product_recommendation"
    description: str = "根據用戶需求推薦合適的產品"
    products: List[Dict[str, Any]] = Field(default_factory=list)
    
    def __init__(self, **data):
        super().__init__(**data)
        self.products = self._load_products()
    
    def _load_products(self) -> List[Dict[str, Any]]:
        """加載產品數據"""
        products_file = Path(__file__).parent.parent / "data" / "documents" / "products.json"
        with open(products_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data["products"]
    
    def _run(self, requirements: str) -> str:
        """執行產品推薦"""
        requirements = requirements.lower()
        recommendations = []
        
        # 根據需求匹配產品
        for product in self.products:
            score = 0
            
            # 檢查產品描述
            if any(keyword in product["description"].lower() for keyword in requirements.split()):
                score += 2
            
            # 檢查產品規格
            for spec_key, spec_value in product["specs"].items():
                if isinstance(spec_value, str) and any(keyword in spec_value.lower() for keyword in requirements.split()):
                    score += 1
            
            if score > 0:
                recommendations.append((product, score))
        
        if not recommendations:
            return "抱歉，沒有找到符合您需求的產品"
        
        # 按匹配分數排序
        recommendations.sort(key=lambda x: x[1], reverse=True)
        
        # 格式化推薦結果
        formatted_recommendations = ["根據您的需求，我推薦以下產品："]
        for product, score in recommendations[:3]:  # 只推薦前3個
            formatted_recommendations.append(f"""
產品名稱: {product['name']}
類別: {product['category']}
價格: NT${product['price']}
描述: {product['description']}
""")
        
        return "\n".join(formatted_recommendations) 