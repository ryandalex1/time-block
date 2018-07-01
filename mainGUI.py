from tkinter import *
from random import *
from tkcalendar import *
from datetime import *
from os import path
import shelve

root = None
frame = None
start_hour = 0
end_hour = 0
dates = []
currentDate = None


class Event:
    """ An event with a name and time the user has added to the calendar"""

    def __init__(self, length, name, beginning_button, date):
        self.name = name
        self.length = length
        self.startButton = beginning_button
        self.date = date
        self.positionInfo = self.startButton.grid_info()
        self.row = self.positionInfo["row"]
        self.positionInfo = None
        self.startButton = None
        self.date.events.append(self)

        self.date.buttons = None
        event_shelve = shelve.open("eventStorage.dat")
        event_shelve[self.date.dString] = self.date
        event_shelve[self.date.dString].load_date()
        event_shelve.close()
        self.date.load_date()
        # self.startButton = None

    def update(self):
        """ Updates all buttons contained in the event with the correct text"""
        x = self.row
        x = int(x)
        number_to_change = x + self.length
        while x < number_to_change:
            self.date.buttons[x-1]["text"] = self.name
            x += 1
        indexes = [i for i, y in enumerate(self.date.buttons) if y["text"] == self.name]
        for z in indexes:
            if z not in range(int(self.row)-1, int(self.row)-1 + self.length):
                self.date.buttons[z]["text"] = "Nothing Scheduled"


class Date:
    """ Contains all events on a specific date"""

    def __init__(self, date):
        self.date = date
        self.events = []
        self.startH = start_hour
        self.endH = end_hour
        self.dString = str(self.date.year) + str(self.date.month) + str(self.date.day)
        self.startHChange = self.startH

    def load_date(self):
        """ Loads the GUI for a specific day"""
        global currentDate
        currentDate = self

        self.buttons = []
        times = []

        # Display date at top left
        date_string = str(self.date.month) + "/" + str(self.date.day)
        Label(frame, text=date_string, foreground="royal blue").grid(row=0, column=0, pady=2)

        Button(frame, text='Choose Date', command=pick_date).grid(row=0, column=1, pady=2)

        # Adds labels for each time slot
        self.startHChange = self.startH
        while self.startHChange < self.endH:
            times.append(str(self.startH) + ":00")
            times.append(str(self.startH) + ":15")
            times.append(str(self.startH) + ":30")
            times.append(str(self.startH) + ":45")
            self.startHChange += 1

        # Adds a button for each time slot
        for x in range(len(times)):
            Label(frame, text=times[x]).grid(row=x+1, column=0)
            z = Button(frame, text="Nothing Scheduled", width=15,
                       command=lambda i=x: schedule_dialog_main(self.buttons[i]))
            z.grid(row=x+1, column=1)
            self.buttons.append(z)

        # Displays all events already added
        for event in self.events:
            event.update()
        # TODO Does not load correctly when going back to a day with events


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
        # TODO Find fix for OSX

        self.button = button
        self.positionInfo = self.button.grid_info()
        self.row = self.positionInfo["row"]

        self.event = None

        # Delete button
        self.d = None

        top = self.top = Toplevel(parent)

        # Create dialog to add event
        if self.button["text"] == "Nothing Scheduled":
            Label(top, text="Event Name").pack()
            self.eventName = Entry(top)
            self.eventName.pack(padx=5)
            self.timeChoice.set("15 min")
            b = Button(top, text="OK", command=self.submit)

        # Create dialog to update event
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
            self.d = Button(top, text="Delete Event", command=lambda i=self.event: self.delete(self.event))

        Label(top, text="How long is the event").pack()
        self.howLongMenu = OptionMenu(top, self.timeChoice, *choices)
        self.howLongMenu.pack(padx=5)

        b.pack(pady=5)
        if self.d is not None:
            self.d.pack(pady=5)

    def edit(self, event):
        """ Update the selected event"""
        event.length = (self.choiceValues.get(str(self.timeChoice.get())))
        event.name = self.eventName.get()
        event.update()

        self.top.destroy()

    def submit(self):
        """ Create a new event as specified and update it"""
        number_to_change = (self.choiceValues.get(str(self.timeChoice.get())))

        self.event = Event(number_to_change, self.eventName.get(), self.button, currentDate)
        self.event.update()
        self.top.destroy()

    def delete(self, event):
        """ Deletes an event"""
        for x in currentDate.events:
            if x.name == event.name:
                currentDate.events.remove(x)
        event.length = 0
        event.update()
        self.top.destroy()


