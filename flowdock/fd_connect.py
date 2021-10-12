import time 
import subprocess 
import datetime 
import requests
import redis 
import os


def button_preset(channel):
    #
    # play a preset
    #
    # get preset number (1-4) from channel
    preset_channel = [6, 13, 19, 26]
    presety = preset_channel.index(channel)
    # get preset name value from redis
    r = redis.StrictRedis(host='redis', port=6379, db=0, decode_responses=True)
    p = r.get("p" + str(presety + 1))
    print("Preset {0} ({1}) pressed.".format(p, presety))
    # play/display the file image
    text_icon = ["\U000F03A4", "\U000F03A7", "\U000F03AA", "\U000F03AD"]
    play_file(p, text_icon[presety])

