import database_manager


def create(npc_name, npc_health):
    output, msg = database_manager.add_new_npc(npc_name, npc_health)
    if not output:
        return msg
    return msg
