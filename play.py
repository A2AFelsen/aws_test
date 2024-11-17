import database_manager


def find_character(user, campaign):
    character_info = database_manager.find_character()
    if not character_info:
        return False, f"User '{user}' has no Characters associated with Campaign '{campaign}'"
    character_name = character_info[2]
    max_health = character_info[3]
    current_health = character_info[4]
    initiate = character_info[5]
    return True, f"User '{user}' is Playing Character '{character_name}' for Campaign '{campaign}'."
