
import random
import sys
import time
import zmq

import Boat
from BoatConstant import BoatConstant
import Erg_pb2

envelope = "EasyErgsocket"
maxFPS = 60
randomId = random.getrandbits(128)

def main():

    #Socket to publish boat-data
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:5556")

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
    
    
    
    



#Subscribe to the right envelope
# Ascii bytes to unicode str is needed here
if isinstance(envelope, bytes):
    envelope = envelope.decode('ascii')
socket.setsockopt_string(zmq.SUBSCRIBE, envelope)

while True:
    currentMessage = socket.recv_multipart()
    erg = Erg_pb2.Erg()
    erg.ParseFromString(currentMessage[1])
    print erg.displayedMeters

