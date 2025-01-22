from tkinter import *
from tkinter.font import Font
from math import ceil

class GUIgenerator:
    def __init__(self):
        self.__root = None
        self.__magicNumbers = {"x_pos": 10, "y_pos": 10, "x_pos_const": 10, "y_pos_const": 10, "descriptionPadding": 14, "padding": 30, "default_width": 400, "entry_width": 30,
                               "wrapMargin": 40, "fontSize": 10, "positioningMargins": [8, 10, 20], "button2PlacementHeight": 40, "center2Entry": 25}
        self.__width = 0
        self.__entries = []
        
    def create(self, func, **args):
        if "args" in args.keys():
            self.__root = Tk()
            self.label_font = Font(family="Arial", size=self.__magicNumbers["fontSize"])
            self.__numberOfCharsInArow = self.__maxNumberOfChars(args)
            self.__placeDescription(args)
            self.__generateEntries(args)
            self.__createButtonAndStart(args, func)
        else:
            self.__resultWindow(func())

    def __maxNumberOfChars(self, args):
        max_label_width = max(self.label_font.measure(arg) for arg in args["args"])
        entry_pixel_width = self.__magicNumbers["entry_width"] * self.__magicNumbers["positioningMargins"][0]
        self.__width = (self.__magicNumbers["x_pos"] + max_label_width + self.__magicNumbers["positioningMargins"][1] + entry_pixel_width + self.__magicNumbers["positioningMargins"][2])
        avg_char_width = self.label_font.measure("A")
        return (self.__width - self.__magicNumbers["wrapMargin"]) // avg_char_width

    def __placeDescription(self, args):
        if "desc" in args.keys():
            Label(self.__root, text=args["desc"], font=self.label_font, wraplength=self.__width - self.__magicNumbers["wrapMargin"]).place(x=self.__magicNumbers["x_pos"], y=self.__magicNumbers["y_pos"])
            self.__magicNumbers["y_pos"] += (ceil(len(args["desc"]) / self.__numberOfCharsInArow) * self.__magicNumbers["descriptionPadding"]) + self.__magicNumbers["descriptionPadding"]

    def __generateEntries(self, args):
        for i in args["args"]:
            Label(self.__root, text=i, font=self.label_font).place(x=self.__magicNumbers["x_pos"], y=self.__magicNumbers["y_pos"])
            label_width = self.label_font.measure(i)
            entry_x_pos = (self.__magicNumbers["x_pos"] + label_width + 10)
            entry = Entry(self.__root, width=self.__magicNumbers["entry_width"])
            entry.place(x=entry_x_pos, y=self.__magicNumbers["y_pos"])
            self.__entries.append(entry)
            self.__magicNumbers["y_pos"] += self.__magicNumbers["padding"]

    def __createButtonAndStart(self, args, func):
        button = Button(self.__root, text="Confirm", command=lambda: self.__handleConfirmation(args, func))
        button.place(x=((self.__width - button.winfo_reqwidth()) // 2), y=self.__magicNumbers["y_pos"])
        self.__magicNumbers["y_pos"] += self.__magicNumbers["wrapMargin"]
        
        self.__root.title(func.__name__)
        self.__root.geometry(f"{int(self.__width)}x{self.__magicNumbers['y_pos']}+100+100")
        self.__root.mainloop()

    def __handleConfirmation(self, args, func):
        values = [int(entry.get()) for entry in self.__entries]
        f = func(*values)
        self.__resultWindow(f)

    def addInput(self, arg=""):
        t = Toplevel()
        t.title("Additional input")
        label_font = Font(family="Arial", size=self.__magicNumbers["fontSize"])
        entry_pixel_width = self.__magicNumbers["entry_width"] * self.__magicNumbers["positioningMargins"][0]
        self.__width = (10 + label_font.measure(arg) + entry_pixel_width)
        t.geometry(f"{self.__width}x80+200+200")
        result = ""
        if arg != "":
            Label(t, text=arg, font=label_font).place(x=self.__magicNumbers["x_pos_const"], y=self.__magicNumbers["y_pos_const"])
            label_width = label_font.measure(arg)
            entry_x_pos = (label_width + self.__magicNumbers["padding"])
            entry = Entry(t, width=self.__magicNumbers["entry_width"])
            entry.place(x=entry_x_pos, y=self.__magicNumbers["y_pos_const"])
        else:
            entry = Entry(t, width=self.__magicNumbers["entry_width"])
            entry.place(x=self.__magicNumbers["x_pos_const"]+self.__magicNumbers["center2Entry"], y=self.__magicNumbers["y_pos_const"])

        def confirm():
            nonlocal result
            result = entry.get()
            if len(result) > 0:
                t.destroy()

        button = Button(t, text="Confirm", command=lambda: confirm())
        button.place(x=((self.__width - button.winfo_reqwidth()) // 2), y=self.__magicNumbers["button2PlacementHeight"])
        
        self.__root.wait_window(t)
        return result

    def __resultWindow(self, result):
        __result = Tk()
        __result.title("Result (scroll if necessary)")
        __result.geometry("300x300+200+200")
        frame = Frame(__result)
        frame.pack(expand=True, fill=BOTH)
        text_widget = Text(frame, wrap=WORD, font=("Arial", 10), padx=10, pady=10)
        text_widget.pack(side=LEFT, expand=True, fill=BOTH)
        scrollbar = Scrollbar(frame, command=text_widget.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        text_widget.config(yscrollcommand=scrollbar.set)
        text_widget.insert(END, result)
        text_widget.config(state=DISABLED)
        __result.mainloop()
