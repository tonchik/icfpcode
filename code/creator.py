from threading import Thread
import messages
import objects

class Creator(Thread):
    def __init__(self, reader_2_creator):
        self.reader_2_creator = reader_2_creator
        self.world_container = WorldContainer()
        Thread.__init__(self)
        
    def run(self):
        print 'Creator started'
        while True:
            msg = self.reader_2_creator.get()
            if msg[0] == messages.TERMINATE:
                break
            if msg[0] == messages.TELE_MESSAGE:
                self.world_container.add_object(msg)
        try:
            pass
        except Exception, e:
            print e
        finally:
            pass

class WorldContainer():
    def __init__(self):
        self.hashmap = {}
        self.prev_hash = 0
        self.timestamp = -1
        
    def add_objects(tele_mess):
        self.timestamp = tele_mess[1][0]
        visible_objects = tele_mess[1][6]
        if hash(visible_objects) == self.prev_hash:
            return
        for object in visible_objects:
            if not object[0] == objects.object_martian:
                self.hashmap[object[1][0], object[1][1]] = (object[0], object[1][2]) 
        self.prev_hash = hash(visible_objects)