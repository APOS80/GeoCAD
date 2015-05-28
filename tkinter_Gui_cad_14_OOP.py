# Python 3

import sys
import functools
import math


from tkinter import *
from tkinter.ttk import Combobox


class functions(object):

    @staticmethod
    def DrawPoints(objects,color):
        index = len(objects[0])
        for x in range(len(objects[0])):
            if objects[5][x] == "pp":
                draw.create_oval(objects[1][x] - 2 , objects[2][x] - 2 , objects[1][x] + 2, objects[2][x] + 2, fill=color)
        if len(objects[5]) > 0:
            if objects[5][index - 1] == "ll":
                draw.create_oval(objects[1][index-1] - 2 , objects[2][index-1] - 2 , objects[1][index-1] + 2, objects[2][index-1] + 2, fill=color)


    @staticmethod
    def DrawLines(x,y,objects,keyes1,new1,color):
       
        
        rangeindex = (len(objects[5]))
        linexy = []
        
        if len(objects[0]) > 1:            
            i = 0
                       
            

            while i != rangeindex:
                           
                if objects[5][i] == "ll":
                    linexy.append(objects[1][i])
                    linexy.append(objects[2][i])
                            
                elif objects[5][i] == "/ll":
                    linexy.append(objects[1][i])
                    linexy.append(objects[2][i])
                             
                    draw.create_line(linexy,fill=color)
                    del linexy
                    linexy = []

                i = i + 1
                
       
        if len(objects[0]) >= 1: 
            if keyes1[0] == "ll" and new1[0] == 0 and objects[5][rangeindex - 1] == "/ll" or objects[5][rangeindex - 1] == "ll":
                linexy.append(objects[1][rangeindex - 1])
                linexy.append(objects[2][rangeindex - 1])
                linexy.append(x)
                linexy.append(y)
                draw.create_line(linexy,fill=color)
                

                
        
    @staticmethod
    def DrawArcs(a,b,objects,keyes1,arc,color):
        def DArcs(objects):
            if len(objects[5]) >= 3:

            
                oxy = []
                angels = []
                r1 = []
                coord = []
                arc1 = []
                check = []
                
                rangeindex = (len(objects[5]))
                i = 0
                
                while i != rangeindex:
                    if objects[5][i] == "la":
                        arc1.append(objects[1][i])
                        arc1.append(objects[2][i])

                    if objects[5][i] == "/la":
                        arc1.append(objects[1][i])
                        arc1.append(objects[2][i])
                                                                    
                                        
                        oxy.append((((arc1[3]**2-arc1[1]**2+arc1[2]**2-arc1[0]**2)/(2*(arc1[2]-arc1[0])))-((arc1[5]**2-arc1[3]**2+arc1[4]**2-arc1[2]**2)/(2*(arc1[4]-arc1[2]))))
                                  /(((arc1[3]-arc1[5])/(arc1[4]-arc1[2]))-((arc1[1]-arc1[3])/(arc1[2]-arc1[0]))))

                        oxy.append((oxy[0]*((arc1[1]-arc1[3])/(arc1[2]-arc1[0])))+((arc1[3]**2-arc1[1]**2+arc1[2]**2-arc1[0]**2)/(2*(arc1[2]-arc1[0]))))
                        
                        
                        oxy.reverse()
                        
                        r1.append(math.sqrt((arc1[1]-oxy[1])**2+(arc1[0]-oxy[0])**2)) # Radius
                        #print("r1",r1[0])
                        angels.append((math.atan((arc1[1]-oxy[1])/(arc1[0]-oxy[0]))*57.29577951)) #Degrees point 
                        angels.append((math.atan((arc1[5]-oxy[1])/(arc1[4]-oxy[0]))*57.29577951)) #Degrees point
                        check.append((math.atan((arc1[3]-oxy[1])/(arc1[2]-oxy[0]))*57.29577951)) #Degrees point
                        
                        
                        # Point one
                        if (arc1[0]-oxy[0]) < 0:
                                angels[0] = angels[0] + 180
                    
                        if (arc1[0]-oxy[0]) > 0 and (arc1[1]-oxy[1]) < 0:
                            angels[0] = angels[0] + 360

                        # Point two
                        if (arc1[4]-oxy[0]) < 0:
                                angels[1] = angels[1] + 180
                    
                        if (arc1[4]-oxy[0]) > 0 and (arc1[5]-oxy[1]) < 0:
                            angels[1] = angels[1] + 360

                        # Check point
                        if (arc1[2]-oxy[0]) < 0:
                                check[0] = check[0] + 180
                    
                        if (arc1[2]-oxy[0]) > 0 and (arc1[3]-oxy[1]) < 0:
                            check[0] = check[0] + 360
                        


                        if angels[0] > angels[1]:
                            angels.reverse()

                        if check[0] < angels[0] or check[0] > angels[1]:
                            #print("Wrong")
                            angels[0] = 360 - angels[0]
                            angels[1] = 360 + (360 - angels[1] - angels[0]) 
                            #print(angels)
                        
                        else:
                            angels[0] = 360 - angels[0]
                            angels[1] = 360 - angels[1] - angels[0]
                        
                        
                            if angels[1] > 0:
                                angels[1] *= -1

                                          
                        # Now wee got a raidus, two angels and a center point.

                        coord = [oxy[0] - r1[0],oxy[1] + r1[0],oxy[0] + r1[0], oxy[1] - r1[0]]
                            
                        draw.create_arc(coord,start=angels[0],extent=angels[1], style="arc", outline=color)
                        
                        
                        
                        #draw.create_oval(oxy[0] - 2 , oxy[1] - 2 , oxy[0] + 2, oxy[1] + 2, fill="red")
                
                        
                        del oxy[:]
                        del r1[:]
                        del angels[:]
                        del coord[:]
                        del arc1[:]
                        del check[:]

                                         
                    i = i + 1

        DArcs(objects)
        # Paint arc live.
        if keyes1[0] == "la" and len(arc) == 6:
            
            TempArc = [[],[],[],[],[],[]]
            i = 0
            while i != 6:
                TempArc[0].append("arc")                
                TempArc[1].append(arc[0 + i])
                TempArc[2].append(arc[1 + i])
                TempArc[3].append(arc[2 + i])                
                TempArc[4].append("kod")
                TempArc[5].append("la")
                i +=3

            if a != arc[0] and a != arc[3] and b != arc[1] and b != arc[4]:
                TempArc[0].append("arc")                
                TempArc[1].append(a)
                TempArc[2].append(b)
                TempArc[3].append(0)                
                TempArc[4].append("kod")
                TempArc[5].append("/la")

                DArcs(TempArc)

                del TempArc[0][:]
                del TempArc[1][:]
                del TempArc[2][:]
                del TempArc[3][:]
                del TempArc[4][:]
                del TempArc[5][:]
            


