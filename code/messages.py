#message types

INIT = 'I'

# INIT_MESSAGE = ( 'I', (    dx, dy, time_limit, min_sensor, max_sensor, max_speed, max_turn, max_turn_hard    )  )
#


TELE = 'T'
#TELE_MESSAGE ::= ('T', ( timestamp, !control!, x, y, dir, speed, !objects!))
# !objects! : == [None] | [('b', (x, y, radius))] | [( 'h', (x,y,radius)] | [('c', (x,y,radius)] | [('m', (x,y, dir, speed)]
#
#!control! :== (states.accelerating|states.rolling| states.breaking;  states.turn_left| states.turn_left_hard|....)
#acelerate :== 

END = 'E'
# END_MESSAGE = ('E', (time, score))
#

DIE = 'D'
#DIE_MESSAGE = ('D', (reason, timestamp)
#
SUCCESS = 'S'
#SUCCESS_MESSAGE = ('S', (timestamp))
#

SEND_MESSAGE = 'N'
#for Sender:
#SEND_MESSAGE = ('N', command = ';' | 'a;' | 'b;' | 'l;' | 'r;' | 'al;' | 'ar;' | 'bl' | 'br')
#

TERMINATE = 'X'

SEND_MESSAGE = 'S'

#
#TERMINATE_MESS = ('X',)


# if message[0] == messages.TERMINATE:
    #exit
#elif message[0] == messages.TELE:
    #s'df'dskf'ksdf