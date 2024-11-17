import database_manager


def create(username, campaign, campaign_password, character_name, character_health):
    if not database_manager.login_campaign(campaign, campaign_password):
        return "Campaign Password incorrect!"
    output, msg = database_manager.add_new_character(username, campaign, character_name, character_health)
    if not output:
        return msg
    return msg
