#Rate your doctor
import win32console
import win32gui
win=win32console.GetConsoleWindow()       
win32gui.ShowWindow(win,0)
import csv
import re
from collections import defaultdict
from tkinter import *

d='☆'
e='★'
c=[0]

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


co=defaultdict(list)
with open("./data/doctor_data.csv") as f:
    reader=csv.DictReader(f) # read rows into a dictionary format
    for row in reader: # read a row as {column1: value1, column2: value2,...}
        for (k,v) in row.items(): # go over each column name and value 
            co[k].append(v)

doc_name=co['name']
root = Tk()
root.iconbitmap("./images/py.ico")
root.title("Feedback")
canvas = Canvas(root, height=280, width=390,highlightthickness=0,bg="#006699")
canvas.pack()
label=Label(root,text="RATE DOCTOR",font=18,bg="#006699",fg='#ffffff').place(x=140,y=15)

my=StringVar()
com=Combobox_Autocomplete(root,co['name'],textvariable=my,font='Helvetica 11')
com.focus()
com.place(x=80,y=60,height=25,width=240)
text=Label(root,relief=FLAT).place(x=0,y=120,height=200,width=390)

def get(c):
    btn.config(text=d,fg='black')
    btn1.config(text=d,fg='black')
    btn2.config(text=d,fg='black')
    btn3.config(text=d,fg='black')
    btn4.config(text=d,fg='black')
    btn.config(text=e,fg='#ff751a')
    c[0]=1
               
def get1(c):
    btn.config(text=d,fg='black')
    btn1.config(text=d,fg='black')
    btn2.config(text=d,fg='black')
    btn3.config(text=d,fg='black')
    btn4.config(text=d,fg='black')
    btn.config(text=e,fg='#ff751a')
    btn1.config(text=e,fg='#ff751a')
    c[0]=2
               
def get2(c):
    btn.config(text=d,fg='black')
    btn1.config(text=d,fg='black')
    btn2.config(text=d,fg='black')
    btn3.config(text=d,fg='black')
    btn4.config(text=d,fg='black')
    btn.config(text=e,fg='#ff751a')
    btn1.config(text=e,fg='#ff751a')
    btn2.config(text=e,fg='#ff751a')
    c[0]=3

def get3(c):
    btn.config(text=d,fg='black')
    btn1.config(text=d,fg='black')
    btn2.config(text=d,fg='black')
    btn3.config(text=d,fg='black')
    btn4.config(text=d,fg='black')
    btn.config(text=e,fg='#ff751a')
    btn1.config(text=e,fg='#ff751a')
    btn2.config(text=e,fg='#ff751a')
    btn3.config(text=e,fg='#ff751a')
    c[0]=4

def get4(c):
    btn.config(text=d,fg='black')
    btn1.config(text=d,fg='black')
    btn2.config(text=d,fg='black')
    btn3.config(text=d,fg='black')
    btn4.config(text=d,fg='black')
    btn.config(text=e,fg='#ff751a')
    btn1.config(text=e,fg='#ff751a')
    btn2.config(text=e,fg='#ff751a')
    btn3.config(text=e,fg='#ff751a')
    btn4.config(text=e,fg='#ff751a')  
    c[0]=5
            
    
btn=Button(root,text=d,font=15, borderwidth=0, relief=SUNKEN,command=lambda: get(c))
btn.place(x=147,y=145)
btn1=Button(root,text=d,font=15, borderwidth=0, relief=SUNKEN,command=lambda: get1(c))
btn1.place(x=167,y=145)
btn2=Button(root,text=d,font=15, borderwidth=0, relief=SUNKEN,command=lambda: get2(c))
btn2.place(x=187,y=145)
btn3=Button(root,text=d,font=15, borderwidth=0, relief=SUNKEN,command=lambda: get3(c))
btn3.place(x=207,y=145)
btn4=Button(root,text=d,font=15, borderwidth=0, relief=SUNKEN,command=lambda: get4(c))
btn4.place(x=227,y=145)

def submit(c):
    a=my.get()
    for i in range(len(doc_name)):
        if(doc_name[i]==a):
            co = defaultdict(list)
            with open("./data/rating.csv") as f:
                reader = csv.DictReader(f) 
                for row in reader:
                    for (k,v) in row.items():
                        co[k].append(v)             
            r1=co['rating_avg']
            for j in range(len(r1)):
                r1[j]=r1[j].split(",")
            for j in range(len(r1)):
                r1[j][0]=float(r1[j][0])
                r1[j][1]=int(r1[j][1])
            
            r1[i][0]=r1[i][0]*r1[i][1]
            r1[i][1]+=1
            r1[i][0]=(r1[i][0]+float(c[0]))/r1[i][1]
            for i in range(len(r1)):
                x=","+str(r1[i][1])
                r1[i]=str(r1[i][0])+x
               
            with open("./data/rating.csv", 'w') as fout:
                writer = csv.writer(fout, lineterminator='\n')
                writer.writerow(['rating_avg'])
                for val in r1:
                    writer.writerow([val])
    root.destroy()

button=Button(root,text='SUBMIT',font='Helvetica 10 bold',bg="#00b33c",relief=FLAT,fg='#ffffff',cursor="hand2",command=lambda: submit(c)).place(x=150,y=220,height=25,width=100)
root.resizable(width=False, height=False)  
root.mainloop()