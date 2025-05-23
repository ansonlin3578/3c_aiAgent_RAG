from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List
import json
import logging
import os
from dotenv import load_dotenv
from .agents.product_agent import ProductAgent
from app.api.endpoints import products

# 加載環境變量
load_dotenv()

# 配置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="3C產品電商 AI Agent API")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# 存儲WebSocket連接
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, client_id: str):
        logger.info(f"Attempting to connect client {client_id}")
        try:
            await websocket.accept()
            self.active_connections[client_id] = websocket
            logger.info(f"Client {client_id} connected successfully")
        except Exception as e:
            logger.error(f"Failed to connect client {client_id}: {str(e)}")
            raise
    
    def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]
            logger.info(f"Client {client_id} disconnected")
    
    async def send_message(self, message: str, client_id: str):
        if client_id in self.active_connections:
            await self.active_connections[client_id].send_text(message)
            logger.info(f"Message sent to client {client_id}: {message}")
        else:
            logger.warning(f"Client {client_id} not found when trying to send message")

manager = ConnectionManager()

# 創建Agent實例
product_agent = ProductAgent()
logger.info("ProductAgent initialized")

# 包含路由
app.include_router(products.router, prefix="/api/products", tags=["products"])

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket, client_id)
    try:
        while True:
            # 接收消息
            data = await websocket.receive_text()
            logger.info(f"Received message from client {client_id}: {data}")
            
            try:
                message = json.loads(data)
                
                # 處理消息
                if message["type"] == "chat":
                    logger.info(f"Processing chat message: {message['content']}")
                    # 使用ProductAgent處理消息
                    response = await product_agent.run(message["content"])
                    logger.info(f"Agent response: {response}")
                    
                    # 發送響應
                    await manager.send_message(
                        json.dumps({
                            "type": "response",
                            "content": response["response"],
                            "status": response["status"]
                        }),
                        client_id
                    )
            except json.JSONDecodeError as e:
                logger.error(f"JSON decode error: {e}")
                await manager.send_message(
                    json.dumps({
                        "type": "error",
                        "content": "Invalid message format",
                        "status": "error"
                    }),
                    client_id
                )
            except Exception as e:
                logger.error(f"Error processing message: {e}")
                await manager.send_message(
                    json.dumps({
                        "type": "error",
                        "content": str(e),
                        "status": "error"
                    }),
                    client_id
                )
            
    except WebSocketDisconnect:
        manager.disconnect(client_id)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(client_id)

@app.get("/")
async def root():
    return {"message": "Welcome to 3C產品電商 AI Agent API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 