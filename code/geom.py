import math
            
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
    rover      = MPoint(0.0, 0.0, 0.2)
    obstacle = MPoint(1.0, 1000.0, 0.3)
    destination = MPoint(1.0, 1.0, 0.0)
    
    b, d = rover.isObstacleInStripe(destination, obstacle)
    print b, d