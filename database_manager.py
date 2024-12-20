import sqlite3
import argparse

DND_DB = "dnd.db"


def drop_table(table):
    conn = sqlite3.connect(DND_DB)
    cursor = conn.cursor()
    cursor.execute(f'''DROP TABLE {table}''')
    conn.commit()
    conn.close()


def list_table(table):
    conn = sqlite3.connect(DND_DB)
    cursor = conn.cursor()
    for entry in cursor.execute(f'''SELECT * FROM {table}''').fetchall():
        print(entry)


def check_login_table():
    conn = sqlite3.connect(DND_DB)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS login_table (
            user_name TEXT,
            password  TEXT,
            PRIMARY KEY(user_name)
        )
    ''')
    conn.commit()
    conn.close()


def check_campaign_table():
    conn = sqlite3.connect(DND_DB)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS campaign_table (
            campaign_name    TEXT,
            player_password  TEXT,
            dungeon_master   TEXT,
            dm_password      TEXT,
            PRIMARY KEY(campaign_name)
        )
    ''')
    conn.commit()
    conn.close()


def check_character_table():
    conn = sqlite3.connect(DND_DB)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS character_table (
            user_name      TEXT,
            campaign_name  TEXT,
            character_name TEXT,
            max_health     INT,
            current_health INT,
            initiative     INT,
            PRIMARY KEY(user_name, campaign_name)
        )
    ''')
    conn.commit()
    conn.close()


def check_npc_table():
    conn = sqlite3.connect(DND_DB)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS npc_table (
            npc_name   TEXT,
            max_health INT,
            PRIMARY KEY(npc_name)
        )
    ''')
    conn.commit()
    conn.close()


