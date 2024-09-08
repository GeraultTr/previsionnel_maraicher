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

def win2():
    global window2
    window2 = Tk()
    
def win3():
    global window3
    window3 = Tk()

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
    for k in range(len(answer) - 5, len(answer)):
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
                if d.month in [k for k in range(get_time(k[i][len(k[i])-5]).month, get_time(k[i][len(k[i])-1]).month + 1)]:
                    lgn += [k[i]]
    return lgn
    


def plot_ligne(n, l, d, i):
    lgn = select_planche(n, l, d)
    intervention = [[0 for j in range(len(lgn) + 2)] for k in range(4)]
    col = ["white", "y", "g", "r"]
     
    for k in range(len(lgn)):
        for j in range(4):
            if get_time(lgn[k][j+9]).month == d.month:
                intervention[j][k+1] = [get_time(lgn[k][j+9]).day]
        if get_time(lgn[k][len(lgn[k])-4]).month <= d.month < get_time(lgn[k][len(lgn[k])-3]).month :
            intervention[1][k+1] = (d + monthdelta(1) - d).days
        if get_time(lgn[k][len(lgn[k])-3]).month <=d.month < get_time(lgn[k][len(lgn[k])-2]).month :
            intervention[2][k+1] = (d + monthdelta(1) - d).days
        if get_time(lgn[k][len(lgn[k])-2]).month <=d.month < get_time(lgn[k][len(lgn[k])-1]).month :
            intervention[3][k+1] = (d + monthdelta(1) - d).days

    x = [0] + [float(k[2]) + float(k[3])/2 for k in lgn] + [120]
    width = [0.1] + [float(k[3]) for k in lgn] + [0.1]
    lab = [""] + [k[1] for k in lgn] + [""]
    
    for k in range(1, len(lgn)):
        if intervention[0][k] == 0 and intervention[1][k] == 0 and intervention[2][k] == 0 and intervention[3][k] == 0:
            lab[k] = ''


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
    
def tot_legume(l, d, h, leg):
    ct = 0
    dnb = 1
    for k in range(9):
        lgn = select_planche(k+1, l, d)
        for i in lgn:                     
            if get_time(i[-5]).month == get_time(i[-4]).month:
                tp = [get_time(i[-5]).month]
            else:
                tp = [get_time(i[-5]).month, get_time(i[-4]).month]
            if i[1] == leg and d.month in tp and get_time(i[-5]) != get_time(i[-4]):
                info = i
                ct +=1
                if len(tp) == 2:
                    if d.month == get_time(i[-5]).month:
                        dnb = ((d + monthdelta(1) -get_time(i[-5])).days - 1) / (get_time(i[-4]) - get_time(i[-5])).days
                    else:
                        dnb = (get_time(i[-4]) - d).days / (get_time(i[-4]) - get_time(i[-5])).days
            
                        
    if ct == 0:
        return 0
    else:
        totli = 20/float(info[h.index('intra_rang')])
        totpl = int(info[h.index('Nb_rangs')])*totli
        totplmois = int(totpl*dnb)
        
        return ct*totplmois

### Classes

###  
    
