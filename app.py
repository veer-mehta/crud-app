from flask import Flask, render_template, request, flash, url_for
import mysql.connector as mysql

dbnm = "videogames"
tbnm = "videogamelist"
edt_row = []

app = Flask(__name__)
app.config["SECRET_KEY"] = "sdfklnsdlknrgriofdskfdgsjf"

db = mysql.connect(host="localhost", user="root", password="Vam#090905", database=dbnm)
csr = db.cursor(buffered = True)
csr.execute('show tables')
if tbnm not in [i[0] for i in csr]:
	csr.execute(f"create table {tbnm}(gameid int not null auto_increment  primary key, name varchar(50) distinct, review varchar(50), rating int)")


@app.route('/edit/<rowid>', methods = ["POST"])
def edt(rowid):
	edt_row.append(int(rowid))
	return dsp()


@app.route('/save/<rowid>', methods=["POST"])
def sav(rowid):
	gamenm = request.form["game_name"]
	review = request.form["review"]
	rating = request.form["rating"]
	edt_row.remove(int(rowid))
	csr.execute(f"update {tbnm} set name='{gamenm}', review='{review}', rating={rating} where gameid={rowid}")
	db.commit()
	return dsp()


@app.route('/delete/<rowid>', methods = ["POST"])
def dlt(rowid):
	csr.execute(f"delete from {tbnm} where gameid='{rowid}'")
	db.commit()
	return dsp()


@app.route('/add', methods = ["POST"])
def add():
	gamenm = request.form["game_name"]
	review = request.form["review"]
	rating = request.form["rating"]

	csr.execute(f"insert into {tbnm} values(0, '{gamenm}', '{review}', {rating})")
	db.commit()
	return dsp()

@app.route('/')
def dsp():
	csr.execute(f"select * from {tbnm}")
	return render_template('index.html', tbl=csr, edt_row=edt_row)
