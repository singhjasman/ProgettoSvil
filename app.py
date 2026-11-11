
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_login import UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Configurazione
app.config["SECRET_KEY"] = "cinehub-chiave-segreta"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cinehub.db"

# Database
db = SQLAlchemy(app)

# Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# Tabella utenti
class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


# HOMEPAGE
@app.route("/")
def home():
    return render_template("index.html")


# REGISTRAZIONE
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user:
            flash("Email già registrata!")
            return redirect(url_for("register"))

        password_hash = generate_password_hash(password)

        nuovo_utente = User(
            username=username,
            email=email,
            password=password_hash
        )

        db.session.add(nuovo_utente)
        db.session.commit()

        flash("Registrazione completata! Ora puoi accedere.")
        return redirect(url_for("login"))

    return render_template("register.html")


# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):

            login_user(user)

            return redirect(url_for("profile"))

        else:
            flash("Email o password errati!")

    return render_template("login.html")


# PROFILO
@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html")


# LOGOUT
@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(url_for("home"))


# AVVIO APPLICAZIONE
if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    app.run(debug=True, port=5000)
