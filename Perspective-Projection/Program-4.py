import PIL
import sys
import math
from PIL import Image
from random import randint
from time import time
from cv2 import sqrt, validateDisparity
import numpy as np

# GLOBAL VARIABLES

loop = True
datalines = [] # holds the endpoint coordinates (defined in WCS) of each line in the input file
eyecoords = [] # holds the endpoint coordinates (defined in ECS) of each line 
screencoords = [] # the 2D screen coordinates of each line
newpoints = [] # the new, transformed points

# FUNCTIONS

def bresenham_alg(x0, y0, x1, y1, pixels):      
    
    """ Draws a line using Bresenham's Scan-Conversion Algorithm.
        The code to create a window and draw a single pixel can be found here: https://rosettacode.org/wiki/Draw_a_pixel#Python  
    """
     
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
           
def translate(tx, ty, tz):
    
    # transformation matrix 
    t = np.array(
        [[1, 0, 0, 0],
         [0, 1, 0, 0],
         [0, 0, 1, 0],
         [tx, ty, tz, 1]])
    
    return apply_transformation(t, datalines)
       
def scale(sx, sy, sz, cx, cy, cz):
    
    # transformation matrices 
    t1 = np.array(
        [[1, 0, 0, 0],
         [0, 1, 0, 0],
         [0, 0, 1, 0],
         [-cx, -cy, -cz, 1]])
    bs = np.array(
        [[sx, 0, 0, 0],
         [0, sy, 0, 0],
         [0, 0, sz, 0],
         [0, 0, 0, 1]])
    t2 = np.array(
        [[1, 0, 0, 0],
         [0, 1, 0, 0],
         [0, 0, 1, 0],
         [cx, cy, cz, 1]])
    
    m = t1 @ bs
    t = m @ t2 # overall transformation matrix
    
    return apply_transformation(t, datalines)

def rotatex(angle, cx, cy, cz):
    
    # transformation matrices 
    t1 = np.array(
        [[1, 0, 0, 0],
         [0, 1, 0, 0],
         [0, 0, 1, 0],
         [-cx, -cy, -cz, 1]])
    br = np.array(
        [[1, 0, 0, 0],
         [0, math.cos(math.radians(angle)), math.sin(math.radians(angle)), 0],
         [0, -math.sin(math.radians(angle)), math.cos(math.radians(angle)), 0],
         [0, 0, 0, 1]]) 
    t2 = np.array(
        [[1, 0, 0, 0],
         [0, 1, 0, 0],
         [0, 0, 1, 0],
         [cx, cy, cz, 1]])
    
    m = t1 @ br
    t = m @ t2 # overall transformation matrix
     
    return apply_transformation(t, datalines)

    
    # transformation matrix 
    t = np.array(
        [[cos(radians(angle)), -sin(radians(angle)), 0],
         [sin(radians(angle)), cos(radians(angle)), 0],
         [0, 0, 1]]) 
     
    return apply_transformation(t, datalines, newpoints) 

def rotatey(angle, cx, cy, cz):
    
    # transformation matrices 
    t1 = np.array(
        [[1, 0, 0, 0],
         [0, 1, 0, 0],
         [0, 0, 1, 0],
         [-cx, -cy, -cz, 1]])
    br = np.array(
        [[math.cos(math.radians(angle)), 0, -math.sin(math.radians(angle)), 0],
         [0, 1, 0, 0],
         [math.sin(math.radians(angle)), 0, math.cos(math.radians(angle)), 0],
         [0, 0, 0, 1]]) 
    t2 = np.array(
        [[1, 0, 0, 0],
         [0, 1, 0, 0],
         [0, 0, 1, 0],
         [cx, cy, cz, 1]])
    
    m = t1 @ br
    t = m @ t2 # overall transformation matrix
     
    return apply_transformation(t, datalines)
    
