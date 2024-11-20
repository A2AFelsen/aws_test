import database_manager


def find_character(user, campaign):
    character_info = database_manager.find_character(user, campaign)
    if not character_info:
        return False, f"User '{user}' has no Characters associated with Campaign '{campaign}'"
    character_name = character_info[2]
    max_health = character_info[3]
    current_health = character_info[4]
    initiate = character_info[5]
    return True, f"User '{user}' is Playing Character '{character_name}' for Campaign '{campaign}'."


def print_battle(campaign):
    msg = ""
    combatants_list = database_manager.get_combatants(campaign)
    for combatant in combatants_list:
        character_name = combatant[0]
        current_health = combatant[1]
        initiative = combatant[2]
        msg += f"{character_name} is at {current_health} HP. (Initiative: {initiative})\n"
    return msg


def update_character(campaign_name, character_name, current_health, initiative):
    return database_manager.update_character(campaign_name, character_name, current_health, initiative)


def add_npc(npc_name, campaign_name):
    return database_manager.add_npc_to_battle(npc_name, campaign_name)
