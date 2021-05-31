import numpy as np
import cv2
i = 0
x = np.zeros([100], np.uint8)
y = np.zeros([100], np.uint8)

##global iy
ab = 0
def fill(a):
    global i, ab
    i+=1
    ab = 0
    for b in range(0,len(a)):
        for c in range(0,len(a[0])):
            if a[b,c] == i-1:
                x[ab],y[ab] = b,c
                ab+=1
            
                
    for n in range(0,ab):
        
        if x[n]>0 and y[n]>0 and x[n]<(len(a)-1) and y[n]<(len(a[0])-1):
            if (a[x[n]-1,y[n]]==100):
                a[x[n]-1,y[n]] = i
            if(a[x[n]+1,y[n]] == 100):
                a[x[n]+1, y[n]] = i
            if(a[x[n],y[n]-1] == 100):
                a[x[n],y[n]-1] = i
            if(a[x[n],y[n]+1] == 100):
                a[x[n],y[n]+1] = i
                
           
            
        elif x[n]>0 and y[n]==0 and x[n]<(len(a)-1):
            if (a[x[n]-1,y[n]]==100):
                a[x[n]-1,y[n]] = i
            if(a[x[n]+1,y[n]] == 100):
                a[x[n]+1, y[n]] = i
            if(a[x[n],y[n]+1] == 100):
                a[x[n],y[n]+1] = i
                
            
                

        elif x[n]==0 and y[n]>0 and y[n]<(len(a[0])-1):
            if(a[x[n],y[n]-1] == 100):
                a[x[n],y[n]-1] = i
            if(a[x[n],y[n]+1] == 100):
                a[x[n],y[n]+1] = i
            if(a[x[n]+1,y[n]] == 100):
                a[x[n]+1, y[n]] = i

            
            
                    
        elif y[n]>0 and x[n]==(len(a)-1) and y[n]<(len(a[0])-1):
            if(a[x[n],y[n]-1] == 100):
                a[x[n],y[n]-1] = i
            if(a[x[n],y[n]+1] == 100):
                a[x[n],y[n]+1] = i
            if (a[x[n]-1,y[n]]==100):
                a[x[n]-1,y[n]] = i          
            
            
                
        elif x[n]>0 and x[n]<(len(a)-1) and y[n]==(len(a[0])-1):
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
            
           

        elif x[n]==(len(a)-1) and y[n]==(len(a[0])-1):
            if (a[x[n]-1,y[n]]==100):
                a[x[n]-1,y[n]] = i
            if(a[x[n],y[n]-1] == 100):
                a[x[n],y[n]-1] = i

       
    for b in range(0,len(a)):
        for c in range(0,len(a[0])):
            if a[b,c] == 100:
                fill(a)


        
img = np.zeros(([640,480,3]), np.uint8)
arr = np.full([6,5],100, np.uint8)
ux = np.array((37, 180, 307))
uy = np.array((17,190,450,))
vx = np.array((145, 270, 417))
vy = np.array((130,280,560))
cx = np.zeros([3], np.uint32)
cy = np.zeros([3], np.uint32)

##pt1 = np.array((( 37 , 17 ),( 205 , 219 ),( 307 , 450 )))
##pt2 = np.array(((145 , 130), (317 , 382), (426 , 605 )))


w = vx[2]-ux[2] 
h = vy[2]-uy[2]
a = 0
b = h
i1 = 0

for n in range(0,3):
    cv2.rectangle(img, (ux[n], uy[n]), (vx[n], vy[n]), (255,255,0), 1)
    cx[n] = ux[n] + (vx[n]-ux[n])/2
    cy[n] = uy[n] + (vy[n]-uy[n])/2
    img[cy[n]-5:cy [n]+5, cx[n]-5:cx[n]+5] = 155
for i in range(0, 480+w, w):
    a=i+w
    for j in range(0, 640+h, h):
        cv2.rectangle(img, (i,j), (a,b), (255,255,255), -1)
        cv2.rectangle(img, (i,j), (a,b), (0,255,255), 1)
        
        b+=h
            
        for nx in range(1,2):
            if(ux[nx]>i and ux[nx]<i+w and uy[nx]>j and uy[nx]<j+h):
                cv2.rectangle(img, (i,j), (a,b), (0,0,0), -1)
                arr[j/h,i/w] = 255
            
            if(vx[nx]>i and vx[nx]<i+w and vy[nx]>j and vy[nx]<j+h):
                cv2.rectangle(img, (i,j), (a,b), (0,0,0), -1)
                arr[j/h,i/w] = 255

            if(ux[nx]+w>i and ux[nx]+w<i+w and uy[nx]>j and uy[nx]<j+h):
                cv2.rectangle(img, (i,j), (a,b), (0,0,0), -1)
                arr[j/h,i/w] = 255

            if(vx[nx]-w>i and vx[nx]-w<i+w and vy[nx]>j and vy[nx]<j+h):
                cv2.rectangle(img, (i,j), (a,b), (0,0,0), -1)
                arr[j/h,i/w] = 255

        if(cx[0]>i and cx[0]<i+w and cy[0]>j and cy[0]<j+h):
            arr[j/h,i/w] = 0
            
            
        
            
                
            

for n in range(0,3):
    cv2.rectangle(img, (ux[n], uy[n]), (vx[n], vy[n]), (255,255,0), 1)
    cx[n] = ux[n] + (vx[n]-ux[n])/2
    cy[n] = uy[n] + (vy[n]-uy[n])/2
    img[cy[n]-5:cy [n]+5, cx[n]-5:cx[n]+5] = 155
i=0
fill(arr)
print arr




cv2.imshow('img', img)
while True:
    if cv2.waitKey(1)==ord('q'):
        break
    
cv2.destroyAllWindows()

