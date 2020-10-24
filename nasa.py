import requests
import datetime 
import json 
import shutil
import datetime
import tweepy
import schedule 
from os import environ


now = datetime

# Authenticate to Twitter
yy
CONSUMER_KEY = environ['CONSUMER_KEY']
CONSUMER_SECRET = environ['CONSUMER_SECRET']
ACCES_KEY = environ['ACCES_KEY']
ACCES_SECRET = environ['ACCES_SECRET']
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCES_KEY, ACCES_SECRET)

#connection a twitter
api = tweepy.API(auth)

#notre url api
reponse = requests.get("https://api.nasa.gov/planetary/apod?api_key=ajqyncy6aXyymD7lYmMeioI2z0Lj5JlxKYttwvIn")

#api temperature de mars
mars = requests.get("https://mars.nasa.gov/rss/api/?feed=weather&category=insight&feedtype=json&ver=1.0")


#On importe l'api du rover et on y insere la bonne date
date = datetime.datetime.now().date()
rover = requests.get("https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/latest_photos/?api_key=ajqyncy6aXyymD7lYmMeioI2z0Lj5JlxKYttwvIn")




	
	
#verifie la temperature le sol actuel
def verifier_sol(obj):
	current_sol = mars.json()['sol_keys'][6]

	print(current_sol)
	
#Enregistre une photo d'un rover sur mars 
def photo_rover(obj):
	image_rover = rover.json()['latest_photos']
	for x in range(len(image_rover)):
		print(len(image_rover))
	length = (len(image_rover)) -1
	image_rover = image_rover[length]
	image_rover = image_rover['img_src']
	resp = requests.get(image_rover, stream=True)
	image_rover = open("rover.png","wb")
	resp.raw.decode_content = True
	shutil.copyfileobj(resp.raw, image_rover)
	del resp

	
#descrip
def description_rover(obj):
	description = rover.json()['latest_photos']
	longueur_liste = (len(description)) -1
	description = description[longueur_liste]
	description = description['sol']

	return description


	
	


#prend un objet json en entre
def jprint(obj):

	#formate en string l'objet JSON
	text = json.dumps(obj, sort_keys = True, indent = 6)
	print(text)

#donne le titre de la photo du jour
def titre_photo(obj):
	titre = reponse.json()['title']
	return titre


# donne la definition de la photo du jour
def definition_photo(obj):
	definition = reponse.json()['explanation']
	print(len(definition))
	index = 0
	for x in definition:
		print(x, end ='')

		if (x == '.'):
			
			break
		index = index+1	

	definition = definition[:index+1]
	return definition
		
	



#verifi le type de fichier prend pour entre l;objet json
def photo_jour(obj):

	#on va verifier si c'est une video, si c'est le cas, on va faire autre chose
	if reponse.json()['media_type'] != "video":
		image =(reponse.json()['hdurl'])
		print(image)
		resp = requests.get(image, stream=True)
		image = open("photo_jour.png","wb")
		resp.raw.decode_content = True
		shutil.copyfileobj(resp.raw, image)
		del resp
	else:
		urllib.request.urlretrieve(reponse.json()['media_type'], 'video_name.mp4') 

#tweeter un texte
def tweet(obj):
	api.update_status("Hello World!")

def tweet_image_day():

	photo_jour(reponse.json())
	
	#texte dans le tweet
	status = (definition_photo(reponse.json()))
	#Nom du fichier dans lequel notre image est
	filename = ("photo_jour.png")
	
	#poster le tweet
	tweet_image = api.update_with_media(filename, status)
	return tweet_image
def tweet_image_rover():

	sol = description_rover(rover.json())
	
	#texte dans le tweet
	status = ("curiosity sol #{0}".format(sol))
	#Nom du fichier dans lequel notre image est
	filename = ("rover.png")
	
	#poster le tweet
	tweet_rover = api.update_with_media(filename, status)
	return tweet_rover
def tweet_video():

	#ce qui est ecrit en description du tweet
	status = "Curiosity"

	#upload la video
	filename = (".mp4")

	#poste le tweet
	api.update_with_media(filename,status)



#va liker tous les tweet dans lequel nous sommes mentionné
def like_tweet():
	tweets = api.mentions_timeline()
	for tweet in tweets:
		tweet.favorite()


def loop():
	tweet_image_rover()
	tweet_image_day()


schedule.every().day.at("10:00").do(loop(), 4)
while True:
	schedule.run_pending()
	time.sleep(1)


