import redis 
import os

redisHost = os.getenv("REDIS_HOST") or 'redis'
class DbFunctions():

    def GetImage(imageID):
        #
        # Returns bytes from image stored with key <imageID>
        #
        
        # Don't automatically convert responses from bytes to strings
        r = redis.StrictRedis(host=redisHost, port=6379, db=0, decode_responses=False)
        img = r.get(imageID)
        
        return img


    def SetImage(imageID, imageBytes):
        #
        # Adds an image to the database. Returns 'True' or 'False'
        #
        r = redis.StrictRedis(host=redisHost, port=6379, db=0, decode_responses=False)
        # Add the image to the database, which expires in ex seconds
        result = r.set(imageID, imageBytes, ex=36000)
        
        if not result:
            print("Error setting image!")
        else:
            print("Keys in DB = " + str(r.dbsize()))
            
        # Add a record of the image that does not expire
        result = r.set('NXP' + imageID, '1')
        if not result:
            print("Error setting image record!")
            
        return result
        
        
    def ImageExists(imageID):
        #
        # Returns False if <imageID> has never existed in the database, or True if it has (even if expired)
        #
        r = redis.StrictRedis(host=redisHost, port=6379, db=0, decode_responses=True)
        return ( 1 == r.exists('NXP' + imageID) )    

    
    
