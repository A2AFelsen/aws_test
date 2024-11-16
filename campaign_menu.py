import database_manager
import flask


def play_campaign(campaign, password, username):
    output, msg = True, f"'Play' Coming Soon! ({password})"
    return flask.render_template('campaign_action.html', username=username, msg=msg)


def create_campaign(campaign, campaign_password, dungeon_master, dm_password):
    output, msg = database_manager.add_new_campaign(campaign, campaign_password, dungeon_master, dm_password)
    return flask.render_template('campaign_action.html', username=dungeon_master, msg=msg)


def delete_campaign(campaign, dm_password, username):
    output, msg = True, "'Delete' Coming Soon!"
    return flask.render_template('campaign_action.html', username=username, msg=msg)
