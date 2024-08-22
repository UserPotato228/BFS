# import blueprint
import os.path

import flask

from app.index import bp
# flask modules
from flask import render_template, session, redirect, request

from app.models.files import Files
from app.models.users import Users
from app.extensions import db
from app.models.folders import Folders
from config import Config

@bp.route('/')
def index():
    if "login" not in session:
        return redirect('/login')
    profile = db.session.query(Users).filter((Users.login == session['login']) & (Users.password == session['password'])).first()
    folders = db.session.query(Folders).filter(Folders.owner_id == profile.id).all()
    return render_template('index.html', folders=folders)

@bp.route('/new_fldr', methods=["GET", "POST"])
def new_folder():
    if "login" not in session:
        return redirect('/login')
    name = request.form.get('folder_name', None) or None
    if not name:
        return "<script>alert('Введите имя!'); history.go(-1);</script>"

    profile = db.session.query(Users).filter((Users.login==session['login'])&(Users.password == session['password'])).first()
    new_folder = Folders(owner_id = profile.id, name = name)
    db.session.add(new_folder)
    db.session.commit()
    return redirect("/")

@bp.route('/ren_fldr', methods=['GET', 'POST'])
def rename_folder():
    if "login" not in session:
        return redirect('/login')
    name = request.form.get("folder_name", None) or None
    folder_id = request.form.get("folder_id", None) or None

    if not folder_id: return "<script>alert('Ошибка!'); history.go(-1);</script>";
    if not name: return redirect("/");

    profile = db.session.query(Users).filter((Users.login == session['login']) & (Users.password == session['password'])).first()
    folder = db.session.query(Folders).filter((Folders.id == folder_id)&(Folders.owner_id == profile.id)).first()

    if not folder: return "<script>alert('Ошибка!'); history.go(-1);</script>";

    db.session.query(Folders).filter((Folders.id == folder_id)&(Folders.owner_id == profile.id)).update({"name":name})
    db.session.commit()

    return redirect("/")

@bp.route("/del_fldr", methods=["GET", "POST"])
def delete_folders():
    profile = db.session.query(Users).filter(
        (Users.login == session['login']) & (Users.password == session['password'])).first()
    if not profile:
        return "<script>alert('ОШИБКА'); history.go(-1);</script>"

    folders = request.get_json()

    for i in folders:
        folder = db.session.query(Folders).filter((Folders.id==i['id'])&(Folders.owner_id==profile.id)).first()
        if folder:
            files = db.session.query(Files).filter(Files.folder_id==i['id']).all()
            for n in files:
                os.remove(os.path.join(Config.UPLOAD_FOLDER, n.filepath))
                db.session.delete(n)
                db.session.commit()
            db.session.delete(folder)
            db.session.commit()

    return flask.make_response("OK", 200)
