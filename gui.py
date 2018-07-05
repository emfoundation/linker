import linker
import tkinter as tk

class Application(tk.Frame):
    PAD_X = 25
    PAD_Y = 25
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        self.filename = tk.Label(self,text="Filename")
        self.filename.grid(row=0)

        self.file_input = tk.Entry(self)
        self.file_input.grid(row=0, column=1)

        self.enter = tk.Button(self)
        self.enter["text"] = "Enter"
        self.enter["command"] = lambda: linker.check_links(self.file_input.get())
        self.enter.grid(row=1, column=0)

        self.QUIT = tk.Button(self, text="QUIT", fg="red",
                                            command=self.quit)
        self.QUIT.grid(row=1, column=1)                                   

def run():
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()