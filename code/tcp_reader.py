from threading import Thread

import socket, select
import messages

MSG_BUFF = 4096
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
        self.dict = {'I':self.init_message, 'T':self.telemetry_message, 'B': self.die_message, 'C': self.die_message, 'K':self.die_message, 'S':self.success_message, 'E': self.end_message}
    def send_message_to_queue(self, mess):
        print mess
        
    def parse(self, mess):
        parse_funct = self.dict[mess[0]]
        parse_funct(mess)
        #print mess
    def init_message(self, string):
        turple = dx, dy, time_limit, min_sensor, max_sensor, max_speed, max_turn, max_turn_hard = string.split()[1:]
        message = (messages.INIT, turple)
        self.send_message_to_queue(message)
        #print 'init', dx, dy, time_limit, min_sensor, max_sensor, max_speed, max_turn, max_turn_hard
    def telemetry_message(self, string):
        turple = string.split()
        message = (messages.TELE, turple)
        self.send_message_to_queue(message)
        #pass#print 'telemetry', string
    def die_message(self, string):
        reason ,timestamp = string.split()#print 'die', string
        message = (messages.DIE, (reason, timestamp))
        self.send_message_to_queue(message)
        #print 'dead!', reason
    def success_message(self, string):
        time = string.split()[1]#print 'success', string 
        message = (messages.SUCESS, (time))
    def end_message(self, string):
        time, score = string.split()[1:]#print 'end', string
        #print 'end score:', score
        message = (messages.END, (time, score))
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

        except Exception, e:
            print e
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