class SettingsDialog(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent

        self.startValues = {"5:00AM": 5, "6:00AM": 6, "7:00AM": 7, "8:00AM": 8, "9:00AM": 9, "10:00AM": 10}
        self.startChoice = StringVar(root)
        self.startChoice.set("7:00AM")

        self.endValues = {"5:00PM": 17, "6:00PM": 18, "7:00PM": 19, "8:00PM": 20, "9:00PM": 21, "10:00PM": 22}
        self.endChoice = StringVar(root)
        self.endChoice.set("7:00PM")

        Label(parent, text="Welcome to Time Blocker").pack()

        Label(parent, text="What time does your day start?").pack()

        self.startTimeMenu = OptionMenu(parent, self.startChoice, *self.startValues.keys())
        self.startTimeMenu.pack(padx=5)

        Label(parent, text="What time does your day end?").pack()

        self.endTimeMenu = OptionMenu(parent, self.endChoice, *self.endValues.keys())
        self.endTimeMenu.pack(padx=5)

        Button(parent, text="OK", command=self.set_settings).pack(pady=5)

    def set_settings(self):
        file = open("settings.txt", "a")
        file.write(str(self.startValues[str(self.startChoice.get())]) + "\n")
        file.write(str(self.endValues[str(self.endChoice.get())]))
        file.close()
        self.parent.destroy()


def pick_date():
    """ Dialog that allows user to change the date displayed"""

    def get_date():
        """Loads picked date"""
        date_shelve = shelve.open("eventStorage.dat")
        for date_key in date_shelve:
            selected = cal.selection_get()
            new_value = date_shelve[date_key].date
            if new_value.month == selected.month and new_value.day == selected.day and new_value.year == selected.year:
                top.destroy()
                date_shelve[date_key].load_date()
                date_shelve.close()
                return

        x = Date((cal.selection_get()))
        date_shelve[str(x.date.year) + str(x.date.month) + str(x.date.day)] = x
        top.destroy()
        x.load_date()
        date_shelve.close()

    top = tk.Toplevel(root)
    top.grab_set()

    cal = Calendar(top, font="Arial 14", selectmode='day', selectforeground="blue", foreground="black")

    cal.pack(fill="both", expand=True)
    tk.Button(top, text="Ok", command=get_date).pack()


def schedule_dialog_main(button):
    """Opens scheduling dialog"""
    d = ScheduleDialog(root, button)
    root.wait_window(d.top)


def settings_dialog_main():
    """ Gets users settings from settings.txt"""
    global start_hour
    global end_hour

    if not path.exists("settings.txt"):
        root = Tk()
        SettingsDialog(root).pack(side="top", fill="both", expand=True)
        root.mainloop()

    settings_file = open("settings.txt", "r")
    start_hour = int(settings_file.readline().rstrip())
    end_hour = int(settings_file.readline())


def main():

    def add_scrollbar(Event):
        """Adds scrollbar for canvas"""
        canvas.configure(scrollregion=canvas.bbox("all"), width=200, height=356)

    settings_dialog_main()

    global root
    global frame

    root = Tk()

    sizex = 225
    sizey = 356
    root.wm_geometry("%dx%d+0+0" % (sizex, sizey))
    root.title("Time Blocker")
    root.resizable(width=False, height=False)

    myframe = Frame(root, relief=GROOVE, width=50, height=100, bd=1)
    myframe.place(x=0, y=0)

    # Add support for scrollbar
    canvas = Canvas(myframe)
    frame = Frame(canvas)
    myscrollbar = Scrollbar(myframe, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=myscrollbar.set)
    myscrollbar.pack(side="right", fill="y")
    canvas.pack(side="left")
    canvas.create_window((0, 0), window=frame, anchor='nw')
    frame.bind("<Configure>", add_scrollbar)

    event_shelve = shelve.open("eventStorage.dat")
    current = datetime.now()
    try:
        event_shelve[str(current.year) + str(current.month) + str(current.day)].load_date()
    except TypeError:
        event_shelve[str(current.year) + str(current.month) + str(current.day)] = Date(datetime.now())
        event_shelve[str(current.year) + str(current.month) + str(current.day)].load_date()
    event_shelve.close()

    root.mainloop()


if __name__ == "__main__":
    main()