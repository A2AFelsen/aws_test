# app.py
from flask import Flask, request, render_template
import login
import main_menu
import campaign_menu

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
    username = request.form.get('username')
    action = request.form.get('action')

    if action == 'character':
        return main_menu.character(username)
    elif action == 'campaign':
        return main_menu.campaign(username)


@app.route('/campaign_menu_submit', methods=['POST'])
def campaign_menu_submit():
    username = request.form.get('username')
    action = request.form.get('action')

    campaign = request.form.get('campaign')
    campaign_password = request.form.get('campaign_password')
    dm_password = request.form.get('dm_password')

    if action == 'main_menu':
        return render_template('main_menu.html', username=username)
    elif not campaign:
        return render_template('campaign_menu.html', username=username)
    elif action == 'play':
        if dm_password:
            return campaign_menu.play_campaign(campaign, dm_password, username)
        else:
            if campaign_password:
                return campaign_menu.play_campaign(campaign, campaign_password, username)
            else:
                return render_template('campaign_menu.html', username=username)
    elif action == 'create':
        return campaign_menu.create_campaign(campaign, campaign_password, username, dm_password)
    elif action == 'delete':
        return campaign_menu.delete_campaign(campaign, dm_password, username)


@app.route('/campaign_action_submit', methods=['POST'])
def campaign_action_submit():
    username = request.form.get('username')
    action = request.form.get('action')

    if action == 'return':
        return render_template('campaign_menu.html', username=username)
    elif action == 'main_menu':
        return render_template('main_menu.html', username=username)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
