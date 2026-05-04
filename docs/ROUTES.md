# 路由與頁面設計文件 (Routes Design) - 食譜收藏夾系統

本文件基於 PRD、架構與資料庫設計，規劃 Flask 應用程式的路由與頁面對應關係。

---

## 1. 路由總覽表格

| 功能名稱 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| **首頁 / 搜尋** | `GET` | `/` | `templates/recipes/index.html` | 顯示所有食譜列表；若帶有 `?q=` 參數則進行搜尋 |
| **新增食譜表單** | `GET` | `/recipes/new` | `templates/recipes/form.html` | 顯示新增食譜的空白表單 |
| **建立食譜** | `POST` | `/recipes` | — | 接收新增表單資料，寫入 DB 後重導向至首頁 |
| **食譜詳情頁** | `GET` | `/recipes/<int:id>` | `templates/recipes/detail.html` | 顯示指定食譜的完整內容 |
| **編輯食譜表單** | `GET` | `/recipes/<int:id>/edit` | `templates/recipes/form.html` | 顯示帶有現有資料的編輯表單（共用 form 模板） |
| **更新食譜** | `POST` | `/recipes/<int:id>/update` | — | 接收編輯表單資料，更新 DB 後重導向至詳情頁 |
| **刪除食譜** | `POST` | `/recipes/<int:id>/delete` | — | 刪除指定食譜，完成後重導向至首頁 |

---

## 2. 路由詳細說明

### 2.1 首頁 / 搜尋 (`GET /`)
- **輸入**：URL 參數 `q`（非必填，用於關鍵字搜尋）。
- **處理邏輯**：
  - 檢查是否有 `q` 參數。
  - 若有，呼叫 `Recipe.get_all(search_query=q)`。
  - 若無，呼叫 `Recipe.get_all()`。
- **輸出**：渲染 `index.html`，並傳遞 `recipes` 變數。
- **錯誤處理**：無特定錯誤，若無資料則前端顯示「目前沒有食譜」。

### 2.2 新增食譜表單 (`GET /recipes/new`)
- **輸入**：無。
- **處理邏輯**：準備空白表單供使用者填寫。
- **輸出**：渲染 `form.html`，設定 `action` 指向 `/recipes`。

### 2.3 建立食譜 (`POST /recipes`)
- **輸入**：表單欄位 `title` (必填), `ingredients`, `steps`, `notes`。
- **處理邏輯**：
  - 驗證 `title` 是否存在。
  - 呼叫 `Recipe.create(data)`。
- **輸出**：重導向 (Redirect) 至 `/`。
- **錯誤處理**：若 `title` 空白，可透過 flash 訊息提示，並重新渲染表單或回傳 400。

### 2.4 食譜詳情頁 (`GET /recipes/<int:id>`)
- **輸入**：URL 路徑變數 `id`。
- **處理邏輯**：呼叫 `Recipe.get_by_id(id)`。
- **輸出**：渲染 `detail.html`，傳遞 `recipe` 變數。
- **錯誤處理**：若找不到該 id，回傳 404 (Not Found)。

### 2.5 編輯食譜表單 (`GET /recipes/<int:id>/edit`)
- **輸入**：URL 路徑變數 `id`。
- **處理邏輯**：呼叫 `Recipe.get_by_id(id)` 取得現有資料。
- **輸出**：渲染 `form.html`，設定 `action` 指向 `/recipes/<id>/update`，並帶入預設值。
- **錯誤處理**：若找不到該 id，回傳 404。

### 2.6 更新食譜 (`POST /recipes/<int:id>/update`)
- **輸入**：URL 路徑變數 `id`、表單欄位 `title` (必填), `ingredients`, `steps`, `notes`。
- **處理邏輯**：
  - 驗證 `title` 是否存在。
  - 呼叫 `Recipe.update(id, data)`。
- **輸出**：重導向至 `/recipes/<id>`。
- **錯誤處理**：若 `title` 空白，透過 flash 提示；找不到 id 回傳 404。

### 2.7 刪除食譜 (`POST /recipes/<int:id>/delete`)
- **輸入**：URL 路徑變數 `id`。
- **處理邏輯**：呼叫 `Recipe.delete(id)`。
- **輸出**：重導向至 `/`。
- **錯誤處理**：若找不到該 id，回傳 404。

---

## 3. Jinja2 模板清單

所有模板皆位於 `app/templates/` 目錄中：

1. **`base.html`**
   - 核心版面（包含 Header、CSS 引入、Flash 訊息區塊）。
   - 被其他所有頁面繼承 (`{% extends "base.html" %}`)。
2. **`recipes/index.html`**
   - 繼承自 `base.html`。
   - 包含搜尋列、新增按鈕與食譜卡片列表。
3. **`recipes/detail.html`**
   - 繼承自 `base.html`。
   - 顯示食譜詳細內容（食材、步驟、筆記），並包含「編輯」與「刪除」按鈕。
4. **`recipes/form.html`**
   - 繼承自 `base.html`。
   - **共用表單**：同時用於新增與編輯食譜，透過 Jinja2 邏輯判斷是否帶入既有資料。

---

## 4. 路由骨架程式碼

路由的骨架定義於 `app/routes/recipe.py` 中，請參閱專案檔案。