# move and zoom operations
class transform(object):

	def move(event,transformation):

		transformation

		return 

	def zoom(event,transformation):
		
		transformation
		
		return 



class fileop(object):
    
    def __init__(self):
        self.objects = [[],[],[],[],[],[]]#id,x,y,z,code,typecode
        self.cl = ['black']
        self.file = ['noname']
        self.path = ['']

    @staticmethod
    def newfile():
        files.append(fileop())
        f = len(files) - 1
        openfiles.append(files[f].file[0])
        filebox['values'] = openfiles
        filebox.current(len(files)-1)
        colorvar.set(files[f].cl[0])
        print(len(files))

    @staticmethod
    def openfile():
        pass

    @staticmethod
    def closeactivefile():

        if (len(files)-1) > 0:
            f = filebox.current()
            files.pop(f)
            openfiles.pop(f)
            filebox['values'] = openfiles
            filebox.current(0)
            colorvar.set(files[0].cl[0])
        else:
            files[0].objects = [[],[],[],[],[],[]]
            files[0].cl[0] = ['black']
            files[0].file[0] = ['noname']
            files[0].path[0] = ['']
            openfiles.append(files[0].file[0])
            filebox['values'] = openfiles
            filebox.current(0)
            colorvar.set(files[0].cl[0])
            
            
        

    @staticmethod
    def savefile():
        pass

    @staticmethod
    def saveasfile():
        pass

    @staticmethod
    def changeactive(event):
        f = filebox.current()
        print(f)
        colorvar.set(files[f].cl[0])

    @staticmethod
    def colorset(event):
        color[0] = colorvar.get()
        f = filebox.current()
        print(f,color[0])
        files[f].cl[0] = color[0]
    


