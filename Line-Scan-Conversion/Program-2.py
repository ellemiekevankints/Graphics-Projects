import PIL
from PIL import Image
from random import randint
from time import time

# draws a line using the basic line drawing algorithm
# the code to create a window and draw a single pixel can be found https://rosettacode.org/wiki/Draw_a_pixel#Python 
def bresenham_alg(x0, y0, x1, y1):      
     
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    x, y = x0, y0 
     
    if x0 == x1 and y0 == y1: # singular point     
        
        pixels[x0,y0] = (255,255,255)
        return
     
    elif x0 == x1: # vertical   
        
        if y1 > y0:
            while y <= y1:
                pixels[x0,y] = (255,255,255)
                y += 1
        else:
            while y >= y1:
                pixels[x0,y] = (255,255,255)
                y -= 1          
        return 
      
    elif y0 == y1: # horizontal  
        
        if x1 > x0:
            while x <= x1:
                pixels[x,y0] = (255,255,255)
                x += 1
        else:
            while x >= x1:
                pixels[x,y0] = (255,255,255)
                x -= 1
        return 
     
    if dx > dy:
       
        e = 2 * dy - dx 
        inc1 = 2 * dy
        inc2 = 2 * (dy - dx) 
         
        if x1 > x0:
             
            if y1 > y0:
                 
                # critical loop 
                while x <= x1:
                    pixels[x, y] = (255,255,255)
                    if e < 0:
                        e += inc1
                    else:
                        y += 1
                        e += inc2
                    x += 1  
                return     
                    
            elif y0 > y1:

                # critical loop 
                while x <= x1:
                    pixels[x, y] = (255,255,255)
                    if e < 0:
                        e += inc1
                    else:
                        y -= 1
                        e += inc2
                    x += 1        
                return
                
        elif x0 > x1:
            
            if y1 > y0:

                # critical loop  
                while x >= x1:
                    pixels[x, y] = (255,255,255)
                    if e < 0:
                        e += inc1
                    else:
                        y += 1
                        e += inc2
                    x -= 1   
                return
            
            elif y0 > y1:

                # critical loop  
                while x >= x1:
                    pixels[x, y] = (255,255,255)
                    if e < 0:
                        e += inc1
                    else:
                        y -= 1
                        e += inc2
                    x -= 1   
                return 
             
    elif dy > dx:
        
        e = 2 * dx - dy 
        inc1 = 2 * dx
        inc2 = 2 * (dx - dy) 
        
        if x1 > x0:
            
            if y1 > y0: 
                
                # critical loop 
                while y <= y1:
                    pixels[x, y] = (255,255,255)
                    if e < 0:
                        e += inc1
                    else:
                        x += 1
                        e += inc2
                    y += 1       
                return 
            
            elif y0 > y1: 

                # critical loop 
                while y >= y1:
                    pixels[x, y] = (255,255,255)
                    if e < 0:
                        e += inc1
                    else:
                        x += 1
                        e += inc2
                    y -= 1       
                return      
             
        elif x0 > x1:
            
            if y1 > y0:

                # critical loop  
                while y <= y1:
                    pixels[x, y] = (255,255,255)
                    if e < 0:
                        e += inc1
                    else:
                        x -= 1
                        e += inc2
                    y += 1   
                return
            
            elif y0 > y1:

                # critical loop  
                while y >= y1:
                    pixels[x, y] = (255,255,255)
                    if e < 0:
                        e += inc1
                    else:
                        x -= 1
                        e += inc2
                    y -= 1   
                return
                  
    else: # perfectly diagonal, i.e. dx == dy
        
        e = 2 * dy - dx 
        inc1 = 2 * dy
        inc2 = 2 * (dy - dx)
        
        if x1 > x0:

            while x <= x1:
                pixels[x, y] = (255,255,255)
                if e < 0:
                    e += inc1
                else:
                    y += 1
                    e += inc2
                x += 1       
            return
             
        else:
            
            while x >= x1:
                pixels[x, y] = (255,255,255)
                if e < 0:
                    e += inc1
                else:
                    y -= 1
                    e += inc2
                x -= 1 
            return               
             
# generates a random x coordinate everytime it executes 
def xcoordinate():
   return randint(0, 959)

# generates a random y coordinate everytime it executes 
def ycoordinate():
    return randint(0, 599)

# the window is 960 x 600
# x bounds [0, 959]
# y bounds [0, 599] 
img = Image.new('RGB', (960, 600)) 
pixels = img.load() 

# all input is read as positive integer values
n = abs(int(input("Please enter how many lines you would like to draw: ")))

t = 0
# loops from 0 to n (exclusive)
for i in range(n): 
    x0 = xcoordinate()
    y0 = ycoordinate() 
    x1 = xcoordinate()
    y1 = ycoordinate()
    # print("Coordinate Values:")
    # print("(" + str(x0) + ", " + str(y0) + ")")
    # print("(" + str(x1) + ", " + str(y1) + ")\n")
    
    start = time()
    bresenham_alg(x0, y0, x1, y1)
    end = time()
    t = t + (end - start) # calculate execution time 

print("Execution time:", t, "seconds")
img = img.transpose(Image.Transpose.FLIP_TOP_BOTTOM)   
img.show()