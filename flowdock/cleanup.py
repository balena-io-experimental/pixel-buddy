from db_functions import DbFunctions
import os
import time

path = "/data/my_data/"
DEBUG = (os.getenv("DEBUG") or "false") != "false"

while True:
    keys = DbFunctions.Keys()
    if DEBUG:
        print("redis keys " + str(keys))
    
    files = os.listdir(path)
    if DEBUG:
        print("files: " + str(files))

    for file in files:
        messageId = file.split('_')[0]
        if DEBUG:
            print("Checking whether to clean up messageId" + messageId)
        if not messageId in keys:
            print("cleaning up " + path + file)
            os.remove(path + file)
    
    time.sleep(60)
