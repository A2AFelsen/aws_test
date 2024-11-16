# app.py
from flask import Flask, request, render_template
import database_manager

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    # Get the form data
    username = request.form.get('username')
    password = request.form.get('password')
    
    # For now, let's just print it (you could process it here)
    print(f"Received username: {username}")
    print(f"Received password: {password}")

    with open("submit.txt", "w") as fl:
        fl.write(f"Received username: {username}\n")
        fl.write(f"Received password: {password}\n")

    msg = "Incorrect Username/Password!"
    if username == "admin" and password == "admin":
        output, msg = database_manager.get_all_users()
        msg += f"\n\nusername == {username}\npassword == {password}"
    else:
        msg += f"\n\nusername = {username}\npassword = {password}"
    return msg


@app.route('/main_menu_submit', methods=['POST'])
def main_menu_submit():
    user_input = request.form.get('user_input_main_menu')
    return f"You have chosen {user_input}"


@app.route('/login', methods=['POST'])
def login():
    # Get the form data
    username = request.form.get('username')
    password = request.form.get('password')
    
    # For now, let's just print it (you could process it here)
    print(f"Received username: {username}")
    print(f"Received password: {password}")

    with open("login.txt", "w") as fl:
        fl.write(f"Received username: {username}\n")
        fl.write(f"Received password: {password}\n")

    output, msg = database_manager.login_user(username, password)

    if not output:
        return "Failed to Login"

    return render_template('main_menu.html', username=username) 
    
    with open("logged_in.html", "r") as fl:
        content = fl.read()    
    return content


@app.route('/new_user', methods=['POST'])
def new_user():
    # Get the form data
    username = request.form.get('username')
    password = request.form.get('password')
    
    # For now, let's just print it (you could process it here)
    print(f"Received username: {username}")
    print(f"Received password: {password}")

    with open("new_user.txt", "w") as fl:
        fl.write(f"Received username: {username}\n")
        fl.write(f"Received password: {password}\n")

    output, msg = database_manager.add_new_user(username, password)
    return msg


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
