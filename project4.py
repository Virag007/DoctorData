#Main objective of software-search doctor by symptoms
import win32console
import win32gui
win=win32console.GetConsoleWindow()       
win32gui.ShowWindow(win,0)
from tkinter import *
import csv
import re
from collections import defaultdict
import numpy as np  #library is used for making array of multiple dimension
import geopy.distance
import geocoder
from tkinter.scrolledtext import ScrolledText

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


co = defaultdict(list)
with open("./data/disease_pred.csv") as f:
    reader = csv.DictReader(f) # read rows into a dictionary format
    for row in reader: # read a row as {column1: value1, column2: value2,...}
        for (k,v) in row.items(): # go over each column name and value 
            co[k].append(v)

e1=co['symptoms_list']
for i in range(len(e1)):
    e1[i] = e1[i].split(",")

root=Tk()
root.iconbitmap("./images/py.ico")
root.title("Search")

canvas = Canvas(root, height=400, width=640,bg="#ffffff",highlightthickness=0)
canvas.pack()
my_image = PhotoImage(file="./images/mapC.png")
canvas.create_image(320, 200, image=my_image)

my=StringVar()
com=Combobox_Autocomplete(root,e1[0],textvariable=my,font='Helvetica 11')
com.focus()
com.place(x=300,y=15,height=25,width=240)

def add():
    sym=my.get()
    if(sym!=''):
        text.insert(INSERT,sym)
        text.insert(INSERT,',')
    com.delete(0, END)
    
