from tkinter import *
import tkinter.ttk as ttk
from tkinter import colorchooser

import threading
import datetime as dt
import random as random
import PIL
from PIL import Image,ImageTk


import matplotlib
import matplotlib.figure as figure
import matplotlib.animation as animation
#import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

import serial
import time
from datetime import datetime
# from firebase import firebase

#setup connections
ser=serial.Serial('/dev/ttyUSB0',9600)
time.sleep(1)
ser.flushInput()
#firebase = firebase.FirebaseApplication('https://patient-monitoring-syste-6132a.firebaseio.com/')

now=datetime.now()



###############################################################################
# Parameters and global variables
dataAr=[0,0,0,0,0,0,0,0]
new_temp=25
new_lux=25
us1_bp_range=[0,280]
us2_bp_range=[0,280]
toco_range=[0,100]
ecg_range=[0,100]
spo2_range=[90,110]
art_range=[40,180]
resp_range=[20,200]
temp_c=0
lux=0

# Parameters
millis=0;
prev=0;
freq=0;
update_interval = 0.1# Time (ms) between polling/animation updates
max_elements = 200     # Maximum number of elements to store in plot lists

# Declare global variables
root = None
dfont = None
frame = None
canvas = None
ax1 = None
running=False

###figures
##p1_fig1=figure.Figure()
##p1_fig2=figure.Figure()
##p1_fig3=figure.Figure()
##p1_fig4=figure.Figure()
##p2_fig1=figure.Figure()
##p2_fig2=figure.Figure()
##
###colors



colorArray={"background_color":"Black",
            "spo2_color":"Blue",
            "menu_bar_color":"#a0ccda",
            "us1_color":"blue",
            "us2_color":"red",
            "ecg_color":"green",
            "resp_color":"red",
            "art_color":"red",
            "temp_color":"white",
            "nibp_color":"grey",
            "toco_color":"orange"}

#clr = colorchooser.askcolor(title="background_color")
#colorArray["background_color"]=clr[1]
#clr = colorchooser.askcolor(title="Spo2 Color")
#colorArray["background_color"]=clr[1]

#Gui critical parameters
menu_bar_top_height="30"
name_label_height="30"
p_label_width="150"
special_button_w=130
special_button_h=96
individual_button_w=135
individual_button_h=60
pc_in_monitor_w=60
pc_in_monitor_h=60


#alarms and warning
us_bp_alarm_u=160
us_bp_alarm_l=120

#image_flatmode = PhotoImage(file = r"E:\Aca Folders\Final Year Project\Kv FYP\6.High Level Controller\Rasberry PI\Python Codes\IOT\Position Controller buttons\flatmode.png")

#thread parameters
##threadUploadFirebase
##threadUploadFirebase
uploadEnable=False
serialEnable=False


class MyApp(Tk):
    def __init__(self):
        print("myapp init..")
        Tk.__init__(self)
        container = ttk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        self.frames = {}
        for F in (PageOne, PageTwo,PagePC,PageSettings):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='NSEW')
        self.show_frame(PageOne)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def _destroy(event):
        #global threadUploadFirebase
        #global threadSerialRead
        global uploadEnable
        global serialEnable
        print("destroy function has called")
        uploadEnable=False
        serialEnable=False
        #threadUploadFirebase.join()
        pass
        
      
