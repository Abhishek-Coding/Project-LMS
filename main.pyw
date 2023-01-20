import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import mysql.connector
import sconfig

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Library Management System")
        self.geometry('999x666')
        self.resizable(0, 0)


        #-----Variables
        # Defining them here instead of inside their methods because in that case new widgets will be created every time a method is called.
        # Defining them here will avoid the above problem and save memory [Just my theory].
        self.bookId = tk.StringVar()
        self.bookTitle = tk.StringVar()
        self.Author = tk.StringVar()
        self.options = tk.StringVar()

        global i0,i1,i2,i3,i4
        i0 = tk.PhotoImage(file='images/background.png')
        self.w0 = tk.Label(image=i0, bd=0)
        self.w1 = tk.Label()
        i1 = tk.PhotoImage(file='images/add.png')
        self.w2 = tk.Button(image=i1, relief='groove', bd='2px black', command=self.addClick)
        i2 = tk.PhotoImage(file='images/modify.png')
        self.w3 = tk.Button(image=i2, relief='groove', bd='2px black', command=self.modClick)
        i3 = tk.PhotoImage(file='images/search.png')
        self.w4 = tk.Button(image=i3, relief='groove', bd='2px black', command=self.searchClick)
        i4 = tk.PhotoImage(file='images/home.png')
        self.w5 = tk.Button(image=i4, command=self.Home)
        self.w6 = tk.Canvas(highlightthickness=0)
        self.w7 = tk.Label(text='Add A Book', font='Broadway 46')
        self.w8 = tk.Label(text='Book ID:', font='Algerian 19')
        self.w9 = tk.Label(text='Title:', font='Algerian 19')
        self.w10 = tk.Label(text='Author:', font='Algerian 19')
        self.w11 = tk.Label(text='Status:', font='Algerian 19')
        self.w12 = tk.Entry(textvariable=self.bookId, bg='#002244', fg='#FF8000')
        self.w13 = tk.Entry(textvariable=self.bookTitle, bg='#002244', fg='#FF8000')
        self.w14 = tk.Entry(textvariable=self.Author, bg='#002244', fg='#FF8000')
        self.w15 = tk.OptionMenu(self,self.options, "Available", "Not Available")
        self.w16 = tk.Button(text='Submit')
        self.w17 = tk.Button(text='Delete')
        self.treeframe = tk.Frame(bg='silver')
        self.w18 = tk.Label(self.treeframe, text="Search By", font='Georgia 14', bg='silver', fg='Maroon')
        self.w19 = tk.Entry(self.treeframe,textvariable=self.bookId,font='Georgia 14')
        self.scroll_bar = tk.Scrollbar(self.treeframe)
        self.w20 = tk.OptionMenu(self.treeframe,self.options,"Name","ID","Author")
        self.treev = ttk.Treeview(self.treeframe,yscrollcommand=self.scroll_bar.set)
        #-----Variables-End-
        
        mymenubar = tk.Menu()
        mymenu = tk.Menu(mymenubar, tearoff=0)
        mymenu.add_command(label='Import', command=self.imCsv)
        mymenu.add_command(label='Export', command=self.exCsv)
        mymenubar.add_cascade(label='File', menu=mymenu)
        mymenubar.add_cascade(label='Server', command=lambda: sconfig.serverConfig(self))
        mymenubar.add_command(label='Exit', command=quit)
        self.config(menu=mymenubar)
        self.columnconfigure(0, minsize=290)
        self.rowconfigure(0, minsize=225)
        self.w6.create_rectangle(0, 0, 376, 263, fill='brown')
        
    def setUp(self):
        for widget in self.grid_slaves():
            widget.grid_forget()
        for widget in self.place_slaves():
            widget.place_forget()
        self.w0.place(x=0, y=0)
        
    def Home(self):
        self.setUp()
        self.bookId.set('')
        self.bookTitle.set('')
        self.Author.set('')
        self.options.set('')
        self.w1.place(x=499, y=100, anchor='c')
        self.w1.config(text="Welocme To\n Library",font='Elephant 28')
        self.w2.place(x=225, y=333, anchor='c')
        self.w3.place(x=500, y=333, anchor='c')
        self.w4.place(x=775, y=333, anchor='c')
        self.w12.bind('<KeyRelease>','')
        self.w16.config(text='Submit')

    def addClick(self):
        def dbAdd():
            if self.bookId.get().strip()!='' and self.bookTitle.get().strip()!='' and self.Author.get().strip()!='':
                try:
                    cursor.execute("INSERT INTO binf(B_Id,B_Ttl,Author,Status) VALUES (%s,%s,%s,%s);",(self.bookId.get(),self.bookTitle.get(),self.Author.get(),self.options.get()))
                    mydb.commit()
                except mysql.connector.DataError:
                    messagebox.showerror(title='Error',message='Word Limit Exceeded')
                except mysql.connector.IntegrityError:
                    messagebox.showerror(title='Error',message=f'Book Id {self.bookId.get()} Already Exsists')
                else:
                    messagebox.showinfo(title='Success',message='Successfully Added Book')
        self.setUp()
        self.w5.place(x=0, y=0)
        self.options.set("Available")
        self.w6.create_rectangle(0, 0, 376, 263, fill='brown') #I was trying to completely hide the canvas but it accidentally gave the section a 3D Look
        self.w6.place(x=500, y=333, anchor='c')
        self.w1.place(x=499, y=100, anchor='c')
        self.w1.config(text="Add A Book",font=('Comic Sans Ms',46))
        self.w8.grid(row=1, column=1, padx=50, pady=5)
        self.w9.grid(row=2, column=1, pady=5)
        self.w10.grid(row=3, column=1, pady=5)
        self.w11.grid(row=4, column=1, pady=5)
        self.w12.grid(row=1, column=2, padx=50)
        self.w13.grid(row=2, column=2)
        self.w14.grid(row=3, column=2)
        self.w15.grid(row=4, column=2)
        self.w16.grid(row=5, column=1, columnspan=2, pady=25)
        self.w16.config(command=dbAdd)

    def modClick(self):
        def dbGet(event):
            cursor.execute("SELECT B_Ttl,Author,Status FROM `binf` WHERE B_Id=%s",(self.bookId.get(),))
            for i in cursor:
                temp = 0
                for j in i:
                    if temp == 0:
                        self.bookTitle.set(j)
                    elif temp == 1:
                        self.Author.set(j)
                    else:
                        self.options.set(j)
                    temp+=1
        def check():
            cursor.execute("SELECT Status FROM `binf` WHERE B_Id=%s;",(self.bookId.get(),))
            for i in cursor:
                return len(i)>0
        def dbDel():
            if check():
                cursor.execute("DELETE FROM `binf` WHERE B_Id=%s;",(self.bookId.get(),))
                mydb.commit()
                messagebox.showinfo(title='Success',message='Deleted Entry')
            else:
                messagebox.showerror(title='Error',message=f'Book Id {self.bookId.get()} does not exist')
        def dbMod():
            if check():
                cursor.execute("UPDATE binf SET B_Ttl=%s, Author=%s, Status=%s WHERE B_Id=%s;",(self.bookTitle.get(),self.Author.get(),self.options.get(),self.bookId.get()))
                mydb.commit()
                messagebox.showinfo(title='Success',message='Modified Entry')
            else:
                messagebox.showerror(title='Error',message=f'Book Id {self.bookId.get()} does not exist')
        self.setUp()
        self.w1.place(x=499, y=100, anchor='c')
        self.w1.config(text="Modify",font=('Comic Sans Ms',46))
        self.w5.place(x=0, y=0)
        self.w6.place(x=500, y=333, anchor='c')
        self.w8.grid(row=1, column=1, padx=50, pady=5)
        self.w9.grid(row=2, column=1, pady=5)
        self.w10.grid(row=3, column=1, pady=5)
        self.w11.grid(row=4, column=1, pady=5)
        self.w12.grid(row=1, column=2, padx=50)
        self.w12.bind('<KeyRelease>',dbGet)
        self.w13.grid(row=2, column=2)
        self.w14.grid(row=3, column=2)
        self.w15.grid(row=4, column=2)
        self.w16.grid(row=5, column=1, pady=25)
        self.w16.config(text='Update', command=dbMod)
        self.w17.grid(row=5, column=2)
        self.w17.config(command=dbDel)

    def rep(self,event=''):
        for i in self.treev.get_children():
            self.treev.delete(i)
        if len(self.bookId.get())==0:
            cursor.execute("SELECT * FROM `binf`;")
        else:
            match self.options.get():
                case 'Name':
                    cursor.execute("SELECT * FROM `binf` WHERE B_Ttl LIKE '{}%';".format(self.bookId.get()))
                case 'ID':
                    cursor.execute("SELECT * FROM `binf` WHERE B_Id LIKE '{}%';".format(self.bookId.get()))
                case 'Author':
                    cursor.execute("SELECT * FROM `binf` WHERE Author LIKE '{}%';".format(self.bookId.get()))      
        count = 0
        self.treev.tag_configure('oddRow',background='wheat')
        self.treev.tag_configure('evenRow',background='aqua')
        for i in cursor:
            if count%2==0:
                self.treev.insert('','end',values=i,tags='evenRow')
            else:
                self.treev.insert('','end',values=i,tags='oddRow')
            count+=1
            
    def searchClick(self):
        self.setUp()
        self.w1.place(x=490, y=100, anchor='c')
        self.w1.config(text="Search",font=('Comic Sans Ms',46))
        self.w5.place(x=0, y=0)
        self.options.set("Name")
        s1 = ttk.Style()
        s1.theme_use('clam')
        s1.configure('self.treeview',fieldbackground='silver')
        self.treeframe.place(x=100,y=200)
        self.w18.place(x=20,y=0) 
        self.w20.place(x=120,y=0)
        self.w19.grid(row=0, column=0) 
        self.treev.grid(row=1, column=0)
        self.treev['columns'] = (0,1,2,3)
        self.treev.heading(0,text='Book ID')
        self.treev.heading(1,text='Book Name')
        self.treev.heading(2,text='Author')
        self.treev.heading(3,text='Status')
        self.treev['show'] = 'headings'
        self.scroll_bar.grid(row=1, column=1, sticky='ns')
        self.scroll_bar.config(command=self.treev.yview)
        
        self.w19.bind('<KeyRelease>',self.rep)
        self.w20.bind('<Configure>',self.rep)
        self.rep()
        
    def exCsv(self):
        with open('datexpo.csv','w',newline='') as f:
            k=csv.writer(f)
            cursor.execute("SELECT * FROM `binf`")
            for i in cursor:
                k.writerow(i)

    def imCsv(self):
        f = filedialog.askopenfile(mode='r',filetypes=[('CSV Files','*.csv')])
        k=csv.reader(f)
        try:
            for i in k:
                cursor.execute("INSERT INTO binf(B_Id,B_Ttl,Author,Status) VALUES (%s,%s,%s,%s);",(i[0],i[1],i[2],i[3]))
                mydb.commit()
        except mysql.connector.IntegrityError:
            messagebox.showerror(title='Error', message='File Conflicting With Exsisting Data')
        f.close()
        self.rep()
                        
if __name__ == "__main__":
    app = App()
    try:
        f = open('server.dat','rb')
    except:
        app.withdraw()
        sconfig.serverConfig(app,1)
    finally:
        f = open('server.dat','rb')
        Host,User,Passwd = sconfig.datRetrieve(f)
        f.close()
        try:
            mydb = mysql.connector.connect(host=Host,user=User,passwd=Passwd,database='dbLMS')
            cursor = mydb.cursor()
        except:
            messagebox.showerror(title='Error',message='Unable to Connect to Server')
            quit()
            
    app.Home()
    app.mainloop()
    mydb.close()
