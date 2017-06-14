__author__ = 'u3k'
from Tkinter import *
import tkFileDialog
import tkFont
import threading
import os

import math
import numpy as np
from watermark import FFT
from LSB1 import LSB
from PIL import Image, ImageTk


root = Tk()
color = 'beige'
button = Button(root)
root.title("Digital Watermarking")
root.geometry("370x120")
root.configure(background = color)
root.resizable(width=True, height=True)
v = IntVar()
#maxsize = 600,330

class Digimark(threading.Thread):

    v1=StringVar()
    v2=StringVar()
    tempdir1 = ""
    tempdir2 = ""
    openLabel = Entry(root,textvariable=v1,width=50)
    label1 = Label()
    label2 = Label()
    carrierSize = Label()
    markedSize = Label()
    RMS = Label()

    def __init__(self):
        super(Digimark, self).__init__()
        self.customFont = tkFont.Font(family="Courier", size=10)
        button.grid_forget()


    # def PSNR(self,original, marked):
    #     # imageA = cv2.imread(original)
    #     # imageB = cv2.imread(marked)
    #     # imageA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
    #     # imageB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)
    #     imageA= Image.open(original)
    #     imageA = imageA.convert('1')
    #     imageB= Image.open(marked)
    #     imageB = imageB.convert('1')
    #     # the 'Mean Squared Error' between the two images is the
    #     # sum of the squared difference between the two images;
    #     # NOTE: the two images must have the same dimension
    #     err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    #     err /= float(imageA.shape[0] * imageA.shape[1])
    #     psnr = 10*(math.log((65025/err),10))
    #     print(psnr)
    #     return str(psnr)


    def openfile(self):
        currdir = os.getcwd()
        self.tempdir1 = tkFileDialog.askopenfilename(parent=root, filetypes = (("jpeg files","*.jpg"),("jpeg","*.jpeg"),("png","*.png")) ,initialdir=currdir, title='Please select a directory')
        self.v1.set(self.tempdir1)
        self.openfilename = os.path.split(self.tempdir1)[0] + "/" + os.path.split(self.tempdir1)[1]


    def postProcess(self,path,algo,mode):
        self.label1.grid_forget()
        self.label2.grid_forget()
        root.geometry("1250x600")
        self.image1 = Image.open(self.openfilename)
        self.image1.thumbnail((630,300),Image.ANTIALIAS)
        photo1 = ImageTk.PhotoImage(self.image1)
        self.label1 = Label(image=photo1)
        self.label1.image = photo1
        self.label1.grid(row=5,column=0,padx=10,columnspan = 20,pady=20)

        if(algo==0 and mode==0):
            self.label2 = Label(text=path)

        else:
            self.image2 = Image.open(path)
            self.image2.thumbnail((630,300),Image.ANTIALIAS)
            photo2 = ImageTk.PhotoImage(self.image2)
            self.label2 = Label(image=photo2)
            self.label2.image = photo2

        self.label2.grid(row=5,column=20,padx=10,pady=20)

        # if(mode==1):
        #     self.carrierSize = Label(text = str(os.stat(self.openfilename).st_size/1024) + " KB",bg = color)
        #     self.markedSize = Label(text = str(os.stat(path).st_size/1024) + " KB",bg = color)
        #     #self.RMS = Label(text = "PSNR = " + self.PSNR(self.openfilename,path),bg = color)
        #     self.carrierSize.grid(row = 6,column = 1)
        #     self.markedSize.grid(row = 6,column = 20)
        #     #self.RMS.grid(row=7,column = 20, padx=10,pady=5)


    def selector(self,flag,mode):
        print(flag)
        if(flag==2):
            path = FFT(self.openfilename,mode)
            self.postProcess(path,0,mode)
        else:
            path = LSB(self.openfilename,mode)
            self.postProcess(path,1,mode)


    def paint(self):
        self.button1 = Button(root,text="Open",command = self.openfile)
        R1 = Radiobutton(root, text="LSB", variable=v, value=1, bg=color)
        R2 = Radiobutton(root, text="FFT", variable=v, value=2, bg=color)
        encode = Button(root,text="Watermark",command = lambda: self.selector(v.get(),1),padx='5')
        decode = Button(root,text="Detect",command = lambda: self.selector(v.get(),0) )
        R1.select()
        R1.grid(row=3,column=0,sticky='W')
        R2.grid(row=3,column=0)
        self.openLabel.grid(row=1,column=0,sticky='W',pady='10',padx='5')
        self.button1.grid(row=1,column=1,pady='10',sticky='W')
        encode.grid(row=4,column=0,sticky='W',padx='5')
        decode.grid(row=4,column=0,padx='5')


    def run(self):
        self.paint()


digi = Digimark()
digi.start()
mainloop()