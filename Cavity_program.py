#Notes:
#Update program to Github
#Create JSON file in LabVIEW
#.CR2 to .jpg file conversion after reading from JSON
#include cavity model path in JSON?
#takes inputs theta and z-coordinate from JSON and converts to x,y, and z coords

import os.path
import json
import math

#PythonOCC library
from OCC.Display.SimpleGui import init_display
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere
from OCC.Core.gp import gp_Pnt
from OCC.Extend.DataExchange import read_step_file

#image processing
from tkinter import *
from PIL import ImageTk, Image
from tkinter.ttk import *

#import rawpy
#import imageio

#converts raw .CR2 file type to .jpg
#pathNames = ["LSF9-1_C3_EQ_Phi0.CR2", "LSF9-1_C3_EQ_Phi0_t0C4.CR2", "LSF9-1_C3_EQ_Phi5.CR2"]

#for i in pathNames:
#    path = "C:\\Users\\Owner\\Desktop\\Documents\\School_20-21\\JLab\\DefectImages\\" + i
#    savedPath = "C:\\Users\\Owner\\Desktop\\Documents\\School_20-21\\JLab\\DefectImages\\" + str(i) + ".jpg"

#    with rawpy.imread(path) as raw:
#        rgb = raw.postprocess()
#        imageio.imsave(savedPath, rgb)
  
# creates a Tk() object 
master = Tk() 
  
# sets the geometry of main  
# root window 
master.geometry("420x100") 
  
# function to open a new window  
# on a button click 
def openCavityProgram(): 

    #cavityPath = input("Enter 3D cavity file path: ")  #/Users/Owner/Desktop/Cavity Models/JL0031321 C75 CAVITY ASSY.stp
    # Constants
    HASH_SIZE = 256
    DEFECT_MARKER_SIZE = 6.0
    DEFECT_MARKER_TRANSPARENCY = 0.0

    #include in talk 
    #takes inputs theta and z-coordinate to place defect on weld
    #theta = float(input("Input θ in degrees:  "))
    #z_coor = float(input("Input the z-coordinate: "))
    #x_coor = 91.425*(math.cos(theta))
    #y_coor = 91.425*(math.sin(theta))

    # read a json file with image and cavity paths into a dictionary:
    with open("C:/Users/Owner/Desktop/Documents/School_20-21/JLab/imagePathNames.json") as f:
        data = json.load(f)
        modelPath = data["modelPath"]
        defects = data["defects"]
	
    marker_info = {} # Coords and filenames by object hash
    marker_spheres = [] # The OCC Geometry Objects

    # look up the marker by its hash and print the coordinates and the image file name
    def print_defect_filename(shp, *kwargs):
        for shape in shp:
            hash = shape.HashCode(HASH_SIZE)
            if hash in marker_info:
                imagefile = marker_info[hash]['image_file']
                #print("Defect Coordinates: " + str(marker_info[hash]['location']) + " Image file: " + imagefile)
                
                root = Tk()
                root.title("Cavity Display Window")
                root.geometry("1000x600")

                my_pic = Image.open(imagefile)
                tk_pil_img = ImageTk.PhotoImage(my_pic, master=root)
                #print("width: " + str(tk_pil_img.width()) + " height: " + str(tk_pil_img.height()))

                resized = my_pic.resize((900,500), Image.ANTIALIAS)
                new_pic = ImageTk.PhotoImage(resized)

                x_info = str("{:.1f}".format(91.425*(math.cos(marker_info[hash]['location'][1]))))
                y_info = str("{:.1f}".format(91.425*(math.sin(marker_info[hash]['location'][1]))))
                z_info = str(marker_info[hash]['location'][0])

                my_label = Label(root, 
                                text = "Close this window before selecting another defect\n       Defect Coordinates: [" + x_info + ", " + y_info + ", " + z_info + "]",
                                foreground = "#A7A799",
                                font=("Helvetica", 13),
                                image = new_pic,
                                compound = "bottom")
                my_label.pack(pady=20)
                my_label.image = new_pic
                root.mainloop()
                

    ### Create the markers
    for n in range(len(defects)):
        z = defects[n]['location'][0]
        theta = defects[n]['location'][1]
        x = 91.425*(math.cos(theta))
        y = 91.425*(math.sin(theta))

        marker_geom = BRepPrimAPI_MakeSphere(gp_Pnt(x,y,z), DEFECT_MARKER_SIZE).Shape()
        geom_hash = marker_geom.HashCode(HASH_SIZE)
        marker_spheres.append(marker_geom)
        marker_info[geom_hash] = defects[n]
    #print(marker_info)
    #print(marker_spheres)

    display, start_display, add_menu, add_function_to_menu = init_display()

    # register callbacks
    display.register_select_callback(print_defect_filename)

    ### Load the cavity model
    
    cavity = read_step_file(modelPath)
    display.DisplayShape(cavity, update=True)
    # display the markers
    for sphere in marker_spheres:
        ais_sphere = display.DisplayColoredShape(sphere, color="RED")[0]
        ais_sphere.SetTransparency(DEFECT_MARKER_TRANSPARENCY)
    display.FitAll()
    start_display()

#Instruction window- a button widget which will open a new window + cavity program on button click 
master.title("Cavity Program")  
label = Label(master,  
              text ="Close each Cavity Display Window before selecting another defect", 
              font=("Helvetica", 10)
             ) 
  
label.pack(pady = 10) 
  
def close_window():
    master.destroy()

btn = Button(master,  
             text ="Continue",  
            command = lambda:[close_window(), openCavityProgram()])
btn.pack(pady = 10) 
  
# mainloop, runs infinitely 
mainloop() 