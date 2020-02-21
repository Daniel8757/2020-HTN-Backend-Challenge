#Imports
from flask import Flask, jsonify, request, render_template, redirect, url_for, abort
from formatter import arrayToDict, sqlToJson, fixJson, jsonEvents
import sqlite3
import json

#Creates app
app = Flask(__name__)


#Routes and Controllers
@app.route('/')
def help():
    return jsonify({"project": "HTN 2020 Backend Coding Challenge", "message": "Hope you like my submission!"})

@app.route('/users')
def returnAllUsers():
	conn = sqlite3.connect('hackers.db')
	c = conn.cursor()
	c.execute("SELECT * from hackers")
	
	lat = request.args.get('lat', default = None)
	if not(lat==None):
		lat = float(lat)
	longit = request.args.get('long', default = None)
	if not(longit==None):
		longit = float(longit)
	rang = request.args.get('range', default = None)
	if not(rang==None):
		rang = float(rang)
	
	if (lat == None and longit == None) or rang == None:
		users = c.fetchall()
	elif lat == None:
		c.execute("SELECT * from hackers WHERE longitude >= {} AND longitude <= {}".format(longit-rang, longit+rang))
		users = c.fetchall()
	elif longit == None:
		c.execute("SELECT * from hackers WHERE latitude >= {} AND latitude <= {}".format(lat-rang, lat+rang))
		users = c.fetchall()
	else:
		c.execute("SELECT * from hackers WHERE latitude >= {} AND latitude <= {} AND longitude >= {} AND longitude <= {}".format(lat-rang, lat+rang, longit-rang, longit+rang))
		users = c.fetchall()
	conn.close()
	return jsonify(sqlToJson(users))
	
	
@app.route('/users/<int:id>')
def returnOneUser(id):
	conn = sqlite3.connect('hackers.db')
	c = conn.cursor()
	c.execute("SELECT * from hackers WHERE id=?", (id,))
	user = c.fetchone()
	conn.close()
	if user == None:
		return abort(404)
	else:
		return jsonify(arrayToDict(user))
		
@app.route('/events')
def getEvents():
	conn = sqlite3.connect('hackers.db')
	c = conn.cursor()
	c.execute("SELECT * from events")

	events = c.fetchall()
	newAr = []
	for i in events:
		newAr.append(fixJson(i))
	conn.close()
	return jsonify(newAr)
	
@app.route('/events/<int:id>')
def getOneEvent(id):
	conn = sqlite3.connect('hackers.db')
	c = conn.cursor()
	c.execute("SELECT * from events WHERE id=?", (id,))
	event = c.fetchone()
	conn.close()
	return jsonify(fixJson(event))

@app.route('/events/<int:id>/attendees', methods=['GET', 'POST'])
def modiftyUserInEvent(id):
	conn = sqlite3.connect('hackers.db')
	c = conn.cursor()

	if request.method == "POST":	
		hackerid = json.loads(request.form['up'])['user_id']
		c.execute("SELECT * from hackers WHERE id=?", (hackerid,))
		doesexist = c.fetchall()
		print(doesexist)
		if doesexist == []:
			return abort(400)
		eventid = id
		c.execute("INSERT INTO hackersEventsTable(hackerid, eventid) VALUES (?, ?)", (hackerid, eventid))
		conn.commit()
		conn.close()
		return redirect(url_for("getOneEvent", id=id))
	else:
		return render_template("update.html")

#Errors

@app.errorhandler(400)
def bad_request(error):
	return jsonify({"message": "invalid input", "status": 400})

@app.errorhandler(404)
def not_found(error):
	return jsonify({"message": "not found", "status": 404})

#Starts app, port: 5000
if __name__ == '__main__':
	app.debug = True
	app.run()