#### End Classes

# Start Main!

    

def motion(event, objects1, keyes1, new1, arc, WidthHeight, color):
    
    draw.delete(ALL)
    a, b = event.x, event.y 
    xy1.set("x " + str(a) + " y" + str(b))
    draw.create_rectangle(0, 0, WidthHeight[0], WidthHeight[1], fill="white")
    
    # Draw points
    functions.DrawPoints(objects1,color)
    
        
    # Draw Lines
    functions.DrawLines(a,b,objects1,keyes1,new1,color)
    

    # Draw Arcs
    functions.DrawArcs(a,b,objects1,keyes1,arc,color)
    
    
    if snapp[0] == "sp": # snapp nerest
        
        x = event.x
        y = event.y
        maxl = 0
        minl = 0

        for xy in range(len(objects[0])):
            l = math.sqrt((x - objects[1][xy])**2+(y - objects[2][xy])**2)
            if l > minl:
                maxl = l
        minl = maxl

        

        for xyz in range(len(objects[0])):
            l = math.sqrt((x - objects[1][xyz])**2+(y - objects[2][xyz])**2)
            if l <= minl:                
                minl = l
                del snapp_xy[:]
                snapp_xy.append(objects[1][xyz])
                snapp_xy.append(objects[2][xyz])
                snapp_xy.append(objects[3][xyz])
        draw.create_rectangle(snapp_xy[0] - 5,snapp_xy[1] - 5,snapp_xy[0] + 5 ,snapp_xy[1] + 5, width=2, outline="black")   
           
        
                                    
                   
    draw.create_line(a, 0, a, WidthHeight[1], fill="red")
    draw.create_line(0, b, WidthHeight[0], b, fill="red")
    draw.create_rectangle(a - 10,b - 10,a + 10 ,b + 10, outline="red")
    
##    draw.create_rectangle(250,250,a,b, outline="red")
##    draw.create_arc(250, 250, a, b, start=0, extent=-45)
    return

