# 3C 產品電商 AI 助手

這是一個基於 RAG (Retrieval-Augmented Generation) 技術的 3C 產品電商 AI 助手，能夠智能地回答用戶關於產品規格、庫存、價格等問題。

## 功能特點

- 智能產品搜索：使用語意搜索技術，能夠理解用戶的自然語言查詢
- 多語言支持：使用多語言模型，支持中文和英文查詢
- 精確的規格查詢：能夠準確返回產品的完整規格信息
- 庫存查詢：支持即時查詢產品庫存狀態
- 智能錯誤處理：當查詢不存在的產品時，會給出友好的提示

## 技術架構

- 後端：Python FastAPI
- 向量數據庫：Chroma
- 嵌入模型：paraphrase-multilingual-MiniLM-L12-v2
- 前端：HTML + JavaScript

## 安裝步驟

1. 克隆專案：
```bash
git clone [repository_url]
cd [project_directory]
```

2. 安裝依賴：
```bash
pip install -r requirements.txt
```

3. 啟動服務：
```bash
python run.py
```

4. 訪問應用：
打開瀏覽器訪問 `http://localhost:8000/static/index.html`

## 使用範例

### 1. 規格查詢
```
提示：MacBook Pro 規格
回答：
MacBook Pro 的規格如下：

處理器: M3 Pro
記憶體: 16GB
儲存空間: 512GB SSD
顯示器: 14.2吋 Liquid Retina XDR
電池: 70瓦時
連接埠: HDMI、SDXC、MagSafe 3、Thunderbolt 4
```

### 2. 庫存查詢
```
提示：MacBook Pro 目前庫存還有多少台？
回答：MacBook Pro 目前庫存還有 50 台
```

### 3. 價格查詢
```
提示：MacBook Pro 的價格是多少？
回答：產品名稱: MacBook Pro 類別: 筆記型電腦 價格: 59900元 庫存: 50台
```

### 4. 不存在的產品查詢
```
提示：Nintendo Switch OLED 的價格是多少？
回答：目前商店中沒有此商品
```

## 查詢技巧

1. 規格查詢：
   - 使用"規格"關鍵字可以獲取完整的產品規格信息
   - 例如："MacBook Pro 規格"、"iPhone 15 Pro 規格"

2. 庫存查詢：
   - 使用"庫存"、"剩下"、"還有"等關鍵字
   - 例如："MacBook Pro 目前庫存還有多少台？"

3. 價格查詢：
   - 直接詢問產品價格
   - 例如："MacBook Pro 的價格是多少？"

## 注意事項

1. 確保產品名稱輸入正確，系統會進行精確匹配
2. 查詢不存在的產品時，系統會返回"目前商店中沒有此商品"
3. 系統使用語意搜索，可以理解相似的表達方式
4. 支持中文和英文查詢

## 開發者信息

- 作者：[Your Name]
- 版本：1.0.0
- 最後更新：2024-03-21

## 授權協議

MIT License 