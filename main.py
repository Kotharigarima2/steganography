from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
from stegano import lsb
from tkVideoPlayer import TkinterVideo
import pygame

pygame.mixer.init()

win = Tk()
win.geometry('700x1100')
win.config(bg='pink')

# Global player
videoplayer = None
audiolabel = None

#ceasor cipher
def encrypt_caesar(plaintext, key):
    try:
        key = int(key)
    except ValueError:
        return plaintext  # Agar key invalid hai to original text return kar do

    result = ""
    for char in plaintext:
        if char.isupper():
            result += chr((ord(char) + key - 65) % 26 + 65)
        elif char.islower():
            result += chr((ord(char) + key - 97) % 26 + 97)
        else:
            result += char
    return result

def decrypt_caesar(ciphertext, key):
    try:
        key = int(key)
    except ValueError:
        return ciphertext

    return encrypt_caesar(ciphertext, -key)

#Buttonfuc
def selecte_img():
    global selecte_file
    selecte_file = filedialog.askopenfilename(initialdir=os.getcwd(),
                                            title='Select file type',
                                            filetypes=(('PNG File','*.png'),('JPG File','*.jpg'),('All Files','*.txt')))
    img = Image.open(selecte_file)
    img = img.resize((200,200))
    img = ImageTk.PhotoImage(img)
    lf1.config(image=img)
    lf1.image = img

def hide_txt():
    global hide_msg
    key = code.get()
    if key == '':
        messagebox.showerror('ERROR', 'No key entered')
    else:
        msg = text1.get(1.0, END)
        e_msg = encrypt_caesar(msg, key)
        hide_msg = lsb.hide(str(selecte_file), e_msg)
        messagebox.showinfo('SUCCESS', 'Msg successfully hidden, save the image')
        code.set('')

def save_img():
    default_path = r"C:\Users\garima kothari\PycharmProjects\steganography\stegno_data"

    # Make sure the directory exists
    if not os.path.exists(default_path):
        os.makedirs(default_path)

    file_path = filedialog.asksaveasfilename(
        initialdir=default_path,
        defaultextension=".png",
        filetypes=(("PNG files", "*.png"), ('JPG File', '*.jpg'), ('All Files', '*.*')),
        title="Save Image As"
    )

    if file_path:
        hide_msg.save(file_path)
        messagebox.showinfo('SAVED', f'Message saved successfully as:\n{file_path}')


def show_data():
    key = code.get()
    if key == '':
        messagebox.showerror('ERROR', 'No key entered')
    else:
        show_msg = lsb.reveal(selecte_file)
        d_msg = decrypt_caesar(show_msg, key)
        text1.delete(1.0, END)
        text1.insert(END, d_msg)
        code.set('')


def selecte_av():
    global videoplayer, audiolabel , is_paused, current_media

    selected_file = filedialog.askopenfilename(initialdir=os.getcwd(),
                                               title='Select file type',
                                               filetypes=(
                                                   ('Media files', '*.mp3 *.mp4'),
                                                   ('All Files', '*.*')))

    # Stop previous media
    if videoplayer:
        videoplayer.stop()
        videoplayer.destroy()
        videoplayer = None

    if audiolabel:
        pygame.mixer.music.stop()
        audiolabel.destroy()
        audiolabel = None

    is_paused = False

    # Play video
    if selected_file.endswith(".mp4"):
        videoplayer = TkinterVideo(master=f3, scaled=True, width=240, height=190)
        videoplayer.place(x=0, y=0)
        videoplayer.load(selected_file)
        videoplayer.play()

    # Play audio
    elif selected_file.endswith(".mp3"):
        pygame.mixer.music.load(selected_file)
        pygame.mixer.music.play()

        audiolabel = Label(f3, text="🎵 Playing Audio...", bg='#E6E6FA', font=("Arial", 10))
        audiolabel.place(x=50, y=80)

    else:
        print("Unsupported file format.")

# def toggle_pause(event=None):
#     global is_paused, videoplayer, current_media
#
#     if current_media == "video" and videoplayer:
#         if is_paused:
#             videoplayer.play()
#         else:
#             videoplayer.pause()
#         is_paused = not is_paused
#
#     elif current_media == "audio":
#         if is_paused:
#             pygame.mixer.music.unpause()
#         else:
#             pygame.mixer.music.pause()
#         is_paused = not is_paused
#
#
# # Bind the spacebar to toggle pause/play
# root.bind("<space>", toggle_pause)
def hide_txtav():
    pass
def save_av():
    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=(("PNG files", "*.png"), ('JPG File', '*.jpg'), ('All Files', '*.txt')),
        title="Save Image As"
    )



def show_data_av():
    pass
#logo
original_logo = Image.open("stego_logo.png")
resized_logo = original_logo.resize((100, 70), Image.ANTIALIAS)
logo = ImageTk.PhotoImage(resized_logo)
Label(win,image=logo,bd=0).place(x=60,y=0)

#heading
Label(win,text='STEGNOGRAPY',font='impack 40 bold',bg='pink',fg='#87CEEB').place(x=180,y=12)

#frams
f1 = Frame(win,width=250,height=200,bg='#E6E6FA',bd=5)
f1.place(x=10,y=80)
lf1 = Label(f1,bg='#E6E6FA')
lf1.place(x=0,y=0)

f2 = Frame(win,width=300,height=230,bg='white',bd=5)
f2.place(x=350,y=80)
text1 = Text(f2,font='ariel 15 bold',bg='white')
text1.place(x=0,y=0,width=290,height=200)

f3 = Frame(win,width=250,height=200,bg='#E6E6FA',bd=5)
f3.place(x=10,y=420)
lf3 = Label(f1,bg='#E6E6FA')
lf3.place(x=0,y=0)

f4 = Frame(win,width=300,height=230,bg='white',bd=5)
f4.place(x=350,y=420)
text2 = Text(f4,font='ariel 15 bold',bg='white')
text2.place(x=0,y=0,width=290,height=200)

#secret
Label(win,text='Enter Secret Key', font='10', fg='purple',bg='pink').place(x=226,y=319)

#entery of key
code = StringVar()
Entry(win,bd=3,textvariable=code,font='impack 10 bold', show='*').place(x=230,y=342)

#buttons
open_button= Button(win, text='Select Image', bg='blue',fg='white', font='ariel 10 bold', cursor='hand2', command=selecte_img)
open_button.place(x='30',y='380')

save_button= Button(win, text='Save Image', bg='blue',fg='white', font='ariel 10 bold', cursor='hand2',command=save_img)
save_button.place(x='160',y='380')

hide_button= Button(win, text='Hide data', bg='blue',fg='white', font='ariel 10 bold', cursor='hand2',command=hide_txt)
hide_button.place(x='400', y='380')

show_button= Button(win, text='Show data', bg='blue',fg='white', font='ariel 10 bold', cursor='hand2',command=show_data)
show_button.place(x='500', y='380')

o_button= Button(win, text='Select Audio/Video', bg='blue',fg='white', font='ariel 10 bold', cursor='hand2', command=selecte_av)
o_button.place(x='30', y='660')

s_button= Button(win, text='Save Audio/Video', bg='blue',fg='white', font='ariel 10 bold', cursor='hand2', command=save_av)
s_button.place(x='200', y='660')

h_button= Button(win, text='Hide data', bg='blue',fg='white', font='ariel 10 bold', cursor='hand2', command=hide_txtav)
h_button.place(x='400', y='660')

sh_button= Button(win, text='Show data', bg='blue',fg='white', font='ariel 10 bold', cursor='hand2', command=show_data_av)
sh_button.place(x='500', y='660')

mainloop()
