import PIL
import sys
from PIL import Image
from random import randint
from time import time
from math import sin
from math import cos
from math import radians
import numpy as np

# draws a line using the basic line drawing algorithm
# the code to create a window and draw a single pixel can be found https://rosettacode.org/wiki/Draw_a_pixel#Python 
def bresenham_alg(x0, y0, x1, y1, pixels):      
     
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

            if y1 > y0:
                 
                while x <= x1 and y <= y1:
                    pixels[x, y] = (255,255,255)
                    if e < 0:
                        e += inc1
                    else:
                        y += 1
                        e += inc2
                    x += 1  
            
            else:
                
                while x <= x1 and y >= y1:
                    pixels[x, y] = (255,255,255)
                    if e < 0:
                        e += inc1
                    else:
                        y -= 1
                        e += inc2
                    x += 1                               
       
        else:
             
            if y1 > y0: 
                
                while x >= x1 and y <= y1:
                    pixels[x, y] = (255,255,255)
                    if e < 0:
                        e += inc1
                    else:
                        y += 1
                        e += inc2
                    x -= 1 
                     
            else:
                
                while x >= x1 and y >= y1:
                    pixels[x, y] = (255,255,255)
                    if e < 0:
                        e += inc1
                    else:
                        y -= 1
                        e += inc2
                    x -= 1          
        
        return               
             
def translate(tx, ty):
    
    # transformation matrix 
    t = np.array(
        [[1, 0, 0],
         [0, 1, 0],
         [tx, ty, 1]])
    
    return apply_transformation(t, datalines, newpoints)
        
def scale(sx, sy, cx, cy):
    
    # transformation matrices 
    t1 = np.array(
        [[1, 0, 0],
         [0, 1, 0],
         [-cx, -cy, 1]])
    bs = np.array(
        [[sx, 0, 0],
         [0, sy, 0],
         [0, 0, 1]])
    t2 = np.array(
        [[1, 0, 0],
         [0, 1, 0],
         [cx, cy, 1]])
    
    m = t1 @ bs
    t = m @ t2 # overall transformation matrix
    
    return apply_transformation(t, datalines, newpoints)

def rotate(angle, cx, cy):
    
    # transformation matrices 
    t1 = np.array(
        [[1, 0, 0],
         [0, 1, 0],
         [-cx, -cy, 1]])
    br = np.array(
        [[cos(radians(angle)), -sin(radians(angle)), 0],
         [sin(radians(angle)), cos(radians(angle)), 0],
         [0, 0, 1]]) 
    t2 = np.array(
        [[1, 0, 0],
         [0, 1, 0],
         [cx, cy, 1]])
    
    m = t1 @ br
    t = m @ t2 # overall transformation matrix
     
    return apply_transformation(t, datalines, newpoints)

def basic_scale(sx, sy):
    
    # transformation matrix 
    t = np.array(
        [[sx, 0, 0],
         [0, sy, 0],
         [0, 0, 1]])

    return apply_transformation(t, datalines, newpoints)
    
def basic_rotate(angle):
    
    # transformation matrix 
    t = np.array(
        [[cos(radians(angle)), -sin(radians(angle)), 0],
         [sin(radians(angle)), cos(radians(angle)), 0],
         [0, 0, 1]]) 
     
    return apply_transformation(t, datalines, newpoints)

def apply_transformation(t, input, output):
    
    # transform the points 
    for line in input:
        
        m = np.array([line[0], line[1], 1])
        prod0 = m @ t # matrix multiplication
        x0 = prod0[0] 
        y0 = prod0[1]
         
        n = np.array([line[2], line[3], 1])
        prod1 = n @ t # matrix multiplication 
        x1 = prod1[0]
        y1 = prod1[1] 
        
        output.append([x0, y0, x1, y1])
    
    # check to see if resulting trasformation is completley visible  
    for line in output: 
        x0 = line[0]
        y0 = line[1]
        x1 = line[2]
        y1 = line[3]
        
        # if a point is out of range, immediately return false 
        if x0 < 0 or x0 > 959 or y0 < 0 or y0 > 599 or x1 < 0 or x1 > 959 or y1 < 0 or y1 > 599:
            return False
    
    # no points were out of range, so return true 
    return True
 
def prompt_user():
   print("\nCommand Options")
   print(" - Translate: t")
   print(" - Scale: s")
   print(" - Rotate: r")
   print(" - Basic Scale: bs")
   print(" - Basic Rotate: br")
   print(" - Quit: q\n") 

def display_pixels():                                                          
    # the window is 960 x 600
    # x bounds [0, 959]
    # y bounds [0, 599] 
    img = Image.new('RGB', (960, 600)) 
    pixels = img.load() 
    
    # scan-convert each line
    for points in newpoints:   
        x0 = int(points[0])
        y0 = int(points[1])
        x1 = int(points[2])
        y1 = int(points[3])
        # print("Coordinate Values:")
        # print("(" + str(x0) + ", " + str(y0) + ")")
        # print("(" + str(x1) + ", " + str(y1) + ")\n")
        bresenham_alg(x0, y0, x1, y1, pixels)

    img = img.transpose(Image.Transpose.FLIP_TOP_BOTTOM)   
    img.show()

