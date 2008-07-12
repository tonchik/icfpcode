import sched,time
import Queue
import thread

class Path:
    def __init__():
        self.path = []
        '''
            (x,y,al,v,va,time,dx,dy,dal,dv,dva,dtime?)
        '''
fields = ('x','y','al','v','va','time','dx','dy','dal','dv','dva','dtime')

def SchedWrapper(q):
    pts = PathTrackingShed(q)
    pts.update()
    
class PathTrackingShed:
    def __init__(self,q):
        self.sh = sched.scheduler(time.time,self.sleep)
        self.q = q
        self.events = [] #delay : command
        self.timestep = 0.05 # 5 ms
        self.exit = False
       
    def send(self,elem):
        print "sending%s"%elem
        del self.events[0]
        print "len:%d"%len(self.events)
     
    def update(self):
        while True:
            msg = self.q.get()
            if msg.data:
                self.reset(msg.data)
                self.sh.run()
            
            if self.exit:
                break
        
        
    def sleep(self,delay):
        while True:
            msg = None
            try:
                msg = self.q.get_nowait()
            except Exception,e:
                #print e
                pass
                
            if msg:
                if msg.isExitMessage():
                    self.exit = True
                    break
                    
                if msg.data:
                    self.reset(msg.data)
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
            event = self.sh.enterabs(elem['time'],1,self.send,([elem]))
            self.events.append(event)


class Message:
    def __init__(self, data, bExit):
        self.data = data
        self.bExit = bExit
    def isExitMessage(self):
        return self.bExit
        
if __name__ == '__main__':
    q1 = Queue.Queue(10000)
    thread.start_new_thread(SchedWrapper, tuple([q1]))
    cur_time = time.time()
    Path = ({'time' : cur_time + 2  ,"blah" : 'stroka'},{'time' : cur_time + 12  ,"blah0" : 'stroka'},{'time' : cur_time + 20  ,"blah00" : 'stroka'})
    msg = Message(Path, False)
    q1.put_nowait(msg)
    time.sleep(10)
    cur_time = time.time()
    Path = ({'time' : cur_time + 2  ,"blah2" : 'stroka'},{'time' : cur_time + 12  ,"blah3" : 'stroka'},{'time' : cur_time + 20  ,"blah4" : 'stroka'})
    msg = Message(Path, False)
    q1.put_nowait(msg)
    time.sleep(40)
    msg =Message(None,True)