class PageOne(ttk.Frame):
    label_date_time=ttk.Label()
    
    def __init__(self, parent, controller):
        self.controller = controller
        ttk.Frame.__init__(self, parent)
        self.make_widget()
        self.label_date_time.after(1000, self.refresh_label)

    def make_widget(self):
        global colorArray
        global p1_fig1,p1_fig2,p1_fig3,p1_fig4
        global line11,line12,line13,line14
        
        self.cvs = Canvas(self, width="800", height="600", background=colorArray.get("background_color"))

        self.cvs.create_rectangle

        #self.cvs.create_rectangle(600, 550, 800, 600, fill="#a0ccda", outline="#a0ccdb")
        label_menu_bar_top=ttk.Label(self, background=colorArray.get("menu_bar_color"))
        label_menu_bar_top.place(x=0,y=0,width ="800",height=menu_bar_top_height)
        
        label_menu_bar_bottom=ttk.Label(self, background=colorArray.get("menu_bar_color"))
        label_menu_bar_bottom.place(x=0,y=600-int(menu_bar_top_height),width ="800",height=menu_bar_top_height)
        
        
        label_patient_id=ttk.Label(self, text="ID:", font="Arial 16 bold", state="normal")
        label_patient_id.place(x=0,y=570,width ="50",height=menu_bar_top_height)
        
        label_patient_name=ttk.Label(self, text="Name:", font="Arial 16 bold", state="normal")
        label_patient_name.place(x=175,y=570,width ="75",height=menu_bar_top_height)
        
        label_window_name=ttk.Label(self,text="Multi-Monitor", font="Arial 16 bold", state="normal")
        label_window_name.place(x=300,y=0,width ="180",height=menu_bar_top_height)
        
        self.label_date_time=ttk.Label(self, text=now.strftime("%m/%d %H:%M"), font="Arial 15",background="#a0ccda")
        self.label_date_time.place(x=650,y=0,width ="150",height=menu_bar_top_height)
        
        fig1 = plt.figure(dpi=100,facecolor=colorArray.get("background_color"),tight_layout=True)
        gs1 = gridspec.GridSpec(ncols=1, nrows=4, height_ratios=[4,4,3,4],figure=fig1)
        a1=fig1.add_subplot(gs1[0,0],facecolor=colorArray.get("background_color"))
        a1.set_ylim(ecg_range)
        #a1.set_ylabel('CPU Temperature', color=colorArray.get("ecg_color"))
        #a1.set_xlabel('x',color=colorArray.get("background_color"))
        a1.tick_params(axis='y', labelcolor=colorArray.get("ecg_color"))
        line11,=a1.plot(xs, ecgs, linewidth=2, color=colorArray.get("ecg_color"))
        
        a2=fig1.add_subplot(gs1[1,0],facecolor=colorArray.get("background_color"))
        a2.set_ylim(spo2_range)
        #a2.set_ylabel('CPU Temperature', color=colorArray.get("spo2_color"))
        #a2.set_xlabel('x',color=colorArray.get("background_color"))
        a2.tick_params(axis='y', labelcolor=colorArray.get("spo2_color"))
        line12,=a2.plot(xs, spo2, linewidth=2, color=colorArray.get("spo2_color"))
        
        a3=fig1.add_subplot(gs1[2,0],facecolor=colorArray.get("background_color"))
        a3.set_ylim(art_range)
        #a3.set_ylabel('CPU Temperature', color=colorArray.get("art_color"))
        #a3.set_xlabel('x',color=colorArray.get("background_color"))
        a3.tick_params(axis='y', labelcolor=colorArray.get("art_color"))
        line13,=a3.plot(xs, art, linewidth=2, color=colorArray.get("art_color"))

        a4=fig1.add_subplot(gs1[3,0],facecolor=colorArray.get("background_color"))
        
        a4.set_ylim(resp_range)
        #a4.set_ylabel('CPU Temperature', color=colorArray.get("resp_color"))
        #a4.set_xlabel('x',color=colorArray.get("background_color"))
        a4.tick_params(axis='y', labelcolor=colorArray.get("resp_color"))
        line14,=a4.plot(xs, resp, linewidth=2, color=colorArray.get("resp_color"))

        #fig1, (a1, a2,a3,a4) = plt.subplots(nrows=4, sharex=True)
        plt.subplots_adjust(left=0.1)
        
        canvas = FigureCanvasTkAgg(fig1,self)
        canvas.draw()
        canvas_fig1 = canvas.get_tk_widget()
        canvas_fig1.place(x=0,y=30,width="600",height="450")

        label_a1_name=ttk.Label(self, text="ECG I", font="Arial 9", state="normal",
                                 background=colorArray.get("background_color"),foreground=colorArray.get("ecg_color"),
                                 )
        label_a1_name.place(x=70,y=30,width ="50",height="20")

        label_a2_name=ttk.Label(self, text="Pleth:", font="Arial 9", state="normal",
                                 background=colorArray.get("background_color"),foreground=colorArray.get("spo2_color"),
                                 )
        label_a2_name.place(x=70,y=155,width ="50",height="20")

        label_a3_name=ttk.Label(self, text="Art", font="Arial 9", state="normal",
                                 background=colorArray.get("background_color"),foreground=colorArray.get("art_color"),
                                 )
        label_a3_name.place(x=70,y=270,width ="50",height="20")

        label_a4_name=ttk.Label(self, text="Imped:", font="Arial 9", state="normal",
                                 background=colorArray.get("background_color"),foreground=colorArray.get("resp_color"),
                                 )
        label_a4_name.place(x=70,y=360,width ="50",height="20")
        
        
        label_ecg_name=ttk.Label(self,text="ECG", font="Arial 16 bold", state="normal",
                                 borderwidth=2,relief="solid",
                                 background=colorArray.get("background_color"),
                                 foreground=colorArray.get("ecg_color"))
        label_ecg_name.place(x=600,y=int(menu_bar_top_height),width =p_label_width,height=name_label_height)
        self.label_ecg_data=ttk.Label(self, text='65' ,background=colorArray.get("background_color"),
                                 foreground=colorArray.get("ecg_color"), font="Arial 30 bold",
                                 borderwidth=2, relief="solid")
        self.label_ecg_data.place(x=600,y=int(menu_bar_top_height)+int(name_label_height),width =p_label_width,height=str(100-int(name_label_height)))

        
        label_sp02_name=ttk.Label(self, text="SpO2", font="Arial 16 bold", state="normal",
                                  background=colorArray.get("background_color"),foreground=colorArray.get("spo2_color"),
                                  borderwidth=2, relief="solid")
        label_sp02_name.place(x=600,y=100+int(menu_bar_top_height),width =str(int(p_label_width)/2),height=name_label_height)
        self.label_sp02_data=ttk.Label(self, text='98', font="Arial 30 bold",background=colorArray.get("background_color"),
                                  foreground=colorArray.get("spo2_color"),borderwidth=2, relief="solid")
        self.label_sp02_data.place(x=600,y=100+int(menu_bar_top_height)+int(name_label_height),
                              width =str(int(p_label_width)/2),height=str(100-int(name_label_height)))

        label_pr_name=ttk.Label(self, text="PR", font="Arial 16", state="normal",
                                  background=colorArray.get("background_color"),foreground=colorArray.get("spo2_color"),
                                  borderwidth=2, relief="solid")
        label_pr_name.place(x=600+int(p_label_width)/2,y=100+int(menu_bar_top_height),width =str(int(p_label_width)/2),height=name_label_height)
        self.label_pr_data=ttk.Label(self, text='60', font="Arial 25 bold",background=colorArray.get("background_color"),
                                  foreground=colorArray.get("spo2_color"),borderwidth=2, relief="solid")
        self.label_pr_data.place(x=600+int(p_label_width)/2,y=100+int(menu_bar_top_height)+int(name_label_height),
                              width =str(int(p_label_width)/2),height=str(100-int(name_label_height)))
                
        label_art_name=ttk.Label(self, text="Art", font="Arial 10 bold", state="normal",
                                 background=colorArray.get("background_color"),foreground=colorArray.get("art_color"),
                                 borderwidth=2, relief="solid")
        label_art_name.place(x=600,y=230,width =p_label_width,height="20")
        self.label_art_data=ttk.Label(self, text='125/95(95)', font="Arial 20 bold",background=colorArray.get("background_color"),
                                 foreground=colorArray.get("art_color"),borderwidth=2, relief="solid")
        self.label_art_data.place(x=600,y=250,width =p_label_width,height="50")
        
        label_resp_name=ttk.Label(self, text="Resp", font="Arial 16 bold",background=colorArray.get("background_color"),
                                  foreground=colorArray.get("resp_color"), state="normal",borderwidth=2, relief="solid")
        label_resp_name.place(x=600,y=300,width =p_label_width,height=name_label_height)
        self.label_resp_data=ttk.Label(self, text='70', font="Arial 30 bold",background=colorArray.get("background_color"),
                                  foreground=colorArray.get("resp_color"),borderwidth=2, relief="solid")
        self.label_resp_data.place(x=600,y=330,width =p_label_width,height=str(100-int(name_label_height)))
        
        label_nibp_name=ttk.Label(self, text="NIBP", font="Arial 16 bold",background=colorArray.get("background_color"),
                                  foreground=colorArray.get("nibp_color"), state="normal",borderwidth=2, relief="solid")
        label_nibp_name.place(x=600,y=400,width =p_label_width,height=name_label_height)
        self.label_nibp_data=ttk.Label(self, text='120/65(92)', font="Arial 20 bold",
                                  background=colorArray.get("background_color"),foreground=colorArray.get("nibp_color"),
                                  borderwidth=2, relief="solid")
        self.label_nibp_data.place(x=600,y=430,width =p_label_width,height=str(100-int(name_label_height)))
        
        label_temp_name=ttk.Label(self, text="Temp", font="Arial 16",background=colorArray.get("background_color"),
                                  foreground=colorArray.get("temp_color"), state="normal",borderwidth=2, relief="solid")
        label_temp_name.place(x=0,y=450,width ="110",height="30")
        self.label_temp_data=ttk.Label(self, text="50.2", font="Arial 16 bold",background=colorArray.get("background_color"),
                                  foreground=colorArray.get("temp_color"),borderwidth=2, relief="solid")
        self.label_temp_data.place(x=0,y=480,width ="110",height="80")

        label_pa_name=ttk.Label(self, text="Weight(Kg)", font="Arial 10 bold",background=colorArray.get("background_color"),
                                  foreground=colorArray.get("temp_color"),borderwidth=2, relief="solid")
        label_pa_name.place(x=600,y=500,width =p_label_width,height="20")

        self.label_pa_data=ttk.Label(self, text="85", font="Arial 14 bold",background=colorArray.get("background_color"),
                                  foreground=colorArray.get("temp_color"),borderwidth=2, relief="solid")
        self.label_pa_data.place(x=600,y=520,width =p_label_width,height="40")

        label_pc_buttons=ttk.Label(self,background=colorArray.get("background_color"),
                                  borderwidth=2, relief="solid")
        label_pc_buttons.place(x=110,y=450,width ="490",height="110")
        
