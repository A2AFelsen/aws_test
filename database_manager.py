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


def check_user_campaign_table():
    conn = sqlite3.connect(DND_DB)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_campaign_table (
            user_name     TEXT,
            campaign_name TEXT,
            PRIMARY KEY(user_name, campaign_name)
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
            initiative     INT
        )
    ''')
    conn.commit()
    conn.close()


def check_all_tables():
    check_login_table()
    check_campaign_table()
    check_user_campaign_table()
    check_character_table()
    check_npc_table()
    #check_npc_battle_table()


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
    msg = f"New NPC {npc_name} Added!"
    return True, msg


def main(user_drop, user_list):
    if user_drop:
        drop_table(user_drop)
    if user_list:
        list_table(user_list)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--drop', default=None, action='store', help='Table name to drop.')
    parser.add_argument('-l', '--list', default=None, action='store', help='Table to list.')
    args = parser.parse_args()
    main(args.drop, args.list)
