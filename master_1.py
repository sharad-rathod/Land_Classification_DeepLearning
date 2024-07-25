

import tkinter as tk
from tkinter import ttk, LEFT, END
from PIL import Image, ImageTk

##############################################+=============================================================
root = tk.Tk()
root.configure(background="brown")


w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))
root.title("Land Classification on Satellite Images")


# ++++++++++++++++++++++++++++++++++++++++++++
#####For background Image
image2 = Image.open('farmer.jpg')
image2 = image2.resize((1500, 800), Image.ANTIALIAS)

background_image = ImageTk.PhotoImage(image2)

background_label = tk.Label(root, image=background_image)

background_label.image = background_image

background_label.place(x=0, y=0)  # , relwidth=1, relheight=1)
#
label_l1 = tk.Label(root, text="Land classification By Using Satellite Image",font=("Times New Roman", 30, 'bold'),
                    background="Green", fg="white", width=60, height=2)
label_l1.place(x=0, y=0)



#################################################################$%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%






def reg():
    from subprocess import call
    call(["python","GUI_Master_old.py"])

def log():
    from subprocess import call
    call(["python","price_prediction.py"])
    
def gov():
    from subprocess import call
    call(["python","govt.py"])

    
def window():
  root.destroy()


button1 = tk.Button(root, text="Soil Detection", command=reg, width=17, height=1,font=('times', 20, ' bold '), bg="LimeGreen", fg="black")
button1.place(x=100, y=160)

button2 = tk.Button(root, text="Price Prediction",command=log,width=17, height=1,font=('times', 20, ' bold '), bg="LimeGreen", fg="black")
button2.place(x=100, y=240)

button3 = tk.Button(root, text="Government Scheme",command=gov,width=17, height=1,font=('times', 20, ' bold '), bg="LimeGreen", fg="black")
button3.place(x=100, y=330)

button3 = tk.Button(root, text="Exit",command=window,width=17, height=1,font=('times', 20, ' bold '), bg="red", fg="black")
button3.place(x=100, y=420)

root.mainloop()