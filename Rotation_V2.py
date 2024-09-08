### Imports
import os
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 
from datetime import datetime, date, timedelta
from monthdelta import monthdelta
from tkinter import *

### Fonctions

def csv_to_table(t):
    T = t.split()
    return [k.split(";") for k in T]

def read_csv(d, file):
    t = open(d + "/" + file, "r").read()
    return csv_to_table(t)

def get_time(j):
    return datetime.strptime(j, "%Y-%m-%d").date()

def in_int(current, d, f):
    delta = f-d
    date_list = [d + timedelta(days=x) for x in range(delta.days+1)]
    return current in date_list

def ligne(n, d):
    l = []
    for k in range(n):
        directory = d + "/Ligne_" + str(k + 1)
        for i in os.listdir(directory):
            l += [read_csv(directory, i)]
    return l

def ajout_planche(d, h, length, answer, Year):
    if '' in answer:
        return 'Champ vide'
    
    nb = int(answer[-1])
    answer = answer[:-1]
    for k in range(5, 9):
        answer[k] = str(datetime.strptime(answer[k] + '-' + Year, '%d-%m-%Y').date())
    x = float(answer[h.index("x_planche")])
    L = float(answer[h.index("l_planche")])
    
    
    for k in range(nb):
        add = x
        add += k*(L + 0.2)
        answer[2] = round(add, 2)
        file = open(d + "/Ligne_" + answer[0] + "/" + str(answer[2]) + ".csv", "a")
        head = len(open(d + "/Ligne_" + answer[0] + "/" + str(answer[2]) + ".csv", "r").read())
        if head == 0:
            for i in range(len(h)):
                if i == len(h) - 1:
                    file.write(h[i])
                else :
                    file.write(h[i] + ";")
            file.write("\n")
        for i in range(len(answer)):
            if i == len(answer) - 1:
                file.write(str(answer[i]))
            else:
                file.write(str(answer[i]) + ";")
        file.write("\n")
        
        file.close()
    return 'Success'


def nb_planches(h, length, answer):
    x = float(answer[h.index("x_planche")])
    L = float(answer[h.index("l_planche")])
    m =int((length - x)/(L+0.2))
    return m


def delete_planche(l, d, di, n, leg):
    
    lgn = select_planche(n, l, d)
    for k in lgn:
        delete = ''
        if k[1] == leg:
            for i in k:
                delete += i + ';'
            delete = delete[:-1] + '\n'
            f = open(di + "/Ligne_" + k[0] + "/" + k[2] + ".csv", "r")
            file_data = f.read()
            f.close()

            file_data = file_data.replace(delete, '')

            file = open(di + "/Ligne_" + k[0] + "/" + k[2] + ".csv", "w")
            file.write(file_data)
            file.close()
        

def select_ligne(n, l):
    lgn = []
    for k in l:
        for i in range(1, len(k)):
            if int(k[i][0]) == n:
                lgn += [k[i]]
    return lgn

def select_planche(n, l, d):
    lgn = []
    for k in l:
        for i in range(1, len(k)):
            if int(k[i][0]) == n:
                if d.month in [k for k in range(get_time(k[i][5]).month, get_time(k[i][8]).month + 1)]:
                    lgn += [k[i]]
    return lgn
    


def plot_ligne(n, l, d, i):
    lgn = select_planche(n, l, d)
    intervention = [[0 for j in range(len(lgn) + 2)] for k in range(5, 9)]
    col = ["white", "y", "g", "r"]
     
    for k in range(len(lgn)):
        for j in range(5, 9):
            if get_time(lgn[k][j]).month == d.month:
                intervention[j - 5][k+1] = [get_time(lgn[k][j]).day]
        if get_time(lgn[k][5]).month <= d.month < get_time(lgn[k][7]).month :
            intervention[2][k+1] = (d + monthdelta(1) - d).days

    x = [0] + [float(k[2]) + float(k[3])/2 for k in lgn] + [120]
    width = [0.1] + [float(k[3]) for k in lgn] + [0.1]
    lab = [""] + [k[1] for k in lgn] + [""]
    for k in range(len(x)):
        rep = x.count(x[k])
        if  rep > 1 :
            w = width[k]
            f = [x[k+1:].index(x[k]) + k + 1]
            tp = x
            for i in range(rep - 2):
                tp = tp[f[-1]+1:]
                f += [tp.index(x[k])]
            reposi = w*(-1/2 + 1/(2*rep))
            x[k] += reposi
            width[k] = w/rep
            lab[k] = lab[k][:3]
            for i in range(1, rep):
                x[f[i-1]] += reposi + i*(w/rep)
                width[f[i-1]] = w/rep
                lab[k] += '-' + lab[f[i-1]][:3]
                lab[f[i-1]] = ''
                   
    return x, intervention, width, lab, col
    
    
    
