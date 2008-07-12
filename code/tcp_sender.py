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
        ready_to_read, ready_to_write, error = select.select([],[self.sock],[self.sock], 30)
        while (totalsent < len(string)) and (len(self.ready_to_write) > 0) and (len(error) == 0):           
            sent = self.sock.send(msg[totalsent:])
            if sent == 0:
                break#raise RuntimeError , "socket connection broken"

            totalsent = totalsent + sent
            ready_to_read, ready_to_write, error = select.select([],[self.sock],[self.sock], 30)

    def run(self):
        print 'Sender starting'
        try:
            msg = self.queue.get()
            if msg[0] == messages.SEND_MESSAGE:
                self.send(msg[1])
            elif msg[0] == messages.TERMINATE:
                break
            else:
                assert(False)

        except Exception, e:
            print e
        finally:
            self.sock.close()