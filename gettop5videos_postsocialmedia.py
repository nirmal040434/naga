# This program is used to generate the top five top viewed videos on a particualr topic in YouTube

__author__ = "CodeOps Technologies"
__copyright__ = "Copyright (C) 2017 CodeOps Technologies"

import json, operator, time, re, sys, urllib, requests, facebook
from twython import Twython
from xml.etree import ElementTree as ETT
from hashlib import sha1

# Function to get the search term from the command line. If nothing is entered, an error message is diaplayed 

def getSearchTerm():
	try:
		term = sys.argv[1:]
		lengthOfArgs = len(term)
		if(lengthOfArgs == 0):
			print 'Please enter a valid query. Example: python gentop5videos.py docker'	
			sys.exit()
		else:
			searchTerm = ' '.join(term)
	except IndexError:
		print 'Please enter a valid search term.'
	return searchTerm

# Function to get the Json data 

def getJsonData(youtubeApiPrefix, searchTerm, youtubeApiSuffix):
	youtubeApiUrl = youtubeApiPrefix + searchTerm + youtubeApiSuffix 
	response = urllib.urlopen(youtubeApiUrl)
	jsonResponse = json.load(response)
	return jsonResponse

# Function to genreate an inference on the total number of videos. If there are more than 50000 videos avaliable on YouTube for the particular
# topic, then we infer that there are a lot of high quality learning material and content available in YouTube.

def inferenceOnTotalVideos(totalResults , searchTerm):
	content = ''
	maxLimit = 50000
	midLimit = 20000
	minLimit = 0
	if (totalResults > maxLimit):
		content = 'There are a lot videos available in YouTube on ' + searchTerm + '. Here is the list of top viewed videos on this topic. Enjoy!'
	elif (totalResults < maxLimit and totalResults > midLimit):
		content = 'There are a number of videos in YouTube on ' + searchTerm + '. Here is the list of top viewed videos on this topic. Enjoy!'
	elif (totalResults > minLimit and totalResults < midLimit):
		content = 'There are very few videos in YouTube on ' + searchTerm + '. Check them out!'
	else:
		content = 'Sorry, there are no videos in YouTube on ' + searchTerm + '. Please search for another term.'
		sys.exit()
	return content

# Function to get the list of video ids	

def getListOfVideoId(jsonData):
	for incrementor in range(0,5):
		try:   
			videoIdList.append(jsonData['items'][incrementor]['id']['videoId'])
		except IndexError:
			continue
		except KeyError:
			continue
		
	return videoIdList

# Function to get view count for the videos

def getStatsOfVideo(statistics):
	youtubeApiPrefix = """https://www.googleapis.com/youtube/v3/videos?part=statistics&id="""
	youtubeApiSuffix = """&key=AIzaSyDfPhJwDXRZ0MSDjlCvGSLLAy41b0yf87g"""
	jsonStatisticsResponse = getJsonData(youtubeApiPrefix, statistics, youtubeApiSuffix)
	totalResultsCount = jsonStatisticsResponse['pageInfo']['totalResults']
	likecount = []
	for incrementor in range(totalResultsCount):
		try:
			views = jsonStatisticsResponse['items'][incrementor]['statistics']['viewCount']
			viewCountList.append(views)
		except KeyError:
			continue
	return viewCountList

# Fucntion to sort the videos depending on the number of views. First, a dictionary is created with key as the videoid and value as the view count and 
# sort the dictionary depending on the number of views.

def sortVideoId(statistics):
	viewCountList = getStatsOfVideo(statistics)
	youtubeDict = {}
	for incrementor in range(len(videoIdList)):
		youtubeDict[videoIdList[incrementor]] = viewCountList[incrementor]	
	sortedYoutube = sorted(youtubeDict.items(), key=operator.itemgetter(1),reverse = True)
	return sortedYoutube
	
# Function to generate the URL for a video

def getVideoUrl(id):
	videoUrlPrefix = """https://www.youtube.com/watch?v="""
	videoUrl = videoUrlPrefix + id
	return videoUrl
	
# Function to create a dictionary with details like name, URL, like count, view count

