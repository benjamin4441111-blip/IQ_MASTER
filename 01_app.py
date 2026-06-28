from flask import Flask, render_template, request, redirect, url_for, flash

from flask_sqlalchemy import SQLAlchemy

from flask_login import (

    LoginManager,

    UserMixin,

    login_user,

    logout_user,

    login_required,
    current_user
)

from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your_secret_key_here')

database_url = os.environ.get('DATABASE_URL', 'sqlite:///database.db')
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = database_url

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)



login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "login"



# =======================

# DATABASE MODELS

# =======================


class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100), unique=True)

    email = db.Column(db.String(120), unique=True)

    password = db.Column(db.String(200))

    iq_score = db.Column(db.Integer, default=0)


    correct = db.Column(db.Integer, default=0)

    incorrect = db.Column(db.Integer, default=0)

    skipped = db.Column(db.Integer, default=0)

    avg_time = db.Column(db.Float, default=0)


    country = db.Column(

    db.String(100),

    default="India"
)


tests_taken = db.Column(

    db.Integer,

    default=0
)



@login_manager.user_loader

def load_user(user_id):

    return User.query.get(int(user_id))



# =======================

# HOME

# =======================


@app.route("/")

def home():

    return render_template("index.html")



# =======================

# REGISTER

# =======================


@app.route("/register", methods=["GET", "POST"])

def register():


    if request.method == "POST":

        username = request.form["username"]

        email = request.form["email"]

        password = request.form["password"]


        user = User.query.filter_by(email=email).first()


        if user:

            flash("Email already exists!")
            return redirect(url_for("register"))


        hashed = generate_password_hash(password)


        new_user = User(

            username=username,

            email=email,

            password=hashed
        )


        db.session.add(new_user)

        db.session.commit()


        flash("Registration successful!")
        return redirect(url_for("login"))


    return render_template("register.html")



# =======================

# LOGIN

# =======================


@app.route("/login", methods=["GET", "POST"])

def login():


    if request.method == "POST":

        email = request.form["email"]

        password = request.form["password"]


        user = User.query.filter_by(email=email).first()


        if user and check_password_hash(

                user.password,

                password):

            login_user(user)

            return redirect(url_for("dashboard"))


        flash("Invalid email or password")


    return render_template("login.html")



# =======================

# DASHBOARD

# =======================


@app.route("/dashboard")
def dashboard():

    correct = current_user.correct
    incorrect = current_user.incorrect
    skipped = current_user.skipped

    accuracy = round(
    (correct / (correct + incorrect + skipped)) * 100 if (correct + incorrect + skipped) > 0 else 0,
    2
)

    iq_score = 80 + (correct * 2)
    
    return render_template(
       "dashboard.html",
       correct=correct,
       incorrect=incorrect,
       skipped=skipped,
       accuracy=accuracy,
       iq_score=iq_score
    )


  



# =======================

# QUIZ

# =======================


@app.route("/quiz")

@login_required

def quiz():

    return render_template("quiz.html")



# =======================

# SAVE SCORE

# =======================


@app.route("/save_score", methods=["POST"])

@login_required

def save_score():

    current_user.correct = int(

        request.form["correct"]
    )

    current_user.incorrect = int(

        request.form["incorrect"]
    )


    current_user.skipped = int(

        request.form["skipped"]
    )


    current_user.avg_time = float(

        request.form["avg_time"]
    )


    current_user.iq_score = int(

        request.form["iq_score"]
    )


    db.session.commit()


    return redirect(url_for("dashboard"))



# =======================

# LEADERBOARD

# =======================


@app.route("/leaderboard")

def leaderboard():


    users = User.query.order_by(

        User.iq_score.desc()
    ).all()

    return render_template(

        "leaderboard.html",
        users=users
    )



# =======================

# LOGOUT

# =======================


@app.route("/logout")

@login_required

def logout():

    logout_user()

    return redirect(url_for("home"))



# =======================

# PROFILE

# =======================
@app.route('/profile')
@login_required
def profile():
    user = current_user
    avg_iq = round(user.iq_score / user.tests_taken, 1) if user.tests_taken > 0 else 0
    total_questions = user.correct + user.incorrect + user.skipped
    correct_pct = round(user.correct / total_questions * 100, 1) if total_questions else 0
    incorrect_pct = round(user.incorrect / total_questions * 100, 1) if total_questions else 0
    skipped_pct = round(user.skipped / total_questions * 100, 1) if total_questions else 0
    return render_template('profile.html',
                           user=user,
                           avg_iq=avg_iq,
                           total_questions=total_questions,
                           correct_pct=correct_pct,
                           incorrect_pct=incorrect_pct,
                           skipped_pct=skipped_pct)



# =======================

# MAIN

# =======================

with app.app_context():
    db.create_all()

if __name__ == "__main__":

    


    app.run(debug=True)