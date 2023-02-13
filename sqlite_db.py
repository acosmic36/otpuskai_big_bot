import sqlite3 as sq


def sql_start():
    global base, cur
    base = sq.connect('message_ids.db')
    cur = base.cursor()
    if base:
        print('base ok!')
    try:
        base.execute('CREATE TABLE IF NOT EXISTS message_ids(message_type INTEGER UNIQUE, message_id INTEGER)')
        base.commit()
        for i in range(8):
            cur.execute(f"INSERT INTO message_ids(message_type) VALUES ('{i+1}')")
        base.commit()
    except:
        print('base already created or else')
        pass


def get_msg_id_by_type(message_type):
    cur.execute(f'''SELECT message_id
        FROM message_ids
        WHERE message_type = {message_type}''')
    message_id = cur.fetchall()[0][0]
    return message_id


def update_id_by_type(message_type, message_id):
    base.execute(f'''UPDATE message_ids
    SET message_id = {message_id}
    WHERE message_type = {message_type}''')
    base.commit()
    pass


