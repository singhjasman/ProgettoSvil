
from flask import Flask, render_template, request, redirect, url_for, flash, session
from database import connect_db
from werkzeug.security import generate_password_hash, check_password_hash
import os
import pymysql

app = Flask(__name__)

# Chiave utilizzata per proteggere le sessioni
app.secret_key = os.getenv("SECRET_KEY", "chiave-segreta-solo-per-sviluppo")


# HOMEPAGE
@app.route("/")
def home():
    return render_template("index.html")


# REGISTRAZIONE
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        # Controllo dei dati inseriti
        if not username or not email or not password:
            flash("Compila tutti i campi.")
            return redirect(url_for("register"))

        if len(password) < 8:
            flash("La password deve contenere almeno 8 caratteri.")
            return redirect(url_for("register"))

        # Creazione dell'hash della password
        password_hash = generate_password_hash(password)

        connection = connect_db()

        try:
            with connection.cursor() as cursor:

                # Verifichiamo se l'email è già registrata
                cursor.execute(
                    "SELECT id FROM users WHERE email = %s",
                    (email,)
                )

                if cursor.fetchone():
                    flash("Questa email è già registrata.")
                    return redirect(url_for("register"))

                # Inserimento del nuovo utente
                cursor.execute(
                    """
                    INSERT INTO users
                    (username, email, password, role, is_verified)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (username, email, password_hash, "user", False)
                )

            connection.commit()

            flash("Registrazione completata! Ora puoi accedere.")
            return redirect(url_for("login"))

        except pymysql.MySQLError:
            connection.rollback()
            flash("Si è verificato un errore durante la registrazione.")
            return redirect(url_for("register"))

        finally:
            connection.close()

    return render_template("register.html")


# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        connection = connect_db()

        try:
            with connection.cursor() as cursor:

                cursor.execute(
                    "SELECT * FROM users WHERE email = %s",
                    (email,)
                )

                user = cursor.fetchone()

        finally:
            connection.close()

        # Controllo delle credenziali
        if user and check_password_hash(user["password"], password):

            session.clear()
            session["user_id"] = user["id"]

            flash("Accesso effettuato!")
            return redirect(url_for("dashboard"))

        flash("Email o password non corretti.")
        return redirect(url_for("login"))

    return render_template("login.html")


# AREA PERSONALE
@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        flash("Effettua il login per continuare.")
        return redirect(url_for("login"))

    connection = connect_db()

    try:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT id, username, email, role
                FROM users
                WHERE id = %s
                """,
                (session["user_id"],)
            )

            user = cursor.fetchone()

    finally:
        connection.close()

    if not user:
        session.clear()
        return redirect(url_for("login"))

    return render_template("dashboard.html", user=user)


# LOGOUT
@app.route("/logout")
def logout():

    session.clear()
    flash("Hai effettuato la disconnessione.")

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
