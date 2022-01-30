from flask import Flask, render_template, request, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import smtplib

EMAIL = ""
PASSWORD = ""



class Addpost(FlaskForm):
    title = StringField(label="title", validators=[DataRequired()])
    sub = StringField(label="sub", validators=[DataRequired()])
    cont = TextAreaField(label="cont", validators=[DataRequired()])
    submit = SubmitField(label="Submit")



class Login(FlaskForm):
    username = StringField(label="Username", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    submit = SubmitField(label="Log in")


conection = sqlite3.connect("PostsData.db",check_same_thread=False)
cursor = conection.cursor()


class Post():

    def __init__(self, postd):
        self.title = postd[0]
        self.sub = postd[1]
        self.cont = postd[2]
        cursor.execute("INSERT INTO posts VALUES (:title, :sub, :cont)", {'title':self.title, 'sub': self.sub, 'cont':self.cont})
        conection.commit()




app = Flask(__name__)
app.secret_key = "QTSFAG-QGSGQJ-SQHUSWK"



conection1 = sqlite3.connect("users.db", check_same_thread=False)
cursor1 = conection1.cursor()


class User():
    def __init__(self):
         self.authenticated = 0

    def atuth(self):
        self.authenticated +=1

    def log(self):
        self.authenticated -= self.authenticated



usera = User()


@app.route("/")
def home():
    cursor.execute("SELECT * FROM posts")
    conection.commit()
    post = cursor.fetchall()
    return render_template("index.html", posts=reversed(post))


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/post/<id>")
def post(id):
    cursor.execute("SELECT * FROM posts WHERE title=:title",{'title':id})
    conection.commit()
    post = cursor.fetchall()
    title = post[0][0]
    sub = post[0][1]
    cont = post[0][2]

    return render_template("posts.html", title=title, sub=sub, cont=cont)


@app.route("/form-entry", methods=["POST"])
def get_form():
    form = request.form
    send_email(form["name"], form["email"], form["text"])
    return render_template("sent.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    login = Login()
    admin = 0
    if login.validate_on_submit():
        user2 = login.username.data
        passw = login.password.data

        cursor1.execute("SELECT * FROM user WHERE user=:user", {'user': user2})
        conection1.commit()
        user1 = cursor1.fetchall()


        if len(user1) == 0:
            admin -=1
        elif check_password_hash(user1[0][1], passw) and user2 == user1[0][0]:
            usera.atuth()
            return redirect(url_for('admin'))
        else:
            admin -= 1

    return render_template("login.html", form=login, admin=admin)



@app.route("/addpost", methods=["GET","POST"])
def add_post():
    global usera
    if usera.authenticated >=1:
        addpost = Addpost()
        if addpost.validate_on_submit():
            title = addpost.title.data
            sub = addpost.sub.data
            cont = addpost.cont.data
            post = [title,sub,cont]
            Post(post)

        return render_template("add.html", form= addpost)
    else:
        return redirect(url_for('login'))


@app.route("/delete", methods=["GET"])
def delete():
    global usera
    if usera.authenticated >= 1:
        cursor.execute("SELECT * FROM posts")
        conection.commit()
        post = cursor.fetchall()
        return render_template("delete.html",posts=reversed(post))
    else:
        return redirect(url_for('login'))


@app.route("/delete1/<id>",methods=["GET","POST"])
def delete_post(id):
    global usera
    if usera.authenticated >=1:
        cursor.execute("DELETE FROM posts WHERE title=:title", {'title': id})
        conection.commit()
        return render_template("deleted.html")
    else:
        return redirect(url_for('login'))


@app.route("/admin")
def admin():
    global usera
    if usera.authenticated >= 1:
        return render_template("admin.html")
    else:
        return redirect(url_for('login'))



@app.route('/logout')
def logout():
    usera.log()
    return redirect(url_for("home"))





def send_email(name, email, message):
    email_message = f"Subject:New Message\n\nName: {name}\nEmail: {email}\nMessage:{message}"
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(EMAIL, PASSWORD)
        connection.sendmail(EMAIL, EMAIL, email_message)


if __name__ == "__main__":
    app.run()
