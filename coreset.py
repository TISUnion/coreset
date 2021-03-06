# -*- coding: utf-8 -*-
import requests
import os
import sys
import traceback
from time import sleep

helpmsg = '''this is a tool for setting the server core jar
usage:!!coreset [minecraft server jar URL]
'''

def onServerInfo(server, info):
  if info.isPlayer == 1:
    if info.content.startswith('!!coreset'):
      args = info.content.split(' ')
      if len(args) == 1:
        for singleline in helpmsg.splitlines():
          server.say(singleline)
      elif (len(args)>2) and (info.content.endswith('.jar')):
        server.say('Wrong URL')
      elif args[1].startswith('https://launcher.mojang.com'):
        server.say('[coreset]:starting download...')
        try:
          response = requests.get(args[1],timeout = 3.5)
          if (response.status_code == requests.codes.ok):
            with open('./server/new.jar','wb') as handle:
              handle.write(response.content)
          else:
            server.say('Failed to download: ' + response.status_code)
        except:
          server.say('Failed to download.try later?')
          print(traceback.format_exc())
          sys.exit(0)
        server.say('download scucessful.restarting server in 10 seconds')
        sleep(1)
        for countdown in range(1,10):
          server.say('[coreset]:COUNTDOWN! REBOOTING IN ' + str(10-countdown) + ' SECOND(S)')
          sleep(1)
        server.stop()
        os.system('mv ./server/server.jar ./server/old.jar')
        os.system('mv ./server/new.jar ./server/server.jar')
        try:
          server.start()
          os.system('rm -f ./server/old.jar')
        except:
          os.system('mv ./server/old.jar ./server/server.jar')
          server.start()
          
