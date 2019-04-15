#Check your booking status
import win32console
import win32gui
win=win32console.GetConsoleWindow()       
win32gui.ShowWindow(win,0)
import sqlite3
from tkinter import *

r = Tk()
r.iconbitmap("./images/py.ico")
r.title("Check Status")
canvas = Canvas(r, height=530, width=560,bg="#006699",highlightthickness=0)
canvas.pack()
my=StringVar()
label=Label(r,text="ENTER YOUR TOKEN",bg="#006699",fg='#ffffff',font='Helvetica 19 bold').place(x=145,y=10)
entry=Entry(r,textvariable=my,font='Helvetica 15',relief=FLAT)
entry.place(x=185,y=60,height=25,width=190)

def get_status():
    p=my.get()
    entry.delete(0,END)
    conn = sqlite3.connect("appointment.db")
    cur = conn.cursor()
    t=['']*3
    i=0
    c=0
    cur.execute("SELECT * FROM appointment")
    rows = cur.fetchall()
    for row in rows:
        t[i]=row
        i+=1
        
    for j in range(i):
        for k in range(len(t[j])):
            if(t[j][k]==p):
                text.delete(1.0,END)
                text.tag_configure("center", justify='center')
                text.insert(INSERT,'TOKEN NUMBER:   ','front')
                text.insert(INSERT,t[j][1],'front')
                text.tag_add("center", "1.0")
                text.insert(INSERT,'\n\n')
                text.insert(INSERT,'DOCTOR NAME:   ','front')
                text.insert(INSERT,t[j][2],'front')
                text.tag_add("center", "3.0")
                text.insert(INSERT,'\n\n')
                text.insert(INSERT,'PATIENT NAME:   ','front')
                text.insert(INSERT,t[j][3],'front')
                text.tag_add("center", "5.0")
                text.insert(INSERT,'\n\n')
                text.insert(INSERT,'E-MAIL:   ','front')
                text.insert(INSERT,t[j][4],'front')
                text.tag_add("center", "7.0")
                text.insert(INSERT,'\n\n')
                text.insert(INSERT,'PATIENT AGE:   ','front')
                text.insert(INSERT,t[j][5],'front')
                text.tag_add("center", "9.0")
                text.insert(INSERT,'\n\n')
                text.insert(INSERT,'GENDER:   ','front')
                text.insert(INSERT,t[j][6],'front')
                text.tag_add("center", "11.0")
                text.insert(INSERT,'\n\n')
                text.insert(INSERT,'PHONE:   ','front')
                text.insert(INSERT,t[j][7],'front')
                text.tag_add("center", "13.0")
                text.insert(INSERT,'\n\n')
                text.insert(INSERT,'ADDRESS:   ','front')
                text.insert(INSERT,t[j][8],'front')
                text.tag_config('front', font='Garamond 14 bold', foreground='white')
                text.tag_add("center", "15.0")
                c=1
    
    if(c==0):
        text.delete(1.0,END)
        text.tag_configure("center", justify='center')
        text.insert(INSERT,'NO TOKEN ID EXISTS IN OUR DATABASE','front8')
        text.tag_config('front8', font='Garamond 14 bold', foreground='white')
        text.tag_add("center", "1.0")            
    conn.close()


button=Button(r,text='GET STATUS',font='Helvetica 10 bold',bg="#00b33c",relief=FLAT,fg='#ffffff',cursor="hand2",command=get_status).place(x=185,y=92,height=25,width=190)
text=Text(r,bg="#006699",relief=FLAT)
text.place(x=0,y=170,width=560)

r.resizable(width=False, height=False)
r.mainloop()