class MyWindow:
    
    def __init__(self, win):
        
        #Paramètres
        
        self.L = 120
        self.Year = '2022'
        self.header = ["ligne", "nom", "x_planche", "l_planche", "intra_rang", "d_cycle", "f_semis", "d_récolte", "f_cylce"]
        self.dir = "/home/tristang/Documents/Outils info/Python/Rotation Maraîchage"
        self.date = datetime.strptime("01-01-" + self.Year, '%d-%m-%Y').date()
        self.p = 1
        
        self.lignes = ligne(9, self.dir)
        
        # Widgets
        
        self.lbl1=Label(win, text='1ère ligne')
        self.lbl1.place(x=85, y=120)
        
        self.lbl2 = Label(win, text='Mois')
        self.lbl2.place(x=212, y=120)
        
        
        self.txt1 = StringVar()
        self.lb3 = Label(win, textvariable=self.txt1, fg = 'blue')
        
        self.txt2 = StringVar()
        self.txt2.set("Ajout légume")
        self.lb4 = Label(win, textvariable=self.txt2)
        self.lb4.place(x=85, y=380)
        
        self.lb = []
        self.t = []
        for k in range(len(self.header)):
             
            self.lb += [Label(win, text = self.header[k])]
            self.lb[-1].place(x = 85, y = 400 + k*45)
            if k == 0:
                self.t += [Entry(win, bd=2)]
                self.t[-1].bind("<FocusOut>" , self.occupe)
                self.t[-1].place(x = 85, y = 420 + k*45)  
            else:
                self.t += [Entry(win, bd=2)]
                self.t[-1].place(x = 85, y = 420 + k*45)
                
        self.txt3 = StringVar()
        self.txt3.set("Nb_planches")
        self.lb += [Label(win, textvariable = self.txt3)]
        self.lb[-1].place(x = 85, y = 810)
        self.t += [Entry(win, bd=2)]
        self.t[-1].bind("<FocusIn>", self.max_p)
        self.t[-1].place(x = 85, y = 830)
        
        self.txt4 = StringVar()
        self.lb5 = Label(win, textvariable=self.txt4, fg = 'blue')
            
        self.btn1=Button(window, text="Ajouter", command = self.add)
        self.btn1.place(x=30, y=900)
        
        self.btn2=Button(window, text="Supprimer", command = self.delete)
        self.btn2.place(x=30, y=960)
        
        self.s1 = Scale(win, from_= 1, to = 12, length = 200)
        self.s1.bind("<ButtonRelease-1>", self.updateTime)
        self.s1.place(x=200, y=150)
        
        self.s2 = Scale(win, from_= 1, to = 7, length = 200)
        self.s2.bind("<ButtonRelease-1>", self.updateBlock)
        self.s2.place(x=100, y=150)
        
        self.init_plot()
        
    def init_plot(self):
        self.fig = Figure(figsize = (12, 10),  dpi = 100) 
        
        self.plot1 = self.fig.add_subplot(131)
        self.plot2 = self.fig.add_subplot(132)
        self.plot3 = self.fig.add_subplot(133)
        
        colors = {'Semis':'y', 'Végétatif':'g', 'Récolte':'r'}
        labels = list(colors.keys())
        handles = [plt.Rectangle((0,0),1,1, color=colors[label]) for label in labels]
        self.fig.legend(handles, labels, loc = "upper right")
        
        self.canvas = FigureCanvasTkAgg(self.fig, master = window)   
        self.canvas.draw() 
    
        self.canvas.get_tk_widget().pack() 
  
    
    def update_plot(self):
        self.fig.suptitle(self.date.strftime("%B"), fontsize = 20)
        
        p1 = plot_ligne(self.p, self.lignes, self.date, 0)
        p2 = plot_ligne(self.p+1, self.lignes, self.date, 1)
        p3 = plot_ligne(self.p+2, self.lignes, self.date, 2)
        
        self.plot1.clear()
        self.plot2.clear()
        self.plot3.clear()
        
        for k in range(len(p1[1])):
            self.plot1.barh(p1[0], p1[1][-(k+1)], p1[2], tick_label = p1[3], color = p1[4][-(k+1)])
            self.plot2.barh(p2[0], p2[1][-(k+1)], p2[2], tick_label = p2[3], color = p2[4][-(k+1)])
            self.plot3.barh(p3[0], p3[1][-(k+1)], p3[2], tick_label = p3[3], color = p3[4][-(k+1)])
          
        self.canvas.draw() 
        
        
    def updateTime(self, event):
        self.date += monthdelta(self.s1.get() - self.date.month)
        
        self.update_plot()
        
    def updateBlock(self, event):
        self.p = self.s2.get()
        
        self.update_plot()
        
    def add(self):
        self.lb3.place_forget()
        result = ajout_planche(self.dir, self.header, self.L, [k.get() for k in self.t], self.Year)
        [k.delete(0, 'end') for k in self.t]
        self.txt1.set(result)
        self.lb3.place(x=135, y=905)
        if result == 'Success':
            self.lignes = ligne(9, self.dir)
            self.update_plot()
            
    def delete(self):
        if ('' == self.t[0].get()) or ('' == self.t[1].get()):
            print("Champs vides")
            self.txt4.set("Champs vides")
            self.lb5.place(x=135, y=965)
        else:
            lgn = select_planche(int(self.t[0].get()), self.lignes, self.date)
            count = 0
            for k in lgn:
                    if k[1] == self.t[1].get():
                        count = 1
            if count == 1:                        
                delete_planche(self.lignes, self.date, self.dir, int(self.t[0].get()), self.t[1].get())
                self.lignes = ligne(9, self.dir)
                self.update_plot()
                self.txt4.set("Supprimé")
                self.lb5.place(x=135, y=965)
            else:
                print("Légume non présent")
                self.txt4.set("Légume non présent")
                self.lb5.place(x=135, y=965)
            
    def occupe(self, event):
        g = self.t[0].get()
        if g in [str(k+1) for k in range(9)]:
            li = select_ligne(int(g), self.lignes)
            self.txt2.set(str(sorted([float(li[i][2]) for i in range(len(li))]))) 
        else:
            self.txt2.set('Ligne Inexistante') 
            
    def max_p(self, event):
        maxp = nb_planches(self.header, self.L, [k.get() for k in self.t[:-1]])
        self.txt3.set("Nb_planches (max " + str(maxp) + ")")
        
            

        
       


### Script
        
# GUI
window=Tk()
mywin=MyWindow(window)
window.title('Planification Block')
window.geometry("1920x1080+30+30")
window.mainloop()

