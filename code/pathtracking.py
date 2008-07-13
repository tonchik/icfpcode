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

class Params():
    def __init__():
        pass
        
class ParameterEstimator():
    def __init__(self):
        self.Angles = []
        self.expBegin = False
        self.expEnd = False
        self.lastDir = 0
        self.AngleDelay = 0.1
        self.isFirstA = False
        self.isFirstB = False
        self.isAngleEstimated = False
        self.isVelEstimated = False
        self.isVelEstimatedB = False
        
        
    def InitMessage(self,msg):
        dx, dy, time_limit, min_sensor, max_sensor, max_speed, max_turn, max_turn_hard = msg[1]
        localtime = msg[2]
        #self.min_sensor = min_sensor
        #self.max_sensor = max_sensor
        self.params = Params
        self.params.max_speed = max_speed
        self.params.max_turn = max_turn
        self.params.max_turn_hard = max_turn_hard
        self.firsttime = localtime
        
     
    def TeleMessage(self,msg):
        pass
    def VelEst(self):
        self.params.a = (self.secondVel - self.firstVel) /(( 1 - self.firstVel**2/self.params.max_speed**2)*self.AngleDelay)
        self.params.k = self.params.a/self.params.max_speed**2
        print "K est: %f"%(self.params.k)
        print "A est: %f"%(self.params.a)
    def VelEstB(self):
        self.params.b = -(self.params.k*self.firstVelB**2 + (self.secondVelB - self.firstVelB)/self.AngleDelay)
        print "B est: %f"%(self.params.b)
    def AngleEst(self):
        #timestamp, control, x, y, dir, speed, objects,localtime = msg
        self.params.AngleAcs = abs((self.lastDir - self.firstDir)/(self.AngleDelay**2))
        print "Angle est: %f" % self.params.AngleAcs
        print self.lastDir,self.firstDir
        if self.params.AngleAcs * self.AngleDelay > self.params.max_turn_hard:
            print "Achtung!"
    def AngleProc(self,msg):
        timestamp, control, x, y, dir, speed, objects,localtime = msg
        
        if not self.expBegin and not control == '--':
            self.expBegin = True
            
        elif not self.expBegin and control == '--':
            self.firstDir = dir
            self.lastDir = self.firstDir
        
        if self.expBegin:
            if (self.lastDir - dir) < 0.01 and not self.isAngleEstimated:
                self.AngleEst()
                self.isAngleEstimated = True
            else:
                self.lastDir = dir
        if self.isFirstA and control[0] == 'a':
            self.secondVel = speed
            if not self.isVelEstimated:
                self.VelEst()
                self.isVelEstimated = True
        if not self.isFirstA and control[0] == 'a':
            self.firstVel = speed
            self.isFirstA = True
        
        if self.isFirstB and control[0] == 'b':
            self.secondVelB = speed
            if not self.isVelEstimatedB:
                self.VelEstB()
                self.isVelEstimatedB = True
        if not self.isFirstB and control[0] == 'b':
            self.firstVelB = speed
            self.isFirstB = True



class mode:      
    INIT = 'I'
    ANGLE_EXP = 'A'
    TRACK = 'T'
    STANDART='S'

