import PIL
from PIL import Image
from random import randint

# draws a line using the basic line drawing algorithm
# the code to create a window and draw a single pixel can be found https://rosettacode.org/wiki/Draw_a_pixel#Python 
def basic_alg(x0, y0, x1, y1): 
    
    dy = abs(y1 - y0)               
    dx = abs(x1 - x0)               
    m = (y1 - y0)/(x1 - x0) # slope 
    b = y0 - (m * x0)       # y-intercept 
    
    if x0 == x1: # vertical  
        print()
    elif y0 == y1: # horizontal 
        print()
    elif dx == dy: # perfectly diagonal 
        print()
    else:
       
       if dx > dy and x1 > x0: 
           # (0, 0) to (8, 4)
           # (0, 1) to (4, 0)
           
           for i in range(dx):
               x = x0 + i
               y = (m * i) + b
               y = int(y)
               pixels[x,y] = (255,255,255)   
                
       elif dx > dy and x0 > x1:
           # (4, 0) to (0, 1)
           # (4, 2) to (0, 0)
           
           for i in range(dx):
               x = x1 + i
               y = (m * i) + b
               y = int(y)
               pixels[x,y] = (255,255,255)  
            
       elif dy > dx and y1 > y0:
           # (0, 0) to (3, 8) 
           # (3, 0) to (0, 8)
           
           for i in range(dy):
               y = y0 + i
               x = (y - b)/m 
               x = int(x)
               pixels[x,y] = (255,255,255)
        
       elif dy > dx and y0 > y1: 
           # (0, 8) to (6, 0)
           # (6, 8) to (0, 0) 
           
           for i in range(dy):
               y = y1 + i
               x = (y - b)/m 
               x = int(x)
               pixels[x,y] = (255,255,255)
             
# generates a random x coordinate everytime it executes 
def xcoordinate():
   return randint(0, 959)

# generates a random y coordinate everytime it executes 
def ycoordinate():
    return randint(0, 599)

# the window is 960 x 600
# x bounds [0, 959]
# y bounds [0, 599] 
img = Image.new('RGB', (100, 100)) 
pixels = img.load() 

# only accepts positive integer values as input
n = abs(int(input("Please enter how many lines you would like to draw: ")))

# loops from 0 to n (exclusive)
for i in range(n): 
    #x0 = xcoordinate()
    #y0 = ycoordinate() 
    #x1 = xcoordinate()
    #y1 = ycoordinate()
    #print("\nCoordinate Values:")
    #print("(" + x0 + ", " + y0 + ")")
    #print("(" + x1 + ", " + y1 + ")\n")
    x0 = 6
    y0 = 8
    x1 = 0
    y1 = 0
    basic_alg(x0, y0, x1, y1)

img = img.transpose(Image.Transpose.FLIP_TOP_BOTTOM)   
img.show()