##        label_NIBP_List_name=ttk.Label(self, text="NIBP List", font="Arial 16",background=colorArray.get("background_color"),
##                                       foreground=colorArray.get("nibp_color"), state="normal",
##                                       borderwidth=2, relief="solid")
##        label_NIBP_List_name.place(x=250,y=450,width ="100",height="30")
##        label_NIBP_List_data=ttk.Label(self, text='120/65 (92)',font="Arial 16 bold",
##                                       background=colorArray.get("background_color"),foreground=colorArray.get("nibp_color"),
##                                       borderwidth=2, relief="solid")
##        label_NIBP_List_data.place(x=300,y=500,width ="150",height="50")

        
        

        # Menu bar

        label_side_menu=ttk.Label(self, state="normal", background=colorArray.get("menu_bar_color"),
                                  borderwidth=2, relief="solid")
        label_side_menu.place(x=755,y=30,width ="45",height="540")
        

        btnMultiMonitor = Button(self, text="MM", font="Arial 16",
                           command=lambda: self.controller.show_frame(PageOne),
                           bg=colorArray.get("menu_bar_color")
                           )
        btnMultiMonitor .place(x=755, y=30, width="45", height="45")

        btnFetalMonitor = Button(self, text="FM", font="Arial 16",
                           command=lambda: self.controller.show_frame(PageTwo),
                           bg=colorArray.get("menu_bar_color")
                           )
        btnFetalMonitor .place(x=755, y=75, width="45", height="45")

        btnPositionController = Button(self, text="PC", font="Arial 16",
                           command=lambda: self.controller.show_frame(PagePC),
                           bg=colorArray.get("menu_bar_color")
                           )
        btnPositionController .place(x=755, y=120, width="45", height="45")

        btnSettings = Button(self, text="SE", font="Arial 16",
                           command=lambda: self.controller.show_frame(PageSettings),
                           bg=colorArray.get("menu_bar_color")
                           )
        btnSettings .place(x=755, y=165, width="45", height="45")

        btnUpload = Button(self, text="^", font="Arial 30 bold",
                           command=lambda: self.controller.show_frame(PageSettings),
                           bg=colorArray.get("menu_bar_color")
                           )
        btnUpload .place(x=755, y=525, width="45", height="45")

        #Bed_Position_Buttons
        btnFlat = Button(self, text="FM", font="Arial 16",
                           command=lambda: self.controller.show_frame(PageOne),
                           bg=colorArray.get("menu_bar_color")
                           )
        btnFlat .place(x=140, y=490, width=str(pc_in_monitor_w), height=str(pc_in_monitor_h))

        btnWheelchair = Button(self, text="WC", font="Arial 16",
                           command=lambda: self.controller.show_frame(PageTwo),
                           bg=colorArray.get("menu_bar_color")
                           )
        btnWheelchair .place(x=230, y=490, width=str(pc_in_monitor_w), height=str(pc_in_monitor_h))

        btnTendelenburg = Button(self, text="T", font="Arial 16",
                           command=lambda: self.controller.show_frame(PagePC),
                           bg=colorArray.get("menu_bar_color")
                           )
        btnTendelenburg .place(x=320, y=490, width=str(pc_in_monitor_w), height=str(pc_in_monitor_h))

        btnReverseTendelenburg = Button(self, text="RT", font="Arial 16",
                           command=lambda: self.controller.show_frame(PageSettings),
                           bg=colorArray.get("menu_bar_color")
                           )
        btnReverseTendelenburg .place(x=410, y=490, width=str(pc_in_monitor_w), height=str(pc_in_monitor_h))

        btn30DegreeBackrest = Button(self, text="30DB", font="Arial 16",
                           command=lambda: self.controller.show_frame(PageSettings),
                           bg=colorArray.get("menu_bar_color")
                           )
        btn30DegreeBackrest .place(x=500, y=490, width=str(pc_in_monitor_w), height=str(pc_in_monitor_h))

        

        
##        button_bg_color =ttk.Button(self, text='B',
##                             command=lambda: self.color_selecter("background_color"))
##        button_bg_color.place(x=0, y=550, width="10", height="10")

        self.cvs.pack()

        def change_page(self):
            pass

    def refresh_label(self):
        """ refresh the content of the label every second """
        # increment the time
        # display the new time
        now=datetime.now()
        self.label_date_time.configure(text=now.strftime("%m/%d %H:%M"))
        self.label_ecg_data.configure(text=str(dataAr[3]))
        self.label_sp02_data.configure(text=str(dataAr[4]))
        self.label_resp_data.configure(text=str(dataAr[6]))
        # request tkinter to call self.refresh after 1s (the delay is given in ms)
        self.label_date_time.after(5000, self.refresh_label)
        #print("abc")

    def _destroy(event):
        #global threadUploadFirebase
        #global threadSerialRead
        global uploadEnable
        global serialEnable
        print("destroy function has called")
        uploadEnable=False
        serialEnable=False
        #threadUploadFirebase.join()
        pass
        
    def color_selecter(self,color_base):
        global colorArray
        clr = colorchooser.askcolor(title="select color")
        #root.configure(background=clr[1])
        colorArray[color_base]=clr[1]
        self.cvs.configure(background=colorArray.get("background_color"))


