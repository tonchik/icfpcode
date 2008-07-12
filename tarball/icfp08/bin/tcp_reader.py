from threading import Thread
import socket, select

MSG_BUFF = 2048
DELIM = ';'
class SocketScheduler:
    def __init__(self, dist_host, dist_port):
        self.dist_port = dist_port
        self.dist_host = dist_host
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.sock.connect((self.dist_host, self.dist_port))
        
        self.sock.setblocking(0)
        
        
        
        
class SocketReader(Thread):
    def __init__(self, sock):
        self.sock = sock
        self.current_message = ''
        
        Thread.__init__(self)
        
    def sendMessage(self,mess):
        pass#print 'Message:%s'%mess
    def reliableRead(self):
            #msg = ''
            #while ';' not in self.current_message:
            chunk = self.sock.recv(MSG_BUFF)
            if chunk == '':
                return -1#RuntimeError, "socket connection broken"
            self.current_message = self.current_message + chunk
            while DELIM in self.current_message:
                #self.sendMessage()
                pos = self.current_message.find(DELIM)
                self.sendMessage(self.current_message[:pos])
                if pos < len(self.current_message):
                    self.current_message = self.current_message[pos+1:]
                else:
                    self.current_message = ''
            return 0        
    def run(self):
        try:
            ready_to_read, ready_to_write, error = select.select([self.sock],[],[self.sock], 30)
            while (len(ready_to_read) > 0) and (len(error) == 0):
                if -1 ==  self.reliableRead():
                    break
                ready_to_read, ready_to_write, error = select.select([self.sock],[],[self.sock], 30)
            #print self.current_message
        #print 'end!'
        finally:
            self.sock.close()
        
def MessageParser():
    
    def __init__(self):
        self.dict = {'I':init_message, 'T':telemetry_message, 'B': boulder, 'C': crater, 'K':martian}
    def parse(self, mess):
        parse_funct = self.dict[mess[0]]
    def init_message(self, string):
        pass
    def telemetry_message(self, string):
        pass
    def boulder(self, string):
        pass
    def crater(self, string):
        pass
    def martian(self, string):
        pass
        
if __name__ == '__main__':
    import sys
    #print 'creating schelduler'
    scheduler = SocketScheduler(sys.argv[1], int(sys.argv[2]))
    #print 'created'
    #print 'creating reader'
    reader = SocketReader(scheduler.sock)
    #print 'starting reader'
    reader.start()