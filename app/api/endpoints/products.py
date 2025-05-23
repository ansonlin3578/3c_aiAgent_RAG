from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from app.services.product_service import ProductService

router = APIRouter()
product_service = ProductService()

@router.get("/search")
async def search_products(query: str, k: int = 3) -> List[Dict[str, Any]]:
    """
    使用 RAG 搜索產品
    
    Args:
        query: 搜索查詢
        k: 返回結果數量
        
    Returns:
        相關產品列表
    """
    try:
        results = product_service.search_products(query, k)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 