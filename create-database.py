#Imports
from flask import Flask
import sqlite3
import json
import array

conn = sqlite3.connect('hackers.db')
c = conn.cursor()

#Loads JSON data from file
with open('data.json', 'r') as myfile:
	data = myfile.read()

jsonData = json.loads(data)

#Table of hackers
c.execute("""CREATE TABLE hackers(
				id integer not null primary key autoincrement,
				name string,
				picture string,
				company string,
				email string,
				phone string,
				latitude real,
				longitude real
				)""")

#Table of events
c.execute("""CREATE TABLE events(
				id integer not null primary key autoincrement,
				name string
				)""")

#Junction table to model a many to many relationship between hackers and events
c.execute("""CREATE TABLE hackersEventsTable(
				hackerid integer references hackers(id),
				eventid integer references events(id),
				primary key(hackerid, eventid)
				)""")

#Inserts hackers into database
for hacker in jsonData:
	c.execute("INSERT INTO hackers (name, picture, company, email, phone, latitude, longitude) VALUES (?, ?, ?, ?, ?, ?, ?)", (hacker['name'], hacker['picture'], hacker['company'], hacker['email'], hacker['phone'], hacker['latitude'], hacker['longitude']))
	conn.commit()

#Inserts events and hacker-event relationships into database
eventDictionary = {}
for hacker in jsonData:
	for event in hacker['events']:
		if not(event['name'] in eventDictionary):
			eventDictionary[event['name']] = True
			c.execute("INSERT INTO events (name) VALUES (?)",(event['name'],))
			conn.commit()
		c.execute("SELECT * from hackers WHERE name=?", (hacker['name'],))
		hackerid = c.fetchone()[0]
		c.execute("SELECT * from events WHERE name=?", (event['name'],))
		eventid = c.fetchone()[0]
		c.execute("INSERT INTO hackersEventsTable VALUES (?, ?)", (hackerid, eventid))
		conn.commit()





