#Python 3.4



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

        self.IdEntry = StringVar()
        self.XEntry = StringVar()
        self.XEntry.trace('w',self.numbers_val)
        self.YEntry = StringVar()
        self.YEntry.trace('w',self.numbers_val)
        self.ZEntry = StringVar()
        self.ZEntry.trace('w',self.numbers_val)
        self.CodeEntry = StringVar()


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

        self.drawmenu = Menu(self.menubar, tearoff=0)
        self.drawmenu.add_command(label="Point   D>P", command=functools.partial(self.keypressed,event='<tkinter.Event object>', char1=['d','p']))
        self.drawmenu.add_command(label="Line    D>L", command=functools.partial(self.keypressed,event='<tkinter.Event object>', char1=['d','l']))
        self.drawmenu.add_separator()
        self.drawmenu.add_command(label="ARC_3p  A>3", command=functools.partial(self.keypressed,event='<tkinter.Event object>', char1=['a','3']))
        self.menubar.add_cascade(label="Draw", menu=self.drawmenu)

        self.snappmenu = Menu(self.menubar, tearoff=0)
        self.snappmenu.add_command(label="Point   S>P", command=functools.partial(self.keypressed,event='<tkinter.Event object>', char1=['s','p']))
        self.snappmenu.add_command(label="NoSnapp S>O", command=functools.partial(self.keypressed,event='<tkinter.Event object>', char1=['s','o']))
        self.menubar.add_cascade(label="Snapp", menu=self.snappmenu)

        self.helpmenu = Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label="Help", command=passit())
        self.helpmenu.add_command(label="About...", command=passit())
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)

        self.root.config(menu=self.menubar)

        self.filebox = Combobox(root, textvariable=self.filevar, values=self.openfiles, state='readonly')
        self.filebox.current(0)
        self.colorbox = Combobox(root, textvariable=self.colorvar, values=self.colors, state='readonly')
        self.colorbox.current(data.data[0][0])
        self.draw = Canvas(root, cursor="none", width=self.WidthHeight[0], height=self.WidthHeight[1])
        self.label1 = Label(root, textvariable = self.mode, bg="white", fg="black")
        self.label2 = Label(root, textvariable = self.xy1, bg="white", fg="black")
        self.label3 = Label(root, textvariable = self.scroll, bg="white", fg="black")
        self.label4 = Label(root, text = "Tools", bg="white", fg="black")

        self.xyzgroup = LabelFrame(root, text="Insert", padx=5, pady=5,width=100,height=self.WidthHeight[1])
        self.ID = Label(self.xyzgroup,text="Id:")
        self.IdE = Entry(self.xyzgroup, textvariable = self.IdEntry)
        self.XT = Label(self.xyzgroup,text="X:")
        self.XE = Entry(self.xyzgroup, textvariable = self.XEntry)
        self.YT = Label(self.xyzgroup,text="Y:")
        self.YE = Entry(self.xyzgroup, textvariable = self.YEntry)
        self.ZT = Label(self.xyzgroup,text="Z:")
        self.ZE = Entry(self.xyzgroup, textvariable = self.ZEntry)
        self.CT = Label(self.xyzgroup,text="Code:")
        self.CE = Entry(self.xyzgroup, textvariable = self.CodeEntry)
        self.ok = Button(self.xyzgroup, text='Add', command = self.OkRespons)

        self.draw.bind("<Motion>",functools.partial(self.motion, WidthHeight=self.WidthHeight, moving = 0))
        self.draw.bind("<Button-1>", self.MouseRespons )

        self.draw.bind_all("<KeyPress>", functools.partial(self.keypressed, char1='none'))

        # Scrollwheel        
        self.draw.bind("<MouseWheel>", functools.partial(self.motion, WidthHeight=self.WidthHeight, moving = 2)) #win/osx
        self.draw.bind("<Button-4>", functools.partial(self.motion, WidthHeight=self.WidthHeight, moving = 2)) #linux
        self.draw.bind("<Button-5>", functools.partial(self.motion, WidthHeight=self.WidthHeight, moving = 2)) #linux
        # middlebutton + move
        self.draw.bind("<B2-Motion>",functools.partial(self.motion, WidthHeight=self.WidthHeight, moving=1))


        self.filebox.bind("<<ComboboxSelected>>", lambda f: self.colorbox.current(data.data[self.filebox.current()][0]))
        self.colorbox.bind("<<ComboboxSelected>>", lambda c: data.change_color(self.filebox.current(),self.colorbox.current()))

        self.filebox.grid(row=0, rowspan = 1, column=2, columnspan=1, sticky=W+E)
        self.colorbox.grid(row=0, rowspan = 1, column=3, columnspan=1, sticky=W+E)
        self.draw.grid(row=1,column=2, columnspan=9, sticky=W+E)

        self.xyzgroup.grid(row=1, column=0, columnspan=2, sticky=W+E+N)
        self.ID.grid(row=0, rowspan = 1,column=0, columnspan=1)
        self.IdE.grid(row=0, rowspan = 1,column=1, columnspan=1)
        self.XT.grid(row=1, rowspan = 1,column=0, columnspan=1)
        self.XE.grid(row=1, rowspan = 1,column=1, columnspan=1)
        self.YT.grid(row=2, rowspan = 1,column=0, columnspan=1)
        self.YE.grid(row=2, rowspan = 1,column=1, columnspan=1)
        self.ZT.grid(row=3, rowspan = 1,column=0, columnspan=1)
        self.ZE.grid(row=3, rowspan = 1,column=1, columnspan=1)
        self.CT.grid(row=4, rowspan = 1,column=0, columnspan=1)
        self.CE.grid(row=4, rowspan = 1,column=1, columnspan=1)
        self.ok.grid(row=5, rowspan = 1,column=1, columnspan=1)


        self.label4.grid(row=0, rowspan = 1, column=0, columnspan=2, sticky=W+E)
        self.label1.grid(row=2, rowspan = 1, column=2, columnspan=1, sticky=W+E)
        self.label2.grid(row=2, rowspan = 1, column=3, columnspan=1, sticky=W+E)
        self.label3.grid(row=2, rowspan = 1, column=4, columnspan=1, sticky=W+E)

        self.root.resizable(0,0)

        self.draw.focus_set()

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

    def keypressed(self,event,char1): # Short commands
        print(event)
        if char1 == 'none':
            chars = [event.char]

        else:
            chars = char1

        command_sel = {
            "nn": "none", "nn": "none",
            "d" : "Draw:","dp": "Draw: Point", "dl" : "Draw: Line",
            "a" : "Arc:", "a3" : "Arc: 3point",
            "s" : "Snapp:", "sp": "Snapp: Point", "so":"Snapp: Off"
            }

        for char in chars:
            if char == chr(27):
                self.draw.focus_set()
                self.mode.set("")
                del self.keyes_w[:]
                del self.keyes[:]
                del self.snapp[:]
                self.keyes_w.append(0)
                self.keyes_w.append(0)
                self.keyes.append("nn")
                self.snapp.append("so")
                self.new[0] = 1


            else:
                if self.draw.focus_get()== self.draw:
                    if len(self.keyes_w) == 2 :
                        if char == "n": # flag for new object
                            self.new[0] = 1
                        elif char not in command_sel:
                            print("not in dict")
                        else:
                            del self.keyes_w[:]
                            self.keyes_w.append(char)


                    elif len(self.keyes_w) == 1:
                        self.keyes_w.append(char)

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

    def MouseRespons(self,event):
        if self.snapp[0] != 'so' and len(data.data[self.filebox.current()][3][0]) == 0:
            pass
        else:
            data.paint(self.IdE.get(),int(self.Map_XY[0]),int(self.Map_XY[1]),0, self.CE.get(), self.keyes, self.snapp, self.new, self.filebox.current())
            self.new[0] = 0

    def OkRespons(self):
        if len(self.XE.get()) > 0 and len(self.YE.get()) > 0 and len(self.ZE.get()) > 0:
            data.paint(self.IdE.get(),int(float(self.XE.get())*1000),int(float(self.YE.get())*1000),int(float(self.ZE.get())*1000), self.CE.get(), self.keyes, self.snapp, self.new, self.filebox.current())
            self.new[0] = 0

    def numbers_val(self, *args):

        XE = self.XEntry.get()
        YE = self.YEntry.get()
        ZE = self.ZEntry.get()

        XEN = [""]
        YEN = [""]
        ZEN = [""]

        Xdott = False
        Ydott = False
        Zdott = False

        numbers = '0123456789.,'

        for char in XE:
            if char in numbers:
                if char == '.' or char == ',':
                    if Xdott == True:
                        pass
                    elif char == ',':
                        XEN[0] += '.'
                        Xdott = True
                    else:
                        XEN[0] += '.'
                        Xdott = True
                else:
                    XEN[0] += char

        for char in YE:
            if char in numbers:
                if char == '.' or char == ',':
                    if Ydott == True:
                        pass
                    elif char == ',':
                        YEN[0] += '.'
                        Ydott = True
                    else:
                        YEN[0] += '.'
                        Ydott = True
                else:
                    YEN[0] += char

        for char in ZE:
            if char in numbers:
                if char == '.' or char == ',':
                    if Zdott == True:
                        pass
                    elif char == ',':
                        ZEN[0] += '.'
                        Zdott = True
                    else:
                        ZEN[0] += '.'
                        Zdott = True
                else:
                    ZEN[0] += char


        self.XEntry.set(XEN[0])
        self.YEntry.set(YEN[0])
        self.ZEntry.set(ZEN[0])



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

        def findOjectNear():
            pass



        # Draws the shit.
        self.draw.delete(ALL) # Clear the canvas
        self.xy1.set("N = %0.3fm E = %0.3fm  " % (float(self.Map_XY[0])/1000,float(self.Map_XY[1])/1000))

        self.draw.create_rectangle(0, 0, WidthHeight[0], WidthHeight[1], fill="white")

        # Origo_lines
        self.draw.create_line(modifying_YtoX(0),modifying_XtoY(-10),modifying_YtoX(0),modifying_XtoY(zoomit(Canvas_YX[0])+ self.Map_XY[0]), fill="black", dash=(4,4))
        self.draw.create_line(modifying_YtoX(-10),modifying_XtoY(0),modifying_YtoX(zoomit(WidthHeight[0]-Canvas_YX[1])+ self.Map_XY[1]),modifying_XtoY(0), fill="black",dash=(4,4))


        # Arcfunction used in "DrawIt()"
        def tk_arc_calculate(arc1):

            oxy = []
            angels = []
            r1 = []
            coord = []
            check = []

            try:
                oxy.append((((arc1[3]**2-arc1[1]**2+arc1[2]**2-arc1[0]**2)/(2*(arc1[2]-arc1[0])))-((arc1[5]**2-arc1[3]**2+arc1[4]**2-arc1[2]**2)/(2*(arc1[4]-arc1[2]))))
                          /(((arc1[3]-arc1[5])/(arc1[4]-arc1[2]))-((arc1[1]-arc1[3])/(arc1[2]-arc1[0]))))

                oxy.append((oxy[0]*((arc1[1]-arc1[3])/(arc1[2]-arc1[0])))+((arc1[3]**2-arc1[1]**2+arc1[2]**2-arc1[0]**2)/(2*(arc1[2]-arc1[0]))))
            except ZeroDivisionError:
                oxy.append((arc1[1]+arc1[5])/2)
                oxy.append((arc1[0]+arc1[4])/2)



            oxy.reverse()

            r1.append(math.sqrt((arc1[1]-oxy[1])**2+(arc1[0]-oxy[0])**2)) # Radius
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
            

            return [coord, angels,r1,oxy]

        # Arcfunction for large radius

        def Arc_as_line(center_x,center_y,radius,start,extent):

            points = []
            slices = int(radius) * 2

            if extent < 0:
                start,extent = extent + start,start 
                
                
            elif extent > 0:
                extent += start
                if extent > 360:
                    extent -= 360

            start,extent = 360 - extent,360 - start
            
                    
            currentAngle = start  * (math.pi*2)/360 # startAngle in radians
            endAngle = extent * (math.pi*2)/360 # endAngle in radians

            def findxy(center_x,center_y,radius,currentAngle,endAngle,slices):
                
                for i in range(slices):
                    px = center_x + radius * math.cos(currentAngle) 
                    py = center_y + radius * math.sin(currentAngle)
                    points.append((int(px), int(py)))
                    currentAngle += ((math.pi*2)/slices)
                    if currentAngle >= endAngle:
                        px = center_x + radius * math.cos(endAngle) 
                        py = center_y + radius * math.sin(endAngle)
                        points.append((int(px), int(py)))
                        break

            if currentAngle >= endAngle:
                
                findxy(center_x,center_y,radius,currentAngle,math.pi*2,slices)
                findxy(center_x,center_y,radius,0,endAngle,slices)

            else:
                findxy(center_x,center_y,radius,currentAngle,endAngle,slices)

            return points


        
        # Draw everything
        for file in range(len(data.data)):

            current = self.filebox.current()

               
            def DrawIt():
                index = len(data.data[file][3][5])
                linexy = [] # For linedraw
                arc1 = []
                tk_arc = []
                

                for x,y,thetype in zip(data.data[file][3][1],data.data[file][3][2],data.data[file][3][5]):

                    # Draw points
                    if thetype == "dp":
                        self.draw.create_oval(modifying_YtoX(y) - 2 , modifying_XtoY(x) - 2 , modifying_YtoX(y) + 2, modifying_XtoY(x) + 2, fill=self.colors[data.data[file][0]])

                
                    # Draw lines       
                    if thetype == "dl":
                        linexy.append(modifying_YtoX(y))
                        linexy.append(modifying_XtoY(x))
                                
                    elif thetype == "/dl":
                        linexy.append(modifying_YtoX(y))
                        linexy.append(modifying_XtoY(x))
                                 
                        self.draw.create_line(linexy,fill=self.colors[data.data[file][0]])
                        del linexy
                        linexy = []

                    # Draw arcs
                    
                        
                    if thetype == "a3":
                        arc1.append(modifying_YtoX(y))
                        arc1.append(modifying_XtoY(x))

                    elif thetype == "/a3":
                        arc1.append(modifying_YtoX(y))
                        arc1.append(modifying_XtoY(x))


                        tk_arc = tk_arc_calculate(arc1)
  
                        #self.draw.create_arc(tk_arc[0],start=tk_arc[1][0],extent=tk_arc[1][1], style="arc", outline=self.colors[data.data[file][0]])
                        if tk_arc[2][0] > 1:                             
                            arcline = Arc_as_line(tk_arc[3][0],tk_arc[3][1],tk_arc[2][0],tk_arc[1][0],tk_arc[1][1])
                            self.draw.create_line(arcline,fill=self.colors[data.data[file][0]])
                            arcline = []

                        tk_arc = []
                        arc1 = []
                            

                
                # If only one linepoint paint dott        
                if index > 0:
                    if data.data[file][3][5][index - 1] == "dl":
                        self.draw.create_oval(modifying_YtoX(y) - 2 , modifying_XtoY(x) - 2 , modifying_YtoX(y) + 2, modifying_XtoY(x) + 2, fill=self.colors[data.data[file][0]])

                # Draw last linepoint to cross
                if file == current:
                    if index >= 1: 
                        if self.keyes[0] == "dl" and self.new[0] == 0 and data.data[file][3][5][index - 1] == "/dl" or data.data[file][3][5][index - 1] == "dl":
                            linexy.append(modifying_YtoX(data.data[file][3][2][index - 1]))
                            linexy.append(modifying_XtoY(data.data[file][3][1][index - 1]))
                            linexy.append(Canvas_YX[1])
                            linexy.append(Canvas_YX[0])
                            self.draw.create_line(linexy,fill=self.colors[data.data[file][0]])

                # Draw arc as you paint
                if len(data.arc) == 6 and self.Map_XY[0] != data.arc[0] and self.Map_XY[1] != data.arc[1] and self.Map_XY[0] != data.arc[3] and self.Map_XY[1] != data.arc[4] and (
                    data.arc[0]*(data.arc[4]-self.Map_XY[1])
                    + data.arc[3]*(self.Map_XY[1]-data.arc[1])
                    + self.Map_XY[0]*(data.arc[1]-data.arc[4])
                    ) != 0:
                       
                    tk_arc = tk_arc_calculate([modifying_YtoX(data.arc[1]),modifying_XtoY(data.arc[0]),
                                               modifying_YtoX(data.arc[4]),modifying_XtoY(data.arc[3]),
                                               modifying_YtoX(self.Map_XY[1]),modifying_XtoY(self.Map_XY[0])])
                    #self.draw.create_arc(tk_arc[0],start=tk_arc[1][0],extent=tk_arc[1][1], style="arc", outline=self.colors[data.data[file][0]])
                    
                    if tk_arc[2][0] > 1:                             
                            arcline = Arc_as_line(tk_arc[3][0],tk_arc[3][1],tk_arc[2][0],tk_arc[1][0],tk_arc[1][1])
                            self.draw.create_line(arcline,fill=self.colors[data.data[file][0]])
                            print(len(arcline))
                            arcline = []
                
                # Crosshair
                self.draw.create_line(Canvas_YX[1], 0, Canvas_YX[1], WidthHeight[1], fill="black")
                self.draw.create_line(0, Canvas_YX[0], WidthHeight[0], Canvas_YX[0], fill="black")
                self.draw.create_rectangle(Canvas_YX[1] - 10,Canvas_YX[0] - 10,Canvas_YX[1] + 10 ,Canvas_YX[0] + 10, outline="black")


        
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
