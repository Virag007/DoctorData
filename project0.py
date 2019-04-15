#Book an appointment
import win32console
import win32gui
win=win32console.GetConsoleWindow()       
win32gui.ShowWindow(win,0)
from tkinter import *
import re
import backend
import random
import csv
from collections import defaultdict

def add_command():
    r.destroy()
    o=Tk()
    o.iconbitmap("./images/py.ico")
    o.title("Token")
    canvas = Canvas(o, height=250, width=270,bg="#ffffff",highlightthickness=0)
    canvas.pack()
    s=Label(o,font='Garamond 14 bold',bg="#ffffff")
    s.place(x=70,y=70)
    token="DD-"+str(random.randint(1000000,9999999))
    s.config(text="YOUR TOKEN:\n\n"+token)    
    o.resizable(width=False, height=False)
    o.mainloop()
    backend.insert(token,doctor.get(),name.get(),email.get(),age.get(),gender.get(),phone.get(),address.get())

try:
    from Tkinter import StringVar, Entry, Frame, Listbox, Scrollbar
    from Tkconstants import *
except ImportError:
    from tkinter import StringVar, Entry, Frame, Listbox, Scrollbar
    from tkinter.constants import *


def autoscroll(sbar, first, last):
    """Hide and show scrollbar as needed."""
    first, last = float(first), float(last)
    if first <= 0 and last >= 1:
        sbar.grid_remove()
    else:
        sbar.grid()
    sbar.set(first, last)


