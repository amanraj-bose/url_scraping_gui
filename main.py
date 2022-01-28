from requests import get
from bs4 import BeautifulSoup
from re import compile
from tkinter import *
from tkinter import messagebox
import urllib
from urllib.request import urlopen


class gui(Tk):
    def __init__(self):
        super().__init__()
        self.geometry("500x500")
        self.title("URL Scraping")
        self.config(bg="#02060a")
        self.resizable(False, False)
    def connection(self) -> None:
        try:
            urlopen("https://www.google.com/", timeout=5)
            return True
        except urllib.error.URLError:
            return False

    def Status(self) -> None:
        self.Root_Status = StringVar()
        if self.connection():
            self.Root_Status.set("Internet Connection Available !!")
        else:
            self.Root_Status.set("Internet Connection Failed")
            messagebox.showerror("Error", "Internet Connection Failed")
        self.Status_Label = Label(
            self, textvar=self.Root_Status, fg="magenta", anchor="w", bg="#000")
        self.Status_Label.pack(side=BOTTOM, fill=X)

    def cleanup(self) -> None:
        self.Frame_Url.destroy()
    def write_txt(self):
        with open('links.txt', 'wt') as f:
            for text in self.link.get('href'):
                f.writelines(text)
    def clean_button(self) -> None:
        self.menu = Menu(self)
        self.Options = Menu(self.menu, tearoff=0)
        self.Options.add_command(
            label="Cleaning", command=self.cleanup, foreground="cyan", background="black")
        self.Options.add_command(label="Write", command=self.write_txt,foreground="cyan",background="black")
        self.Options.add_separator()
        self.Options.add_command(
            label="Exit", command=quit, foreground="magenta", background="black")
        self.menu.add_cascade(label="Options", menu=self.Options)
        self.config(menu=self.menu)

    def main(self) -> None:
        self.Frame = Frame(self, bg="#02060a", bd=0)
        self.Frame.pack(side=TOP, fill=X, padx=5)
        self.Label = Label(self.Frame, text="URL : ", bd=0, fg="cyan",
                           bg="#02060a", relief=RAISED, font=('ds-digital', 20))
        self.Label.pack(side=LEFT, padx=5)
        self.input = Entry(self.Frame, bg="#fff", fg="black",
                           bd=0, relief=RAISED, font=('ds-digital', 20))
        self.input.pack(padx=20, pady=10, side=LEFT, fill=X)
        self.confirmButton = Button(self.Frame, text="Submit", fg="#000", bg="green",
                                    relief=RAISED, bd=0, command=self.code, font=('ds-digital', 10))
        self.confirmButton.pack(side=LEFT, anchor=W)

    def code(self) -> None:
        self.Frame_Url = Frame(self, bg="#062f58", bd=0,
                               height=1000, width=1000)
        self.Frame_Url.pack(side=TOP, fill=X, padx=5, pady=20)
        self.r = get(str(self.input.get()))
        self.html = self.r.content
        self.soup = BeautifulSoup(self.html, 'html.parser')
        self.url_data = self.soup.find_all(
            'a', attrs={'href': compile(r"^https://")})
        self.scrollbar = Scrollbar(self.Frame_Url,orient=VERTICAL, background="#000")
        self.scrollbar.pack(fill=Y, side=RIGHT)
        self.scrollbar_X = Scrollbar(self.Frame_Url,orient=HORIZONTAL, background="#000")
        self.scrollbar_X.pack(fill=X, side=BOTTOM)
        self.List_url = Listbox(self.Frame_Url, fg="#fff", bg="#062f58", relief=RAISED, font=(
            'ds-digital', 20), bd=0, yscrollcommand=self.scrollbar.set,xscrollcommand=self.scrollbar_X)
        for self.link in self.url_data:
            self.List_url.insert(END, self.link.get('href'))
        self.List_url.pack(side=TOP, fill=X, padx=5)
        self.scrollbar.config(command=self.List_url.yview)
        self.scrollbar_X.config(command=self.List_url.xview)

    def __main__(self) -> None:
        self.main()
        self.clean_button()
        self.Status()


if __name__ == '__main__':
    op = gui()
    op.__main__()
    op.mainloop()
