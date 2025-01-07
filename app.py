from flask import Flask, request, jsonify
from models.foods import Foods
from database import db

app = Flask(__name__)
app.config['SECRET_KEY'] = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///foods.db'

db.init_app(app)

id_control = 1

@app.route("/foods", methods=["POST"])
def create_food():
    global id_control
    data = request.get_json()

    name=data.get("name")
    description=data.get("description")
    date=data.get("date")
    hour=data.get("hour")
    diet=data.get("diet")

    if not all([name, description, date, hour, diet is not None]):
        return jsonify({"message": "Credenciais inválidas"}), 400
    
    new_food = Foods(
        name=name,
        description=description,
        date=date,
        hour=hour,
        diet=bool(diet)
    )

    try:
        db.session.add(new_food)
        db.session.commit()
        id_control += 1  # Incrementar o controle de ID
        return jsonify({"message": "Refeição registrada com sucesso"}), 200
    
    except Exception as e:
        db.session.rollback()  # Reverter alterações em caso de erro
        return jsonify({"message": "Erro ao registrar a refeição", "error": str(e)}), 500

@app.route("/food/<int:id>", methods=["GET"])
def read_food(id):
    food = Foods.query.get(id)

    if food:
        return jsonify({
            "name": food.name,
            "description": food.description,
            "date": food.date,
            "hour": food.hour,
            "diet": food.diet,
        }), 200

    return jsonify({"message": "Registro não encontrado"}), 404

@app.route("/food/<int:id>", methods=["PUT"])
def update_food(id):
    data = request.json
    food = Foods.query.get(id)

    if food and data.get("name") or data.get("description") or data.get("date") or data.get("hour") or data.get("diet"):
        food.name = data.get("name")
        food.description = data.get("description")
        food.date = data.get("date")
        food.hour = data.get("hour") 
        food.diet = data.get("diet") 
        db.session.commit()

        return jsonify({"message": f"A refeição {id} atualizada com sucesso"})

    return jsonify({"message": "Registro não encontrado"}), 404

@app.route("/food/<int:id>", methods=["DELETE"])
def delete_food(id):
    food = Foods.query.get(id)

    if food:
        db.session.delete(food)
        db.session.commit()
        return jsonify({"message": f"Comida {id} deletado com sucesso"})

    return jsonify({"message": "Registro não encontrado"}), 404

@app.route("/foods", methods=["GET"])
def list_food():
    
    try:
        foods = Foods.query.all()  # Consulta ao banco
        if not foods:
            return jsonify({"message": "Nenhuma refeição encontrada."}), 200
        
        foods_list = [food.to_dict() for food in foods]
        return jsonify(foods_list), 200

    except Exception as e:
        return jsonify({"message": "Erro ao listar as refeições", "error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
