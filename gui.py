import tkinter as tk


class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self,parent, *args, **kwargs)
        self.parent = parent

        #gui goes here

        # top menu bar
        menu = tk.Menu(parent)
        parent.config(menu=menu)
        filemenu = tk.Menu(menu)
        menu.add_cascade(label='File', menu=filemenu)
        filemenu.add_command(label='Reset')
        filemenu.add_command(label='Open...')
        filemenu.add_separator()
        filemenu.add_command(label='Exit', command=parent.destroy)
        helpmenu = tk.Menu(menu)
        menu.add_cascade(label='Help', menu=helpmenu)
        helpmenu.add_command(label='Debug')

        # frame
        frametop = tk.Frame(parent)
        frametop.pack(side="top")
        widget = tk.Label(frametop, text="AteBall")
        widget.pack()

        # frame
        frame = tk.Frame(parent)
        frame.pack(side="left")
        redbutton = tk.Button(frame, text='Red', fg='red', width='17', height='5')
        redbutton.pack()
        greenbutton = tk.Button(frame, text='Green', fg='green', width='17', height='5')
        greenbutton.pack()
        bluebutton = tk.Button(frame, text='Blue', fg='blue', width='17', height='5')
        bluebutton.pack()
        yellowbutton = tk.Button(frame, text='Yellow', fg='yellow', width='17', height='5')
        yellowbutton.pack()
        orangebutton = tk.Button(frame, text='Orange', fg='orange', width='17', height='5')
        orangebutton.pack()
        purplebutton = tk.Button(frame, text='Purple', fg='purple', width='17', height='5')
        purplebutton.pack()

        frame2 = tk.Frame(parent)
        frame2.pack(side="right")
        redbutton2 = tk.Button(frame2, text='Red', fg='red', width='17', height='5')
        redbutton2.pack()
        greenbutton2 = tk.Button(frame2, text='Green', fg='green', width='17', height='5')
        greenbutton2.pack()
        bluebutton2 = tk.Button(frame2, text='Blue', fg='blue', width='17', height='5')
        bluebutton2.pack()
        yellowbutton2 = tk.Button(frame2, text='Yellow', fg='yellow', width='17', height='5')
        yellowbutton2.pack()
        orangebutton2 = tk.Button(frame2, text='Orange', fg='orange', width='17', height='5')
        orangebutton2.pack()
        purplebutton2 = tk.Button(frame2, text='Purple', fg='purple', width='17', height='5')
        purplebutton2.pack()


def main():
    root = tk.Tk()
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.resizable(width=False, height=False)
    root.geometry("255x615")
    root.title("8ballbot")
    root.mainloop()

if __name__ == "__main__":
    main()