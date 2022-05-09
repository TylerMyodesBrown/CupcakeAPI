from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()



class Cupcake(db.Model):
    """Cupcake"""

    __tablename__ = "employees"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    flavor = db.Column(db.Text, nullable=False)
    size = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float)
    image = db.Column(db.Text, default='https://tinyurl.com/demo-cupcake')


    def __repr__(self):
        e = self
        return f"<Cupcake Info - ID: {e.id} Flavor: {e.flavor} Size: {e.size} Rating: {e.rating}>"