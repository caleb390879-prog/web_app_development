from app import create_app
import sqlite3
import os

app = create_app()

def init_db():
    """初始化資料庫"""
    db_path = os.path.join(os.path.dirname(__file__), 'instance', 'database.db')
    schema_path = os.path.join(os.path.dirname(__file__), 'database', 'schema.sql')
    
    # 確保 instance 資料夾存在
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    with sqlite3.connect(db_path) as conn:
        with open(schema_path, 'r', encoding='utf-8') as f:
            conn.executescript(f.read())
    print("資料庫初始化完成！")

if __name__ == '__main__':
    # 檢查是否需要自動建立資料庫
    if not os.path.exists(os.path.join('instance', 'database.db')):
        init_db()
        
    # 啟動開發伺服器
    app.run(debug=True, host='0.0.0.0', port=5000)
