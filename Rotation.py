### Imports
import os
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
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

def ajout_planche(d, h, length):
    global lignes, Year
    answer = []
    
    for k in range(len(h)):
        tp = input(h[k] + "? :")
        if k == 0:
            li = select_ligne(int(tp), lignes)
            print(sorted([float(li[i][2]) for i in range(len(li))]))
        answer += [tp]
    for k in range(5, 9):
        answer[k] = str(datetime.strptime(answer[k] + '-' + Year, '%d-%m-%Y').date())
    x = float(answer[h.index("x_planche")])
    L = float(answer[h.index("l_planche")])
    m =int((length - x)/(L+0.2))
    print(str(m) + " planches possibles.")
    nb = min(int(input("Combien de planches? :")), m)
    
    
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
        
def delete_planche(l, d, di):
    n = int(input("Quelle planche? :"))
    lgn = select_planche(n, l, d)
    leg = input("Quel légume? :")
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
    
def update_time(val):
    global lignes, date, p
    
    v = int(date_slider.val)
    date += monthdelta(v - date.month)
    plot_ligne(p, lignes, date, 0)
    plot_ligne(p+1, lignes, date, 1)
    plot_ligne(p+2, lignes, date, 2)


def plot_ligne(n, l, d, i):
    lgn = select_planche(n, l, d)
    plt.title(d.strftime("%B"), x = 0.55, y=30, fontsize=20)
    intervention = [[0 for j in range(len(lgn) + 2)] for k in range(5, 9)]
    col = ["white", "y", "g", "r"]
    
    colors = {'Semis':'y', 'Végétatif':'g', 'Récolte':'r'}
    labels = list(colors.keys())
    handles = [plt.Rectangle((0,0),1,1, color=colors[label]) for label in labels]
    plt.legend(handles, labels, loc = "upper right", bbox_to_anchor=(1.3,28))
    
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
                
    
    
    ax[i].clear()    
    for k in range(len(intervention)):
        ax[i].barh(x, intervention[-(k+1)], width, tick_label = lab, color = col[-(k+1)])
        


### Script

# Paramètres
L = 120
Year = '2022'
init = datetime.strptime("01-01-" + Year, '%d-%m-%Y').date()
header = ["ligne", "nom", "x_planche", "l_planche", "intra_rang", "d_cycle", "f_semis", "d_récolte", "f_cylce"]
dir = "/home/tristang/Documents/Outils info/Python/Rotation Maraîchage"


date = init
lignes = ligne(9, dir)


p = int(input("Première ligne? :"))

# GUI
#window=Tk()
##
#window.title('Planification Block')
#window.geometry("500x500+30+30")
#window.mainloop()

# Plot block

fig, ax = plt.subplots(1, 3)
fig.set_size_inches(18.5, 10.5)
axdate = plt.axes([0.15, 0.025, 0.65, 0.03])
date_slider = Slider(
        ax=axdate,
        label='Mois',
        valmin=1,
        valmax=12,
        valinit=date.month,
        valstep=1)


plot_ligne(p, lignes, date, 0)
plot_ligne(p+1, lignes, date, 1)
plot_ligne(p+2, lignes, date, 2)
date_slider.on_changed(update_time)
    
plt.show()

