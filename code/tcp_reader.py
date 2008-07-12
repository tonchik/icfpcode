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
        
        
class MessageParser():
    
    def __init__(self):
        self.dict = {'I':self.init_message, 'T':self.telemetry_message, 'B': self.die, 'C': self.die, 'K':self.die}
    def parse(self, mess):
        parse_funct = self.dict[mess[0]]
        parse_funct(mess)
        #print mess
    def init_message(self, string):
        print 'init', string#pass
    def telemetry_message(self, string):
        print 'telemetry', string
    def die(self, string):
        print 'die', string
    def sucess(self, string):
        print 'success', string        
    def end(self, string):
        print 'end', string
        
class SocketReader(Thread):
    def __init__(self, sock):
        self.sock = sock
        self.current_message = ''
        self.parser = MessageParser()
        #print self.parser
        #print
        Thread.__init__(self)
        
    def sendMessage(self,mess):
        self.parser.parse(mess)
    def reliableRead(self):
            chunk = self.sock.recv(MSG_BUFF)
            if chunk == '':
                return -1
            self.current_message = self.current_message + chunk
            if DELIM in self.current_message:
                list = self.current_message.split(";")
                for mes in list[:-1]:
                    self.sendMessage(mes)
                self.current_message = list[-1]
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
        

        
if __name__ == '__main__':
    import sys
    #print 'creating schelduler'
    scheduler = SocketScheduler(sys.argv[1], int(sys.argv[2]))
    #print 'created'
    #print 'creating reader'
    reader = SocketReader(scheduler.sock)
    #print 'starting reader'
    reader.start()