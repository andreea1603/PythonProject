from tkinter import Button
from matplotlib import pyplot as plt


def savePdf():
    """ Description: saving the plot as pdf    """
    plt.savefig('plot.pdf')


def savePng():
    """ Description: saving the plot as png    """
    plt.savefig('plot.png')


def plotButton(k):
    """ Description: displaying the button for saving the plot """

    if k == 0:
        b1 = Button(text="Save as Png", command=savePng)
        b1.place(x=200, y=400, width=150)
        b2 = Button(text="Save as Pdf", command=savePdf)
        b2.place(x=200, y=350, width=150)
        plt.show()
        k = 1