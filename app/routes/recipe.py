from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from app.models.recipe import Recipe

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
    search_query = request.args.get('q')
    recipes = Recipe.get_all(search_query)
    return render_template('recipes/index.html', recipes=recipes)

@recipe_bp.route('/recipes/new', methods=['GET'])
def new_recipe():
    """
    顯示新增食譜的表單。
    輸入: 無
    邏輯: 無
    輸出: 渲染 recipes/form.html
    """
    return render_template('recipes/form.html', recipe=None)

@recipe_bp.route('/recipes', methods=['POST'])
def create_recipe():
    """
    接收表單資料並建立新食譜。
    輸入: 表單資料 (title, ingredients, steps, notes)
    邏輯: 驗證 title，呼叫 Recipe.create()
    輸出: 重導向至首頁
    """
    title = request.form.get('title')
    ingredients = request.form.get('ingredients')
    steps = request.form.get('steps')
    notes = request.form.get('notes')

    # 基本輸入驗證
    if not title or title.strip() == '':
        flash('食譜名稱為必填欄位！')
        return redirect(url_for('recipe.new_recipe'))

    data = {
        'title': title.strip(),
        'ingredients': ingredients.strip() if ingredients else '',
        'steps': steps.strip() if steps else '',
        'notes': notes.strip() if notes else ''
    }

    new_id = Recipe.create(data)
    if new_id:
        flash('成功新增食譜！')
        return redirect(url_for('recipe.index'))
    else:
        flash('新增食譜失敗，請稍後再試。')
        return redirect(url_for('recipe.new_recipe'))

@recipe_bp.route('/recipes/<int:id>', methods=['GET'])
def recipe_detail(id):
    """
    顯示特定食譜的詳細內容。
    輸入: 食譜 id
    邏輯: 呼叫 Recipe.get_by_id(id)
    輸出: 渲染 recipes/detail.html，若找不到則 404
    """
    recipe = Recipe.get_by_id(id)
    if not recipe:
        abort(404)
    return render_template('recipes/detail.html', recipe=recipe)

@recipe_bp.route('/recipes/<int:id>/edit', methods=['GET'])
def edit_recipe(id):
    """
    顯示編輯食譜的表單並帶入現有資料。
    輸入: 食譜 id
    邏輯: 呼叫 Recipe.get_by_id(id)
    輸出: 渲染 recipes/form.html，若找不到則 404
    """
    recipe = Recipe.get_by_id(id)
    if not recipe:
        abort(404)
    return render_template('recipes/form.html', recipe=recipe)

@recipe_bp.route('/recipes/<int:id>/update', methods=['POST'])
def update_recipe(id):
    """
    接收表單資料並更新食譜。
    輸入: 食譜 id, 表單資料 (title, ingredients, steps, notes)
    邏輯: 驗證 title，呼叫 Recipe.update()
    輸出: 重導向至食譜詳情頁
    """
    # 先確認食譜存在
    recipe = Recipe.get_by_id(id)
    if not recipe:
        abort(404)

    title = request.form.get('title')
    ingredients = request.form.get('ingredients')
    steps = request.form.get('steps')
    notes = request.form.get('notes')

    # 基本輸入驗證
    if not title or title.strip() == '':
        flash('食譜名稱為必填欄位！')
        return redirect(url_for('recipe.edit_recipe', id=id))

    data = {
        'title': title.strip(),
        'ingredients': ingredients.strip() if ingredients else '',
        'steps': steps.strip() if steps else '',
        'notes': notes.strip() if notes else ''
    }

    success = Recipe.update(id, data)
    if success:
        flash('食譜已成功更新！')
        return redirect(url_for('recipe.recipe_detail', id=id))
    else:
        flash('更新食譜失敗，請稍後再試。')
        return redirect(url_for('recipe.edit_recipe', id=id))

@recipe_bp.route('/recipes/<int:id>/delete', methods=['POST'])
def delete_recipe(id):
    """
    刪除指定食譜。
    輸入: 食譜 id
    邏輯: 呼叫 Recipe.delete(id)
    輸出: 重導向至首頁
    """
    # 先確認食譜存在
    recipe = Recipe.get_by_id(id)
    if not recipe:
        abort(404)

    success = Recipe.delete(id)
    if success:
        flash('食譜已成功刪除！')
    else:
        flash('刪除食譜失敗，請稍後再試。')
    
    return redirect(url_for('recipe.index'))
