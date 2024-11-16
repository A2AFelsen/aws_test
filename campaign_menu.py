import database_manager
import flask

def play_campaign():
    return "Play a Campaign!"


def create_campaign(campaign, campaign_password, dungeon_master, dm_password):
    output, msg = database_manager.add_new_campaign(campaign, campaign_password, dungeon_master, dm_password)
    return flask.render_template('campaign_action.html', username=dungeon_master, user_action=f'Created {campaign}')


def delete_campaign():
    return "Delete a Campaign!"
