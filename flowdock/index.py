import flowdock
import os
import time
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import requests
from datetime import datetime
from db_functions import DbFunctions
from text2image import TextFunctions

flowNames = (os.getenv('FLOWS') or 'pub,team-happiness').split(',')
tags = os.getenv('TAGS') or 'proofoflegs,memeservice,announce'
flowdockToken = os.getenv("FLOWDOCK_TOKEN")
frequency = int(os.getenv("FREQUENCY") or 120)
background = os.getenv("BACKGROUND_COLOUR") or "white"
noExpiryTags = (os.getenv('NO_EXPIRY_TAGS') or 'proofoflegs,memeservice').split(',')
expiry = int((os.getenv("EXPIRY") or 12) * 60 * 60)
fontName = os.getenv("FONT") or "arial"
fontSize = os.getenv("FONT_SIZE") or 40
FLUSH = (os.getenv("FLUSH") or "false") != "false"
DEBUG = (os.getenv("DEBUG") or "false") != "false"
imagePath = "/data/my_data/"

if( None == flowdockToken ):
    exit("No flowdock API in environment variable. Please set it as FLOWDOCK_TOKEN")
flowdockClient = flowdock.connect(token=flowdockToken)

def WriteImageToFilesystem(filepath, fileContents):
    f = open(imagePath + filepath, "wb")
    f.write(fileContents)
    f.close()

def GetName(token, uuid) -> int:
    API = 'https://api.flowdock.com'
    if not hasattr(GetName, 'cache'):
        GetName.cache = {}
        resp = requests.get(f'{API}/users', auth=(token, ''))
        assert resp.status_code == 200, (resp.status_code, resp.content)
        # print(resp.json())
        GetName.cache.update({u['id']: u['nick'] for u in resp.json()})

    if not uuid in GetName.cache.keys():
        return "@unknown"
    else:
        return "@" + GetName.cache[int(uuid)]

def GetImageTags(message):
    messageTags = message['tags']
    messageTags.pop(0)
    result = ""
    for tag in messageTags:
        result = result + "#" + tag + " "
    return result

def MessageExpired(message):
    timestamp = (message['sent'])
    convertedTimestamp = datetime.fromtimestamp(round(timestamp / 1000))
    currentTimeUtc = datetime.utcnow()
    difference = ((currentTimeUtc - convertedTimestamp).total_seconds())
    if DEBUG:
        print("The image is " + str(difference) + " seconds old and the expiry is " + str(expiry) + " seconds")
        print("Message expired = " + str(difference > expiry))
    return difference > expiry

def ProcessMessages(messages):
      for message in messages:
            #some random messages don't have a UUID - thanks Flowdock!
            if 'uuid' in message:
                messageId = message['uuid']
            else:
                messageId = message['flow'] + "-" + str(message['id'])
            
            if DbFunctions.ImageExists(messageId):
                # we have processed this message
                if DEBUG:
                    print("Already processed " + messageId)
                continue
            
            #if the message has any tag that's in the don't expire list, ignore the timestamp
            if not (any(item in message['tags'] for item in noExpiryTags)):
                if DEBUG:
                    print("Checking if message has expired")
                if MessageExpired(message):
                    if DEBUG:
                        print("Message has expired")
                    continue

            username = GetName(flowdockToken, message['user'])
            newFileName = messageId + "_" + username + "_" + GetImageTags(message)
            
            if(message['event'] == 'file'):
                if DbFunctions.SetImage(messageId,newFileName):
                    fileContents = flow.download(message['content']['path'])
                    WriteImageToFilesystem(newFileName, fileContents)
            else:
                if("announce" in message['tags']):
                    print(message)
                    if DbFunctions.SetImage(messageId,newFileName):
                        TextFunctions.SaveTextToImage(message['content'], newFileName)

# flush the redis cache - used to reset the device
if FLUSH:
    DbFunctions.Flush()

if DEBUG:
    print("DEBUG logging set :)")

print("On the lookout for these: " + tags)
print("These tags don't expire: " + str(noExpiryTags))
while True:
    for flowName in flowNames:
        print("Checking out what's going on in " + flowName)
        flow = flowdockClient(org='rulemotion', flow=flowName)
        messages = flow.list(tags=tags, sort='desc', tag_mode='or', limit=100)
        if None != messages:
            ProcessMessages(messages)
    time.sleep(frequency)