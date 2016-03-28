
import random
import sys
import time
import zmq

import Boat
from BoatConstant import BoatConstant
import Erg_pb2

PUBADDRESS = "tcp://127.0.0.1:21744"
envelope = "EasyErgsocket"
maxFPS = 60

def createErg(name, playertype):
    erg = Erg_pb2.Erg()
    erg.ergId = str(random.getrandbits(128))
    erg.name = name
    erg.ergtype = Erg_pb2.ROW
    erg.playertype = playertype
    erg.distance = 0.0
    return erg

def main():
    #Socket to publish boat-data
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind(PUBADDRESS)
    print "Connected to " + PUBADDRESS

    bots = []
    bots.append(BoatConstant("Bot1", pace=120, spm=18))
    bots.append(BoatConstant("Bot2", pace=121, spm=22))
    bots.append(BoatConstant("Bot3", pace=122, spm=20))
    bots.append(BoatConstant("Bot4", pace=123, spm=17))
    bots.append(BoatConstant("Bot5", pace=124, spm=24))

    boats = []
    boats.append(createErg("Player", Erg_pb2.HUMAN))
    boats.append(createErg("Bot1", Erg_pb2.BOT))
    boats.append(createErg("Bot2", Erg_pb2.BOT))
    boats.append(createErg("Bot3", Erg_pb2.BOT))
    boats.append(createErg("Bot4", Erg_pb2.BOT))

    startTime = time.time()
    while True:
        #move the boat
        currentTime = time.time() - startTime
        for bot in bots:
            bot.move(currentTime)

        messages = [envelope]
        for index, boat in enumerate(boats):
            boat.distance = bots[index].distance
            boat.cadence = bots[index].spm
            boat.paceInSecs = bots[index].pace
            boat.exerciseTime = currentTime
            messages.append(boat.SerializeToString())
        socket.send_multipart(messages)

        #sleep some time to run not faster than maxFPS
        sleepTime = 1./maxFPS
        time.sleep(sleepTime)

    #we never get here but clean up anyhow
    publisher.close()
    context.term()

if __name__=="__main__":
    main()
