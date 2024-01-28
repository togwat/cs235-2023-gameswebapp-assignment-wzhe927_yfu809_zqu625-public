from flask import Blueprint, render_template, redirect, url_for, session
import games.authentication.services as services

authentication_blueprint = Blueprint('authentication_bp', __name__)


@authentication_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    """Goes to the login page, or authenticates with login form"""
    form = services.LoginForm()

    login_fail = False

    if form.validate_on_submit():  # form is submitted, POST request sent
        # authenticate user
        repo_user = services.get_user(form.username.data)
        # if user exists and password matches
        if repo_user is not None and services.check_password(
                form.password.data, repo_user.password):

            # initialise session
            session.clear()
            session['username'] = repo_user.username

            # redirect to profile
            return redirect(url_for('profile_bp.profile'))

        # password fails
        login_fail = True

    return render_template('authentication/login.html',
                           form=form, login_fail=login_fail)


@authentication_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    """Goes to the register page, or register new user with register form"""
    form = services.RegisterForm()
    username_fail = False
    password_confirm_fail = False

    if form.validate_on_submit():
        try:
            # add new user into repo, redirect to login page
            services.add_user(form.username.data, form.password.data)
            return redirect(url_for('authentication_bp.login'))

        except services.NameNotUniqueException:
            username_fail = True

    # password confirm check, uses default message
    if 'password_repeat' in form.errors or 'password' in form.errors:
        password_confirm_fail = True

    return render_template('authentication/register.html',
                           form=form,
                           username_fail=username_fail,
                           password_confirm_fail=password_confirm_fail)
