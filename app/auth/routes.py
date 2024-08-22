# import blueprints
from app.auth import bp
# flask modules
from flask import request, redirect, session, render_template
# db conn
from app.extensions import db
from app.models.users import Users

@bp.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if "login" in session:
            return redirect('/')
        return render_template("login.html")
    else:
        login = request.form.get("login", None) or None
        password = request.form.get("password", None) or None

        user = db.session.query(Users).filter((Users.login==login)&(Users.password==password)).first() or None
        if not user:
            return ("<script>alert('неверный логин или пароль!'); history.go(-1)</script>")

        session['login'] = login
        session['password'] = password

        return ("<script>alert('Вы успешно авторизировались!'); location.href='/'</script>")


@bp.route("/reg", methods=["GET", "POST"])
def reg():
    if request.method == "GET":
        if "login" in session:
            return redirect("/")
        return render_template("reg.html")
    else:
        login = request.form.get("login", None) or None
        password = request.form.get("password", None) or None
        agn_password = request.form.get("agn_password", None) or None

        if password != agn_password:
            return("<script>alert('Пароли не совпадают!'); history.go(-1)</script>")

        profiles = db.session.query(Users).filter((Users.login == login)).all()
        if len(profiles)>0:
            return ("<script>alert('Логин занят.'); history.go(-1)</script>")

        profile = Users(login=login, password=password)
        db.session.add(profile)
        db.session.commit()

        return ("<script>alert('Вы успешно прошли регистрацию!'); location.href='/login'</script>")

@bp.route('/logout')
def logout():
    session.pop('login', None)
    session.pop('password', None)
    return "<script>alert('Вы покинули учетную запись.'); location.href='/login'</script>"