def get():
    p=text.get("1.0", "end-1c")
    text.delete(1.0,END)
    text1.delete(1.0,END)
    p=p.split(",")
    symp=['']*(len(p)-1)
    for i in range(len(p)-1):
        symp[i]=p[i]
        
    co = defaultdict(list)
    with open("./data/disease_pred.csv") as f:
        reader = csv.DictReader(f) # read rows into a dictionary format
        for row in reader: # read a row as {column1: value1, column2: value2,...}
            for (k,v) in row.items(): # go over each column name and value 
                co[k].append(v)
    
    ip=symp
    e1=co['symptoms']
    e3=co['specialty']
    le=[0]*len(e1)
    le1=[0]*len(e1)
    q=0
    q1=0
    count=0
    same=0
    out=''
    
    for i in range(len(e1)):
        e1[i] = e1[i].split(",")
    
    for i in range(len(e1)):
        a=set(e1[i])
        b=set(ip).issubset(a)
        if(b==True):
            le[i]=len(e1[i])
            q+=1
            
    sor=[index for index, num in sorted(enumerate(le), key=lambda z: z[-1])]
    if(len(ip)==1 or len(ip)==2):
        out='General Medicine'
    elif(len(ip)==0):
        text1.insert(INSERT,' Enter the symptoms first','get1')
        text1.tag_config('get1', font='Garamond 14 bold', foreground='green')
    elif(q!=0):
        if(q==1):
            out=e3[sor[len(le)-q]]
        elif(le[sor[len(le)-q]]==le[sor[len(le)+1-q]]):
            out='General Medicine'  
        else:
            out=e3[sor[len(le)-q]]
    else:
        for j in range(len(ip)):
            for i in range(len(e1)):
                d=set(e1[i])
                e=set([ip[j]]).issubset(d)
                if(e==True):
                    le1[i]+=1
                    q1+=1
        for i in range(len(le1)):
            if(le1[i]!=0):
                count+=1
        sor1=[index for index, num in sorted(enumerate(le1), key=lambda v: v[-1])]
        max=le1[sor1[len(sor1)-1]]
        if(q1!=0):
            if(le1[sor1[len(le1)-1]]==le1[sor1[len(le)-2]]):
                for i in range(count):
                    st=le1[sor1[len(le1)-1]]
                    st1=le1[sor1[len(le1)-count+i]]
                    if(st==st1):
                        same+=1
                        le1[sor1[len(le1)-count+i]]=len(e1[sor1[len(le1)-count+i]])
                sor2=[index for index, num in sorted(enumerate(le1), key=lambda w: w[-1])]
                if(q1==1):
                    out=e3[sor2[len(le1)-same]]
                elif(max==1 or max==2):
                    out='General Medicine'
                elif(le1[sor2[len(le1)-same]]==le1[sor2[len(le1)+1-same]]):
                    out='General Medicine'
                else:
                    out=e3[sor2[len(le1)-same]]
            else:
                out=e3[sor1[len(le1)-1]]
    
    spec=out 
    columns = defaultdict(list)
    with open("./data/doctor_data.csv") as f:
        reader = csv.DictReader(f) # read rows into a dictionary format
        for row in reader: # read a row as {column1: value1, column2: value2,...}
            for (k,v) in row.items(): # go over each column name and value 
                columns[k].append(v)
    
    ra = defaultdict(list)
    with open("./data/rating.csv") as f:
        reader = csv.DictReader(f) # read rows into a dictionary format
        for row in reader: # read a row as {column1: value1, column2: value2,...}
            for (k,v) in row.items(): # go over each column name and value 
                ra[k].append(v)
    
    r1=ra['rating_avg']
    for i in range(len(r1)):
        r1[i] = r1[i].split(",")                         
    for i in range(len(r1)):
        r1[i][0]=float(r1[i][0])
        r1[i][1]=int(r1[i][1])
    
    col0=np.array(columns['name'])  #1-D array containing data of all doctor names in csv file
    avg=[0]*(len(col0))
    val=[0]*(len(col0))
    val1=[0]*(len(col0))
    c=0
    col=np.array(columns['specialty'])  #1-D array containig all doctor's speciality in csv file
    col6=np.array(columns['address'])
    col7=np.array(columns['phone'])
    col8=np.array(columns['email'])
    col9=np.array(columns['gender'])
    col10=np.array(columns['website'])
    col11=np.array(columns['title'])
    ss=np.array(columns['summary'])
    long=np.array(columns['loc_lon'],dtype=float)
    lat=np.array(columns['loc_lat'],dtype=float)
    
    g=geocoder.ip('me')
    mycoord=g.latlng
    
    for i in range(len(col)):
        avg[i]=r1[i][0]  #calculating average of all rating columns
    
    for i in range(len(col)):
        if spec in col[i]:  #condition if input speciality is matched with csv file doctor speciality
            val[i]=avg[i]
            mycoord1=(lat[i], long[i])
            val1[i]=geopy.distance.vincenty(mycoord, mycoord1).km
            c+=1
    if(c==0):
        text1.insert(INSERT,' No results found!!','get')
        text1.tag_config('get', font='Garamond 14 bold', foreground='green')
    j=len(col)
    t=j
    t1=c
    if(len(spec)==0):
        c=0
    #Sort array and return original indexes of sorted array
    sorted_index_pos = [index for index, num in sorted(enumerate(val), key=lambda x: x[-1])]
    sorted_index_pos_loc = [index for index, num in sorted(enumerate(val1), key=lambda y: y[-1])]
    while(c!=0): 
        if((val[sorted_index_pos[t-1]]==val[sorted_index_pos[j-1]]) and val1[sorted_index_pos_loc[t-t1]]==val1[sorted_index_pos_loc[t-c]]): #highest rating doctor results with specific speciality
            text1.insert(INSERT,"Your Best Predicted Doctor:-----",'front')
            text1.tag_config('front', font='Garamond 14 bold', foreground='blue')
            text1.insert(INSERT,"\n")
            text1.insert(INSERT,'\nDoctor Name: \t','de')
            text1.tag_config('de', font='Garamond 13 bold')
            text1.insert(INSERT,col0[sorted_index_pos_loc[t-c]],'demo')
            text1.tag_config('demo', font='Garamond 13 bold', foreground='red')
            text1.insert(INSERT,'\n')
            text1.insert(INSERT,'Gender: \t')
            text1.insert(INSERT,col9[sorted_index_pos_loc[t-c]])
            text1.insert(INSERT,'\tDegree: \t')
            text1.insert(INSERT,col11[sorted_index_pos_loc[t-c]])
            text1.insert(INSERT,'\tRating: \t')
            text1.insert(INSERT,avg[sorted_index_pos_loc[t-c]])
            text1.insert(INSERT,"\n")
            text1.insert(INSERT,"Phone: \t")
            text1.insert(INSERT,col7[sorted_index_pos_loc[t-c]])
            text1.insert(INSERT,"\n")
            text1.insert(INSERT,"Speciality: \t")
            text1.insert(INSERT,col[sorted_index_pos_loc[t-c]])
            text1.insert(INSERT,"\n")
            text1.insert(INSERT,"Email: \t")
            text1.insert(INSERT,col8[sorted_index_pos_loc[t-c]])
            text1.insert(INSERT,"\n")
            text1.insert(INSERT,"Website: \t")
            text1.insert(INSERT,col10[sorted_index_pos_loc[t-c]])
            text1.insert(INSERT,"\n")
            text1.insert(INSERT,"Address: \t")
            text1.insert(INSERT,col6[sorted_index_pos_loc[t-c]])
            text1.insert(INSERT,"\n")
            text1.insert(INSERT,"Profile: \t")
            text1.insert(INSERT,ss[sorted_index_pos_loc[t-c]])
            text1.insert(INSERT,"\n")
            c-=1
            j-=1
        else:
            break
    
button=Button(root,text="ADD",font='Helvetica 9 bold',bg="#00b33c",relief=FLAT,fg='#ffffff',cursor="hand2",command=add)
button.place(x=550,y=14,height=25,width=60)
button1=Button(root,text='FIND DOCTOR',font='Helvetica 9 bold',relief=FLAT,fg='#ffffff',bg="#00b33c",cursor="hand2",command=get)
button1.place(x=240,y=140,height=25,width=160)
text=Text(root,bd=2,relief=GROOVE,font='Helvetica 11',fg="red")
text.place(x=120,y=60,height=60,width=410)
text1=ScrolledText(root,bg="#ffffff")
text1.place(x=0,y=185,width=640,height=215)

root.resizable(width=False, height=False)  
root.mainloop()