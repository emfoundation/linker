import linker
import tkinter as tk
from tkinter import filedialog, ttk

class AuthDialog():
    auth = ()
    def __init__(self, parent):
        self.win = tk.Toplevel(parent)
        self.win.wm_title("Authentication Required")

        self.u = tk.Label(self.win, text="Username")
        self.u.grid(row=0, column=0)

        self.auth_user = tk.Entry(self.win)
        self.auth_user.grid(row=0, column=1)

        self.p = tk.Label(self.win, text="Password")
        self.p.grid(row=1, column=0)

        self.auth_pass = tk.Entry(self.win)
        self.auth_pass.grid(row=1, column=1)

        self.b = ttk.Button(self.win, text="Enter", command=self.return_auth)
        self.b.grid(row=2, column=1)

    def return_auth(self):
        print("clicked")
        self.auth = self.auth_user.get(), self.auth_pass.get()
        self.win.destroy()


class LinkerGUI(tk.Frame):
    PAD_X = 25
    PAD_Y = 25
    user = ''
    pswd = ''

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.createWidgets()

    def get_broken_links(self):
        self.results.delete(0,tk.END)
        filename = self.file_input.get()
        if filename != "":
            errors = linker.check_links(filename)
            if errors == 401:
                print("Auth required")
                popup = AuthDialog(self)
                self.wait_window(popup.win)
                auth = popup.auth

                print(auth)
                errors = linker.check_links(filename, auth)

            for url, error, location in errors:
                self.results.insert(tk.END, "===== BROKEN LINK DETECTED ======")
                self.results.insert(tk.END, "Broken Link path: ", url)
                self.results.insert(tk.END, "Error Code: ", error)
                self.results.insert(tk.END, "Location of broken URL: ",location)
                self.results.insert(tk.END, "================================")
                self.results.insert(tk.END, " ")

        else:
            print("No file specified!")

    def browse_file(self):
        self.filename = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("XML Files","*.xml"),("all files","*.*")))
        self.file_input.insert(0, self.filename)

    def createWidgets(self):
        # Set title of window
        self.winfo_toplevel().title("Linker")

        self.title = tk.Label(self, font='Helvetica 18', text="Linker - The broken link finder")
        self.title.grid(row=0, columnspan=3, pady=20)

        self.intro_text = tk.Label(self, font='Helvetica 18', wraplength=600, text="To get started, browse for the file or enter the filename manually (with .xml extension) and click enter. \n The results will be outputted to the terminal immediately, and to a text file + listbox below after")
        self.intro_text.grid(row=1, columnspan=3, rowspan=2, pady=20)

        self.filename_label = tk.Label(self,text="Filename")
        self.filename_label.grid(row=3)

        self.file_input = tk.Entry(self)
        self.file_input.grid(row=3, column=1)
        
        self.results = tk.Listbox(self)
        self.results.config(width=70, height=25)
        self.results.grid(row=4, padx=25, pady=25, column=0, columnspan=3)

        # ====== Buttons ====== #
        # Browse
        self.browse = tk.Button(self)
        self.browse["text"] = "Browse..."
        self.browse["command"] = self.browse_file
        self.browse.grid(row=3, column=2)

        # Quit
        self.QUIT = tk.Button(self, text="QUIT", fg="red", command=self.quit)
        self.QUIT.grid(row=5, pady=10, column=0)

        # Enter
        self.enter = tk.Button(self)
        self.enter["text"] = "Enter"
        self.enter["command"] = self.get_broken_links
        self.enter.grid(row=5, pady=10, column=2)


def run():
    root = tk.Tk()
    app = LinkerGUI(master=root)
    app.mainloop()