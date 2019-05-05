
from tkinter import *
from tkinter.filedialog import asksaveasfilename
import threading
import socket
import time
import note
from PIL import Image, ImageTk
import webbrowser

conn_array = []
addr_array=[]
username_array = []
username="나"
count=0
main_body_text=0
port = []
myname=""
th = []

class Server(threading.Thread):
    def __init__(self,port):
        threading.Thread.__init__(self)
        self.port=port

    def run(self):
        global conn_array
        global addr_array
        global username_array
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.bind(('',self.port))
        s.listen(1)
        writeToScreen("소켓 상태가 양호합니다, 포트에 연결되기 전까지 대기 해주세요 : "+str(self.port),"System")
        while 1:
            if len(conn_array) <= 3:
                a=len(username_array)
                conn_init,addr_init=s.accept()
                conn_array.append(conn_init)
                addr_array.append(addr_init)
                thindex = threading.Thread(target=Runner,args=(conn_init,str(addr_init[0]),False))
                th.append(thindex)
                thindex.start()
                global statusConnect
                statusConnect.set("연결 끊기")
                connecter.config(state=DISABLED)
                if a==len(username_array):
                    time.sleep(1)
                writeToScreen("연결 성공",username_array[a])
            else:
                conn, addr = s.accept()
                netThrow(conn, "방이 꽉 찼습니다.")
                time.sleep(3)
                conn.close()

def QuickServer():
    Server(9990).start()

def resetting(master):
    connecter.config(state=NORMAL)
    master.destroy()

def server_options_window(master):
    top = Toplevel(master)
    top.title("연결")
    top.grab_set()
    top.protocol("WM_DELETE_WINDOW", lambda: resetting(top))
    Label(top, text="Port:").grid(row=0)
    port = Entry(top)
    port.grid(row=0, column=1)
    port.focus_set()
    go = Button(top, text="실행", command=lambda:
                server_options_go(port.get(), top))
    go.grid(row=1, column=1)

def server_options_go(port,window):
    if port_process(port):
        Server(int(port)).start()
    else:
        writeToScreen("잘못 입력하셨습니다.")
        connecter.config(state=NORMAL)
    window.destroy()

def saveHistory():
    global main_body_text
    file_name = asksaveasfilename(
        title="저장 위치",
        filetypes=[('Plain text', '*.txt'), ('Any File', '*.*')])
    print(file_name)
    try:
        filehandle = open(file_name + ".txt", "w")
    except IOError:
        print("저장 할 수 없습니다.")
        return
    contents = main_body_text.get(1.0, END)
    for line in contents:
        filehandle.write(line)
    filehandle.close()

def list_info(master,myname=""):
    top=Toplevel(master)
    top.title("대화 참여자")
    top.protocol("WM_DELETE_WINDOW",lambda:top.destroy())
    top.grab_set()
    top.focus_set()
    listbox=Listbox(top)
    for i in range(0,len(username_array)):
        listbox.insert(END,username_array[i])
    listbox.pack()

class Client(threading.Thread):
    def __init__(self,host,port,name):
        threading.Thread.__init__(self)
        self.port=port
        self.host=host
        self.name=name
    def run(self):
        global conn_array
        global port

        conn_init=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        conn_init.connect((self.host,self.port))
        port.append(self.port)
        writeToScreen("연결 성공","채팅 서버")
        netThrow(conn_init,"TnTiTcTk : "+self.name)
        conn_array.append(conn_init)
        threading.Thread(target=Runner,args=(conn_init,self.host,True)).start()
        global statusConnect
        statusConnect.set("연결 끊기")
        connecter.config(state=NORMAL)

def client_options_go(dest,name,port,window):
    window.destroy()

    if ip_process(dest.split(".")) and port_process(port) and len(name)>0:
        Client(dest,int(port),name).start()
        note.sql(name)

    else:
        writeToScreen("you mistake input")
        connecter.config(state=NORMAL)


def ip_process(ipArray):
    if len(ipArray) != 4:
        return False
    for ip in ipArray:
        if not ip.isnumeric():
            return False
        if int(ip)<0 or int(ip)>255:
            return False
    return True

def port_process(port):
    if not port.isnumeric():
        return False
    if int(port)<0 or 65555<int(port):
        return False
    return True

def QuickClient():
    window = Toplevel(root)
    window.title("연결 옵션")
    window.grab_set()
    Label(window,text="서버 IP : ").grid(row=0)
    destination = Entry(window)
    destination.grid(row=0,column=1)
    Label(window,text=" 닉네임 : ").grid(row=1)
    name = Entry(window)

    name.grid(row=1,column=1)
    go = Button(window,text="연결",command=lambda:
                client_options_go(destination.get(),name.get().strip(),"9990",window))
    go.grid(row=2,column=1)

