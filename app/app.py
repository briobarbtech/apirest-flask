from CONFIG import config
from flask import Flask, request, jsonify
from http import HTTPStatus as http


app = Flask(__name__)  # Inicializamos flask en una variable

recipes = [
    {
        'id': 1,
        'name': 'Egg Salad',
        'description': 'This is a lovely egg salad recipe.'
    },
    {
        'id': 2, 'name': 'Tomato Pasta',
        'description': 'This is a lovely tomato pasta recipe.'
    }
]

### Get all recipes ###
@app.route("/recipes")
def get_all_recipes():
    return jsonify({"data": recipes}), http.OK

### Get a specific recipe ###
@app.route('/recipes/<int:id>')
def get_spec_recipe(id):
    recipe = ""
    for recipe in recipes:
        if recipe['id']==id:
            recipe=recipe

    if recipe:
        return jsonify(recipe), http.OK
    return jsonify({'message': 'recipe not found'}), http.NOT_FOUND

### create a recipe ###
@app.route('/recipes', methods=['POST'])
def create_recipe():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    recipe = {
        'id': recipes[-1]['id']+1,
        'name': name,
        'description': description
    }
    recipes.append(recipe)
    return jsonify(recipes), http.CREATED

### Update a recipe ###
@app.route('/recipes/<int:id>', methods=['PUT'])
def update_recipe(id):
    recipe = next((recipe for recipe in recipes if recipe['id'] == id), None)
    if not recipe:
        return jsonify({'message': 'recipe NOT found'}), http.NOT_FOUND
    data = request.get_json()
    recipe.update(
        {
            'name': data.get('name'),
            'description': data.get('description')
        }
    )
    return jsonify(recipe), http.OK

### Delete a recipe ###
@app.route('/recipes/<int:id>', methods=['DELETE'])
def delete_recipe(id):
    recipe = next((recipe for recipe in recipes if recipe['id']==id), None)

    if not recipe:
        return jsonify({'message':'recipe NOT found'}), http.NOT_FOUND
    recipes.remove(recipe)
    return '', http.NO_CONTENT


if __name__ == "__main__":
    app.config.from_object(config['developmentConfig'])
    app.run()