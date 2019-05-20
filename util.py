import psycopg2

def close_db(con, cur):
    con.commit()
    con.close()
    cur.close()

def clear_answers(handler):
    dbdat = open("db.dat", "r")
    con = psycopg2.connect(dbdat.read().strip(), sslmode='require')
    #con = psycopg2.connect(os.environ["DATABASE_URL"], sslmode='require')
    cur = con.cursor()
    #TODO: remove just answers from current URL
    cur.execute("DELETE FROM answers")

    close_db(con, cur)

    handler.get_guesses().clear();

def help_string():
    help = \
        ".new - obtain a new puzzle\n" + \
        ".current - show current puzzle\n" + \
        ".answer <ANSWER> - submit an answer\n" + \
        ".show - shows guesses thus far\n\n" + \
        \
        "--Use these with caution--\n" \
        ".clear - clear guesses\n"+ \
        ".refresh - refresh database\n" + \
        ".reset - deletes list of completed puzzles"
    return help