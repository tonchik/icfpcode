import math

def fromPoint2Line(dist_point, dist_radius, rover_radius, line_point1, line_point2):
    if (line_point1[1] == line_point2[1]) :
        a = 0.0
        b = 1.0
        c = line_point1[1]
    else:
        a = 1.0
        b = (line_point1[0] - line_point2[0])/(line_point1[1] - line_point2[1])
        c = -line_point1[0] - b*line_point1[1]
        b = -b    
    dist = (a*dist_point[0] + b*dist_point[1]+ c)/((a*a + b*b)**0.5)
    print 'a,b,c', a,b,c
    
    xmax = max(line_point1[0], line_point2[0])
    xmin = min(line_point1[0], line_point2[0])
    
    ymax = max(line_point1[1], line_point2[1])
    ymin = min(line_point1[1], line_point2[1])
    
    if ((dist_point[0] > xmin) and (dist_point[0] < xmax)
        and (dist_point[1] > ymin) and (dist_point[1] < ymax)) :
        b_in_rect = True
    else :
        b_in_rect = False
       
    if abs(dist) > (rover_radius + dist_radius):
        return (b_in_rect, False, dist)
    
    return (b_in_rect, True, dist)
        
        
class MPoint:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r
    
    def mprint(self) :
        print 'Point', self
        print self.x, self.y, self.r
    def distToLine(self, mLine):
        print 'dist to line'
        mLine.mprint()
        self.mprint()
        assert(mLine.a != 0 or mLine.b != 0)
        d = (mLine.a*self.x + mLine.b*self.y + mLine.c)/((mLine.a*mLine.a + mLine.b*mLine.b)**0.5)
        print d
        return d

    def isObstacleInStripe(self, destp, objpoint):
        assert(objpoint.r > 0)
        assert(self.r > 0)
        h = self.r
        line = MLine(self, destp)
        dist = objpoint.distToLine(line)
        if abs(dist) > (h + objpoint.r):
            return (False, dist)
        return (True, dist)
     
class MLine:
    def __init__(self, point,  point2):
        x = point2.x
        y = point2.y
        if (y == point.y) :
            self.a = 0.0
            self.b = 1.0
            self.c = y
        else :
            self.a = 1.0
            self.b = (x - point.x)/(y - point.y)
            self.c = -x - self.b*y
    def mprint(self):
        print 'mline', self
        print self.a, self.b, self.c
        
if __name__ == '__main__':
    obstacle = (1.0, 1.0)
    obstacle_radius = 1
    
    rover = (0.0, 0.0)
    rover_radius = 0.2
    
    target = (2.0, 2.0)
       
    br, b, d = fromPoint2Line(obstacle, obstacle_radius, rover_radius, rover, target)#rover.isObstacleInStripe(destination, obstacle)
    print br, b, d
    
    obstacle2 = (-obstacle[0], -obstacle[1])
    
    print obstacle2
    br, b, d = fromPoint2Line(obstacle2, obstacle_radius, rover_radius, rover, target)#rover.isObstacleInStripe(destination, obstacle)
    print br, b, d
 
    
    