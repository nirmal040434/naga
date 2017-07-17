import meetup.api
import urllib,json
from pprint import pprint

authonticationURI = """https://secure.meetup.com/oauth2/authorize?client_id=3c6811277d58807d5c75286b2b586223&response_type=token&redirect_uri=https://learnfree.azurewebsites.tech"""

search = """docker%2Ccontainer+technology"""
radius = """smart"""
lon = """77.5946"""
lat = """12.9716"""
meetupUrl = """https://api.meetup.com/find/events?photo-host=secure&text="""+search+"""&sig_id=226346307&radius="""+radius+"""&lon="""+lon+"""&lat="""+lat+"""&sig=85dcd520f3c81701fca3e821fe6e7d7c2ae1adbc"""

jsonStaticResponse = urllib.urlopen(meetupUrl)
jsonData = json.load(jsonStaticResponse)

for i in range(len(jsonData)):
	try:
		linkToMeetupPage = jsonData[i]['link']
		eventName = jsonData[i]['name']
		meetupGroupName = jsonData[i]['group']['urlname']
		venueName = jsonData[i]['venue']['name']
		venueAddress = jsonData[i]['venue']['address_1']
		details = "Meetup link: %s \nMeetup name: %s \nUrlname: %s \nVenuename: %s \nVenueaddress: %s\n\n" %(linkToMeetupPage, eventName, meetupGroupName, venueName, venueAddress)
		print details
		
	except KeyError:
		details = "Meetup link: %s \nMeetup name: %s \nUrlname: %s " %(linkToMeetupPage, eventName, meetupGroupName)
		print details+'\n'+'venue details yet to be announced\n\n'
		continue
