# 系統架構設計文件 (Architecture) - 食譜收藏夾系統

## 1. 技術架構說明

本專案旨在提供輕量化、易於個人部署與使用的數位食譜筆記本，因此選用以下技術棧：

- **後端框架：Python + Flask**
  - **原因**：Flask 是輕量級的微框架，適合個人專案及中小型應用，學習曲線平緩且能快速建置原型，具備極高的靈活性。
- **模板引擎：Jinja2**
  - **原因**：Flask 內建支援 Jinja2，不需要額外維護前後端分離的架構。由後端直接渲染 HTML 頁面，可以降低開發複雜度，並且對於不需要高度互動的頁面（如食譜閱讀）效能表現優異。
- **資料庫：SQLite**
  - **原因**：無伺服器的輕量資料庫，資料儲存於單一檔案中，非常適合個人單機使用、備份與遷移。配合 Python 內建的 `sqlite3` 模組或輕量 ORM 即可輕鬆操作。
- **前端樣式：原生 CSS / 輕量 CSS 框架**
  - **原因**：專案重視「行動版閱讀優化」，使用原生 CSS (搭配 CSS Variables 與 Flexbox/Grid) 即可打造簡約且響應式的介面，避免引入過於笨重的前端框架影響載入速度。

### Flask MVC 模式說明
雖然 Flask 本身沒有嚴格規範，但在本專案中我們將採用類似 MVC (Model-View-Controller) 的職責分離架構：
- **Model (資料模型)**：負責與 SQLite 資料庫互動，處理食譜的增刪改查 (CRUD) 與資料驗證。
- **View (視圖)**：Jinja2 模板與 CSS，負責將 Controller 傳來的資料轉化為使用者看到的 HTML 網頁介面。
- **Controller (控制器/路由)**：Flask 的路由 (`routes`)，負責接收使用者的 HTTP 請求、呼叫 Model 取得資料，再將資料傳遞給 View 進行渲染。

---

## 2. 專案資料夾結構

為了保持專案整潔與可擴展性，我們採用 Flask 原廠推薦的 Application Factory 模式或標準的模組化結構。

```text
web_app_development/
├── app/                      # Flask 應用程式主目錄
│   ├── __init__.py           # 初始化 Flask App 與設定
│   ├── models.py             # 資料庫模型與操作 (Model)
│   ├── routes.py             # 路由定義與商業邏輯 (Controller)
│   ├── static/               # 靜態資源檔案
│   │   ├── css/              # 樣式表 (主打行動版優先的 style.css)
│   │   ├── js/               # 簡單的互動腳本 (如需動態新增標籤等)
│   │   └── img/              # 預留給未來食譜圖片的儲存資料夾
│   └── templates/            # Jinja2 HTML 模板 (View)
│       ├── base.html         # 共用模板 (Header, Footer, 導覽列)
│       ├── index.html        # 食譜列表首頁 (含搜尋與列表)
│       ├── detail.html       # 食譜詳細閱讀頁 (優化行動版排版)
│       └── form.html         # 新增/編輯食譜表單頁
├── instance/                 # 存放不該進版控的執行期檔案
│   └── database.db           # SQLite 資料庫檔案
├── docs/                     # 專案文件
│   ├── PRD.md                # 產品需求文件
│   └── ARCHITECTURE.md       # 系統架構文件 (本文件)
├── requirements.txt          # Python 依賴套件清單
└── app.py                    # 專案啟動入口 (entry point)
```

---

## 3. 元件關係圖

以下圖表說明當使用者操作瀏覽器時，系統各元件之間的互動關係：

```mermaid
flowchart TD
    Browser[瀏覽器 (使用者介面)]
    
    subgraph Flask App [Flask 應用程式]
        Route[Controller: Flask Routes]
        Template[View: Jinja2 Templates]
        Model[Model: Database Logic]
        Static[Static: CSS/JS]
    end
    
    DB[(SQLite 資料庫\ninstance/database.db)]

    %% 請求流程
    Browser -- "1. 發送 HTTP 請求\n(GET / POST)" --> Route
    Route -- "2. 查詢/寫入食譜資料" --> Model
    Model -- "3. 執行 SQL 指令" --> DB
    DB -- "4. 回傳資料結果" --> Model
    Model -- "5. 將資料回傳給 Controller" --> Route
    
    %% 渲染流程
    Route -- "6. 傳入資料並要求渲染" --> Template
    Template -- "7. 結合 Static 資源生成 HTML" --> Route
    Route -- "8. 回傳 HTTP Response" --> Browser
    Static -. "載入樣式與腳本" .-> Browser
```

---

## 4. 關鍵設計決策

1. **採用伺服器端渲染 (SSR) 而非前後端分離 (SPA)**
   - **原因**：本專案的核心需求是結構化的資料建檔與閱讀，互動需求相對單純。使用 Jinja2 渲染 HTML 可以大幅節省開發時間，不需維護獨立的 API 層與前端專案，也更容易達到頁面秒開的效能目標。
2. **行動優先 (Mobile-First) 的介面設計**
   - **原因**：根據 PRD，使用者經常會在廚房「一邊操作一邊觀看」。因此 CSS 設計會優先考量手機螢幕尺寸，採用大字體、按鈕易觸控、以及無須頻繁縮放的版面佈局，桌機版則透過 Media Queries 向下相容。
3. **選擇 SQLite 作為資料庫**
   - **原因**：作為個人食譜收藏夾，資料量不會達到需要 MySQL 或 PostgreSQL 等大型關聯式資料庫的規模。SQLite 零配置、單一檔案的特性，讓專案不論是備份、搬移到其他電腦，或是在不同環境部署都非常容易。
4. **將食譜結構拆分為獨立欄位**
   - **原因**：相較於只提供一個大型的 Rich Text 編輯器，PRD 明確要求將「食材清單」、「烹飪步驟」與「私房筆記」分開。在資料庫 Schema 設計時，這些將會是獨立的欄位（或關聯表），這樣在前端顯示時才能分別給予最佳化的排版（例如步驟前加上自動編號大圓圈，食材清單採用核取方塊樣式）。
