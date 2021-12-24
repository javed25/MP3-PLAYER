from tkinter import *
from pygame import mixer
from tkinter import filedialog
from tkinter import messagebox as msg
from mutagen.mp3 import MP3
import time
from tkinter import ttk

parentfilelist=[]
current_playing=None
paused=False
current_playing_path=None
a=None
b=None

def slide(x):
    global song_length,song_time,current_playing,current_playing_path,a,b
    a=int(slider.get())
    b=time.strftime("%M:%S",time.gmtime(a))
    mixer.music.load(current_playing_path)
    mixer.music.play(start=a)

def play_time():
    global current_playing_path,seconds,song_length,song_time,a,b,song_length,paused
    song_info=MP3(current_playing_path)
    song_length=song_info.info.length
    song_time=time.strftime("%M:%S",time.gmtime(song_length))
    seconds=mixer.music.get_pos()/1000
    playing_time=time.strftime("%M:%S",time.gmtime(seconds))
    # print(a)
    if paused:
        pass
    elif a!=None:
        b=time.strftime("%M:%S",time.gmtime(a))
        slider.config(value=a)
        status.config(text=f"Time Elapsed : {b} of {song_time}   ")
        slider_label.config(text=f"{b}")
        if a<int(song_length):
            a+=1
    else:
        slider.config(value=seconds)
        status.config(text=f"Time Elapsed : {playing_time} of {song_time}   ")
        slider_label.config(text=f"{playing_time}")

    status.after(1000,play_time)




################## PLAY ,PAUSE AND STOP FUNCTION #################

def stop_song():
    global current_playing_path
    current_playing_path=None
    slider_label.config(text="0")
    status.config(text="")
    slider.config(value=0)
    mixer.music.stop()
    songbox.selection_clear(ACTIVE)
    current_playing_path=None

def pause_song():
    global paused
    if paused==True:
        mixer.music.unpause()
        paused=False
    else:
        mixer.music.pause()
        paused=True

def play_song():
    global paused,position,current_playing,current_playing_path,a,b,song_length
    song=songbox.get(ACTIVE)
    position_tuple=songbox.curselection()
    position=position_tuple[0]
    
    for i in range(len(parentfilelist)):
        if song in parentfilelist[i]:
            mixer.music.load(parentfilelist[i])
            mixer.music.play()
            current_playing_path=parentfilelist[i]
            current_playing=current_playing_path.split("/")
            current_playing=current_playing[-1]
            current_playing=current_playing.replace(".mp3","")
            if paused:
                paused=False
            slider.config(value=0)
            a=None
            b=None
            play_time()
            slider.config(to=int(song_length))
            
                    

def next_song():
    global parentfilelist,position,paused,current_playing,current_playing_path,stop_variable,a,b
    if position==(songbox.size()-1):
        position=0
    else:
        position=position+1
    song1=songbox.get(position)
    for i in range(len(parentfilelist)):
        if song1 in parentfilelist[i]:
            mixer.music.load(parentfilelist[i])
            mixer.music.play()
            current_playing_path=parentfilelist[i]
            current_playing=current_playing_path.split("/")
            current_playing=current_playing[-1]
            current_playing=current_playing.replace(".mp3","")
            songbox.selection_clear(0,END)
            songbox.activate(position)
            songbox.selection_set(position,last=None)
            if paused:
                paused=False
            slider.config(value=0)
            a=None
            b=None
            slider.config(to=song_length)

def previous_song():
    global parentfilelist,position,paused,current_playing,current_playing_path,a,b
    if position==0:
        position=songbox.size()-1
    else:
        position=position-1
    song1=songbox.get(position)
    for i in range(len(parentfilelist)):
        if song1 in parentfilelist[i]:
            mixer.music.load(parentfilelist[i])
            mixer.music.play()
            current_playing_path=parentfilelist[i]
            current_playing=current_playing_path.split("/")
            current_playing=current_playing[-1]
            current_playing=current_playing.replace(".mp3","")
            songbox.selection_clear(0,END)
            songbox.activate(position)
            songbox.selection_set(position,last=None)
            if paused:
                paused=False
            slider.config(value=0)
            a=None
            b=None
            slider.config(to=song_length)


    ################# MENU COMMMANDS #############

