import os
from datetime import datetime

import config
from app.folder import bp
from flask import render_template, session, redirect, request, send_from_directory, send_file, make_response
from app.extensions import db
from app.models.users import Users
from app.models.folders import Folders
from app.models.files import Files
from config import Config

def check_ext(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS


class File:
    def __init__(self, name, ext, id):
        self.id = id
        self.name = name
        self.ext = ext

@bp.route("/<int:id>")
def folder(id):
    if "login" not in session:
        return redirect('/login')
    profile = db.session.query(Users).filter((Users.login == session['login']) & (Users.password == session['password'])).first()
    folders = db.session.query(Folders).filter((Folders.owner_id == profile.id)).all()
    files = db.session.query(Files).filter((Files.owner_id == profile.id) & (Files.folder_id == id)).all()
    folder = db.session.query(Folders).filter((Folders.owner_id == profile.id)&(Folders.id == id)).first()
    files_prepare = []
    for file in files:
        ext = file.name.split('.')[len(file.name.split('.'))-1]
        for i in config.formats:
            if ext.lower() in config.formats[i]:
                ext = i
                continue
        files_prepare.append(File(id=file.id, name=file.name, ext=ext))

    return render_template("folder.html", folders=folders, id=id, files=files_prepare, title=folder.name)


@bp.route("/<int:id>/upl_files", methods=['POST', "GET"])
def updload_files(id):
    files = request.files.getlist("files")
    print(files)
    profile = db.session.query(Users).filter((Users.login == session['login']) & (Users.password == session['password'])).first()
    folder = db.session.query(Folders).filter((Folders.id == id) & (Folders.owner_id == profile.id)).first()
    if not profile or not folder:
        return "<script>alert('ОШИБКА'); history.go(-1);</script>"


    for file in files:
        mask_name = "%d%d%s.%s"%(profile.id, id, datetime.now().strftime('%d%m%Y%H%M%S%f'), file.filename.split('.')[len(file.filename.split('.'))-1])
        print(mask_name)
        file.save(os.path.join(Config.UPLOAD_FOLDER, mask_name))
        file_record = Files(name=file.filename, filepath=mask_name, folder_id=id, owner_id=profile.id, )
        db.session.add(file_record)
        db.session.commit()

    return redirect("/%d"%id)

@bp.route("/<int:id_fldr>/<int:id_file>")
def show_file(id_fldr, id_file):
    if "login" not in session:
        return redirect("/")
    profile = db.session.query(Users).filter((Users.login == session['login']) & (Users.password == session['password'])).first()
    folder = db.session.query(Folders).filter((Folders.id == id_fldr) & (Folders.owner_id == profile.id)).first()
    if not profile or not folder:
        session.pop('login', None)
        session.pop('password', None)
        return redirect("/login")

    file = db.session.query(Files).filter((Files.owner_id==profile.id)&(Files.folder_id==id_fldr)&(Files.id==id_file)).first()
    if not file:
        return redirect("/")
    print(os.path.join(Config.UPLOAD_FOLDER, file.filepath))
    return send_from_directory(os.path.join(Config.UPLOAD_FOLDER), file.filepath, as_attachment=True, download_name=file.name)


@bp.route("/<int:id_fldr>/del_files", methods=["GET", "POST"])
def delete_files(id_fldr):
    profile = db.session.query(Users).filter(
        (Users.login == session['login']) & (Users.password == session['password'])).first()
    folder = db.session.query(Folders).filter((Folders.id == id_fldr) & (Folders.owner_id == profile.id)).first()
    if not profile or not folder:
        return "<script>alert('ОШИБКА'); history.go(-1);</script>"

    files = request.get_json()
    print(files)
    for i in files:
        print(i)
        file = db.session.query(Files).filter(Files.id==int(i['id'])).first()
        os.remove(os.path.join(Config.UPLOAD_FOLDER, file.filepath))
        db.session.delete(file)
        db.session.commit()
    return make_response("OK", 200)

@bp.route("/<int:fldr_id>/rn_file", methods=["GET", "POST"])
def rename_file(fldr_id):
    profile = db.session.query(Users).filter(
        (Users.login == session['login']) & (Users.password == session['password'])).first()
    folder = db.session.query(Folders).filter((Folders.id == fldr_id) & (Folders.owner_id == profile.id)).first()
    if not profile or not folder:
        return "<script>alert('ОШИБКА'); history.go(-1);</script>"

    new_name = request.form.get("file_name", None) or None
    file_id = request.form.get("file_id", None) or None

    file = db.session.query(Files).filter((Files.id==file_id)&(Files.owner_id==profile.id)&(Files.folder_id==fldr_id)).first()
    if not file:
        return "<script>alert('ОШИБКА'); history.go(-1);</script>"

    db.session.query(Files).filter(Files.id==file_id).update({"name":new_name+"."+file.name.split('.')[len(file.name.split('.'))-1]})
    db.session.commit()

    return redirect("/%d"%fldr_id)