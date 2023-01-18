# -*- coding: utf-8 -*-
"""
Created on Fri Apr 27 00:11:44 2018

@author: Badr et oponcet: RocketWoman
Bienvenue dans cette simulation de lancée de notre fusée RocketWoman
"""
from matplotlib.widgets import Button, Slider
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.image as mi5 
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

condi=input("Vous voulez que le dessin soit bien dessiné (pas des\
bizzares ligne) ou vous voulez que vous soyez capable de répeter\
le dessin comme vous voulez?\n\
Si vous voulez voir des bons dessins mais pas pouvoir répeter l'opération\
 tapper yes.\nSi vous voulez répeter l'opération, tappez n'importe quoi\n\
                             ")

landingText = "The landing velocity is: %f\n\
and the threshold velocity is: %f"


stop = 10000
dt=0.2

factor= 1
g=-10*factor
ay=(0.1+10)*factor
ts=100*(-g/ay)
v_thresh=1*factor
restart = True
ys = 0.5*(ay+g)*ts**2
vs = (ay+g)*ts


tr = stop
retro_vie = tr + 10

xdata, ydata, vdata= [],[],[]


t_after = -2*vs/g
disc = vs**2 - 4 * 0.5*g * ys
t_free = (vs - np.sqrt(disc))/(2*0.5*g)
t_total = ts + t_after + t_free


fig = plt.figure("Badr")

#Axes:

#Premeir axe pour la fusée

xmax = 50
ymax = -0.5*(vs**2/g) + ys
ax = fig.add_axes([0.1,0.31,0.3,0.64],xlim=(-xmax,xmax), ylim=(0,ymax))
ax.set_title('Rocket Science')
if 1:
    rocket, = ax.plot([], [], marker='o', markersize=15)

#Deuxième axe pour la fonction de l'altidude dans le temps

ax1 = fig.add_axes([0.5,0.31,0.4,0.25])
ax1.set_xlim(0,t_total)
ax1.set_ylim(0,ymax)
ax1.grid()
ax1.set_title("Y(t)")
ax1.set_xlabel("Time(s)")
ax1.set_ylabel('Altitude(mm)')
graph, = ax1.plot([],[],'g',lw=2)

altitude_template = 'Altitude = %i m'
altitude_text = ax1.text(0,0,'')

#Troisième pour la fonction de la vitesse dans le temps

ax2 = fig.add_axes([0.5,0.7,0.4,0.25])
ax2.set_xlim(0,t_total)
ax2.set_ylim(0,vs)
ax2.set_title('V(t)')
ax2.set_ylabel('Velocity(mm/s)')
ax2.set_xlabel('Time(s)')
ax2.grid()
graphv, = ax2.plot([],[],'r',lw=2)

velocity_template = 'Velocity = %.2f m/s'
velocity_text = ax2.text(0,0,'')



img = mi5.imread("Rocket3.png")
imagebox = OffsetImage(img, zoom=0.05)

#Sliders:

#Premier slider pour l'accélération
axaccel  = plt.axes([0.25, 0.16, 0.65, 0.03], facecolor='beige')
Reg_accel = Slider(axaccel, u'Acceleration', -g,12*factor , valinit=ay)

def change2(val):
    global ay,vs,ys,ymax,ts,t_after,t_free,t_total
    
    ay = Reg_accel.val
    
    ts = 100 * (-g/ay)
    ys = 0.5*(ay+g)*ts**2
    vs = (ay+g)*ts
    t_after = -2*vs/g
    disc = vs**2 - 4 * 0.5*g * ys
    t_free = (vs - np.sqrt(disc))/(2*0.5*g)
    t_total = ts + t_after + t_free
    ymax = -0.5*(vs**2/g) + ys
    
    ax.set_ylim(0,ymax)
    ax1.set_xlim(0,t_total)
    ax1.set_ylim(0,ymax)
    ax2.set_xlim(0,t_total)
    ax2.set_ylim(0,vs)
    
    fig.canvas.draw_idle()

Reg_accel.on_changed(change2)
    
#Deuxième pour la vitesse seuil
axvseuil  = plt.axes([0.25, 0.22, 0.65, 0.03], facecolor='beige')
Reg_vseuil = Slider(axvseuil, u'Threshold Velocity', 0, 2*factor, valinit=v_thresh)

def change(val):    
    global v_thresh
    v_thresh = Reg_vseuil.val
    fig.canvas.draw_idle()

Reg_vseuil.on_changed(change)
#Troisième pour l'intervalle de temps
axtime  = plt.axes([0.25, 0.10, 0.65, 0.03], facecolor='beige')
Reg_time = Slider(axtime, u'Time Interval', 0, 2, valinit=dt)
def change3(val):

    global dt
    dt = Reg_time.val
    fig.canvas.draw.idle()

Reg_time.on_changed(change3)
    

#Boutons:    


def Restart(on_clicked):
    global restart, tr,xdata,ydata,vdata,retro_vie
    xdata,ydata,vdata=[],[],[]
    tr = stop
    retro_vie = tr+10
    
    if restart==False:
        restart = True
        ax.set_ylim(0,ymax)
        ax1.set_xlim(0,t_total)
        ax1.set_ylim(0,ymax)
        ax2.set_xlim(0,t_total)
        ax2.set_ylim(0,vs)
    else:
        restart = False
    print("ça fonction")
        
