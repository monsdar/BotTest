
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
randomId = random.getrandbits(128)

def main():

    #Socket to publish boat-data
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.connect(PUBADDRESS)
    print "Connected to " + PUBADDRESS

    botBoat = BoatConstant("Bot1")
    
    startTime = time.time()
    while True:
        #move the boat
        currentTime = time.time() - startTime
        botBoat.move(currentTime)
        
        erg = Erg_pb2.Erg()
        erg.ergId = str(randomId)
        erg.name = "TestBot"
        erg.ergtype = Erg_pb2.ROW
        erg.playertype = Erg_pb2.BOT
        erg.distance = botBoat.distance
        currentMessage = erg.SerializeToString()
        
        socket.send_multipart([envelope, currentMessage])
        
        #sleep some time to run not faster than maxFPS
        sleepTime = 1./maxFPS
        time.sleep(sleepTime)
        
    #we never get here but clean up anyhow
    publisher.close()
    context.term()

if __name__=="__main__":
    main()
