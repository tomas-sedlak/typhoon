import tkinter

z="extra"
size, rect = 400, 400/8
canvas = tkinter.Canvas(width=size, height=size)
canvas.pack()
pole=[[1]*8 for _ in range(8)]
stare_pole=[[1]*8 for _ in range(8)]
for row in range(8):
        for col in range(8):
            color = "yellow" if pole[row][col] else "red"
            canvas.create_rectangle(rect * col, rect * row, rect * (col + 1), rect * (row + 1), fill=color)
def on_click(event):
    global z,stare_pole
    col = int(event.x // rect)
    row = int(event.y // rect)
    new_color = "red" if pole[row][col] else "yellow"
    pole[row][col] = 0 if pole[row][col] else 1
    canvas.create_rectangle(rect * col, rect * row, rect * (col + 1), rect * (row + 1), fill=new_color)



    if stare_pole!=pole:
        lokacia=0
        for row in range(8):#zistujeme co sa zmenilo
            for col in range(8):
                if pole[row][col]!=stare_pole[row][col]:
                    lokacia=[row,col]
        row,col=lokacia
        if z=="extra" and pole[row][col]==1:#zistujeme z kade sa pohol
            z=lokacia
        if pole[row][col]==0:#zistujeme kde sa pohol
            print(z,[row,col])
            z="extra"
        stare_pole[row][col]=pole[row][col]#nastavujeme stare na nove

canvas.bind("<Button-1>", on_click)
tkinter.mainloop()
import tkinter

z="extra"
size, rect = 400, 400/8
canvas = tkinter.Canvas(width=size, height=size)
canvas.pack()
pole=[[1]*8 for _ in range(8)]
stare_pole=[[1]*8 for _ in range(8)]
for row in range(8):
        for col in range(8):
            color = "yellow" if pole[row][col] else "red"
            canvas.create_rectangle(rect * col, rect * row, rect * (col + 1), rect * (row + 1), fill=color)
def on_click(event):
    global z,stare_pole
    col = int(event.x // rect)
    row = int(event.y // rect)
    new_color = "red" if pole[row][col] else "yellow"
    pole[row][col] = 0 if pole[row][col] else 1
    canvas.create_rectangle(rect * col, rect * row, rect * (col + 1), rect * (row + 1), fill=new_color)



    if stare_pole!=pole:
        lokacia=0
        for row in range(8):#zistujeme co sa zmenilo
            for col in range(8):
                if pole[row][col]!=stare_pole[row][col]:
                    lokacia=[row,col]
        row,col=lokacia
        if z=="extra" and pole[row][col]==1:#zistujeme z kade sa pohol
            z=lokacia
        if pole[row][col]==0:#zistujeme kde sa pohol
            print(z,[row,col])
            z="extra"
        stare_pole[row][col]=pole[row][col]#nastavujeme stare na nove

canvas.bind("<Button-1>", on_click)
tkinter.mainloop()
import tkinter

z="extra"
size, rect = 400, 400/8
canvas = tkinter.Canvas(width=size, height=size)
canvas.pack()
pole=[[1]*8 for _ in range(8)]
stare_pole=[[1]*8 for _ in range(8)]
for row in range(8):
        for col in range(8):
            color = "yellow" if pole[row][col] else "red"
            canvas.create_rectangle(rect * col, rect * row, rect * (col + 1), rect * (row + 1), fill=color)
def on_click(event):
    global z,stare_pole
    col = int(event.x // rect)
    row = int(event.y // rect)
    new_color = "red" if pole[row][col] else "yellow"
    pole[row][col] = 0 if pole[row][col] else 1
    canvas.create_rectangle(rect * col, rect * row, rect * (col + 1), rect * (row + 1), fill=new_color)



    if stare_pole!=pole:
        lokacia=0
        for row in range(8):#zistujeme co sa zmenilo
            for col in range(8):
                if pole[row][col]!=stare_pole[row][col]:
                    lokacia=[row,col]
        row,col=lokacia
        if z=="extra" and pole[row][col]==1:#zistujeme z kade sa pohol
            z=lokacia
        if pole[row][col]==0:#zistujeme kde sa pohol
            print(z,[row,col])
            z="extra"
        stare_pole[row][col]=pole[row][col]#nastavujeme stare na nove

canvas.bind("<Button-1>", on_click)
tkinter.mainloop()
