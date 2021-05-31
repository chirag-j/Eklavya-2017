import numpy as np

import cv2
i = 0
go1 = False
go2 = False
go3 = False
go4 = False

##global i

def fill(a, x, y):
    global i, go1, go2, go3, go4
    i+=1
    if x>0 and y>0 and x<5 and y<4:
        if (a[x-1,y]==0):
            a[x-1,y] = i
            go1 = True
        if(a[x+1,y] == 0):
            a[x+1, y] = i
            go2 = True
        if(a[x,y-1] == 0):
            a[x,y-1] = i
            go3 = True
        if(a[x,y+1] == 0):
            a[x,y+1] = i
            go4 = True
            
        if go1 == True:
            go1 = False
            fill(a,x-1,y)
        if go2 == True:
            go2 = False
            fill(a,x+1, y)
        if go3 == True:
            go3 = False
            fill(a,x,y-1)
        if go4 == False:
            go4 = False
            fill(a,x,y+1)
        
    if x>0 and y==0 and x<5:
        if (a[x-1,y]==0):
            a[x-1,y] = i
            go1 = True
        if(a[x+1,y] == 0):
            a[x+1, y] = i
            go2 = True
        if(a[x,y+1] == 0):
            a[x,y+1] = i
            go4 = True
            
        if go1 == True:
            go1 = False
            fill(a,x-1,y)
        if go2 == True:
            go2 = False
            fill(a,x+1, y)
        if go3 == True:
            go3 = False
            fill(a,x,y-1)
        if go4 == False:
            go4 = False
            fill(a,x,y+1)
        
            

    if x==0 and y>0 and y<4:
        if(a[x,y-1] == 0):
            a[x,y-1] = i
            go3 = True
        if(a[x,y+1] == 0):
            a[x,y+1] = i
            go4 = True
        if(a[x+1,y] == 0):
            a[x+1, y] = i
            go2 = True

        if go1 == True:
            go1 = False
            fill(a,x-1,y)
        if go2 == True:
            go2 = False
            fill(a,x+1, y)
        if go3 == True:
            go3 = False
            fill(a,x,y-1)
        if go4 == False:
            go4 = False
            fill(a,x,y+1)
        
                
    if y>0 and x==5 and y<4:
        if(a[x,y-1] == 0):
            a[x,y-1] = i
            go3 = True
        if(a[x,y+1] == 0):
            a[x,y+1] = i
            go4 = True
        if(a[x-1,y] == 0):
            a[x-1, y] = i
            go1 = True
            
        if go1 == True:
            go1 = False
            fill(a,x-1,y)
        if go2 == True:
            go2 = False
            fill(a,x+1, y)
        if go3 == True:
            go3 = False
            fill(a,x,y-1)
        if go4 == False:
            go4 = False
            fill(a,x,y+1)
        
            
    if x>0 and x<5 and y==4:
        if (a[x-1,y]==0):
            a[x-1,y] = i
            go1 = True
        if(a[x+1,y] == 0):
            a[x+1, y] = i
            go2 = True
        if(a[x,y-1] == 0):
            a[x,y-1] = i
            go3 == True

        if go1 == True:
            go1 = False
            fill(a,x-1,y)
        if go2 == True:
            go2 = False
            fill(a,x+1, y)
        if go3 == True:
            go3 = False
            fill(a,x,y-1)
        if go4 == False:
            go4 = False
            fill(a,x,y+1)

    if x==0 and y==0:
        if(a[x+1,y] == 0):
            a[x+1, y] = i
            go2 = True
        if(a[x,y+1] == 0):
            a[x,y+1] = i
            go4 = True
        
        if go2 == True:
            go2 = False
            fill(a,x+1, y)
        if go4 == False:
            go4 = False
            fill(a,x,y+1)

    if x==5 and y==4:
        if (a[x-1,y]==0):
            a[x-1,y] = i
            go1 = True
        if(a[x,y-1] == 0):
            a[x,y-1] = i
            go3 = True

        if go1 == True:
            go1 = False
            fill(a,x-1,y)
        if go3 == True:
            go3 = False
            fill(a,x,y-1)

        
        

arr = np.zeros([6,5], np.uint8)
arr[2,2] = 100
fill(arr, 2, 2)
arr[2,2] = 0
print arr