class PageTwo(ttk.Frame):
    def __init__(self, parent, controller):
        print("Page two init..")
        self.controller = controller  
        ttk.Frame.__init__(self, parent)
        self.make_widget()
        self.label_date_time.after(10000, self.refresh_label)

    def make_widget(self):
        #colors
        global colorArray

        #animation
        global p2_fig1
        global p2_fig2
        global line1
        global line2
        global line3
        
        self.cvs = Canvas(self, width="800", height="600", background=colorArray.get("background_color"))

        label_menu_bar_top=ttk.Label(self, background="#a0ccda")
        label_menu_bar_top.place(x=0,y=0,width ="800",height=menu_bar_top_height)
        
        label_menu_bar_bottom=ttk.Label(self, background="#a0ccda")
        label_menu_bar_bottom.place(x=0,y=600-int(menu_bar_top_height),width ="800",height=menu_bar_top_height)
        
        
        label_patient_id=ttk.Label(self, text="ID:", font="Arial 16 bold", state="normal")
        label_patient_id.place(x=0,y=570,width ="50",height=menu_bar_top_height)
        
        label_patient_name=ttk.Label(self, text="Name:", font="Arial 16 bold", state="normal")
        label_patient_name.place(x=175,y=570,width ="75",height=menu_bar_top_height)
        
        label_window_name=ttk.Label(self,text="Fetal-Monitor", font="Arial 16 bold", state="normal")
        label_window_name.place(x=300,y=0,width ="180",height=menu_bar_top_height)
        
        self.label_date_time=ttk.Label(self, text='09/22  12:30 AM', font="Arial 15",background="#a0ccda")
        self.label_date_time.place(x=650,y=0,width ="150",height=menu_bar_top_height)
        
        fig2 = plt.figure(facecolor=colorArray.get("background_color"),edgecolor=colorArray.get("background_color"),tight_layout=True)
        gs2= gridspec.GridSpec(ncols=1, nrows=2, height_ratios=[6,3],figure=fig2)
        a21=fig2.add_subplot(gs2[0,0],facecolor=colorArray.get("background_color"))
        a22=a21.twinx()

        a_def1=a21.twinx()
        a_def2=a21.twinx()
        a_def1.plot(xs, [us_bp_alarm_u]*max_elements, color='C4', linestyle='--')
        a_def1.set_ylim(us1_bp_range)
        a_def2.plot(xs, [us_bp_alarm_l]*max_elements, color='C4', linestyle='--')
        a_def2.set_ylim(us1_bp_range)
        
        a21.clear()
        #a21.set_ylabel(None, color=colorArray.get("us1_color"))
        a21.set_ylim(us1_bp_range)
        a21.tick_params(axis='y', labelcolor=colorArray.get("us1_color"))
        line1,=a21.plot(xs, us1, linewidth=2, color=colorArray.get("us1_color"))
        #a1.plot([1,2,3,4,5,6,7,8],[5,6,1,4,7,8,3,4])
        
        a22.clear()
        a22.set_ylim(us2_bp_range)
        #a22.set_ylabel(None, color=colorArray.get("us2_color"))
        a22.tick_params(axis='y', labelcolor=colorArray.get("us2_color"))
        line2,=a22.plot(xs, us2, linewidth=2, color=colorArray.get("us2_color"))
        
        #a21.spines["top"].set_visible(False)
        a22.spines["left"].set_color(colorArray.get("us2_color"))
        a22.spines["left"].set_color(colorArray.get("us2_color"))

##        a22.spines['top'].set_color(colorArray.get("toco_color"))
##        a22.spines['bottom'].set_color(colorArray.get("toco_color"))
##        a22.spines['left'].set_color(colorArray.get("toco_color"))
##        a22.spines['right'].set_color(colorArray.get("toco_color"))
        #a21.spines["bottom"].set_visible(False)
        #a21.spines["left"].set_visible(True)
