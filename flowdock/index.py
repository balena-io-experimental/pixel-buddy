import flowdock
import os
import time
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import requests
from datetime import datetime

from db_functions import DbFunctions

flowNames = (os.getenv('FLOWS') or 'cattlegrid').split(',')
tags = os.getenv('TAGS') or 'proofoflegs'
flowdockToken = os.getenv("FLOWDOCK_TOKEN")  
frequency = int(os.getenv("FREQUENCY") or 120)
background = os.getenv("BACKGROUND_COLOUR") or "white"
noExpiryTags = (os.getenv('NO_EXPIRY_TAGS') or 'proofoflegs,memeservice').split(',')
fontName = os.getenv("FONT") or "arial"
fontSize = os.getenv("FONT_SIZE") or 40
if( None == flowdockToken ):
    exit("No flowdock API in environment variable. Please set it as FLOWDOCK_API")
flowdockClient = flowdock.connect(token=flowdockToken)

def WriteImageToFilesystem(filepath, fileContents):
    f = open("/data/my_data/" + filepath, "wb")
    f.write(fileContents)
    f.close()

def GetName(token, uuid) -> int:
    API = 'https://api.flowdock.com'
    if not hasattr(GetName, 'cache'):
        GetName.cache = {}
        resp = requests.get(f'{API}/users', auth=(token, ''))
        assert resp.status_code == 200, (resp.status_code, resp.content)
        
        GetName.cache.update({u['id']: u['nick'] for u in resp.json()})
        
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
    difference = ((currentTimeUtc - convertedTimestamp).total_seconds() / 60 / 60)
    return difference > 24

while True:
    for flowName in flowNames:
        flow = flowdockClient(org='rulemotion', flow=flowName)
        messages = flow.list(tags=tags, sort='desc', tag_mode='or', limit=100)
        
        if None == messages:
            continue
        
        for message in messages:
            #some random messages don't have a UUID - thanks Flowdock!
            if 'uuid' in message:
                messageId = message['uuid']
            else:
                messageId = message['flow'] + "-" + str(message['id'])
            
            if DbFunctions.ImageExists(messageId):
                # we have processed this message
                continue
            
            #if the message has any tag that's in the don't expire list, ignore the timestamp
            if not (any(message['tags']) in noExpiryTags):
                if MessageExpired(message):
                    continue

            if DbFunctions.SetImage(messageId, str(message['content'])):
                if(message['event'] == 'file'):
                    path = str(message['content']['file_name'])
                    fileContents = flow.download(message['content']['path'])
                    username = GetName(flowdockToken, message['user'])
                    
                    newFileName = messageId + "_" + username + "_" + GetImageTags(message)
                    print(newFileName)
                    WriteImageToFilesystem(newFileName, fileContents)
                else:
                    print(message)
                    # img = Image.new('L', (720, 720), color=background)
                    # draw = ImageDraw.Draw(img)
                    # font = ImageFont.truetype(fontName, fontSize)
                    # # print(message['content'])
                    # draw.text((0, 0), message['content'], font=font)
                    # # img.save(message['content']['file_name'])
                    # img.save('test.png')
            # print("Number of messages in redis: " + str(len(storedImages)))
    time.sleep(frequency)