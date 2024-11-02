import argparse
import sys
import sqlite3
import os


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


def add_new_user(user, password):
    conn = sqlite3.connect(DND_DB)
    cursor = conn.cursor()
    try:
        cursor.execute(f"INSERT INTO login_table VALUES ('{user}', '{password}')")
    except sqlite3.IntegrityError:
        print("ERROR: User Already Exists!")
        sys.exit(1)
    except Exception as e:
        print(e)
        sys.exit(1)
    conn.commit()
    conn.close()


def add_new_campaign_menu(user):
    os.system("cls")
    campaign = input("Please give a name for the campaign: ")
    password = input("Please give a password for the campaign: ")
    add_new_campaign(user, campaign, password)


def add_new_campaign(user, campaign, password):
    conn = sqlite3.connect(DND_DB)
    cursor = conn.cursor()
    try:
        cursor.execute(f"INSERT INTO campaign_table VALUES ('{campaign}', '{password}')")
    except sqlite3.IntegrityError:
        input("ERROR: Campaign Already Exists! Press ENTER to continue")
        return False
    except Exception as e:
        print(e)
        sys.exit(1)
    conn.commit()
    conn.close()

    os.system("cls")
    print(f"{campaign} Successfully Added!")
    add_user_to_campaign(user, campaign, clear_terminal=False)
    return True


def add_user_to_campaign_menu():
    conn = sqlite3.connect(DND_DB)
    cursor = conn.cursor()

    os.system("cls")
    user_campaign = input("Choose a Campaign to add user to: ")

    output = cursor.execute(f"SELECT * from campaign_table WHERE campaign_name = '{user_campaign}'").fetchone()
    if not output:
        input(f"Unable to find {user_campaign}. Press ENTER to continue")
        return False

    user_campaign_password = input("Campaign Password: ")
    if not user_campaign_password == output[1]:
        input(f"Incorrect password ({output[1]}). Press ENTER to continue")
        return False

    user_to_add = input("Select User to add: ")
    output = cursor.execute(f"SELECT * from login_table WHERE user_name = '{user_to_add}'").fetchone()
    if not output:
        input(f"Unable to find user '{user_to_add}'. Press ENTER to continue.")
        return False

    add_user_to_campaign(user_to_add, user_campaign)


def add_user_to_campaign(user, campaign, clear_terminal=True):
    conn = sqlite3.connect(DND_DB)
    cursor = conn.cursor()
    try:
        cursor.execute(f"INSERT INTO user_campaign_table VALUES ('{user}', '{campaign}')")
    except sqlite3.IntegrityError:
        input(f"ERROR: {user} already a part of {campaign}! Press ENTER to continue.")
        return False
    except Exception as e:
        print(e)
        sys.exit(1)
    conn.commit()
    conn.close()
    if clear_terminal:
        os.system("cls")
    input(f"{user} Successfully Added to {campaign}! Press ENTER to continue.")
    return True


def login_user(user, password):
    conn = sqlite3.connect(DND_DB)
    cursor = conn.cursor()
    login_info = cursor.execute(f"SELECT * FROM login_table WHERE user_name='{user}' AND password='{password}'").fetchone()
    if not login_info:
        print("Incorrect User Name and/or Password!")
        sys.exit(1)
    else:
        os.system("cls")
        input("Login Successful! Press ENTER to continue")
        return True


def login_campaign(campaign, password):
    conn = sqlite3.connect(DND_DB)
    cursor = conn.cursor()
    login_info = cursor.execute(f"SELECT * FROM campaign_table WHERE user_name='{campaign}' AND password='{password}'").fetchone()
    if not login_info:
        print("Incorrect User Name and/or Password!")
        sys.exit(1)
    else:
        os.system("cls")
        input("Login Successful! Press ENTER to continue")
        return True


def main_menu(user, password):
    looping = True
    options_list = ['Add a New Campaign', 'Add a User to a Campaign']
    while looping:
        os.system("cls")
        for i, option in enumerate(options_list):
            print(f"{i+1}: {option}")
        user_input = input("Choose an Option (or 'E' to exit): ")
        if user_input == "1":
            add_new_campaign_menu(user)
        elif user_input == "2":
            add_user_to_campaign_menu()
        elif user_input == "e" or user_input == "E":
            looping = False


def main(user, password, new_user):
    check_all_tables()
    if new_user:
        add_new_user(user, password)
    login_user(user, password)
    main_menu(user, password)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--user',     default=None,  action='store', help='User Name')
    parser.add_argument('-p', '--password', default=None,  action='store', help='Password')
    parser.add_argument('-n', '--new_user', default=False, action='store_true', help='Is a New User')
    args = parser.parse_args()

    msg = ""
    if not args.user:
        msg += "ERROR: No '-u' set. Please give a User Name\n"
    if not args.password:
        msg += "ERROR: No '-p' set. Please give a Password\n"
    if msg:
        print(msg.strip())
        sys.exit(1)

    main(args.user, args.password, args.new_user)
