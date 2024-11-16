import sqlite3
import argparse

DND_DB = "dnd.db"


def drop_table(table):
    conn = sqlite3.connect(DND_DB)
    cursor = conn.cursor()
    cursor.execute(f'''DROP TABLE {table}''')
    conn.commit()
    conn.close()


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


def check_all_tables():
    check_login_table()
    check_campaign_table()
    check_user_campaign_table()


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
    output = cursor.execute(f"SELECT dungeon_master, dm_password FROM campaign_table WHERE campaign = '{campaign}'").fetchone()
    if not output:
        conn.close()
        return False, f"ERROR: No Such Campaign '{campaign}'"

    if not dm_password == output[1]:
        return False, f"ERROR: Incorrect Password!"

    cursor.execute(f"DELETE FROM campaign_table WHERE campaign = '{campaign}'")
    cursor.commit()
    conn.close()
    return True, f"Deleted Campaign '{campaign}'"


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


def main(drop):
    if drop:
        drop_table(drop)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--drop', default=None, action='store', help='Table name to drop.')
    args = parser.parse_args()
    main(args.drop)
