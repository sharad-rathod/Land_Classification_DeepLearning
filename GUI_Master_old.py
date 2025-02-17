import tkinter as tk
from tkinter import ttk, LEFT, END
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfilename

# import cv2
import numpy as np
import time
import cv2
import CNNModel
import sqlite3

# import tfModel_test as tf_test
global fn
fn = ""
##############################################+=============================================================
root = tk.Tk()
root.configure(background="seashell2")
# root.geometry("1300x700")


w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))
root.title("Land Classification Using Satellite Image")


# 430
# ++++++++++++++++++++++++++++++++++++++++++++
#####For background Image
img = ImageTk.PhotoImage(Image.open("img1.jpg"))

img2 = ImageTk.PhotoImage(Image.open("img2.jpg"))

img3 = ImageTk.PhotoImage(Image.open("img3.jpg"))


logo_label = tk.Label()
logo_label.place(x=0, y=0)

x = 1


# function to change to next image
def move():
    global x
    if x == 4:
        x = 1
    if x == 1:
        logo_label.config(image=img)
    elif x == 2:
        logo_label.config(image=img2)
    elif x == 3:
        logo_label.config(image=img3)
    x = x + 1
    root.after(2000, move)


move()

lbl = tk.Label(
    root,
    text="Land Classification on Satellite Images",
    font=("times", 35, " bold "),
    height=1,
    width=65,
    bg="violet Red",
    fg="Black",
)
lbl.place(x=0, y=0)


frame_alpr = tk.LabelFrame(
    root,
    text=" --Process-- ",
    width=220,
    height=400,
    bd=5,
    font=("times", 14, " bold "),
    bg="lawn Green",
)
frame_alpr.grid(row=0, column=0, sticky="nw")
frame_alpr.place(x=10, y=120)


def update_label1(str_T):
    # clear_img()
    result_label = tk.Label(
        root, text=str_T, width=40, font=("bold", 25), bg="bisque2", fg="black"
    )
    result_label.place(x=300, y=550)


################################$%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def update_cal(str_T):
    # clear_img()
    result_label = tk.Label(
        root, text=str_T, width=40, font=("bold", 25), bg="bisque2", fg="black"
    )
    result_label.place(x=350, y=400)


###########################################################################
def train_model():

    update_label("Model Training Start...............")

    start = time.time()

    X = CNNModel.main()

    end = time.time()

    ET = "Execution Time: {0:.4} seconds \n".format(end - start)

    msg = "Model Training Completed.." + "\n" + X + "\n" + ET

    print(msg)


import functools
import operator


def convert_str_to_tuple(tup):
    s = functools.reduce(operator.add, (tup))
    return s


def test_model_proc(fn):
    from keras.models import load_model
    from tensorflow.keras.optimizers import Adam

    #    global fn

    IMAGE_SIZE = 64
    LEARN_RATE = 1.0e-4
    CH = 3
    print(fn)
    if fn != "":
        # Model Architecture and Compilation

        model = load_model("land1_model.h5")

        img = Image.open(fn)
        img = img.resize((IMAGE_SIZE, IMAGE_SIZE))
        img = np.array(img)

        img = img.reshape(1, IMAGE_SIZE, IMAGE_SIZE, 3)

        img = img.astype("float32")
        img = img / 255.0
        print("img shape:", img)
        prediction = model.predict(img)
        print(np.argmax(prediction))
        crop = np.argmax(prediction)
        print(crop)

        if crop == 0:
            Cd = "agricultural"
            # _label = tk.Label(root, text="Crop \n Wheat,Sunflower,Soybean,Cotton,Sorghum,Maize,Groundnut,Citrus,Beans", width=48, font=("bold", 25), bg='black', fg='white')
            # _label.place(x=300, y=650)
        elif crop == 1:
            Cd = "baseballdiamond"
            # _label = tk.Label(root, text="Crop\n Alfalfa,peaches,pears,nectarines,cherries,Cucurbitaceae,Corn,squash,small shrubs", width=48, font=("bold", 25), bg='black', fg='white')
            # _label.place(x=300, y=650)
        elif crop == 2:
            Cd = "beach"
            # _label = tk.Label(root, text="Crop \n sunnhemp,dhaincha,pillipesara,clusterbeans,sesbania,rostrata,cow pea", width=48, font=("bold", 25), bg='black', fg='white')
            # _label.place(x=300, y=650)
        elif crop == 3:
            Cd = "forest"

        elif crop == 4:
            Cd = "golfcourse"

        elif crop == 5:
            Cd = "river"

        elif crop == 6:
            Cd = "runway"

        A = Cd
        return A


