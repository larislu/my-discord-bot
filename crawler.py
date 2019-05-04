# Note, check robots.txt for respectful crawling
import io
import requests
from PyPDF2 import PdfFileReader

puzzles = []

def pull_puzzles_test():
    solutionSuffix = "&view=solution"
    
    puzzlesFile = open("puzzles.dat", "w")

    url = "https://www.collegepuzzlechallenge.com/Puzzles/ViewPuzzle.ashx?id=1437"
    urlSolution = url + solutionSuffix

    r = requests.get(urlSolution)
    f = io.BytesIO(r.content)

    reader = PdfFileReader(f)
    contents = reader.getPage(0).extractText().split('n')
    matching = [line for line in contents if "ANSWER" in line]
    answerLine = matching[0].replace("\n", "").replace(" ", "")
    #print(answerLine.split("ANSWER:"))
    #puzzlesFile.write(url + " " + answerLine.split("ANSWER:")[1] + "\n")
    puzzles.append([url, answerLine.split("ANSWER:")[1]])

    url2 = "https://www.collegepuzzlechallenge.com/Puzzles/ViewPuzzle.ashx?id=1438"
    urlSolution2 = url2 + solutionSuffix

    r2 = requests.get(urlSolution2)
    f2 = io.BytesIO(r2.content)

    reader = PdfFileReader(f2)
    contents = reader.getPage(0).extractText().split('n')
    matching = [line for line in contents if "ANSWER" in line]
    answerLine = matching[0].replace("\n", "").replace(" ", "")
    #print(answerLine.split("ANSWER:"))
    puzzles.append([url2, answerLine.split("ANSWER:")[1]])

def pull_from_db():
    #TODO
    return {}

def get_puzzles():
    return puzzles

"""
My notes
>>> con.commit()
>>> con.close()
>>> cur.close()
>>> con = psycopg2.connect("postgres://fomnisvxmuhmiq:ea6db68e7bf7b4f745d98c7863ef35226ea0b4898cce22a2bfe802cd37c16e2b@ec2-23-21-129-125.compute-1.amazonaws.com:5432/d4ch5ipss84190", sslmode='require')
>>> cur = con.cursor()
>>> cur.execute("SELECT * FROM solved")
>>> rows = cur.fetchall()

>>> cur.execute("INSERT into solved (url) VALUES ('test')")
>>> cur.execute("SELECT * FROM solved")
>>> rows = cur.fetchall()
>>> print (rows)
[('test',)]
"""