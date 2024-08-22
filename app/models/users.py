from app.extensions import db

class Users(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    login = db.Column(db.String(50))
    password = db.Column(db.String(50))

    def __repr__(self):
        return '<User %s>'%self.id