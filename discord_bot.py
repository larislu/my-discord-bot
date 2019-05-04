import discord
import os
import psycopg2
import random
from crawler import pull_puzzles_test, pull_from_db, get_puzzles
from datetime import datetime

client = discord.Client()

@client.event
async def on_ready():
    print("Deployment Successful")
    await client.change_presence(activity=discord.Game(name="python3.6"))

@client.event
async def on_message(message):
    channel = message.channel

    if message.content == ".test":
        await channel.send("Test Successful")
        puzzles = get_puzzles()
        for p in puzzles:
            await channel.send(p[0])
            await channel.send(p[1])

    if message.content == ".new":
        random.seed(datetime.now())
        puzzles = get_puzzles()
        if (len(puzzles) == 0):
            await channel.send("No puzzles, refresh database")
        else:
            print(puzzles)
            randIndex = random.randint(0, len(puzzles))
            await channel.send(puzzles[randIndex])

    if message.content == ".refresh":
        dbdat = open("db.dat", "r")
        #con = psycopg2.connect(dbdat.read().strip(), sslmode='require')
        #print("Connection Successful")
        con = psycopg2.connect(os.environ["DATABASE_URL"], sslmode='require')
        cur = con.cursor()
        cur.execute("DELETE FROM puzzles")

        print("Pulling")
        pull_puzzles_test()
        puzzles = get_puzzles()
        print(puzzles)
        for p in puzzles:
            statement = "INSERT INTO puzzles (url, solution) VALUES (\'" + p[0] + "\',\'" + p[1] + "\')"
            print(statement)
            cur.execute(statement)

        con.commit()
        con.close()
        cur.close()


#tokendat = open("token.dat", "r")
#client.run(tokendat.read().strip())
client.run(os.environ["ACCESS_TOKEN"])
