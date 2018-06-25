from tkinter import *
from random import *

root = Tk()
startHour = 8
endHour = 21
myButtons = []

class ScheduleDialog:
    """The dialog window to add an event in a time block"""

    def __init__(self, parent, button):

        choices = ["15 min", "30 min", "45 min", "1 hour", "2 hours", "3 hours"]
        self.choiceValues = {"15 min": 1, "30 min": 2, "45 min": 3, "1 hour": 4, "2 hours": 8, "3 hours": 12}
        self.timeChoice = StringVar(root)

        self.colorChoices = ["royal blue", "medium sea green", "yellow", "salmon", "coral", "indian red",
                             "medium orchid", "DarkOliveGreen1", "turquoise1", "khaki", "aquamarine"]
        shuffle(self.colorChoices)

        self.button = button
        self.positionInfo = self.button.grid_info()
        self.row = self.positionInfo["row"]

        top = self.top = Toplevel(parent)

        if self.button["text"] == "Nothing Scheduled":
            Label(top, text="Event Name").pack()
            self.eventName = Entry(top)
            self.eventName.pack(padx=5)
            self.timeChoice.set("15 min")
            b = Button(top, text="OK", command=self.submit)

        else:
            Label(top, text="Add Event").pack()
            self.eventName = Entry(top)
            self.eventName.pack(padx=5)
            self.eventName.insert(END, self.button["text"])

            i = 0
            for x in myButtons:
                if x["text"] == self.button["text"]:
                    i += 1
            for key, value in self.choiceValues.items():
                if value == i:
                    self.timeChoice.set(key)

            b = Button(top, text="OK", command=self.edit)

        Label(top, text="How long is the event").pack()
        self.howLongMenu = OptionMenu(top, self.timeChoice, *choices)
        self.howLongMenu.pack(padx=5)

        b.pack(pady=5)

    def edit(self):
        a = None
        for x in myButtons:
            if x["text"] == self.button["text"]:
                a = x.grid_info()
                break

        numberToChange = (self.choiceValues.get(str(self.timeChoice.get())))
        for x in range(int(a["row"]), int(a["row"]) + numberToChange):
            myButtons[x]["text"] = self.eventName.get()
        indexes = [i for i, x in enumerate(myButtons) if x["text"] == self.eventName.get()]
        for x in indexes:
            if x not in range(int(a["row"]), int(a["row"]) + numberToChange):
                myButtons[x]["text"] = "Nothing Scheduled"
        self.top.destroy()

    def submit(self):
        numberToChange = (self.choiceValues.get(str(self.timeChoice.get())))
        for x in range(int(self.row), int(self.row) + numberToChange):
            myButtons[x]["text"] = self.eventName.get()
            # myButtons[x].configure(background="aquamarine")     # self.colorChoices[8]
        self.top.destroy()


def dialogMain(button):
    """Adds an event to a the time block"""
    d = ScheduleDialog(root, button)
    root.wait_window(d.top)


def addTimes(startH, endH, frame):
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
        z = Button(frame, text="Nothing Scheduled", command=lambda i=x: dialogMain(myButtons[i]), width=15)
        z.grid(row=x, column=1)
        myButtons.append(z)


def main():

    def addScrollbar(Event):
        """Adds scrollbar for canvas"""
        canvas.configure(scrollregion=canvas.bbox("all"), width=200, height=356)

    sizex = 225
    sizey = 356
    root.wm_geometry("%dx%d+0+0" % (sizex, sizey))
    root.title("Time Blocker")
    root.resizable(width=False, height=False)

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
    addTimes(startHour, endHour, frame)
    root.mainloop()


if __name__ == "__main__":
    main()