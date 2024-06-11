6.1 Source code 
Client code: 
import socket import sys import tkinter as tk from tkinter import * 
from tkinter.filedialog import askopenfile import cv2 import numpy as np import 
struct window = tk.Tk() window.geometry("250x200") window.title("Login") username_value=tk.StringVar() password_value=tk.StringVar() def upload(): 
    filepath=filedialog.askopenfilename(filetypes=[("image",".jpeg"),("image", 
".png"),("image", ".jpg")])     print("File location : "+filepath)     extension = filepath.split('.', 1)     print("File Type : "+extension[1]) 
    clientSock.sendto(extension[1].encode(), ("127.0.0.1", 20001))     img=cv2.imread (filepath)     cv2.imshow('img',img) 
    img_encode=cv2.imencode ("."+extension[1], img)[1]     data_encode=np.array (img_encode)     data=data_encode.tostring()     #data=cv2.imencode("."+extension[1],img)[1].tostring()     print("Length of Data : "+ str(len(data)))     print("Encoded Byte Data : ")     print(data) 
    #Defining file headers,Packaging into a structure 
     
    fhead=struct.pack ("l", len (data)) 
     
    #Send file header: 
     
    clientSock.sendto (fhead, ("127.0.0.1", 20001)) 
     
    #Cyclic picture stream 
     
    for i in range (len (data) //1024 + 1): 
        if 1024 * (i + 1)>len (data): 
            #checks if any data is left and sends it irrespective of size             clientSock.sendto (data [1024 * i:], ("127.0.0.1", 20001))         else: 
            #sends data with a size of 1024 
            clientSock.sendto (data [1024 * i:1024 * (i + 1)], ("127.0.0.1", 20001))     cv2.waitKey(0)     cv2.destroyAllWindows() def submit_login(): 
    username=username_value.get()     password=password_value.get()     if(username=="client" and password=="client"): 
        print("You are now logged in")         window.destroy()         global clientSock 
        clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)         clientSock.sendto("Client connection established".encode(), ("127.0.0.1", 20001))         print("Connection established, sent message to server")         upload_file=tk.Tk()         upload_file.geometry("400x300")         upload_file.title("Upload an Image") 
        tk.Label(upload_file,text="Upload 	an 	Image", 	font="times 	15 	bold", width=30).grid(row=1,column=1) 
        tk.Button(text="Upload an Image",width=20,command=upload).grid(row=2, column=1) 
             else: 
        print("Error") 
tk.Label(window,text="Client Login", font="times 15 bold").grid(row=0,column=3) username=tk.Label(window,text="Username").grid(row=1,column=2,padx=10,pady=10) password=tk.Label(window,text="Password").grid(row=2,column=2,padx=10) username_box=tk.Entry(window,textvariable=username_value).grid(row=1,column=3) password_box=tk.Entry(window,textvariable=password_value,show="*").grid(row=2,col umn=3) 
tk.Button(text="Login",command=submit_login).grid(row=4, column=3,pady=20) window.mainloop() 
 