def client_options_window(master):
    top = Toplevel(master)
    top.title("연결 옵션")
    top.protocol("WM_DELETE_WINDOW", lambda: resetting(top))
    top.grab_set()
    Label(top, text="서버 IP").grid(row=0)
    location = Entry(top)
    location.grid(row=0, column=1)
    location.focus_set()
    Label(top, text="Port:").grid(row=1)
    port = Entry(top)
    port.grid(row=1, column=1)
    Label(top,text=" 닉네임 :  ").grid(row=2)
    name = Entry(top)

    name.grid(row=2,column=1)

    go = Button(top, text="연결", command=lambda:
                client_options_go(location.get(),name.get().strip(), port.get(), top))
    go.grid(row=3, column=1)

def netThrow(conn,text):
    try:
        conn.send(text.encode("utf-8"))
    except socket.error:
        writeToScreen("실패","SYSTEM")

def netCatch(conn):
    try:
        message = conn.recv(512)
        return message.decode("utf-8")
    except socket.error:
        writeToScreen("실패","SYSTEM")

def username_options_window(master):
    top=Toplevel(master)
    top.title("닉네임 변경")
    top.grab_set()
    Label(top,text="닉네임:").grid(row=0)
    name=Entry(top)
    name.focus_set()
    name.grid(row=0,column=1)
    go=Button(top,text="변경",command=lambda:username_options_go(name.get(),top))
    go.grid(row=1,column=1)

def username_options_go(name,window):
    if len(conn_array)!=0:
        netThrow(conn_array[0],"TcThTaTn : "+name)
    else:
        writeToScreen("연결 먼저 해주세요.","System")
    window.destroy()
def Search(master):
    sea=Toplevel(master)
    sea.title("검색")
    sea.geometry('200x80')
    sea.grab_set()
    Label(sea,text="검색어:").grid(row=0)
    name=Entry(sea)
    name.focus_set()
    name.grid(row=0,column=1)
    go=Button(sea,text="검색",command=lambda:Search_naver(name.get(),sea))
    go.grid(row=1,column=1)
def Search_naver(name, window):
    url='https://search.naver.com/search.naver?where=nexearch&sm=top_sug.pre&fbm=0&acr=1&acq=goo&qdt=0&ie=utf8&query='+name
    webbrowser.open(url)
    window.destroy()


def Constellation():
    url = 'https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&query=%EB%B3%84%EC%9E%90%EB%A6%AC%20%EC%9A%B4%EC%84%B8'
    webbrowser.open(url)

def News():
    url = 'http://www.hani.co.kr/'
    webbrowser.open(url)

def Adv(master):
    window = Toplevel(master)

    window.grab_set()
    window.title("Poster")
    window.geometry('500x700')
    path = 'poster.jpg'
    img = ImageTk.PhotoImage(Image.open(path))
    panel =Label(window, image=img)

    # The Pack geometry manager packs widgets in rows or columns.
    panel.pack(side="bottom", fill="both", expand="yes")
    window.mainloop()

def ProgramExit() :
    global conn_array

    fd = conn_array[0].getsockname()

    netThrow(conn_array[0], "TdTeTlTe : "+str(fd[1]))

    conn_array[0].close()
    conn_array.pop()
    root.destroy()

def Runner(conn,addr,clientType,name=""):
    global username_array
    global conn_array
    while 1:
        data = netCatch(conn)
        if type(data) == type(None) :
            time.sleep(10)
            break
        elif clientType==False:
            if data[0:11]=="TnTiTcTk : ":
                if len(username_array)!=0:
                    for i in range(len(username_array)):
                        netThrow(conn_array[i],"TuTsTeTr : "+data[11:])
                    for i in range(len(username_array)):
                        netThrow(conn,"TuTsTeTr : "+username_array[i])
                try:
                    username_array.find(data[11:])
                except AttributeError:
                    username_array.append(data[11:])
                    continue
            elif data[0:11]=="TdTeTlTe : ":
                i = 0
                for ip, por in addr_array:
                    if str(por) == data[11:] :
                        port = por
                        break
                    i += 1
                conn_array[i].close()
                conn_array.pop(i)
                addr_array.pop(i)
                username_array.pop(i)
            elif data[0:11]=="TcThTaTn : ":
                writeToScreen(" 닉네임 : "+username_array[conn_array.index(conn)]+" 닉네임 변경  : "+data[11:],"System")
                username_array[conn_array.index(conn)]=data[11:]
                for i in range(len(conn_array)):
                    if i!=conn_array.index(conn):
                        netThrow(conn_array[i],data)
            else:
                for i in range(0,len(conn_array)):
                    if conn!=conn_array[i]:
                        netThrow(conn_array[i],data+"+"+username_array[conn_array.index(conn)])
                    else:
                        writeToScreen(data,username_array[i])
        else:
            if data[0:11]=="TuTsTeTr : ":
                if myname!=data[11:]:
                    username_array.append(data[11:])
                continue
            if data[0:11]=="TcThTaTn : ":
                writeToScreen(" 닉네임 : "+username_array[conn_array.index(conn)]+" 닉네임 변경  : "+data[11:],"System")
                username_array[conn_array.index(conn)]=data[11:]
                continue
            if data.rfind("+")==-1:
                writeToScreen(data,"서버")
            else:
                writeToScreen(data[0:data.rfind("+")],data[data.rfind("+")+1:])

