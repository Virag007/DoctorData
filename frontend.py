#Main Front GUI
from tkinter import *
from PIL import ImageTk
import webbrowser
import os
    
url1="https://www.twitter.com"
url2="https://www.blogger.com"
url3="https://www.facebook.com"
url4="https://plus.google.com"
url5="https://www.vimeo.com"
url6="https://www.instagram.com"
url7="https://www.linkedin.com"
url8="https://in.pinterest.com"
url9="https://www.youtube.com"


def pop0():
    os.system("python project0.py")
    
def pop1():
    os.system("python project6.py")
    
def pop2():
    os.system("python project1.py")

def pop3():
    os.system("python project2.py")
    
def pop4():
    os.system("python project4.py")
    
def pop5():
    root=Tk()
    root.iconbitmap("./images/py.ico")
    root.title("Copyright")
    canvas = Canvas(root, height=150, width=290,bg="#004080",highlightthickness=0)
    canvas.pack()
    label=Label(root,text='This software is reserved to Doctor Data Inc.',bg="#004080",fg='#ffffff',font='Helvetica 9 bold').place(x=10,y=10)
    label=Label(root,text='Credits:---',bg="#004080",fg='#ffffff',font='Helvetica 9 bold').place(x=10,y=50)
    label=Label(root,text='Parag Thakur',bg="#004080",fg='#ffffff').place(x=10,y=70)
    root.resizable(width=False, height=False)
    root.mainloop()
    
def pop6():
    os.system("python project3.py")
    
def pop7():
    os.system("python project5.py")
    
def open_web1():
    webbrowser.open(url1)
    
def open_web2():
    webbrowser.open(url2)
    
def open_web3():
    webbrowser.open(url3)
    
def open_web4():
    webbrowser.open(url4)
    
def open_web5():
    webbrowser.open(url5)
    
def open_web6():
    webbrowser.open(url6)
    
def open_web7():
    webbrowser.open(url7)
    
def open_web8():
    webbrowser.open(url8)
    
def open_web9():
    webbrowser.open(url9)

# Create a window
window=Tk()
window.title("Doctor Data")
window.iconbitmap("./images/py.ico")

#Canvas for window-size
c=Canvas(window,height=450,width=990,highlightthickness=0)
c.pack(fill=X)
#Canvas for side panel
d=Canvas(window, bg="#ffffff", height=500, width=72,highlightthickness=0)
d.place(x=0)

#Icons on Mid-body
img000=ImageTk.PhotoImage(file="./images/germ.png")
t000=Button(window,image=img000,highlightthickness=0,height=260,width=446,cursor="hand2",command=pop2)
t000.pack()
t000.place(x=70,y=190)
img001=ImageTk.PhotoImage(file="./images/rating.png")
t001=Button(window,image=img001,highlightthickness=0,height=260,width=470,cursor="hand2",command=pop7)
t001.pack()
t001.place(x=520,y=190)
img003=ImageTk.PhotoImage(file="./images/appoint.png")
t003=Button(window,image=img003,highlightthickness=0,height=178,width=446,cursor="hand2",command=pop0)
t003.pack()
t003.place(x=70,y=45)
img002=ImageTk.PhotoImage(file="./images/medicine.png")
t002=Button(window,image=img002,highlightthickness=0,height=178,width=470,cursor="hand2",command=pop1)
t002.pack()
t002.place(x=520,y=45)

#Rainbow effect on upper panel
a=Canvas(window, bg="#ff1a75", height=16, width=160,highlightthickness=0)
a.place(x=72,y=49)
b=Canvas(window, bg="#b3b300", height=16, width=160,highlightthickness=0)
b.place(x=230,y=49)
x=Canvas(window, bg="#ff471a", height=16, width=160,highlightthickness=0)
x.place(x=380,y=49)
y=Canvas(window, bg="#39ac39", height=16, width=160,highlightthickness=0)
y.place(x=530,y=49)
z=Canvas(window, bg="#4dd2ff", height=16, width=160,highlightthickness=0)
z.place(x=680,y=49)
p=Canvas(window, bg="#adad85", height=16, width=160,highlightthickness=0)
p.place(x=830,y=49)

#Header text & image
l1=Label(window,text="Doctor Data",font='Helvetica 15 bold',height=2,width=150,fg="#00134d",bg="#ffffff",highlightthickness=0)
l1.place(x=0)
img=ImageTk.PhotoImage(file="./images/doctor.jpg")
t1=Label(window,image=img,height=68,width=68,highlightthickness=0)
t1.pack()
t1.place(x=0,y=0)