##        a22.spines["top"].set_visible(False)
##        a22.spines["right"].set_visible(True)
##        a22.spines["bottom"].set_visible(False)
##        a22.spines["right"].set_color(colorArray.get("us1_color"))
        #seaborn.despine(left=True, bottom=True, right=True)
        #canvas_p2_fig1 = FigureCanvasTkAgg(p2_fig1, self)
        #canvas.show()
        #canvas_p2_fig1.get_tk_widget().place(x=50,y=50,width="500",height="300")
        
        #p2_fig2 = figure.Figure(figsize=(2, 2),facecolor=colorArray.get("background_color"))
        ax2=fig2.add_subplot(gs2[1,0],facecolor=colorArray.get("background_color"))
        ax2.set_ylim(toco_range)
        ax2.tick_params(axis='y', labelcolor=colorArray.get("toco_color"))
        ax2.spines['top'].set_color(colorArray.get("toco_color"))
        ax2.spines['bottom'].set_color(colorArray.get("toco_color"))
        ax2.spines['left'].set_color(colorArray.get("toco_color"))
        ax2.spines['right'].set_color(colorArray.get("toco_color"))
        #a1.set_facecolor(colorArray.get("background_color"))
        line3,=ax2.plot(xs, tocos, linewidth=2, color=colorArray.get("toco_color"))

        plt.subplots_adjust(left=0.1)
        
        canvas = FigureCanvasTkAgg(fig2,self)
        canvas.draw()
        canvas_fig2 = canvas.get_tk_widget()
        canvas_fig2.place(x=0,y=30,width="630",height="450")


        #self.cvs.create_rectangle(600, 550, 800, 600, foreground="#a0ccda", outline="#a0ccdb")

        #graph_labels
        label_us1_name=ttk.Label(self, text="US1", font="Arial 10 bold", state="normal", background=colorArray.get("background_color"),
                                  foreground=colorArray.get("us1_color"))
        label_us1_name.place(x=65,y=50,width ="50",height="20")

        label_us1_name=ttk.Label(self, text="US2", font="Arial 10 bold", state="normal", background=colorArray.get("background_color"),
                                  foreground=colorArray.get("us2_color"))
        label_us1_name.place(x=530,y=50,width ="50",height="20")

        label_us1_name=ttk.Label(self, text="TOCO", font="Arial 10 bold", state="normal", background=colorArray.get("background_color"),
                                  foreground=colorArray.get("toco_color"))
        label_us1_name.place(x=65,y=320,width ="50",height="20")

        
        #name_label_parameters
        
        label_us1_name=ttk.Label(self, text="US1", font="Arial 25 bold", state="normal", background=colorArray.get("background_color"),
                                  foreground=colorArray.get("us1_color"),borderwidth=2, relief="solid")
        label_us1_name.place(x=600,y=30,width =p_label_width,height="50")
        self.label_us1_data=ttk.Label(self, text='138', font="Arial 40 bold",background=colorArray.get("background_color"),
                                  foreground=colorArray.get("us1_color"),borderwidth=2, relief="solid")
        self.label_us1_data.place(x=600,y=80,width =p_label_width,height="100")
        
        label_us2_name=ttk.Label(self, text="US2", font="Arial 25 bold", state="normal",background=colorArray.get("background_color"),
                                  foreground=colorArray.get("us2_color"),borderwidth=2, relief="solid")
        label_us2_name.place(x=600,y=180,width =p_label_width,height="50")
        self.label_us2_data=ttk.Label(self, text='114', font="Arial 40 bold",background=colorArray.get("background_color"),
                                  foreground=colorArray.get("us2_color"),borderwidth=2, relief="solid")
        self.label_us2_data.place(x=600,y=230,width =p_label_width,height="100")
        
        label_toco_name=ttk.Label(self, text="TOCO", font="Arial 16 bold", state="normal",background=colorArray.get("background_color"),
                                  foreground=colorArray.get("toco_color"),borderwidth=2, relief="solid")
        label_toco_name.place(x=600,y=330,width =p_label_width,height="50")
        self.label_toco_data=ttk.Label(self, text='10', font="Arial 40 bold",background=colorArray.get("background_color"),
                                  foreground=colorArray.get("toco_color"),borderwidth=2, relief="solid")
        self.label_toco_data.place(x=600,y=380,width =p_label_width,height="100")

        label_temp_name=ttk.Label(self, text="Temp", font="Arial 16",background=colorArray.get("background_color"),
                                  foreground=colorArray.get("temp_color"), state="normal",borderwidth=2, relief="solid")
        label_temp_name.place(x=0,y=450,width ="110",height="30")
        self.label_temp_data=ttk.Label(self, text="50.2", font="Arial 16 bold",background=colorArray.get("background_color"),
                                  foreground=colorArray.get("temp_color"),borderwidth=2, relief="solid")
        self.label_temp_data.place(x=0,y=480,width ="110",height="80")

        label_pa_name=ttk.Label(self, text="Weight(Kg)", font="Arial 10 bold",background=colorArray.get("background_color"),
                                  foreground=colorArray.get("temp_color"),borderwidth=2, relief="solid")
        label_pa_name.place(x=600,y=480,width =p_label_width,height="40")

        self.label_pa_data=ttk.Label(self, text="85", font="Arial 14 bold",background=colorArray.get("background_color"),
                                  foreground=colorArray.get("temp_color"),borderwidth=2, relief="solid")
        self.label_pa_data.place(x=600,y=520,width =p_label_width,height="40")

        label_pc_buttons=ttk.Label(self,background=colorArray.get("background_color"),
                                  borderwidth=2, relief="solid")
        label_pc_buttons.place(x=110,y=450,width ="490",height="110")

        
        #Menu Selection Bar

        label_side_menu=ttk.Label(self, state="normal", background=colorArray.get("menu_bar_color"),
                                  borderwidth=2, relief="solid")
        label_side_menu.place(x=755,y=30,width ="45",height="540")
        
        btnMultiMonitor = Button(self, text="MM", font="Arial 16",
                           command=lambda: self.controller.show_frame(PageOne),
                           bg=colorArray.get("menu_bar_color")
                           )
        btnMultiMonitor .place(x=755, y=30, width="45", height="45")

        btnFetalMonitor = Button(self, text="FM", font="Arial 16",
                           command=lambda: self.controller.show_frame(PageTwo),
                           bg=colorArray.get("menu_bar_color")
                           )
        btnFetalMonitor .place(x=755, y=75, width="45", height="45")

        btnPositionController = Button(self, text="PC", font="Arial 16",
                           command=lambda: self.controller.show_frame(PagePC),
                           bg=colorArray.get("menu_bar_color")
                           )
        btnPositionController .place(x=755, y=120, width="45", height="45")

        btnSettings = Button(self, text="SE", font="Arial 16",
                           command=lambda: self.controller.show_frame(PageSettings),
                           bg=colorArray.get("menu_bar_color")
                           )
        btnSettings .place(x=755, y=165, width="45", height="45")

        btnUpload = Button(self, text="^", font="Arial 30 bold",
                           command=lambda: self.controller.show_frame(PageSettings),
                           bg=colorArray.get("menu_bar_color")
                           )
        btnUpload .place(x=755, y=525, width="45", height="45")

         #Bed_Position_Buttons
        self.btnFlat = Button(self, text="FM", font="Arial 16",
                           command=lambda: self.controller.show_frame(PageOne),
                           bg=colorArray.get("menu_bar_color")
                           )
        self.btnFlat .place(x=140, y=490, width=str(pc_in_monitor_w), height=str(pc_in_monitor_h))

        btnWheelchair = Button(self, text="WC", font="Arial 16",
                           command=lambda: self.controller.show_frame(PageTwo),
                           bg=colorArray.get("menu_bar_color")
                           )
        btnWheelchair .place(x=230, y=490, width=str(pc_in_monitor_w), height=str(pc_in_monitor_h))

        btnTendelenburg = Button(self, text="T", font="Arial 16",
                           command=lambda: self.controller.show_frame(PagePC),
                           bg=colorArray.get("menu_bar_color")
                           )
        btnTendelenburg .place(x=320, y=490, width=str(pc_in_monitor_w), height=str(pc_in_monitor_h))

        btnReverseTendelenburg = Button(self, text="RT", font="Arial 16",
                           command=lambda: self.controller.show_frame(PageSettings),
                           bg=colorArray.get("menu_bar_color")
                           )
        btnReverseTendelenburg .place(x=410, y=490, width=str(pc_in_monitor_w), height=str(pc_in_monitor_h))

        btn30DegreeBackrest = Button(self, text="30DB", font="Arial 16",
                           command=lambda: self.controller.show_frame(PageSettings),
                           bg=colorArray.get("menu_bar_color")
                           )
        btn30DegreeBackrest .place(x=500, y=490, width=str(pc_in_monitor_w), height=str(pc_in_monitor_h))


        
        button_bg_color =ttk.Button(self, text='B',
                             command=lambda: self.color_selecter("background_color"))
        button_bg_color.place(x=0, y=550, width="10", height="10")

        self.cvs.pack()

        def change_page(self):
            pass

        self.bind("<Destroy>", self._destroy())

    def refresh_label(self):
        """ refresh the content of the label every second """
        # increment the time
        # display the new time
        now=datetime.now()
        self.label_date_time.configure(text=now.strftime("%m/%d %H:%M"))
        self.label_us1_data.configure(text=str(dataAr[0]))
        self.label_us2_data.configure(text=str(dataAr[1]))
        self.label_toco_data.configure(text=str(dataAr[2]))
        # request tkinter to call self.refresh after 1s (the delay is given in ms)
        self.label_date_time.after(5000, self.refresh_label)
        #print("abc")

    def _destroy(event):
        #global threadUploadFirebase
        #global threadSerialRead
        global uploadEnable
        global serialEnable
        print("destroy function has called")
        uploadEnable=False
        serialEnable=False
        #threadUploadFirebase.join()
        pass

    def color_selecter(self,color_base):
        global colorArray
        clr = colorchooser.askcolor(title="select color")
        #root.configure(background=clr[1])
        colorArray[color_base]=clr[1]
        #self.cvs.configure(background=colorArray.get("background_color"))
        
        

