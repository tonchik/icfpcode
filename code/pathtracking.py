import sched,time
import Queue
import threading
import messages
import tcp_sender

# class Path:
    # def __init__():
        # self.path = []
        # '''
            # (x,y,al,v,va,time,dx,dy,dal,dv,dva,dtime?)
        # '''
# fields = ('x','y','al','v','va','time','dx','dy','dal','dv','dva','dtime')
#pathtracker = pathtracking.PathTracker(sheduler.sock, reader_2_tracker, creator_2_tracker)

class PathTracker(threading.Thread):
    def __init__(self,sock,reader_2_tracker, creator_2_tracker):
        self.sock = sock
        self.reader_2_tracker = reader_2_tracker
        self.creator_2_tracker = creator_2_tracker
        self.exit = False
        #init queues and PathTrackingSheduler
        self.innerQueue = Queue.Queue(10000)
        self.senderQueue = Queue.Queue(10000)
        self.pts = PathTrackingShed(self.innerQueue,self.senderQueue)
        threading.Thread.__init__(self)
    
    def run(self):
        while True:
             self.ParseReaderMessage()
             self.ParseCreatorMessage()
             self.process()
             if self.exit:
                break
        #terminate all
        self.innerQueue.put((messages.TERMINATE,))
        self.senderQueue.put((messages.TERMINATE,))
    def process(self):
        pass
    
    def ParseReaderMessage(self):
        msg = self.reader_2_tracker.get()
        if msg[0] == messages.TERMINATE:
            self.exit = True
        print msg
        
    def ParseCreatorMessage(self):
        pass
        
class CommandToSend:
    def __init__(self,time,command):
        self.command = command
        self.time = time
        
class PathTrackingShed(threading.Thread):
    def __init__(self,q,qout):
        self.sh = sched.scheduler(time.time,self.sleep)
        self.q = q
        self.qout = qout
        self.events = [] #delay : command
        self.timestep = 0.05 # 5 ms
        self.exit = False
        threading.Thread.__init__(self)
    
        
    def send(self,elem):
        print "sending %s"%elem.command
        del self.events[0]
        self.qout.put_nowait((messages.SEND_MESSAGE,elem.command))
        print "len:%d"%len(self.events)
     
    def run(self):
        while True:
            if self.exit:
                break
            msg = self.q.get()
            
            if msg:
                #print "msg in run %s"%(str(msg))
                
                if len(msg)>1 and msg[1]:
                    self.reset(msg[1])
                    self.sh.run()       
                if msg[0] == messages.TERMINATE:
                    break
        
        
    def sleep(self,delay):
        while True:
            msg = None
            
            if not self.q.empty():
                msg = self.q.get_nowait()
                
            if msg:
                #print "msg in sleep %s"%(str(msg))
                if msg[0] == messages.TERMINATE:
                    print "Try to exit!"
                    self.exit = True
                    self.reset([])
                    break
                    
                if len(msg)>1 and msg[1]:
                    self.reset(msg[1])
                    break
            if delay > self.timestep:
                delay -= self.timestep
                time.sleep(self.timestep)
            else:
                break

                
    def reset(self,path):
        cur_time = time.time()
        print "reseting! events len:%d"%(len(self.events))
        for i,elem in enumerate(self.events):
            try:
                self.sh.cancel(elem)
            except RuntimeError:
                print "Event not in que"
        self.events = []
        self.path = path

        for elem in path:
            event = self.sh.enterabs(elem.time,1,self.send,([elem]))
            self.events.append(event)


class Message:
    def __init__(self, data, bExit):
        self.data = data
        self.bExit = bExit
    def isExitMessage(self):
        return self.bExit
        
if __name__ == '__main__':
    '''Tests and example of usage'''
    q1 = Queue.Queue(10000)
    q2 = Queue.Queue(10000)
    #thread.start_new_thread(SchedWrapper, tuple([q1]))
    pts = PathTrackingShed(q1,q2)
    pts.start()
    cur_time = time.time()
    Path = (CommandToSend(cur_time + 1,"al"),CommandToSend(cur_time + 5,"al2"),CommandToSend(cur_time + 12,"bl"))
    msg = ('Send',Path)
    q1.put_nowait(msg)
    time.sleep(10)
    cur_time = time.time()
    Path = (CommandToSend(cur_time + 1,"as"),CommandToSend(cur_time + 5,"ar"),CommandToSend(cur_time + 20,"rr"))
    msg = ('Send',Path)
    q1.put_nowait(msg)
    time.sleep(10)
    msg = (messages.TERMINATE,)
    q1.put_nowait(msg)
    print "Thats all!"
    