class PathTracker(threading.Thread):
    def __init__(self,sock,reader_2_tracker, creator_2_tracker):
        self.sock = sock
        self.reader_2_tracker = reader_2_tracker
        self.creator_2_tracker = creator_2_tracker
        self.exit = False
        #init queues and PathTrackingSheduler
        self.innerQueue = Queue.Queue(10000)
        self.senderQueue = Queue.Queue(10000)

        self.tcp_sender = tcp_sender.Sender(sock,self.senderQueue)

        self.tcp_sender.start()
        self.parEst = ParameterEstimator()
        self.firstTime = None
        self.mode = mode.ANGLE_EXP
        self.isAngleEstimated = False
        #self.pts = PathTrackingShed(self.innerQueue,self.senderQueue)
        #self.pts.start()
        threading.Thread.__init__(self)

    def run(self):
        while True:
            self.ParseReaderMessage()
            self.ParseCreatorMessage()
            if  hasattr(self,'pts'):
                self.ProcessMode()
                if self.mode == 'test':
                    self.test()                    
                elif self.mode == mode.ANGLE_EXP:
                    self.GenAngleExperiment()
            
            if self.exit:
                    break
        #terminate all
        self.innerQueue.put((messages.TERMINATE,))
        self.senderQueue.put((messages.TERMINATE,))
        
    def ProcessMode(self):
        if self.mode == mode.ANGLE_EXP and self.pts.myTime() > 1.5:
            self.mode = mode.STANDART
    #def CalcAngle(self,time,angle):
        
    def GenPath(self,time,delay,event1,event2,path):
        path.append(CommandToSend(time,event1))
        path.append(CommandToSend(time + delay,event2))
        path.sort(key = lambda x:x.time)
   
    def GenAngleExperiment(self):
        if not self.isAngleEstimated:
            path = []
            self.GenPath(0.41,0.0,"r;","r;",path)
            self.GenPath(0.41 + self.parEst.AngleDelay,0.0,"l;","l;",path)
            self.GenPath(0.78,0.0,"a;",";",path)
            self.GenPath(0.92 + self.parEst.AngleDelay,0.0,"b;","b;",path)
            self.isAngleEstimated = True
            #self.GenPath(1.2,0.0,"r;","r;",path)
            #self.GenPath(1.3,0.0,"l;","l;",path)
            # self.GenPath(4.0,0.0,";","r;",path)
            # self.GenPath(4.05,0.0,";","l;",path)
            # self.GenPath(5.0,0.0,";","r;",path)
            # self.GenPath(5.1,0.0,";","l;",path)
            # self.GenPath(6.0,0.0,";","r;",path)
            # self.GenPath(6.2,0.0,";","l;",path)
            # self.GenPath(7.0,0.0,";","r;",path)
            # self.GenPath(7.3,0.0,";","l;",path)
            msg  = ('Send',path)
            #print "Sending msg:%s"%str(msg)
            self.innerQueue.put(msg)
            #return (0.4,0.5)
        
    def ParseReaderMessage(self):
        if not self.reader_2_tracker.isEmpty():
            msg = self.reader_2_tracker.get()
            #print msg
            if msg[0] == messages.TERMINATE:
                self.exit = True
            elif msg[0] == messages.INIT:
                self.parEst.InitMessage(msg)
            elif msg[0] == messages.TELE:
                self.parEst.TeleMessage(msg[1])
                if self.mode == mode.ANGLE_EXP:
                    self.parEst.AngleProc(msg[1]);
                        
                if not self.firstTime:
                    timestamp,localtime = msg[1][0],msg[1][-1]
                    self.firstTime = localtime # - timestamp/10
                    self.pts = PathTrackingShed(self.innerQueue,self.senderQueue,self.firstTime)
                    self.pts.start()
                    
        
    def ParseCreatorMessage(self):
        pass

    # def test(self):
        # if  hasattr(self,'pts') and not hasattr(self,'once'):
            #cur_time = time.time()
            # cur_time = 0
            # self.once = True
            # path = (CommandToSend(1.001 + cur_time,"al;"),CommandToSend(5.0 + cur_time,"ar;"),CommandToSend(6.0 + cur_time,"b;"),CommandToSend(6.5 + cur_time,"r;"),CommandToSend(6.6 + cur_time,"a;"))
            # msg  = ('Send',path)
            # print "put in inner que!"
            # self.innerQueue.put(msg)
            #time.sleep(20)
        
class CommandToSend:
    def __init__(self,time,command):
        self.command = command
        self.time = time

def makeTimefunc(firstTime):
    def blah():
        return time.time() - firstTime 
    return blah     

class PathTrackingShed(threading.Thread):
    def __init__(self,q,qout,firstTime = 0):
        #self.curTime = time.time()
        print "firstTime %d"%firstTime
        self.firstTime = firstTime
        self.timeErr = 0
        self.sh = sched.scheduler(self.myTime,self.sleep)
        #self.sh = sched.scheduler(time.time,self.sleep)
        self.q = q
        self.qout = qout
        self.events = [] #delay : command
        self.timestep = 0.3 # 50 ms
        self.exit = False
        threading.Thread.__init__(self)
    
    def setTimeErr(self,timeErr):
        '''check if we can brake smth'''
        pass
        
    def myTime(self):
        return time.time() - self.firstTime - self.timeErr
        
    def send(self,elem):
        #print "sending %s %f"%(elem.command,time.time())
        del self.events[0]
        self.qout.put_nowait((messages.SEND_MESSAGE,elem.command))
        #print "len:%d"%len(self.events)
     
    def run(self):
        while True:
            if self.exit:
                break
            msg = self.q.get()
            
            if msg:
                print "msg in run %s"%(str(msg))
                
                if msg[0] == 'Send':
                    self.reset(msg[1])
                    self.sh.run()  
                elif msg[0] == 'Append':
                    self.reset(msg[1],False)
                    self.sh.run()
                elif msg[0] == messages.TERMINATE:
                    break
    
        
    def sleep(self,delay):
        while True:
            msg = None
            
            if not self.q.empty():
                msg = self.q.get_nowait()
                
                if msg:
                    print "msg in sleep %s"%(str(msg))
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
                time.sleep(delay)
                break

                
    def reset(self,path,clear = True):
        cur_time = time.time()
        
        if clear:
            print "reseting! events len:%d"%(len(self.events))
            for i,elem in enumerate(self.events):
                try:
                    self.sh.cancel(elem)
                except RuntimeError:
                    print "Event not in que"
            
                    
            self.events = []
            
        self.path = path
        for elem in path:
            print elem
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
    