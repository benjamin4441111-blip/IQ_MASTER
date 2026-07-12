from flask import Flask, render_template, request, redirect, url_for, flash, session

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
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your_secret_key_here')


database_url = os.environ.get('DATABASE_URL', 'sqlite:///database.db')
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = database_url

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.environ.get('GOOGLE_CLIENT_ID'),
    client_secret=os.environ.get('GOOGLE_CLIENT_SECRET'),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)



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

    google_id = db.Column(db.String(200), unique=True, nullable=True)

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

def home_page():

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

            return redirect(url_for("home_inside"))


        flash("Invalid email or password")


    return render_template("login.html")


@app.route("/auth/google")
def google_login():
    redirect_uri = url_for("google_callback", _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route("/auth/google/callback")
def google_callback():
    token = google.authorize_access_token()
    user_info = token["userinfo"]

    email = user_info["email"]
    name = user_info.get("name", email.split("@")[0])
    google_id = user_info.get("sub")

    user = User.query.filter_by(email=email).first()

    if not user:
        base_username = name.replace(" ", "_").lower()
        username = base_username
        counter = 1
        while User.query.filter_by(username=username).first():
            username = f"{base_username}{counter}"
            counter += 1

        user = User(
            username=username,
            email=email,
            password=None,
            google_id=google_id
        )
        db.session.add(user)
        db.session.commit()
    elif not user.google_id:
        user.google_id = google_id
        db.session.commit()

    login_user(user)
    return redirect(url_for("home_inside"))



# =======================

# DASHBOARD

# =======================


@app.route("/dashboard")
@login_required
def dashboard():
    recent = session.get('recent', {
        'correct': 0,
        'incorrect': 0,
        'skipped': 0,
        'avg_time': 0,
        'iq_score': 0
    })

    correct = recent['correct']
    incorrect = recent['incorrect']
    skipped = recent['skipped']

    accuracy = round(
        (correct / (correct + incorrect + skipped)) * 100 if (correct + incorrect + skipped) > 0 else 0,
        2
    )

    return render_template(
        "dashboard.html",
        correct=correct,
        incorrect=incorrect,
        skipped=skipped,
        accuracy=accuracy,
        iq_score=recent['iq_score']
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
    correct = int(request.form["correct"])
    incorrect = int(request.form["incorrect"])
    skipped = int(request.form["skipped"])
    avg_time = float(request.form["avg_time"])
    iq_score = int(request.form["iq_score"])

    # Add to all-time totals
    current_user.correct += correct
    current_user.incorrect += incorrect
    current_user.skipped += skipped
    current_user.iq_score += iq_score
    current_user.avg_time = avg_time
    

    db.session.commit()

     # Save THIS test's result separately (for dashboard)
    session['recent'] = {
        'correct': correct,
        'incorrect': incorrect,
        'skipped': skipped,
        'avg_time': avg_time,
        'iq_score': iq_score
    }

    return redirect(url_for("dashboard"))




# =======================

# LEADERBOARD

# =======================


@app.route("/leaderboard")
def leaderboard():

    filter_type = request.args.get("filter", "global")

    query = User.query.filter(User.iq_score > 0)

    if filter_type == "country" and current_user.is_authenticated and current_user.country:
        query = query.filter(User.country == current_user.country)

    users = query.order_by(User.iq_score.desc()).all()

    my_rank = None
    if current_user.is_authenticated:
        for idx, u in enumerate(users, start=1):
            if u.id == current_user.id:
                my_rank = idx
                break

    return render_template(
        "leaderboard.html",
        users=users,
        filter_type=filter_type,
        my_rank=my_rank
    )



# =======================

# LOGOUT

# =======================

@app.route("/logout")
@login_required
def logout():
    from flask_login import logout_user
    logout_user()
    return redirect(url_for("index.html"))



# =======================

# PROFILE

# =======================
@app.route('/profile')
@login_required
def profile():
    user = current_user
    total_questions = user.correct + user.incorrect + user.skipped
    tests_taken = max(1, round(total_questions / 20))  # Assuming each test has 20 questions
    avg_iq = round(user.iq_score / tests_taken, 1) if tests_taken > 0 else 0
    
    correct_pct = round(user.correct / total_questions * 100, 1) if total_questions else 0
    incorrect_pct = round(user.incorrect / total_questions * 100, 1) if total_questions else 0
    skipped_pct = round(user.skipped / total_questions * 100, 1) if total_questions else 0
    return render_template('profile.html',
                           user=user,
                           avg_iq=avg_iq,
                           total_questions=total_questions,
                           tests_taken=tests_taken,
                           correct_pct=correct_pct,
                           incorrect_pct=incorrect_pct,
                           skipped_pct=skipped_pct)


# ================

# debug column

#=================

@app.route('/debug_columns')
def debug_columns():
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    columns = [col['name'] for col in inspector.get_columns('user')]
    return {"columns": columns}





#==============

#HOME

#==============

@app.route("/home")
@login_required
def home_inside():
    return render_template("home.html", user=current_user)


#============
#category
#===========
@app.route("/category")
@login_required
def category():
    return render_template("category.html")














# =======================

# MAIN

# =======================

with app.app_context():
    db.create_all()

    from sqlalchemy import text
    try:
        db.session.execute(text('ALTER TABLE "user" ADD COLUMN tests_taken INTEGER DEFAULT 0'))
        db.session.commit()
        print("tests_taken column added successfully")
    except Exception as e:
        db.session.rollback()
        print("Column might already exist:", e)

if __name__ == "__main__":
    app.run(debug=True)