class PagePC(ttk.Frame):
    def __init__(self, parent, controller):
        print("Page PC Menu init..")
        self.controller = controller  
        ttk.Frame.__init__(self, parent)
        self.make_widget()
        self.label_date_time.after(10000, self.refresh_label)

    def make_widget(self):
        #colors

        self.cvs = Canvas(self, width="800", height="600", background=colorArray.get("background_color"))

        label_menu_bar_top=ttk.Label(self, background="#a0ccda")
        label_menu_bar_top.place(x=0,y=0,width ="800",height=menu_bar_top_height)
        
        label_menu_bar_bottom=ttk.Label(self, background="#a0ccda")
        label_menu_bar_bottom.place(x=0,y=600-int(menu_bar_top_height),width ="800",height=menu_bar_top_height)
        
        
        label_patient_id=ttk.Label(self, text="ID:", font="Arial 16 bold", state="normal")
        label_patient_id.place(x=0,y=570,width ="50",height=menu_bar_top_height)
        
        label_patient_name=ttk.Label(self, text="Name:", font="Arial 16 bold", state="normal")
        label_patient_name.place(x=175,y=570,width ="75",height=menu_bar_top_height)
        
        label_window_name=ttk.Label(self,text="Bed Position Control Menu", font="Arial 16 bold", state="normal")
        label_window_name.place(x=250,y=0,width ="280",height=menu_bar_top_height)
        
        self.label_date_time=ttk.Label(self, text='09/22  12:30 AM', font="Arial 15",background="#a0ccda")
        self.label_date_time.place(x=650,y=0,width ="150",height=menu_bar_top_height)

        #self.cvs.create_line(600, 550, 800, 600, fill="#a0ccda", outline="#a0ccdb",width=2)


         #Menu Selection Bar

        label_side_menu=ttk.Label(self, state="normal", background=colorArray.get("menu_bar_color"),
                                  borderwidth=2, relief="solid")
        label_side_menu.place(x=755,y=30,width ="45",height="540")
        
        btnMultiMonitor = Button(self, text="MM", font="Arial 16",
                           command=lambda: self.controller.show_frame(PageOne),
                           bg=colorArray.get("menu_bar_color")
                           )
        btnMultiMonitor .place(x=755, y=30, width="45", height="45")

        btnFetalMonitor = Button(self, text="FM", font="Arial 16",
                           command=lambda: self.controller.show_frame(PageTwo),
                           bg=colorArray.get("menu_bar_color")
                           )
        btnFetalMonitor .place(x=755, y=75, width="45", height="45")

        btnPositionController = Button(self, text="PC", font="Arial 16",
                           command=lambda: self.controller.show_frame(PagePC),
                           bg=colorArray.get("menu_bar_color")
                           )
        btnPositionController .place(x=755, y=120, width="45", height="45")

        btnSettings = Button(self, text="SE", font="Arial 16",
                           command=lambda: self.controller.show_frame(PageSettings),
                           bg=colorArray.get("menu_bar_color")
                           )
        btnSettings .place(x=755, y=165, width="45", height="45")

        
        button_bg_color =ttk.Button(self, text='B',
                             command=lambda: self.color_selecter("background_color"))
        button_bg_color.place(x=0, y=550, width="10", height="10")

        #special buttons

        btnFlat = Button(self, text="Flat Mode", font="Arial 16",
                           command=lambda: self.controller.show_frame(PageOne),
                           bg=colorArray.get("menu_bar_color")
                           )
        btnFlat .place(x=10, y=40, width=str(special_button_w), height=str(special_button_h))

        btnWheelchair = Button(self, text="Wheel Chair", font="Arial 16",
                           command=lambda: self.controller.show_frame(PageTwo),
                           bg=colorArray.get("menu_bar_color")
                           )
        btnWheelchair .place(x=10, y=146, width=str(special_button_w), height=str(special_button_h))

        btnTendelenburg = Button(self, text="Tendelenburg", font="Arial 16",
                           command=lambda: self.controller.show_frame(PagePC),
                           bg=colorArray.get("menu_bar_color")
                           )
        btnTendelenburg .place(x=10, y=252, width=str(special_button_w), height=str(special_button_h))

        btnReverseTendelenburg = Button(self, text="Reverse\nTendelenburg", font="Arial 16",
                           command=lambda: self.controller.show_frame(PageSettings),
                           bg=colorArray.get("menu_bar_color")
                           )
        btnReverseTendelenburg .place(x=10, y=358, width=str(special_button_w), height=str(special_button_h))

        btn30DegreeBackrest = Button(self, text="30\nDegree\nBackrest", font="Arial 16",
                           command=lambda: self.controller.show_frame(PageSettings),
                           bg=colorArray.get("menu_bar_color")
                           )
        btn30DegreeBackrest .place(x=10, y=464, width=str(special_button_w), height=str(special_button_h))

        self.cvs.create_line(150,40,150,560,fill="#a0ccdb")


        #individual_position_control_buttons
        btnLiftUp = Button(self, text="Lift Up", font="Arial 16",
                           command=lambda: self.controller.show_frame(PageOne),
                           bg=colorArray.get("menu_bar_color")
                           )
        btnLiftUp .place(x=170, y=50, width=str(individual_button_w), height=str(individual_button_h))

        btnLiftDown = Button(self, text="Lift Down", font="Arial 16",
                           command=lambda: self.controller.show_frame(PageTwo),
                           bg=colorArray.get("menu_bar_color")
                           )
        btnLiftDown .place(x=170, y=130, width=str(individual_button_w), height=str(individual_button_h))

        btnTiltClockwise = Button(self, text="Tilt\nClockwise", font="Arial 16",
                           command=lambda: self.controller.show_frame(PagePC),
                           bg=colorArray.get("menu_bar_color")
                           )
        btnTiltClockwise .place(x=345, y=50, width=str(individual_button_w), height=str(individual_button_h))

        btnTiltAntiClockwise = Button(self, text="Tilt Anti\nClockwise", font="Arial 16",
                           command=lambda: self.controller.show_frame(PageSettings),
                           bg=colorArray.get("menu_bar_color")
                           )
        btnTiltAntiClockwise .place(x=345, y=130, width=str(individual_button_w), height=str(individual_button_h))

        btnBackrestUp = Button(self, text="Backrest\nUp", font="Arial 16",
                           command=lambda: self.controller.show_frame(PageSettings),
                           bg=colorArray.get("menu_bar_color")
                           )
        btnBackrestUp .place(x=170, y=210, width=str(0.7*individual_button_w), height=str(individual_button_h))

        btnBackrestDown = Button(self, text="Backrest\nDown", font="Arial 16",
                           command=lambda: self.controller.show_frame(PageSettings),
                           bg=colorArray.get("menu_bar_color")
                           )
        btnBackrestDown .place(x=170, y=410, width=str(0.7*individual_button_w), height=str(individual_button_h))

        btnFootrestUp = Button(self, text="Footrest\nUp", font="Arial 16",
                           command=lambda: self.controller.show_frame(PageSettings),
                           bg=colorArray.get("menu_bar_color")
                           )
        btnFootrestUp .place(x=345+40, y=210, width=str(0.7*individual_button_w), height=str(individual_button_h))

        btnFootrestDown = Button(self, text="Footrest\nDown", font="Arial 16",
                           command=lambda: self.controller.show_frame(PageSettings),
                           bg=colorArray.get("menu_bar_color")
                           )
        btnFootrestDown .place(x=345+40, y=410, width=str(0.7*individual_button_w), height=str(individual_button_h))

        btnBaseExtension = Button(self, text="Base\nExtension", font="Arial 16",
                           command=lambda: self.controller.show_frame(PageSettings),
                           bg=colorArray.get("menu_bar_color")
                           )
        btnBaseExtension .place(x=170, y=490, width=str(individual_button_w), height=str(individual_button_h))

        btnBaseContraction = Button(self, text="Base\nContraction", font="Arial 16",
                           command=lambda: self.controller.show_frame(PageSettings),
                           bg=colorArray.get("menu_bar_color")
                           )
        btnBaseContraction .place(x=345, y=490, width=str(individual_button_w), height=str(individual_button_h))

        self.cvs.create_line(500,40,500,560,fill="#a0ccdb")
        
        #extension Position Indicators

        self.cvs.create_rectangle(520,80,730,350,outline="#a0ccdb")

        label_bed_extension=ttk.Label(self, text="Bed Extension", font="Arial 16 bold", state="normal", background="#a0ccdb")
        label_bed_extension.place(x=520,y=50,width ="211",height="30")

        label_backrest_image=ttk.Label(self, font="Arial 16 bold", state="normal")
        label_backrest_image.place(x=590,y=100,width ="70",height="80")

        label_seat_image=ttk.Label(self, font="Arial 16 bold", state="normal")
        label_seat_image.place(x=590,y=185,width ="70",height="70")

        label_footrest_image=ttk.Label(self, font="Arial 16 bold", state="normal")
        label_footrest_image.place(x=590,y=260,width ="70",height="70")

        label_backrest_extension_l_image=ttk.Label(self, font="Arial 16 bold", state="normal")
        label_backrest_extension_l_image.place(x=550,y=100,width ="35",height="80")

        label_seat_extension_l_image=ttk.Label(self, font="Arial 16 bold", state="normal")
        label_seat_extension_l_image.place(x=550,y=185,width ="35",height="70")

        label_backrest_extension_r_image=ttk.Label(self, font="Arial 16 bold", state="normal")
        label_backrest_extension_r_image.place(x=665,y=100,width ="35",height="80")

        label_seat_extension_r_image=ttk.Label(self, font="Arial 16 bold", state="normal")
        label_seat_extension_r_image.place(x=665,y=185,width ="35",height="70")

        

        
        
        button_bg_color =ttk.Button(self, text='B',
                             command=lambda: self.color_selecter("background_color"))
        button_bg_color.place(x=0, y=550, width="10", height="10")

        self.cvs.pack()

        def change_page(self):
            pass
        
    def refresh_label(self):
        """ refresh the content of the label every second """
        # increment the time
        # display the new time
        now=datetime.now()
        self.label_date_time.configure(text=now.strftime("%m/%d %H:%M"))
        # request tkinter to call self.refresh after 1s (the delay is given in ms)
        self.label_date_time.after(5000, self.refresh_label)
        #print("abc")

    def _destroy(event):
        #global threadUploadFirebase
        #global threadSerialRead
        global uploadEnable
        global serialEnable
        print("destroy function has called")
        uploadEnable=False
        serialEnable=False
        #threadUploadFirebase.join()
        pass
        