class Combobox_Autocomplete(Entry, object):
    def __init__(self, master, list_of_items=None, autocomplete_function=None, listbox_width=None, listbox_height=7, ignorecase_match=False, startswith_match=True, vscrollbar=True, hscrollbar=True, **kwargs):
        if hasattr(self, "autocomplete_function"):
            if autocomplete_function is not None:
                raise ValueError("Combobox_Autocomplete subclass has 'autocomplete_function' implemented")
        else:
            if autocomplete_function is not None:
                self.autocomplete_function = autocomplete_function
            else:
                if list_of_items is None:
                    raise ValueError("If not guiven complete function, list_of_items can't be 'None'")

                if ignorecase_match:
                    if startswith_match:
                        def matches_function(entry_data, item):
                            return item.startswith(entry_data)
                    else:
                        def matches_function(entry_data, item):
                            return item in entry_data

                    self.autocomplete_function = lambda entry_data: [item for item in self.list_of_items if matches_function(entry_data, item)]
                else:
                    if startswith_match:
                        def matches_function(escaped_entry_data, item):
                            if re.match(escaped_entry_data, item, re.IGNORECASE):
                                return True
                            else:
                                return False
                    else:
                        def matches_function(escaped_entry_data, item):
                            if re.search(escaped_entry_data, item, re.IGNORECASE):
                                return True
                            else:
                                return False
                    
                    def autocomplete_function(entry_data):
                        escaped_entry_data = re.escape(entry_data)
                        return [item for item in self.list_of_items if matches_function(escaped_entry_data, item)]

                    self.autocomplete_function = autocomplete_function

        self._listbox_height = int(listbox_height)
        self._listbox_width = listbox_width

        self.list_of_items = list_of_items
        
        self._use_vscrollbar = vscrollbar
        self._use_hscrollbar = hscrollbar

        kwargs.setdefault("background", "white")

        if "textvariable" in kwargs:
            self._entry_var = kwargs["textvariable"]
        else:
            self._entry_var = kwargs["textvariable"] = StringVar()

        Entry.__init__(self, master, **kwargs)

        self._trace_id = self._entry_var.trace('w', self._on_change_entry_var)
        
        self._listbox = None

        self.bind("<Tab>", self._on_tab)
        self.bind("<Up>", self._previous)
        self.bind("<Down>", self._next)
        self.bind('<Control-n>', self._next)
        self.bind('<Control-p>', self._previous)

        self.bind("<Return>", self._update_entry_from_listbox)
        self.bind("<Escape>", lambda event: self.unpost_listbox())
        
    def _on_tab(self, event):
        self.post_listbox()
        return "break"

    def _on_change_entry_var(self, name, index, mode):
        
        entry_data = self._entry_var.get()

        if entry_data == '':
            self.unpost_listbox()
            self.focus()
        else:
            values = self.autocomplete_function(entry_data)
            if values:
                if self._listbox is None:
                    self._build_listbox(values)
                else:
                    self._listbox.delete(0, END)

                    height = min(self._listbox_height, len(values))
                    self._listbox.configure(height=height)

                    for item in values:
                        self._listbox.insert(END, item)
                
            else:
                self.unpost_listbox()
                self.focus()

    def _build_listbox(self, values):
        listbox_frame = Frame()

        self._listbox = Listbox(listbox_frame, background="white", selectmode=SINGLE, activestyle="none", exportselection=False)
        self._listbox.grid(row=0, column=0,sticky = N+E+W+S)

        self._listbox.bind("<ButtonRelease-1>", self._update_entry_from_listbox)
        self._listbox.bind("<Return>", self._update_entry_from_listbox)
        self._listbox.bind("<Escape>", lambda event: self.unpost_listbox())
        
        self._listbox.bind('<Control-n>', self._next)
        self._listbox.bind('<Control-p>', self._previous)

        if self._use_vscrollbar:
            vbar = Scrollbar(listbox_frame, orient=VERTICAL, command= self._listbox.yview)
            vbar.grid(row=0, column=1, sticky=N+S)
            
            self._listbox.configure(yscrollcommand= lambda f, l: autoscroll(vbar, f, l))
            
        if self._use_hscrollbar:
            hbar = Scrollbar(listbox_frame, orient=HORIZONTAL, command= self._listbox.xview)
            hbar.grid(row=1, column=0, sticky=E+W)
            
            self._listbox.configure(xscrollcommand= lambda f, l: autoscroll(hbar, f, l))

        listbox_frame.grid_columnconfigure(0, weight= 1)
        listbox_frame.grid_rowconfigure(0, weight= 1)

        x = -self.cget("borderwidth") - self.cget("highlightthickness") 
        y = self.winfo_height()-self.cget("borderwidth") - self.cget("highlightthickness")

        if self._listbox_width:
            width = self._listbox_width
        else:
            width=self.winfo_width()

        listbox_frame.place(in_=self, x=x, y=y, width=width)
        
        height = min(self._listbox_height, len(values))
        self._listbox.configure(height=height)

        for item in values:
            self._listbox.insert(END, item)

    def post_listbox(self):
        if self._listbox is not None: return

        entry_data = self._entry_var.get()
        if entry_data == '': return

        values = self.autocomplete_function(entry_data)
        if values:
            self._build_listbox(values)

    def unpost_listbox(self):
        if self._listbox is not None:
            self._listbox.master.destroy()
            self._listbox = None

    def get_value(self):
        return self._entry_var.get()

    def set_value(self, text, close_dialog=False):
        self._set_var(text)

        if close_dialog:
            self.unpost_listbox()

        self.icursor(END)
        self.xview_moveto(1.0)
        
    def _set_var(self, text):
        self._entry_var.trace_vdelete("w", self._trace_id)
        self._entry_var.set(text)
        self._trace_id = self._entry_var.trace('w', self._on_change_entry_var)

    def _update_entry_from_listbox(self, event):
        if self._listbox is not None:
            current_selection = self._listbox.curselection()
            
            if current_selection:
                text = self._listbox.get(current_selection)
                self._set_var(text)

            self._listbox.master.destroy()
            self._listbox = None

            self.focus()
            self.icursor(END)
            self.xview_moveto(1.0)
            
        return "break"

    def _previous(self, event):
        if self._listbox is not None:
            current_selection = self._listbox.curselection()

            if len(current_selection)==0:
                self._listbox.selection_set(0)
                self._listbox.activate(0)
            else:
                index = int(current_selection[0])
                self._listbox.selection_clear(index)

                if index == 0:
                    index = END
                else:
                    index -= 1

                self._listbox.see(index)
                self._listbox.selection_set(first=index)
                self._listbox.activate(index)

        return "break"

    def _next(self, event):
        if self._listbox is not None:

            current_selection = self._listbox.curselection()
            if len(current_selection)==0:
                self._listbox.selection_set(0)
                self._listbox.activate(0)
            else:
                index = int(current_selection[0])
                self._listbox.selection_clear(index)
                
                if index == self._listbox.size() - 1:
                    index = 0
                else:
                    index +=1
                    
                self._listbox.see(index)
                self._listbox.selection_set(index)
                self._listbox.activate(index)
        return "break"

