Server Code from PIL import Image import socket import sys import cv2 import tkinter as tk import numpy as np import struct window = tk.Tk() window.geometry("250x200") window.title("Login") username_value=tk.StringVar() password_value=tk.StringVar() def submit_login(): 
    username=username_value.get()     password=password_value.get()     if(username=="admin" and password=="admin"): 
        print("You are now logged in")         window.destroy() 
        # Create a datagram socket 
        UDPServerSocket=socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) 
 
        # Bind to address and ip 
        UDPServerSocket.bind(("127.0.0.1", 20001))         print("UDP server up and listening")         connection,addr = UDPServerSocket.recvfrom(1024)         print("\n"+connection.decode())         image_ext,addr= UDPServerSocket.recvfrom(1024)         print("\nImage Extension: "+image_ext.decode()) 
        # Receive file header,The length of the file header 
        count=0         packet_loss=0         packet_lpercent=0         packet_spercent=0         #receive size and data         recv_size=0         data_size=0         data_total=b""         while True :  
            fhead_size=struct.calcsize ("l") 
            buf, addr=UDPServerSocket.recvfrom (fhead_size)             if buf: 
                #returns tuple 
                data_size=struct.unpack("l",buf)[0]                 while not recv_size ==data_size:                     if data_size - recv_size>1024: 
                        data,addr=UDPServerSocket.recvfrom(1024)                         recv_size+=len(data) 
                        print("\nTotal size of message received through buffer till this stream 
"+str(recv_size)+" (size 1024)")                         count=count+1                     else: 
                        data,addr=UDPServerSocket.recvfrom(1024)                         recv_size+=len(data)                         count=count+1 
                        print("\nTotal size of message received through buffer till this stream 
"+str(recv_size)+" (size "+str(len(data))+")")                         print("\nImage received")                     data_total+=data 
                nparr=np.fromstring (data_total, np.uint8) 
                img_decode=cv2.imdecode (nparr,cv2.IMREAD_COLOR)                 #cv2.imshow('result',img_decode)                 if(image_ext.decode()=="jpg"): 
                    cv2.imwrite('C:/Users/hanis/Desktop/result.jpg', img_decode)                     # open method used to open different extension image file 
                    #im = Image.open(r"C:/Users/hanis/Desktop/result.jpg")  
                    # This method will show image in any image viewer  
                    #im.show()                  elif(image_ext.decode()=="jpeg"): 
                    cv2.imwrite('C:/Users/hanis/Desktop/result.jpeg', img_decode) 
                    #im = Image.open(r"C:/Users/hanis/Desktop/result.jpeg")  
                    # This method will show image in any image viewer  
                    #im.show()                 else: 
                    cv2.imwrite('C:/Users/hanis/Desktop/result.png', img_decode) 
                    #im = Image.open(r"C:/Users/hanis/Desktop/result.png")  
                    # This method will show image in any image viewer  
                    #im.show()                 break            if(recv_size!=data_size): 
            packet_loss=data_size-recv_size         packet_lpercent=(packet_loss//data_size)*100         packet_spercent=(recv_size//data_size)*100 
        print("\nTotal No of messages / packets received: "+str(count))         print("\nTotal packet/data Loss if any : "+str(packet_loss))         print("\nPacket/data loss % : "+str(packet_lpercent)+"%")         print("\nPacket/data success % : "+str(packet_spercent)+"%")         cv2.waitKey(0)         cv2.destroyAllWindows() 
   
                       else:         print("Error") 
tk.Label(window,text="Server Login", font="times 15 bold").grid(row=0,column=3) username=tk.Label(window,text="Username").grid(row=1,column=2,padx=10,pady=10) password=tk.Label(window,text="Password").grid(row=2,column=2,padx=10) username_box=tk.Entry(window,textvariable=username_value).grid(row=1,column=3) password_box=tk.Entry(window,textvariable=password_value,show="*").grid(row=2,col umn=3) 
tk.Button(text="Login",command=submit_login).grid(row=4, column=3,pady=20) window.mainloop() 