class Block:
    
    def __init__(self, win):
        
        #Paramètres
        
        self.L = 120
        self.Year = '2022'
        self.header = ["ligne", "nom", "x_planche", "l_planche", "Nb_rangs", "inter_rang", "intra_rang", "déphasage", "d_cycle_serre", "d_cycle_champ", "f_semis", "d_récolte", "f_cylce"]
        self.dir = "/home/tristangrlt/Documents/Outils info/Python/Rotation Maraîchage"
        self.date = datetime.strptime("01-01-" + self.Year, '%d-%m-%Y').date()
        self.p = 1
        
        self.lignes = ligne(9, self.dir)
        
        # Widgets
        
        #Label Scale
        self.lbl1=Label(win, text='1ère ligne')
        self.lbl1.place(x=85, y=20)
        
        self.lbl2 = Label(win, text='Mois')
        self.lbl2.place(x=212, y=20)
        
        #Label Var
        self.txt1 = StringVar()
        self.lb3 = Label(win, textvariable=self.txt1, fg = 'blue')
        
        self.txt2 = StringVar()
        self.txt2.set("Ajout légume")
        self.lb4 = Label(win, textvariable=self.txt2)
        self.lb4.place(x=30, y=380)
        
        #Entry fields et leurs Label
        self.lb = []
        self.t = []
        for k in range(len(self.header)):
            a, c = 0, 0
            seuil = 6
            if k > seuil:
                a = 140
                c = 1
            self.lb += [Label(win, text = self.header[k])]
            self.lb[-1].place(x = 30 + a, y = 400 + k*45 -c*(seuil+1)*45)
            if k == 0:
                self.t += [Entry(win, bd=2, width = 15)]
                self.t[-1].bind("<FocusOut>" , self.occupe)
                self.t[-1].place(x = 30 + a, y = 420 + k*45-c*(seuil+1)*45)  
            elif k == 1:
                self.t += [Entry(win, bd=2, width = 15)]
                self.t[-1].bind("<FocusOut>" , self.profile)
                self.t[-1].place(x = 30 + a, y = 420 + k*45-c*(seuil+1)*45)
            else:
                self.t += [Entry(win, bd=2, width = 15)]
                self.t[-1].place(x = 30 + a, y = 420 + k*45-c*(seuil+1)*45)
                
        self.txt3 = StringVar()
        self.txt3.set("Nb_planches")
        self.lb += [Label(win, textvariable = self.txt3)]
        self.lb[-1].place(x = 30, y = 810)
        self.t += [Entry(win, bd=2, width = 15)]
        self.t[-1].bind("<FocusIn>", self.max_p)
        self.t[-1].place(x = 30, y = 830)
        
        self.txt4 = StringVar()
        self.lb5 = Label(win, textvariable=self.txt4, fg = 'blue')
        
        #Buttons
        self.btn1=Button(window, text="Ajouter", command = self.add)
        self.btn1.place(x=30, y=900)
        
        self.btn2=Button(window, text="Supprimer", command = self.delete)
        self.btn2.place(x=30, y=940)
        
        # self.btn3=Button(window, text="Maille", command = self.plot_maille)
        # self.btn3.place(x=1600, y=900)
        
        self.btn4=Button(window, text="Semis serre", command = self.plot_serre)
        self.btn4.place(x=1700, y=900)
        
        #Sliders
        self.s1 = Scale(win, from_= 1, to = 12, length = 300, command = self.updateTime)
        self.s1.place(x=200, y=50)
        
        self.s2 = Scale(win, from_= 1, to = 7, length = 300, command = self.updateBlock)
        self.s2.place(x=100, y=50)
        
        #Listbox
        self.lbl1=Label(win, text='Profiles')
        self.lbl1.place(x=1650, y=170)
        
        self.lstb1 = Listbox(win)
        self.lstb1.bind("<Double-Button-1>", self.legume_details)
        self.lstb1.place(x = 1600, y = 200)
        
        self.lbl2=Label(win, text='Combinaisons')
        self.lbl2.place(x=1650, y=400)
        
        self.lstb2 = Listbox(win)
        self.lstb2.bind("<Double-Button-1>", self.plot_maille)
        self.lstb2.place(x = 1600, y = 430)
        
        #Init Functions
        self.init_plot()
        self.update_plot()
        self.update_listb()
        
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
            
        
        self.update_listb2(p1, p2, p3)
        
        self.canvas.draw() 
        
        
    def update_listb(self):
        self.lstb1.delete(0,END)
        self.lignes = ligne(9, self.dir)
        
        tlegumes = []
        for k in self.lignes:
            for i in k:
                tlegumes +=[i[1]]
        while 'nom' in tlegumes:
            tlegumes.remove('nom')
        used = []
        self.legumes = sorted([k for k in tlegumes if k not in used and (used.append(k) or True)])
        
        for k in range(len(self.legumes)):
            self.lstb1.insert(k+1, self.legumes[k])
            
    def update_listb2(self, p1, p2, p3):
        
        output = set()
        for x in p1[3] + p2[3] + p3[3]:
            output.add(x)
        output = list(output)
        while '' in output:
            output.remove('')
        self.combi = [sorted(output)] + [[[] for k in range(len(output))]]
        
        lgn1 = select_planche(self.p, self.lignes, self.date)
        lgn2 = select_planche(self.p+1, self.lignes, self.date)
        lgn3 = select_planche(self.p+2, self.lignes, self.date)
        x = [k[2] for k in lgn1] + [k[2] for k in lgn2] + [k[2] for k in lgn3]
        lab = [k[1] for k in lgn1] + [k[1] for k in lgn2] + [k[1] for k in lgn3]
        
        for k in range(len(self.combi[0])):
            if self.combi[0][k] in lab:
                self.combi[1][k] += [self.combi[0][k]]
            else:
                rep = self.combi[0][k].count('-')
                tp = [k[:3] for k in lab]
                for j in range(rep+1):
                    self.combi[1][k] += [lab[tp.index(self.combi[0][k][4*j :4*j+3])]]
        
        self.lstb2.delete(0,END)
        for k in range(len(self.combi[0])):
            self.lstb2.insert(k+1, self.combi[0][k])
        
        
        
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
            self.update_listb()
            
    def delete(self):
        if ('' == self.t[0].get()) or ('' == self.t[1].get()):
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
                self.update_listb()
                self.txt4.set("Supprimé")
                self.lb5.place(x=135, y=965)
            else:
                self.txt4.set("Légume non présent")
                self.lb5.place(x=135, y=965)
        
        
    def plot_serre(self):
        x = [[0 for j in range(12)] for k in range(len(self.legumes))]
        for k in range(12):
            dtp = get_time(self.Year + '-' + str(k+1) + '-01')
            for j in range(len(self.legumes)):
                x[j][k] = tot_legume(self.lignes, dtp, self.header, self.legumes[j])
        win2()
        ser=Serre(window2, x, self.legumes)
        window2.title('Plannification des semis en serre')
        window2.geometry("1080x1080+30+30")
        window2.mainloop()
        
        
    def plot_maille(self, event):
        win3()
        ser=Maille(window3, self.combi, self.lstb2.get(ACTIVE))
        window3.title('Maille')
        window3.geometry("1080x1080+30+30")
        window3.mainloop()
                
    def occupe(self, event):
        g = self.t[0].get()
        if g in [str(k+1) for k in range(9)]:
            li = select_ligne(int(g), self.lignes)
            self.txt2.set(str(sorted([float(li[i][2]) for i in range(len(li))]))) 
        else:
            self.txt2.set('Ligne Inexistante') 
            
    def profile(self, event):
        leg = self.t[1].get()
        if leg in self.legumes:
            for k in self.lignes:
                for i in k:
                    if leg in i:
                        for j in range(3, len(self.t)-1):
                            self.t[j].delete(0, 'end')
                            if j > 7:
                                tp = get_time(i[j])
                                self.t[j].insert(0, str(tp.day) + '-' + str(tp.month))
                            else:
                                self.t[j].insert(0, i[j])
                        break
                else:
                    # Continue if the inner loop wasn't broken.
                    continue
                # Inner loop was broken, break the outer.
                break
            
            
    def max_p(self, event):
        maxp = nb_planches(self.header, self.L, [k.get() for k in self.t])
        self.txt3.set("Nb_planches (max " + str(maxp) + ")")
        
    def legume_details(self, event):
        self.t[1].delete(0, 'end')
        self.t[1].insert(0, self.lstb1.get(ACTIVE))
        self.profile(event)
    
        
 