def output_file():
    file = open("output.txt", "w")
    for i in newpoints:
        for j in i:
            file.write("%f " % j)
        file.write("\n") 
    file.close()

# main program begins
print("  ____  ____                                                                      ")                                                                  
print(" |___ \|  _ \                                                                     ")                                                              
print("   __) | | | |                                                                    ")                                                           
print("  / __/| |_| |                                                                    ")                                                            
print(" |_____|____/                     _        _                                      ")                      
print("  / ___| ___  ___  _ __ ___   ___| |_ _ __(_) ___                                 ")                    
print(" | |  _ / _ \/ _ \| '_ ` _ \ / _ \ __| '__| |/ __|                                ")                 
print(" | |_| |  __/ (_) | | | | | |  __/ |_| |  | | (__                                 ")              
print("  \____|\___|\___/|_| |_| |_|\___|\__|_|  |_|\___|        _   _                   ")             
print(" |_   _| __ __ _ _ __  ___ / _| ___  _ __ _ __ ___   __ _| |_(_) ___  _ __  ___   ") 
print("   | || '__/ _` | '_ \/ __| |_ / _ \| '__| '_ ` _ \ / _` | __| |/ _ \| '_ \/ __|  ")
print("   | || | | (_| | | | \__ \  _| (_) | |  | | | | | | (_| | |_| | (_) | | | \__ \  ")
print("   |_||_|  \__,_|_| |_|___/_|  \___/|_|  |_| |_| |_|\__,_|\__|_|\___/|_| |_|___/  ")

loop = True
datalines = [] # holds the endpoints of each line in the input file
newpoints = [] # the new, transformed points
name = input("\nPlease provide the name of the file containing the data points: ").strip()

# open and read the file
try: 
    with open(name) as f:
        # read lines from txt file 
        for line in f.readlines():
            # append each line to the list
            datalines.append(line.strip().split(" "))
        f.close() 
        print("\nFile opened successfully!")    
except OSError as e:
    print("OS ERROR:", e.strerror)
    print("Exiting program...")
    sys.exit(1)
except:
    print("UNEXPECTED ERROR:", sys.exc_info()[0])
    print("Exiting program...")
    sys.exit(1)

# change all elements in datalines to floats
rows = len(datalines)
cols = len(datalines[0])
for i in range(rows):
    for j in range(cols):
        datalines[i][j] = float(datalines[i][j])   

# main program loop
while (loop):
    
    prompt_user()
    inp = input("Choose a command: ")
    print()
    
    if inp == "q":
        
        print("Quitting the program..\nBye!\n")
        loop = False
         
    elif inp == "t":
        
        tx = float(input("Translation in the x direction: "))
        ty = float(input("Translation in the y direction: "))  
        result = translate(tx, ty) # translate
        
        # check if transformed img is in the bounds of the screen 
        if result == False:
           print("\nTranslated image is out of range. Please try again with different values.")
           newpoints.clear() # reset
           continue 
        else: 
            output_file() # output results to txt file
            display_pixels() # scan-convert
            newpoints.clear() # reset
            
    elif inp == "s":
        
        sx = float(input("Horizontal scaling factor: "))
        sy = float(input("Vertical scaling factor: ")) 
        cx = float(input("Center of scale (x): "))
        cy = float(input("Center of scale (y): "))
        result = scale(sx, sy, cx, cy) # scale
        
        if result == False:
            print("\nScaled image is out of range. Please try again with different values.")
            newpoints.clear() # reset
            continue
        else:
            output_file() # output results to txt file
            display_pixels() # scan-convert
            newpoints.clear() # reset
        
    elif inp == "r":
        
        angle = float(input("Rotation angle (clockwise): ")) 
        cx = float(input("Center of rotation (x): "))
        cy = float(input("Center of rotation (y): "))
        result = rotate(angle, cx, cy) # rotate 
        
        # checks if transformed img is in the bounds of the screen
        if result == False: 
            print("\nRotated image is out of range. Please try again with different values.")
            newpoints.clear() # reset
            continue
        else:
            output_file() # output results to txt file
            display_pixels() # scan-convert
            newpoints.clear() # reset   
        
    elif inp == "bs":
        
        sx = float(input("Horizontal scaling factor: "))
        sy = float(input("Vertical scaling factor: "))  
        result = basic_scale(sx, sy) # scale 
        
        # checks if transformed img is in the bounds of the screen
        if result == False: 
            print("\nScaled image is out of range. Please try again with different values.")
            newpoints.clear() # reset
            continue
        else:
            output_file() # output results to txt file
            display_pixels() # scan-convert
            newpoints.clear() # reset
            
    elif inp == "br":
        
        angle = float(input("Rotation angle (clockwise): ")) 
        result = basic_rotate(angle) # rotate 
        
        # checks if transformed img is in the bounds of the screen
        if result == False: 
            print("\nRotated image is out of range. Please try again with a different value.")
            newpoints.clear() # reset
            continue
        else:
            output_file() # output results to txt file
            display_pixels() # scan-convert
            newpoints.clear() # reset
        
    else:
        print("ERROR: Command not recognized")
        