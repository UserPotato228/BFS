from app.extensions import db


class Files(db.Model):
    __tablename__ = "files"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    filepath = db.Column(db.String(255))
    folder_id = db.Column(db.Integer)
    owner_id = db.Column(db.Integer)

    def __repr__(self):
        return '<Files %s>'%self.id