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


if __name__ == "__main__":
    app.run(debug=True)
