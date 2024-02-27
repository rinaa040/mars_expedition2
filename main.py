from flask import Flask, render_template, redirect
from data import db_session
from data.users import User
from data.news import News
from forms.users import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route("/")
def index():
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.is_private != True)
    return render_template("index.html", news=news)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


def main():
    db_session.global_init("db/mars_explorer.db")
    user = User()
    user2 = User()
    user3 = User()
    user.surname = "Scott"
    user.name = "Ridley"
    user.age = 21
    user.position = "captain"
    user.speciality = "research engineer"
    user.address = "module_1"
    user.email = "scott_chief@mars.org"

    user2.surname = "Stalina"
    user2.name = "Maria"
    user2.age = 16
    user2.position = "doctor"
    user2.speciality = "weed engineer"
    user2.address = "module_1"
    user2.email = "tofic_protasov@mars.org"

    user3.surname = "Abasheva"
    user3.name = "Arina"
    user3.age = 16
    user3.position = "chef"
    user3.speciality = "cooking dishes"
    user3.address = "module_1"
    user3.email = "arisha@mars.org"

    db_sess = db_session.create_session()
    db_sess.add(user)
    db_sess.add(user2)
    db_sess.add(user3)
    db_sess.commit()



    app.run()


if __name__ == '__main__':
    main()
