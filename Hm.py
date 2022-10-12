from tkinter import *
from tkinter import ttk
import mysql.connector
from tkinter import messagebox as ms
from tkinter import simpledialog as sd

PK = None

'creating application window'

rt = Tk()
rt.geometry("500x500")
rt.title('Python Project 1')
rt.minsize(300, 300)




'creating labels'

l1 = Label(rt, text='nm', font=('arial', 20))
l1.grid(row=11, column=11, padx=20, pady=10, sticky=E)

l2 = Label(rt, text='con', font=('arial', 20))
l2.grid(row=12, column=11, padx=20, pady=10, sticky=W)

l3 = Label(rt, text='gen', font=('arial', 20))
l3.grid(row=13, column=11, padx=20, pady=10, sticky=W)

l4 = Label(rt, text='cat', font=('arial', 20))
l4.grid(row=14, column=11, padx=20, pady=10, sticky=W)

l5 = Label(rt, text='med', font=('arial', 20))
l5.grid(row=15, column=11, padx=20, pady=10, sticky=W)



'creating entry for name and password'

e1 = Entry(bg='white', fg='black', font=('arial', 20))
e1.grid(row=11, column=12, columnspan=2, padx=20, pady=10)

e2 = Entry(bg='red', fg='white', font=('arial', 20)) #, show='-'
e2.grid(row=12, column=12, columnspan=2, padx=20, pady=10)



'creating radiobutton for gender'

r = BooleanVar()

r1 = Radiobutton(rt, text='Male',font=('arial', 20), variable=r, value=1)
r1.grid(row=13, column=12)

r2 = Radiobutton(rt, text='Female',font=('arial', 20), variable=r, value=0)
r2.grid(row=13, column=13)
r.set(1)




'creating combobox'

op = ['surgen', 'ENT', 'chest']

cb = ttk.Combobox(rt, values=op, font=('arial', 20))
cb.set('--select option--')
cb.grid(row=14, column=12, columnspan=2, padx=20)





'creating listbox'

med = ['med1', 'med2', 'med3', 'med4', 'med5', 'med6']

lst1 = Listbox(rt, selectmode='multiple', height=3, font=('arial', 20))
for i in med: lst1.insert(END,i)

lst1.grid(row=15, column=12, columnspan=2, pady=10)




'creating treeview to show data'

col = ['Sr. No','Name', 'Contact', 'Gender', 'Category', 'Medicine']
t= ttk.Treeview(rt, columns=col)
t.grid(row=11, column=14, rowspan=4, columnspan=5)

for i in col : t.heading(i, text=i)

t.column("#0", minwidth=0, width=0)
t.column("Sr. No", width=50, anchor=CENTER)
t.column("Name", width=80, anchor=CENTER)
t.column("Contact", width=80, anchor=CENTER)
t.column("Gender", width=80, anchor=CENTER)
t.column("Category", width=80, anchor=CENTER)
t.column("Medicine", width=150, anchor=CENTER)



'creating heading'
hd = Label(rt, text="Project",bg = 'blue', fg='cyan',
           font=('times new roman', 40,  'bold'))
hd.grid(row=10, column=10, columnspan=8, pady=30)



def data():
    try :
        d = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            passwd="root",
            database='new',
            auth_plugin='mysql_native_password')# to solve auth problem
        cur = d.cursor()
        cur.execute("select * from hs")
        dt = cur.fetchall()
        return dt
    except : return None

def read():
    for item in t.get_children():
        t.delete(item)
    for i in data():
        t.insert(parent='', index=END, values=i)
    e1.focus_set()

read()



# Adding the data to database
def ad():
    n = e1.get()
    c = e2.get()
    if len(c) != 10:
        ms.showerror("wrong contact", "please provide the valid contact")
        return
    g = 'Male' if r.get() else 'Female'
    t = cb.get()
    m = ''
    for i in lst1.curselection(): m += (lst1.get(i)+',')

    d = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            passwd="root",
            database='new',
            auth_plugin='mysql_native_password' # to solve auth problem
        )
    cur = d.cursor()

    try :
        q = "INSERT INTO hs (nm, con, gen, cat, med) values(%s, %s, %s, %s, %s)"
        v = [n, c, g, t, m]
        cur.execute(q, v)
        d.commit()
        read()
        ms.showinfo('Insert', 'Data is added....')
        e1.delete(0, END)
        e2.delete(0, END)
        r.set(1)
        cb.set(' ')
        lst1.selection_clear(0, END)
        e1.focus_set()
    except Exception as e:
        ms.showerror('Failed to insert', str(e))
    cur.close()


