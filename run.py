import uvicorn
from fastapi.staticfiles import StaticFiles
from app.main import app

# 掛載靜態文件
app.mount("/static", StaticFiles(directory="app/static"), name="static")

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    ) 