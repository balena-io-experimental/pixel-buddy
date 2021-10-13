import flowdock
import os
import time
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

from db_functions import DbFunctions

def WriteImageToFilesystem(filepath, fileContents):
    f = open("/data/my_data/" + filepath, "wb")
    f.write(fileContents)
    f.close()

flowNames = (os.getenv('FLOWS') or 'cattlegrid').split(',')
tags = os.getenv('TAGS') or 'proofoflegs'
flowdockToken = os.getenv("FLOWDOCK_TOKEN")  or '241865f63c44215fc3beae531b496b72'
frequency = int(os.getenv("FREQUENCY") or 600)
background = os.getenv("BACKGROUND_COLOUR") or "white"
fontName = os.getenv("FONT") or "arial"
fontSize = os.getenv("FONT_SIZE") or 40
if( None == flowdockToken ):
    exit("No flowdock API in environment variable. Please set it as FLOWDOCK_API")
flowdockClient = flowdock.connect(token=flowdockToken)

while True:
    for flowName in flowNames:
        flow = flowdockClient(org='rulemotion', flow=flowName)
        messages = flow.list(tags=tags, sort='desc', tag_mode='or', limit=100)
        if None == messages:
            continue
        for message in messages:
            if 'uuid' in message:
                messageId = message['uuid']
            else:
                messageId = message['flow'] + "-" + str(message['id'])
            
            if DbFunctions.ImageExists(messageId):
                # we have processed this message!
                continue

            if DbFunctions.SetImage(messageId, str(message['content'])):
                if(message['event'] == 'file'):
                    path = str(message['content']['file_name'])
                    fileContents = flow.download(message['content']['path'])
                    WriteImageToFilesystem(path, fileContents)
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