from twisted.internet import reactor
from twisted.python import log
from kademlia.network import Server
import sys
from kademlia.utils import deferredDict
import socket
import pickle
from collections import Counter

log.startLogging(sys.stdout)

st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
st.connect(('10.0.0.1', 8468))  # connecting to a UDP address doesn't send packets
local_ip = st.getsockname()[0]
print local_ip
st.close()

def udpListener():
    print "Listening UDP"  
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    host = local_ip #Host i.p
    port = 8468 #Reserve a port for your service
    sock.bind((host,port))
    while True:
        data, addr = sock.recvfrom(1024)
        if data is not None:
            break
    print "Data : ",  data
    print "Requester : ",addr
    sock.close()

def resourceDiscovery():
    print "Sending broadcast request"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = "Give me your resources"
    sock.sendto(data, ('10.0.0.2', 8468))
    sock.sendto(data, ('10.0.0.3', 8468))

def done(result):
    print "Key result:", result
    fp = open('Textfile.txt','w')
    result = str(fp)
    fp.write(result)
    #pickle.dump(result, fp)
    print "write to file Completed"

    #reactor.stop()
def wordprocess(x):    
    fpi=open('Textfile.txt','r')
    fpo = open('TextOut.txt','w')
    vowels=("A","E","I","O","U","a","e","i","o","u")
    text = fpi.read()
    s_without_vowels = ""
    for x in text:
       if x not in vowels:
           s_without_vowels += x
    return s_without_vowels
    #pickle.dump(new_str, fpo)
    result = remove_vowels('s')
    print result
    fpo.write(s_without_vowels)

def setDone(result, server):
    print "Adding 'abc' in to the network"
    a = server.get('110').addCallback(done)
    b = server.get('110').addCallback(wordprocess)

def bootstrapDone(found, server):
    print "Setting key 107 and value xxx"
    server.set("107", "xxx").addCallback(setDone, server)

udpListener()
server = Server()
server.listen(8468)
server.bootstrap([("10.0.0.1", 8468)]).addCallback(bootstrapDone, server)


reactor.run()