def check_npc_battle_table():
    conn = sqlite3.connect(DND_DB)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS npc_battle_table (
            npc_name       TEXT,
            campaign_name  TEXT,
            current_health INT,
            initiative     INT,
            PRIMARY KEY(npc_name, campaign_name)
        )
    ''')
    conn.commit()
    conn.close()


def check_all_tables():
    check_login_table()
    check_campaign_table()
    check_character_table()
    check_npc_table()
    check_npc_battle_table()


def get_all_users():
    check_all_tables()
    conn = sqlite3.connect(DND_DB)
    cursor = conn.cursor()
    entries = cursor.execute(f"SELECT * FROM login_table").fetchall()
    msg = ""
    for entry in entries:
        msg += f"{entry[0]}: {entry[1]}<br>"
    return msg


def add_new_user(user, password):
    check_all_tables()
    conn = sqlite3.connect(DND_DB)
    cursor = conn.cursor()
    try:
        cursor.execute(f"INSERT INTO login_table VALUES ('{user}', '{password}')")
    except sqlite3.IntegrityError:
        msg = "ERROR: User Already Exists!"
        return False, msg
    except Exception as e:
        print(e)
        return False, None
    conn.commit()
    conn.close()
    msg = "New User Added!"
    return True, msg


def add_new_campaign(campaign, player_password, dungeon_master, dm_password):
    check_all_tables()
    conn = sqlite3.connect(DND_DB)
    cursor = conn.cursor()
    try:
        cursor.execute(f"INSERT INTO campaign_table VALUES ('{campaign}', '{player_password}', '{dungeon_master}', '{dm_password}')")
    except sqlite3.IntegrityError:
        msg = f"ERROR: Campaign '{campaign}' Already Exists!"
        return False, msg
    except Exception as e:
        print(e)
        return False, None
    conn.commit()
    conn.close()
    msg = f"New Campaign '{campaign}' Added!"
    return True, msg


def delete_campaign(campaign, dm_password):
    check_all_tables()
    conn = sqlite3.connect(DND_DB)
    cursor = conn.cursor()
    output = cursor.execute(f"SELECT dungeon_master, dm_password FROM campaign_table WHERE campaign_name = '{campaign}'").fetchone()
    if not output:
        conn.close()
        return False, f"ERROR: No Such Campaign '{campaign}'"

    if not dm_password == output[1]:
        return False, f"ERROR: Incorrect Password!"

    cursor.execute(f"DELETE FROM campaign_table WHERE campaign_name = '{campaign}'")
    conn.commit()
    conn.close()
    return True, f"Deleted Campaign '{campaign}'"


def play(user, campaign, character):
    conn = sqlite3.connect(DND_DB)
    cursor = conn.cursor()

    if campaign:
        pass
    elif character:
        pass


def login_user(user, password):
    check_all_tables()
    conn = sqlite3.connect(DND_DB)
    cursor = conn.cursor()
    login_info = cursor.execute(
        f"SELECT * FROM login_table WHERE user_name='{user}' AND password='{password}'").fetchone()
    if not login_info:
        msg = "Incorrect User Name and/or Password!"
        return False, msg
    else:
        msg = "Login Successful!"
        return True, msg


def check_campaign_exists(campaign):
    conn = sqlite3.connect(DND_DB)
    cursor = conn.cursor()
    exists = cursor.execute(f"SELECT * FROM campaign_table WHERE campaign_name = '{campaign}'").fetchone()
    if exists:
        return True
    else:
        return False


def login_campaign(campaign, password):
    conn = sqlite3.connect(DND_DB)
    cursor = conn.cursor()
    login_info = cursor.execute(
        f"SELECT * FROM campaign_table WHERE campaign_name ='{campaign}' and player_password='{password}'").fetchone()
    if not login_info:
        return False
    else:
        return True


def add_new_character(user, campaign, character, max_health):
    check_all_tables()
    max_health = int(max_health)
    conn = sqlite3.connect(DND_DB)
    cursor = conn.cursor()
    try:
        cursor.execute(f"INSERT INTO character_table VALUES ('{user}', '{campaign}', '{character}', {max_health}, {max_health}, 0)")
    except sqlite3.IntegrityError:
        msg = f"ERROR: User '{user}' in Campaign '{campaign}' Already Exists!"
        return False, msg
    except Exception as e:
        print(e)
        return False, None
    conn.commit()
    conn.close()
    msg = f"New Character '{character}' in Campaign '{campaign}' Added!"
    return True, msg


def delete_character(user, campaign):
    check_all_tables()
    conn = sqlite3.connect(DND_DB)
    cursor = conn.cursor()
    output = cursor.execute(f"SELECT * from character_table WHERE user_name='{user}' AND campaign_name='{campaign}'").fetchone()
    if not output:
        msg = f"User '{user}' has no Characters associated with Campaign '{campaign}'"
        return False, msg
    cursor.execute(f"DELETE from character_table WHERE user_name='{user}' AND campaign_name='{campaign}'")
    conn.commit()
    conn.close()
    msg = f"Character '{output[2]}' in Campaign '{campaign}' Deleted!"
    return True, msg


def find_character(user, campaign):
    check_all_tables()
    conn = sqlite3.connect(DND_DB)
    cursor = conn.cursor()
    output = cursor.execute(f"SELECT * from character_table WHERE user_name='{user}' AND campaign_name='{campaign}'").fetchone()
    return output


def add_new_npc(npc_name, max_health):
    check_all_tables()
    max_health = int(max_health)
    conn = sqlite3.connect(DND_DB)
    cursor = conn.cursor()
    try:
        cursor.execute(f"INSERT INTO npc_table VALUES ('{npc_name}', {max_health})")
    except sqlite3.IntegrityError:
        msg = f"ERROR: NPC '{npc_name}' Already Exists!"
        return False, msg
    except Exception as e:
        msg = e
        return False, msg
    conn.commit()
    conn.close()
    msg = f"New NPC '{npc_name}' Added!"
    return True, msg


def name_new_npc_to_battle(npc_tuple):
    if not npc_tuple:
        return False
    i = 0
    for entry in npc_tuple:
        npc_name = entry[0].split("_")[0]
        npc_num = int(entry[0].split("_")[1])
        if i != npc_num:
            return f"{npc_name}_{i}"
        else:
            i += 1
    return f"{npc_name}_{i}"


def add_npc_to_battle(npc_name, campaign_name):
    check_all_tables()
    conn = sqlite3.connect(DND_DB)
    cursor = conn.cursor()
    output = cursor.execute(f"SELECT * FROM npc_table WHERE npc_name ='{npc_name}'").fetchone()
    if not output:
        msg = f"NPC '{npc_name} Not Found. Try Adding it first!"
        return False, msg
    npc_health = int(output[1])
    output = cursor.execute(f"""SELECT *
                                FROM npc_battle_table 
                                WHERE npc_name LIKE '{npc_name}_%' 
                                AND campaign_name='{campaign_name}'
                                ORDER BY npc_name ASC""").fetchall()
    npc_name_num = name_new_npc_to_battle(output)
    if not npc_name_num:
        npc_name_num = f"{npc_name}_0"
    try:
        cursor.execute(f"INSERT INTO npc_battle_table VALUES ('{npc_name_num}', '{campaign_name}', {npc_health}, 0)")
    except sqlite3.IntegrityError:
        msg = "Some Error Occurred o.0"
        return False, msg
    conn.commit()
    conn.close()
    msg = f"NPC '{npc_name_num}' Added to campaign '{campaign_name}'"
    return True, msg


def remove_npc_from_battle(npc_name, campaign_name):
    conn = sqlite3.connect(DND_DB)
    cursor = conn.cursor()

    npc_data = cursor.execute(f"""DELETE 
                                  FROM npc_battle_table
                                  WHERE npc_name = '{npc_name}'
                                  AND campaign_name = '{campaign_name}'                         
                                  """).fetchone()

    conn.commit()
    conn.close()


def get_combatants(campaign_name):
    conn = sqlite3.connect(DND_DB)
    cursor = conn.cursor()
    combatants = cursor.execute(f"""SELECT * FROM (
                                        SELECT character_name, current_health, initiative 
                                        FROM character_table WHERE campaign_name='{campaign_name}'
                                        UNION
                                        SELECT npc_name, current_health, initiative
                                        FROM npc_battle_table WHERE campaign_name='{campaign_name}'
                                    ) AS combined_results
                                    ORDER BY initiative DESC;
                                """).fetchall()
    return combatants


def update_npc(campaign_name, npc_name, current_health, initiative):
    conn = sqlite3.connect(DND_DB)
    cursor = conn.cursor()

    npc_data = cursor.execute(f"""SELECT * 
                                  FROM npc_battle_table
                                  WHERE npc_name = '{npc_name}'
                                  AND campaign_name = '{campaign_name}'                         
                                  """).fetchone()

    if not npc_data:
        return False

    if current_health == "":
        current_health = int(npc_data[2])
    if initiative == "":
        initiative = int(npc_data[3])

    if int(current_health) <= 0:
        remove_npc_from_battle(npc_name, campaign_name)

    cursor.execute(f"""UPDATE npc_battle_table
                       SET (current_health, initiative) = ({int(current_health)}, {int(initiative)}) 
                       WHERE campaign_name = '{campaign_name}'
                       AND npc_name = '{npc_name}'
                    """)
    conn.commit()
    conn.close()
    return True


def update_character(campaign_name, character_name, current_health, initiative):
    conn = sqlite3.connect(DND_DB)
    cursor = conn.cursor()

    character_data = cursor.execute(f"""SELECT * 
                                        FROM character_table
                                        WHERE character_name = '{character_name}'
                                        AND campaign_name = '{campaign_name}'                         
                                    """).fetchone()

    if not character_data:
        conn.close()
        return update_npc(campaign_name, character_name, current_health, initiative)

    if current_health == "":
        current_health = int(character_data[4])
    if initiative == "":
        initiative = int(character_data[5])

    cursor.execute(f"""UPDATE character_table
                       SET (current_health, initiative) = ({int(current_health)}, {int(initiative)}) 
                       WHERE campaign_name = '{campaign_name}'
                       AND character_name = '{character_name}'
                    """)
    conn.commit()
    conn.close()
    return True


def main(user_drop, user_list, combatants):
    if user_drop:
        drop_table(user_drop)
    if user_list:
        list_table(user_list)
    if combatants:
        output, msg = add_npc_to_battle('Zombie', combatants)
        print(msg)
        print(get_combatants(combatants))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--drop', default=None, action='store', help='Table name to drop.')
    parser.add_argument('-l', '--list', default=None, action='store', help='Table to list.')
    parser.add_argument('-c', '--combatants', default=None, action='store', help='Lists combatants of given campaign')
    args = parser.parse_args()
    main(args.drop, args.list, args.combatants)
