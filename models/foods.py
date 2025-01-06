from database import db

class Foods(db.Model):
    __tablename__ = 'foods'  # Nome opcional da tabela

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    date = db.Column(db.String(20), nullable=False)
    hour = db.Column(db.String(10), nullable=False)
    diet = db.Column(db.Boolean, default=False)

    def to_dict(self):
        """Converte a instância do modelo em um dicionário."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "date": self.date,
            "hour": self.hour,
            "diet": self.diet
        }