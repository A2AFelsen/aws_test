# app.py
from flask import Flask, request, render_template
import login
import main_menu
import campaign_menu
import character_action
import create_character

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


@app.route('/character_menu_submit', methods=['POST'])
def character_menu_submit():
    username = request.form.get('username')
    action = request.form.get('action')

    if action == 'play':
        return render_template('character_action.html', username=username, user_action='play')
    elif action == 'create':
        return render_template('character_action.html', username=username, user_action='create')
    elif action == 'delete':
        return render_template('character_action.html', username=username, user_action='delete')
    elif action == 'npc':
        return "Create NPC!"
    elif action == 'main_menu':
        return render_template('main_menu.html', username=username)


@app.route('/character_action_submit', methods=['POST'])
def character_action_submit():
    username = request.form.get('username')
    action = request.form.get('action')
    campaign = request.form.get('campaign_name')

    if action == 'main_menu':
        return render_template('main_menu.html', username=username)

    if not character_action.check_campaign(campaign):
        return f"ERROR: No such campaign '{campaign}'"

    if action == 'play':
        return "Play Character"
    elif action == 'create':
        return render_template('create_character.html', username=username, campaign=campaign)
    elif action == 'delete':
        return "Delete Character"


@app.route('/character_create_submit', methods=['POST'])
def character_create_submit():
    username = request.form.get('username')
    action = request.form.get('action')
    campaign = request.form.get('campaign')
    character_name = request.form.get('character_name')
    character_health = request.form.get('character_health')
    campaign_password = request.form.get('campaign_password')

    if action == 'create':
        return create_character.create(username, campaign, campaign_password, character_name, character_health)
    elif action == 'main_menu':
        return render_template('main_menu.html', username=username)


@app.route('/play_submit', methods=['POST'])
def play_submit():
    username = request.form.get('username')
    action = request.form.get('action')
    return render_template('main_menu.html', username=username)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
