#Imports
import sqlite3
import json

# Takes a user and returns a JSON format with valid dictionary
def arrayToDict(entry):
	conn = sqlite3.connect('hackers.db')
	c = conn.cursor()
	entryDictionary = {}
	c.execute("SELECT events.name FROM events INNER JOIN (hackers INNER JOIN hackersEventsTable ON hackers.id=hackersEventsTable.hackerid) ON events.id=hackersEventsTable.eventid WHERE hackers.id=(?);",(entry[0],))
	events = c.fetchall()
	theirevents = []
	for event in events:
		theirevents.append(event[0])
	entryDictionary['events'] = tuple(theirevents)	

	for key in range(len(entry)):
		if key==0:
			entryDictionary['id'] = entry[key]
		elif key==1:
			entryDictionary['name'] = entry[key]
		elif key==2:
			entryDictionary['picture'] = entry[key]
		elif key==3:
			entryDictionary['company'] = entry[key]
		elif key==4:
			entryDictionary['email'] = entry[key]
		elif key==5:
			entryDictionary['phone'] = entry[key]
		elif key==6:
			entryDictionary['latitude'] = entry[key]
		else:
			entryDictionary['longitude'] = entry[key]
	conn.close()
	return entryDictionary

#Takes an array of users and outputs a valid JSON format of them
def sqlToJson(data):
	newData = []
	for entry in data:
		newData.append(arrayToDict(entry))
	return newData

#Takes an event and outputs a valid JSON format of them
def fixJson(entry):
	conn = sqlite3.connect('hackers.db')
	c = conn.cursor()
	
	c.execute("SELECT * FROM hackers INNER JOIN (events INNER JOIN hackersEventsTable on events.id=hackersEventsTable.eventid) ON hackers.id=hackersEventsTable.hackerid WHERE events.id=(?);",(entry[0],))

	hackers = c.fetchall()
	a = []
	for hacker in hackers:
		entryDictionary = {}
		for key in range(len(hacker)):
			if key==0:
				entryDictionary['id'] = hacker[key]
			elif key==1:
				entryDictionary['name'] = hacker[key]
			elif key==2:
				entryDictionary['picture'] = hacker[key]
			elif key==3:
				entryDictionary['company'] = hacker[key]
			elif key==4:
				entryDictionary['email'] = hacker[key]
			elif key==5:
				entryDictionary['phone'] = hacker[key]
			elif key==6:
				entryDictionary['latitude'] = hacker[key]
			else:
				entryDictionary['longitude'] = hacker[key]
		a.append(entryDictionary)
	
	finalDictionary = {}
	finalDictionary['event_id'] = entry[0]
	finalDictionary['event_name'] = entry[1]
	finalDictionary['attendees'] = tuple(a)
	conn.close()
	return finalDictionary

#Takes an array of events and outputs a valid JSON format of them
def jsonEvents(events):
	newdata = []
	for entry in data:
		newdata.append(fixJson(entry))





