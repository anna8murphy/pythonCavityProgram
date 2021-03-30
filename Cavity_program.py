import os.path
import math
from OCC.Display.SimpleGui import init_display
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere
from OCC.Core.gp import gp_Pnt
from OCC.Extend.DataExchange import read_step_file

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
      
    # Constants
    HASH_SIZE = 256
    DEFECT_MARKER_SIZE = 6.0
    DEFECT_MARKER_TRANSPARENCY = 0.0

    #takes inputs theta and z-coordinate to place defect on weld
    #theta = float(input("Input θ in degrees:  "))
    #z_coor = float(input("Input the z-coordinate: "))
    #x_coor = 91.425*(math.cos(theta))
    #y_coor = 91.425*(math.sin(theta))

    ### Globals
    # The location of the defects and the corresponding image file names
    defects = [
    {
    'location': [0, 91.425, 415.5],
    'image_file': 'C:\\Users\\Owner\\Desktop\\Documents\\School_20-21\\JLab\\DefectImages\\LSF9-1_C3_EQ_Phi0.CR2.jpg',
    },
    {
    'location': [0, 91.425, 315.5],
    'image_file': 'C:\\Users\\Owner\\Desktop\\Documents\\School_20-21\\JLab\\DefectImages\\LSF9-1_C3_EQ_Phi0_t0C4.CR2.jpg',
    },
    {
    'location': [0, 91.425, 215.5],
    'image_file': 'C:\\Users\\Owner\\Desktop\\Documents\\School_20-21\\JLab\\DefectImages\\LSF9-1_C3_EQ_Phi5.CR2.jpg',
    },
    ]

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

                my_label = Label(root, 
                                text = "Close this window before selecting another defect\n       Defect Coordinates: " + str(marker_info[hash]['location']),
                                foreground = "#A7A799",
                                font=("Helvetica", 13),
                                image = new_pic,
                                compound = "bottom")
                my_label.pack(pady=20)
                my_label.image = new_pic
                root.mainloop()
                

    ### Create the markers
    for n in range(len(defects)):
        x = defects[n]['location'][0]
        y = defects[n]['location'][1]
        z = defects[n]['location'][2]
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
    cavity = read_step_file(os.path.join("/Users", "Owner/Desktop", "Cavity Models", "JL0031321 C75 CAVITY ASSY.stp"))
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
