# app.py
from flask import Flask, request, render_template
import login

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
        login.admin(username, password)
    elif action == 'login':
        login.login(username, password)
    elif action == 'new_user':
        login.new_user(username, password)


@app.route('/main_menu_submit', methods=['POST'])
def main_menu_submit():
    user_input = request.form.get('user_input_main_menu')
    return f"You have chosen {user_input}"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
