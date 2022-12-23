import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import csv
import mysql.connector
import sconfig

ij=0
myImgs=['images\home1.png','images\home2.png','images\home3.png']

def Home():
    for i in app.grid_slaves():
        i.destroy()
    for i in app.place_slaves():
        i.destroy()
    app.setCanvas()
    bgChange()
    app.canvas.create_window(200,235,window=tk.Button(text="Add Book",font='Algerian 23',padx=29,command=addClick,bg="brown"))
    app.canvas.create_window(200,295,window=tk.Button(text="Modify Book",font='Algerian 23',padx=6,command=modClick,bg="brown"))
    app.canvas.create_window(200,355,window=tk.Button(text="View Book",font='Algerian 23',padx=24,command=searchClick,bg="brown"))
    app.canvas.create_window(200,415,window=tk.Button(text="Issue Book",font='Algerian 23',padx=19,bg="brown"))
    app.canvas.create_window(200,475,window=tk.Button(text="Return Book",font='Algerian 23',padx=2,bg="brown"))
        
def addClick():
    app.after_cancel(app.call_id.get())
    app.canvas.destroy()
    app.config(bg='red')
    app.bookId = tk.StringVar()
    app.bookTitle = tk.StringVar()
    app.Author = tk.StringVar()
    app.clicked = tk.StringVar()
    app.clicked.set("Available")
    tframe = tk.Frame(height=300,width=300,bg='red')
    tk.Button(text='Back',command=Home).place(x=0,y=0)
    tframe.grid(row=0,column=0)
    cnv = tk.Canvas(highlightthickness=0)
    cnv.create_rectangle(0,0,376,263,fill='brown') #I was trying to completely hide the canvas but it accidentally gave the section a 3D Look
    cnv.place(x=515,y=400,anchor='c')
    tk.Label(text='Add A Book',font='Broadway 46').place(x=300,y=50)
    tk.Label(text='Book ID:',font='Algerian 19').grid(row=1,column=1,padx=50,pady=5)
    tk.Label(text='Title:',font='Algerian 19').grid(row=2,column=1,pady=5)
    tk.Label(text='Author:',font='Algerian 19').grid(row=3,column=1,pady=5)
    tk.Label(text='Status:',font='Algerian 19').grid(row=4,column=1,pady=5)
    tk.Entry(textvariable=app.bookId,bg='#002244',fg='#FF8000').grid(row=1,column=2,padx=50)
    tk.Entry(textvariable=app.bookTitle,bg='#002244',fg='#FF8000').grid(row=2,column=2)
    tk.Entry(textvariable=app.Author,bg='#002244',fg='#FF8000').grid(row=3,column=2)
    tk.OptionMenu(app,app.clicked,"Available","Not Available").grid(row=4,column=2)
    tk.Button(text='Submit',command=dbAdd).grid(row=5,column=1,columnspan=50,pady=25)

def modClick():
    app.after_cancel(app.call_id.get())
    app.canvas.destroy()
    app.boid = tk.StringVar()
    app.config(bg='yellow')
    tk.Button(text='Back',command=Home).grid()
    tk.Label(text='Book Id').place(x=100,y=100)
    tk.Entry(textvariable=app.boid).place(x=150,y=100)
    tk.Button(text='Submit',command=dbMod).place(x=180,y=150)
    
def searchClick():
    app.after_cancel(app.call_id.get())
    app.config(bg='blue')
    tk.Button(text='Back',command=Home).place(x=0,y=0)
    app.canvas.destroy()
    srchArg = tk.StringVar()
    s1 = ttk.Style()
    s1.theme_use('clam')
    s1.configure('Treeview',fieldbackground='silver')
    treeframe = tk.Frame(bg='silver')
    treeframe.place(x=100,y=200)
    tentry = tk.Entry(treeframe,textvariable=srchArg)
    tentry.pack()
    scroll_bar = tk.Scrollbar(treeframe)
    treev = ttk.Treeview(treeframe,yscrollcommand=scroll_bar.set)
    treev.pack(side='left')
    treev['columns'] = (0,1,2,3)
    treev.heading(0,text='Book ID')
    treev.heading(1,text='Book Name')
    treev.heading(2,text='Author')
    treev.heading(3,text='Status')
    treev['show'] = 'headings'
    scroll_bar.pack(side='left',fill='y')
    scroll_bar.config(command=treev.yview)
    def phir(event=''):
        for i in treev.get_children():
            treev.delete(i)
        if len(srchArg.get())==0:
            cursor.execute("SELECT * FROM `binf`;")
        else:
            cursor.execute("SELECT * FROM `binf` WHERE B_Ttl LIKE '{}%';".format(srchArg.get()))
        count = 0
        treev.tag_configure('oddRow',background='wheat')
        treev.tag_configure('evenRow',background='aqua')
        for i in cursor:
            if count%2==0:
                treev.insert('','end',values=i,tags='evenRow')
            else:
                treev.insert('','end',values=i,tags='oddRow')
            count+=1
    tentry.bind('<KeyRelease>',phir)
    phir()
    

