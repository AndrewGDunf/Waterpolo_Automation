import socket
import pickle
from tkinter import *

HEADERSIZE = 12
x=10
y=10

root1 = Tk()
root1.title('Pool Output Map - Andrew Dunford')
root1.geometry("700x700")

root2 = Tk()
root2.title('Goal Output Map - Andrew Dunford')
root2.geometry("800x350")

cnv1=Canvas(root1, width=800, height=700, bg="white")
cnv1.pack()

cnv2=Canvas(root2, width=800, height=350, bg="white")
cnv2.pack()

cnv1.create_line(15,305,15,395,fill="grey")
cnv1.create_line(15,305,50,305,fill="grey")
cnv1.create_line(15,395,50,395,fill="grey")

ball1 = cnv1.create_oval(x-7,y-7,x+7,y+7, fill="yellow")
cnv1.create_rectangle(50,50,625,650,fill="blue")
cnv1.create_line(110,50,110,650,fill="white")
cnv1.create_line(170,50,170,650,fill="red")
cnv1.create_line(290,50,290,650,fill="yellow")
cnv1.create_line(320,50,320,650,fill="green")
cnv1.create_oval(x-7,y-7,x+7,y+7, fill="yellow")
#ball = cnv.create_oval(x-7,y-7,x+7,y+7, fill="yellow")

cnv2.create_line(25,25,775,25,fill="grey")
cnv2.create_line(18,18,782,18,fill="grey")
cnv2.create_line(25,25,25,325,fill="grey")
cnv2.create_line(18,18,18,325,fill="grey")
cnv2.create_line(775,25,775,325,fill="grey")
cnv2.create_line(782,18,782,325,fill="grey")
ball2 = cnv2.create_oval(x-20,y-20,x+20,y+20, fill="yellow")

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
            cnv1.delete(ball1)
            cnv2.delete(ball2)
            root1.update()
            root2.update()

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
            g = d[5]
            px = d[6]
            py = d[7]
            #print(px,py)
            if g == 1:
                ball1 = cnv1.create_oval(x_od-8,y_od-8,x_od+8,y_od+8, fill="green")
                ball2 = cnv2.create_oval(px-20,py-20,px+20,py+20, fill="yellow")
            else:
                ball1 = cnv1.create_oval(x_od-8,y_od-8,x_od+8,y_od+8, fill="yellow")
            root1.update()
            root2.update()

            new_msg = True
            full_msg = b''
    root1.mainloop()
    root2.mainloop()