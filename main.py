from tkinter import *
import threading
import time
import random


root = Tk()

#defining
x1 = 0
y1 = 0
x2 = 10
y2 = 10
body = [[x1,y1,x2,y2]]

lx1 = 0
ly1 = 0
lx2 = 10
ly2 = 10

fx1 = 0
fy1 = 0
fx2 = 0
fy2 = 0

last_key = 'd'
colision = True

def getKey(event):
    global last_key
    if event.keysym == 'Left' or event.char == 'a':
        if last_key == 'd':
            pass
        else:
            last_key = 'a'
    elif event.keysym == 'Right' or event.char == 'd':
        if last_key == 'a':
            pass
        else:
            last_key = 'd'
    elif event.keysym == 'Up' or event.char == 'w':
        if last_key == 's':
            pass
        else:
            last_key = 'w'
    elif event.keysym == 'Down' or event.char == 's':
        if last_key == 'w':
            pass
        else:
            last_key = 's'


def moveLeft():
    global canvas
    global x1,x2
    x1 -= 10
    x2 -= 10
    if x2 == 0:
        x1 = 290
        x2 = 300
    canvas.coords(player,x1,y1,x2,y2)


def moveRight():
    global canvas
    global x1,x2
    x1 += 10
    x2 += 10
    if x2 == 310:
        x1 = 0
        x2 = 10
    canvas.coords(player,x1,y1,x2,y2)


def moveTop():
    global canvas
    global y1,y2
    y1 -= 10
    y2 -= 10
    if y2 == 0:
        y1 = 290
        y2 = 300
    canvas.coords(player,x1,y1,x2,y2)


def moveBottom():
    global canvas
    global y1,y2
    y1 += 10
    y2 += 10
    if y2 == 310:
        y1 = 0
        y2 = 10
    canvas.coords(player,x1,y1,x2,y2)


def autoMove():
    global x1,x2
    global canvas
    global last_key
    while True:
        time.sleep(0.1)
        if last_key == 'a':
            moveLeft()
        elif last_key == 'd':
            moveRight()
        elif last_key == 'w':
            moveTop()
        elif last_key == 's':
            moveBottom()
    

def fruitGenerator():
    global colision
    global fx1,fx2,fy1,fy2
    global fruit
    while True:
        time.sleep(0.05)
        if colision:
            canvas.delete(fruit)
            fx1 = random.randrange(0,290,10)
            fy1 = random.randrange(0,290,10)
            fx2 = fx1 + 10
            fy2 = fy1 + 10
            fruit = canvas.create_rectangle(fx1,fy1,fx2,fy2, fill='#FF0000')
            colision = False
        else:
            verifyColision()


def verifyColision():
    global x1,x2,y1,y2
    global fx1,fx2,fy1,fy2
    global colision
    if (x1 == fx1) and (x2 == fx2)  and (y1 == fy1) and (y2 == fy2):
        colision = True



movement = threading.Thread(target=autoMove)
movement.start()

fruitThread = threading.Thread(target=fruitGenerator)
fruitThread.start()

#canvas
canvas = Canvas(root, bg='#33AA33', width=300, height=300, highlightthickness=1, highlightcolor='#000000', highlightbackground='#000000')
player = canvas.create_rectangle(x1,y1,x2,y2, fill='#7777FF')
fruit = canvas.create_rectangle(0,0,1,1,fill='#FFFFFF')

#placing
canvas.place(relx=0.3,rely=0.15)

#binding
root.bind('<Key>', getKey)
root.geometry('720x480')
root.resizable(0,0)
root['bg'] = '#DDDDDD'
root.mainloop()
