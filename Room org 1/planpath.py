import numpy as np
import cv2
fi = 0
obj_lim = 10
x = np.zeros([100], np.uint8)
y = np.zeros([100], np.uint8)
ux = np.zeros([obj_lim], np.uint32)
vx = np.zeros([obj_lim], np.uint32)
uy = np.zeros([obj_lim], np.uint32)
vy = np.zeros([obj_lim], np.uint32)
cx = np.zeros([obj_lim], np.uint32)
cy = np.zeros([obj_lim], np.uint32)
drawing = False
##global iy
ab = 0
ir = 0
def draw_rect(event,x,y,flags,param):
    global drawing, ix, iy, jx, jy, ir
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        #go = False
        #print go
        ix, iy = x, y
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            cv2.rectangle(frame, (ix, iy), (x,y), (255,255,255), -1)
            
            
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.rectangle(frame, (ix, iy), (x,y), (255,255,255), -1)
        jx, jy = x, y
        ux[ir], uy[ir], vx[ir], vy[ir] = ix, iy, jx, jy
        cx[ir] = ux[ir] + (vx[ir]- ux[ir])/2
        cy[ir] = uy[ir] + (vy[ir]- uy[ir])/2
        print '(', ux[ir],',',  uy[ir], ') {',  vx[ir],',',  vy[ir],')'
##        print cx[i], cy[i]
        ir+=1

co = 0
def fill(a):
    global fi, ab
    fi+=1
    ab =0
    for bf in range(0,len(a)):
        for cf in range(0,len(a[0])):
            if a[bf,cf] == fi-1:
                x[ab],y[ab] = bf, cf
                ab+=1
            
                
    for n in range(0,ab):
        
        if x[n]>0 and y[n]>0 and x[n]<(len(a)-1) and y[n]<(len(a[0])-1):
            if (a[x[n]-1,y[n]]==100):
                a[x[n]-1,y[n]] = fi
            if(a[x[n]+1,y[n]] == 100):
                a[x[n]+1, y[n]] = fi
            if(a[x[n],y[n]-1] == 100):
                a[x[n],y[n]-1] = fi
            if(a[x[n],y[n]+1] == 100):
                a[x[n],y[n]+1] = fi
                
           
            
        elif x[n]>0 and y[n]==0 and x[n]<(len(a)-1):
            if (a[x[n]-1,y[n]]==100):
                a[x[n]-1,y[n]] = fi
            if(a[x[n]+1,y[n]] == 100):
                a[x[n]+1, y[n]] = fi
            if(a[x[n],y[n]+1] == 100):
                a[x[n],y[n]+1] = fi
                
            
                

        elif x[n]==0 and y[n]>0 and y[n]<(len(a[0])-1):
            if(a[x[n],y[n]-1] == 100):
                a[x[n],y[n]-1] = fi
            if(a[x[n],y[n]+1] == 100):
                a[x[n],y[n]+1] = fi
            if(a[x[n]+1,y[n]] == 100):
                a[x[n]+1, y[n]] = fi

            
            
                    
        elif y[n]>0 and x[n]==(len(a)-1) and y[n]<(len(a[0])-1):
            if(a[x[n],y[n]-1] == 100):
                a[x[n],y[n]-1] = fi
            if(a[x[n],y[n]+1] == 100):
                a[x[n],y[n]+1] = fi
            if (a[x[n]-1,y[n]]==100):
                a[x[n]-1,y[n]] = fi          
            
            
                
        elif x[n]>0 and x[n]<(len(a)-1) and y[n]==(len(a[0])-1):
            if (a[x[n]-1,y[n]]==100):
                a[x[n]-1,y[n]] = fi
            if(a[x[n]+1,y[n]] == 100):
                a[x[n]+1, y[n]] = fi
            if(a[x[n],y[n]-1] == 100):
                a[x[n],y[n]-1] = fi

           

        elif x[n]==0 and y[n]==0:
            if(a[x[n]+1,y[n]] == 100):
                a[x[n]+1, y[n]] = fi
            if(a[x[n],y[n]+1] == 100):
                a[x[n],y[n]+1] = fi
            
           

        elif x[n]==(len(a)-1) and y[n]==(len(a[0])-1):
            if (a[x[n]-1,y[n]]==100):
                a[x[n]-1,y[n]] = fi
            if(a[x[n],y[n]-1] == 100):
                a[x[n],y[n]-1] = fi

      
    for fb in range(0,len(a)):
        for fc in range(0,len(a[0])):
            if a[fb,fc] == 100 and fi<50:
                fill(a)
    if fi>50:
        print fi
