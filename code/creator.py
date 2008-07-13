from threading import Thread
import geom
import messages
import objects

class Creator(Thread):
    def __init__(self, reader_2_creator):
        self.reader_2_creator = reader_2_creator
        self.world_container = WorldContainer()
        self.local_target = None
        self.global_target = (0,0)
        self.isHomeReachable = True
        self.x, self.y, self.radius = None, None, 0.5
        Thread.__init__(self)
    def sendWaypoint(self):
        waypoint = (self.local_target, self.global_target)
        print 'Creator: sending waypoint', waypoint
        self.reader_2_creator = reader_2_creator.put(waypoint)
        
    def isLocalNear(self):
        return (self.x - self.local_target)**2 + (self.y - self.local_target)**2 < self.radius
    def run(self):
        while True:
            msg = self.reader_2_creator.get()
            if msg[0] == messages.TELE:
                self.x, self.y = msg[1][2], msg[1][3]
                if (0 == self.world_container.add_objects(msg)) and (not isLocalNear()):
                    continue                
                else:
                    self.recalculate()
                    self.sendWaypoint()
            elif msg[0] == messages.TERMINATE:
                break
            elif msg[0] == messages.INIT:
                self.x, self.y = msg[1][0],msg[1][1]
                self.recalculate()
                self.sendWaypoint()
                
    def recalculate(self):
        '''calculates  local target. Checks if home is reachable and calculates local waypoint'''
        object_2_distance = []
        isObstacleBetween = False
        for object in self.world_container.hashmap:
            if self.world_container.hashmap[object][0] == objects.object_home:
                continue
            inRect, isObstacle, dist = geom.fromPoint2Line(object, object_2_distance[object][1], self.radius, self.x, self.y, self.global_target)
            object_2_distance.append(object, dist)
            
            if inRect and isObstacle:
                isObstacleBetween = True
        if not isObstacleBetween:
            self.local_target = self.global_target
        else:
            #print 'some cool logic here!'
            cmp_f = lambda x, y: cmp(x[1]*x[1], y[1]*y[1])
            object_2_distance.sort(cmp = cmp_f)
            for i in xrange(len(object_2_distance)):
                obstacle = object_2_distance
                local = getPointToSearch(object, self.global_target, obstacle_radius)
                
                nearest1 =  geom.fromPoint2Line(object_2_distance[(i+1) % len(object_2_distance)], object_2_distance[object][1], self.radius, self.x, self.y, local)
                nearest2 =  geom.fromPoint2Line(object_2_distance[(i-1) % len(object_2_distance)], object_2_distance[object][1], self.radius, self.x, self.y, local)
                
                if (not (nearest1[1] and nearest1[0])) and (not (nearest1[1] and nearest1[0])):
                    self.local_target = local
                    break
            #nearest are at top
    def getPointToSearch(obstacle_coords, target_coords, obstacle_radius):
        obstacle_x, obstacle_y = obstacle_coords
        target_x, target_y = target_coords
        
        vector_2_target = target_x - self.x, target_y - self.y
        vector_2_obstacle = obstacle_x - self.x, obstacle_y - self.y
        
        dot_product = vector_2_target[0]*vector_2_obstacle[0]+vector_2_target[0]*vector_2_obstacle[0]
        
        normal_vector_x =  -vector_2_obstacle[0] + dot_product * vector_2_target[0]
        normal_vector_y =  -vector_2_obstacle[1] + dot_product * vector_2_target[1]
        
        if (normal_vector_x == 0) and (normal_vector_y == 0):
            normal_vector_x, normal_vector_y = -vector_2_obstacle_y,vector_2_obstacle_x
            
        norma = (normal_vector_x**2 + normal_vector_y**2)**0.5
        
        normal_vector_x, normal_vector_y = normal_vector_x/norma, normal_vector_y/norma
        
        
        delta_x, delta_y  = normal_vector_x * (obstacle_radius + self.x), normal_vector_y * (obstacle_radius + self.x)
        
        return obstacle_x + delta_x, obstacle_y + delta_y
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