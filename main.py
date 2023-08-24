from PIL import Image, ImageFont, ImageDraw
import face_recognition_models
import PIL
import time
import pynput.keyboard
from PIL import ImageGrab
import pydirectinput as auto
from tkinter import *
from queue import Queue
import threading
import pyautogui as pyauto
import msvcrt

q = Queue()
root = Tk()
root.title("softaim")
correctionslabel = Label(root, text="factor: 2.78359 @ 800x63")
label1 = Label(root, text="X position:")
label1.grid(row=1, column=0)
currentxlabel = Label(root, text="0")
currentxlabel.grid(row=1, column=1, padx=10)
label2 = Label(root, text="Y position: ")
label2.grid(row=2, column=0)
currentylabel = Label(root, text="0")
currentylabel.grid(row=2, column=1)
label3 = Label(root, text="trg st")
label3.grid(row=3, column=0)
targetstatus = Label(root, text="waiting for trigger")
targetstatus.configure(fg="#fab700")
targetstatus.grid(row=3, column=1)
snapcoslabel = Label(root, text="trg cr:")
snapcoslabel.grid(row=4, column=0)
snapcoordinates = Label(root, text="N/A")
snapcoordinates.configure(fg="#fab700")
snapcoordinates.grid(row=4, column=1)
statuslabel = Label(root, text="stat:")
statuslabel.grid(row=5, column=0)
status = Label(root, text="initializing program")
status.grid(row=5, column=1)

window_width = 210
window_height = 110

# Berechne die Position des Fensters, um es mittig zu zentrieren
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2

# Kombiniere die Position und Größe, um die Geometry des Fensters zu setzen
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

def Snaptoplayer():
    ImageBox = None
    IN = ImageGrab.grab(ImageBox)
    IN.save("screenshot.png")
    IN.close()

    imageToScan = face_recognition_models.load_image_file("screenshot.png")
    face_locations = face_recognition_models.face_locations(imageToScan)

    xcoordinate = ""
    ycoordinate = ""
    Snapto = ""

    for location in face_locations:
        xcoordinate = location[3] + 40
        ycoordinate = location[8] + 20
        Snapto = (xcoordinate, ycoordinate)
        rcos = [location[1], location[8], location[3], location[2]]
        br = (location[3], location[2] + 5)
        br2 = (location[3], location[2] + 50)

        if xcoordinate == "" or ycoordinate == "":
            return

        relativex = xcoordinate - 960
        relativey = ycoordinate - 540

        myfont = ImageFont.truetype(r"", 30)

        image = PIL.Image.fromarray(imageToScan)
        draw = ImageDraw.Draw(image)
        draw.rectangle(rcos, outline="yellow", width=15)
        draw.text((5, 5), text=f"current: {auto.position()} \ntarget: {xcoordinate}, {ycoordinate}")

        image.save("myimage.png")


def GUILoop():
    def updateCoordinates():
        coordinates = auto.position()
        xc = coordinates[0]
        yc = coordinates[1]

        xcoordinate = ""
        ycoordinate = ""

        for s in str(xc):
            if s == "(" or s == ")" or s == "," or s == "":
                continue
            else:
                xcoordinate = xcoordinate + s
        for s in str(yc):
            if s == "(" or s == ")" or s == "," or s == "":
                continue
            else:
                ycoordinate = ycoordinate + s

        currentxlabel.configure(text=xcoordinate)
        currentylabel.configure(text=ycoordinate)

    while True:
        try:
            data = q.get(False)
        except:
            updateCoordinates()
            time.sleep(0.1)
            continue

        updateCoordinates()
        continue


gui_thread = threading.Thread(target=GUILoop)
gui_thread.daemon = True
gui_thread.start()

q.put("init")
root.mainloop()