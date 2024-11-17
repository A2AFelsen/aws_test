import flask


def character(username):
    return flask.render_template('character_menu.html', username=username)


def campaign(username):
    return flask.render_template('campaign_menu.html', username=username)