if __name__ == '__main__':
    try:
        from Tkinter import Tk
    except ImportError:
        from tkinter import Tk
        
        
    columns = defaultdict(list)

    with open("./data/doctor_data.csv") as f:
        reader = csv.DictReader(f) # read rows into a dictionary format
        for row in reader: # read a row as {column1: value1, column2: value2,...}
            for (k,v) in row.items(): # go over each column name and value 
                columns[k].append(v)

    r = Tk()
    r.iconbitmap("./images/py.ico")
    r.title("Book")
    canvas = Canvas(r, height=550, width=560,bg="#ffffff",highlightthickness=0)
    canvas.pack()
    
    aa=Canvas(r, bg="#ff1a75", height=11, width=115,highlightthickness=0)
    aa.place(x=0,y=0)
    bb=Canvas(r, bg="#b3b300", height=11, width=115,highlightthickness=0)
    bb.place(x=110,y=0)
    xx=Canvas(r, bg="#ff471a", height=11, width=115,highlightthickness=0)
    xx.place(x=220,y=0)
    yy=Canvas(r, bg="#39ac39", height=11, width=115,highlightthickness=0)
    yy.place(x=335,y=0)
    zz=Canvas(r, bg="#4dd2ff", height=11, width=115,highlightthickness=0)
    zz.place(x=450,y=0)
    pp=Canvas(r, bg="#adad85", height=11, width=115,highlightthickness=0)
    pp.place(x=730,y=0)
      
    pop1=Label(r,text="Enter Doctor name",font='Garamond 14 bold',fg="#00134d",bg="#ffffff")
    pop1.place(x=20,y=50)
    doctor=StringVar()
    pop2 = Combobox_Autocomplete(r, columns['name'], highlightthickness=1,font='Garamond 13',textvariable=doctor)
    pop2.focus()
    pop2.place(x=270,y=50,width=250,height=30)
    pop3=Label(r,text="Patient Details",font='Garamond 14 bold',fg="#00134d",bg="#ffffff")
    pop3.place(x=20,y=120)
    
    a=Canvas(r, bg="#5c8a8a", height=1, width=520,highlightthickness=0)
    a.place(x=20,y=160)
    b=Canvas(r, bg="#5c8a8a", height=1, width=520,highlightthickness=0)
    b.place(x=20,y=440)
    c=Canvas(r, bg="#5c8a8a", height=280, width=1,highlightthickness=0)
    c.place(x=20,y=160)
    d=Canvas(r, bg="#5c8a8a", height=280, width=1,highlightthickness=0)
    d.place(x=540,y=160)
    
    pop4=Label(r,text="Patient name",font='Helvetica 11 bold',bg="#ffffff")
    pop4.place(x=35,y=180)
    name=StringVar()
    pop5=Entry(r,bg="#ffffff",textvariable=name)
    pop5.place(x=270,y=180,width=250,height=22)
    pop6=Label(r,text="Email",font='Helvetica 11 bold',bg="#ffffff")
    pop6.place(x=35,y=220)
    email=StringVar()
    pop7=Entry(r,bg="#ffffff",textvariable=email)
    pop7.place(x=270,y=220,width=250,height=22)
    pop8=Label(r,text="Age",font='Helvetica 11 bold',bg="#ffffff")
    pop8.place(x=35,y=260)
    age=StringVar()
    pop9=Entry(r,bg="#ffffff",textvariable=age)
    pop9.place(x=270,y=260,width=250,height=22)
    pop10=Label(r,text="Gender",font='Helvetica 11 bold',bg="#ffffff")
    pop10.place(x=35,y=310)
    gender=StringVar()
    pop11=Radiobutton(r,text="Male",font='Helvetica 11 bold',bg="#ffffff",value="Male",variable=gender)
    pop11.place(x=290,y=310)
    pop12=Radiobutton(r,text="Female",font='Helvetica 11 bold',bg="#ffffff",value="Female",variable=gender)
    pop12.place(x=410,y=310)
    pop13=Label(r,text="Contact Number",font='Helvetica 11 bold',bg="#ffffff")
    pop13.place(x=35,y=360)
    phone=StringVar()
    pop14=Entry(r,bg="#ffffff",textvariable=phone)
    pop14.place(x=270,y=360,width=250,height=22)
    pop15=Label(r,text="Address",font='Helvetica 11 bold',bg="#ffffff")
    pop15.place(x=35,y=400)
    address=StringVar()
    pop16=Entry(r,bg="#ffffff",textvariable=address)
    pop16.place(x=270,y=400,width=250,height=22)
    
    pop17=Button(r,text="Book",font='Garamond 14 bold',height=1,width=10,highlightthickness=0,relief=FLAT,bd=3,bg="#00b33c",fg='#ffffff',cursor="hand2",command=add_command)
    pop17.place(x=230,y=480)
    
    r.resizable(width=False, height=False)
    r.mainloop()
    