def rotatez(angle, cx, cy, cz):
    
    # transformation matrices 
    t1 = np.array(
        [[1, 0, 0, 0],
         [0, 1, 0, 0],
         [0, 0, 1, 0],
         [-cx, -cy, -cz, 1]])
    br = np.array(
        [[math.cos(math.radians(angle)), math.sin(math.radians(angle)), 0, 0],
         [-math.sin(math.radians(angle)), math.cos(math.radians(angle)), 0, 0],
         [0, 0, 1, 0],
         [0, 0, 0, 1]]) 
    t2 = np.array(
        [[1, 0, 0, 0],
         [0, 1, 0, 0],
         [0, 0, 1, 0],
         [cx, cy, cz, 1]])
    
    m = t1 @ br
    t = m @ t2 # overall transformation matrix
    
    return apply_transformation(t, datalines) 

def apply_transformation(t, input):
    
    """ Apply transformation matrix t to the input points. """
     
    output = [] # the transformed endpoints
 
    # transform the points 
    for line in input:
        m = np.array([line[0], line[1], line[2], 1])
        prod0 = m @ t # matrix multiplication
        x0 = prod0[0] 
        y0 = prod0[1]
        z0 = prod0[2]
         
        n = np.array([line[3], line[4], line[5], 1])
        prod1 = n @ t # matrix multiplication 
        x1 = prod1[0]
        y1 = prod1[1]
        z1 = prod1[2] 
        
        output.append([x0, y0, z0, x1, y1, z1])
    
    return output

def map_points(x, y, z, points):
    
    """ Map points from World Coordinate System (WCS) to Eye Coordinate System (ECS). """
     
    # multiply each axis by -1
    T1 = np.array(
        [[1, 0, 0, 0],
         [0, 1, 0, 0],
         [0, 0, 1, 0],
         [-x, -y, -z, 1]])

    # rotation of x-axis by 90 degrees
    T2 = np.array(
        [[1, 0, 0, 0],
         [0, 0, -1, 0],
         [0, 1, 0, 0],
         [0, 0, 0, 1]])

    # rotation about the y-axis
    m = x / math.sqrt(x**2 + y**2)
    n = y / math.sqrt(x**2 + y**2)
    T3 = np.array(
        [[-n, 0, m, 0],
         [0, 1, 0, 0],
         [-m, 0, -n, 0],
         [0, 0, 0, 1]])

    # rotation about the x-axis
    p = z / math.sqrt(z**2 + math.sqrt(x**2 + y**2)**2)  
    q = math.sqrt(x**2 + y**2) / math.sqrt(z**2 + math.sqrt(x**2 + y**2)**2)
    T4 = np.array(
        [[1, 0, 0, 0],
         [0, q, p, 0],
         [0, -p, q, 0],
         [0, 0, 0, 1]])
     
    # last transformation
    T5 = np.array(
        [[1, 0, 0, 0],
         [0, 1, 0, 0],
         [0, 0, -1, 0],
         [0, 0, 0, 1]]) 
    
    V = T1 @ T2 @ T3 @ T4 @ T5 # viewing transformation matrix
    
    eyecoords = [] # holds the endpoints defined in ECS 
    for point in points:
         
        wcs0 = np.array([point[0], point[1], point[2], 1]) 
        wcs1 = np.array([point[3], point[4], point[5], 1])  
        
        # map points from ECS to WCS
        ecs0 = wcs0 @ V
        ecs1 = wcs1 @ V
        
        # clip last element  
        ecs0 = ecs0[:3] 
        ecs1 = ecs1[:3] 
          
        ecsline = ecs0.tolist() + ecs1.tolist() # store transformed endpoints in a list
        eyecoords.append(ecsline) 
 
    return eyecoords 

def perspective_projection(d, s, points):
    
    # screen is size 1024 x 1024
     
    vsx = 511.5 
    vsy = 511.5 
    vcx = 511.5 
    vcy = 511.5 
     
    screencoords = [] 
    for point in points:
       xe0 = point[0]
       ye0 = point[1]
       ze0 = point[2]
       xe1 = point[3]
       ye1 = point[4]
       ze1 = point[5]
       
       xs0 = ( (d*xe0) / (s*ze0) ) * vsx + vcx 
       ys0 = ( (d*ye0) / (s*ze0) ) * vsy + vcy
       xs1 = ( (d*xe1) / (s*ze1) ) * vsx + vcx 
       ys1 = ( (d*ye1) / (s*ze1) ) * vsy + vcy
       screencoords.append([xs0, ys0, xs1, ys1])
    
    return screencoords