def update_label(str_T):
    # clear_img()
    result_label = tk.Label(
        root, text=str_T, width=40, font=("bold", 25), bg="bisque2", fg="black"
    )
    result_label.place(x=300, y=450)


def test_model():
    global fn
    if fn != "":
        update_label("Model Testing Start...............")

        start = time.time()

        X = test_model_proc(fn)

        X1 = "Selected  satellite Image is {0}".format(X)

        end = time.time()

        ET = "Execution Time: {0:.4} seconds \n".format(end - start)

        msg = "Image Testing Completed.." + "\n" + X1 + "\n" + ET
        fn = ""
    else:
        msg = "Please Select Image For Prediction...."

    update_label(msg)


def openimage():

    global fn
    fileName = askopenfilename(
        initialdir="D:/Final code/crop classification",
        title="Select image for Aanalysis ",
        filetypes=[("all files", "*.*")],
    )
    IMAGE_SIZE = 200
    imgpath = fileName
    fn = fileName

    #        img = Image.open(imgpath).convert("L")
    img = Image.open(imgpath)

    img = img.resize((IMAGE_SIZE, 200))
    img = np.array(img)
    #        img = img / 255.0
    #        img = img.reshape(1,IMAGE_SIZE,IMAGE_SIZE,3)

    x1 = int(img.shape[0])
    y1 = int(img.shape[1])

    #
    #        gs = cv2.cvtColor(cv2.imread(imgpath, 1), cv2.COLOR_RGB2GRAY)
    #
    #        gs = cv2.resize(gs, (x1, y1))
    #
    #        retval, threshold = cv2.threshold(gs, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    im = Image.fromarray(img)
    imgtk = ImageTk.PhotoImage(im)
    img = tk.Label(root, image=imgtk, height=250, width=250)

    # result_label1 = tk.Label(root, image=imgtk, width=250,height=250)
    # result_label1.place(x=300, y=100)
    img.image = imgtk
    img.place(x=300, y=100)


# out_label.config(text=imgpath)


def convert_grey():
    global fn
    IMAGE_SIZE = 200

    img = Image.open(fn)
    img = img.resize((IMAGE_SIZE, 200))
    img = np.array(img)

    x1 = int(img.shape[0])
    y1 = int(img.shape[1])

    gs = cv2.cvtColor(cv2.imread(fn, 1), cv2.COLOR_RGB2GRAY)

    gs = cv2.resize(gs, (x1, y1))

    retval, threshold = cv2.threshold(
        gs, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )
    print(threshold)

    im = Image.fromarray(gs)
    imgtk = ImageTk.PhotoImage(image=im)

    # result_label1 = tk.Label(root, image=imgtk, width=250, font=("bold", 25), bg='bisque2', fg='black',height=250)
    # result_label1.place(x=300, y=400)
    img2 = tk.Label(root, image=imgtk, height=250, width=250, bg="white")
    img2.image = imgtk
    img2.place(x=580, y=100)

    im = Image.fromarray(threshold)
    imgtk = ImageTk.PhotoImage(image=im)

    img3 = tk.Label(root, image=imgtk, height=250, width=250)
    img3.image = imgtk
    img3.place(x=880, y=100)
    # result_label1 = tk.Label(root, image=imgtk, width=250,height=250, font=("bold", 25), bg='bisque2', fg='black')
    # result_label1.place(x=300, y=400)


#################################################################################################################
def window():
    root.destroy()


button1 = tk.Button(
    frame_alpr,
    text=" Select_Image ",
    command=openimage,
    width=15,
    height=1,
    font=("times", 15, " bold "),
    bg="white",
    fg="black",
)
button1.place(x=10, y=50)

button2 = tk.Button(
    frame_alpr,
    text="Image_preprocess",
    command=convert_grey,
    width=15,
    height=1,
    font=("times", 15, " bold "),
    bg="white",
    fg="black",
)
button2.place(x=10, y=130)

# button3 = tk.Button(frame_alpr, text="Train Model", command=train_model, width=12, height=1, font=('times', 15, ' bold '),bg="white",fg="black")
# button3.place(x=10, y=160)

button4 = tk.Button(
    frame_alpr,
    text="CNN_Prediction",
    command=test_model,
    width=15,
    height=1,
    bg="white",
    fg="black",
    font=("times", 15, " bold "),
)
button4.place(x=10, y=210)
#
#
# button5 = tk.Button(frame_alpr, text="button5", command=window,width=8, height=1, font=('times', 15, ' bold '),bg="yellow4",fg="white")
# button5.place(x=450, y=20)


exit = tk.Button(
    frame_alpr,
    text="Exit",
    command=window,
    width=15,
    height=1,
    font=("times", 15, " bold "),
    bg="red",
    fg="white",
)
exit.place(x=10, y=290)


root.mainloop()
