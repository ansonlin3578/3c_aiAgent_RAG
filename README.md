# 3C產品智能助手

這是一個基於 LangChain 和 FastAPI 開發的智能產品諮詢系統，能夠回答用戶關於3C產品的問題，提供產品搜索和推薦功能。

## 功能特點

- 產品搜索：根據產品名稱、類別或規格進行搜索
- 產品推薦：根據用戶需求推薦合適的產品
- 即時對話：支持自然語言交互
- 本地模型：使用 Ollama 運行本地模型，無需 API 密鑰

## 系統要求

- Python 3.8+
- Ollama（用於運行本地模型）

## 安裝步驟

1. 克隆代碼庫：
```bash
git clone [repository_url]
cd [repository_name]
```

2. 安裝 Python 依賴：
```bash
pip install -r requirements.txt
```

3. 安裝 Ollama：
   - 訪問 [Ollama 官網](https://ollama.ai/) 下載並安裝
   - 下載 Mistral 模型：
```bash
ollama pull mistral
```

4. 配置環境變量：
   - 複製 `.env.example` 到 `.env`
   - 根據需要修改配置

## 運行系統

1. 啟動服務器：
```bash
python run.py
```

2. 訪問 Web 界面：
   - 打開瀏覽器訪問 `http://localhost:8000/static/index.html`

## 使用示例

1. 產品搜索：
   - "列出所有手機"
   - "有哪些耳機產品？"
   - "iPhone 15 Pro 的詳細信息是什麼？"

2. 產品推薦：
   - "請推薦一款適合辦公的筆記本電腦"
   - "我需要一台性價比高的耳機"
   - "推薦一款拍照好的手機"

## 系統架構

```
app/
├── agents/          # 智能代理
│   ├── base_agent.py
│   └── product_agent.py
├── data/           # 數據文件
│   └── documents/
│       └── products.json
├── static/         # 靜態文件
│   └── index.html
├── tools/          # 工具函數
│   └── product_tools.py
└── main.py         # 主程序
```

## 開發指南

1. 添加新產品：
   - 在 `app/data/documents/products.json` 中添加產品信息

2. 自定義模型：
   - 修改 `.env` 文件中的 `MODEL_NAME` 參數
   - 可選模型：mistral, llama2, codellama, neural-chat

3. 擴展功能：
   - 在 `app/tools/` 中添加新的工具
   - 在 `app/agents/` 中創建新的代理

## 常見問題

1. 模型加載失敗：
   - 確保 Ollama 已正確安裝
   - 檢查模型是否已下載
   - 查看服務器日誌

2. 搜索結果不準確：
   - 檢查產品數據格式
   - 確認搜索關鍵詞
   - 查看工具日誌

## 貢獻指南

1. Fork 項目
2. 創建特性分支
3. 提交更改
4. 推送到分支
5. 創建 Pull Request

## 許可證

MIT License

## 聯繫方式

如有問題或建議，請提交 Issue 或 Pull Request。 