def paint(event, keyes1, snapp1, new1, arc):

    index = 0

    
    print(keyes1)
    

    if len(keyes1) == 1:
        
        if len(objects[5]) > 0:
            if keyes1[0] != "ll" and objects[5][len(objects[5])-1] == "ll":
                objects[5][len(objects[5])-1] = "pp"
                print("did")

        
        # Point
        if keyes1[0] == "pp":
            del arc[:]
            x1 = event.x 
            y1 = event.y
            objects[0].append("id")

            if snapp[0] == "sp":
                objects[1].append(snapp_xy[0])
                objects[2].append(snapp_xy[1])
                objects[3].append(snapp_xy[2])
            else:    
                objects[1].append(x1)
                objects[2].append(y1)
                objects[3].append(0)
            
            
            objects[4].append("kod")
            objects[5].append("pp")

            
        # Line
        elif keyes1[0] == "ll":
            del arc[:]
            x1 = event.x 
            y1 = event.y

            objects[0].append("id")

            if snapp[0] == "sp":
                objects[1].append(snapp_xy[0])
                objects[2].append(snapp_xy[1])
                objects[3].append(snapp_xy[2])
            else:    
                objects[1].append(x1)
                objects[2].append(y1)
                objects[3].append(0)

            
            objects[4].append("kod")
            
            index = len(objects[5]) - 1
            
            
            if index >= 0:
                if objects[5][index] == "ll" or objects[5][index] == "/ll" and new1[0] == 0:
                    objects[5].append("/ll")
                    objects[5][index] = "ll"
                else:
                    objects[5].append("ll")
                    if new1[0] == 1:
                        new.remove(1)
                        new.append(0)
            else:
                objects[5].append("ll")

        # Arc
        elif keyes1[0] == "la":   
            if len(arc) <= 9:

                    x1 = event.x 
                    y1 = event.y
                    
                    
                    if snapp[0] == "sp":
                        arc.append(snapp_xy[0])
                        arc.append(snapp_xy[1])
                        arc.append(snapp_xy[2])
                    else:    
                        arc.append(x1)
                        arc.append(y1)
                        arc.append(0)
                        
                    if len(arc) == 6 and arc[0] == arc[3] and arc[1] == arc[4]:
                        #print("no")
                        arc.pop()
                        arc.pop()
                        arc.pop()
                        
                    elif len(arc) == 9 and arc[0] == arc[6] and arc[1] == arc[7]:
                        #print("no")
                        arc.pop()
                        arc.pop()
                        arc.pop()
                        
                    elif len(arc) == 9 and arc[3] == arc[6] and arc[4] == arc[7]:
                        #print("no")
                        arc.pop()
                        arc.pop()
                        arc.pop()
                        
            if len(arc) == 9 :
                    print(arc)

                    i = 0    
                        
                    while i != 9:                 
                        objects[0].append("arc")                
                        objects[1].append(arc[0 + i])
                        objects[2].append(arc[1 + i])
                        objects[3].append(arc[2 + i])                
                        objects[4].append("kod")

                        if i == 6:
                            objects[5].append("/la")
                        else:
                            objects[5].append("la") 

                        i = i + 3
                    del arc[:]
                    
        else:
            pass
    else:
        pass

    
##    i = 0
##    u = 0
##
##    for i in range(len(objects)):
##        print()
##        for u in range(len(objects[i])):
##            print(objects[i][u], "," , end='')
##
##    print()
        
    return


def clearit():

    del objects[0][:]
    del objects[1][:]
    del objects[2][:]
    del objects[3][:]
    del objects[4][:]
    del objects[5][:]

    draw.delete(all)
    draw.create_rectangle(0, 0, WidthHeight[0], WidthHeight[1], fill="white")
    return 

def keypressed(event): # Short commands

    if event.char == chr(27):
        mode.set("")
        del keyes_w[:]
        del keyes[:]
        del snapp[:]
        keyes_w.append(0)
        keyes_w.append(0)
        keyes.append("nn")
        
        snapp.append("nn")
        
    else:

        if len(keyes_w) == 2 :
            if event.char == "n": # flag for new object
                new.remove(0)
                new.append(1)
            elif event.char not in command_sel:
                print("not in dict")
            else:    
                del keyes_w[:]
                keyes_w.append(event.char)


        elif len(keyes_w) == 1:
            keyes_w.append(event.char)

            if keyes_w[0]+keyes_w[1] not in command_sel:
                    print("not in dict")
                    keyes_w.pop()
                    print(keyes_w)
            
        if len(keyes_w) == 2 and keyes_w[0] != "s" :
            del keyes[:]
            keyes.append(keyes_w[0]+keyes_w[1])
           

        if len(keyes_w) == 2 and keyes_w[0] == "s" :
            del snapp[:]
            snapp.append(keyes_w[0]+keyes_w[1])


