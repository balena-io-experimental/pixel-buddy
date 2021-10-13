import time 
import subprocess 
import datetime 
import requests
import redis 
import os


def GetImage(imageID):
    #
    # Returns bytes from image stored with key <imageID>
    #
    
    # Don't automatically convert responses from bytes to strings
    r = redis.StrictRedis(host='redis', port=6379, db=0, decode_responses=False)
    img = r.get(imageID)
    
    return img


def SetImage(imageID, imageBytes):
    #
    # Adds an image to the database. Returns 'OK' or 'ERROR'
    #
    r = redis.StrictRedis(host='redis', port=6379, db=0, decode_responses=True)
    # Add the image to the database, which expires in ex seconds
    ret = r.set(imageID, imageBytes, ex=36000)
    if ret != 'OK':
        print("Error setting image!")
        ret = "ERROR"
        
    # Add a record of the image that does not expire
    ret = r.set('NXP' + imageID, '1')
    if ret != 'OK':
        print("Error setting image record!")
        ret = "ERROR"
        
    return ret
    
    
def ImageExists(imageID):
    #
    # Returns 0 if <imageID> has never existed in the database, or 1 if it has (even if expired)
    #
    r = redis.StrictRedis(host='redis', port=6379, db=0, decode_responses=True)
    ret = r.exists('NXP' + imageID)
    
    return ret
    
    

    
    
