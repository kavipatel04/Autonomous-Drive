import socket
import threading
import random

information = 30
#init
s = socket.socket()
host = '' #ip of raspberry pi
port = 56582
s.bind((host, port))
s.listen(5)
counter = 0
newCounter = 0

def serverThread():
    global information
    global counter
    global s
    while True:
        #print("run")
        try:
            c, addr = s.accept()
            #print ('Got connection from',addr)
            random = random.randint(10, 20)
            if counter > random:
                c.send(bytes('request', 'utf-8'))
                print("request sent")
                msg = c.recv(1024)
                msg = msg.decode('utf-8')
                information = msg
                #print(msg)
                counter = 0
            else: 
                c.send(bytes('standby', 'utf-8'))
            c.close()
        except:
            c.close()
        counter += 1
        print(counter)


        
def main():
    global newCounter
    global information
    
    theServerThread = threading.Thread(target=serverThread)
    theServerThread.start()
    print("threads have started")
    
    while True: 
        if newCounter == 5:
            print(information)
            newCounter = 0
        newCounter += 1
        
    theServerThread.join()
    th.join()
if __name__=='__main__':
    main()
    




    

    