def processUserText(event):
    writeToScreen(text_input.get(),username)
    netThrow(conn_array[0],text_input.get())
    text_input.delete(0,END)

def writeToScreen(text,user=""):
    global main_body_text
    main_body_text.config(state=NORMAL)
    main_body_text.insert(END,'\n')
    if user:
        main_body_text.insert(END,"["+user+"]")
    main_body_text.insert(END,text)
    main_body_text.yview(END)
    main_body_text.config(state=DISABLED)

def connects(clientType):
    global conn_array
    connecter.config(state=DISABLED)
    if len(conn_array) == 0:
        if clientType == 0:
            client_options_window(root)
        if clientType == 1:
            server_options_window(root)
    else:
        ProgramExit()

def make_label(parent, img):
    label = Label(parent, image=img)
    label.pack()


def toOne():
    global clientType
    clientType = 0


def toTwo():
    global clientType
    clientType = 1

root=Tk()
root.title("PyTalk")


root.resizable(width=TRUE, height=TRUE)

label1 = Label(root, text="Welcome to PyTalk")

label1.pack()

menubar=Menu(root)

file_menu = Menu(menubar,tearoff=0)
file_menu.add_command(label="채팅 저장",command=lambda:saveHistory())
file_menu.add_command(label="닉네임 변경",command=lambda:username_options_window(root))
file_menu.add_command(label="종료",command=lambda:root.destroy())
menubar.add_cascade(label="파일",menu=file_menu)

connection_menu = Menu(menubar,tearoff=0)
connection_menu.add_command(label="빠른 연결",command=QuickClient)
connection_menu.add_command(label="포트에 연결",command=lambda:client_options_window(root))
connection_menu.add_command(label="연결 끊기",command=ProgramExit)
menubar.add_cascade(label="연결",menu=connection_menu)

add_menu = Menu(menubar,tearoff=0)
add_menu.add_command(label='네이버 검색', command=lambda :Search(root))
add_menu.add_command(label="오늘의 별자리",command=lambda :Constellation())
add_menu.add_command(label="뉴스",command=lambda :News())
add_menu.add_command(label="광고",command=lambda :Adv(root))
menubar.add_cascade(label='검색',menu=add_menu)

server_menu = Menu(menubar,tearoff=0)
server_menu.add_command(label="서버 실행",command=QuickServer)
server_menu.add_command(label="새 서버 실행",command=lambda:server_options_window(root))
menubar.add_cascade(label="서버",menu=server_menu)

menubar.add_command(label="대화 참여자",command=lambda:list_info(root,myname))

root.config(menu=menubar)

main_body = Frame(root,height=100,width=100)

main_body_text = Text(main_body)
body_text_scroll = Scrollbar(main_body)
main_body_text.focus_set()
body_text_scroll.pack(side=RIGHT,fill=Y)
main_body_text.pack(side=LEFT,fill=Y)
body_text_scroll.config(command=main_body_text.yview)
main_body_text.config(yscrollcommand=body_text_scroll.set)
main_body.pack()

main_body_text.insert(END,"채팅 프로그램에 오신걸 환영합니다!")
main_body_text.config(state=DISABLED)

text_input = Entry(root,width=80)
text_input.bind("<Return>",processUserText)
text_input.pack()

statusConnect = StringVar()
statusConnect.set("연결")
clientType = 1
Radiobutton(root,text="Client",variable=clientType,value=0,command=toOne).pack(anchor=E)
Radiobutton(root,text="Server",variable=clientType,value=1,command=toTwo).pack(anchor=E)
connecter = Button(root,textvariable=statusConnect,command=lambda: connects(clientType))
connecter.pack()

root.mainloop()