#Left panel icons
img0=ImageTk.PhotoImage(file="./images/loc.png")
t0=Button(window,image=img0,height=93,width=68,highlightthickness=0,relief=FLAT,cursor="hand2",bg="#ffffff",command=pop3)
t0.pack()
t0.place(x=0,y=169)
img01=ImageTk.PhotoImage(file="./images/settings.png")
t01=Button(window,image=img01,height=90,width=68,highlightthickness=0,relief=FLAT,cursor="hand2",bg="#ffffff",command=pop6)
t01.pack()
t01.place(x=0,y=266)
img02=ImageTk.PhotoImage(file="./images/search.png")
t02=Button(window,image=img02,height=93,width=68,highlightthickness=0,relief=FLAT,cursor="hand2",bg="#ffffff",command=pop4)
t02.pack()
t02.place(x=0,y=72)
img03=ImageTk.PhotoImage(file="./images/copyright.png")
t03=Button(window,image=img03,height=86,width=68,highlightthickness=0,relief=FLAT,cursor="hand2",bg="#ffffff",command=pop5)
t03.pack()
t03.place(x=0,y=360)

#Mid-body labels
b1=Label(window,text="Request an appointment!",font='Helvetica 15 bold',fg="#00134d")
b1.place(x=155,y=175)
b3=Label(window,text="Check Medicine Substitute",font='Helvetica 15 bold',fg="#00134d")
b3.place(x=620,y=175)
b4=Label(window,text="Disease Information",font='Helvetica 15 bold',fg="#00134d")
b4.place(x=200,y=370)
b4=Label(window,text="Your Feedback",font='Helvetica 15 bold',fg="#00134d")
b4.place(x=680,y=370)

#Mid-panel centered image
img00=ImageTk.PhotoImage(file="./images/anti.png")
t00=Label(window,image=img00,highlightthickness=0)
t00.pack()
t00.place(x=453,y=200)

#Social media icons
img1=ImageTk.PhotoImage(file="./images/a2.jpg")
t2=Button(window,image=img1,height=22,width=22,highlightthickness=0,relief=FLAT,cursor="hand2",command=open_web1)
t2.pack()
t2.place(x=964,y=120)
img2=ImageTk.PhotoImage(file="./images/a4.jpg")
t3=Button(window,image=img2,height=22,width=22,highlightthickness=0,relief=FLAT,cursor="hand2",command=open_web2)
t3.pack()
t3.place(x=964,y=146)
img3=ImageTk.PhotoImage(file="./images/a3.jpg")
t4=Button(window,image=img3,height=22,width=22,highlightthickness=0,relief=FLAT,cursor="hand2",command=open_web3)
t4.pack()
t4.place(x=964,y=172)
img4=ImageTk.PhotoImage(file="./images/a5.jpg")
t5=Button(window,image=img4,height=22,width=22,highlightthickness=0,relief=FLAT,cursor="hand2",command=open_web4)
t5.pack()
t5.place(x=964,y=198)
img5=ImageTk.PhotoImage(file="./images/a9.jpg")
t6=Button(window,image=img5,height=22,width=22,highlightthickness=0,relief=FLAT,cursor="hand2",command=open_web5)
t6.pack()
t6.place(x=964,y=224)
img6=ImageTk.PhotoImage(file="./images/a6.jpg")
t7=Button(window,image=img6,height=22,width=22,highlightthickness=0,relief=FLAT,cursor="hand2",command=open_web6)
t7.pack()
t7.place(x=964,y=250)
img7=ImageTk.PhotoImage(file="./images/a7.jpg")
t8=Button(window,image=img7,height=22,width=22,highlightthickness=0,relief=FLAT,cursor="hand2",command=open_web7)
t8.pack()
t8.place(x=964,y=276)
img8=ImageTk.PhotoImage(file="./images/a8.jpg")
t9=Button(window,image=img8,height=22,width=22,highlightthickness=0,relief=FLAT,cursor="hand2",command=open_web8)
t9.pack()
t9.place(x=964,y=302)
img9=ImageTk.PhotoImage(file="./images/a1.jpg")
t10=Button(window,image=img9,height=22,width=22,highlightthickness=0,relief=FLAT,cursor="hand2",command=open_web9)
t10.pack()
t10.place(x=964,y=328)

#Disabling the full-screen mode
window.resizable(width=False, height=False)

# Run the window loop
window.mainloop()