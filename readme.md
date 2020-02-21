#Hack the North 2020 Backend Coding Challenge
## Summary

Here's my submission for HTN-2020 Backend Coding Challenge. Hope you enjoy! My features are:

- Creating database
- Getting all users
- Finding users by id
- Finding users by location
- Getting all events(and all attendees)
- Finding events by id(and all attendees)
- Adding hackers to events

## Database

I have 2 main tables, 1 junction table and 1 "hidden" table(used to assign unique ID's to hackers and events). The 2 main tables model the data of hackers and events, while the junction table models the many-to-many relationships between hackers and events. The hidden table is autocreated if you use autoincrement, and helps with assigning unique IDs to all hackers and events.

## How to Run

Once you download the file, activate the virtual enviroment and create the database by running: 
```
pip3 create-database.py
```
Note that this file should only be run once. If you want to start fresh, then you can delete the database (named "hackers.db") and run the above command again. 
Then, run:
```
pip3 app.py
```
Which should start the flask server on port 5000.

###Endpoints
####Note that the JSON data is sorted alphabetically, so when testing things like events, make sure to scroll to the bottom of attendees to find the eventid and event name
`GET /users`
Returns all users
`GET /users?lat=48.473000&long=-34.736000&range=0.1`
Returns all users within one range of the longitude and latitude. Note that if range is not specified, it returns all users, and if either latitude or longitude or latitude is not specified, it only uses the other value(so if longitude is not specified, it returns all hackers of latitude within the range
`GET /users/<int:id>`
Returns one user with the unique id
`GET /events`
returns all events
`GET /events/<int:id>`
returns one event with the unique id
`GET /events/<int:id>/attendees`
returns an html page where you can add users to events with that id
`POST /events/<int:id>/attendees`
takes JSON data of the form:
`{"user_id": 1}`
and adds the user to that event
###Input Restrictions and Reponses
`Status: 400`
This indicates that the user tried to add a hacker that does not exist to an event(hackerid not found in table)
`Status: 404`
This indicates that the user tried to search for an event or hacker that does not exist(hackerid or eventid not found in table

## What I would do add if I had more time
- In a real world setting, a user refraining from inputting longitude, latitude, or range might've done it by accident and a valid response may case trouble, so I would require more specific inputs if a user wanted to only use longitude or latitude
- I would use SQLAlchemy to simplify a lot of things. I chose not to in this project because I wanted to demonstrate my ability to utilize SQL queries without imports
- When I load attendees for events, I chose not to add the attendee's events because I felt that it was a bit redundant, but I could create an option for users to see it when loading events
- I would add ways to delete users from events, add users to database, add events to database, and create more endpoints to identify users(for example, if we only had the user's name)