def Reset(on_clicked):
    
    Reg_vseuil.reset()
    Reg_accel.reset()
    Reg_time.reset()



#Premier bouton pour la "Rétro-Fusée"
engine_ax = plt.axes([0.25,0.015,0.2,0.05], facecolor='beige')
engine = Button(engine_ax ,('Rétro-Fusée'),color='c', hovercolor='g')
#Deuxième pour reset les sliders
reset_ax = plt.axes([0.65,0.015,0.2,0.05], facecolor='beige')
reset = Button(reset_ax, 'reset', color='c', hovercolor='r')
reset.on_clicked(Reset)
#Troisième pour pause and restart les graphiques
button2_ax = plt.axes([0.45, 0.015, 0.2, 0.05], facecolor='beige')
button2 = Button(button2_ax,('Pause - Restart'),color='c', hovercolor='w')
button2.on_clicked(Restart)


if 0:
    a=AnnotationBbox(imagebox, (0,0), frameon=False)
    ax.add_artist(a)

    
def setData():
    x=0
    y=0
    i=0
    while i < stop:
        if restart:
            if i<=ts:
                x = 0
                v = (ay+g)*i
                y+= v*dt
                #print('i<ts: %.3f %.3f %.3f'%(y,v,i))
                
            
            elif i>ts and i<tr:
                v = g*(i-ts) + vs
                y += v*dt
                #print('i>ts: %.3f %.3f %.3f'%(y,v,i))
                
                
                if i>0 and y<=0:
                    print(landingText%(np.abs(v),v_thresh))
                    if np.abs(v) <= v_thresh:
                        print("Good landing")
                    else:
                        print("Bad landing")
                    break 
            
            elif i>=tr and i<retro_vie:
                #v+= (ay+2+g)*dt
                y+= v*dt
                #print('i>tr: %.3f %.3f %.3f'%(y,v,i))
                
                if i>0 and y<=0:
                    print(landingText%(np.abs(v),v_thresh))
                    if np.abs(v) <= v_thresh:
                        print("C'est un succés, prochaine mission: vers \n\l'infini et au délà!")
                    else:
                        print("Houston, on a eu un GROS problème")
                    break
            elif i>=retro_vie and i>tr:
                v+= g*dt
                y+= v*dt
                #print('i<retro_vie: %.3f %.3f %.3f'%(y,v,i))
                if i>0 and y<=0:
                    print(landingText%(np.abs(v),v_thresh))
                    if np.abs(v) <= v_thresh:
                        print("C'est un succés, prochaine mission: vers \n\l'infini et au délà!")
                    else:
                        print("Houston, on a eu un GROS problème")
                    break
               
#            print(y,v,i)
                            
            yield x,y,v,ys,vs,i
        i+=dt
    
def update(setData):
    x,y,v,y_max,v_max,t = setData
    #print(y,t,v)
    xdata.append(t)
    ydata.append(y)
    vdata.append(np.abs(v))
    
    velocity_text.set_text(velocity_template%(v))
    altitude_text.set_text(altitude_template%(y))
    
    graph.set_data(xdata,ydata)
    graphv.set_data(xdata,vdata)
    if 1:
        rocket.set_data(x,y)
    
    def Engine(on_clicked):
        global tr, retro_vie
        tr = t
        retro_vie = tr+(ts/4)
        #print("happening",tr,t)

    engine.on_clicked(Engine)

    if 0:
        ax.cla()
        a=AnnotationBbox(imagebox, (x,y), frameon=False)
        ax.add_artist(a)
        ax.set_ylim((0,ymax))
        ax.set_xlim(-xmax,xmax)
        ax.set_title("Rocket science")
        ax.grid()
        
    yMin, yMax = ax1.get_ylim()
    Ymin, Ymax = ax.get_ylim()
    tmin, tmax = ax1.get_xlim()
    ymmax = 0.5*(-v_max**2/g) + y_max
    vmin, vmax = ax2.get_ylim()
    

    if y >= Ymax:
        ax.set_ylim(0, ymmax)
        ax1.set_ylim(yMin, ymax)
        ax.figure.canvas.draw()
        ax1.figure.canvas.draw()
        
    if t >= tmax:
        ax2.set_xlim(tmin, tmax+100)
        ax1.set_xlim(tmin, tmax+100)
        ax1.figure.canvas.draw()
        ax2.figure.canvas.draw()
          
    if np.abs(v) >= vmax:
        ax2.set_ylim(vmin, np.sqrt(vmax**2 - 2*g*ys))
        ax2.figure.canvas.draw()
       
def init():
    global xdata,ydata,vdata
    xdata,ydata,vdata=[],[],[]
    graph.set_data([],[])
    graphv.set_data([],[])
    return graph,graphv,

fig.canvas.draw_idle()

if condi=="yes":
    animation = FuncAnimation(fig,update,setData,interval=100,\
                          init_func=init,blit=False,repeat=True)
else:
    animation = FuncAnimation(fig,update,setData,interval=100,\
                          blit=False,repeat=True)
#animation.save('RocketOneTwoThree.mp4', fps = 5)
plt.show(animation)