# Texting

        if len(keyes_w) == 1:
            if keyes_w[0] == "s":
                mode.set(command_sel[keyes[0]]+">>"+command_sel[keyes_w[0]])
            else:    
                mode.set(command_sel[keyes_w[0]]+">>"+command_sel[snapp[0]])
                
        


        if len(keyes_w) == 2:
            mode.set(command_sel[keyes[0]]+">>"+command_sel[snapp[0]])
    
        
        
    return

    

def save():
    return

def donothing(): # none command
   filewin = Toplevel(root)
   button = Button(filewin, text="Do nothing button")
   button.pack()

def about():
    filewin = Toplevel(root)
    label = Label(filewin, text='APOS CAD \n Best geodetic cad in the world!')
    label.pack()



    
files=[]
files.append(fileop())

objects=[[],[],[],[],[],[]]#id,x,y,z,punktkod,typkod
keyes_w = [0,0]
keyes = ["nn"]
snapp = ["so"]
snapp_xy = [0,0,0]
new = [0]
arc = []
color = ["black"]

WidthHeight = [800,500]

openfiles = []
openfiles.append(files[0].file[0])
colors = ["Black","Red","Green","Blue","Cyan","Magenta","Yellow","khaki","Orange"]

command_sel = {
    "nn": "none", "nn": "none",
    "l" : "Line:", "ll" : "Line: Straight", "lc" : "Line: Circle", "la": "Line: Arc",
    "p" : "Point:", "pp": "Point: XYZ",
    "s" : "Snapp:", "sp": "Snapp: Point", "sm": "Snapp: midle", "sg":"Snapp: Grid", "so":"Snapp: Off"
    }
            



   
root = Tk()
root.title("APOS CAD")

xy1 = StringVar()
mode = StringVar()
filevar = StringVar()
colorvar = StringVar()

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=fileop.newfile)
filemenu.add_command(label="Open", command=fileop.openfile)
filemenu.add_command(label="Save", command=fileop.savefile)
filemenu.add_command(label="Save as...", command=fileop.saveasfile)
filemenu.add_command(label="Close Active", command=fileop.closeactivefile)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Undo", command=donothing)
editmenu.add_separator()
editmenu.add_command(label="Cut", command=donothing)
editmenu.add_command(label="Copy", command=donothing)
editmenu.add_command(label="Paste", command=donothing)
editmenu.add_command(label="Delete", command=clearit)
editmenu.add_command(label="Select All", command=donothing)
menubar.add_cascade(label="Edit", menu=editmenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help Index", command=donothing)
helpmenu.add_command(label="About...", command=about)
menubar.add_cascade(label="Help", menu=helpmenu)

root.config(menu=menubar)

filebox = Combobox(root, textvariable=filevar, values=openfiles, state='readonly')
filebox.current(0)
colorbox = Combobox(root, textvariable=colorvar, values=colors, state='readonly')
colorbox.current(0)
label1 = Label(root, textvariable = mode, bg="white", fg="black")
label3 = Label(root, text="vakant", bg="white", fg="black")

draw = Canvas(root, cursor="none", width=WidthHeight[0], height=WidthHeight[1])
draw.bind("<Motion>", functools.partial(motion, objects1=objects, keyes1=keyes, new1=new, arc=arc, WidthHeight=WidthHeight , color=color))
draw.bind("<Button-1>", functools.partial(paint, keyes1=keyes, snapp1=snapp, new1=new, arc=arc))
draw.bind_all("<KeyPress>",  keypressed)
filebox.bind("<<ComboboxSelected>>", fileop.changeactive)
colorbox.bind("<<ComboboxSelected>>", fileop.colorset)


filebox.grid(row=0, column=0, columnspan=1, sticky=W+E)
colorbox.grid(row=0, column=1, columnspan=1, sticky=W+E)
draw.grid(row=1, column=0, columnspan=10, sticky=W+E)
label1.grid(row=2, column=0, columnspan=1, sticky=W+E)
label3.grid(row=2, column=2, columnspan=8, sticky=W+E)

root.mainloop()
