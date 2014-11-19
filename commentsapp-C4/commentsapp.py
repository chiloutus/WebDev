
from flask import Flask, render_template, url_for, request, redirect, flash, session
import time,random,os,datetime
from threading import Thread

app = Flask(__name__)

@app.route('/')
def display_home():
		return render_template("home.html",
					the_title="Welcome to the Word Game, where all the fun is at.",
					comment_url=url_for("getacomment"),
					show_url=url_for("showallcomments"),
					game_url=url_for("wordgame"),
				working_dir= os.getcwd())
@app.route('/comment')
def getacomment():
		return render_template("enter.html",
				 the_title="Please make words from the word given!",
				 the_save_url=url_for("saveformdata") )

def update_log(name, comment):
	time.sleep(15)
	with open('comments.log', 'a') as log:
		print(name, 'said:', file=log)
		print(comment, file=log)

@app.route('/saveform', methods=["POST"])
def saveformdata():
	all_ok = True
	if request.form['user_name'] == '':
		all_ok = False
		flash("Sorry. You must tell me your name. Try again")
		#print('-->', request.form['the_comment'].strip(), '<--')
	if request.form['the_comment'] == '':
		all_ok = False
		flash("Sorry. You must give me a comment. Try again")
	if all_ok:
		t = Thread(target=update_log, args=(request.form['user_name'], request.form	['the_comment']))
		t.start()
		session['last_visitor'] = request.form['user_name']
		return render_template("thanks.html",
				the_title="Thanks!",
				the_user=request.form['user_name'],
				home_link=url_for("display_home"), )
	else:		
		return redirect(url_for("getacomment"))

@app.route('/displaycomments')
def showallcomments():
	with open('comments.log') as log:
		lines = log.readlines()
		return render_template("show.html",
				the_title="Here are the comments to date",
				the_data=lines,							home_link=url_for("display_home"))

@app.route('/wordgame')

def wordgame():
    session['startTime'] = getTimeStamp()
    session['randomWord'] = get_random_line()
    return render_template("game.html",
            the_title="Please make words from the word 	given!",
            the_word=session['randomWord'],
            game_save_url=url_for("savegamedata") )
def getTimeStamp():
        return datetime.datetime.utcnow()
def get_random_line():
    total_bytes = os.stat('longWords.txt').st_size
    random_point = random.randint(0, total_bytes)
    print(str(random_point))
    file = open('longWords.txt')
    file.seek(random_point)
    file.readline() # skip this line to clear the partial line
    return file.readline()#variables

def isAWord(word):
    return '\n' + word + '\n' in open("shortWords.txt").read()
def hasTooManyLetters(word,source,i):
    return source.count(i) < word.count(i)

def isInSource(word,source):
    count = len(word)
    for i in word:
        if i in source:
            if not hasTooManyLetters(word,source,i):
                count -= 1
    if(count == 0):
        return True
    else:
        return False
def checkWords(words):
        correctWords = []
        sourceWord = session['randomWord'].lower()
        for usrin in words:
            if len(usrin) != 0:
                if isAWord(usrin):
                    if usrin + '\n' != sourceWord:
                        if isInSource(usrin,sourceWord):
                            correctWords.append("✔")
                        else:
                            correctWords.append("This cannot be made from the original word!")
                    else:
                        correctWords.append("This is the same as the original word!")
                else:
                    correctWords.append("This is not a word")
            else:
                correctWords.append("This word is blank")
        return correctWords

@app.route('/gameresults', methods=["POST"])

def savegamedata():
    session['endTime'] = getTimeStamp()
    totalTime = timeDifference()
    formattedTime = nice_timedelta_str(totalTime)
    words = [request.form['word1'],request.form['word2'],request.form['word3'],request.form['word4']
        ,request.form['word5'],request.form['word6'],request.form['word7']]


    correctWords = checkWords(words)
    if len(correctWords) > 1:
        return render_template("gameresult.html",
						 word1=request.form["word1"],
						 word2=request.form["word2"],
						 word3=request.form["word3"],
						 word4=request.form["word4"],
						 word5=request.form["word5"],
						 word6=request.form["word6"],
						 word7=request.form["word7"],
                         correctWords = correctWords,
						 home_link=url_for("display_home"),
                         game_link=url_for("wordgame"),
                         game_time= formattedTime)
    else:
        return redirect(url_for("getacomment"))

def timeDifference():
    return session['endTime'] - session['startTime']

def nice_timedelta_str(d):
    result = str(d)
    if result[1] == ':':
        result = '0' + result
    result = result.split('.', 1)[0]
    return result


app.config['SECRET_KEY'] = 'thisismysecretkeywhichyouwillneverguesshahahahahahahaha'
if __name__== "__main__":
    app.run(debug=True)
