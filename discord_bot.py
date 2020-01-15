import discord
import os
import psycopg2
import random
from datetime import datetime

from PuzzleHandler import PuzzleHandler
from util import close_db, help_string

client = discord.Client()
handler = PuzzleHandler(client)

@client.event
async def on_ready():
    print("Deployment Successful")

    dbdat = open("db.dat", "r")
    con = psycopg2.connect(dbdat.read().strip(), sslmode='require')
    #con = psycopg2.connect(os.environ["DATABASE_URL"], sslmode='require')
    cur = con.cursor()

    cur.execute("SELECT * FROM current")
    current = cur.fetchall()[0]
    handler.set_current_puzzle(current)
    print(handler.get_current_puzzle())

    # answer = "tests"
    # command = "UPDATE answers SET answers = array_append(answers, \'" + answer + "\') WHERE url = \'" + "test" + "\'"
    # print(command)
    # cur.execute(command)

    #command = "SELECT answers FROM answers WHERE url = \'" + current[0] + "\'"
    #statement = "INSERT INTO answers(url, answers) VALUES (\'" + "test" + "\', ARRAY[]::TEXT[])"
    #print(statement)
    #cur.execute(statement)

    command = "SELECT answers FROM answers WHERE url = \'test\'"
    print(command)
    cur.execute(command)
    grabbed_answers = cur.fetchall()
    print(grabbed_answers)
    if grabbed_answers:
        answers = grabbed_answers[0][0]
        handler.set_guesses(answers)
        print(answers)

    close_db(con, cur)

    await client.change_presence(activity=discord.Game(name="python3.6"))

@client.event
async def on_message(message):
    channel = message.channel

    if message.content == ".new":
        cur.execute("SELECT * FROM puzzles")
        puzzles = cur.fetchall()
        handler.set_puzzles(puzzles)

        if (len(puzzles) == 0):
            await channel.send("No puzzles")
        else:
            print(puzzles)

            cur.execute("SELECT * FROM solved")
            solved = cur.fetchall()
            handler.set_solved(rows[0])

            random.seed(datetime.now())
            puzzles = handler.get_puzzles()

            randIndex = random.randint(0, len(puzzles))
            #randIndex = 1


            await channel.send(puzzles[randIndex][0])

            handler.set_current_puzzle(puzzles[randIndex])

            dbdat = open("db.dat", "r")
            con = psycopg2.connect(dbdat.read().strip(), sslmode='require')
            #con = psycopg2.connect(os.environ["DATABASE_URL"], sslmode='require')
            cur = con.cursor()
            cur.execute("DELETE FROM current")
            statement = "INSERT INTO current (url, solution) VALUES (\'" + \
                        puzzles[randIndex][0] + "\',\'" + puzzles[randIndex][1] + "\')"
            cur.execute(statement)

            try:
                statement = "INSERT INTO answers(url, answers) VALUES (\'" + puzzles[randIndex][0] + "\', ARRAY[]::TEXT[])"
                print(statement)
                cur.execute(statement)
            except:
                print("Already in db")

            close_db(con, cur)
            clear_answers(handler)

    if message.content == ".current":
        await channel.send(handler.get_current_puzzle()[0][0])

    if ".answer" in message.content:
        print(message.content.split())
        if (message.content.split()[1] == "<ANSWER>"):
            print("help line")
        else:
            #await channel.send(message.content.split(".answer"))
            answer = message.content.split()[1]
            answer.upper().replace(" ", "")
            handler.get_guesses().append(answer)

            dbdat = open("db.dat", "r")
            con = psycopg2.connect(dbdat.read().strip(), sslmode='require')
            #con = psycopg2.connect(os.environ["DATABASE_URL"], sslmode='require')
            cur = con.cursor()
            command = "UPDATE answers SET answers = array_append(answers,\'" + answer + "\') WHERE url = \'" + handler.get_current_puzzle()[0] + "\'"
            cur.execute(command)

            if answer == handler.get_current_puzzle()[1]:
                await channel.send("Correct!!")
                cur.execute("INSERT into solved (url) VALUES (\'" + handler.get_current_puzzle()[0] + "\')")
            else:
                await channel.send(handler.get_current_puzzle()[1])

            close_db(con, cur)

    if message.content == ".show":
        for answer in handler.get_guesses():
            await channel.send(answer)

    if message.content == ".clear":
        await channel.send("Are you sure? (Enter '.yes.clear' if so)")

    if message.content == ".yes.clear":
        clear_answers(handler)

    if message.content == ".refresh":
        await channel.send("Are you sure? (Enter '.yes.refresh' if so)")

    if message.content == ".yes.refresh":
        dbdat = open("db.dat", "r")
        con = psycopg2.connect(dbdat.read().strip(), sslmode='require')
        #con = psycopg2.connect(os.environ["DATABASE_URL"], sslmode='require')
        cur = con.cursor()
        # Are you sure?
        cur.execute("DELETE FROM puzzles")

        print("Pulling")
        handler.pull_puzzles_test()
        puzzles = handler.get_puzzles()
        print(puzzles)
        for p in puzzles:
            statement = "INSERT INTO puzzles (url, solution) VALUES (\'" + p[0] + "\',\'" + p[1] + "\')"
            print(statement)
            cur.execute(statement)

        close_db(con, cur)

    if message.content == ".help":
        await channel.send(help_string())

tokendat = open("token.dat", "r")
client.run(tokendat.read().strip())
#client.run(os.environ["ACCESS_TOKEN"])
