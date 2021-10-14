import redis 
import os

redisHost = os.getenv("REDIS_HOST") or 'redis'
expiry = int((os.getenv("EXPIRY") or 12) * 60 * 60)
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
        result = r.set(imageID, imageBytes, ex=expiry)
        
        if not result:
            print("Error setting image!")
        else:
            print("Keys in DB = " + str(r.dbsize()))
       
            
        return result
        
        
    def ImageExists(imageID):
        r = redis.StrictRedis(host=redisHost, port=6379, db=0, decode_responses=True)
        return ( 1 == r.exists(imageID) )    

    def Flush():
        print("Flushing redis")
        r = redis.StrictRedis(host=redisHost, port=6379, db=0, decode_responses=True)
        r.flushall()
    
    def Keys():
        r = redis.StrictRedis(host=redisHost, port=6379, db=0, decode_responses=True)
        return r.keys('*')
    
    
