# #############################################################################
# #####################################################################CRUD_APP
# #############################################################################

# ###############################################################INTERFACE_ROOT
import sqlite3
from tkinter import Tk, Menu, Frame, Label, Entry, Text, Button, Scrollbar
from tkinter import StringVar
from tkinter import messagebox

root = Tk()
root.title('CRUD APP')
root.resizable(0, 0)
# root.iconbitmap('logo.ico')


# ####################################################################FUNCTIONS
# MENU_BBDD
# SUBMENU_CONECT
def menuDBConect():
    try:
        myConection = sqlite3.connect('Users')
        myCursor = myConection.cursor()
        myCursor.execute('''
                        CREATE TABLE USERS_DATA (
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        FIRST_NAME VARCHAR(50),
                        LAST_NAME VARCHAR(50),
                        PASSWORD VARCHAR(10),
                        ADDRESS VARCHAR(50),
                        COMMENT VARCHAR(100)
                        )
                        ''')
        messagebox.showinfo('DB', 'The database has been created successfully')

    except sqlite3.OperationalError:
        messagebox.showwarning('Warning!', 'The database already exists')

    finally:
        myConection.commit()
        myConection.close()


# SUBMENU_EXIT
def menuDBExit():
    value = messagebox.askokcancel(
        'Exit', 'Do you want to exit the application?')
    if value:
        root.destroy()


# MENU_CLEAN
# SUBMENU_CLEAN_ALL
def menuCleanAll():
    myID.set('')
    myFirstName.set('')
    myLastName.set('')
    myPass.set('')
    myAddress.set('')
    textComment.delete('1.0', 'end')
    entryName.focus_set()


# MENU_CRUD
# SUBMENU_CREATE
def menuCRUDCreate():
    myConection = sqlite3.connect('Users')
    myCursor = myConection.cursor()

    # Forma paramétrica:
    data = (myFirstName.get(),
            myLastName.get(),
            myPass.get(),
            myAddress.get(),
            textComment.get("1.0", "end"))
    myCursor.execute('INSERT INTO USERS_DATA VALUES(NULL,?,?,?,?,?)', (data))

    myConection.commit()
    myConection.close()
    messagebox.showinfo('BBDD', 'The record has been created successfully')
    menuCleanAll()


# MENU_CRUD
# SUBMENU_READ
def menuCRUDRead():
    myConection = sqlite3.connect('Users')
    myCursor = myConection.cursor()

    # Comprobamos que existe
    idUser = myID.get()
    myCursor.execute('SELECT ID FROM USERS_DATA')
    allU = myCursor.fetchall()
    allUsers = []
    for id in allU:
        allUsers.append(id[0])

    # Obtenemos el id seleccionado por el usuario
    myCursor.execute('SELECT * FROM USERS_DATA WHERE ID=' + idUser)
    oneUser = myCursor.fetchall()

    # Leemos y rellenamos la información
    if int(myID.get()) in allUsers:
        for user in oneUser:
            myID.set(user[0])
            myFirstName.set(user[1])
            myLastName.set(user[2])
            myPass.set(user[3])
            myAddress.set(user[4])
            textComment.insert('1.0', user[5])
        myConection.commit()
        myConection.close()
        entryName.focus_set()

    else:
        messagebox.showwarning('Warning!', 'The entered user does not exist')
        myConection.commit()
        myConection.close()
        menuCleanAll()
        entryID.focus_set()


# MENU_CRUD
# SUBMENU_UPDATE
def menuCRUDUpdate():
    myConection = sqlite3.connect('Users')
    myCursor = myConection.cursor()

    # Forma paramétrica:
    data = (myFirstName.get(),
            myLastName.get(),
            myPass.get(),
            myAddress.get(),
            textComment.get("1.0", "end"),
            myID.get())
    myCursor.execute('''UPDATE USERS_DATA
                     SET FIRST_NAME=?, LAST_NAME=?,
                     PASSWORD=?, ADDRESS=?, COMMENT=?
                     WHERE ID=?''', (data))

    myConection.commit()
    myConection.close()
    messagebox.showinfo('BBDD', 'The record has been successfully updated')
    menuCleanAll()


# MENU_CRUD
# SUBMENU_DELETE
def menuCRUDDelete():
    myConection = sqlite3.connect('Users')
    myCursor = myConection.cursor()

    value = messagebox.askokcancel(
        'Exit', 'Are you sure you want to delete this record?')
    if value:
        myCursor.execute('DELETE FROM USERS_DATA WHERE ID=' + myID.get())
        myConection.commit()
        myConection.close()
        messagebox.showinfo('BBDD', 'The record has been successfully deleted')
        menuCleanAll()


# MENU_HELP
# SUBMENU_LICENCE
def menuHelpLicence():
    messagebox.showinfo('Licence', '''
    This project has the GNU General Public License
    Author: Mariano Luna
    Year: 2023
    ''')


