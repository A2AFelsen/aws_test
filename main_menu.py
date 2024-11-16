import flask


def character(username):
    return 'Going to Character Menu!'


def campaign(username):
    return flask.render_template('campaign_menu.html', username=username)
