# 流程圖文件 (Flowchart) - 食譜收藏夾系統

本文件基於產品需求文件 (PRD) 與系統架構文件 (ARCHITECTURE)，規劃了使用者操作的路徑、系統資料流動的序列，以及各項功能的路由設計。

---

## 1. 使用者流程圖 (User Flow)

此流程圖展示了使用者在網站中瀏覽、新增、編輯與搜尋食譜的完整操作路徑。

```mermaid
flowchart LR
    A([使用者開啟網頁]) --> B[首頁 - 食譜列表]
    
    B --> C{選擇操作}
    
    %% 新增食譜流程
    C -->|點擊「新增食譜」| D[填寫食譜表單]
    D -->|送出表單| E[儲存食譜並返回首頁]
    E --> B
    
    %% 搜尋流程
    C -->|輸入關鍵字或點擊標籤| F[顯示篩選後的食譜列表]
    F -->|清除搜尋| B
    F -->|點擊食譜| G
    
    %% 閱讀與編輯流程
    C -->|點擊特定食譜| G[食譜詳細閱讀頁]
    
    G --> H{選擇操作}
    H -->|返回| B
    H -->|點擊「編輯」| I[編輯食譜表單]
    I -->|送出修改| J[更新資料並返回閱讀頁]
    J --> G
    
    H -->|點擊「刪除」| K[確認刪除視窗]
    K -->|確認| L[刪除資料並返回首頁]
    L --> B
    K -->|取消| G
```

---

## 2. 系統序列圖 (Sequence Diagram)

以下以「使用者新增食譜」的流程為例，展示前端瀏覽器、Flask 路由、資料模型與 SQLite 資料庫之間的資料互動與處理順序。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器 (View)
    participant Flask as Flask 路由 (Controller)
    participant Model as 資料模型 (Model)
    participant DB as SQLite 資料庫

    User->>Browser: 點擊「新增食譜」
    Browser->>Flask: GET /recipes/new
    Flask-->>Browser: 回傳 Jinja2 新增表單頁面 (form.html)
    
    User->>Browser: 填寫食材、步驟、心得並送出
    Browser->>Flask: POST /recipes
    
    activate Flask
    Flask->>Flask: 驗證輸入資料格式
    Flask->>Model: 呼叫新增方法 create_recipe(data)
    
    activate Model
    Model->>DB: INSERT INTO recipes ...
    DB-->>Model: 寫入成功
    Model-->>Flask: 回傳新建食譜的 ID
    deactivate Model
    
    Flask-->>Browser: 重導向 (Redirect) 到首頁 /
    deactivate Flask
    
    Browser->>User: 顯示已更新的食譜列表
```

---

## 3. 功能清單對照表

根據 PRD 定義的 CRUD 與搜尋功能，以下是本專案預計實作的 URL 路徑與對應的 HTTP 方法規劃（考量 HTML 原生表單僅支援 GET/POST，因此更新與刪除皆採用 POST 搭配專屬路徑）。

| 功能名稱 | URL 路徑 | HTTP 方法 | 說明 |
| :--- | :--- | :--- | :--- |
| **瀏覽食譜列表 (首頁)** | `/` | `GET` | 顯示所有食譜，支援透過 `?q=關鍵字` 進行搜尋過濾 |
| **新增食譜 (表單頁)** | `/recipes/new` | `GET` | 渲染新增食譜的空白表單 |
| **新增食譜 (送出)** | `/recipes` | `POST` | 接收表單資料並寫入資料庫，完成後重導向至首頁 |
| **瀏覽食譜詳情** | `/recipes/<id>` | `GET` | 顯示特定食譜的詳細內容（食材、步驟、心得） |
| **編輯食譜 (表單頁)** | `/recipes/<id>/edit` | `GET` | 渲染編輯表單，並帶入該食譜的現有資料 |
| **編輯食譜 (送出)** | `/recipes/<id>/edit` | `POST` | 接收表單資料以更新資料庫，完成後重導向至詳情頁 |
| **刪除食譜** | `/recipes/<id>/delete` | `POST` | 從資料庫刪除指定食譜，完成後重導向至首頁 |
