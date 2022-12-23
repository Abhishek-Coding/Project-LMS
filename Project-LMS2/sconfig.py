import tkinter as tk
from tkinter import messagebox
from binascii import hexlify,unhexlify
import mysql.connector
import pickle

def checkStat():
    if boxStat.get()==1:
        passEntry.config(show='')
    else:
        passEntry.config(show='*')

def datSave():
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

def datRetrieve(file):
    return [unhexlify(x).decode() for x in pickle.load(file)]
    
def serverConfig(Type=0):
    global Host,User,Passwd,top,boxStat,passEntry,closeEvent,imge
    imge = tk.PhotoImage(file='images\config.png')
    Host = tk.StringVar()
    User = tk.StringVar()
    Passwd = tk.StringVar()
    boxStat = tk.IntVar()
    top = tk.Toplevel()
    top.title('Server Configuration')
    top.lift()
    top.grab_set()
    top.geometry('500x500')
    top.resizable(0,0)
    tk.Label(top,image=imge).pack(anchor='nw')
    tk.Label(top,text="Host:",font='Comicsansms 15').place(x=60,y=100)
    tk.Label(top,text="User:",font='Comicsansms 15').place(x=60,y=130)
    tk.Label(top,text="Password:",font='Comicsansms 15').place(x=60,y=160)
    tk.Label(top,text="Show Password",font='Comicsansms 10').place(x=90,y=200)
    tk.Entry(top,textvariable=Host).place(x=170,y=107,anchor='nw')
    tk.Entry(top,textvariable=User).place(x=170,y=137)
    passEntry = tk.Entry(top,textvariable=Passwd,show='*')
    passEntry.place(x=170,y=167)
    tk.Checkbutton(top,variable=boxStat,command=checkStat).place(x=190,y=200)
    tk.Button(top,text='Submit',command=datSave).place(x=135,y=240)
    if Type==1:
        closeEvent = top.bind('<Destroy>',quit)
    