def createDict():
	sortedYoutube = sortVideoId(statistics)
	snippetUrlPrefix = """https://www.googleapis.com/youtube/v3/videos?part=snippet&id="""
	snippetUrlSuffix = """&key=AIzaSyDfPhJwDXRZ0MSDjlCvGSLLAy41b0yf87g"""
	videoStatisticsUrlPrefix = """https://www.googleapis.com/youtube/v3/videos?part=statistics&id="""
	videoStatisticsUrlSuffix = """&key=AIzaSyDfPhJwDXRZ0MSDjlCvGSLLAy41b0yf87g"""	

	for incrementor in range(0,len(sortedYoutube)):
		id = sortedYoutube[incrementor][0]
		jsonStatisticsResponse = getJsonData(videoStatisticsUrlPrefix, statistics, videoStatisticsUrlSuffix)
		jsonResponse = getJsonData(snippetUrlPrefix, id, snippetUrlSuffix)
		
		likeCount = jsonStatisticsResponse['items'][0]['statistics']['likeCount']
		viewCount = jsonStatisticsResponse['items'][0]['statistics']['viewCount']
		
		# re.sub is used to substitute non unicode characters with a white space 
		name = re.sub(r'[^\x00-\x7F]+','', jsonResponse['items'][0]['snippet']['title']).strip()
		description = jsonResponse['items'][0]['snippet']['description']
		
		dataOfAllVideos[incrementor+1] = {}
		dataOfAllVideos[incrementor+1]['id'] = id
		dataOfAllVideos[incrementor+1]['data'] = {}
		dataOfAllVideos[incrementor+1]['data']['name'] = name
		dataOfAllVideos[incrementor+1]['data']['description'] = description
		dataOfAllVideos[incrementor+1]['data']['URL'] = getVideoUrl(id)
		dataOfAllVideos[incrementor+1]['data']['like count'] = likeCount
		dataOfAllVideos[incrementor+1]['data']['view count'] = viewCount
	return dataOfAllVideos


# Function to post a message on facebook

def postToFacebook(message):
	facebookAccessToken = 'EAAHLbxvlddgBAAbj21OOBYVZB8JNGFVOD4PjZBGcaRY8sB4aeXlZAUHZCtYE5GfwYVCocZBBwmX06kXKX5HGWzzOHS1PS18rncEj4hUGNZAMDFpsvApXWcpXZC66iLt9YQ0B3V7RC97dLGQYbckYUQ6RNyj0hS0fsUFTDt13G8zegZDZD'
	access = facebook.GraphAPI(facebookAccessToken)
	status = access.put_wall_post(message)

# Function to post a message on twitter
	
def postToTwitter(message):	
	twitterAppKey = 'soeI9mRgGH9zGPbdx6ILuFFjN'
	twitterAppSecret = 'nySryNKPdwjr4mvvCB06rEWR0MXOm44pbSpDNCWXW2LVhkYKFa'
	twitterOauthToken = '854569960399622144-mSWkXRnCOMeEFiRFhXcs1y1oNTrAgYY'
	twitterOauthTokenSecret = 'j6WZyP4t9ZPwcMFb50g4kyQUFGbL7OUcCnNt8PUrwtODy'
	twitter = Twython(twitterAppKey, twitterAppSecret,
                  twitterOauthToken, twitterOauthTokenSecret)
	twitter.update_status(status = message)
	
# Fucntion to get inference depending on the number of likes

