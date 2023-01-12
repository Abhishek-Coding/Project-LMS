import tkinter as tk
from tkinter import messagebox
from binascii import hexlify,unhexlify
import mysql.connector
import pickle
import main

def checkStat():
    if boxStat.get()==1:
        passEntry.config(show='')
    else:
        passEntry.config(show='*')

def datSave(app):
    if Host.get().strip!='' and User.get().strip()!='' and Passwd.get().strip!='':
        try:
            mydb = mysql.connector.connect(host=Host.get(),user=User.get(),passwd=Passwd.get())
            cursor = mydb.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS dbLMS;")
            mydb.close
            mydb = mysql.connector.connect(host=Host.get(),user=User.get(),passwd=Passwd.get(),database='dbLMS')
            cursor = mydb.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS binf(B_Id varchar(32),B_Ttl varchar(64),Author varchar(32),Status varchar(16),PRIMARY KEY(B_Id));")
            mydb.close
        except:
            messagebox.showwarning(title='Error',message='Unable to Connect to Server')
        else:
            with open('server.dat','wb') as f:
                pickle.dump([hexlify(Host.get().encode()).decode(),hexlify(User.get().encode()).decode(),hexlify(Passwd.get().encode()).decode()],f)
                f.close()
                top.bind('<Destroy>','')
                top.destroy()
                app.deiconify()

def datRetrieve(file):
    return [unhexlify(x).decode() for x in pickle.load(file)]
    
def serverConfig(app,Type=0):
    global Host,User,Passwd,top,boxStat,passEntry,closeEvent,imge
    imge = tk.PhotoImage(file='images\config.png')
    Host = tk.StringVar()
    User = tk.StringVar()
    Passwd = tk.StringVar()
    boxStat = tk.IntVar()
    top = tk.Toplevel()
    top.title('Server Configuration')
    top.geometry('500x500')
    top.resizable(0,0)
    top.grab_set()
    canvas = tk.Canvas(top,height=500,width=500,highlightthickness=0)
    canvas.place(x=0,y=0)
    canvas.create_image(0,0,image=imge,anchor='nw')
    tk.Label(top,text="Add Server Details",font=('Comic Sans Ms' ,24)).place(x=90,y=20)
    canvas.create_text(90,130,text="Host:",font=('Default', 19),fill='white')
    canvas.create_text(90,185,text="User:",font=('Default', 19),fill='white')
    canvas.create_text(90,235,text="Password:",font=('Default', 19),fill='white')
    canvas.create_text(110,275,text="Show Password",font=('Comicsansms', 12),fill='orange')
    tk.Entry(top,textvariable=Host,font=('Comicsansms', 10)).place(x=180,y=130,anchor='w')
    tk.Entry(top,textvariable=User,font=('Comicsansms', 10)).place(x=180,y=185,anchor='w')
    passEntry = tk.Entry(top,textvariable=Passwd,show='*',font=('Comicsansms', 10))
    passEntry.place(x=180,y=235,anchor='w')
    tk.Checkbutton(top,variable=boxStat,command=checkStat,bg='#0c0f38').place(x=180,y=275,anchor='w')
    tk.Button(top,text='Submit',command=lambda: datSave(app)).place(x=135,y=290)
    if Type==1:
        closeEvent = top.bind('<Destroy>',quit)
    app.wait_window(top)
