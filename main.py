import app
from flask import Flask, render_template, redirect
from data import db_session
from data.users import User
from data.news import News
from data.jobs import Jobs
from forms.users import RegisterForm
from forms.login import LoginForm
from flask_login import LoginManager, current_user, login_user

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)




@app.route("/")
def index():
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.is_private != True)
    return render_template("index.html", news=news)


@app.route('/register', methods=['GET', 'POST'])
def register():
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
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         db_sess = db_session.create_session()
#         jobs = Jobs()
#         jobs.team_leader = form.team_leader.data
#         jobs.job = form.job.data
#         jobs.work_size = form.work_size.data
#         jobs.collaborations = form.collaborations.data
#         jobs.is_finished = form.is_finished
#         current_user.jobs.append(jobs)
#         db_sess.merge(current_user)
#         db_sess.commit()
#         return redirect("/")
#
#     return render_template('login.html', title='Добавление работы', form=form)
#

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
    user.email = "scott_chief5678@mars.org"
    user.set_password("123")

    # user2.surname = "Stalina"
    # user2.name = "Maria"
    # user2.age = 16
    # user2.position = "doctor"
    # user2.speciality = "weed engineer"
    # user2.address = "module_1"
    # user2.email = "tofic_protasov@mars.org"
    #
    # user3.surname = "Abasheva"
    # user3.name = "Arina"
    # user3.age = 16
    # user3.position = "chef"
    # user3.speciality = "cooking dishes"
    # user3.address = "module_1"
    # user3.email = "arisha@mars.org"

    db_sess = db_session.create_session()
    db_sess.add(user)
    # db_sess.add(user2)
    # db_sess.add(user3)
    db_sess.commit()

    app.run()


if __name__ == '__main__':
    main()