def contentBasedOnLikes():
	dataOfAllVideos = createDict()
	maxLikeCount = 1500
	minLikeCount = 750
	sortedYoutube = sortVideoId(statistics)
	for incrementor in range(0,len(sortedYoutube)):
		if(incrementor == 0): 
			contentOfFb = 'Check out this top viewed video "' + dataOfAllVideos[incrementor + 1]['data']['name'] +'"' + dataOfAllVideos[incrementor + 1]['data']['URL']
			contentOfTwitter = 'Check out this top viewed video ' + dataOfAllVideos[incrementor + 1]['data']['URL']
		elif(incrementor == 1):
			contentOfFb = 'Check out this intersting video "' + dataOfAllVideos[incrementor + 1]['data']['name'] +'"' + dataOfAllVideos[incrementor + 1]['data']['URL'] 
			contentOfTwitter = 'Check out this interesting video ' + dataOfAllVideos[incrementor + 1]['data']['URL'] 
		elif(incrementor == 2):
			contentOfFb = 'Hey guys, I found this on YouTube. Take a look at it "' + dataOfAllVideos[incrementor + 1]['data']['name'] +'"'+ dataOfAllVideos[incrementor + 1]['data']['URL'] 
			contentOfTwitter = 'Hey guys, I found this on YouTube. Take a look at it '+ dataOfAllVideos[incrementor + 1]['data']['URL'] 
		elif(incrementor == 3):
			contentOfFb = 'This is an informative video. Check it out! "' + dataOfAllVideos[incrementor + 1]['data']['name'] +'"' + dataOfAllVideos[incrementor + 1]['data']['URL'] 
			contentOfTwitter = 'This is an informative video. Check it out! ' + dataOfAllVideos[incrementor + 1]['data']['URL'] 
		else:
			contentOfFb = 'Check out this awesome video! "' + dataOfAllVideos[incrementor + 1]['data']['name'] +'"' + dataOfAllVideos[incrementor + 1]['data']['URL'] 
			contentOfTwitter = 'Check out this awesome video! ' + dataOfAllVideos[incrementor + 1]['data']['URL'] 
		print contentOfFb
		#postToFacebook(contentOfFb)
		#postToTwitter(contentOfTwitter)
		#time.sleep(10)
		#print content , '\n'

# Function to get the list of presentations from SlideShare 

def getPresentations(quareyTerm):
	slideShareApiKey = 'oUlQkpw7'
	slideShareApiSecretKey = 'JfPQhRbS'
	index = 1
	slideShareContent = ''
	# JSON request 
	params = {
		"api_key": slideShareApiKey,
		"ts": timeStamp,
		"hash": sha1(slideShareApiSecretKey + str(timeStamp)).hexdigest(),
		"items_per_page": 50,
		"q": quareyTerm,
		"sort": "mostviewed",
		"detailed": 1,
		"lang": "en",
		"what": "tag"
	}
	
	xmlResult = requests.get("https://www.slideshare.net/api/2/search_slideshows", params=params)
	xmlInText = xmlResult.text
	root = ETT.fromstring(xmlInText.encode('utf-8'))
	print 'The top viewed presentations on SlideShare for ', quareyTerm , 'are: \n'
	
	#loop through each node to get the title and the URL
	
	for child in root.findall('Slideshow'):
		slideShareUrl = child.find('SlideshowEmbedUrl').text
		title = '. "' + child.find('Title').text.strip() + '" - '
		content = str(index) + title + slideShareUrl + '\n'
		index = index + 1
		slideShareContent = slideShareContent + content 
	return slideShareContent
	
# Main code that calls all the other functions		

timeStamp =int(time.time())
dataOfAllVideos={}
videoIdList = []
viewCountList = []
total_results = ''

youtubeApiPrefix = """https://www.googleapis.com/youtube/v3/search?part=snippet&q="""
youtubeApiSuffix = """&type=video&order=viewCount&chat=mostPopular&maxResults=6&myRating=like&key=AIzaSyCULb7M-QMhQy6NyfyrNeS-gtNzsEhZahs"""
searchTerm = getSearchTerm()
quareyTerm = urllib.quote(searchTerm)
jsonData = getJsonData(youtubeApiPrefix, quareyTerm, youtubeApiSuffix)

try:
	totalResults = jsonData['pageInfo']['totalResults']
	if(totalResults == 0):
		print 'Please enter a valid query. Example: python gentop5videos.py docker'
		sys.exit()	
except KeyError:
	print 'Oops! No videos are available'
	sys.exit()

content = inferenceOnTotalVideos(totalResults,searchTerm)

videoIdList = getListOfVideoId(jsonData)
if(len(videoIdList) == 0):
	print 'Oops! No videos are available'
	sys.exit()
statistics = ','.join(videoIdList)

#print content, '\n'
contentBasedOnLikes()
slideShareContent = getPresentations(quareyTerm)
#print slideShareContent

