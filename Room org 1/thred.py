import threading
import time
global t
t = 0
print "hi"
def video():
    global t
    t = 52
    time.sleep(5)
    t = 100
def show():
    while t!=100:
        print t
    if t == 100:
        print t
    
thread1= threading.Thread(target = video, args = ())
thread2= threading.Thread(target = show, args = ())
thread1.start()
thread2.start()

##thread1.join()
##thread2.join()
##thread.start_new_thread(video,())
##thread.start_new_thread(show,())
