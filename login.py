import database_manager
import flask


def admin(username, password):
    if username == 'admin' and password == 'admin':
        return database_manager.get_all_users()
    else:
        return f"Incorrect Username '{username}' and Password '{password}'"


def login(username, password):
    output, msg = database_manager.login_user(username, password)
    if not output:
        return f"Incorrect Username '{username}' and Password '{password}'"
    return flask.render_template('main_menu.html', username=username)


def new_user(username, password):
    output, msg = database_manager.add_new_user(username, password)
    return flask.render_template('main_menu.html', username=(username + ' (New User!)'))