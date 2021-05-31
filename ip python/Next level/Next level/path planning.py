import numpy as np
import cv2
##def draw_grid(img,x,y,w,h):
##    a = 0
##    b = 0
##    for i in range(0, 480+w, w):
##        for j in range(0, 640+h, h):
##            cv2.rectangle(img, (i,j), (a+w,b+h), (255,255,255), 1)
##            a, b = i, j
            
        
    
    
    

img = np.zeros(([640,480,3]))
arr = np.ones([6,5], np.uint8)
##print arr
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
    print i
    for j in range(0, 640+h, h):
        cv2.rectangle(img, (i,j), (a,b), (255,255,255), -1)
        cv2.rectangle(img, (i,j), (a,b), (0,255,255), 1)
        
        b+=h
        if(cx[0]>i and cx[0]<i+w and cy[0]>j and cy[0]<j+h):
                
            arr[j/h,i/w] = "f"
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

for n in range(0,3):
    cv2.rectangle(img, (ux[n], uy[n]), (vx[n], vy[n]), (255,255,0), 1)
    cx[n] = ux[n] + (vx[n]-ux[n])/2
    cy[n] = uy[n] + (vy[n]-uy[n])/2
    img[cy[n]-5:cy [n]+5, cx[n]-5:cx[n]+5] = 155

print arr

        
        
##        for n1 in range(i, a):
##            for n2 in range(j, b):
##               if(ux[0], uy[0] == n1,n2):
##                   cv2.rectangle(img, (i,j), (a,b), (0,0,0), -1)
##                for nx in range(0,3):
##                    i1+=1
##                    print i1
##                    if(ux[nx], uy[nx] == n1,n2):
##                        cv2.rectangle(img, (i,j), (a,b), (0,0,0), -1)
##                    elif(vx[nx], vy[x] == n1,n2):
##                        cv2.rectangle(img, (i,j), (a,b), (0,0,0), -1)
##                    else:
##                        pass
                
                

##draw_grid(img, ux[2], uy[2], vx[2]-ux[2], vy[2]-uy[2])
##img = cv2.polylines(img,[pts],False,(0,255,255))
a = np.zeros([640,2], np.uint32)
m = 0

##for i in range(y1, iy1):
##    for j in range(x1,ix1):  
##        if( i-cy0 == (j-cx0)*(cy0-cy2)/(cx0-cx2)):
##            a[m] = j, i
##            print a[m]
##            m+=1
##         
##        
##        
##print 'over'
##print a[0]
##print a[m-1]
##l,s = a[0]
##c, 8j = a[m-1]
##img[s-5:s+5, l-5:l+5] = [150]
##img[j-5:j+5, c-5:c+5] = [150]

cv2.imshow('img', img)
while True:
    if cv2.waitKey(1)==ord('q'):
        break
    
cv2.destroyAllWindows()

##img1 = np.zeros([480, 640], np.uint8)
##img1[]
