import sqlite3
import os
import logging

# 設定 logging
logging.basicConfig(level=logging.ERROR)

# 預設資料庫路徑 (可由外部設定)
DATABASE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'instance', 'database.db')

def get_db_connection():
    """取得資料庫連線，並設定 row_factory 以字典形式存取欄位"""
    try:
        os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        logging.error(f"資料庫連線失敗: {e}")
        raise

class Recipe:
    @staticmethod
    def get_all(search_query=None):
        """
        取得所有食譜，支援關鍵字搜尋
        參數: search_query (str, 預設為 None): 搜尋關鍵字
        回傳: list of dict
        """
        try:
            conn = get_db_connection()
            if search_query:
                query = "SELECT * FROM recipes WHERE title LIKE ? OR ingredients LIKE ? ORDER BY updated_at DESC"
                wildcard_query = f"%{search_query}%"
                recipes = conn.execute(query, (wildcard_query, wildcard_query)).fetchall()
            else:
                recipes = conn.execute('SELECT * FROM recipes ORDER BY updated_at DESC').fetchall()
            return [dict(row) for row in recipes]
        except Exception as e:
            logging.error(f"取得所有食譜失敗: {e}")
            return []
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def get_by_id(recipe_id):
        """
        根據 ID 取得單一食譜
        參數: recipe_id (int): 食譜的 ID
        回傳: dict 或 None (若找不到)
        """
        try:
            conn = get_db_connection()
            recipe = conn.execute('SELECT * FROM recipes WHERE id = ?', (recipe_id,)).fetchone()
            return dict(recipe) if recipe else None
        except Exception as e:
            logging.error(f"取得食譜詳情失敗 (ID: {recipe_id}): {e}")
            return None
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def create(data):
        """
        新增食譜
        參數: data (dict): 包含 title, ingredients, steps, notes 的字典
        回傳: 新增食譜的 ID 或 None (若失敗)
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO recipes (title, ingredients, steps, notes)
                VALUES (?, ?, ?, ?)
            ''', (data.get('title'), data.get('ingredients', ''), data.get('steps', ''), data.get('notes', '')))
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            logging.error(f"新增食譜失敗: {e}")
            if 'conn' in locals() and conn:
                conn.rollback()
            return None
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def update(recipe_id, data):
        """
        更新食譜內容
        參數: recipe_id (int), data (dict): 包含 title, ingredients, steps, notes 的字典
        回傳: bool (是否成功)
        """
        try:
            conn = get_db_connection()
            conn.execute('''
                UPDATE recipes
                SET title = ?, ingredients = ?, steps = ?, notes = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (data.get('title'), data.get('ingredients', ''), data.get('steps', ''), data.get('notes', ''), recipe_id))
            conn.commit()
            return True
        except Exception as e:
            logging.error(f"更新食譜失敗 (ID: {recipe_id}): {e}")
            if 'conn' in locals() and conn:
                conn.rollback()
            return False
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def delete(recipe_id):
        """
        刪除食譜
        參數: recipe_id (int): 要刪除的食譜 ID
        回傳: bool (是否成功)
        """
        try:
            conn = get_db_connection()
            conn.execute('DELETE FROM recipes WHERE id = ?', (recipe_id,))
            conn.commit()
            return True
        except Exception as e:
            logging.error(f"刪除食譜失敗 (ID: {recipe_id}): {e}")
            if 'conn' in locals() and conn:
                conn.rollback()
            return False
        finally:
            if 'conn' in locals() and conn:
                conn.close()
