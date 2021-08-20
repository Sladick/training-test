from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://host:password@adres/dataBase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Profile(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    middle_name = db.Column(db.String(50), nullable=True)
    bornDate = db.Column(db.DateTime, nullable=True)
    gender = db.Column(db.String(10), nullable=True)


class Comment(db.Model):
    education = db.Column(db.Integer, nullable=True)
    comment = db.Column(db.Text, nullable=True)
    citizenship = db.Column(db.Text, nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('profile.user_id'), primary_key=True)


@app.route('/', methods=('POST', 'GET'))
def index():
    if request.method == "POST":

        try:
            valid_Users = Profile(name=request.form['userName'], middle_name=request.form['userSurname'],
                                bornDate=request.form['dateBorn'], gender=request.form['gender'])
            db.session.add(valid_Users)
            db.session.flush()

            valid_Comment = Comment(education=request.form['education'], comment=request.form['comment'],
                                    citizenship=request.form['citizen'], user_id = valid_Users.user_id)

            db.session.add(valid_Comment)
            db.session.commit()
        except:
            db.session.rollback()
            print('error db')

    return render_template("picture.html")


if __name__ == '__main__':
    app.run(debug=True)
