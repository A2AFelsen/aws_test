import database_manager


def check_campaign(campaign):
    return database_manager.check_campaign_exists(campaign)
