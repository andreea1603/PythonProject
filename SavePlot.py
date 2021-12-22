from tkinter import Button
from matplotlib import pyplot as plt


def savePdf():
    plt.savefig('plotTry.pdf')


def savePng():
    plt.savefig('plotTry.png')


def plotButton(k):
    if k == 0:
        k = 1
        b1 = Button(text="Save as Png", command=savePng)
        b1.place(x=200, y=400, width=150)
        b2 = Button(text="Save as Pdf", command=savePdf)
        b2.place(x=200, y=350, width=150)
        plt.show()