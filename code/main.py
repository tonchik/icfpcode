import tcp_reader
import creator
import pathtracking
import messages

from mqueue import MQueue

if __name__ == '__main__' :
    import sys

    reader_2_creator = MQueue(0)
    reader_2_tracker = MQueue(0)
    creator_2_tracker = MQueue(0)
    
    scheduler = tcp_reader.SocketScheduler(sys.argv[1], int(sys.argv[2]))
    reader = tcp_reader.SocketReader(scheduler.sock, reader_2_creator, reader_2_tracker)
    reader.start()
    
    creator = creator.Creator(reader_2_creator, creator_2_tracker)
    creator.start()

    pathtracker = pathtracking.PathTracker(scheduler.sock, reader_2_tracker, creator_2_tracker)
    pathtracker.start()

    reader.join()
    
  #Create terminate message
    termmsg = (messages.TERMINATE,)
  #Terminate all threads in modules
    reader_2_creator.put(termmsg)
    reader_2_tracker.put(termmsg)
         
    
