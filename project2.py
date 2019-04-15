#Doctor at my location
import win32console
import win32gui
win=win32console.GetConsoleWindow()       
win32gui.ShowWindow(win,0)
from tkinter import *
import json
from urllib.request import urlopen
import csv
from collections import defaultdict
import geopy.distance
import geocoder
import numpy as np 
from tkinter.scrolledtext import ScrolledText
 
r = Tk()
r.iconbitmap("./images/py.ico")
r.title("Location")
canvas = Canvas(r, height=450, width=640,bg="#ffffff",highlightthickness=0)
canvas.pack()
my_image = PhotoImage(file="./images/map.png")
canvas.create_image(320, 200, image=my_image)
op=Text(r,font='Helvetica 14',fg="red")
op.place(x=150,y=100,width=330,height=30)
            
def click():
    url = 'http://ipinfo.io/json'
    response = urlopen(url)
    data = json.load(response)
    city = data['city']
    country=data['country']
    region=data['region']
    op.delete(1.0,END)
    op.tag_configure("center", justify='center')
    op.insert(INSERT,city)
    op.insert(INSERT,',  ')
    op.insert(INSERT,region)
    op.insert(INSERT,',  ')
    op.insert(INSERT,country)
    op.tag_add("center", "1.0")
    
pop3=ScrolledText(r,bg="#ffffff")
pop3.place(x=0,y=200,width=640,height=295)  
    
def search():
    c=0
    columns = defaultdict(list)
    with open("./data/doctor_data.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            for (k,v) in row.items():
                columns[k].append(v)
    
    g=geocoder.ip('me')
    mycoord=g.latlng
    long=np.array(columns['loc_lon'],dtype=float)
    lat=np.array(columns['loc_lat'],dtype=float)
    col0=np.array(columns['name'])
    col6=np.array(columns['address'])
    col7=np.array(columns['phone'])
    col8=np.array(columns['email'])
    col9=np.array(columns['gender'])
    col10=np.array(columns['website'])
    col11=np.array(columns['title'])
    col=np.array(columns['specialty'])
    ss=np.array(columns['summary'])
    val1=[0]*(len(long))
    for i in range(len(long)):
        mycoord1=(lat[i], long[i])
        val1[i]=geopy.distance.vincenty(mycoord, mycoord1).km

    pop3.delete(1.0,END)
    for i in range(len(long)):
        if(val1[i]<300):
            gen='Gender: \t'+col9[i]
            deg='Degree: \t'+col11[i]
            pho='Contact: \t'+col7[i]
            spe='Speciality: \t'+col[i]
            em='Email: \t'+col8[i]
            web='Website: \t'+col10[i]
            addr='Address: \t'+col6[i]
            summ='Profile: \t'+ss[i]
            pop3.insert(INSERT,'Doctor Name: \t','de')
            pop3.tag_config('de', font='Garamond 13 bold')
            pop3.insert(INSERT, col0[i],'demo')
            pop3.tag_config('demo', font='Garamond 13 bold', foreground='red')
            pop3.insert(INSERT, '\n')
            pop3.insert(INSERT, gen)
            pop3.insert(INSERT,'\t')
            pop3.insert(INSERT, deg)
            pop3.insert(INSERT, '\n')
            pop3.insert(INSERT, pho)
            pop3.insert(INSERT, '\n')
            pop3.insert(INSERT, spe)
            pop3.insert(INSERT, '\n')
            pop3.insert(INSERT, em)
            pop3.insert(INSERT, '\n')
            pop3.insert(INSERT, web)
            pop3.insert(INSERT, '\n')
            pop3.insert(INSERT, addr)
            pop3.insert(INSERT,'\n')
            pop3.insert(INSERT,summ)
            pop3.insert(INSERT, '\n\n\n')
            c=1
    if(c!=0):
        pop3.insert(INSERT,'NO DOCTOR NEARBY!!')

button=Button(r,text="YOUR LOCATION",font='Helvetica 9 bold',bg="#00b33c",relief=FLAT,fg='#ffffff',cursor="hand2",command=click).place(x=180,y=20,width=134,height=30)
button=Button(r,text="NEARBY DOCTOR",font='Helvetica 9 bold',bg="#00b33c",relief=FLAT,fg='#ffffff',cursor="hand2",command=search).place(x=315,y=20,width=134,height=30)

r.resizable(width=False, height=False)
r.mainloop()