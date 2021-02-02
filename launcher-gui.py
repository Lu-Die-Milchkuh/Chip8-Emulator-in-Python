import chip8
import tkinter as tk
from tkinter import Menu, filedialog, Spinbox, Label, Button, messagebox, Frame
import sys
import os

window = tk.Tk()
window.title("Chip8-Launcher")
fullscreen_state = False
ch8 = chip8.Chip8()

icon = tk.PhotoImage(file="icon/pixelCow.png")
window.iconphoto(False, icon)
window.geometry("640x320")

# Im using a frame to "draw" on it so i can later clear the screen easily
main_frame = Frame(window)
main_frame.config(background="black")
main_frame.grid()

menu = Menu(window)


def close():
    main_frame.quit()
    window.quit()
    sys.exit()


def clear_screen():
    global main_frame
    main_frame.destroy()
    main_frame = Frame(window)
    main_frame.config(background="black")
    main_frame.grid()


def select_rom():
    rom_file = filedialog.askopenfilename(initialdir="roms",
                                          filetypes=(("CH8 File", "*.ch8*"), ("all files", "*.*")))
    print(rom_file)
    rom_name = os.path.split(rom_file)[1]
    print("Init Chip8...")
    ch8.__init__()
    print("Init Screen...")
    ch8.init_screen(rom_name)
    print("Loading ROM...")
    if rom_file != "":
        ch8.rom_loader(rom_file)
        print("ROM loaded.")
        print("Running...")
        ch8.run()
    else:
        tk.messagebox.showwarning(title="Error ", message="No File Selected!")


# Work in Progress
def show_memory():
    print("Not done")
    tk.messagebox.showwarning(title="Error 404", message="Coming soon")


# Switch between Fullscreen and windowed mode(re-do in Future)
def fullscreen():
    global fullscreen_state
    if fullscreen_state:
        fullscreen_state = False
        window.attributes("-fullscreen", fullscreen_state)
        window.update()
    else:
        fullscreen_state = True
        window.attributes("-fullscreen", fullscreen_state)
        window.update()


# Creates "Graphics"-Settings.Very basic stuff
def setting_menu():
    scale_label = Label(main_frame, text="Resolution Scale:", fg="white", bg="black").grid(row=0, column=0)
    color1_label = Label(main_frame, text="Change Color1:", fg="white", bg="black").grid(row=6, column=0)
    color2_label = Label(main_frame, text="Change Color2:", fg="white", bg="black").grid(row=8, column=0)

    spinbox_for_scale = Spinbox(main_frame, from_=1, to=10, width=5).grid(row=0, column=4)

    color1_red = Spinbox(main_frame, from_=0, to=255, width=5, textvariable="2").grid(row=6, column=4)
    color1_green = Spinbox(main_frame, from_=0, to=255, width=5).grid(row=6, column=6)
    color1_blue = Spinbox(main_frame, from_=0, to=255, width=5).grid(row=6, column=8)

    color2_red = Spinbox(main_frame, from_=0, to=255, width=5).grid(row=8, column=4)
    color2_green = Spinbox(main_frame, from_=0, to=255, width=5).grid(row=8, column=6)
    color2_blue = Spinbox(main_frame, from_=0, to=255, width=5).grid(row=8, column=8)

    r_label = Label(main_frame, text="Red", fg="red", bg="black").grid(row=2, column=4)
    g_label = Label(main_frame, text="Green", fg="green", bg="black").grid(row=2, column=6)
    b_label = Label(main_frame, text="Blue", fg="blue", bg="black").grid(row=2, column=8)

    save_button = Button(main_frame, text="Save", fg="black", bg="green").grid(row=10, column=10)
    tk.messagebox.showwarning(title="Error 404", message="Not done yet. Im sorry :)")


# Set Custom Sound(not working at the moment)
def set_sound():
    audio_file = filedialog.askopenfilename(initialdir="sound",
                                            filetypes=(("MP3 File", "*.mp3*"), ("all files", "*.*")))
    tk.messagebox.showwarning(title="Error 404", message="Coming soon")


file_item = Menu(menu, tearoff=0)
file_item.add_command(label="Start ROM", command=select_rom)
file_item.add_command(label="Close Launcher", command=close)

debugger = Menu(menu, tearoff=0)
debugger.add_command(label="Show Memory", command=show_memory)

view = Menu(menu, tearoff=0)
view.add_command(label="Fullscreen", command=fullscreen)

settings = Menu(menu, tearoff=0)
settings.add_command(label="Graphics", command=setting_menu)
settings.add_command(label="Custom Sound", command=set_sound)
settings.add_command(label="Controls", command=show_memory)

menu.add_cascade(label="File", menu=file_item)
menu.add_cascade(label="Debug", menu=debugger)
menu.add_cascade(label="View", menu=view)
menu.add_cascade(label="Settings", menu=settings)

window.config(menu=menu, background="black")
window.mainloop()
