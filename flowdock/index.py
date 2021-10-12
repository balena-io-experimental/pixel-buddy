import flowdock
import os
# import redis
import time
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 

# to be replaced by Redis 
def GetImage(imageId):
    if( imageId in storedImages ):
        return storedImages[imageId]

def SetImage(imageId, path):
    if( None == GetImage(imageId) ):
        print("Added image " + imageId)
        storedImages[imageId] = path
        return True
    else:
        return False

def SendImage(filepath, fileContents):
    f = open(filepath, "wb")
    f.write(fileContents)
    f.close()

# to be removed when we have redis
processedMessages = []
storedImages = {}

flowNames = (os.getenv('FLOWS') or 'pub').split(',')
tags = os.getenv('TAGS') or '@team'
flowdockToken = os.getenv("FLOWDOCK_TOKEN")
frequency = int(os.getenv("FREQUENCY") or 600)
background = os.getenv("BACKGROUND_COLOUR") or "black"
fontName = os.getenv("FONT") or "arial"
fontSize = os.getenv("FONT_SIZE") or 40
if( None == flowdockToken ):
    exit("No flowdock API in environment variable. Please set it as FLOWDOCK_API")
flowdockClient = flowdock.connect(token=flowdockToken)

while True:
    for flowName in flowNames:
        flow = flowdockClient(org='rulemotion', flow=flowName)
        messages = flow.list(tags=tags, sort='desc', tag_mode='or', limit=100)
        if( None == messages):
            continue
        for message in messages:
            if( 'uuid' in message ):
                messageId = message['uuid']
            else:
                messageId = message['flow'] + "-" + str(message['id'])

            if SetImage(messageId, message['content']):
                if(message['event'] == 'file'):
                    path = str(message['content']['file_name'])
                    fileContents = flow.download(message['content']['path'])
                    SendImage(path, fileContents)
                else:
                    print(message)
                    img = Image.new('L', (720, 720), color=background)
                    draw = ImageDraw.Draw(img)
                    font = ImageFont.truetype(fontName, fontSize)
                    draw.text((0, 0), message['content'], font=font)
                    img.save(str(message['content']['file_name']))
            print("Number of messages in redis: " + str(len(storedImages)))
    time.sleep(frequency)