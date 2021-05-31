import numpy as np
import cv2
i = 0
go1 = False
go2 = False
go3 = False
go4 = False
x = np.zeros([100], np.uint8)
y = np.zeros([100], np.uint8)

##global iy
ab = 0
def fill(a):
    global i, ab
    i+=1

    for b in range(0,len(a)):
        for c in range(0,len(a[0])):
            if a[b,c] == i-1:
                x[ab],y[ab] = b,c
                ab+=1
            
                
    for n in range(0,ab):
        
        if x[n]>0 and y[n]>0 and x[n]<5 and y[n]<4:
            if (a[x[n]-1,y[n]]==100):
                a[x[n]-1,y[n]] = i
            if(a[x[n]+1,y[n]] == 100):
                a[x[n]+1, y[n]] = i
            if(a[x[n],y[n]-1] == 100):
                a[x[n],y[n]-1] = i
            if(a[x[n],y[n]+1] == 100):
                a[x[n],y[n]+1] = i
                
           
            
        elif x[n]>0 and y[n]==0 and x[n]<5:
            if (a[x[n]-1,y[n]]==100):
                a[x[n]-1,y[n]] = i
            if(a[x[n]+1,y[n]] == 100):
                a[x[n]+1, y[n]] = i
            if(a[x[n],y[n]+1] == 100):
                a[x[n],y[n]+1] = i
                
            
                

        elif x[n]==0 and y[n]>0 and y[n]<4:
            if(a[x[n],y[n]-1] == 100):
                a[x[n],y[n]-1] = i
            if(a[x[n],y[n]+1] == 100):
                a[x[n],y[n]+1] = i
            if(a[x[n]+1,y[n]] == 100):
                a[x[n]+1, y[n]] = i

            
            
                    
        elif y[n]>0 and x[n]==5 and y[n]<4:
            if(a[x[n],y[n]-1] == 100):
                a[x[n],y[n]-1] = i
            if(a[x[n],y[n]+1] == 100):
                a[x[n],y[n]+1] = i
            if (a[x[n]-1,y[n]]==100):
                a[x[n]-1,y[n]] = i          
            
            
                
        elif x[n]>0 and x[n]<5 and y[n]==4:
            if (a[x[n]-1,y[n]]==100):
                a[x[n]-1,y[n]] = i
            if(a[x[n]+1,y[n]] == 100):
                a[x[n]+1, y[n]] = i
            if(a[x[n],y[n]-1] == 100):
                a[x[n],y[n]-1] = i

           

        elif x[n]==0 and y[n]==0:
            if(a[x[n]+1,y[n]] == 100):
                a[x[n]+1, y[n]] = i
            if(a[x[n],y[n]+1] == 100):
                a[x[n],y[n]+1] = i
            
           

        elif x[n]==5 and y[n]==4:
            if (a[x[n]-1,y[n]]==100):
                a[x[n]-1,y[n]] = i
            if(a[x[n],y[n]-1] == 100):
                a[x[n],y[n]-1] = i

       
    for b in range(0,len(a)):
        for c in range(0,len(a[0])):
            if a[b,c] == 100:
                fill(a)



arr = np.full([6,5],100, np.uint8)
arr[0,0] = 0
arr[3,3] = 255
arr[3,2] = 255
arr[1,4] = 255
fill(arr)
print arr

