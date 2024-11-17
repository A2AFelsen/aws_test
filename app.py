# app.py
from flask import Flask, request, render_template
from flask_socketio import SocketIO, emit
import login
import main_menu
import campaign_menu
import character_action
import create_character
import npc_create
import play

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

# Store the shared field value (you can replace this with a database in a real app)
shared_data = {"field_value": "Initial Value"}


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
            output, msg = campaign_menu.play_campaign(campaign, dm_password, username)
            return render_template('play.html', username=username, msg=msg, field_value=shared_data["field_value"])
        else:
            if campaign_password:
                output, msg = campaign_menu.play_campaign(campaign, campaign_password, username)
                return render_template('play.html', username=username, msg=msg, field_value=shared_data["field_value"])
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
        return render_template('create_npc.html', username=username)
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
        output, msg = play.find_character(username, campaign)
        return render_template('play.html', username=username, msg=msg, field_value=shared_data["field_value"])
    elif action == 'create':
        return render_template('create_character.html', username=username, campaign=campaign)
    elif action == 'delete':
        return character_action.character_delete(username, campaign)


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


@app.route('/npc_create_submit', methods=['POST'])
def npc_create_submit():
    username = request.form.get('username')
    action = request.form.get('action')
    npc_name = request.form.get('npc_name')
    npc_health = request.form.get('npc_health')

    if action == 'create':
        return npc_create.create(npc_name, npc_health)
    elif action == 'main_menu':
        return render_template('main_menu.html', username=username)


@socketio.on('update_field')
def handle_update_field(data):
    # Update the shared field value
    shared_data["field_value"] = data["new_value"]

    # Notify all connected clients of the update
    emit('field_updated', {"new_value": data["new_value"]}, broadcast=True)


@app.route('/play_submit', methods=['POST'])
def play_submit():
    username = request.form.get('username')
    action = request.form.get('action')
    return render_template('main_menu.html', username=username)


if __name__ == '__main__':
    #app.run(debug=True, host='0.0.0.0')
    socketio.run(app, debug=True, host='0.0.0.0')