### 
        
class Serre:
    
    def __init__(self, win2, x, leg):
        
        #Paramètres
        
        self.dir = "/home/tristangrlt/Documents/Outils info/Python/Rotation Maraîchage"
        self.lignes = ligne(9, self.dir)
        self.semis = x
        self.legumes = leg
        
        # Widgets
        
        self.init_plot()
        self.update_plot()
        
    def init_plot(self):
        self.fig = Figure(figsize = (12, 10),  dpi = 100) 
        
        self.plot = self.fig.add_subplot(111)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master = window2)   
        self.canvas.draw() 
    
        self.canvas.get_tk_widget().pack() 
        
    def update_plot(self):
        
        m = [(get_time('2022-01-01')+monthdelta(k)).strftime("%B")[:3] for k in range(12)]
        self.plot.bar(m, self.semis[0], label = self.legumes[0])
        
        bot = [0 for k in range(12)]
        for k in range(len(self.semis)-1):
            for i in range(12):
                bot[i] += self.semis[k][i]
            self.plot.bar(m, self.semis[k+1], bottom = bot, label = self.legumes[k+1])
            
        self.plot.set_ylabel('Semis mensuels')
        self.plot.legend()
        
        self.canvas.draw()
        
    
       
### 
        
class Maille:
    
    def __init__(self, win, combi, act):
        
        #Paramètres
        
        self.dir = "/home/tristangrlt/Documents/Outils info/Python/Rotation Maraîchage"
        self.lignes = ligne(9, self.dir)
        self.legume = combi
        self.act = []
        for k in range(len(self.legume[0])):
            if self.legume[0][k] == act:
                self.act = self.legume[1][k]
        
        # Widgets
        
        self.init_plot()
        self.update_plot()
        
    def init_plot(self):
        self.fig = Figure(figsize = (12, 10),  dpi = 100) 
        self.plot = self.fig.add_subplot(111)
        self.plot.set_facecolor('saddlebrown')
        
        ct = [0 for k in self.act]
        self.info = [0 for k in self.act]
        for k in self.lignes:
            for j in k:
                for i in range(len(self.act)):
                    if j[1] == self.act[i]:
                        if ct[i] == 0:
                            self.info[i] = j
                        ct[i] += 1
        
        self.canvas = FigureCanvasTkAgg(self.fig, master = window3)   
        self.canvas.draw() 
    
        self.canvas.get_tk_widget().pack() 
        
    def update_plot(self):
        for k in self.info:
            self.plot.set_xlim(0, float(k[3]))
            x, y = [], []
            for j in range(int(k[4])):
                for i in range(4):
                    x += [(float(k[3])/2) - ((int(k[4])-1)*float(k[5])/2) + j*float(k[5])]
                    y += [(i+j*float(k[7])/360)*float(k[6])]
                    self.plot.plot([x[-1], x[-1]], [-1, 10], color = 'white', linewidth = 0.1, linestyle='dotted')
            self.plot.plot(x, y, marker=".", markersize=20, linestyle = 'None', label = k[1] + ' ' + str(round(0.5*int(k[4])/float(k[6]), 1)) + '/m2')
            self.plot.set_ylim(min(y), max(y))
        self.plot.legend()
        self.canvas.draw()
        

### Script
        
# GUI
window=Tk()
blk=Block(window)
window.title('Planification Block')
window.geometry("1920x1080+30+30")
window.mainloop()

