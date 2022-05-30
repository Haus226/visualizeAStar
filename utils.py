from csv import reader
from config import COLOR, DEFAULT_RECORD
from tkinter import messagebox, ttk
from tkinter import *

def savePrevColor(filename="prevColor.csv"):
    with open(f"{filename}", "w+") as file:
        for color in COLOR:
            file.write(f"{color}, {COLOR[color]}\n")

def readPrevColor(filename="prevColor.csv"):

    try:
        print(filename)
        with open(f"{filename}", "r") as file:
            record = reader(file)
            for r in record:
                # print(r)
                COLOR[f"{r[0]}"] = r[1].strip()
            # print(COLOR)
        return True
    except FileNotFoundError:
        messagebox.showerror("File not found !", "The file that record previous colour is not found, GUI will display the default colour.")
        COLOR.update(DEFAULT_RECORD)
        return False

def focus(e, win, widgets, dir):
    cur = int(win.focus_get().winfo_name())
    if cur >= 0:
        if dir == "up":
            widgets[cur - 1].focus_set()
        elif dir == "down":
            if cur != 3:
                widgets[cur + 1].focus_set()
            else:
                widgets[0].focus_set()

def destroy_(e, win):
    win.destroy()

def resizeDialog(master):
    window = Toplevel(master)
    tempFrame = Frame(window)
    tempFrame.pack()
    r_c_s, text, widget = [StringVar(), StringVar(), StringVar()], ["Row Numbers", "Column Numbers", "Cell Size"], []
    for cnt in range(3):
        Label(tempFrame, text=text[cnt], font=("Aerial", 12)).grid(row=cnt, column=0)
        entry = Entry(tempFrame, textvariable=r_c_s[cnt], font=("Aerial", 12), name=f"{cnt}")
        entry.grid(row=cnt, column=1)
        widget.append(entry)
    confirm = ttk.Button(window, text="Resize", command=window.destroy, name="3")
    confirm.pack()
    widget.append(confirm)
    for w in widget:
        w.bind("<Up>", lambda e: focus(e, window, widget, "up"))
        w.bind("<Down>", lambda e: focus(e, window, widget, "down"))
        w.bind("<Return>", lambda e: focus(e, window, widget, "down"))
    confirm.bind("<Return>", lambda e: destroy_(e, window))
    widget[0].focus_set()
    window.wait_window()
    return r_c_s

if __name__ == '__main__':
    if not 2 & 1:
        print(0)