# MENU_HELP
# SUBMENU_ABOUT
def menuHelpAbout():
    messagebox.showinfo('ARQFI', '''
    Sitio web de ARQFI:
    https://www.arqfi.com
    ''')


# ###############################################################INTERFACE_MENU
menuBar = Menu(root)
root.config(menu=menuBar, width=400)

menuBBDD = Menu(menuBar, tearoff=0)
menuBBDD.add_command(label='Conect', command=menuDBConect)
menuBBDD.add_command(label='Exit', command=menuDBExit)
menuClean = Menu(menuBar, tearoff=0)
menuClean.add_command(label='Clean All', command=menuCleanAll)
menuCRUD = Menu(menuBar, tearoff=0)
menuCRUD.add_command(label='Create', command=menuCRUDCreate)
menuCRUD.add_command(label='Read', command=menuCRUDRead)
menuCRUD.add_command(label='Update', command=menuCRUDUpdate)
menuCRUD.add_command(label='Delete', command=menuCRUDDelete)
menuHelp = Menu(menuBar, tearoff=0)
menuHelp.add_command(label='License', command=menuHelpLicence)
menuHelp.add_command(label='About...', command=menuHelpAbout)

menuBar.add_cascade(label='BBDD', menu=menuBBDD)
menuBar.add_cascade(label='Clean', menu=menuClean)
menuBar.add_cascade(label='CRUD', menu=menuCRUD)
menuBar.add_cascade(label='Help', menu=menuHelp)


# ###############################################################INTERFACE_GRID
myFrame1 = Frame(root)
myFrame1.pack()

myID = StringVar()
myFirstName = StringVar()
myLastName = StringVar()
myPass = StringVar()
myAddress = StringVar()

labelID = Label(myFrame1, text='ID:')
labelID.grid(row=0, column=0, sticky='e', padx=20, pady=10)
entryID = Entry(myFrame1, textvariable=myID)
entryID.grid(row=0, column=1, padx=0, pady=10)
entryID.config(fg='black', justify='left', width=20)
# entryID.config(state='disabled')

# Label oculto, usado sólo para centrar el formato
labelHide = Label(myFrame1, text='')
labelHide.grid(row=0, column=3, padx=10, pady=10)

labelName = Label(myFrame1, text='Name:')
labelName.grid(row=1, column=0, sticky='e', padx=20, pady=10)
entryName = Entry(myFrame1, textvariable=myFirstName)
entryName.grid(row=1, column=1, padx=0, pady=10)
entryName.config(fg='black', justify='left', width=20)
entryName.focus_set()

labelLastName = Label(myFrame1, text='Last Name:')
labelLastName.grid(row=2, column=0, sticky='e', padx=20, pady=10)
entryLastName = Entry(myFrame1, textvariable=myLastName)
entryLastName.grid(row=2, column=1, padx=0, pady=10)
entryLastName.config(fg='black', justify='left', width=20)

labelPass = Label(myFrame1, text='Password:')
labelPass.grid(row=3, column=0, sticky='e', padx=20, pady=10)
entryPass = Entry(myFrame1, textvariable=myPass)
entryPass.grid(row=3, column=1, padx=0, pady=10)
entryPass.config(fg='black', justify='left', width=20, show='*')

labelAddress = Label(myFrame1, text='Address:')
labelAddress.grid(row=4, column=0, sticky='e', padx=20, pady=10)
entryAddress = Entry(myFrame1, textvariable=myAddress)
entryAddress.grid(row=4, column=1, padx=0, pady=10)
entryAddress.config(fg='black', justify='left', width=20)

labelComment = Label(myFrame1, text='Comment:')
labelComment.grid(row=5, column=0, sticky='e', padx=20, pady=10)
textComment = Text(myFrame1, width=10, height=5)
textComment.grid(row=5, column=1, padx=0, pady=10)
textComment.config(fg='black', width=15)
scrollVert = Scrollbar(myFrame1, command=textComment.yview)
scrollVert.grid(row=5, column=2, sticky='nsew', padx=0, pady=10)
textComment.config(yscrollcommand=scrollVert.set)

myFrame2 = Frame(root)
myFrame2.pack()

buttonCreate = Button(myFrame2, text='Create', command=menuCRUDCreate)
buttonCreate.grid(row=0, column=0, padx=10, pady=20)
buttonRead = Button(myFrame2, text='Read', command=menuCRUDRead)
buttonRead.grid(row=0, column=1, padx=10, pady=20)
buttonUpdate = Button(myFrame2, text='Update', command=menuCRUDUpdate)
buttonUpdate.grid(row=0, column=2, padx=10, pady=20)
buttonDelete = Button(myFrame2, text='Delete', command=menuCRUDDelete)
buttonDelete.grid(row=0, column=3, padx=10, pady=20)

root.mainloop()
