from threading import Thread
import socket, select
import mqueue
import messages

class Sender(Thread):
    def __init__(self, socket, input_queue) :
        self.socket = socket
        self.queue = input_queue
        Thread.__init__(self)

    def send(self, string):
        totalsent = 0
        ready_to_read, ready_to_write, error = select.select([],[self.socket],[self.socket], 30)
        while (totalsent < len(string)) and (len(ready_to_write) > 0) and (len(error) == 0):           
            sent = self.socket.send(string[totalsent:])
            if sent == 0:
        print 'ERROR sock.send'
                break#raise RuntimeError , "socket connection broken"
            totalsent = totalsent + sent
            ready_to_read, ready_to_write, error = select.select([],[self.socket],[self.socket], 30)

    def run(self):
        print 'Sender starting'
        try:
            while(True) :
                msg = self.queue.get()
                if msg[0] == messages.SEND_MESSAGE:
                    self.send(msg[1])
                elif msg[0] == messages.TERMINATE:
                    print 'Terminate message has been arrived'             
                    break
                else:
                    assert(False)
            
        except Exception, e:
            print e
        finally:
            pass
        print 'Sender exiting'
       
