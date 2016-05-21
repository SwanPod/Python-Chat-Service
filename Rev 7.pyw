#Imports all necessary modules
import socket, threading, select, time, winsound
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import queue as queue

global text_color
global text_bg

text_color = open('Settings\\Theme\\text_color.txt').read()
text_bg = open('Settings\\Theme\\text_bg.txt').read()

#Lets the threading work with Tkinter
class ThreadedTask(threading.Thread):
    def __init__(self, queue):
        #Starts threading
        threading.Thread.__init__(self)
        self.queue = queue
        print ("Starting threading")
        threading.Thread(target=recv_loop, args=[sckt]).start()
    def run(self):
        time.sleep(5)
        self.queue.put('Task finished')

#Main chat gui
class GUI:

    #Initializes the layout and widgets
    def __init__(self, master):

        self.master = master
        
        self.queue = queue.Queue()
        ThreadedTask(self.queue).start()

        s = ttk.Style()
        s.theme_use('vista')

        #Creates menubar
        self.menubar = tk.Menu(self.master)

        #Adds menubar submenu
        self.cm = tk.Menu(self.menubar)
        #Adds submenu to menubar
        self.menubar.add_cascade(label='Chat', menu=self.cm)
        #Adds command 'User Settings' to submenu
        self.cm.add_command(label='User Settings', command=self.user)
        self.cm.add_cascade(label='Customize', command=self.customize)

        #Adds another submenu
        self.sm = tk.Menu(self.menubar)
        #Adds submenu to menubar
        self.menubar.add_cascade(label='Server', menu=self.sm)
        #Adds commands and separator
        self.sm.add_command(label='Server Info', command=self.server)
        self.sm.add_separator()
        self.sm.add_command(label='Exit', command=self.close)
        
        #Configures the menu in the window
        self.master.config(menu=self.menubar)

        #Creates the text field for the messages
        self.text = tk.Text(master, bg=text_bg, fg=text_color)
        self.text.grid(row=0, column=0, columnspan=5)

        #Creates textbox entry field
        self.entrym = ttk.Entry(master)
        self.entrym.grid(row=1, column=2, pady=10, columnspan=3)
        #Binds send command to when the user presses enter
        self.entrym.bind('<Return>', (lambda event: self.send()))

        #Message label next to entry field
        self.userm = ttk.Label(master, text='Message:')
        self.userm.grid(row=1, column=2, padx=5)

        #Creates send button
        self.b1 = ttk.Button(master, text='Send', command=self.send)
        self.b1.grid(row=2, column=3, padx=10, pady=10, columnspan=3)

        #Button used for test features
        self.button = ttk.Button(master, text='Test', command = self.user)
        self.button.grid(row=5, column=1)

        #Creates close button
        self.close = ttk.Button(master, text='Quit', command=self.close)
        self.close.grid(row=6, column=1)

        #Runns the connected function
        self.connected()

    #Displays connected message when user logs in
    def connected(self):
        #If the connected server is '127.0.0.1', displays localhost
        if host == '127.0.0.1':
            self.text.insert(tk.END, 'Connected to localhost')
            self.text.update()
        else:
            self.text.insert(tk.END, 'Connected to ' + host)
            self.text.update()

    #Insterts messages recieved into text field        
    def insertf(self, message):
        self.text.insert(tk.END, '\n' + message)
        self.text.update()
        pass

    #Prevents blank messages being sent
    def noMessage(self):
        self.text.insert(tk.END, '\nYou can\'t send blank messages!')
        self.text.update()
        chat.text.see(tk.END)
        pass

    #Sends messages
    def send(self):
        #Gets message from textbox
        message = self.entrym.get()
        #If there is no message, calls noMessage function
        if message == '':
            self.noMessage()
        else:
            #Clears the textbox
            self.entrym.delete(0, tk.END)
            #Creates send message
            send_message = cuser + ": " + message
            #Encodes the message and sends it
            sckt.send(send_message.encode('ascii'))

    #When user brings up server info dialog
    def server(self):
        #If host is '127.0.0.1', displays localhost
        if host == '127.0.0.1':
            tk.messagebox.showinfo('Server Info', 'Server IP: ' + host + '(localhost)' + '\nPort: ' + str(port))
        else:
            tk.messagebox.showinfo('Server Info', 'Server IP: ' + host + '\nPort: ' + str(port))
        pass

    #Asks user if they want to disconnect
    def close(self):
        opt = tk.messagebox.askyesno('Quit', 'Do you want to disconnect and close the app?')
        if opt == True:
            #Destroys(closes) the GUI window
            self.master.destroy()
        else:
            #If user clicks No, closes the dialog window
            pass

    #When user want to bring up User Settings Window
    def user(self):
        #Initializes new window
        self.newWin = tk.Toplevel(self.master)
        self.app = UserOpts(self.newWin)

    def customize(self):
        self.newWin = tk.Toplevel(self.master)
        self.cus = Customize(self.newWin)

