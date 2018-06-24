""" Creates canvas, frame, and scrollbar,
    as well as adding all time intervals."""

from tkinter import *

startHour = 8
endHour = 21


def addTimes(startH, endH):
    """ Adds all 15 minute intervals between start and end time to frame"""
    times = []
    while startH < endH:
        times.append(str(startH) + ":00")
        times.append(str(startH) + ":15")
        times.append(str(startH) + ":30")
        times.append(str(startH) + ":45")
        startH += 1

    for x in range(len(times)):
        Label(frame, text=times[x]).grid(row=x, column=0)
        Label(frame, text="Nothing Scheduled").grid(row=x, column=1)


def addScrollbar(event):
    """Adds scrollbar for canvas"""
    canvas.configure(scrollregion=canvas.bbox("all"), width=200, height=356)


root = Tk()

sizex = 225
sizey = 356
root.wm_geometry("%dx%d+0+0" % (sizex, sizey))
root.title("Time Blocker")

myframe = Frame(root, relief=GROOVE, width=50, height=100, bd=1)
myframe.place(x=0, y=0)

canvas = Canvas(myframe)
frame = Frame(canvas)
myscrollbar = Scrollbar(myframe, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=myscrollbar.set)

myscrollbar.pack(side="right", fill="y")
canvas.pack(side="left")
canvas.create_window((0, 0), window=frame, anchor='nw')
frame.bind("<Configure>", addScrollbar)
addTimes(startHour, endHour)
root.mainloop()
