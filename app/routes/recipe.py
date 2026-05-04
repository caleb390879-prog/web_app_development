from flask import Blueprint, render_template, request, redirect, url_for, flash, abort

# 建立食譜相關的 Blueprint
recipe_bp = Blueprint('recipe', __name__)

@recipe_bp.route('/')
def index():
    """
    處理首頁與食譜搜尋。
    輸入: q (Query String)
    邏輯: 呼叫 Recipe.get_all(q) 取得資料清單
    輸出: 渲染 recipes/index.html
    """
    pass

@recipe_bp.route('/recipes/new', methods=['GET'])
def new_recipe():
    """
    顯示新增食譜的表單。
    輸入: 無
    邏輯: 無
    輸出: 渲染 recipes/form.html
    """
    pass

@recipe_bp.route('/recipes', methods=['POST'])
def create_recipe():
    """
    接收表單資料並建立新食譜。
    輸入: 表單資料 (title, ingredients, steps, notes)
    邏輯: 驗證 title，呼叫 Recipe.create()
    輸出: 重導向至首頁
    """
    pass

@recipe_bp.route('/recipes/<int:id>', methods=['GET'])
def recipe_detail(id):
    """
    顯示特定食譜的詳細內容。
    輸入: 食譜 id
    邏輯: 呼叫 Recipe.get_by_id(id)
    輸出: 渲染 recipes/detail.html，若找不到則 404
    """
    pass

@recipe_bp.route('/recipes/<int:id>/edit', methods=['GET'])
def edit_recipe(id):
    """
    顯示編輯食譜的表單並帶入現有資料。
    輸入: 食譜 id
    邏輯: 呼叫 Recipe.get_by_id(id)
    輸出: 渲染 recipes/form.html，若找不到則 404
    """
    pass

@recipe_bp.route('/recipes/<int:id>/update', methods=['POST'])
def update_recipe(id):
    """
    接收表單資料並更新食譜。
    輸入: 食譜 id, 表單資料 (title, ingredients, steps, notes)
    邏輯: 驗證 title，呼叫 Recipe.update()
    輸出: 重導向至食譜詳情頁
    """
    pass

@recipe_bp.route('/recipes/<int:id>/delete', methods=['POST'])
def delete_recipe(id):
    """
    刪除指定食譜。
    輸入: 食譜 id
    邏輯: 呼叫 Recipe.delete(id)
    輸出: 重導向至首頁
    """
    pass
