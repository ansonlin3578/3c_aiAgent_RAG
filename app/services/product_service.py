from typing import List, Dict, Any
import json
import os
from pathlib import Path
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor

class ProductService:
    def __init__(self):
        # 使用多語言 sentence-transformers 模型
        self.embeddings = HuggingFaceEmbeddings(
            model_name="paraphrase-multilingual-MiniLM-L12-v2",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,  # 減小chunk大小以獲得更精確的匹配
            chunk_overlap=100,
            length_function=len,
        )
        self.vector_store = None
        self.products_data = None
        self._initialize_vector_store()

    def _initialize_vector_store(self):
        """初始化向量存儲"""
        # 讀取產品數據
        products_file = Path("app/data/documents/products.json")
        with open(products_file, "r", encoding="utf-8") as f:
            self.products_data = json.load(f)

        # 將產品數據轉換為文檔
        documents = []
        for product in self.products_data["products"]:
            # 為每個產品創建多個不同角度的文檔
            # 1. 基本信息文檔
            basic_info = f"""
            產品名稱: {product['name']}
            類別: {product['category']}
            價格: {product['price']}元
            庫存: {product['stock']}台
            """
            documents.append(Document(
                page_content=basic_info,
                metadata={
                    "id": product["id"],
                    "name": product["name"],
                    "type": "basic_info"
                }
            ))

            # 2. 完整規格文檔
            specs_info = f"""
            產品名稱: {product['name']}
            完整規格:
            {self._format_specs(product)}
            """
            documents.append(Document(
                page_content=specs_info,
                metadata={
                    "id": product["id"],
                    "name": product["name"],
                    "type": "specs"
                }
            ))

            # 3. 描述和保固文檔
            desc_info = f"""
            產品名稱: {product['name']}
            產品描述: {product['description']}
            保固信息: {product['warranty']}
            """
            documents.append(Document(
                page_content=desc_info,
                metadata={
                    "id": product["id"],
                    "name": product["name"],
                    "type": "description"
                }
            ))

        # 分割文檔
        split_docs = self.text_splitter.split_documents(documents)

        # 創建向量存儲
        self.vector_store = Chroma.from_documents(
            documents=split_docs,
            embedding=self.embeddings,
            persist_directory="chroma_db/products"
        )

    def _format_specs(self, product: Dict[str, Any]) -> str:
        """格式化產品規格"""
        specs = product['specs']
        formatted_specs = []
        
        # 定義規格項目的中文名稱映射
        spec_names = {
            "processor": "處理器",
            "ram": "記憶體",
            "storage": "儲存空間",
            "display": "顯示器",
            "battery": "電池",
            "ports": "連接埠",
            "noise_cancellation": "降噪功能",
            "battery_life": "電池續航",
            "bluetooth": "藍牙版本",
            "weight": "重量",
            "features": "特色功能"
        }
        
        for key, value in specs.items():
            # 獲取中文名稱，如果沒有對應的中文名稱則使用原始key
            display_name = spec_names.get(key, key)
            
            # 處理列表類型的值
            if isinstance(value, list):
                value = "、".join(value)
            
            formatted_specs.append(f"{display_name}: {value}")
        
        return "\n".join(formatted_specs)

    def search_products(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        """搜索產品"""
        if not self.vector_store:
            self._initialize_vector_store()

        # 檢查是否為庫存查詢
        if "庫存" in query or "剩下" in query or "還有" in query:
            for product in self.products_data["products"]:
                if product["name"] in query:
                    return [{
                        "content": f"{product['name']} 目前庫存還有 {product['stock']} 台",
                        "metadata": {
                            "id": product["id"],
                            "name": product["name"],
                            "stock": product["stock"]
                        }
                    }]

        # 檢查是否為規格查詢
        if "規格" in query:
            for product in self.products_data["products"]:
                if product["name"] in query:
                    return [{
                        "content": f"""
{product['name']} 的規格如下：

{self._format_specs(product)}
""",
                        "metadata": {
                            "id": product["id"],
                            "name": product["name"],
                            "type": "specs"
                        }
                    }]

        # 執行相似度搜索
        docs = self.vector_store.similarity_search_with_score(query, k=k)
        
        # 格式化結果並去重
        seen_products = set()
        results = []
        
        for doc, score in docs:
            product_id = doc.metadata["id"]
            if product_id not in seen_products:
                seen_products.add(product_id)
                # 如果是規格相關的查詢，返回完整規格
                if "規格" in query and doc.metadata["type"] == "specs":
                    product = self.get_product_details(product_id)
                    if product:
                        results.append({
                            "content": f"""
{doc.metadata['name']} 的規格如下：

{self._format_specs(product)}
""",
                            "metadata": doc.metadata,
                            "relevance_score": score
                        })
                else:
                    results.append({
                        "content": doc.page_content,
                        "metadata": doc.metadata,
                        "relevance_score": score
                    })
        
        return results

    def get_product_details(self, product_id: str) -> Dict[str, Any]:
        """獲取產品詳細信息"""
        for product in self.products_data["products"]:
            if product["id"] == product_id:
                return product
        return None 