class Customize:

    def __init__(self, master):

        self.master = master
        self.master.title('Customize Interface')
        self.master.geometry('500x500')

        self.bw = ttk.Radiobutton(self.master, text='Black and White')
        self.default = ttk.Radiobutton(self.master, text='Deafult')

        self.choosen = tk.IntVar()
        fd = open('Settings\\Theme\\theme.txt').read()

        if fd == 'default':
            self.chosen.set(1)
        elif fd == 'bw':
            self.chosen.set(2)
        else:
            self.chosen.set(1)

        self.default.grid(row=1, column=1, command=self.deaf, variable=self.chosen, value=1)
        self.bw.grid(row=2, column=1, command = self.bwf, variable=self.chosen, value=2)

    def deaf(self):
        self.textf = open('Settings\\Theme\\text_color.txt', 'w')
        self.textf.write('black')
        self.textf.close()

        self.textb = open('Settings\\Theme\\text_bg.txt', 'w')
        self.textb.write('Ivory')
        self.textb.close()

    def bwf(self):
        pass

#User Options GUI Window
class UserOpts:

    #Initializes Window
    def __init__(self, master):

        self.master = master
        self.master.title('User Settings')
        self.master.geometry('400x400')

        self.userl = 'Username: ' + cuser
        
        self.user = tk.Label(master, text=self.userl)
        self.user.grid(row=0, column=0, padx=5, pady=10)

#Server Login Window
class LoginWin:

    #Initializes window properties
    def __init__(self, master):

        self.master = master
        self.master.title('Login')
        self.master.geometry('200x250')
        self.createWindow()

    #Creates the widgets for the window
    def createWindow(self):

        self.ip_label = ttk.Label(self.master, text='Server IP:')
        self.ip_label.pack(pady=10)
        self.ip_entry = ttk.Entry(self.master)
        self.ip_entry.pack()
        self.ip_entry.bind('<Return>', (lambda event: self.loginCheck()))
        self.port_label = ttk.Label(self.master, text='Port:')
        self.port_label.pack(pady=10)
        self.port_entry = ttk.Entry(self.master)
        self.port_entry.pack()
        self.port_entry.bind('<Return>', (lambda event: self.loginCheck()))
        self.user_label = ttk.Label(self.master, text='Username:')
        self.user_label.pack(pady=10)
        self.user_entry = ttk.Entry(self.master)
        self.user_entry.pack()
        self.user_entry.bind('<Return>', (lambda event: self.loginCheck()))
        self.login_button = ttk.Button(self.master, text='Connect', command=self.loginCheck)
        self.login_button.pack(pady=10)

    #Checks for blank fields and logs in
    def loginCheck(self):
        #Sets variables that can be used throughout program
        global username
        global cuser
        global host
        global port

        #Sets values from Login Window textboxes
        host = self.ip_entry.get()
        port = self.port_entry.get()
        cuser = self.user_entry.get()
        
        if cuser == '':
            tk.messagebox.showwarning('Name Error', 'Please enter a username.')
            self.__init__(self.master)
        else:
            self.master.destroy()
            login()
    
def startchat():
    global chat
    root = tk.Tk()
    if host == '127.0.0.1':
        root.title('Chat - localhost')
    else:
        root.title('Chat - ' + host)
    root.geometry('700x560')
    chat = GUI(root)
    root.lift()
    root.attributes('-topmost', True)
    root.attributes('-topmost', False)
    s = ttk.Style()
    s.theme_use('vista')
    root.mainloop()

def loginstart():
    root = tk.Tk()
    root.geometry('150x220')
    login = LoginWin(root)
    root.mainloop()

def recv_loop(connection):
    
    while True:
        (readable, writable, errored) = select.select([connection], [], [connection], 0.1)
        if readable or errored:
            ins = connection.recv(1024)
            if not ins:
                print ("Disconnected")
                return
            global message
            message = ins.decode('utf8')
            
            chat.text.insert(tk.END, '\n' + message)
            chat.text.update()
            chat.text.see(tk.END)
            winsound.PlaySound('SystemQuestion', winsound.SND_ASYNC)

def login():
    global sckt
    global username
    global cuser
    global host
    global port
    
    if (len(host) > 0):
        if host == 'localhost':
            host = '127.0.0.1'
        else:
            host = host
    if (len(port) > 0):
        port = int(port)

    sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print ("Connecting to server")
    sckt.connect((host, port))
    
    startchat()

loginstart()
