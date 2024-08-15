#videogame vault

from flask import Flask, render_template, request, flash, url_for
import mysql.connector as mysql

dbnm = "videogames"
tbnm = "videogamelist"

app = Flask(__name__)
app.config["SECRET_KEY"] = "sdfklnsdlknrgriofdskfdgsjf"

db = mysql.connect(host="localhost", user="root", password="Vam#090905", database=dbnm)
csr = db.cursor(buffered = True)
csr.execute('show tables')
if tbnm not in [i[0] for i in csr]:
	csr.execute(f"create table {tbnm}(gameid int not null auto_increment  primary key, name varchar(50) distinct, review varchar(50), rating int)")

@app.route('/<name>', methods = ["POST"])
def dlt(name):
	csr.execute(f"delete from {tbnm} where name='{name}'")
	db.commit()
	return dsp()	

@app.route('/', methods=["POST"])
def add():
	gamenm = request.form["game_name"]
	review = request.form["review"]
	rating = request.form["rating"]

	csr.execute(f"insert into {tbnm} values(0, '{gamenm}', '{review}', {rating})")
	db.commit()
	return dsp()

@app.route('/')
def dsp():

	csr.execute(f"select name, review, rating from {tbnm}")

	return render_template('index.html', tbl=csr)
