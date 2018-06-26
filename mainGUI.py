from tkinter import *
from random import *
from tkcalendar import *

root = Tk()
dates = []
currentDate = None


class Event:
    """ An event with a name and time the user has added to the calendar"""

    def __init__(self, length, name, beginningButton, date):
        self.name = name
        self.length = length
        self.startButton = beginningButton
        self.date = date
        self.positionInfo = self.startButton.grid_info()
        self.row = self.positionInfo["row"]
        self.date.events.append(self)

    def update(self):
        x = self.row
        x = int(x)
        amountToChange = x + self.length
        while x < amountToChange:
            self.date.buttons[x]["text"] = self.name
            x += 1
        indexes = [i for i, y in enumerate(self.date.buttons) if y["text"] == self.name]
        for z in indexes:
            if z not in range(int(self.row), int(self.row) + self.length):
                self.date.buttons[z]["text"] = "Nothing Scheduled"


class Date:
    """ Contains all events on a specific date"""

    def __init__(self, date, frame):
        self.date = date
        self.events = []
        self.buttons = []
        self.startH = 8
        self.endH = 21
        self.frame = frame

    def loadDate(self):
        global currentDate
        currentDate = self

        times = []

        while self.startH < self.endH:
            times.append(str(self.startH) + ":00")
            times.append(str(self.startH) + ":15")
            times.append(str(self.startH) + ":30")
            times.append(str(self.startH) + ":45")
            self.startH += 1

        for x in range(len(times)):
            Label(self.frame, text=times[x]).grid(row=x+1, column=0)
            z = Button(self.frame, text="Nothing Scheduled", width=15, command=lambda i=x: dialogMain(self.buttons[i]))
            z.grid(row=x+1, column=1)
            self.buttons.append(z)

        for event in self.events:
            event.update()


class ScheduleDialog:
    """The dialog window to add an event in a time block"""

    def __init__(self, parent, button):
        global currentDate
        choices = ["15 min", "30 min", "45 min", "1 hour", "2 hours", "3 hours"]
        self.choiceValues = {"15 min": 1, "30 min": 2, "45 min": 3, "1 hour": 4, "2 hours": 8, "3 hours": 12}
        self.timeChoice = StringVar(root)

        self.colorChoices = ["royal blue", "medium sea green", "yellow", "salmon", "coral", "indian red",
                             "medium orchid", "DarkOliveGreen1", "turquoise1", "khaki", "aquamarine"]
        shuffle(self.colorChoices)

        self.button = button
        self.positionInfo = self.button.grid_info()
        self.row = self.positionInfo["row"]

        self.event = None

        top = self.top = Toplevel(parent)

        if self.button["text"] == "Nothing Scheduled":
            Label(top, text="Event Name").pack()
            self.eventName = Entry(top)
            self.eventName.pack(padx=5)
            self.timeChoice.set("15 min")
            b = Button(top, text="OK", command=self.submit)

        else:
            Label(top, text="Edit Event").pack()
            self.eventName = Entry(top)
            self.eventName.pack(padx=5)
            self.eventName.insert(END, self.button["text"])

            for event in currentDate.events:
                if event.name == self.button["text"]:
                    self.event = event
                    for key, value in self.choiceValues.items():
                        if value == event.length:
                            self.timeChoice.set(key)
                break

            b = Button(top, text="OK", command=lambda i=self.event: self.edit(self.event))

        Label(top, text="How long is the event").pack()
        self.howLongMenu = OptionMenu(top, self.timeChoice, *choices)
        self.howLongMenu.pack(padx=5)

        b.pack(pady=5)

    def edit(self, event):
        event.length = (self.choiceValues.get(str(self.timeChoice.get())))
        event.name = self.eventName.get()
        event.update()

        self.top.destroy()

    def submit(self):
        numberToChange = (self.choiceValues.get(str(self.timeChoice.get())))

        self.event = Event(numberToChange, self.eventName.get(), self.button, currentDate)
        self.event.update()
        self.top.destroy()


def dialogMain(button):
    """Adds an event to a the time block"""
    d = ScheduleDialog(root, button)
    root.wait_window(d.top)


def main():

    def addScrollbar(Event):
        """Adds scrollbar for canvas"""
        canvas.configure(scrollregion=canvas.bbox("all"), width=200, height=356)

    def pickDate():
        def getDate():
            for date in dates:
                if date.date == cal.selection_get():
                    top.destroy()
                    date.loadDate()
                    return

            x = Date((cal.selection_get()), frame)
            dates.append(x)
            top.destroy()
            x.loadDate()

        top = tk.Toplevel(root)
        top.grab_set()

        cal = Calendar(top, font="Arial 14", selectmode='day', selectforeground="blue", foreground="black")

        cal.pack(fill="both", expand=True)
        tk.Button(top, text="Ok", command=getDate).pack()

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
    Button(frame, text='Choose Date', command=pickDate).grid(row=0, column=1, pady=2)
    root.mainloop()


if __name__ == "__main__":
    main()