import socket
import pickle
from tkinter import *

HEADERSIZE = 10
x=10
y=10
root = Tk()
root.title('Pool Output Map - Andrew Dunford')
root.geometry("800x700")

cnv=Canvas(root, width=800, height=700, bg="white")
cnv.pack()

cnv.create_line(15,305,15,395,fill="grey")
cnv.create_line(15,305,50,305,fill="grey")
cnv.create_line(15,395,50,395,fill="grey")

ball = cnv.create_oval(x-7,y-7,x+7,y+7, fill="yellow")
cnv.create_rectangle(50,50,625,650,fill="blue")
cnv.create_line(110,50,110,650,fill="white")
cnv.create_line(170,50,170,650,fill="red")
cnv.create_line(290,50,290,650,fill="yellow")
cnv.create_line(320,50,320,650,fill="green")
cnv.create_oval(x-7,y-7,x+7,y+7, fill="yellow")
#ball = cnv.create_oval(x-7,y-7,x+7,y+7, fill="yellow")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 1903))

while True:
    full_msg = b''
    new_msg = True
    while True:
        msg = s.recv(16)
        if new_msg:
            #print("new msg len:",msg[:HEADERSIZE])
            msglen = int(msg[:HEADERSIZE])
            new_msg = False
            cnv.delete(ball)
            root.update()

        #print(f"full message length: {msglen}")

        full_msg += msg

        #print(len(full_msg))


        if len(full_msg)-HEADERSIZE == msglen:
            #print("full msg recvd")
            #print(full_msg[HEADERSIZE:])

            d=pickle.loads(full_msg[HEADERSIZE:])
            #print(d)

            x = d[1]
            y = d[2]
            x_od = d[3]                                                        #this is to ensure the ball correseponds to the new coordinates of the output diagram
            y_od = d[4]
            #print(x,y)
            ball = cnv.create_oval(x_od-8,y_od-8,x_od+8,y_od+8, fill="yellow")
            root.update()

            new_msg = True
            full_msg = b''
    root.mainloop()