b1 = Button(text='ADD', bg='Green', font=('arial', 20, 'bold'), command=ad)
b1.grid(row=16, column=11, padx=20, pady=10, sticky=W)


def rw(event):
    sel = t.focus()
    print(sel)
    val = t.item(sel)
    print(val)
    global PK
    PK, n, c, g, ct, m =  val['values']

    e1.delete(0, END)
    e1.insert(0, n)
    e2.delete(0, END)
    e2.insert(0, c)
    r.set(1 if g=='Male' else 0)
    cb.set(ct)
    e1.focus_set()

t.bind('<Double-1>', rw)


# Updating the data of database
def up():
    n = e1.get()
    c = e2.get()
    if len(c) != 10:
        ms.showerror("wrong contact", "please provide the valid contact")
        return
    g = 'Male' if r.get() else 'Female'
    t = cb.get()
    m = ''
    for i in lst1.curselection(): m += (lst1.get(i) + ',')

    d = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        passwd="root",
        database='new',
        # auth_plugin='mysql_native_password' # to solve auth problem
    )
    cur = d.cursor()

    try:
        q = "update hs set nm=%s, con=%s, gen=%s, cat=%s, med=%s where id=%s"
        v = [n, c, g, t, m, PK]
        cur.execute(q, v)
        d.commit()
        read()
        ms.showinfo('Update', 'Data has been changed....')
        e1.delete(0, END)
        e2.delete(0, END)
        r.set(1)
        cb.set(' ')
        lst1.selection_clear(0, END)
        e1.focus_set()
    except Exception as e:
        ms.showerror('Failed to insert', str(e))
    cur.close()


def up():
    n = e1.get()
    c = e2.get()
    if len(c) != 10:
        ms.showerror("wrong contact", "please provide the valid contact")
        return
    g = 'Male' if r.get() else 'Female'
    t = cb.get()
    m = ''
    for i in lst1.curselection(): m += (lst1.get(i)+',')

    d = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            passwd="root",
            database='new',
            auth_plugin='mysql_native_password' # to solve auth problem
        )
    cur = d.cursor()

    try :
        q = "update hs set nm=%s, con=%s, gen=%s, cat=%s, med=%s where id=%s"
        v = [n, c, g, t, m, PK]
        cur.execute(q, v)
        d.commit()
        read()
        ms.showinfo('Insert', 'Data is update....')
        e1.delete(0, END)
        e2.delete(0, END)
        r.set(1)
        cb.set(' ')
        lst1.selection_clear(0, END)
        e1.focus_set()
    except Exception as e:
        ms.showerror('Failed to insert', str(e))
    cur.close()


b2 = Button(text='UPDATE', bg='cyan', font=('arial', 20, 'bold'), command=up)
b2.grid(row=16, column=12, padx=20, pady=10)


# Deleting the single data from database
def dt():
    d = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        passwd="root",
        database='new',
        auth_plugin='mysql_native_password'  # to solve auth problem
    )
    cur = d.cursor()

    m = ms.askyesno("Delete", "Are you sure?")
    if m:
        try:
            q = "delete from hs where id=%s"
            v = [sd.askinteger('Delete','Enter Primary')]
            cur.execute(q, v)
            d.commit()
            read()
            ms.showwarning('Delete', 'Data is deleted....')

        except Exception as e:
            ms.showerror('Failed to delete', str(e))
        cur.close()


b3 = Button(text='DELETE', bg='yellow', font=('arial', 20, 'bold'), command=dt)
b3.grid(row=16, column=13, padx=20, pady=10)





# Deleting all data from database
def dta():
    d = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        passwd="root",
        database='new',
        auth_plugin='mysql_native_password'  # to solve auth problem
    )
    cur = d.cursor()
    m = ms.askyesno("Delete All", "Do you want to delete all data?")
    if m:
        try:

            q = "truncate table hs;"
            cur.execute(q)
            d.commit()
            read()
            ms.showinfo('delete all', 'all data is deleted')
        except Exception as e:
            ms.showerror('Failed to delete', str(e))
        cur.close()


b4 = Button(text='DELETE ALL', bg='red', font=('arial', 20, 'bold'), command=dta)
b4.grid(row=16, column=14, padx=20, pady=10)


b5 = Button(text='EXIT', bg='black', fg='white', font=('arial', 20, 'bold'))
b5.grid(row=17, column=11, pady=20, padx=20)
b5.bind('<Double-1>', quit)
rt.mainloop()