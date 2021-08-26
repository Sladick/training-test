from flask import Flask, render_template, request
from sqlalchemy import create_engine, Column, Integer, String,  ForeignKey, DateTime, Text
from sqlalchemy.orm import Session
from sqlalchemy.orm import declarative_base
Base = declarative_base()
app = Flask(__name__)
engine = create_engine('postgresql://sladick_db1:203320v@localhost/postgres', echo=True)


class ProfileUser(Base):
    __tablename__ = 'profile'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=True)
    middle_name = Column(String(50), nullable=True)
    bornDate = Column(DateTime, nullable=True)
    gender = Column(String(10), nullable=True)


class Comment(Base):
    __tablename__ = 'comment'

    education = Column(Integer, nullable=True)
    commentUser = Column(Text, nullable=True)
    citizenship = Column(Text, nullable=True)
    phone = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey('profile.id'), primary_key=True)

# Base.metadata.create_all(engine)


@app.route('/', methods=('POST', 'GET'))
def index():
    if request.method == "POST":
        with Session(engine) as session:
            session.begin()
            try:
                valid_Users = ProfileUser(name=request.form['userName'], middle_name=request.form['userSurname'],
                                    bornDate=request.form['dateBorn'], gender=request.form['gender'])
                session.add(valid_Users)  # если бы не было этих двух строк я бы завернул эти две переменные в функцию
                session.flush()  # и сделал к ней декоратор с сессией, а так, ничего придумать не могу :С
                valid_Comment = Comment(education=request.form['education'], commentUser=request.form['comment'],
                                        citizenship=request.form['citizen'], phone=request.form['phone'], user_id=valid_Users.id)
                session.add(valid_Comment)
            except:
                session.rollback()
                raise
            else:
                session.commit()

    return render_template("picture.html")


if __name__ == '__main__':
    app.run(debug=True)
