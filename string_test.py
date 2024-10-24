from flask import Flask
from flask import request
from flask import render_template

app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template("my-form.html") # This should be the name of your HTML file

@app.route('/', methods=['POST'])
def my_form_post():
    text1 = request.form['text1']
    text2 = request.form['text2']

    with open("text_test.txt", "w") as fl:
        fl.write(f"text1 = {text1}\n")
        fl.write(f"text2 = {text2}")
    
    if text1 == text2:
        return "<h1>Plagiarism Detected !</h1>"
    else :
        return "<h1>No Plagiarism Detected !</h1>"

if __name__ == '__main__':
    app.run()