class PageSettings(ttk.Frame):
    def __init__(self, parent, controller):
        print("Page SeMenu init..")
        self.controller = controller  
        ttk.Frame.__init__(self, parent)
        self.make_widget()
        self.label_date_time.after(10000, self.refresh_label)
        #self.label_patient_id.after(5000, self.refresh_image)

    def make_widget(self):
        #colors
        global colorArray

        self.cvs = Canvas(self, width="800", height="600", background=colorArray.get("background_color"))

        label_menu_bar_top=ttk.Label(self, background="#a0ccda")
        label_menu_bar_top.place(x=0,y=0,width ="800",height=menu_bar_top_height)
        
        label_menu_bar_bottom=ttk.Label(self, background="#a0ccda")
        label_menu_bar_bottom.place(x=0,y=600-int(menu_bar_top_height),width ="800",height=menu_bar_top_height)
        
        
        self.label_patient_id=ttk.Label(self, text="ID:", font="Arial 16 bold", state="normal")
        self.label_patient_id.place(x=0,y=570,width ="50",height=menu_bar_top_height)
        
        label_patient_name=ttk.Label(self, text="Name:", font="Arial 16 bold", state="normal")
        label_patient_name.place(x=175,y=570,width ="75",height=menu_bar_top_height)
        
        label_window_name=ttk.Label(self,text="Settings", font="Arial 16 bold", state="normal")
        label_window_name.place(x=300,y=0,width ="180",height=menu_bar_top_height)
        
        self.label_date_time=ttk.Label(self, text='09/22  12:30 AM', font="Arial 15",background="#a0ccda")
        self.label_date_time.place(x=650,y=0,width ="150",height=menu_bar_top_height)

        #Menu Selection Bar

        label_side_menu=ttk.Label(self, state="normal", background=colorArray.get("menu_bar_color"),
                                  borderwidth=2, relief="solid")
        label_side_menu.place(x=755,y=30,width ="45",height="540")
        
        btnMultiMonitor = Button(self, text="MM", font="Arial 16",
                           command=lambda: self.controller.show_frame(PageOne),
                           bg=colorArray.get("menu_bar_color")
                           )
        btnMultiMonitor .place(x=755, y=30, width="45", height="45")

        btnFetalMonitor = Button(self, text="FM", font="Arial 16",
                           command=lambda: self.controller.show_frame(PageTwo),
                           bg=colorArray.get("menu_bar_color")
                           )
        btnFetalMonitor .place(x=755, y=75, width="45", height="45")

        btnPositionController = Button(self, text="PC", font="Arial 16",
                           command=lambda: self.controller.show_frame(PagePC),
                           bg=colorArray.get("menu_bar_color")
                           )
        btnPositionController .place(x=755, y=120, width="45", height="45")

        btnSettings = Button(self, text="SE", font="Arial 16",
                           command=lambda: self.controller.show_frame(PageSettings),
                           bg=colorArray.get("menu_bar_color")
                           )
        btnSettings .place(x=755, y=165, width="45", height="45")

        #image
##        buttonImage = Image.open('flatmode.png')
##        buttonPhoto = ImageTk.PhotoImage(buttonImage)
##
##        myButton = ttk.Button(self, image=buttonPhoto)
##        myButton.place(x=755, y=165, width="45", height="45")
##        # assign image to other object
##        myButton.image = buttonPhoto
        
        button_bg_color =ttk.Button(self, text='B',
                             command=lambda: self.color_selecter("background_color"))
        button_bg_color.place(x=0, y=550, width="10", height="10")

        self.cvs.pack()

        

        def change_page(self):
            pass

        self.bind("<Destroy>", self._destroy())

    def refresh_label(self):
        now=datetime.now()
        self.label_date_time.configure(text=now.strftime("%m/%d %H:%M"))
        # request tkinter to call self.refresh after 1s (the delay is given in ms)
        self.label_date_time.after(5000, self.refresh_label)
        #print("abc")
        
    def refresh_image(self):
        self.label_patient_id.configure(image=buttonPhoto)
        # request tkinter to call self.refresh after 1s (the delay is given in ms)
        #self.label_patient_id.after(5000, self.refresh_label)
        #print("abc")

    def _destroy(event):
        #global threadUploadFirebase
        #global threadSerialRead
        global uploadEnable
        global serialEnable
        print("destroy function has called")
        uploadEnable=False
        serialEnable=False
        #threadUploadFirebase.join()
        pass

        
        
# This function is called periodically from FuncAnimation
def animate(i, us1, us2,tocos):
    global time
    global dataAr
    global prev
    millis = int(round(time.time() * 1000))
    freq=1000/(millis-prev)
    prev = millis
    print(freq)
    #dataAr=[random.randint(122,158),random.randint(100,125),random.randint(0,25)+random.randint(40,50)]+dataAr[3:]
    try:
