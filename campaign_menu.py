import database_manager
import play
import flask


def play_campaign(campaign, password, username):
    output, msg = play.find_character(username, campaign)
    return flask.render_template('play.html', username=username, msg=msg)


def create_campaign(campaign, campaign_password, dungeon_master, dm_password):
    output, msg = database_manager.add_new_campaign(campaign, campaign_password, dungeon_master, dm_password)
    return flask.render_template('campaign_action.html', username=dungeon_master, msg=msg)


def delete_campaign(campaign, dm_password, username):
    output, msg = database_manager.delete_campaign(campaign, dm_password)
    return flask.render_template('campaign_action.html', username=username, msg=msg)
