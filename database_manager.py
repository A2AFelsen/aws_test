import sqlite3

DND_DB = "dnd.db"


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
            campaign_name TEXT,
            password  TEXT,
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
    return True, msg


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