def prompt_user():
   print("\nCommand Options")
   print(" - Translate: t")
   print(" - Scale: s")
   print(" - Rotate: r")
   print(" - Change user input: i") 
   print(" - Quit: q\n") 

def display_pixels():    
                                                          
    # the window is 1024 x 1024
    # x bounds [0, 1023]
    # y bounds [0, 1023] 
    
    # check that the screen coordinates are within the bounds of the screen
    for line in screencoords:
        x0 = int(line[0])
        y0 = int(line[1]) 
        x1 = int(line[2])
        y1 = int(line[3])
        
        # if a point is out of range, immediately return
        if x0 < 0 or x0 > 1023 or y0 < 0 or y0 > 1023 or x1 < 0 or x1 > 1023 or y1 < 0 or y1 > 1023:
            print("\nTranslated image is out of range. Please try again with different values.")
            return

    img = Image.new('RGB', (1024, 1024)) 
    pixels = img.load() 
    
    # scan-convert each line
    for line in screencoords:  
        x0 = int(line[0])
        y0 = int(line[1]) 
        x1 = int(line[2])
        y1 = int(line[3])
        # print("Coordinate Values:")
        # print("(" + str(x0) + ", " + str(y0) + ")")
        # print("(" + str(x1) + ", " + str(y1) + ")\n")
        bresenham_alg(x0, y0, x1, y1, pixels)

    img = img.transpose(Image.Transpose.FLIP_TOP_BOTTOM)   
    img.show()
    return

def input_file():
   
    points = [] 
    name = input("\nPlease provide the name of the file containing the data points: ").strip()

    # open and read the file
    try: 
        with open(name) as f:
            # read lines from txt file 
            for line in f.readlines():
                # append each line to the list
                points.append(line.strip().split(" "))
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

    # change all coordinates to floats
    rows = len(points)
    cols = len(points[0])
    for i in range(rows):
        for j in range(cols):
            points[i][j] = float(points[i][j])  
    
    return points 

def output_file():
    file = open("output.txt", "w")
    for i in newpoints:
        for j in i:
            file.write("%f " % j)
        file.write("\n") 
    file.close()

# MAIN PROGRAM BEGINS 

print("  ____  _____                                                                     ")                                                                  
print(" |___ \|  __ \                                                                    ")                                                              
print("   __) | |  | |                                                                   ")                                                           
print("  |__ <| |  | |                                                                   ")                                                            
print("  ___) | |__| |                                                                   ")   
print(" |____/|_____/                    _        _                                      ")                   
print("  / ___| ___  ___  _ __ ___   ___| |_ _ __(_) ___                                 ")                    
print(" | |  _ / _ \/ _ \| '_ ` _ \ / _ \ __| '__| |/ __|                                ")                 
print(" | |_| |  __/ (_) | | | | | |  __/ |_| |  | | (__                                 ")              
print("  \____|\___|\___/|_| |_| |_|\___|\__|_|  |_|\___|        _   _                   ")             
print(" |_   _| __ __ _ _ __  ___ / _| ___  _ __ _ __ ___   __ _| |_(_) ___  _ __  ___   ") 
print("   | || '__/ _` | '_ \/ __| |_ / _ \| '__| '_ ` _ \ / _` | __| |/ _ \| '_ \/ __|  ")
print("   | || | | (_| | | | \__ \  _| (_) | |  | | | | | | (_| | |_| | (_) | | | \__ \  ")
print("   |_||_|  \__,_|_| |_|___/_|  \___/|_|  |_| |_| |_|\__,_|\__|_|\___/|_| |_|___/  ")

# USER INPUT

datalines = input_file()
viewpoint = input("\nPlease provide the x y z coordinates of the viewpoint, separated by spaces only: ").strip().split(" ")

# make sure viewpoint coordinates were entered correctly 
try:
    for i in range(3):
        viewpoint[i] = float(viewpoint[i])