def dbAdd():
    if app.bookId.get().strip()!='' and app.bookTitle.get().strip()!='' and app.Author.get().strip()!='':
        cursor.execute("INSERT INTO binf(B_Id,B_Ttl,Author,Status) VALUES (%s,%s,%s,%s);",(app.bookId.get(),app.bookTitle.get(),app.Author.get(),app.clicked.get()))

def dbMod():
    app.B_Id = tk.StringVar()
    app.B_T = tk.StringVar()
    app.B_A = tk.StringVar()
    app.B_S = tk.StringVar()
    app.B_Id.set(app.boid.get())
    cursor.execute("SELECT B_Ttl FROM `binf` WHERE B_Id=%s",(app.boid.get(),))
    for i in cursor:
        for j in i:
            app.B_T.set(j)
    cursor.execute("SELECT Author FROM `binf` WHERE B_Id=%s",(app.boid.get(),))
    for i in cursor:
        for j in i:
            app.B_A.set(j)
    cursor.execute("SELECT Status FROM `binf` WHERE B_Id=%s",(app.boid.get(),))
    for i in cursor:
        for j in i:
            app.B_S.set(j)
    for i in app.place_slaves():
        i.destroy()
    tk.Label(text='Book Id').place(x=100,y=100)
    tk.Label(text='Book Title').place(x=100,y=150)
    tk.Label(text='Author').place(x=100,y=200)
    tk.Label(text='Status').place(x=100,y=250)
    tk.Entry(textvariable=app.B_Id).place(x=180,y=100)
    tk.Entry(textvariable=app.B_T).place(x=180,y=150)
    tk.Entry(textvariable=app.B_A).place(x=180,y=200)
    tk.OptionMenu(app,app.B_S,"Available","Not Available").place(x=200,y=250)
    tk.Button(text='Delete',command=dbDel).place(x=190,y=280)
    tk.Button(text='Update',command=dbModif).place(x=280,y=280)

def dbDel():
    cursor.execute("DELETE FROM `binf` WHERE B_Id=%s",(app.boid.get(),))

def dbModif():
    cursor.execute("UPDATE binf SET B_Id=%s ,B_Ttl=%s ,Author=%s WHERE B_Id=%s",(app.B_Id.get(),app.B_T.get(),app.B_A.get(),app.boid.get()))

def exCsv():
    with open('datexpo.csv','w',newline='') as f:
        k=csv.writer(f)
        cursor.execute("SELECT * FROM `binf`")
        for i in cursor:
            k.writerow(i)
        f.close()
        
def bgChange():
    global ij
    app.call_id = tk.StringVar()
    if ij==3:
        ij=0
    app.bgImg(myImgs[ij])
    ij+=1
    app.call_id.set(app.after(5000,bgChange))
 
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Library Management System")
        self.geometry("1000x667")
        self.resizable(0,0)

    def setCanvas(self):
        self.canvas = tk.Canvas(self,height=667,width=1000,highlightthickness=0)
        self.canvas.pack(fill='both',expand=True)

    def bgImg(self,path):
        self.img = tk.PhotoImage(file=path)
        self.canvas.create_image(0,0,image=self.img,anchor='nw')

if __name__ == '__main__':
    app = App()
    try:
        f = open('server.dat','rb')
    except:
        app.withdraw()
        sconfig.serverConfig(1)
    else:
        Host,User,Passwd = sconfig.datRetrieve(f)
        f.close()
        try:
            mydb = mysql.connector.connect(host=Host,user=User,passwd=Passwd,database='dbLMS')
            cursor = mydb.cursor()
        except:
            messagebox.showwarning(title='Error',message='Unable to Connect to Server')
            quit()
    mymenubar = tk.Menu()
    mymenu = tk.Menu(mymenubar,tearoff=0)
    mymenu.add_command(label='Import')
    mymenu.add_command(label='Export',command=exCsv)
    mymenubar.add_cascade(label='File',menu=mymenu)
    mymenubar.add_cascade(label='Server',command=sconfig.serverConfig)
    mymenubar.add_command(label='Exit',command=quit)
    app.config(menu=mymenubar)
    Home()
    app.mainloop()
    mydb.close()