def add_one_song():
    global parentfilelist
    filename=filedialog.askopenfilename(initialdir="D:\\MY PYTHON\PROJECTS\\MP3 PLAYER\\SONGS",title="SELECT A SONG",filetypes=(("mp3 files",'*.mp3'),))
    if filename not in parentfilelist:
        parentfilelist.append(filename)
        songname=filename.split("/")
        songname=songname[-1]
        songname=songname.replace(".mp3","")
        songbox.insert(END,songname)

def add_many_songs():
    global parentfilelist
    filename=filedialog.askopenfilenames(initialdir="D:\\MY PYTHON\PROJECTS\\MP3 PLAYER\\SONGS",title="SELECT MULTIPLE SONGS",filetypes=(("mp3 files",'*.mp3'),))
    for i in filename:
        if i not in parentfilelist:
            parentfilelist.append(i)
            songname=i.split("/")
            songname=songname[-1]
            songname=songname.replace(".mp3","")
            songbox.insert(END,songname)
                
def delete():
    global current_playing,parentfilelist,current_playing_path
    print(current_playing)
    temp=songbox.get(ACTIVE)
    songbox.delete(ANCHOR)
    for i in parentfilelist:
        if temp in i:
            parentfilelist.remove(i)
    if current_playing==temp:
        mixer.music.stop()
        current_playing_path=None
        slider_label.config(text="0")
        status.config(text="")
        slider.config(value=0)

def deleteall():
    global parentfilelist,current_playing_path
    songbox.delete(0,END)
    mixer.music.stop()
    parentfilelist=[]
    current_playing_path=None
    slider_label.config(text="0")
    status.config(text="")
    slider.config(value=0)

def volume(x):
    mixer.music.set_volume(volume_slider.get())

root=Tk()
root.title("MP3PLAYER")
root.geometry("600x450")
# root.config(bg="black")

scroll=Scrollbar(root)
scroll.pack(side=RIGHT,fill=Y)

songbox=Listbox(root,yscrollcommand=scroll.set,bg="black",fg="#fcba03",width=60,selectbackground="gray",selectforeground="black")
songbox.pack(pady=12)
scroll.config(command=songbox.yview)
mixer.init()

##################CREATING PHOTO ##############
play=PhotoImage(file="images\\play.png")
pause=PhotoImage(file='images\\pause.png')
back=PhotoImage(file='images/backward.png')
forward=PhotoImage(file="images/forward.png")
stop=PhotoImage(file="images/stop.png")

#########CREATING BUTTONS###########
f=Frame(root)
f.pack()

play_btn=Button(f,image=play,borderwidth=0,command=play_song)
pause_btn=Button(f,image=pause,borderwidth=0,command=pause_song)
stop_btn=Button(f,image=stop,borderwidth=0,command=stop_song)
forward_btn=Button(f,image=forward,borderwidth=0,command=next_song)
back_btn=Button(f,image=back,borderwidth=0,command=previous_song)

back_btn.grid(row=0,column=0,padx=10)
play_btn.grid(row=0,column=1,padx=10)
pause_btn.grid(row=0,column=2,padx=10)
stop_btn.grid(row=0,column=3,padx=10)
forward_btn.grid(row=0,column=4,padx=10)


############CREATING MENU##########
m=Menu(root)
m1=Menu(m,tearoff=0)
m1.add_command(label="ADD ONE SONG TO PLAYLIST",command=add_one_song)
m1.add_command(label="ADDD MULTIPLE SONGS TO PLAYLIST",command=add_many_songs)
m.add_cascade(menu=m1,label="ADD SONGS")

m2=Menu(m,tearoff=0)
m2.add_command(label="DELETE SONG",command=delete)
m2.add_command(label="DELETE ALL SONGS",command=deleteall)
m.add_cascade(menu=m2,label="REMOVE SONGS")

root.config(menu=m)

slider=ttk.Scale(root,from_=0,to=100,orient=HORIZONTAL,value=0,command=slide,length=360)
slider.pack(pady=30)

slider_label=Label(root,text="0")
slider_label.pack(pady=20)

status=Label(root,text="",bd=1,anchor=E,relief="groove")
status.pack(side=BOTTOM,ipady=12,fill=X)


volume_label=LabelFrame(f,text="VOLUME")
volume_label.grid(row=0,column=5,sticky=N,padx=25)

volume_slider=ttk.Scale(volume_label,from_=0,to=1,orient=VERTICAL,value=0.5,command=volume,length=225)
volume_slider.pack(padx=15,side=RIGHT)

root.mainloop()