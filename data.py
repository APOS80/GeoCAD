
import sys
import math
import pickle
import re

class CadData(object):

    def __init__(self):
        self.data =[
            [
            0,
            'Noname','',
            [[],[],[],[],[],[]]
            ]
            ]#color,filename,path//id,x,y,z,code,typecode

        self.arc = []
        self.snapp_xy = []
        
    def new_file(self):
        self.data.append(
            [
            0,
            'Noname_' + str(len(self.data)),
            '',
            [[],[],[],[],[],[]]
            ]
            )#color,filename,path//id,x,y,z,code,typecode

    def open_file(self,filepath):
        with open(filepath, 'rb') as handle:
            self.data.append(pickle.load(handle))
            

    def close_file(self,active_file):
        self.data.pop(active_file)
        #prompt for save or save as.

    def save_file(self,active_file,directory):
        if len(directory) > 0:
            self.data[active_file][2] = directory
            filename = re.findall(r'\w+(?=.cad)', directory, re.I)
            self.data[active_file][1] = filename[-1]
            
            with open(directory, 'wb') as handle:
                pickle.dump(self.data[active_file], handle)
            
            
            
        

    def save_close_all(self):
        pass
    
    def change_color(self, active_file, color):
        self.data[active_file][0] = color

    def paint(self, ide, MAP_X, MAP_Y, MAP_Z,code, keyes1, snapp, new, active_file): #Get values from gui.


        x = MAP_X
        y = MAP_Y
        z = MAP_Z

        

        # Catch Snapp Nerest
        if snapp[0] == "sp":
        
            maxl = 0
            minl = 0
            snapp_xy = []

            for xy in range(len(self.data[active_file][3][1])):
                l = math.sqrt((x - self.data[active_file][3][1][xy])**2+(y - self.data[active_file][3][2][xy])**2)
                if l > minl:
                    maxl = l
            minl = maxl

            

            for xyz in range(len(self.data[active_file][3][1])):
                l = math.sqrt((x - self.data[active_file][3][1][xyz])**2+(y - self.data[active_file][3][2][xyz])**2)
                if l <= minl:                
                    minl = l
                    del self.snapp_xy[:]
                    self.snapp_xy.append(self.data[active_file][3][1][xyz])
                    self.snapp_xy.append(self.data[active_file][3][2][xyz])
                    self.snapp_xy.append(self.data[active_file][3][3][xyz])

            
        

        # Fix one point lines
        if len(keyes1) == 1:
            
            if len(self.data[active_file][3][5]) > 0:
                if keyes1[0] != "dl" and self.data[active_file][3][5][len(self.data[active_file][3][5])-1] == "dl":
                    self.data[active_file][3][5][len(self.data[active_file][3][5])-1] = "dp"
                    print("did")

            
            # Point
            if keyes1[0] == "dp":
                del self.arc[:]
                self.data[active_file][3][0].append(ide)

                if snapp[0] == "sp":
                    self.data[active_file][3][1].append(self.snapp_xy[0])
                    self.data[active_file][3][2].append(self.snapp_xy[1])
                    self.data[active_file][3][3].append(self.snapp_xy[2])
                else:    
                    self.data[active_file][3][1].append(x)
                    self.data[active_file][3][2].append(y)
                    self.data[active_file][3][3].append(z)
                
                
                self.data[active_file][3][4].append(code)
                self.data[active_file][3][5].append("dp")

                
            # Line
            elif keyes1[0] == "dl":
                del self.arc[:]
                self.data[active_file][3][0].append(ide)

                if snapp[0] == "sp":
                    self.data[active_file][3][1].append(self.snapp_xy[0])
                    self.data[active_file][3][2].append(self.snapp_xy[1])
                    self.data[active_file][3][3].append(self.snapp_xy[2])
                else:    
                    self.data[active_file][3][1].append(x)
                    self.data[active_file][3][2].append(y)
                    self.data[active_file][3][3].append(z)

                
                self.data[active_file][3][4].append(code)
                
                index = len(self.data[active_file][3][5]) - 1
                
                
                if index >= 0:
                    if self.data[active_file][3][5][index] == "dl" or self.data[active_file][3][5][index] == "/dl" and new[0] == 0:
                        self.data[active_file][3][5].append("/dl")
                        self.data[active_file][3][5][index] = "dl"
                    else:
                        self.data[active_file][3][5].append("dl")
                else:
                    self.data[active_file][3][5].append("dl")

            # Arc
            elif keyes1[0] == "a3":   
                if len(self.arc) <= 9:
                        
                        if snapp[0] == "sp":
                            self.arc.append(self.snapp_xy[0])
                            self.arc.append(self.snapp_xy[1])
                            self.arc.append(self.snapp_xy[2])
                        else:    
                            self.arc.append(x)
                            self.arc.append(y)
                            self.arc.append(z)
                            
                        if len(self.arc) == 6 and self.arc[0] == self.arc[3] and self.arc[1] == self.arc[4]:
                            #print("no")
                            self.arc.pop()
                            self.arc.pop()
                            self.arc.pop()
                            
                        elif len(self.arc) == 9 and self.arc[0] == self.arc[6] and self.arc[1] == self.arc[7]:
                            #print("no")
                            self.arc.pop()
                            self.arc.pop()
                            self.arc.pop()
                            
                        elif len(self.arc) == 9 and self.arc[3] == self.arc[6] and self.arc[4] == self.arc[7]:
                            #print("no")
                            self.arc.pop()
                            self.arc.pop()
                            self.arc.pop()

                        elif len(self.arc) == 9 and (
                            self.arc[0]*(self.arc[4]-self.arc[7])
                            + self.arc[3]*(self.arc[7]-self.arc[1])
                            + self.arc[6]*(self.arc[1]-self.arc[4])
                            ) == 0:
                            print("no")
                            self.arc.pop()
                            self.arc.pop()
                            self.arc.pop()
                            
                if len(self.arc) == 9 :
                        print(self.arc)

                        i = 0    
                            
                        while i != 9:                 
                            self.data[active_file][3][0].append(ide)                
                            self.data[active_file][3][1].append(self.arc[0 + i])
                            self.data[active_file][3][2].append(self.arc[1 + i])
                            self.data[active_file][3][3].append(self.arc[2 + i])                
                            self.data[active_file][3][4].append(code)

                            if i == 6:
                                self.data[active_file][3][5].append("/a3")
                            else:
                                self.data[active_file][3][5].append("a3") 

                            i = i + 3
                        del self.arc[:]
                        
            else:
                pass
        else:
            pass


        print(self.data)
            
        return