ipl = 0
def plan_path(a, x, y):
    global ptp, ipl
    ptp = np.zeros([a[x,y]+1, 2], np.uint8)
    ptp[0] = y, x
    while a[x,y]!=0:
        ipl+=1
        if x>0 and y>0 and x<(len(a)-1) and y<(len(a[0])-1):
            if (a[x-1,y]<a[x,y]):
                ptp[ipl] = y, x-1
                x, y = x-1, y
            elif(a[x+1,y] <a[x,y]):
                ptp[ipl] = y,x+1
                x, y = x+1, y
            elif(a[x,y-1] <a[x,y]):
                ptp[ipl] = y-1, x
                x, y = x, y-1
            elif(a[x,y+1] <a[x,y]):
                ptp[ipl] = y+1, x
                x, y = x, y+1
                
           
            
        elif x>0 and y==0 and x<(len(a)-1):
            if (a[x-1,y]<a[x,y]):
                ptp[ipl] = y, x-1
                x, y = x-1, y
            elif(a[x+1,y] <a[x,y]):
                ptp[ipl] = y,x+1
                x, y = x+1, y
            elif(a[x,y+1] <a[x,y]):
                ptp[ipl] = y+1,x
                x, y = x, y+1
                
            
                

        elif x==0 and y>0 and y<(len(a[0])-1):
            if(a[x,y-1] <a[x,y]):
                ptp[ipl] = y-1,x
                x, y = x, y-1
            elif(a[x,y+1] <a[x,y]):
                ptp[ipl] = y+1,x
                x, y = x, y+1
            elif(a[x+1,y] <a[x,y]):
                ptp[ipl] = y,x+1
                x, y = x+1, y

            
            
                    
        elif y>0 and x==(len(a)-1) and y<(len(a[0])-1):
            if(a[x,y-1] <a[x,y]):
                ptp[ipl] = y-1,x
                x, y = x, y-1
            elif(a[x,y+1] <a[x,y]):
                ptp[ipl] = y+1,x
                x, y = x, y+1
            elif (a[x-1,y]<a[x,y]):
                ptp[ipl] = y,x-1
                x, y = x-1, y
            
            
                
        elif x>0 and x<(len(a)-1) and y==(len(a[0])-1):
            if (a[x-1,y]<a[x,y]):
                ptp[ipl] = y,x-1
                x, y = x-1, y
            elif(a[x+1,y] <a[x,y]):
                ptp[ipl] = y,x+1
                x, y = x+1, y
            if(a[x,y-1] <a[x,y]):
                ptp[ipl] = y-1,x
                x, y = x, y-1

           

        elif x==0 and y==0:
            if(a[x+1,y] <a[x,y]):
                ptp[ipl] = y,x+1
                x, y = x+1, y
            elif(a[x,y+1] <a[x,y]):
                ptp[ipl] = y+1,x
                x, y = x, y+1
            
           

        elif x==(len(a)-1) and y==(len(a[0])-1):
            if (a[x-1,y]<a[x,y]):
                ptp[ipl] = y,x-1
                x, y = x-1, y
            elif(a[x,y-1] <a[x,y]):
                ptp[ipl] = y-1,x
                x, y = x, y-1

    return ptp
        


frame = np.zeros(([640,480,3]), np.uint8)
cv2.namedWindow('frame')
cv2.setMouseCallback('frame', draw_rect)
while True:
    cv2.imshow('frame', frame)
    k = cv2.waitKey(1) & 0xFF  
    if k == 27:
        break





##img = np.zeros(([640,480,3]), np.uint8)      

w = (vx[0] - ux[0])
h = (vy[0] - uy[0])
ag = 0
bg = h
i1 = 0
global arx, ary
arx = 480/w +1
ary = 640/h +1
arr = np.full([ary,arx], 100, np.uint8)
c1 = 0
c2 = 0

for xg in range(0, 480, w):
    ag=xg+w
    c1+=1
    for yg in range(0, 640, h):
        cv2.rectangle(frame, (xg,yg), (ag,bg), (0,255,255), 1)
        bg+=h
        c2+=1
print 'w: ', w
print 'h: ', h
for xg in range(1,ir-1):
    arr[uy[xg]/h : vy[xg]/h+1, ux[xg]/w : vx[xg]/w+1] = 255
arr[cy[ir-1]/h, cx[ir-1]/w] = 0

##print cy[0]/h, cx[0]/w

print 'arx : ', arx
print 'ary : ', ary
print 'c1: ', c1
print 'c2: ', c2/c1
i=0
print arr
fill(arr)
print cy[0]/h, cx[0]/w
ptp = plan_path(arr, cy[0]/h, cx[0]/w)
print ptp
ptps = np.zeros([len(ptp), 2], np.uint32)
for d in range(0, len(ptp)):
    ptps[d] = ((ptp[d,0]*w)+ w/2 , (ptp[d,1]*h)+ h/2)
ptps = np.int0(ptps)
cv2.polylines(frame, [ptps], False, 255, 2)
print arr
##print i




cv2.imshow('img', frame)
while True:
    if cv2.waitKey(1)==27:
        break
    
cv2.destroyAllWindows()

