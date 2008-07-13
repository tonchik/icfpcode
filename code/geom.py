import math
import cmath

def objectToReperPoints(obj_point, obj_radius) :
    p1 = (obj_point[0] , obj_point[1] + obj_radius)
    p2 = (obj_point[0] , obj_point[1] - obj_radius)
    
    p3 = (obj_point[0] + obj_radius, obj_point[1])
    p4 = (obj_point[0] - obj_radius, obj_point[1])
    return [p1, p2, p3, p4]

def createRect(rect_point1, rect_point2) :
    xmax = max(rect_point1[0], rect_point2[0])
    xmin = min(rect_point1[0], rect_point2[0])
    
    ymax = max(rect_point1[1], rect_point2[1])
    ymin = min(rect_point1[1], rect_point2[1])
    return (xmin, ymin, xmax, ymax)
    
#delta = rover_radius*2
def checkRect(rect, delta):
    xmin, ymin, xmax, ymax = rect    
    
    if xmax - xmin <= delta:
        xmin = xmin - delta/2
        xmax = xmax + delta/2
  
    if ymax - ymin <= delta:
        ymin = ymin - delta/2
        ymax = ymax + delta/2
        
    return (xmin, ymin, xmax, ymax)
    
def isPointInRect(rect, point) :
    xmin, ymin, xmax, ymax = rect
    if (xmin <= point[0] <= xmax) and (ymin <= point[1] <= ymax) :
        return True
    else :
        return False

#rect = (xmin, ymin, xmax, ymax)
def isPointsInRect(points, rect) :
    for point in points:
        if isPointInRect(rect, point) :
            return True
    return False

    
def searchPoint(source, obstacle, obstacle_radius, source_radius, bleft):
    ao = (obstacle[0] - source[0], obstacle[1] - source[1])
    #print 'ao', ao
    ao_module = (ao[0]**2 + ao[1]**2)**0.5
    #print 'ao_module', ao_module
    ao_norm = (ao[0]/ao_module, ao[1]/ao_module)
    #print 'ao_norm', ao_norm
    if bleft:
        sina = (obstacle_radius + source_radius)/ao_module
        cosa = (1 - sina**2)**0.5
    else :
        sina = (obstacle_radius + source_radius)/ao_module
        cosa = -(1 - sina**2)**0.5
    
    #print 'sin cos', sina, cosa
    
    ao_norm_c = complex(ao_norm[0], ao_norm[1])
    #print 'ao_norm_c', ao_norm_c
    #print 'rot', complex(-sina, cosa)
    
    ob = ao_norm_c*complex(-sina, cosa)*(source_radius + obstacle_radius)
    #print 'ob', ob
    result = (source[0] + ao[0] + ob.real, source[1] + ao[1] + ob.imag)
    return result
    
    
def fromPoint2Line(dist_point, dist_radius, rover_radius, line_point1, line_point2):
    if (line_point1[1] == line_point2[1]) :
        a = 0.0
        b = 1.0
        c = line_point1[1]
    else:
        a = 1.0
        b = (line_point1[0] - line_point2[0])/(line_point1[1] - line_point2[1])
        b = -b
        c = -line_point1[0] - b*line_point1[1]
            
        
    print a, b, c
    dist = (a*dist_point[0] + b*dist_point[1]+ c)/((a*a + b*b)**0.5)
    
    rect = createRect(line_point1, line_point2)
    checked_rect = checkRect(rect, 2*rover_radius)
        
    object_points = objectToReperPoints(dist_point, dist_radius)
    b_in_rect = isPointsInRect(object_points, rect)
       
    if abs(dist) > (rover_radius + dist_radius):
        return (b_in_rect, False, dist)
    
    return (b_in_rect, True, dist)

if __name__ == '__main__':
#def searchPoint(source, obstacle, obstacle_radius, source_radius, bright):
    #print fromPoint2Line((15.0, 15.0) ,5.0, 0.5 ,(25.0, 25.0) ,(0, 0))
    print searchPoint((1e9,0), (0,0), 1, 2, True)
    print searchPoint((1e9,0), (0,0), 1, 2, False)
    