except:
    print("UNEXPECTED ERROR:", sys.exc_info()[0])
    print("Exiting program...")
    sys.exit(1)
        
screensize = float(input("\nPlease provide the size of the screen (in cm): ").strip())
s = screensize/2 # s is always equal to half the size of the screen 
d = float(input("\nLastly, please provide the distance away from the viewing point (in cm): ").strip())

# position of eye in virtual world
xv = viewpoint[0]
yv = viewpoint[1]
zv = viewpoint[2]

# MAIN PROGRAM LOOP

while (loop):
    
    prompt_user()
    inp = input("Choose a command: ").strip()
    print()
     
    if inp == "q":
        
        print("Quitting the program..\nBye!\n")
        loop = False
         
    elif inp == "t":
        
        tx = float(input("Translation in the x direction: "))
        ty = float(input("Translation in the y direction: ")) 
        tz = float(input("Translation in the z direction: "))   
        newpoints = translate(tx, ty, tz) # translate
        output_file() # output results to txt file 
        
        eyecoords = map_points(xv, yv, zv, newpoints) # map points to ECS  
        screencoords = perspective_projection(d, s, eyecoords) # apply perspective projection 
        display_pixels() # scan-convert
        
        # reset lists
        eyecoords.clear()
        screencoords.clear() 
        newpoints.clear() 
            
    elif inp == "s":
        
        sx = float(input("Horizontal scaling factor: "))
        sy = float(input("Vertical scaling factor: "))
        sz = float(input("Depth scaling factor: ")) 
        cx = float(input("Center of scale (x): "))
        cy = float(input("Center of scale (y): "))
        cz = float(input("Center of scale (z): "))
        newpoints = scale(sx, sy, sz, cx, cy, cz) # scale
        output_file() # output results to txt file 
        
        eyecoords = map_points(xv, yv, zv, newpoints) # map points to ECS  
        screencoords = perspective_projection(d, s, eyecoords) # apply perspective projection 
        display_pixels() # scan-convert
        
        # reset lists
        eyecoords.clear()
        screencoords.clear() 
        newpoints.clear()  
        
    elif inp == "r":
        
        print(" - Rotate about x-axis: x ")
        print(" - Rotate about y-axis: y ")
        print(" - Rotate about z-axis: z \n")
        axis = input("Choose an axis: ").strip()

        angle = float(input("\nRotation angle (counter-clockwise): ")) 
        cx = float(input("Center of rotation (x): "))
        cy = float(input("Center of rotation (y): "))
        cz = float(input("Center of rotation (z): ")) 

        if axis == "x":
            newpoints = rotatex(angle, cx, cy, cz)
        elif axis == "y": 
            newpoints = rotatey(angle, cx, cy, cz)
        elif axis == "z":
            newpoints = rotatez(angle, cx, cy, cz)
        else:
           print("\nERROR: Command not recognized")  
           continue    
        
        eyecoords = map_points(xv, yv, zv, newpoints) # map points to ECS  
        screencoords = perspective_projection(d, s, eyecoords) # apply perspective projection 
        display_pixels() # scan-convert
        
        # reset lists
        eyecoords.clear()
        screencoords.clear() 
        newpoints.clear()  
    
    elif inp == "i":
        
        viewpoint = input("Please provide the x y z coordinates of the viewpoint, separated by spaces only: ").strip().split(" ")

        # make sure viewpoint coordinates were entered correctly 
        try:
            for i in range(3):
                viewpoint[i] = float(viewpoint[i])
        except:
            print("UNEXPECTED ERROR:", sys.exc_info()[0])
            print("Exiting program...")
            sys.exit(1)
        
        screensize = float(input("\nPlease provide the size of the screen (in cm): ").strip())
        s = screensize/2 # s is always equal to half the size of the screen 
        d = float(input("\nLastly, please provide the distance away from the viewing point (in cm): ").strip())

        # position of eye in virtual world
        xv = viewpoint[0]
        yv = viewpoint[1]
        zv = viewpoint[2] 
    
    else:
        print("ERROR: Command not recognized")
        