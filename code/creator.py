from threading import Thread
import messages
import objects

class Creator(Thread):
    def __init__(self, reader_2_creator):
        self.reader_2_creator = reader_2_creator
        self.world_container = WorldContainer()
        self.waypoints = None
        
        self.global_target = None
        self.local_target = None
        Thread.__init__(self)
        
    def run(self):
        print 'Creator started'
        while True:
            msg = self.reader_2_creator.get()
            if msg[0] == messages.TELE:
                if 0 == self.world_container.add_objects(msg):
                    continue
                else:
                    self.recalculate()
            elif msg[0] == messages.TERMINATE:
                break
            elif msg[0] == message.INIT:
                self.waypoints = getWaypoints(msg[1][0], msg[1][1], msg[1][4], msg[1][3])
                self.global_target = self.waypoints.pop()
                self.recalculate()
                
    def recalculate(self):
        '''calculates  local target'''
        pass
    #def calculate(self):
    #    pass
    
    def getWaypoints(self, dx, dy, ellipse_a, ellipse_b):
        ''' returns [(point1_x, point1_y), (point2_x, point2_y), ...]'''
        return [(0,0),]
        
class WorldContainer():
    def __init__(self):
        self.hashmap = {}
        self.prev_hash = 0
        self.timestamp = -1
        
    def add_objects(self, tele_mess):
        '''returns 0 if nothing changed, 1 otherwise '''
        self.timestamp = tele_mess[1][0]
        visible_objects = tele_mess[1][6]
        if hash(visible_objects) == self.prev_hash:
            return 0
        for object in visible_objects:
            if not object[0] == objects.object_martian:
                self.hashmap[object[1][0], object[1][1]] = (object[0], object[1][2]) 
        self.prev_hash = hash(visible_objects)
        return 1