#         dataAr=[random.randint(122,158),random.randint(100,125),random.randint(0,25)+random.randint(40,50)]+dataAr[3:]
        
        #print(dataAr)
#         ser.write(b'P2\n')
        temparray = [int(x) for x in str(ser.readline()).split("^")[1:-1]]
        #print (temparray)
        dataAr=temparray+dataAr[3:]
        l_dataAr=dataAr
    except:
        pass
    #dataAr=[random.randint(122,158),random.randint(100,125),random.randint(0,25)+random.randint(40,50),random.randint(0,100),random.randint(95,100),random.randint(60,120),random.randint(60,140)]   # Update our labels
    #temp_c.set(round(new_temp/1023*5,2))
    #lux.set(new_lux)

    # Append timestamp to x-axis list
    #timestamp = mdates.date2num(dt.datetime.now())
    #xs.append(timestamp)

    # Append sensor data to lists for plotting
    us1.append(round((l_dataAr[0]), 2))
    us2.append(round((l_dataAr[1]), 2))
    tocos.append(round((l_dataAr[2]), 2))

    # Limit lists to a set number of elements
    #xs = xs[-max_elements:]
    us1 = us1[-max_elements:]
    us2 = us2[-max_elements:]
    tocos=tocos[-max_elements:]
    
    line1.set_ydata(us1)
    line2.set_ydata(us2)
    line3.set_ydata(tocos)

    return [line1,line2,line3,]

# This function is called periodically from FuncAnimation
def animate2(i, ecgs, spo2,art,resp):
    global dataAr
    try:
        dataAr=dataAr[0:3]+[random.randint(0,100),random.randint(95,100),random.randint(60,120),random.randint(60,140)]
        l_dataAr=dataAr
        #print(dataAr)
        ser.write(b'P1\n')
        temparray=str(ser.readline()).split("^")
        
    except:
        pass
        
    #dataAr=[random.randint(122,158),random.randint(100,125),random.randint(0,25)+random.randint(40,50),random.randint(0,100),random.randint(95,100),random.randint(60,120),random.randint(60,140)]
    # Append sensor data to lists for plotting
    ecgs.append(round((l_dataAr[3]), 2))
    spo2.append(round((l_dataAr[4]), 2))
    art.append(round((l_dataAr[5]), 2))
    resp.append(round((l_dataAr[6]), 2))

    # Limit lists to a set number of elements
    ecgs = ecgs[-max_elements:]
    spo2 = spo2[-max_elements:]
    art = art[-max_elements:]
    resp = resp[-max_elements:]
    
    line11.set_ydata(ecgs)
    line12.set_ydata(spo2)
    line13.set_ydata(art)
    line14.set_ydata(resp)
    
    return [line11,line12,line13,line14,]

# Dummy function prevents segfault
def _destroy(event):
    #global x
    global uploadEnable
    
    uploadEnable=False
    #x.join()
    pass

def serialRead():
    global dataAr
    while True:
        dataAr[0]=random.randint(122,158)
        dataAr[1]=random.randint(100,125)
        dataAr[2]=random.randint(0,25)+random.randint(40,50)
        dataAr[3]=random.randint(0,100)
        dataAr[4]=random.randint(95,100)
        dataAr[5]=random.randint(60,120)
        dataAr[6]=random.randint(60,140)

def uploadFirebase():
    while uploadEnable:
        global dataAr
        now=datetime.now()
        result = firebase.post('patientMonitor',{'datetime':now.strftime("%d/%m/%Y %H:%M:%S"),'us1':str(dataAr[0]),'us2':str(dataAr[1]),'toco':str(dataAr[2]),'ECG':str(dataAr[3]),'Spo2':str(dataAr[4]),'Art':str(dataAr[5]),'Resp':str(dataAr[6])})

xs = list(range(0, max_elements))
us1 = [0]*max_elements
us2 = [0]*max_elements
tocos=[0]*max_elements
ecgs = [0]*max_elements
spo2 = [0]*max_elements
art = [0]*max_elements
resp = [0]*max_elements


#fig2 = figure.Figure(figsize=(2, 2),facecolor=colorArray.get("background_color"),edgecolor=colorArray.get("background_color"))
fig2 = plt.figure(figsize=(2, 2),facecolor=colorArray.get("background_color"),edgecolor=colorArray.get("background_color"))
gs2= gridspec.GridSpec(ncols=1, nrows=2, height_ratios=[6,3],figure=fig2)
a21=fig2.add_subplot(gs2[0,0],facecolor=colorArray.get("background_color"))
a22=a21.twinx()


line1,=a21.plot(xs, us1, linewidth=2, color=colorArray.get("us1_color"))

line2,=a22.plot(xs, us2, linewidth=2, color=colorArray.get("us2_color"))

ax2=fig2.add_subplot(gs2[1,0],facecolor=colorArray.get("background_color"))
line3,=ax2.plot(xs, tocos, linewidth=2, color=colorArray.get("toco_color"))


#fig1 = figure.Figure(dpi=100,facecolor=colorArray.get("background_color"),tight_layout=False)
fig1 = plt.figure(dpi=100,facecolor=colorArray.get("background_color"),tight_layout=False)
gs1 = gridspec.GridSpec(ncols=1, nrows=4, height_ratios=[4,4,3,4],figure=fig1)
a1=fig1.add_subplot(gs1[0,0])
line11,=a1.plot(xs, ecgs, linewidth=2, color=colorArray.get("ecg_color"))

a2=fig1.add_subplot(gs1[1,0],facecolor=colorArray.get("background_color"))
line12,=a2.plot(xs, spo2, linewidth=2, color=colorArray.get("spo2_color"))

a3=fig1.add_subplot(gs1[2,0],facecolor=colorArray.get("background_color"))
line13,=a3.plot(xs, art, linewidth=2, color=colorArray.get("art_color"))

a4=fig1.add_subplot(gs1[3,0],facecolor=colorArray.get("background_color"))
line14,=a4.plot(xs, resp, linewidth=2, color=colorArray.get("resp_color"))



if __name__ == '__main__':
    
    root = MyApp()
    
    root.title('Patient Monitoring and Bed control system')

#     fargs = (ecgs, spo2,art,resp)
#     ani=animation.FuncAnimation(fig1,
#                                  animate2,
#                                  fargs=fargs,
#                                  interval=update_interval,
#                                  blit=True)
    
    fargs = (us1, us2,tocos)
    ani2=animation.FuncAnimation(fig2, 
                                animate, 
                                fargs=fargs, 
                                interval=update_interval,
                                blit=True)

#     serialEnable=True
#     uploadEnable=True
#     threadSerialRead=threading.Thread(target=serialRead, args=())
#     threadUploadFirebase=threading.Thread(target=uploadFirebase, args=())
#     threadUploadFirebase.start()
    #threadSerialRead.start()
    #app.bind("<Destroy>", app._destroy())

    #PageOne.label_date_time.configure("Text":)
    root.mainloop()
