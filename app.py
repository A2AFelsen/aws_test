# app.py
from flask import Flask, request, render_template
import login
import main_menu

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    # Get the form data
    username = request.form.get('username')
    password = request.form.get('password')
    action = request.form.get('action')

    if action == 'admin':
        return login.admin(username, password)
    elif action == 'login':
        return login.login(username, password)
    elif action == 'new_user':
        return login.new_user(username, password)
    else:
        return "How did you even get here?"


@app.route('/main_menu_submit', methods=['POST'])
def main_menu_submit():
    action = request.form.get('action')

    if action == 'character':
        main_menu.character()
    elif action == 'campaign':
        main_menu.campaign()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
