import sqlite3
import os
from datetime import datetime

# 預設資料庫路徑 (可由外部設定)
DATABASE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'instance', 'database.db')

def get_db_connection():
    """取得資料庫連線，並設定 row_factory 以字典形式存取欄位"""
    # 確保 instance 資料夾存在
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

class Recipe:
    @staticmethod
    def get_all(search_query=None):
        """取得所有食譜，支援關鍵字搜尋"""
        conn = get_db_connection()
        if search_query:
            query = "SELECT * FROM recipes WHERE title LIKE ? OR ingredients LIKE ? ORDER BY updated_at DESC"
            wildcard_query = f"%{search_query}%"
            recipes = conn.execute(query, (wildcard_query, wildcard_query)).fetchall()
        else:
            recipes = conn.execute('SELECT * FROM recipes ORDER BY updated_at DESC').fetchall()
        conn.close()
        return [dict(row) for row in recipes]

    @staticmethod
    def get_by_id(recipe_id):
        """根據 ID 取得單一食譜"""
        conn = get_db_connection()
        recipe = conn.execute('SELECT * FROM recipes WHERE id = ?', (recipe_id,)).fetchone()
        conn.close()
        return dict(recipe) if recipe else None

    @staticmethod
    def create(data):
        """新增食譜"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO recipes (title, ingredients, steps, notes)
            VALUES (?, ?, ?, ?)
        ''', (data.get('title'), data.get('ingredients', ''), data.get('steps', ''), data.get('notes', '')))
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        return new_id

    @staticmethod
    def update(recipe_id, data):
        """更新食譜內容"""
        conn = get_db_connection()
        conn.execute('''
            UPDATE recipes
            SET title = ?, ingredients = ?, steps = ?, notes = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (data.get('title'), data.get('ingredients', ''), data.get('steps', ''), data.get('notes', ''), recipe_id))
        conn.commit()
        conn.close()
        return True

    @staticmethod
    def delete(recipe_id):
        """刪除食譜"""
        conn = get_db_connection()
        conn.execute('DELETE FROM recipes WHERE id = ?', (recipe_id,))
        conn.commit()
        conn.close()
        return True
