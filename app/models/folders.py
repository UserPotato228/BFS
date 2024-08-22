from app.extensions import db

class Folders(db.Model):
    __tablename__ = "folders"

    id = db.Column(db.Integer, primary_key =True, autoincrement=True)
    owner_id = db.Column(db.Integer)
    name = db.Column(db.Text)

    def __repr__(self):
        return '<Folders %s>'%self.id