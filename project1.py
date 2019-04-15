#Disease information
import win32console
import win32gui
win=win32console.GetConsoleWindow()       
win32gui.ShowWindow(win,0)
import wikipedia
from tkinter.scrolledtext import ScrolledText
from tkinter import *

r = Tk()
r.iconbitmap("./images/py.ico")
r.title("Disease Information")
canvas = Canvas(r, height=550, width=560,bg="#ffffff",highlightthickness=0)
canvas.pack()
my_image = PhotoImage(file="./images/info.png")
canvas.create_image(270, 80, image=my_image)

a=Canvas(r, bg="#ff1a75", height=11, width=115,highlightthickness=0)
a.place(x=0,y=165)
b=Canvas(r, bg="#b3b300", height=11, width=115,highlightthickness=0)
b.place(x=110,y=165)
x=Canvas(r, bg="#ff471a", height=11, width=115,highlightthickness=0)
x.place(x=220,y=165)
y=Canvas(r, bg="#39ac39", height=11, width=115,highlightthickness=0)
y.place(x=335,y=165)
z=Canvas(r, bg="#4dd2ff", height=11, width=115,highlightthickness=0)
z.place(x=450,y=165)
p=Canvas(r, bg="#adad85", height=11, width=115,highlightthickness=0)
p.place(x=730,y=165)

def get_var():
    pol=mystring.get()
    new=wikipedia.summary(pol)
    pop3.delete(1.0,END)
    print(new)
    
mystring = StringVar()
pop1=Label(r,text="ENTER DISEASE NAME",font='Garamond 13 bold',fg="#00134d",bg="#ffffff")
pop1.place(x=30,y=200)
pop2=Entry(r,relief=GROOVE,bd=2,textvariable=mystring)
pop2.place(x=290,y=200,width=180,height=25)
pop3=ScrolledText(r,bg="#d6e0f5",relief=FLAT)
pop3.place(x=0,y=255,width=560,height=295)
button1=Button(r,text='Search',font='Helvetica 9 bold',bg="#00b33c",relief=FLAT,fg='#ffffff',cursor="hand2", command=lambda : get_var())
button1.place(x=482,y=198)

def redirector(inputStr):
    pop3.insert(INSERT, inputStr)

sys.stdout.write = redirector

r.resizable(width=False, height=False)
r.mainloop()