#Python 3

import sys
import functools
import math
from data import CadData


from tkinter import *
from tkinter.filedialog import *
from tkinter.ttk import Combobox


class CadGui(object):

    def __init__(self,root):
        self.root = root
        root.title("APOS CAD")

        self.xy1 = StringVar()
        self.mode = StringVar()
        
       
        self.WidthHeight = [800,500]
        
        self.filevar = StringVar() # Filebox
        self.openfiles = [data.data[0][1]]
        self.colorvar = StringVar() #Colorbox
        self.colors = ["Red","Green","Blue","Cyan","Magenta","Yellow","Black","khaki","Orange"]

        self.scroll = IntVar() # Scaltefactor
        self.scroll.set(1)
        self.wheel = IntVar() # Wheel
        self.wheel.set(1)
        self.savedyx = [0,0] # Last canvas xy for calc
        self.modyx = [self.WidthHeight[1],0] # Moved origo
        self.modyxset = [0,0] # moved origo hold
        self.Map_XY = [0,0] # Crosshairs place on map


        self.xy1 = StringVar()
        self.mode = StringVar()
        self.keyes_w = [0,0]
        self.keyes = ["nn"]
        self.snapp = ["so"]
        self.snapp_xy = [0,0,0]
        self.new = [0]
        
        def passit():
            pass

        self.menubar = Menu(root)
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="New", command= self.newfile)
        self.filemenu.add_command(label="Open", command= self.openfile)
        self.filemenu.add_command(label="Save", command= self.save)
        self.filemenu.add_command(label="Save as...", command= self.saveas)
        self.filemenu.add_command(label="Close", command= self.close)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.root.quit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        self.editmenu = Menu(self.menubar, tearoff=0)
        self.editmenu.add_command(label="Undo", command=passit())
        self.editmenu.add_separator()
        self.editmenu.add_command(label="Cut", command=passit())
        self.editmenu.add_command(label="Copy", command=passit())
        self.editmenu.add_command(label="Paste", command=passit())
        self.editmenu.add_command(label="Delete", command=passit())
        self.editmenu.add_command(label="Select All", command=passit())
        self.menubar.add_cascade(label="Edit", menu=self.editmenu)

        self.helpmenu = Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label="Help", command=passit())
        self.helpmenu.add_command(label="About...", command=passit())
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)

        self.root.config(menu=self.menubar)

        self.filebox = Combobox(root, textvariable=self.filevar, values=self.openfiles, state='readonly')
        self.filebox.current(0)
        self.colorbox = Combobox(root, textvariable=self.colorvar, values=self.colors, state='readonly')
        self.colorbox.current(data.data[0][0])
        self.label1 = Label(root, textvariable = self.mode, bg="white", fg="black")
        self.label2 = Label(root, textvariable = self.xy1, bg="white", fg="black")
        self.label3 = Label(root, textvariable = self.scroll, bg="white", fg="black")



        self.draw = Canvas(root, cursor="none", width=self.WidthHeight[0], height=self.WidthHeight[1])
        self.draw.bind("<Motion>",functools.partial(self.motion, WidthHeight=self.WidthHeight, moving = 0))
        self.draw.bind("<Button-1>", self.respons )
        
        self.draw.bind_all("<KeyPress>",  self.keypressed)
        
        # Scrollwheel        
        self.draw.bind("<MouseWheel>", functools.partial(self.motion, WidthHeight=self.WidthHeight, moving = 2)) #win/osx
        self.draw.bind("<Button-4>", functools.partial(self.motion, WidthHeight=self.WidthHeight, moving = 2)) #linux
        self.draw.bind("<Button-5>", functools.partial(self.motion, WidthHeight=self.WidthHeight, moving = 2)) #linux
        # middlebutton + move
        self.draw.bind("<B2-Motion>",functools.partial(self.motion, WidthHeight=self.WidthHeight, moving=1))

        self.filebox.bind("<<ComboboxSelected>>", lambda f: self.colorbox.current(data.data[self.filebox.current()][0]))
        self.colorbox.bind("<<ComboboxSelected>>", lambda c: data.change_color(self.filebox.current(),self.colorbox.current()))


        self.filebox.grid(row=0, column=0, columnspan=1, sticky=W+E)
        self.colorbox.grid(row=0, column=1, columnspan=1, sticky=W+E)
        self.draw.grid(row=1, column=0, columnspan=10, sticky=W+E)
        self.label1.grid(row=2, column=0, columnspan=1, sticky=W+E)
        self.label2.grid(row=2, column=1, columnspan=1, sticky=W+E)
        self.label3.grid(row=2, column=2, columnspan=1, sticky=W+E)
        
        self.root.resizable(0,0)


    def newfile(self):
        data.new_file()
        self.openfiles.append(data.data[-1][1])
        self.filebox['values'] = self.openfiles

    def save(self):
        currentfile = self.filebox.current()
        if len(data.data[currentfile][2]) > 0:
            data.save_file(currentfile,data.data[currentfile][2])
        else:
            print('nono')

    def saveas(self):
        currentfile = self.filebox.current()
        data.save_file(currentfile,filedialog.asksaveasfilename(defaultextension=".cad"))
        self.openfiles[currentfile] = data.data[currentfile][1]
        self.filebox['values'] = self.openfiles
        self.filebox.current(currentfile)
        print(currentfile)
        print(data.data)
        

    def openfile(self):
        data.open_file(filedialog.askopenfilename())
        self.openfiles.append(data.data[-1][1])
        self.filebox['values'] = self.openfiles
        print(data.data)

    def close(self):
        currentfile = self.filebox.current()
        data.close_file(currentfile)
        self.openfiles.pop(currentfile)
        self.filebox['values'] = self.openfiles
        self.filebox.current(0)
        print(data.data)

    def keypressed(self,event): # Short commands

        command_sel = {
            "nn": "none", "nn": "none",
            "l" : "Line:", "ll" : "Line: Straight", "lc" : "Line: Circle", "la": "Line: Arc",
            "p" : "Point:", "pp": "Point: XYZ",
            "s" : "Snapp:", "sp": "Snapp: Point", "sm": "Snapp: midle", "sg":"Snapp: Grid", "so":"Snapp: Off"
            }

        if event.char == chr(27):
            self.mode.set("")
            del self.keyes_w[:]
            del self.keyes[:]
            del self.snapp[:]
            self.keyes_w.append(0)
            self.keyes_w.append(0)
            self.keyes.append("nn")
            
            self.snapp.append("nn")

            self.new[0] = 1
            
            
        else:

            if len(self.keyes_w) == 2 :
                if event.char == "n": # flag for new object
                    self.new[0] = 1
                elif event.char not in command_sel:
                    print("not in dict")
                else:    
                    del self.keyes_w[:]
                    self.keyes_w.append(event.char)


            elif len(self.keyes_w) == 1:
                self.keyes_w.append(event.char)

                if self.keyes_w[0]+self.keyes_w[1] not in command_sel:
                        print("not in dict")
                        self.keyes_w.pop()
                        print(self.keyes_w)
                
            if len(self.keyes_w) == 2 and self.keyes_w[0] != "s" :
                del self.keyes[:]
                self.keyes.append(self.keyes_w[0]+self.keyes_w[1])
               

            if len(self.keyes_w) == 2 and self.keyes_w[0] == "s" :
                del self.snapp[:]
                self.snapp.append(self.keyes_w[0]+self.keyes_w[1])


            # Show active mode

            if len(self.keyes_w) == 1:
                if self.keyes_w[0] == "s":
                    self.mode.set(command_sel[self.keyes[0]]+">>"+command_sel[self.keyes_w[0]])
                else:    
                    self.mode.set(command_sel[self.keyes_w[0]]+">>"+command_sel[self.snapp[0]])
                    
            


            if len(self.keyes_w) == 2:
                self.mode.set(command_sel[self.keyes[0]]+">>"+command_sel[self.snapp[0]])
    
        
        
        return

    def respons(self,event):
        data.paint(int(self.Map_XY[0]),int(self.Map_XY[1]), self.keyes, self.snapp, self.new, self.filebox.current())
        self.new[0] = 0
    
    def motion(self,event,WidthHeight, moving): # mouse event responsese and draw the canvas

        # Catching events
        
        Canvas_YX = [event.y , event.x]
        
              
        # Respons to Linux/Windows wheel event
        if moving == 2: # CHECK !!!
            if event.num == 5 or event.delta == -120: # CHECK !!!

                if self.wheel.get() > 1:
                    self.wheel.set(self.wheel.get() - 1)
                    self.scroll.set(self.wheel.get()*self.wheel.get())

                    self.modyx[0] += Canvas_YX[0]/(1/self.scroll.get())-Canvas_YX[0]/(1/((self.wheel.get()+1)*(self.wheel.get()+1)))    
                    self.modyx[1] += Canvas_YX[1]/(1/self.scroll.get())-Canvas_YX[1]/(1/((self.wheel.get()+1)*(self.wheel.get()+1)))
                  
            if event.num == 4 or event.delta == 120: # CHECK !!!!
                self.wheel.set(self.wheel.get() + 1)
                self.scroll.set(self.wheel.get()*self.wheel.get())

                self.modyx[0] += Canvas_YX[0]/(1/self.scroll.get())-Canvas_YX[0]/(1/((self.wheel.get()-1)*(self.wheel.get()-1)))    
                self.modyx[1] += Canvas_YX[1]/(1/self.scroll.get())-Canvas_YX[1]/(1/((self.wheel.get()-1)*(self.wheel.get()-1)))


            
        # Respons to B2-Motion  CHECK!
        if moving == 0:
            self.savedyx[0] = Canvas_YX[0]
            self.savedyx[1] = Canvas_YX[1]

            if self.modyxset[:] != self.modyx[:]:
                #print("changeing")
                self.modyxset[:] = self.modyx[:]
                        
        if moving == 1:
                                
            self.modyx[0]= self.modyxset[0] + (Canvas_YX[0] - self.savedyx[0]) / (1/self.scroll.get()) 
            self.modyx[1]= self.modyxset[1] + (Canvas_YX[1] - self.savedyx[1]) / (1/self.scroll.get())
       
        # Map coord   CHECK!       
        self.Map_XY[1] = -self.modyx[1] - ((Canvas_YX[1] * -1) / (1/self.scroll.get())) 
        self.Map_XY[0] = self.modyx[0] - (Canvas_YX[0] / (1/self.scroll.get()))
        





        # Transalte operation   CHECK!
        def modifying_XtoY(value):
            scroll = self.scroll.get()
            y = 0
            y = Canvas_YX[0] - ((value - self.Map_XY[0])*1/scroll)
            return y

        def modifying_YtoX(value):
            scroll = self.scroll.get()
            x = 0
            x = Canvas_YX[1] + ((value - self.Map_XY[1])*1/scroll)
            return x

        def zoomit(value):
            return (value / (1/self.scroll.get()))


                           
        # Draws the shit.
        self.draw.delete(ALL) # Clear the canvas
        self.xy1.set("N = %0.3fm E = %0.3fm  " % (float(self.Map_XY[0])/1000,float(self.Map_XY[1])/1000))
        
        # Crosshair
        self.draw.create_rectangle(0, 0, WidthHeight[0], WidthHeight[1], fill="white")
        self.draw.create_line(Canvas_YX[1], 0, Canvas_YX[1], WidthHeight[1], fill="black")
        self.draw.create_line(0, Canvas_YX[0], WidthHeight[0], Canvas_YX[0], fill="black")
        self.draw.create_rectangle(Canvas_YX[1] - 10,Canvas_YX[0] - 10,Canvas_YX[1] + 10 ,Canvas_YX[0] + 10, outline="black")

        # Origo_lines
        self.draw.create_line(modifying_YtoX(0),modifying_XtoY(-10),modifying_YtoX(0),modifying_XtoY(zoomit(Canvas_YX[0])+ self.Map_XY[0]), fill="black", dash=(4,4))
        self.draw.create_line(modifying_YtoX(-10),modifying_XtoY(0),modifying_YtoX(zoomit(WidthHeight[0]-Canvas_YX[1])+ self.Map_XY[1]),modifying_XtoY(0), fill="black",dash=(4,4))


        

        
        # Draw ewerything
        for file in range(len(data.data)):

            current = self.filebox.current()
        
            def DrawIt():
                index = len(data.data[file][3][5])
                linexy = [] # For linedraw

                for x,y,thetype in zip(data.data[file][3][1],data.data[file][3][2],data.data[file][3][5]):

                    # Draw points
                    if thetype == "pp":
                        self.draw.create_oval(modifying_YtoX(y) - 2 , modifying_XtoY(x) - 2 , modifying_YtoX(y) + 2, modifying_XtoY(x) + 2, fill=self.colors[data.data[file][0]])

                
                    # Draw lines       
                    if thetype == "ll":
                        linexy.append(modifying_YtoX(y))
                        linexy.append(modifying_XtoY(x))
                                
                    elif thetype == "/ll":
                        linexy.append(modifying_YtoX(y))
                        linexy.append(modifying_XtoY(x))
                                 
                        self.draw.create_line(linexy,fill=self.colors[data.data[file][0]])
                        del linexy
                        linexy = []


                # If only one linepoint paint dott        
                if index > 0:
                    if data.data[file][3][5][index - 1] == "ll":
                        self.draw.create_oval(modifying_YtoX(y) - 2 , modifying_XtoY(x) - 2 , modifying_YtoX(y) + 2, modifying_XtoY(x) + 2, fill=self.colors[data.data[file][0]])

                # Draw last linepoint to cross
                if file == current:
                    if index >= 1: 
                        if self.keyes[0] == "ll" and self.new[0] == 0 and data.data[file][3][5][index - 1] == "/ll" or data.data[file][3][5][index - 1] == "ll":
                            linexy.append(modifying_YtoX(data.data[file][3][2][index - 1]))
                            linexy.append(modifying_XtoY(data.data[file][3][1][index - 1]))
                            linexy.append(Canvas_YX[1])
                            linexy.append(Canvas_YX[0])
                            self.draw.create_line(linexy,fill=self.colors[data.data[file][0]])



        
            DrawIt()

            
        # Show snapp point    
        if self.snapp[0] == "sp" and len(data.data[self.filebox.current()][3][1]) > 0:
        
            maxl = 0
            minl = 0
            

            for xy in range(len(data.data[self.filebox.current()][3][1])):
                l = math.sqrt((self.Map_XY[0] - data.data[self.filebox.current()][3][1][xy])**2+(self.Map_XY[1] - data.data[self.filebox.current()][3][2][xy])**2)
                if l > minl:
                    maxl = l
            minl = maxl

            

            for xyz in range(len(data.data[self.filebox.current()][3][1])):
                l = math.sqrt((self.Map_XY[0] - data.data[self.filebox.current()][3][1][xyz])**2+(self.Map_XY[1] - data.data[self.filebox.current()][3][2][xyz])**2)
                if l <= minl:                
                    minl = l
                    del self.snapp_xy[:]
                    self.snapp_xy.append(data.data[self.filebox.current()][3][1][xyz])
                    self.snapp_xy.append(data.data[self.filebox.current()][3][2][xyz])
                    self.snapp_xy.append(data.data[self.filebox.current()][3][3][xyz])
                    
           
            self.draw.create_rectangle(modifying_YtoX(self.snapp_xy[1]) - 5,modifying_XtoY(self.snapp_xy[0]) - 5,modifying_YtoX(self.snapp_xy[1]) + 5 ,modifying_XtoY(self.snapp_xy[0]) + 5, width=2, outline="black") 

                
      
# Initialize object and load.

data = CadData() # Data handler
root = Tk()      # Gui handler
mygui = CadGui(root)

root.mainloop()
