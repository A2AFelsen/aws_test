import database_manager


def check_campaign(campaign):
    return database_manager.check_campaign_exists(campaign)


def character_delete(user, campaign):
    output, msg = database_manager.delete_character(user, campaign)
    if not output:
        return msg
    return msg


def character_play(user, campaign):
    pass #
